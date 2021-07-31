
# configure

# require
from rdr import *

# read
@click.command()
@click.argument( 'carrel' )
def browse( carrel ) :

	"""Open a study carrel using Lynx"""

	url = 'file://' + LOCALLIBRARY + '/' + carrel
	os.system( 'lynx' + ' ' + url )
