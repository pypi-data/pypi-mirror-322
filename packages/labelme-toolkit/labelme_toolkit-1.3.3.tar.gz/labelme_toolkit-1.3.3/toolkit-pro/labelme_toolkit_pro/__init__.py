import importlib.metadata

from . import _cli

__version__ = importlib.metadata.version("labelme_toolkit_pro")

COMMANDS = [getattr(_cli, name) for name in dir(_cli) if not name.startswith("_")]
