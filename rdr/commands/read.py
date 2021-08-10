
# read - open the root of a study carrel in a Web browser

# require
from rdr import *

# read
@click.command( options_metavar='<options>' )
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='output in a more human-readable form')
@click.argument( 'carrel', metavar='<carrel>' )
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
	
		url = REMOTELIBRARY + '/' + CARRELS + '/' + carrel
		open( url )
