
# configure
CARREL = 'test-carrel'

# require
import rdr

def test_items() : assert rdr.extents( CARREL, 'items' )  == 48
def test_items() : assert rdr.extents( CARREL, 'words' )  == 272735
def test_items() : assert int( rdr.extents( CARREL, 'flesch' ) ) == 76
