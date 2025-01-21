from importlib import metadata as _metadata

from uv_version.cli import cli  # noqa: F401

try:
    __version__ = _metadata.version('uv-version')

except _metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
