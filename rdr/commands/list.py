
# require
from rdr import *
from configparser import ConfigParser

# list
@click.command()
@click.argument( 'location' )
def list( location ) :

	"""List contents of the library at the given LOCATION"""

	# configure
	TSV = '/catalog/catalog.tsv'
	
	# get locations of local and remote libraries
	directory      = pathlib.Path( click.get_app_dir( APPLICATION ) )
	file           = directory / CONFIGURATION
	configurations = ConfigParser()
	configurations.read( str( file ) )
	remoteLibrary  = configurations[ 'REMOTE' ][ 'remotelibrary' ] 
	localLibrary   = configurations[ 'LOCAL' ][ 'locallibrary' ] 

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

