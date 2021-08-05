
# require
from rdr import *

# config
@click.command()
def home() :

	"""Echo the full path to your local library of study carrels
	
	This is useful if you want to change directories to your local collection of carrels, and then interact with them directly.
	
	Examples:
	
	\b
	  * rdr home"""
	
	# initialize and do the work
	click.echo( str( configuration( 'localLibrary' ) ) )
