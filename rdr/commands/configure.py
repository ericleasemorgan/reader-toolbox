
# require
from rdr import *
from configparser import ConfigParser

# config
@click.command()
def configure() :

	"""Get and set the configured location of your study carrels"""
	
	# create the application directory
	directory = pathlib.Path( click.get_app_dir( APPLICATION ) )
	directory.mkdir( parents=True, exist_ok=True )
	
	# define configuration file
	file = directory / CONFIGURATION

	configurations           = ConfigParser()
	configurations["REMOTE"] = { 'REMOTELIBRARY' : 'http://library.distantreader.org' }
	configurations["LOCAL"]  = { 'LOCALLIBRARY'  : '/Users/eric/Desktop/library' }
	with open( str( file ), 'w' ) as handle : configurations.write( handle )
	
	click.echo( str( file ) )