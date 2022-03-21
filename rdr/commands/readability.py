
# readability - given a study carrel, output readability (Flesch) scores

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='score', type=click.Choice( [ 'id', 'score' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def readability( carrel, sort, output, save ) :

	"""Report on the readability (Flesch score) of items in <carrel>
	
	It is possible to denote how difficult a text is to read by measuring things like number of words, density of the vocabulary, the length of a document, etc. Such calculations have been done against <carrel>, and this subcommand will output the results. If the returned values are wide-ranging, then this will tell you one thing about <carrel>. For example, some of the documents are either difficult to read, very long, or poorly transcribed ("OCR'ed"). If the measurements are homogeneous, then your carrel is more sane than not.
	
	Example: rdr readability homer -o boxplot"""

	# configure
	SCORE   = 'SELECT id, flesch FROM bib ORDER BY flesch DESC'
	ID      = 'SELECT id, flesch FROM bib ORDER BY id ASC'
	COLUMNS = [ 'readability' ]
	
	# require
	import matplotlib.pyplot as plt
	import pandas as pd
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# find all rows
	if sort == 'score' : rows = connection.execute( SCORE )
	else               : rows = connection.execute( ID )
		
	# branch according to given output; simple list
	if output == 'list' :
	
		# process each row; output tab-delimited list
		for row in rows : click.echo( '\t'.join( [ row[ 'id' ], str( row[ 'flesch' ] ) ]) )   
   
	# output charts
	else :
			
		# create a simple list of words, and store it in a dataframe
		records = []
		for row in rows : records.append( int( row[ 'flesch' ] ) )
		df = pd.DataFrame( records, columns=COLUMNS )

		# initialize the plot
		figure, axis = plt.subplots()

		# plot
		if output == 'histogram' : 
		
			df.hist( ax=axis )
			if save : plt.savefig( locallibrary/carrel/FIGURES/READABILITYHISTOGRAM )
			else    : plt.show()

		else :
		
			df.boxplot( ax=axis )		
			if save : plt.savefig( locallibrary/carrel/FIGURES/READABILITYBOXPLOT )
			else    : plt.show()

	# clean up
	connection.close()

