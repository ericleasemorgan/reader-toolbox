
# browse - given a carrel, use lynx to navigate its file system

# require
from rdr import *

@click.command()
@click.argument( 'carrel' )
def browse( carrel ) :

	"""Open a study carrel using Lynx"""

	# configure
	LYNX = 'lynx'
	
	# require
	from os import system
	
	# initialize, create a URL, and do the work
	localLibrary = str( configuration( 'localLibrary' ) )
	url          = 'file://' + localLibrary + '/' + carrel
	system( LYNX + ' ' + url )
