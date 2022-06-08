
# url - given a study carrel, output urls

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-s', '--select', default='url', type=click.Choice( [ 'url', 'domain' ] ), help='full URLs or just domain')
@click.option('-l', '--like',   type=click.STRING, help="filter results using the expression")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def url( carrel, select, count, like ) :

	"""Filter URLs and domains from <carrel>

	Use this subcommand to learn what is hyperlinked from <carrel>. To the best of its ability, the Distant Reader extracted all the URLs found in <carrel>. This information was saved in sets of files located in the urls directory of <carrel>. This information as has been saved in a relational database file. This subcommand queries that database. Use this command to learn what URLs are in the carrel and from what domains do the URLs emanate. Through this process you may identify URLs of extreme importance or characterize the URLs as coming from governments, companies, organizations. Alternatively, you may create lists of URLs that can be fed to Internet spiders for harvesting or feeding back into the Reader for additional carrel creation. Be forewarned. The plain text whence these URLs came is ugly, thus producing ugly URLs; not all values for URLs are valid.

	Examples:

	\b
	  rdr url ital
	  rdr url -s url ital
	  rdr url -s url -l .pdf ital
	  rdr url -s domain -c ital

	See also: rdr adr --help"""

	# do the work and return it
	click.echo( urls( carrel, select, count, like ) )