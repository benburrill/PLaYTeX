import abc
import importlib
import hashlib
import pathlib

from playtex.modules import module_path


kinds = {}


def register(name, cls=None):
    def decorator(cls):
        kinds[name] = cls
        return cls

    if cls is None:
        return decorator
    decorator(cls)


def get_kind(name):
    try:
        return kinds[name]
    except KeyError:
        raise LookupError(f"{name} is not a known kind of requirement")


class Metadata:
    def __init__(self, *, player_file=None):
        """
        __init__ may take no arguments to indicate no data.
        Arguments may be added at any time.
        """

        if player_file is not None:
            self.player_file = pathlib.Path(player_file)

    @property
    def home_dir(self):
        return self.player_file.parent


class Requirement(abc.ABC):
    @abc.abstractmethod
    def __init__(self, meta, **kwargs):
        self.meta = meta

    @abc.abstractmethod
    def digest(self)->bytes:
        pass

    @abc.abstractmethod
    def get(self):
        pass

    def __hash__(self):
        return hash(self.digest())


@register("file")
class FileRequirement(Requirement):
    def __init__(self, meta, *, path, mode="rt", give_handle=False):
        self.meta = meta
        self.path = pathlib.Path(path)
        self.mode = mode
        self.give_handle = give_handle

    @property
    def absolute_path(self):
        if self.path.is_absolute():
            return self.path

        home_dir = getattr(self.meta, "home_dir", pathlib.Path())
        return (home_dir / self.path).absolute()

    def digest(self):
        hash = hashlib.md5()
        with open(self.absolute_path, "rb") as file:
            for line in file:
                hash.update(line)
        return hash.digest()

    def get(self):
        handle = open(self.absolute_path, self.mode)
        
        if self.give_handle:
            return handle

        with handle:
            return handle.read()


@register("module")
class ModuleRequirement(FileRequirement):
    def __init__(self, meta, *, name):
        self.meta = meta
        self.name = name

    @property
    def path(self):
        return module_path(self.name)

    def get(self):
        return importlib.import_module(self.name)


@register("literal")
class LiteralRequirement(Requirement):
    def __init__(self, meta, *, value):
        # Convert value into an immutable type where possible, mostly so
        # that the requirement can be hashed.
        if isinstance(value, list):
            value = tuple(value)
        elif isinstance(value, set):
            value = frozenset(value)
        elif isinstance(value, dict):
            raise ValueError("Literal value cannot be a dict")

        self.meta = meta
        self.value = value

    def digest(self):
        ba = bytearray()
        remaining = hash(self.value)
        # add sign bit
        remaining <<= 1
        remaining |= remaining < 0
        remaining = abs(remaining)
        while remaining:
            ba.append(remaining & 0xFF)
            remaining >>= 8
        return bytes(ba)

    def get(self):
        return self.value
