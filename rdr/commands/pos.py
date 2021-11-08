
# pos - given a study carrel, output... parts-of-speech

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-s', '--select', default='parts', type=click.Choice( [ 'parts', 'words', 'lemmas' ] ), help='the type of output')
@click.option('-l', '--like', default='any', help='the part-of-speech')
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.option('-n', '--normalize', is_flag=True, help='lower-case the words or lemmas')
@click.argument( 'carrel', metavar='<carrel>' )
def pos( carrel, select, like, count, normalize ) :

	"""Filter out parts-of-speech, words, and lemmas found in <carrel>.

	Use this subcommand to address questions such as: what is mentioned in <carrel>, what do those things do, and how are they described.

	Examples:

	\b
	  rdr pos homer
	  rdr pos -s parts homer
	  rdr pos -s words -l nouns homer
	  rdr pos -s words -l nouns -c homer
	  rdr pos -s lemmas -l nouns -c -n homer
	  rdr pos -s lemmas -l verbs -c -n homer

	See also: rdr ngrams --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# branch accordingly; parts-of-speech
	if select == 'parts' :
	
		# dump parts-of-speech tags
		if not count :

			# articulate sql, search, and output
			sql  = 'SELECT pos FROM pos;'
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ 'pos' ] )

		# count and tabulate the dump
		else :
		
			# articulate sql, search, and output
			sql  = 'SELECT pos, COUNT( pos ) AS count FROM pos GROUP BY pos ORDER BY count DESC;'
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ 'pos' ], str( row[ 'count' ] ) ] ) )			
			
	# words or lemmas
	else : 
	
		# initialize select
		if select == 'words' : select = 'token'
		else                 : select = 'lemma'
		
		# initialize like
		if like == 'any' : like = '%'
		else             : like = like.upper() + '%'
		
		# simply dump the desired content
		if not count :
		
			# build sql
			if not normalize : sql = ( 'SELECT %s FROM pos WHERE pos LIKE "%s";' % ( select, like ) )
			else : sql = ( 'SELECT LOWER( %s ) AS %s FROM pos WHERE pos LIKE "%s";' % ( select, select, like ) )
						
			# search and process each resulting row
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ select ] )
		
		# count and tabulate the result
		else:

			# do not lower-case words or lemmas
			if not normalize : sql = ( '''SELECT %s AS %s, COUNT( %s ) AS count
			                              FROM pos
			                              WHERE pos LIKE "%s"
			                              GROUP BY %s
			                              ORDER BY count DESC;''' % ( select, select, select, like, select ) )
				
			# lower-case words or lemmas
			else: sql = ( '''SELECT LOWER( %s ) AS %s, COUNT( %s ) AS count
			                 FROM pos
			                 WHERE pos LIKE "%s"
			                 GROUP BY LOWER( %s )
			                 ORDER BY count DESC;''' % ( select, select, select, like, select ) )
				
			# search and process each resulting row
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ select ], str( row[ 'count' ] ) ] ) )
		
	# clean up
	connection.close()

