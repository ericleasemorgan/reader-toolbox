
# read - open the root of a study carrel in a Web browser

# require
from rdr import *

# read
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
def read( carrel ) :

	"""Open <carrel> in your default Web browser
	
	Example: rdr read homer
	"""
		
	# require
	from webbrowser import open
	
	# initialize, create a URL, and do the work
	localLibrary = configuration( 'localLibrary' )
	url = 'file://' + str( localLibrary/carrel/INDEX )
	open( url )