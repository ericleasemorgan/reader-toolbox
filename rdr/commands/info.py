
# info - given a study carrel, basic information about it

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
def info( carrel ) :

	"""Output metadata describing <carrel>.

	Use this subcommand to learn more specifics about <carrel>.

	Examples:

	\b
	  rdr info homer

	See also: rdr catalog --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row

	# parse provenance
	with open( locallibrary/carrel/PROVENANCE ) as handle : provenance = handle.read().split( '\t' )
	process     = provenance[ 0 ]
	originalID  = provenance[ 1 ]
	dateCreated = provenance[ 2 ]
	timeCreated = provenance[ 3 ]
	creator     = provenance[ 4 ]
	input       = provenance[ 5 ][:-1]
	
	# get extents
	sql = 'SELECT COUNT( id ) AS items, SUM( words ) AS words, AVG( flesch ) AS flesch FROM bib;'
	rows = connection.execute( sql )
	for row in rows :

		items  = row[ 'items' ]
		words  = row[ 'words' ]
		flesch = str( int( row[ 'flesch' ] ) )

 	# get keywords
	keywords = []
	sql      = '''SELECT LOWER( keyword ) AS keyword, COUNT( LOWER( keyword ) ) AS count
	              FROM wrd
	              GROUP BY LOWER( keyword )
	              ORDER BY count DESC, LOWER( keyword );'''
	rows = connection.execute( sql )
	for row in rows :
	
		# parse result and update list
		keyword = row[ 'keyword' ]
		count   = str( row[ 'count' ] )
		keywords.append( '%s (%s)' % ( keyword, count ) )
 	
	# output
	click.echo( "     local identifier: %s" % carrel )
	click.echo( "  original identifier: %s" % originalID )
	click.echo( "              creator: %s" % creator )
	click.echo( "         date created: %s" % dateCreated )
	click.echo( "              process: %s" % process )
	click.echo( "                input: %s" % input )
	click.echo( "                items: %s" % items )
	click.echo( "                words: %s" % words )
	click.echo( "               flesch: %s" % flesch )
	click.echo( "           keyword(s): %s" % "; ".join( keywords ) )
	