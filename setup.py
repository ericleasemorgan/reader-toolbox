from setuptools import setup, find_packages

# install_requires=[ 'srsly<1.1.0,>=1.0.2', 'catalogue<1.1.0,>=0.0.7', 'click', 'datasette', 'requests', 'scipy', 'scikit-learn<0.24.0,>=0.19.0', 'matplotlib', 'nltk', 'pandas', 'textacy==0.10.1', 'word2vec' ],

setup(
    name='reader-toolbox',
    packages=find_packages(),
    include_package_data=True,
	install_requires=[ 'catalogue>=1.0.0', 'click>=7.1.2', 'datasette>=0.55', 'matplotlib>=3.4.2', 'nltk>=3.6.2', 'tika>=1.24', 'pandas>=1.3.2', 'gensim==3.8.3', 'requests>=2.26.0', 'scikit-learn>=0.23.2', 'scipy>=1.7.1', 'srsly>=1.0.5', 'textacy>=0.10.1', 'word2vec>=0.11.1' ],
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ] }
)