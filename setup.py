from setuptools import setup, find_packages

setup(
    name='reader-toolbox',
    version='0.1.01',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ 'click<7.2.0,>=7.1.1', 'datasette', 'requests', 'scipy', 'scikit-learn', 'matplotlib', 'nltk', 'textacy', 'gensim<=3.8.3', 'pyLDAvis' ],
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ] }
)