
# require
from rdr import *

# config
@click.command()
def set() :

	"""Set the current location of your study carrels"""
	
	# configure
	LOCALLIBRARY  = 'reader-library'
	REMOTELIBRARY = 'http://library.distantreader.org'

	# require
	from configparser import ConfigParser
	from pathlib      import Path
	
	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory/CONFIGURATIONFILE

	# look for configuration file
	if not configurationFile.exists() : localLibrary = Path.cwd()/LOCALLIBRARY
	else : localLibrary = configuration( 'localLibrary' )

	# get the desired library location
	click.echo( 'From where do you want to save and read your study carrels? Press enter to accept the default.' )
	localLibrary = input( 'Directory [%s]: ' % localLibrary ) or localLibrary
	localLibrary = Path( localLibrary )

	# try to create the directory and save the configuration
	try : localLibrary.mkdir( exist_ok=True )
	except FileNotFoundError : click.echo( "Error: file not found. Are you sure you entered a valid path?", err=True )		
	else :
		applicationDirectory.mkdir( parents=False, exist_ok=True )
		configurations[ "LOCALLIBRARY" ]  = { "locallibrary"  : str( localLibrary ) }
		configurations[ "REMOTELIBRARY" ] = { "remotelibrary" : REMOTELIBRARY }
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )
