
# cluster 

# require
from rdr import *

# config
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-t', '--type', default='dendrogram', type=click.Choice( [ 'dendrogram', 'cube' ] ), help='denote the shape of the output')
def cluster( carrel, type ) :

	"""Apply dimension reduction to <carrel> and visualize the result.
	
	This is useful for determining how holistic <carrel> is. A carrel with many clusters is less holistic and probably means the number of latent topics (think "subjects") is high. On the other hand, you may observe clusters falling into distinct groups surrounding authors, titles, or sources. In other words, use this subcommand to learn the degree <carrel> is a hodgepodge of items or a collection of unrelated items. 
	
	Example: rdr cluster homer
	
	See also: rdr tm --help"""

	# configure
	MAXIMUM   = 0.95
	MINIMUM   = 2
	STOPWORDS = 'english'
	EXTENSION = '.txt'

	# require
	from os                              import path, system, listdir
	from scipy.cluster.hierarchy         import ward, dendrogram
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.manifold                import MDS
	from sklearn.metrics.pairwise        import cosine_similarity
	import matplotlib.pyplot             as     plt

	# sanity check
	checkForCarrel( carrel )

	# initialize
	localLibrary = configuration( 'localLibrary' )
	directory    = localLibrary/carrel/TXT
	filenames    = [ path.join( directory, filename ) for filename in listdir( directory ) ]
	vectorizer   = TfidfVectorizer( input='filename', max_df=MAXIMUM, min_df=MINIMUM, stop_words=STOPWORDS )
	matrix       = vectorizer.fit_transform( filenames ).toarray()
	distance     = 1 - cosine_similarity( matrix )
	keys         = [ path.basename( filename ).replace( EXTENSION, '' ) for filename in filenames ] 

	# branch according to type; dendrogram
	if type == 'dendrogram' :
		linkage_matrix = ward( distance )
		dendrogram( linkage_matrix, orientation="right", labels=keys )
		plt.tight_layout() 

	# cube
	elif type == 'cube' :
		mds = MDS( n_components=3, dissimilarity="precomputed", random_state=1 )
		pos = mds.fit_transform( distance )
		fig = plt.figure()
		ax  = fig.add_subplot( 111, projection='3d' )
		ax.scatter( pos[ :, 0 ], pos[ :, 1 ], pos[ :, 2 ] )
		for x, y, z, s in zip( pos[ :, 0 ], pos[ :, 1 ], pos[ :, 2 ], keys ) : ax.text( x, y, z, s )

	# error
	else : 
		click.echo( f"Error: Unknown value for TYPE: { type }" )
		system( 'rdr cluster --help' )		

	# output
	plt.show()



