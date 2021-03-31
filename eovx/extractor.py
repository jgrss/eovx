from pathlib import Path

import geowombat as gw
import ray
from ray.util.dask import ray_dask_get
import dask
import pandas as pd
import geopandas as gpd
from tqdm import tqdm


class RasterExtractor(object):

    def extract_raster_values(self, values, **kwargs):

        with dask.config.set(scheduler=ray_dask_get):

            with gw.open(values, **kwargs) as src:

                df = gw.extract(src.transpose('band', 'y', 'x'),
                                self.geometry.to_crs(src.crs),
                                n_jobs=self.num_cpus)

        return df

    def extract_by_path(self, values_parent, pattern, **kwargs):

        df_list = []

        values_list = list(Path(values_parent).rglob(pattern))

        with dask.config.set(scheduler=ray_dask_get):

            for values in tqdm(values_list, total=len(values_list)):

                with gw.open(values, **kwargs) as src:

                    bounds = self.geometry.to_crs(src.crs).total_bounds.tolist()
                    left, bottom, right, top = bounds

                    if src.gw.bounds_overlay(tuple(bounds)):

                        values_df = self.geometry.to_crs(src.crs).cx[left:right, bottom:top]

                        if not values_df.empty:

                            dfs = gw.extract(src.transpose('band', 'y', 'x'),
                                             values_df,
                                             n_jobs=self.num_cpus)

                            df_list.append(dfs)

        df = pd.concat(df_list, axis=0)

        return df.drop_duplicates().reset_index()


class BaseExtractor(RasterExtractor):

    @staticmethod
    def validate_geometry(geometry):

        if Path(geometry).is_file():
            return gpd.read_file(geometry)
        elif isinstance(geometry, gpd.GeoDataFrame):
            return geometry
        else:
            raise TypeError('The geometry must be a file or a GeoDataFrame.')

    @staticmethod
    def validate_values(values):

        if isinstance(values, list):
            return 'list'
        elif isinstance(values, tuple):
            return 'list'
        elif Path(values).is_file():
            return 'file'
        elif Path(values).is_dir():
            return 'dir'
        else:
            raise NameError('The values must be a directory, file, or list of files')

    def extract(self, values, pattern=None, chunks=1024):

        """
        Extracts raster values

        Args:
            values (str | Path | list): Either a directory path or a full path to a raster.
            pattern (Optional[str]): A glob file pattern. Only used if ``values`` is a directory.
            chunks (Optional[int]): The chunk size.
        """

        if self.geometry.empty:
            raise ValueError('The GeoDataFrame is empty.')

        values_type = self.validate_values(values)

        ray.shutdown()
        ray.init(num_cpus=self.num_cpus)

        if values_type == 'file':
            df = self.extract_raster_values(values, chunks=chunks)
        elif values_type == 'list':
            df = self.extract_raster_values(values, mosaic=True, chunks=chunks)
        elif values_type == 'dir':
            df = self.extract_by_path(values, pattern, chunks=chunks)

        ray.shutdown()

        return df


class Extractor(BaseExtractor):

    def __init__(self, geometry, num_cpus=1):

        self.geometry = self.validate_geometry(geometry)
        self.num_cpus = num_cpus
