
# documentation - read the online documentation

# require
from rdr import *

# read
@click.command( options_metavar='<options>' )
def about() :

	"""Output a brief description of the Reader Toolbox (rdr) application."""

	# configure
	ABOUT = '''
  The Reader Toolbox (rdr) is a command-line application used to create
  and model data sets called Distant Reader study carrels.
'''

	# do the work and done
	click.echo( ABOUT )