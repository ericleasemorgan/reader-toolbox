
# configure
CARREL = 'test-carrel'

# require
import rdr

def test_APPLICATIONDIRECTORY() : assert rdr.APPLICATIONDIRECTORY == 'rdr'
def test_BIBLIOGRAPHYHTML()     : assert rdr.BIBLIOGRAPHYHTML     == 'bibliography.htm'
def test_BIBLIOGRAPHYJSON()     : assert rdr.BIBLIOGRAPHYJSON     == 'bibliography.json'
def test_BIBLIOGRAPHYTEXT()     : assert rdr.BIBLIOGRAPHYTEXT     == 'bibliography.txt'
def test_BIGRAMSCLOUD()         : assert rdr.BIGRAMSCLOUD         == 'bigrams-cloud.png'
def test_CACHE()                : assert rdr.CACHE                == 'cache'
def test_CARRELS()              : assert rdr.CARRELS              == 'carrels'
def test_CLUSTERCUBE()          : assert rdr.CLUSTERCUBE          == 'cluster-cube.png'
def test_CLUSTERDENDROGRAM()    : assert rdr.CLUSTERDENDROGRAM    == 'cluster-dendrogram.png'
def test_COLLOCATIONS()         : assert rdr.COLLOCATIONS         == 'reader.gml'
def test_CONFIGURATIONFILE()    : assert rdr.CONFIGURATIONFILE    == '.rdrrc'
def test_CORPUS()               : assert rdr.CORPUS               == 'reader.txt'
def test_DATABASE()             : assert rdr.DATABASE             == 'reader.db'
def test_DOCUMENTATION()        : assert rdr.DOCUMENTATION        == 'https://reader-toolbox.readthedocs.io'
def test_ENTITIESANY()          : assert rdr.ENTITIESANY          == 'entities-any.png'
def test_ENTITIESGPE()          : assert rdr.ENTITIESGPE          == 'entities-gpe.png'
