
# bib - given a study carrel, output rudimentary bibliographics

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
def bib( carrel ) :

	"""Output rudimentary bibliographics from <carrel>.

	Use this subcommand to output metadata regarding the specific items in <carrel>. Metadata on the items includes: identifier, author, title, date, size in words, readability (Flesch) score, summary, keywords, location of cached original, and location of derived plain text. Because of the characteristics of the original input used to create <carrel>, some metadata fields may not have values. Author and date are the best examples. Moreover, the value for title be derived. The combined use of the info command and the bib command will garaner you a good understanding of <carrel>'s breadth and depth.

	Example: rdr bib homer

	See also:
	
	\b
	  rdr info --help
	  rdr search --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# query database
	sql  = '''SELECT b.id, b.words, b.extension, b.flesch, b.author, b.title, b.date, GROUP_CONCAT( LOWER( w.keyword ), '; ') AS keywords, b.summary
	          FROM bib AS b, wrd AS w
	          WHERE b.id = w.id
	          GROUP BY b.id
	          ORDER BY b.id, LOWER( b.author );'''
	rows  = connection.execute( sql )
	rows  = rows.fetchall()
	total = len( rows )
	for item, row in enumerate( rows ) :
	
		# parse
		id        = row[ 'id' ]
		author    = row[ 'author' ]
		title     = row[ 'title' ]
		date      = row[ 'date' ]
		words     = row[ 'words' ]
		flesch    = row[ 'flesch' ]
		summary   = row[ 'summary' ]
		keywords  = row[ 'keywords' ]

		# normalize; unescape
		if summary : summary = summary.replace( "''", "'" )
		
		# build cache and plain text
		cache = str( locallibrary/carrel/CACHE/id ) + row[ 'extension' ]
		text  = str( locallibrary/carrel/TXT/id )   + '.txt'
		
		# output
		click.echo( '        item: #%s of %s' % ( str( item + 1 ), total ) )
		click.echo( '          id: %s' % id )
		click.echo( '      author: %s' % author )
		click.echo( '       title: %s' % title )
		click.echo( '        date: %s' % date )
		click.echo( '       words: %s' % words )
		click.echo( '      flesch: %s' % flesch )
		click.echo( '     summary: %s' % summary )
		click.echo( '    keywords: %s' % keywords )
		click.echo( '       cache: %s' % cache )
		click.echo( '  plain text: %s' % text )
		click.echo()
	
	# clean up
	connection.close()

