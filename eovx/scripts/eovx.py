#!/usr/bin/env python

import argparse

import eovx


def main():

    parser = argparse.ArgumentParser(description='Data extraction',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-g', '--geometry', dest='geometry', help='The geometry file', default=None)
    parser.add_argument('-v', '--values', dest='values', help='The raster values', default=None, nargs='+')
    parser.add_argument('-p', '--pattern', dest='pattern', help='The glob search pattern', default=None)
    parser.add_argument('-r', '--use-ray', dest='use_ray', help='Whether to use ray', action='store_true')
    parser.add_argument('-t', '--use-concurrency', dest='use_concurrency', help='Whether to use concurrent.futures', action='store_true')
    parser.add_argument('-n', '--num-cpus', dest='num_cpus', help='The number of CPUs to use for concurrent threading',
                        default=1, type=int)
    parser.add_argument('-c', '--chunks', dest='chunks', help='The chunk size', default=1024, type=int)
    parser.add_argument('-o', '--outfile', dest='out_file', help='The output file', default=None)
    parser.add_argument('--version', dest='version', help='Show the version', action='store_true')

    args = parser.parse_args()

    if args.version:
        print(eovx.__version__)
        return

    ex = eovx.Extractor(args.geometry,
                        num_cpus=args.num_cpus)

    df = ex.extract(args.values[0] if len(args.values) == 1 else args.values,
                    pattern=args.pattern,
                    use_ray=args.use_ray,
                    use_concurrency=args.use_concurrency,
                    chunks=args.chunks)

    if str(args.out_file).lower().endswith('.gpkg'):
        df.to_file(args.out_file, driver='GPKG')
    elif str(args.out_file).lower().endswith('.shp'):
        df.to_file(args.out_file, driver='ESRI Shapefile')


if __name__ == '__main__':
    main()
