
# require
from rdr import *

# config
@click.command()
@click.argument( 'carrel' )
@click.argument( 'type' )
def cluster( carrel, type ) :

	"""Cluster the given CARREL and visualize the results, where TYPE is either 'cube' or 'dendrogram'"""

	# configure
	MAXIMUM   = 0.95
	MINIMUM   = 2
	STOPWORDS = 'english'
	EXTENSION = '.txt'

	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 

	# initialize & compute
	directory  = localLibrary + '/' + carrel + "/txt"
	filenames  = [ os.path.join( directory, filename ) for filename in os.listdir( directory ) ]
	vectorizer = TfidfVectorizer( input='filename', max_df=MAXIMUM, min_df=MINIMUM, stop_words=STOPWORDS )
	matrix     = vectorizer.fit_transform( filenames ).toarray()
	distance   = 1 - cosine_similarity( matrix )
	keys       = [ os.path.basename( filename ).replace( EXTENSION, '' ) for filename in filenames ] 

	# branch according to configuration; visualize
	if type == 'dendrogram' :
		linkage_matrix = ward( distance )
		dendrogram( linkage_matrix, orientation="right", labels=keys )
		plt.tight_layout() 

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
		os.system( 'rdr cluster --help' )		

	# output and done
	plt.show()
	exit()



