
# wrd - given a study carrel, output keywords

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, visualize as word cloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save result in defaul location')
@click.argument( 'carrel', metavar='<carrel>' )
def wrd( carrel, count, wordcloud, save ) :

	"""Filter statistically computed keywords from <carrel>

	Use this subcommand to address the question, "What is <carrel> about?" Algorithms akin to the venerable TF/IDF and Google's PageRank were used against each item in <carrel> to extract statistically significant keywords (think "subject terms"). These words were saved in files in the wrd directory of <carrel>, and they have been saved to a relational database as well. This command queries that database. The results of this command help you describe the "aboutness" of <carrel> and the keywords can be used to increase precision/recall when doing full text searches. Consider also the use of the resulting keywords as input to the concordance subcommand.

	Examples:

	\b
	  rdr wrd homer
	  rdr wrd -c homer

	See also:
	
	\b
	  rdr concordance --help
	  rdr search --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# dump a sorted list of all keywords
	if not count :

		# articulate sql, search, and output
		sql  = 'SELECT DISTINCT( LOWER( keyword ) ) AS keyword FROM wrd ORDER BY LOWER( keyword );'
		rows = connection.execute( sql )
		for row in rows : click.echo( row[ 'keyword' ] )

	# count and tabulate the dump
	else :
	
		# articulate sql, search, and output
		sql  = 'SELECT LOWER( keyword ) AS keyword, COUNT( LOWER( keyword ) ) AS count FROM wrd GROUP BY LOWER( keyword ) ORDER BY count DESC, keyword;'
		rows = connection.execute( sql )
		
		# output a simple list
		if not wordcloud :
			
			for row in rows : 
		
				# output, conditionally; weird
				if row[ 'keyword' ] : click.echo( "\t".join( [ row[ 'keyword' ], str( row[ 'count' ] ) ] ) )			

		# output a word cloud
		else :
			
			# create a list of frequencies
			frequencies = {}
			for row in rows :
			
				if row[ 'keyword' ] : frequencies[ row[ 'keyword' ] ] = row[ 'count' ]
			
			if not save : cloud( frequencies )
			else :
			
				file = locallibrary/carrel/FIGURES/KEYWORDSCLOUD
				cloud( frequencies, file=file )

	# clean up
	connection.close()

