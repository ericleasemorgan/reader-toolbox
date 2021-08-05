
# mallet - do topic modeling

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.option('-t', '--topics', default=5, help="number of topics to generate")
@click.option('-d', '--dimensions', default=5, help="number of words used to denote each topic")
@click.option('-f', '--files', default=1, help="number of files to select from each resulting topic")
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'function', type=click.Choice( [ 'build', 'apply', 'report' ], case_sensitive=False ) )
def mallet( carrel, function, topics, dimensions, files ) :

	"""Use MALLET to do topic modeling against <carrel>, where the given function is one of:
	
	\b
	  * build - create a vectors file
	  * apply - query the vectors file
	  * report - re-organize the output into a more human-readable form
	"""

	# configure
	KEYS            = 'keys.tsv'
	KEYSHEADER      = [ 'ids', 'weights', 'features' ]
	DOCUMENTS       = 'documents.txt'
	DOCUMENTSHEADER = [ 'ids', 'dids', 'files', 'proportions' ]

	# require
	from os import system
	import pandas as pd
	
	# initialize
	localLibrary = configuration( 'localLibrary' )

	# branch accordingly; build
	if function == 'build' :
		
		# initialize
		txt       = localLibrary/carrel/TXT
		stopwords = localLibrary/carrel/ETC/STOPWORDS
		vectors   = MODELDIR + '/' + VECTORS

		# build a command and do the work; too Unix-like
		cmd = MALLETHOME + '/bin/mallet import-dir --input ' + str( txt ) + ' --output ' + vectors + ' --keep-sequence TRUE --stoplist-file ' + str( stopwords )
		system( cmd )

	# apply
	elif function == 'apply' : 
	
		# build the command and do the work; again, Unix-like
		cmd = MALLETHOME + '/bin/mallet train-topics --input ' + MODELDIR + '/' + VECTORS + ' --num-topics ' + str( topics ) + ' --num-top-words ' + str( dimensions ) + ' --num-top-docs ' + str( files ) + ' --num-iterations 1200 ' +  '--num-threads 10 ' + '--optimize-interval 10 ' + '--output-doc-topics ' + MODELDIR + '/topics.tsv ' + '--output-topic-docs ' + MODELDIR + '/documents.txt ' + ' --output-topic-keys ' + MODELDIR + '/keys.tsv ' + ' --random-seed 42 ' + '--topic-word-weights-file ' + MODELDIR + '/weights.tsv' + ' --word-topic-counts-file ' + MODELDIR + '/counts.txt ' + ' --xml-topic-phrase-report ' + MODELDIR + '/phrases.xml ' + '--xml-topic-report ' + MODELDIR + '/topics.xml'
		system( cmd )

	# report
	elif function == 'report' : 

		# initialize
		keys       = MODELDIR + '/' + KEYS
		documents  = MODELDIR + '/' + DOCUMENTS

		# read and sort keys file
		keys = pd.read_csv( keys, sep='\t', names=KEYSHEADER )
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
		click.echo( keys )
		click.echo()

		# create dictionary of labels (map), for future user
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
			for index, row in files.iterrows() :
				click.echo( "  * ", nl=False )
				click.echo( row[ 'files' ] )
	
			# delimit
			click.echo()
	
