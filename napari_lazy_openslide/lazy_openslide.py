import dask.array as da
import zarr
from napari_plugin_engine import napari_hook_implementation


@napari_hook_implementation
def napari_get_reader(path):
    """A basic implementation of the napari_get_reader hook specification.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # Don't handle multiple paths
        return None

    if path.endswith(".mzarr"):
        return reader_function
    else:
        return None


def reader_function(path):
    """Takes a path and returns a LayerData tuple where the data is a dask.array.

    Parameters
    ----------
    path : str
        Path to file

    Returns
    -------
    layer_data : list of LayerData tuples
    """
    grp = zarr.open(path, mode="r")

    multiscales = grp.attrs["multiscales"][0]
    pyramid = [
        # da.from_zarr(grp, component=d["path"]) for d in multiscales["datasets"]
        da.from_zarr(grp[d["path"]]) for d in multiscales["datasets"]
    ]
    tmp = {"name": multiscales["name"]}
    return [(pyramid[0], )]
