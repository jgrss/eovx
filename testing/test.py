import eovx
from eovx.data import l8_224077_224078_20200518

from geowombat.data import l8_224077_20200518_B2
from geowombat.data import l8_224078_20200518_B2


def main():

    ex = eovx.Extractor(l8_224077_224078_20200518,
                        num_cpus=4)

    df = ex.extract(l8_224077_20200518_B2, use_ray=False, band_names=['blue'])
    print(df)

    # df = ex.extract(l8_224078_20200518_B2)
    # print(df)
    #
    # df = ex.extract([l8_224077_20200518_B2, l8_224078_20200518_B2])
    # print(df)

    # df = ex.extract('/geowombat/data',
    #                 pattern='LC08_L1TP_*B2.TIF',
    #                 use_ray=False,
    #                 use_concurrency=True)
    #
    # print(df)


if __name__ == '__main__':
    main()
