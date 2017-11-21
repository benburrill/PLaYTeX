import collections
import functools
import importlib
import pathlib


def module_path(name):
    spec = importlib.util.find_spec(name)
    try:
        get_filename = spec.loader.get_filename
    except AttributeError:
        raise ImportError(f"Module {name!r} has no filename") from None
    return pathlib.Path(get_filename())


class EntryPoint(collections.namedtuple("EntryPoint", "module attrs")):
    @classmethod
    def parse(cls, ep, default_attrs=None):
        parts = ep.split(":", 1)

        if default_attrs is not None and len(parts) < 2:
            module, = parts
            attrs = default_attrs
        else:
            module, attrs = parts

        return cls(module, tuple(attrs.split(".")))

    def __str__(self):
        return f"{self.module}:{'.'.join(self.attrs)}"
    
    def load(self):
        mod = importlib.import_module(self.module)
        return functools.reduce(getattr, self.attrs, mod)
