try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .lazy_openslide import napari_get_reader

__all__ = ["napari_get_reader"]
