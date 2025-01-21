import logging
from functools import partial
from pathlib import Path

import dask.dataframe as dd
import geopandas as gpd
import pandas as pd
from dask.diagnostics import ProgressBar
from spatialdata import SpatialData

from .._constants import SopaFiles, SopaKeys
from ..spatial import assign_transcript_to_cell
from ..utils import add_spatial_element, get_cache_dir, to_intrinsic
from ._patches import Patches2D

log = logging.getLogger(__name__)


class OnDiskTranscriptPatches(Patches2D):
    def __init__(
        self,
        sdata: SpatialData,
        points_key: str,
        patch_width: float,
        patch_overlap: float,
        prior_shapes_key: str | None = None,
        unassigned_value: int | str | None = None,
        min_points_per_patch: int = 4000,
        min_cells_per_patch: int = 1,
        csv_name: str = SopaFiles.TRANSCRIPTS_FILE,
        centroids_csv_name: str = SopaFiles.CENTROIDS_FILE,
        write_cells_centroids: bool = False,
    ):
        super().__init__(sdata, points_key, patch_width, patch_overlap)

        self.points_key = points_key
        self.points = sdata[points_key]

        self.prior_shapes_key = prior_shapes_key
        self.unassigned_value = unassigned_value
        self.min_points_per_patch = min_points_per_patch
        self.min_cells_per_patch = min_cells_per_patch
        self.csv_name = csv_name
        self.centroids_csv_name = centroids_csv_name
        self.write_cells_centroids = write_cells_centroids

        self.cache_dir = get_cache_dir(sdata) / SopaFiles.TRANSCRIPT_CACHE_DIR

    def write(self):
        self.assign_prior_segmentation()

        self.setup_patches_directory()

        patches_geo_df = gpd.GeoDataFrame(geometry=self.polygons)

        if self.write_cells_centroids:
            centroids = self.get_prior_centroids()
            self.write_points(patches_geo_df, centroids, csv_name=self.centroids_csv_name)

        if isinstance(self.points, dd.DataFrame):
            with ProgressBar():
                self.points.map_partitions(partial(self.query_points_partition, patches_geo_df), meta=()).compute()
        else:
            self.write_points(patches_geo_df, self.points)

    def assign_prior_segmentation(self) -> None:
        if self.prior_shapes_key is None:
            return

        if self.prior_shapes_key in self.sdata.shapes:
            assert (
                self.unassigned_value is None
            ), "Unassigned value is not needed when using a prior segmentation based on existing shapes"

            return assign_transcript_to_cell(
                self.sdata, self.points_key, self.prior_shapes_key, self.prior_shapes_key, unassigned_value=0
            )

        assert (
            self.prior_shapes_key in self.points.columns
        ), f"Prior-segmentation column {self.prior_shapes_key} not found in sdata['{self.points_key}']"

        self.points[self.prior_shapes_key] = _assign_prior(self.points[self.prior_shapes_key], self.unassigned_value)

    def get_prior_centroids(self) -> gpd.GeoDataFrame:
        centroids = to_intrinsic(self.sdata, self.prior_shapes_key, self.points).geometry.centroid

        return gpd.GeoDataFrame(
            {
                "x": centroids.geometry.x,
                "y": centroids.geometry.y,
                "z": 0,
                self.prior_shapes_key: range(1, len(centroids) + 1),
            },
            geometry=centroids,
        )

    def add_shapes(self, key_added: str | None = None):
        valid_indices = list(self.valid_indices())

        assert len(valid_indices), "No valid patches found. Check the minimum number of points or cells per patch."

        geo_df = self.as_geodataframe().iloc[valid_indices]
        geo_df[SopaKeys.CACHE_PATH_KEY] = geo_df.index.map(lambda index: str(self.cache_dir / str(index)))
        geo_df[SopaKeys.POINTS_KEY] = self.points_key

        if self.prior_shapes_key:
            geo_df[SopaKeys.PRIOR_SHAPES_KEY] = self.prior_shapes_key

        key_added = key_added or SopaKeys.TRANSCRIPTS_PATCHES

        add_spatial_element(self.sdata, key_added, geo_df)

        log.info(f"{len(valid_indices)} patche(s) were added to sdata['{key_added}']")

    def get_patch_path(self, index: int, csv_name: str | None = None) -> Path:
        return self.cache_dir / str(index) / (csv_name or self.csv_name)

    def setup_patches_directory(self):
        for index in range(len(self)):
            patch_path = self.get_patch_path(index)
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            if patch_path.exists():
                patch_path.unlink()
            if isinstance(self.points, dd.DataFrame):
                pd.DataFrame(columns=self.points.columns).to_csv(patch_path, index=False)

    def valid_indices(self):
        for index in range(len(self)):
            if _check_min_lines(self.get_patch_path(index), self.min_points_per_patch):
                if not self.write_cells_centroids or _check_min_lines(
                    self.get_patch_path(index, csv_name=self.centroids_csv_name), self.min_cells_per_patch
                ):
                    yield index
                    continue

                log.info(f"Patch {index} is out for segmentation (less than {self.min_cells_per_patch} cells).")
                continue

            log.info(f"Patch {index} is out for segmentation (less than {self.min_points_per_patch} transcripts).")

    def query_points_partition(self, patches_gdf: gpd.GeoDataFrame, df: pd.DataFrame) -> pd.DataFrame:
        points_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["x"], df["y"]))
        self.write_points(patches_gdf, points_gdf, mode="a")

    def write_points(
        self, patches_gdf: gpd.GeoDataFrame, points_gdf: gpd.GeoDataFrame, mode="w", csv_name: str | None = None
    ):
        patches_gdf.index.name = "index_right"  # to reuse the index name later
        df_merged: gpd.GeoDataFrame = points_gdf.sjoin(patches_gdf)

        for index, patch_df in df_merged.groupby("index_right"):
            patch_path = self.get_patch_path(index, csv_name=csv_name)
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_df = patch_df.drop(columns=["index_right", "geometry"])
            patch_df.to_csv(patch_path, mode=mode, header=mode == "w", index=False)


def _check_min_lines(path: str, n: int) -> bool:
    if not Path(path).exists():  # empty file are not written at all
        return False
    with open(path, "r") as f:
        for count, _ in enumerate(f):
            if count + 1 >= n:
                return True
        return False


def _assign_prior(series: dd.Series, unassigned_value: int | str | None) -> pd.Series:
    if series.dtype == "string":
        series = series.astype("category")
        series = series.cat.as_known()

        categories = series.cat.categories
        assert unassigned_value in categories, f"Unassigned value {unassigned_value} not in categories"
        categories = categories.delete(categories.get_loc(unassigned_value))
        categories = pd.Index([unassigned_value]).append(categories)

        series = series.cat.reorder_categories(categories)
        return series.cat.codes

    if series.dtype == "int":
        if unassigned_value is None or unassigned_value == 0:
            return series
        return series.replace(int(unassigned_value), 0)

    raise ValueError(f"Invalid dtype {series.dtype} for prior cell ids. Must be int or string.")
