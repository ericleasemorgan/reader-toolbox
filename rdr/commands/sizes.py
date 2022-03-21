
# adr - given a study carrel, output email addresses

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='words', type=click.Choice( [ 'id', 'words' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def sizes( carrel, sort, output, save ) :

	"""Report on the sizes (in words) of items in <carrel>"""

	# configure
	WORDS   = 'SELECT id, words FROM bib ORDER BY words DESC'
	ID      = 'SELECT id, words FROM bib ORDER BY id ASC'
	COLUMNS = [ 'sizes in words' ]
	
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
	if sort == 'words' : rows = connection.execute( WORDS )
	else               : rows = connection.execute( ID )
		
	# branch according to given output; simple list
	if output == 'list' :
	
		# process each row; output tab-delimited list
		for row in rows : click.echo( '\t'.join( [ str( row[ 'id' ] ), str( row[ 'words' ] ) ]) )   
   
	# output charts
	else :
			
		# create a simple list of words, and store it in a dataframe
		records = []
		for row in rows : records.append( int( row[ 'words' ] ) )
		df = pd.DataFrame( records, columns=COLUMNS )

		# initialize the plot
		figure, axis = plt.subplots()
		
		# plot
		if output == 'histogram' : 
		
			df.hist( ax=axis )
			if save : plt.savefig( locallibrary/carrel/FIGURES/SIZESHISTOGRAM )
			else    : plt.show()

		else :
		
			df.boxplot( ax=axis )		
			if save : plt.savefig( locallibrary/carrel/FIGURES/SIZESBOXPLOT )
			else    : plt.show()
		
	# clean up
	connection.close()

