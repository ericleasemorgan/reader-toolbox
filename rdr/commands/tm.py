
# tm - do topic modeling

# require
from rdr import *

# configure
MODELDIR        = 'etc/topic-model'
VECTORS         = 'model.vec'
TXT2VEC         = "%s/bin/mallet import-dir --input %s --output %s --keep-sequence TRUE --stoplist-file %s"
VEC2MODEL       = "%s/bin/mallet train-topics --input %s --num-topics %s --num-top-words %s --num-top-docs %s --num-iterations %s --num-threads 8 --optimize-interval 10 --output-doc-topics %s/topics.tsv --output-state %s/model-state.gz --output-topic-docs %s/documents.txt --output-topic-keys %s/keys.tsv --topic-word-weights-file %s/weights.tsv --word-topic-counts-file %s/counts.txt --xml-topic-phrase-report %s/phrases.xml --xml-topic-report %s/topics.xml"
#VEC2MODEL       = "%s/bin/mallet train-topics --input %s --num-topics %s --num-top-words %s --num-top-docs %s --num-iterations %s --num-threads 8 --optimize-interval 10 --output-doc-topics %s/topics.tsv --output-state %s/model-state.gz --output-topic-docs %s/documents.txt --output-topic-keys %s/keys.tsv --random-seed 0 --topic-word-weights-file %s/weights.tsv --word-topic-counts-file %s/counts.txt --xml-topic-phrase-report %s/phrases.xml --xml-topic-report %s/topics.xml"
KEYS            = 'keys.tsv'
KEYSHEADER      = [ 'ids', 'weights', 'features' ]
DOCUMENTS       = 'documents.txt'
DOCUMENTSHEADER = [ 'ids', 'dids', 'files', 'proportions' ]
TOPDOCS         = 5
SCALE           = 100
PERCENTAGE      = '%1.0f%%'
SQL             = 'SELECT "file:%s/%s/txt/" || id || ".txt" AS file, %s FROM bib order by %s;'
METADATA        = 'metadata.csv'
TOPICS          = 'topics.tsv'
LABELS          = [ 'docId', 'file' ]


def makeSummary( keys, header ) :

	# require
	import pandas as pd

	# read and sort keys file
	keys = pd.read_csv( keys, sep='\t', names=header )
	keys.sort_values( by='weights', ascending=False, inplace=True )

	# create labels for each topic
	labels = []
	for index, row in keys.iterrows() :

		# parse
		features = row[ 'features' ].split()

		# loop through each feature
		for feature in features :

			# build the list, conditionally
			if feature in labels : continue
			labels.append( feature )
			break

	# add the labels, rearrange (just for fun)
	keys[ 'labels' ] = labels
	keys = keys[ [ 'labels', 'weights', 'features' ] ]

	# done
	return keys


def checkForMallet( mallet ) :
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	from requests     import get
	from tempfile     import TemporaryFile
	from zipfile      import ZipFile
	
	# install mallet, conditionally
	if not Path( mallet ).exists() :
	
		click.echo( "MALLET not found. Downoading MALLET... ", err=True )
		response = get( MALLETZIP )

		# initialize a temporary file and write to it
		click.echo( "Saving zip file... ", err=True )
		handle = TemporaryFile()
		handle.write( response.content )

		# unzip the temporary file and close it, which also deletes it
		click.echo( "Unziping zip file... " )
		with ZipFile( handle, 'r' ) as zip : zip.extractall( Path.home() )
		
		# initialize
		click.echo( "Updating configurations... " )
		configurations          = ConfigParser()
		applicationDirectory    = Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
		configurationFile       = applicationDirectory/CONFIGURATIONFILE
		localLibrary            = configuration( 'localLibrary' )
		malletHome              = Path.home()/'mallet'
		configurations[ "RDR" ] = { "localLibrary"  : localLibrary, "malletHome" : malletHome }
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )

		# make mallet executable
		click.echo( "Making MALLET executable... " )
		(malletHome/MALLETBIN).chmod( 0x755 )
		

		# done
		click.echo('''Done. MALLET has been downloaded to your home directory and configured
for future use. You can move MALLET to another location but once you do
so you will need to run 'rdr set -s mallet'.''', err=True )


def pivot( localLibrary, carrel, field, keys ) :

	# require
	import sqlite3
	import pandas as pd

	# initialize
	db         = str( localLibrary/carrel/ETC/DATABASE )
	sql        = ( SQL % ( str( localLibrary ), carrel, field, field ) )
	metadata   = str( localLibrary/carrel/MODELDIR/METADATA )
	topics     = str( localLibrary/carrel/MODELDIR/TOPICS )
	connection = sqlite3.connect( db )

	# search and save; should probably eliminate the I/O
	results    = pd.read_sql_query( sql, connection )
	results.to_csv( metadata, index=False )

	# read saved files
	topics   = pd.read_csv( topics, sep='\t' )
	metadata = pd.read_csv( metadata )

	# create generic labels
	labels  = LABELS
	columns = topics.shape[ 1 ]
	for i in range( 0, columns - 2 ) :

		# compute and update list of column names
		i = str( i )
		labels.append( i )

	# create more meaningful labels; initialize some more
	keys = pd.read_csv( keys, sep='\t', names=KEYSHEADER )
	keys.sort_values( by='weights', ascending=False, inplace=True )

	# add labels, drop docId, and merge with metadata
	topics.columns = labels
	topics         = topics.drop( [ 'docId' ], axis=1 )
	topics         = pd.merge( topics, metadata )

	# create meaningful labels for each topic
	ids    = []
	labels = []
	for index, row in keys.iterrows() :

		# update the list of ids
		ids.append( index )

		# get and loop through each feature
		features = row[ 'features' ].split()
		for feature in features :

			# build the list, conditionally
			if feature in labels : continue
			labels.append( feature )
			break

	# update with generic labels
	keys[ 'labels' ] = labels

	# process each id; update with more meaningful labels
	for index, id in enumerate( ids ) :

		column = str( id )
		label  = labels[ index ]
		topics.rename( columns = { column:label }, inplace=True )

	# pivot and return
	topics = topics.pivot_table( list( topics.columns ), index=field )
	return( topics )


@click.command( options_metavar='<options>' )
@click.option('-p', '--process', default='model', type=click.Choice( [ 'model', 'read' ] ), help="type of work to do" )
@click.option('-t', '--topics', default=7, help="number of topics to generate" )
@click.option('-w', '--words', default=7, help="number of words used to describe topic" )
@click.option('-i', '--iterations', default=2400, help="number of times to cacluate" )
@click.option('-o', '--output', default='summary', type=click.Choice( [ 'summary', 'chart', 'topdocs', 'csv' ] ), help="type of report" )
@click.option('-f', '--field', type=click.Choice( [ 'author', 'title', 'date' ] ), help="field for pivoting" )
@click.option('-y', '--type', default='pie', type=click.Choice( [ 'pie', 'bar', 'barh', 'line', 'scatter' ] ), help="type of chart" )
@click.argument( 'carrel', metavar='<carrel>' )
def tm( carrel, process, topics, words, iterations, output, field, type ) :

	"""Apply topic modeling against <carrel>.
	
	Topic modeling is the process of enumerating latent themes from a corpus, and it is yet another way to describe a corpus's aboutness. It is suggested you start out small when it comes to the values for -t and -w. Repeat the modeling process and gradually increase the values. Increase the value of -i as the size of your carrel increases. 
	
	Remember, there is no such thing as the correct value of -t. After all, exactly how many things is the sum of Shakespeare's works about?
	
	Examples:
	
	\b
	  rdr tm homer
	  rdr tm homer -p read
	  rdr tm homer -p read -o pivot -f title -c line"""

	# require
	from pathlib import Path
	import matplotlib.pyplot as plot
	import os
	import sys
	import pandas as pd
	from   sklearn.manifold  import TSNE

	# sanity checks
	checkForCarrel( carrel )
	checkForMallet( str( configuration( 'malletHome' ) ) + '/' + MALLETBIN )

	# initialize
	localLibrary = configuration( 'localLibrary' )
	mallet       = str( configuration( 'malletHome' ) )
	stopwords    = str( localLibrary/carrel/ETC/STOPWORDS )
	corpus       = str( Path( localLibrary/carrel/TXT ) )
	modeldir     = str( localLibrary/carrel/MODELDIR )
	vectors      = str( localLibrary/carrel/MODELDIR/VECTORS )
	keys         = str( localLibrary/carrel/MODELDIR/KEYS )
	documents    = str( localLibrary/carrel/MODELDIR/DOCUMENTS )
	
	# create a model
	if process == 'model' :
	
		#  make sane
		Path( modeldir ).mkdir( exist_ok=True )

		# create vectors
		command = ( TXT2VEC % ( mallet, corpus, vectors, stopwords ) )	
		os.system( command )
	
		# topic model
		command = ( VEC2MODEL % ( mallet, vectors, topics, words, TOPDOCS, iterations, modeldir, modeldir, modeldir, modeldir, modeldir, modeldir,  modeldir, modeldir ) )
		os.system( command )

		# summarize and output
		keys = makeSummary( keys, KEYSHEADER )
		click.echo( keys )
			
	# read the model
	else : 
	
		# simple summary
		if output == 'summary' :
			
			# summarize and output
			summary = makeSummary( keys, KEYSHEADER )
			click.echo( summary )

		# top documents
		if output == 'topdocs' :
	
			# output a summary
			keys = makeSummary( keys, KEYSHEADER )
			click.echo( keys )
			click.echo()
		
			# create dictionary of labels (map), for future use
			map = keys[ 'labels' ].to_dict()

			# read the documents file
			documents = pd.read_csv( documents, sep=' ', names=DOCUMENTSHEADER, skiprows=1 )

			# map the ids to the documents, and add them to the data frame
			labels = []
			for index, row in documents.iterrows() : labels.append( map[ row[ 'ids' ] ] )
			documents[ 'labels' ] = labels

			# rearrange, just for fun
			documents = documents[ [ 'ids', 'labels', 'files', 'proportions' ] ]

			# process each label (topic) to 
			for id in map :

				# get the label and create a subset of documents
				label = map[ id ]
				files = documents.loc[ documents[ 'labels'] == label ]

				# re-initialize output
				click.echo( label )

				# process each item in the subset; output matching files
				for index, row in files.iterrows() : print( "  *", row[ 'files' ] )

				# delimit
				click.echo()

		# chart
		if output == 'chart' :
		
			# pie chart
			if type == 'pie' :
			
				# output a summary
				summary = makeSummary( keys, KEYSHEADER )
				click.echo( summary, err=True )

				# visualize
				summary[ 'topics' ] = summary[ 'weights' ].apply( lambda x : x * SCALE )
				summary.plot( kind='pie', y='topics', autopct=PERCENTAGE, labels=summary[ 'labels' ], legend=False ) 
				plot.show()

			# scatter
			if type == 'scatter' :
			
				topics = str( localLibrary/carrel/MODELDIR/TOPICS )
				topics = pd.read_csv( topics, sep='\t' )

				# create generic labels
				labels  = LABELS
				columns = topics.shape[ 1 ]
				for i in range( 0, columns - 2 ) :

					# compute and update list of column names
					i = str( i )
					labels.append( i )
				
				# create more meaningful labels; initialize some more
				keys = pd.read_csv( keys, sep='\t', names=KEYSHEADER )
				keys.sort_values( by='weights', ascending=False, inplace=True )

				# add labels, and drop docId and file
				topics.columns = labels
				topics         = topics.drop( [ 'docId', 'file' ], axis=1 )
				
				# create meaningful labels for each topic
				ids    = []
				labels = []
				for index, row in keys.iterrows() :

					# update the list of ids
					ids.append( index )

					# get and loop through each feature
					features = row[ 'features' ].split()
					for feature in features :

						# build the list, conditionally
						if feature in labels : continue
						labels.append( feature )
						break
				
				# process each id; update with more meaningful labels
				for index, id in enumerate( ids ) :

					column = str( id )
					label  = labels[ index ]
					topics.rename( columns = { column:label }, inplace=True )
				
				# rotate the topics and convert to array
				topics = topics.T
				topics = topics.to_numpy()
				
				# specify type of TSNE modeling, and then model
				tsne   = TSNE( perplexity=1, init='pca', learning_rate='auto' )
				model  = tsne.fit_transform( topics )
				
				# plot
				x = model[ :, 0 ]
				y = model[ :, 1 ]
				plot.scatter( x, y )
				for i, label in enumerate( labels ): plot.annotate( label, ( x[ i ], y[ i ] ) )
				plot.show()

			# bar, barh, or line
			if type == 'line' or type == 'bar' or type == 'barh' :
			
				# sanity check
				if not field :
					click.echo( "Error: When using chart of types 'barh', 'bar', or 'line' you must specify a field (-f). See 'rdr tm --help' for more detail.", err=True )
					exit()
				
				# output a summary
				summary = makeSummary( keys, KEYSHEADER )
				click.echo( summary, err=True )

				# pivot the model on the given field
				topics = pivot( localLibrary, carrel, field, keys )
				
				# configure plot and show
				click.echo( topics, err=True )
				topics.plot( kind=type )
				plot.show()

		# csv
		if output == 'csv' :
		
			# sanity check
			if not field :
				click.echo( "Error: When specifying CSV output you must specify a field (-f). See 'rdr tm --help' for more detail.", err=True )
				exit()
			
			# summarize and output
			summary = makeSummary( keys, KEYSHEADER )
			click.echo( summary, err=True )

			# pivot the model on the given field
			topics = pivot( localLibrary, carrel, field, keys )
			
			# configure plot and show
			click.echo( topics.to_csv() )

