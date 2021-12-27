from setuptools import setup, find_packages

setup(
    name='reader-toolbox',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ 'srsly<1.1.0,>=1.0.2', 'catalogue<1.1.0,>=0.0.7', 'click', 'datasette', 'requests', 'scipy', 'scikit-learn<0.24.0,>=0.19.0', 'matplotlib', 'nltk', 'pandas', 'textacy==0.10.1', 'word2vec' ],
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ] }
)