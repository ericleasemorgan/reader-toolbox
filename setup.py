from setuptools import setup, find_packages

setup(
    name='rdr',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ 'click==7.1.2', 'requests==2.26.0', 'scipy==1.7.1', 'scikit-learn==0.24.2', 'matplotlib==3.4.2', 'nltk==3.6.2', 'textacy==0.11.0', 'gensim<=3.8.3', 'pyLDAvis' ],
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ] }
)