
# configure
ZIPFILE = 'study-carrel.zip'
CARRELS = 'carrels'

# require
from rdr import *

# harvest
@click.command()
@click.argument( 'carrel' )
def download( carrel ) :

	"""Download and install a study carrel from the remote library where CARREL is the name of a study carrel"""
			
	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()

	# read configurations
	configurations.read( str( configurationFile ) )
	remoteLibrary  = configurations[ 'REMOTELIBRARY' ][ 'remotelibrary' ] 
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 

	# get the remote zip file; needs error checking
	click.echo( "Getting study carrel... ", err=True, nl=False )
	response = requests.get( remoteLibrary + '/' + CARRELS + '/' + carrel + '/' + ZIPFILE )
	
	# initialize a temporary file and write to it
	click.echo( "Saving study carrel... ", err=True, nl=False )
	handle = TemporaryFile()
	handle.write( response.content )
	
	# unzip the temporary file and close it, which also deletes it
	click.echo( "Unziping study carrel... ", err=True )
	with ZipFile( handle, 'r' ) as zip : zip.extractall( str( localLibrary ) )
	handle.close()

	# done
	click.echo( f"Done. Now you might want to 'rdr info { carrel }'", err=True )
