#!/usr/bin/env python

import argparse

import eovx


def main():

    parser = argparse.ArgumentParser(description='Data extraction',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-g', '--geometry', dest='geometry', help='The geometry file', default=None)
    parser.add_argument('-v', '--values', dest='values', help='The raster values', default=None, nargs='+')
    parser.add_argument('-p', '--pattern', dest='pattern', help='The glob search pattern', default=None)
    parser.add_argument('-o', '--outfile', dest='out_file', help='The output file', default=None)
    parser.add_argument('--version', dest='version', help='Show the version', action='store_true')

    args = parser.parse_args()

    if args.version:
        print(eovx.__version__)
        return

    ex = eovx.Extractor(args.geometry)
    df = ex.extract(args.values[0] if len(args.values) == 1 else args.values,
                    pattern=args.pattern)

    if str(args.out_file).lower().endswith('.gpkg'):
        df.to_file(args.out_file, driver='GPKG')
    elif str(args.out_file).lower().endswith('.shp'):
        df.to_file(args.out_file, driver='ESRI Shapefile')


if __name__ == '__main__':
    main()
