
# require
from rdr import *

# config
@click.command()
@click.option('-s', '--setting', default='local', type=click.Choice( [ 'local', 'mallet' ] ), help='output the given setting')
def get( setting ) :

	"""Echo the full path to your local library of study carrels
	
	This is useful if you want to change directories to your local collection of carrels, and then interact with them directly.
	
	Examples:
	
	\b
	  * rdr home"""
	
	# branch accordingly
	if   setting == 'local' : click.echo( str( configuration( 'localLibrary' ) ) )
	elif setting == 'mallet' : click.echo( str( configuration( 'malletHome' ) ) )
	
	
