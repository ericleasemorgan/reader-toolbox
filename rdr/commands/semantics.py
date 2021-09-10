
# semantics - given query, do word embedding (semantic indexing)

# require
from rdr import *

# make sure the carrel has been indexed; word2vec++
def checkForSemanticIndex( carrel ) :

	# configure
	MODEL   = 'reader.bin'
	TXT     = 'model.txt'
	PHRASES = 'model.phrases'
	
	# require
	from pathlib  import Path
	from word2vec import word2vec, word2phrase
	import               os
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	model        = localLibrary/carrel/ETC/MODEL
	
	# see if we have been here previously
	if not model.exists() :

		# initialize some more
		stopwords = localLibrary/carrel/ETC/STOPWORDS
		corpus    = localLibrary/carrel/ETC/CORPUS
		txt       = str( Path.home()/TXT )
		phrases   = str( Path.home()/PHRASES )
		
		# tokenize
		click.echo( 'Indexing. This needs to be done only once.', err=True )
		click.echo( 'Step #1 of 6: Tokenizing corpus...', err=True )
		tokens = open( corpus ).read().split()

		# normalize
		click.echo( 'Step #2 of 6: Normalizing tokens...', err=True )
		tokens = [ token.lower() for token in tokens if token.isalpha() ]

		# remove stop words
		click.echo( 'Step #3 of 6: Removing stop words...', err=True )
		stopwords = open( stopwords ).read().split()
		tokens    = [ token for token in tokens if token not in stopwords ]

		# save
		click.echo( 'Step #4 of 6: Saving tokens...', err=True )
		with open( txt, 'w' ) as handle : handle.write( ' '.join( tokens ) )
		
		# create phrases
		click.echo( 'Step #5 of 6: Creating phrases...', err=True )
		word2phrase( txt, phrases, verbose=True )

		# do the work
		click.echo( 'Step #6 of 6: Indexing...', err=True )
		word2vec( phrases, str( model ), size=100, binary=True, verbose=True)

		# clean up and done
		os.remove( txt )
		os.remove( phrases )
		click.echo( '\nDone. Happy searching!', err=True )


@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-q', '--query', default='love', help='the word(s) to be used for search')
def semantics( carrel, query ) :

	'''Apply semantic text queries against <carrel>'''

	# configure
	MODEL = 'reader.bin'

	# require
	import word2vec

	# initialize
	localLibrary = configuration( 'localLibrary' )
	model        = str( localLibrary/carrel/ETC/MODEL )

	# sanity checks
	checkForCarrel( carrel )
	checkForSemanticIndex( carrel )
		
	# load model
	model = word2vec.load( model )

	# search and output
	try :
	
		indexes, metrics = model.similar( query )
		similarities = model.generate_response( indexes, metrics ).tolist()
		for similarity in similarities : click.echo( '\t'.join( [ similarity[ 0 ], str( similarity[ 1 ] ) ] ) )
		
	# word not found
	except KeyError as word : click.echo ( ( 'The word -- %s -- is not in the index.' % word ), err=True )

