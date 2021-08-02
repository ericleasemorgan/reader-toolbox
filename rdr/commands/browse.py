
# require
from rdr import *

# read
@click.command()
@click.argument( 'carrel' )
def browse( carrel ) :

	"""Open a study carrel using Lynx"""

	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 

	url = 'file://' + localLibrary + '/' + carrel
	os.system( 'lynx' + ' ' + url )
