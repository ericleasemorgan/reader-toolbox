
# documentation - read the online documentation

# require
from rdr import *

# read
@click.command( options_metavar='<options>' )
def documentation() :

	"""Use your Web browser to read the Toolbox (rdr) online documentation."""

	# require
	from webbrowser import open

	click.echo( "Your Web browser is being used to open the Toolbox online documentation.", err=True )
	url = DOCUMENTATION
	open( url )
