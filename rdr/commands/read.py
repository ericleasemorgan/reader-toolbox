
# read - open the root of a study carrel in a Web browser

# require
from rdr import *

# read
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'location', type=click.Choice( [ 'local', 'remote' ], case_sensitive=False ) )
def read( carrel, location ) :

	"""Open <carrel> in your default Web browser where the location is one of:
	
	\b
	  * local - from your local library
	  * remote - from the remote library
	
	Example: rdr read homer
	"""
		
	# require
	from webbrowser import open
	
	if location == 'local' :
	
		localLibrary  = configuration( 'localLibrary' )
		url = 'file://' + str( localLibrary/carrel/INDEX )
		open( url )
		
	elif location == 'remote' :
	
		remoteLibrary = configuration( 'remoteLibrary' )
		url = remoteLibrary + '/' + CARRELS + '/' + carrel
		open( url )
