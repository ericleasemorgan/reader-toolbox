
# url - given a study carrel, output urls

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-l', '--like',   type=click.STRING, help="filter results using the given regular expression")
@click.option('-t', '--type', default='url', type=click.Choice( [ 'url', 'domain' ] ), help='full URLs or just domain')
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def url( carrel, type, count, like ) :

	"""Filter URLs and domains from <carrel>.

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
	
	# dump a sorted list of all urls
	if type == 'url' :
	
		# don't count
		if not count :
		
			# simple filter
			if like :
			
				# articulate sql
				sql = ( '''SELECT DISTINCT( url ) AS url
				           FROM url
				           WHERE url LIKE "%s"
				           ORDER BY url;''' % ( '%' + like + '%' ) )

			# just dump; articulate sql
			else : sql = 'SELECT DISTINCT( url ) AS url FROM url ORDER BY url;'

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ 'url' ] )

		# count
		else :
		
			# simple filtering
			if like :
			
				# articulate sql
				sql = ( '''SELECT DISTINCT( url ) AS url, COUNT( DISTINCT( url ) ) AS count
				           FROM url
				           WHERE url LIKE '%s'
				           GROUP BY url
				           ORDER BY count DESC;''' % ( '%' + like + '%' ) )
				            
			# no filtering
			else :

				# articulate sql
				sql = '''SELECT DISTINCT( url ) AS url, COUNT( DISTINCT( url ) ) As count
				         FROM url
				         GROUP BY url
				         ORDER BY count DESC;'''

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ 'url' ], str( row[ 'count' ] ) ] ) )	
			
	# domains; count and tabulate the dump
	else :
	
		# no counting
		if not count :
		
			# filter
			if like :
			
				# articulate sql, search, and output
				sql = ( '''SELECT LOWER( DISTINCT( domain ) ) AS domain
				           FROM url
				           WHERE url LIKE '%s'
				           ORDER BY domain;''' % ( '%' + like + '%' ) )

			# no filtering
			else : sql = 'SELECT LOWER( DISTINCT( domain ) ) AS domain FROM url ORDER BY domain;'

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ 'domain' ] )
		
		# count and tabulate
		else :
		
			# filter
			if like :
			
				# articulate sql, search, and output
				sql = ( '''SELECT LOWER( DISTINCT( domain ) ) AS domain, COUNT( LOWER( DISTINCT( domain ) ) ) AS count
				           FROM url
				           WHERE domain LIKE '%s'
				           GROUP BY domain
				           ORDER BY count DESC, domain;''' % ( '%' + like + '%' ) )

			# no filtering
			else :
			
				# articulate sql, search, and output
				sql = '''SELECT LOWER( DISTINCT( domain ) ) AS domain, COUNT( LOWER( DISTINCT( domain ) ) ) AS count
				         FROM url
				         GROUP BY domain
				         ORDER BY count DESC, domain;'''
				         
			# do the work and output
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ 'domain' ], str( row[ 'count' ] ) ] ) )	
			
	# clean up and done
	connection.close()

