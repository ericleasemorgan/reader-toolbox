
# adr - given a study carrel, output email addresses

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-l', '--like',   type=click.STRING, help="filter results using the given pattern")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def adr( carrel, count, like ) :

	"""Filter email addresses from <carrel>.

	Who are you gonna call? 

	Examples:

	\b
	  rdr adr ital
	  rdr adr -c ital
	  rdr adr -c -l gmail ital

	See also: rdr url --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# dump a sorted list of all email addresses
	if not count :

		# articulate sql
		if like :
		
			sql = ( '''SELECT DISTINCT( LOWER( address ) ) AS address
			           FROM adr
			           WHERE address LIKE "%s"
			           ORDER BY address;''' % ('%' + like + '%' ) )
			
		else :
		
			sql  = '''SELECT DISTINCT( LOWER( address ) ) AS address
			          FROM adr
			          ORDER BY address;'''

		# do the work and output
		rows = connection.execute( sql )
		for row in rows : click.echo( row[ 'address' ]  )			

	# count and tabulate the dump
	else :
	
		# articulate sql
		if like :
		
			sql = ( '''SELECT LOWER( address ) AS address, COUNT( LOWER( address ) ) AS count
			           FROM adr
			           WHERE address LIKE "%s"
			           GROUP BY LOWER( address )
			           ORDER BY count DESC, address;''' % ('%' + like + '%' ) )
			
		else :
		
			sql  = '''SELECT LOWER( address ) AS address, COUNT( LOWER( address ) ) AS count
			          FROM adr
			          GROUP BY LOWER( address )
			          ORDER BY count DESC, address;'''

		# do the work and output
		rows = connection.execute( sql )
		for row in rows : click.echo( "\t".join( [ row[ 'address' ], str( row[ 'count' ] ) ] ) )			

	# clean up and done
	connection.close()

