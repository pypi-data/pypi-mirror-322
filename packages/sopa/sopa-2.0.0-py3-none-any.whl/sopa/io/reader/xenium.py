import logging
from pathlib import Path

from spatialdata import SpatialData

from ..._constants import ATTRS_KEY, SopaAttrs
from ...utils import ensure_string_channel_names
from .utils import _default_image_kwargs

log = logging.getLogger(__name__)


def xenium(
    path: str | Path,
    image_models_kwargs: dict | None = None,
    imread_kwargs: dict | None = None,
    cells_boundaries: int = False,
    cells_table: int = False,
    **kwargs: int,
) -> SpatialData:
    """Read Xenium data as a `SpatialData` object. For more information, refer to [spatialdata-io](https://spatialdata.scverse.org/projects/io/en/latest/generated/spatialdata_io.xenium.html).

    This function reads the following files:
        - `transcripts.parquet`: transcripts locations and names
        - `experiment.xenium`: metadata file
        - `morphology_focus.ome.tif`: morphology image (or a directory, for recent versions of the Xenium)


    Args:
        path: Path to the Xenium directory containing all the experiment files
        image_models_kwargs: Keyword arguments passed to `spatialdata.models.Image2DModel`.
        imread_kwargs: Keyword arguments passed to `dask_image.imread.imread`.

    Returns:
        A `SpatialData` object representing the Xenium experiment
    """
    from spatialdata_io.readers.xenium import xenium as xenium_spatialdata_io

    image_models_kwargs, imread_kwargs = _default_image_kwargs(image_models_kwargs, imread_kwargs)

    sdata: SpatialData = xenium_spatialdata_io(
        path,
        cells_table=cells_table,
        nucleus_labels=False,
        cells_labels=False,
        cells_as_circles=False,
        nucleus_boundaries=False,
        cells_boundaries=cells_boundaries,
        image_models_kwargs=image_models_kwargs,
        imread_kwargs=imread_kwargs,
        **kwargs,
    )

    if "table" in sdata.tables:
        sdata["table"].uns[ATTRS_KEY]["region"] = "cell_boundaries"
        sdata["table"].obs["region"] = "cell_boundaries"
        sdata["table"].obs["region"] = sdata["table"].obs["region"].astype("category")

    ensure_string_channel_names(sdata)

    ### Add Sopa attributes to detect the spatial elements
    if "morphology_focus" in sdata.images:
        sdata.attrs[SopaAttrs.CELL_SEGMENTATION] = "morphology_focus"

    if "he_image" in sdata.images:
        sdata.attrs[SopaAttrs.TISSUE_SEGMENTATION] = "he_image"

    if "transcripts" in sdata.points:
        sdata.attrs[SopaAttrs.TRANSCRIPTS] = "transcripts"

    return sdata
