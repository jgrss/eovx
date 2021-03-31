from pathlib import Path
from contextlib import contextmanager
import concurrent.futures

import geowombat as gw
import ray
from ray.util.dask import ray_dask_get
import dask
import pandas as pd
import geopandas as gpd
from tqdm import tqdm


@contextmanager
def _dask_dummy(scheduler=None):
    yield None


@contextmanager
def _futures_dummy(max_workers=None):
    yield None


class RasterExtractor(object):

    def extract_raster_values(self, values, use_ray, num_cpus, **kwargs):

        df = None

        cxt = dask.config.set if use_ray else _dask_dummy

        with cxt(scheduler=ray_dask_get):

            with gw.open(values, **kwargs) as src:

                bounds = self.geometry.to_crs(src.crs).total_bounds.tolist()
                left, bottom, right, top = bounds

                if src.gw.bounds_overlay(tuple(bounds)):

                    values_df = self.geometry.to_crs(src.crs).cx[left:right, bottom:top]

                    if not values_df.empty:

                        df = gw.extract(src.transpose('band', 'y', 'x'),
                                        self.geometry.to_crs(src.crs),
                                        n_jobs=num_cpus)

        return df

    def extract_by_path(self, values_parent, use_ray, use_concurrency, pattern, **kwargs):

        df_list = []

        values_list = list(Path(values_parent).rglob(pattern))

        cxtf = concurrent.futures.ProcessPoolExecutor if use_concurrency else _futures_dummy

        with cxtf(max_workers=self.num_cpus) as executor:

            if use_concurrency:

                futures = (executor.submit(self.extract_raster_values,
                                           values,
                                           use_ray,
                                           1,
                                           **kwargs) for values in values_list)

                for f in tqdm(concurrent.futures.as_completed(futures), total=len(values_list)):
                    res = f.result()
                    df_list.append(res)

            else:

                df_list = [self.extract_raster_values(values,
                                                      use_ray,
                                                      self.num_cpus,
                                                      **kwargs) for values in values_list]

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

    def extract(self, values, pattern=None, use_ray=False, use_concurrency=False, chunks=1024):

        """
        Extracts raster values

        Args:
            values (str | Path | list): Either a directory path or a full path to a raster.
            pattern (Optional[str]): A glob file pattern. Only used if ``values`` is a directory.
            use_ray (Optional[bool]): Whether to use ``ray`` with a ``dask`` configuration.
            use_concurrency (Optional[bool]): Whether to use ``concurrent.futures`` over each raster.
            chunks (Optional[int]): The chunk size.
        """

        if self.geometry.empty:
            raise ValueError('The GeoDataFrame is empty.')

        values_type = self.validate_values(values)

        if use_ray:
            ray.shutdown()
            ray.init(num_cpus=self.num_cpus)

        if values_type == 'file':
            df = self.extract_raster_values(values, use_ray, chunks=chunks)
        elif values_type == 'list':
            df = self.extract_raster_values(values, use_ray, mosaic=True, chunks=chunks)
        elif values_type == 'dir':
            df = self.extract_by_path(values, use_ray, use_concurrency, pattern, chunks=chunks)

        if use_ray:
            ray.shutdown()

        return df


class Extractor(BaseExtractor):

    def __init__(self, geometry, num_cpus=1):

        self.geometry = self.validate_geometry(geometry)
        self.num_cpus = num_cpus
