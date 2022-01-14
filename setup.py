from setuptools import setup, find_packages

setup(
    name='reader-toolbox',
    packages=find_packages(),
    include_package_data=True,
	install_requires=[ 'catalogue>=1.0.0', 'click>=7.1.2', 'datasette>=0.55', 'matplotlib>=3.4.2', 'nltk>=3.6.2', 'tika>=1.24', 'pandas>=1.3.2', 'requests>=2.26.0', 'pytextrank>=3.2.2', 'scikit-learn>=0.23.2', 'scipy>=1.7.1', 'srsly>=1.0.5', 'textacy>=0.12.0' ],
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ] }
)