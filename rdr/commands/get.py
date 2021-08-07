
# require
from rdr import *

# config
@click.command()
@click.argument( 'item', type=click.Choice( [ 'local', 'mallet' ], case_sensitive=False ) )
def get( item ) :

	"""Echo the full path to your local library of study carrels
	
	This is useful if you want to change directories to your local collection of carrels, and then interact with them directly.
	
	Examples:
	
	\b
	  * rdr home"""
	
	# branch accordingly
	if   item == 'local' : click.echo( str( configuration( 'localLibrary' ) ) )
	elif item == 'mallet' : click.echo( str( configuration( 'malletHome' ) ) )
	
	
