
# require
from rdr import *
import webbrowser

# read
@click.command()
@click.argument( 'carrel' )
def read( carrel ) :

	"""Open the study carrel in a web browser"""
		
	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 

	url = 'file://' + localLibrary + '/' + carrel + '/index.htm'
	webbrowser.open( url )