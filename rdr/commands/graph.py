
# require
from rdr import *

# given a carrel, return a spacy doc
def __carrel2doc( carrel ) :

	# configure
	PICKLE  = 'etc/reader.bin'
	CORPUS  = 'etc/reader.txt'

	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 

	# initialize
	pickle = localLibrary + '/' + carrel + '/' + PICKLE

	# check to see if we've previously been here
	if os.path.exists( pickle ) :
		
		# read the pickle file
		doc = next( textacy.io.spacy.read_spacy_docs( pickle ) )
	
	# otherwise
	else :
	
		# warn
		click.echo( 'Reading and formatting data model for future use. This may take many minutes. Please be patient...', err=True )

		# create a doc
		file           = localLibrary + '/' + carrel + '/' + CORPUS
		text           = open( file ).read()
		size           = ( os.stat( file ).st_size ) + 1
		nlp            = spacy.load( MODEL )
		nlp.max_length = size
		doc            = nlp( text )

		# save it for future use
		textacy.io.spacy.write_spacy_docs( doc, filepath=pickle )

	# done
	return doc


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

	# initialize
	doc = __carrel2doc( carrel )

	# create a graph; the magic happens here
	G = textacy.spacier.doc_extensions.to_semantic_network(
		doc,
		normalize=form, 
		nodes='words', 
		edge_weighting='cooc_freq', 
		window_width=int( window ) )

	# output the graph and done
	nx.write_graphml( G, '/dev/stdout' )
