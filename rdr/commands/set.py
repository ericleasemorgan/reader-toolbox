
# require
from rdr import *

# config
@click.command()
@click.option('-s', '--setting', type=click.Choice( [ 'local', 'mallet', 'tika' ] ), help='configure the given setting')
@click.option('-e', '--erase', is_flag=True, help='erase/restore default settings')
def set( setting, erase ) :

	"""Configure the location of study carrels, the subsystem called MALLET, and Tika
	
	In order to read study carrels, they need to be saved on your computer, and the primary purpose of this subcommand is to denote where that will be. By default, study carrels will be saved in your home directory under a subdirectory named reader-library. Trust me. This is a good starting point; run 'rdr set -s local', and accept the default. When you use the build command, the Toolbox will download a file named Tika, save it on your home directory, and update your configurations. You can use this subcommand to denote a location other than your home directory for Tika. The same thing is true for a subsystem called MALLET, which is used by the tm command.
	
	Examples:
	
	\b
	  rdr set -s local
	  rdr set -s mallet
	  rdr set -s tika
	  rdr set -e
	
	See also: rdr get --help"""
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	
	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE
					
	# erase/restore configurations
	if erase : 
	
		# do the work and report
		initializeConfigurations()
		click.echo( '''
  INFO: Your settings have been restored to their defaults. If
  needed, use the 'rdr get' and 'rdr set' commands to customize
  them.
''', err=True )

	# branch
	if setting :
	
		# re-initialize
		localLibrary = configuration( 'localLibrary' )
		malletHome   = configuration( 'malletHome' )
		tikaHome     = configuration( 'tikaHome' )

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
			tikaHome = input( 'File [%s]: ' % tikaHome ) or tikaHome

		# update the configuration file
		configurations[ "RDR" ] = { "localLibrary"  : localLibrary, "malletHome" : malletHome , "tikaHome" : tikaHome }
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )


