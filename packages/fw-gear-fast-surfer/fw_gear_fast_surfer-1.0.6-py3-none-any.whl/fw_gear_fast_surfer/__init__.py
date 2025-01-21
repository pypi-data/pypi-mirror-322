"""The fw_fast-surfer package."""

from importlib.metadata import version

try:
    __version__ = version(__package__)
except:  # noqa: E722
    pass
