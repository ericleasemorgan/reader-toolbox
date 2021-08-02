
# require
from rdr import *

# list
@click.command()
@click.argument( 'location' )
def list( location ) :

	"""List contents of the library at the given LOCATION"""

	# configure
	TSV = '/catalog/catalog.tsv'
	
	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	remoteLibrary  = configurations[ 'REMOTELIBRARY' ][ 'remotelibrary' ] 
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 

	# local
	if location == 'local' :
		carrels = os.listdir( localLibrary )
		carrels.sort()
		for carrel in carrels : click.echo( carrel )
	
	# remote
	elif ( location == 'remote' ) : click.echo( requests.get( remoteLibrary + TSV ).text )
	
	# error
	else : 
		click.echo( "Error: Unknown value for location: { location }" )
		os.system( 'rdr list --help' )		

