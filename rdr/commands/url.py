
# url - given a study carrel, output urls

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-t', '--type', default='url', type=click.Choice( [ 'url', 'domain' ] ), help='full URLs or just domain')
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def url( carrel, type, count ) :

	"""Filter URLs and domains from <carrel>

	Use this subcommand to learn what is hyperlinked from <carrel>.

	Examples:

	\b
	  rdr url ital
	  rdr url -t url ital
	  rdr url -t domain -c ital

	See also: rdr adr --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# dump a sorted list of all email addresses
	if type == 'url' :
	
		if not count :
		
			# articulate sql, search, and output
			sql  = 'SELECT DISTINCT( url ) AS url FROM url ORDER BY url;'
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ 'url' ] )
		
		else :
		
			# articulate sql, search, and output
			sql  = 'SELECT DISTINCT( url ) AS url, COUNT( DISTINCT( url ) ) as COUNT FROM url GROUP BY url ORDER BY count DESC;'
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ 'url' ], str( row[ 'count' ] ) ] ) )	
			
	# count and tabulate the dump
	else :
	
		if not count :
		
			# articulate sql, search, and output
			sql  = 'SELECT LOWER( DISTINCT( domain ) ) AS domain FROM url ORDER BY domain;'
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ 'domain' ] )
		
		else :
		
			# articulate sql, search, and output
			sql  = 'SELECT LOWER( DISTINCT( domain ) ) AS domain, COUNT( LOWER( DISTINCT( domain ) ) ) AS count FROM url GROUP BY domain ORDER BY count DESC, domain;'
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ 'domain' ], str( row[ 'count' ] ) ] ) )	
			
			
	# clean up
	connection.close()

