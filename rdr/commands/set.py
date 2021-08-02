
# require
from rdr import *

# config
@click.command()
def set() :

	"""Set the current location of your study carrels"""
	
	# configure
	LOCALLIBRARY  = 'reader-library'
	REMOTELIBRARY = 'http://library.distantreader.org'

	# initialize
	configurations       = ConfigParser()
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE

	# look for configuration file
	if not configurationFile.exists() : library = pathlib.Path.cwd() / LOCALLIBRARY
	else :
	
		# get the location of the local library
		configurations.read( str( configurationFile ) )
		library = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ]
	
	# get the desired library location
	click.echo( 'From where do you want to save and read your study carrels? Press enter to accept the default.' )
	library = input( 'Directory [%s]: ' % library ) or library
	library = pathlib.Path( library )

	# try to create the directory and save the configuration
	try : library.mkdir( exist_ok=True )
	except FileNotFoundError : click.echo( "Error: file not found. Are you sure you entered a valid path?", err=True )		
	else :
		applicationDirectory.mkdir( parents=False, exist_ok=True )
		configurations[ "LOCALLIBRARY" ]  = { "locallibrary"  : str( library ) }
		configurations[ "REMOTELIBRARY" ] = { "remotelibrary" : REMOTELIBRARY }
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )
