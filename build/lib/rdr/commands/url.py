
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

	"""Filter URLs and domains from <carrel>.

	Use this subcommand to learn what is hyperlinked from <carrel>. To the best of its ability, the Distant Reader extracted all the URLs found in <carrel>. This information was saved in sets of files located in the urls directory of <carrel>. This information as has been saved in a relational database file. This subcommand queries that database. Use this command to learn what URLs are in the carrel and from what domains do the URLs emanate. Through this process you may identify URLs of extreme importance or characterize the URLs as coming from governments, companies, organizations. Alternatively, you may create lists of URLs that can be fed to Internet spiders for harvesting or feeding back into the Reader for additional carrel creation. Be forewarned. The plain text whence these URLs came is ugly, thus producing ugly URLs; not all values for URLs are valid.

	Examples:

	\b
	  rdr url ital
	  rdr url -s url ital
	  rdr url -s url -l .pdf ital
	  rdr url -s domain -c ital

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
	if select == 'url' :
	
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

