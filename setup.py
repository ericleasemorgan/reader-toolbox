from setuptools import setup, find_packages

setup(
    name='rdr',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ 'Click', 'requests', 'scipy', 'sklearn', 'matplotlib', 'nltk', 'textacy' ],
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ],
    }
)