
# configure
CARREL = 'test-carrel'

# require
import rdr

def test_ngram() : assert len( rdr.ngrams( CARREL ).split( '\n' ) ) == 112750
	
	