
# networks - given a carrel, create bigram networks

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-f', '--filter', default=8, help="least number of occurances of bigram")
@click.option('-m', '--measure', default='chisqr', type=click.Choice( [ 'fisher', 'chisqr', 'jaccard', 'likelihood', 'raw' ], case_sensitive=True ), help="type of measure")
@click.option('-l', '--limit', default=1000, help="number of features")
@click.option('-w', '--window', default=5, help="size of window")
@click.option('-o', '--output', default='image', type=click.Choice( [ 'image', 'gml' ], case_sensitive=True ), help="type of output")
def collocations( carrel, window, filter, measure, limit, output ) :

	'''Output network graph based on bigram collocations in <carrel>.

	This is an additional way of answering the questions: 1) what words are spoken in the same breath as other words, and 2) what words taken together connote themes.

	Given a study carrel of about 200,000 words, the default values ought to generate a network graph with enough depth to be interesting. Specify the -o option to output a Graph Modeling Language (GML) file, and load the result into a visualizer like Gephi for further analysis.
	
	If the image output by the Toolbox is not very dense, then iteratively increase or decrease the values of -l and -f until the density is appealing.

	Examples:

	\b
	  rdr networks homer
	  rdr networks homer -o gml > homer.gml
	  rdr networks homer -l 2000 -f 18 -w 5
	  rdr networks homer -l 2000 -f 18 -w 5 -o gml > homer.gml
	  rdr networks pride -l 1600 -f 8'''

	# require
	from   nltk.collocations import BigramAssocMeasures
	import matplotlib.pyplot as plt
	import networkx as nx
	import nltk

	# initialize
	localLibrary = configuration( 'localLibrary' )
	corpus       = str( localLibrary/carrel/ETC/CORPUS )
	stopwords    = str( localLibrary/carrel/ETC/STOPWORDS )

	# sanity checks
	checkForCarrel( carrel )
		
	# read the stop words and the carrel
	with open( stopwords ) as handle : stopwords = handle.read().split( '\n' )
	with open( corpus )    as handle : corpus    = handle.read()

	# featurize the carrel
	features = nltk.word_tokenize( corpus )
	features = [ feature for feature in features if feature.isalpha() ]
	features = [ feature.lower() for feature in features ]
	features = [ feature for feature in features if feature not in stopwords ]

	# collocate
	finder = nltk.BigramCollocationFinder.from_words( features, window_size=window )
	
	# filter
	if filter > 0 : finder.apply_freq_filter( filter )
	
	# measure
	if   measure == 'chisqr'     : records = finder.score_ngrams( BigramAssocMeasures.chi_sq )
	elif measure == 'jaccard'    : records = finder.score_ngrams( BigramAssocMeasures.jaccard )
	elif measure == 'likelihood' : records = finder.score_ngrams( BigramAssocMeasures.likelihood_ratio )
	elif measure == 'raw'        : records = finder.score_ngrams( BigramAssocMeasures.raw_freq )
	elif measure == 'fisher'     : records = finder.score_ngrams( BigramAssocMeasures.fisher )
	
	# create a network from the scores
	G = nx.Graph()
	for index, record in enumerate( records ) :
	
		# parse
		source = record[ 0 ][ 0 ]
		target = record[ 0 ][ 1 ]
		weight = record[ 1 ]
	
		# update
		G.add_edge( source, target, weight=weight )
	
		# continue, conditionally
		if index > limit : break
	
	# debug
	click.echo( 'Parameters:', err=True )
	click.echo( '  * carrel: '  + carrel, err=True )
	click.echo( '  * limit: '   + str( limit ), err=True )
	click.echo( '  * measure: ' + measure, err=True )
	click.echo( '  * filter: '  + str( filter ), err=True )
	click.echo( '  * window: '  + str( window), err=True )
	click.echo( '', err=True )
	click.echo( 'Result:', err=True )
	click.echo( '  * number of nodes: ' + str( G.number_of_nodes() ), err=True )
	click.echo( '  * number of edges: ' + str( G.number_of_edges() ), err=True )
	
	# output image
	if output == 'image' :
	
		# visualize
		plt.figure()
		nx.draw( G, with_labels=True, node_size=10, font_size=9, edge_color='silver' )
		plt.show()
	
	# output gml; will probably break under Windows
	else: nx.write_gml(G, '/dev/stdout' )
	