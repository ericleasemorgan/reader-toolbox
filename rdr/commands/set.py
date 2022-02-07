
# require
from rdr import *

# config
@click.command()
@click.option('-s', '--setting', default='local', type=click.Choice( [ 'local', 'mallet', 'tika' ] ), help='configure the given setting')
def set( setting ) :

	"""Configure the location of study carrels and a subsystem called MALLET.
	
	You need to run this command before you are able to download carrels.
	
	Examples:
	
	\b
	  rdr set
	  rdr set -s mallet
	
	See also: rdr get --help"""
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	
	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory/CONFIGURATIONFILE
	
	# create configuration file, conditionally
	if not configurationFile.exists() :
		
		# initialize
		configurations[ "RDR" ] = { "localLibrary"  : Path.home()/READERLIBRARY, 
		                            "malletHome"    : '',
		                            "tikaHome" : '' }

		# create directory and save the file
		applicationDirectory.mkdir( parents=False, exist_ok=True )
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )
		
	# re-initialize
	localLibrary  = configuration( 'localLibrary' )
	malletHome    = configuration( 'malletHome' )
	tikaHome      = configuration( 'tikaHome' )

	# branch accordingly, local
	if setting == 'local' :
	
		# get the desired library location
		click.echo( 'Where do you want to save your study carrels? Press enter to accept the default.' )
		localLibrary = input( 'Directory [%s]: ' % localLibrary ) or localLibrary
		localLibrary = Path( localLibrary )

		# try to create the directory and save the configuration
		try : localLibrary.mkdir( exist_ok=True )
		except FileNotFoundError : click.echo( "Error: File not found. Are you sure you entered a valid path?", err=True )		

	# mallet
	elif setting == 'mallet' :
	
		# get the desired library location
		click.echo( 'What is the full path to your MALLET distribution?' )
		malletHome = input( 'Directory [%s]: ' % malletHome ) or malletHome

	# tika
	elif setting == 'tika' :
	
		# get the desired library location
		click.echo( 'What is the full path to tika-server.jar?' )
		tikaHome = input( 'Directory [%s]: ' % tikaHome ) or tikaHome

	# update the configuration file
	configurations[ "RDR" ] = { "localLibrary"  : localLibrary, "malletHome" : malletHome , "tikaHome" : tikaHome }
	with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )


