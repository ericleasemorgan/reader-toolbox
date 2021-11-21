
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
@click.option('-t', '--type', default='similarity', type=click.Choice( [ 'similarity', 'distance', 'analogy' ], case_sensitive=True ), help="query type")
@click.option('-q', '--query', default='love', help='the word(s) to be used for search')
@click.option('-s', '--size', default=10, help='number of results to return')
def semantics( carrel, type, query, size ) :

	'''Apply semantic indexing against <carrel>.
	
	Sometimes called "word embedding", use this subcommand to learn: 1) what words are similar to a given word, 2) how close in meaning sets of words are, or 3) what words compare to three other words. In order to work accurately, semantic indexing requires larger rather than smaller corpora; results from corpora less than 1,500,000 words in size ought to be considered dubious at best.
	
	Examples:
	
	\b
	  rdr semantics -t similarity -q war homer
	  rdr semantics -t distance -q "king queen prince love war" homer
	  rdr semantics -t analogy -q "king queen prince" homer'''

	# configure
	MODEL    = 'reader.bin'
	DISTANCE = 'model.distance( ##QUERY## )'

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

	# similarity
	if type == 'similarity' :
	
		# sanity check
		if len( query.split() ) != 1 :
		
			# error
			click.echo( "The query for similarity requires exactly one word.", err=True )
			exit()

		# search and output
		try :
	
			indexes, metrics = model.similar( query, n=size )
			similarities = model.generate_response( indexes, metrics ).tolist()
			for similarity in similarities : click.echo( '\t'.join( [ similarity[ 0 ], str( similarity[ 1 ] ) ] ) )
		
		# word not found
		except KeyError as word : click.echo ( ( 'The word -- %s -- is not in the index.' % word ), err=True )

	# distance
	elif type == 'distance' :

		# get the query words
		words = query.split()

		# sanity check
		if len( words ) < 2 :
		
			# error
			click.echo( "The query for distance requires at least two words.", err=True )
			exit()

		# create a distance command; hacky!
		queries = [ ( "'%s'" % word ) for word in words ]
		command = DISTANCE.replace( '##QUERY##', ', '.join( queries ) )
		
		# try to compute
		try :
		
			# search, sort, output, and done
			distances = eval( command )
			distances.sort( key=lambda i: i[ 2 ], reverse=True )
			for distance in distances : print( '\t'.join( [ distance[ 0 ], distance[ 1 ], str( distance[ 2 ] ) ] ) )

		# error
		except KeyError as word : 
			sys.stderr.write( ( 'A word in your query -- %s -- is not in the index. Please remove it.\n' % word ) )

	# analogy
	elif type == 'analogy' :
	
		# get the query words
		words = query.split()
		
		# sanity check
		if len( words ) != 3 :
		
			# error
			click.echo( "The query for analogy requires exactly three words.", err=True )
			exit()
		
		# try to compute
		try :
		
			# search, sort, output, and done
			indexes, metrics = model.analogy( pos=[ words[ 0 ], words[ 1 ] ], neg=[ words[ 2 ] ], n=size )
			analogies = model.generate_response( indexes, metrics ).tolist()
			for analogy in analogies : print( '\t'.join( [ analogy[ 0 ], str( analogy[ 1 ] ) ] ) )

		# error
		except KeyError as word : click.echo( ( 'A word in your query -- %s -- is not in the index. Please remove it.\n' % word ), err=True )

