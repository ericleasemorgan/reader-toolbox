
# require
from rdr import *

# config
@click.command()
@click.option('-s', '--setting', default='local', type=click.Choice( [ 'local', 'mallet' ] ), help='output the given setting')
def get( setting ) :

	"""Echo the values denoted by the set subcommand.
	
	This is useful for verifying where your locally cached study carrels are saved as well as where you have saved the MALLET subsystem. 
	
	Example: rdr get
	
	See also: rdr set --help"""
	
	# branch accordingly
	if   setting == 'local' : click.echo( str( configuration( 'localLibrary' ) ) )
	elif setting == 'mallet' : click.echo( str( configuration( 'malletHome' ) ) )
	
	
