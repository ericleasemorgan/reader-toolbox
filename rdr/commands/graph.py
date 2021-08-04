
# graph - output a graphml file

# require
from rdr import *

@click.command()
@click.argument( 'carrel' )
@click.argument( 'form' )
@click.argument( 'window' )
def graph( carrel, form, window ) :

	"""Given a CARREL, FORM ('lemma' or 'word'), and WINDOW, """

	# configure
	window = int( window )
	
	# require
	from networkx import write_graphml
	from textacy  import spacier
	
	# initialize
	doc = carrel2doc( carrel )

	# create a graph; the magic happens here
	G = spacier.doc_extensions.to_semantic_network(
		doc,
		normalize=form, 
		nodes='words', 
		edge_weighting='cooc_freq', 
		window_width=window )

	# output the graph and done
	write_graphml( G, '/dev/stdout' )
