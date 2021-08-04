
# read - open the root of a study carrel in a Web browser

# require
from rdr import *

# read
@click.command()
@click.argument( 'carrel' )
def read( carrel ) :

	"""Open the study carrel in a web browser"""
		
	# require
	from webbrowser import open
	
	# initialize
	localLibrary = configuration( 'localLibrary' )

	# create a URL and do the work
	url = 'file://' + str( localLibrary/carrel/INDEX )
	open( url )