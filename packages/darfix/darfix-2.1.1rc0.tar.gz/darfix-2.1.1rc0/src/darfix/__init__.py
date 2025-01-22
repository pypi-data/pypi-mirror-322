from ._version import __version__  # noqa: F401

from ._config import Config as _Config

config = _Config()
"""Global configuration shared with the whole library"""
