import eovx
from eovx.data import l8_224077_224078_20200518

from geowombat.data import l8_224077_20200518_B2
from geowombat.data import l8_224078_20200518_B2


def main():

    ex = eovx.Extractor(l8_224077_224078_20200518)

    df = ex.extract(l8_224077_20200518_B2)
    print(df)

    df = ex.extract(l8_224078_20200518_B2)
    print(df)

    df = ex.extract([l8_224077_20200518_B2, l8_224078_20200518_B2])
    print(df)

    df = ex.extract('/geowombat/data',
                    pattern='LC08_L1TP_*B2.TIF')

    print(df)


if __name__ == '__main__':
    main()
