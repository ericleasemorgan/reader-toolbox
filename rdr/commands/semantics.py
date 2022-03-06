
# semantics - given query, do word embedding (semantic indexing)

# require
from rdr import *

# elaborate about the lack of word2vec
def word2vecwarning() :

	click.echo( "By default, Word2vec not installed, which is required for this subcommand. Linux and Macintosh users can probably run 'pip install word2vec' and then give this subcommand another go. Windows users will have to go through many hoops because the underling word2vec software needs to be compiled. Please see the word2vec home page for more detail: https://github.com/danielfrg/word2vec", err=True )
	exit()


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
@click.option('-t', '--type', default='similarity', type=click.Choice( [ 'similarity', 'distance', 'analogy', 'scatter' ], case_sensitive=True ), help="query type")
@click.option('-q', '--query', default='love', help='the word(s) to be used for search')
@click.option('-s', '--size', default=10, help='number of results to return')
def semantics( carrel, type, query, size ) :

	'''Apply semantic indexing against <carrel>
	
	Sometimes called "word embedding", use this subcommand to learn: 1) what words are similar to a given word, 2) how close in meaning sets of words are, or 3) what words compare to three other words. In order to work accurately, semantic indexing requires larger rather than smaller corpora; results from corpora less than 1,500,000 words in size ought to be considered dubious at best.
	
	This command requires a Python module called "word2vec", which is not installed by default. This is because the module needs to be compiled and doing so on Windows computers is challenging. Linux and Macintosh users can probably do 'pip install word2vec', but Windows users will have to go through additional hoops. But please be consoled when you remember that corpora less than 1.5 million words do not return accurate results. Is <carrel> 1.5 million words long?
	
	Examples:
	
	\b
	  rdr semantics -t similarity -q war homer
	  rdr semantics -t distance -q "king queen prince love war" homer
	  rdr semantics -t analogy -q "king queen prince" homer'''

	# configure
	MODEL    = 'reader.bin'
	DISTANCE = 'model.distance( ##QUERY## )'

	# try to import word2vec
	try    : import word2vec
	except : word2vecwarning()
	
	# require
	import matplotlib.pyplot as plot


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

	# scatter
	elif type == 'scatter' :
	
		from sklearn.manifold import TSNE
		import numpy as np

		words              = ['love', 'horse', 'house', 'son', 'war', 'man', 'woman', 'spear', 'achilles' ]
		embedding_clusters = []
		word_clusters      = []
		for word in words :
			embeddings = []
			words      = []
			indexes, metrics = model.similar( word, n=20 )
			similarities = model.generate_response( indexes, metrics ).tolist()
			for similarity in similarities :
			
				words.append(similarity[ 0 ])
				embeddings.append( ( similarity[ 0 ], similarity[ 1 ] ) )
		
			embedding_clusters.append( embeddings )
			word_clusters.append( words )

		clusters = np.array( embedding_clusters )	
		print( clusters )
		exit()
					
		tsne     = TSNE( perplexity=2, n_components=2, init='pca'  )
		model    = tsne.fit_transform( clusters )

		# plot
		x = model[ :, 0 ]
		y = model[ :, 1 ]
		plot.scatter( x, y )
		plot.show()

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
			click.echo( ( 'A word in your query -- %s -- is not in the index. Please remove it.' % word ), err=True )

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

