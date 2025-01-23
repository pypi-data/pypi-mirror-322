"""Entry point of the uvicorn_configurable library, collects all exportable items."""

from uvicorn_configurable._version import __version__
from uvicorn_configurable.config import UvicornConfigSection

__all__ = [
    "__version__",
    "UvicornConfigSection",
]
