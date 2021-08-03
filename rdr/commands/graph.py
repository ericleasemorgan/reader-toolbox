
# require
from rdr import *

# list
@click.command()
@click.argument( 'carrel' )
@click.argument( 'form' )
@click.argument( 'window' )
def graph( carrel, form, window ) :

	"""Given a CARREL, FORM ('lemma' or 'word'), and WINDOW, """

	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()

	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 
	localLibrary   = pathlib.Path( localLibrary )
	
	file = localLibrary / carrel / ETC / CORPUS

	# get the text to process
	text = open( str( file ) ).read()

	# create model and then then use it against the text
	size = ( os.stat( file ).st_size ) + 1
	nlp  = spacy.load( MODEL )
	nlp.max_length = size
	doc  = nlp( text )

	# create a graph; the magic happens here
	G = textacy.spacier.doc_extensions.to_semantic_network(
		doc,
		normalize=form, 
		nodes='words', 
		edge_weighting='cooc_freq', 
		window_width=int( window ) )

	# output the graph and done
	nx.write_graphml( G, '/dev/stdout' )
