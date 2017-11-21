import collections
import pathlib
import yaml

import playtex.requirements as req
from playtex.requirements import get_kind, ModuleRequirement
from playtex.modules import EntryPoint


def get_requirement(meta, spec):
    if isinstance(spec, collections.Mapping):
        spec = dict(spec)
        kind = spec.pop("kind", "file")
        return req.get_kind(kind)(meta, **spec)
    return req.FileRequirement(meta, path=spec)


Args = collections.namedtuple("Args", "po kw")
def get_arg_requirements(meta, spec):
    po, kw = (), {}

    requires = spec.get("requires", {})
    if isinstance(requires, collections.Mapping):
        kw = {k: get_requirement(meta, v) for k, v in requires.items()}
    else:
        po = tuple(get_requirement(meta, item) for item in requires)

    return Args(po, kw)


class Player:
    def __init__(self, meta, name, entry_point, args):
        self.meta = meta
        self.name = name
        self.entry_point = entry_point
        self.args = args

    @classmethod
    def from_spec(cls, meta, spec, player_name):
        player_spec = spec[player_name]
        entry_point = EntryPoint.parse(player_spec["play"], "play")
        args = get_arg_requirements(meta, player_spec)
        return cls(meta, player_name, entry_point, args)

    @property
    def play_req(self):
        return req.ModuleRequirement(
            self.meta, name=self.entry_point.module
        )

    def play(self):
        return self.entry_point.load()(
            *[arg.get() for arg in self.args.po],
            **{name: arg.get() for name, arg in self.args.kw.items()}
        )

    def freeze(self):
        po, kw = self.args
        return {
            "mod": self.play_req.digest(),
            "po": [item.digest() for item in po],
            "kw": {k: v.digest() for k, v in kw.items()}
        }


class DirMap(collections.MutableMapping):
    """ Mapping for a flat directory of text files """
    def __init__(self, dir, *, encoding="utf-8", errors="strict"):
        self.dir = pathlib.Path(dir)
        self.encoding = encoding
        self.errors = errors

    def path(self, key):
        return self.dir / key

    def __getitem__(self, key):
        try:
            return self.path(key).read_text(self.encoding, self.errors)
        except FileNotFoundError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.dir.mkdir(exist_ok=True)
        self.path(key).write_text(value, self.encoding, self.errors)

    def __delitem__(self, key):
        try:
            self.path(key).unlink()
        except FileNotFoundError:
            raise KeyError(key)

    def __iter__(self):
        for path in self.dir.iterdir():
            yield path.name

    def __len__(self):
        # kinda gross, but I don't really care right now
        return len(tuple(self))


def cache_render(meta, renderer, player, locks, cache):
    renderer = EntryPoint.parse(renderer, "render")
    renderer_hex = req.ModuleRequirement(
        meta, name=renderer.module
    ).digest().hex()
    cache_key = f"{renderer_hex}-{player.name}"

    new_lock = player.freeze()
    if locks.get(player.name, {}) == new_lock:
        try:
            return cache[cache_key]
        except KeyError:
            pass
    else:
        locks[player.name] = new_lock

    result = renderer.load()(player.play())
    cache[cache_key] = result
    return result


def file_render(renderer, player_name, player_file, *, do_cache=False):
    player_file = pathlib.Path(player_file)
    lock_file = pathlib.Path(player_file.parent,
                             f".{player_file.name}.lock")
    cache_dir = pathlib.Path(player_file.parent,
                             f".{player_file.name}-cache")

    meta = req.Metadata(player_file=player_file)
    with open(player_file) as handle:
        spec = yaml.safe_load(handle)
        player = Player.from_spec(meta, spec, player_name)

    if do_cache:
        try:
            with open(lock_file) as handle:
                lock = yaml.safe_load(handle)
        except FileNotFoundError:
            lock = {}
        cache = DirMap(cache_dir)
    else:
        lock, cache = {}, {}

    try:
        return cache_render(meta, renderer, player, lock, cache)
    finally:
        if do_cache:
            with open(lock_file, "w") as handle:
                yaml.safe_dump(lock, handle)
