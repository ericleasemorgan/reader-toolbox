
# adr - given a study carrel, output email addresses

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-l', '--like',   type=click.STRING, help="filter results using the given pattern")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def adr( carrel, count, like ) :

	"""Filter email addresses from <carrel>

	Who are you gonna call? 

	Examples:

	\b
	  rdr adr ital
	  rdr adr -c ital
	  rdr adr -c -l gmail ital

	See also: rdr url --help"""

	# do the work and return it
	click.echo( addresses( carrel, count, like ) )