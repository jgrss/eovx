# eovx (Earth observation value extraction)

## Python API

```python
import eovx

ex = eovx.Extractor('zones.gpkg')
```

Extract values from all rasters under a path

```python
df = ex.extract('/path_to_rasters', pattern='*.tif')
```

Extract values from a specific raster

```python
df = ex.extract('raster.tif')
```

Extract values from a list of rasters

```python
df = ex.extract(['raster1.tif', 'raster2.tif'])
```

## Command line

Extract values from all rasters under a path

```commandline
eovx --geometry zones.gpkg --values /path_to_rasters --pattern *.tif --outfile raster_values.gpkg
```

Extract values from a specific raster

```commandline
eovx --geometry zones.gpkg --values raster.tif --outfile raster_values.gpkg
```

Extract values from a list of rasters

```commandline
eovx --geometry zones.gpkg --values raster1.tif raster2.tif --outfile raster_values.gpkg
```

## Sample over many raster files in parallel

Sample 8 files in parallel

```commandline
eovx --geometry zones.gpkg --values /path_to_rasters --pattern L1*.tif --chunks 1024 --use-concurrency --num-cpus 8 --band-names blue green red nir swir1 swir2 --outfile raster_values.gpkg
```

Any glob pattern works (here, exclude certain NetCDF files)

```commandline
eovx --geometry zones.gpkg --values /path_to_rasters --pattern *[!_angles].nc --chunks 1024 --use-concurrency --num-cpus 8 --band-names blue green red nir swir1 swir2 --outfile raster_values.gpkg
```
