import setuptools
from distutils.core import setup

try:
    import numpy as np
except:
    raise ImportError('NumPy must be installed.')

# Parse the version from the module.
# Source: https://github.com/mapbox/rasterio/blob/master/setup.py
with open('eovx/version.py') as f:
    for line in f:

        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")

            continue

pkg_name = 'eovx'
maintainer = ''
maintainer_email = ''
description = ''
git_url = 'https://github.com/jgrss/eosvault'
download_url = '{GIT}/archive/{PKG}-{VERSION}'.format(GIT=git_url, PKG=pkg_name, VERSION=version)
keywords = []

with open('README.md') as f:
    long_description = f.read()

with open('LICENSE.txt') as f:
    license_file = f.read()

with open('requirements.txt') as f:
    required_packages = f.readlines()


def get_packages():
    return setuptools.find_packages()


def get_console_dict():
    return {'console_scripts': ['eovx=eovx.scripts.eovx:main']}


def setup_package():

    include_dirs = [np.get_include()]

    metadata = dict(name=pkg_name,
                    maintainer=maintainer,
                    maintainer_email=maintainer_email,
                    description=description,
                    license=license_file,
                    version=version,
                    long_description=long_description,
                    packages=get_packages(),
                    keywords=' '.join(keywords),
                    url=git_url,
                    download_url=download_url,
                    install_requires=required_packages,
                    include_dirs=include_dirs,
                    entry_points=get_console_dict(),
                    classifiers=['Intended Audience :: Science/Research',
                                 'License :: MIT',
                                 'Topic :: Scientific :: Remote Sensing',
                                 'Programming Language :: Python :: 3.5',
                                 'Programming Language :: Python :: 3.6',
                                 'Programming Language :: Python :: 3.7',
                                 'Programming Language :: Python :: 3.8'])

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
