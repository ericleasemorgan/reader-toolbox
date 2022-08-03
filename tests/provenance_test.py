
# configure
CARREL = 'test-carrel'

# require
import rdr

def test_process() : assert rdr.provenance( CARREL, 'process' )     == 'toolbox'
def test_date()    : assert rdr.provenance( CARREL, 'dateCreated' ) == '2022-08-02'
def test_time()    : assert rdr.provenance( CARREL, 'timeCreated' ) == '08:14'
def test_creator() : assert rdr.provenance( CARREL, 'creator' )     == 'eric'
def test_input()   : assert rdr.provenance( CARREL, 'input' )       == '/Users/eric/Desktop/test-carrel'
