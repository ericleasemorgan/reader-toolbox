from setuptools import setup, find_packages

setup(
    name='reader-toolbox',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ 'click', 'datasette', 'requests', 'scipy', 'scikit-learn', 'matplotlib', 'nltk', 'textacy', 'word2vec' ],
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ] }
)