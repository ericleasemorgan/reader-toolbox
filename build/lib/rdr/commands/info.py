
# info - given a study carrel, basic information about it

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
def info( carrel ) :

	"""Output metadata describing <carrel>.

	Use this subcommand to output very low-level metadata regarding <carrel>. Metadata includes values for identifiers, a possible title, name and date of publisher and publication, Reader process and input used for carrel creation, various extents, and most common keywords. This subcommand is useful for garnering the most rudimentary information about <carrel>.

	Example: rdr info homer

	See also: rdr catalog --help"""

	# require
	import sqlite3
	import re
	
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
	
	# parse identifier; extract type, title, and source
	parts = carrel.split( '-' )
	if len( parts ) == 3 :

		type   = parts[ 0 ]
	
		title  = parts[ 1 ]
		if not type == 'classification' :
	
			title  = title.replace( '_', ' ' )
			title  = re.sub( '[A-Z]',    lambda m: ' ' + m.group().lower(), title )
			title  = re.sub( r'\b[a-z]', lambda m: m.group().upper(), title )
			#title  = re.sub( r'[a-z]\d', lambda m: ' ', title )
			title  = re.sub( r'^ +', '', title )
	
		source = parts[ 2 ]
	
	else :

		type   = 'unknown'
		title  = carrel
		source = 'unknown'


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
	              ORDER BY count DESC, LOWER( keyword ) LIMIT 5;'''
	rows = connection.execute( sql )
	for row in rows :
	
		# parse result and update list
		keyword = row[ 'keyword' ]
		count   = str( row[ 'count' ] )
		keywords.append( '%s (%s)' % ( keyword, count ) )
 	
	# output
	click.echo( "     local identifier: %s" % carrel )
	click.echo( "  original identifier: %s" % originalID )
	click.echo( "                title: %s" % title )
	click.echo( "            publisher: %s, %s" % ( creator, dateCreated) )
	click.echo( "              process: %s (name); %s (input)" % ( process, input ) )
	click.echo( "              extents: %s items; %s words; %s readability" % ( items, words, flesch ) )
	click.echo( "           keyword(s): %s" % "; ".join( keywords ) )
	