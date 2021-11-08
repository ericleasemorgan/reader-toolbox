
# ent - given a study carrel, output named entitites

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-s', '--select', default='type', type=click.Choice( [ 'type', 'entity' ] ), help='the type of output')
@click.option('-l', '--like', default='any', help='the type of enity')
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def ent( carrel, select, like, count ) :

	"""Filter out named entities and types of entities found in <carrel>

	Use this subcommand to address who, what, when, and where questions regarding <carrel>.

	Examples:

	\b
	  rdr ent homer

	See also: rdr pos --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# branch accordingly; types of entities
	if select == 'type' :
	
		# dump
		if not count :

			# articulate sql, search, and output
			sql  = 'SELECT type FROM ent;'
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ 'type' ] )

		# count and tabulate the dump
		else :
		
			# articulate sql, search, and output
			sql  = 'SELECT type, COUNT( type ) AS count FROM ent GROUP BY type ORDER BY count DESC;'
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ 'type' ], str( row[ 'count' ] ) ] ) )			
			
	# entities
	else : 
			
		# initialize like
		if like == 'any' : like = '%'
		else             : like == like.upper()
		
		# simply dump the desired content
		if not count :
		
			# build sql, search, and output
			sql  = ( 'SELECT entity FROM ent WHERE type LIKE "%s";' % ( like ) )
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ select ] )
		
		# count and tabulate the result
		else:

			# build sql, search, and output
			sql  = ( 'SELECT entity, COUNT( entity ) AS count FROM ent WHERE type LIKE "%s" GROUP BY entity ORDER BY count DESC;' % ( like ) )
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ select ], str( row[ 'count' ] ) ] ) )
			
	# clean up
	connection.close()

