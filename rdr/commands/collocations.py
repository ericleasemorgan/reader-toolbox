
# networks - given a carrel, create bigram networks

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-f', '--filter',  default=4, help="least number of occurances of bigram")
@click.option('-m', '--measure', default='chisqr', type=click.Choice( [ 'fisher', 'chisqr', 'jaccard', 'likelihood', 'raw' ], case_sensitive=True ), help="type of measure")
@click.option('-l', '--limit',   default=4000, help="number of features")
@click.option('-w', '--window',  default=4, help="size of window")
@click.option('-o', '--output',  default='image', type=click.Choice( [ 'image', 'gml' ], case_sensitive=True ), help="type of output")
@click.option('-v', '--save',    is_flag=True, help='save graph to default location')
def collocations( carrel, window, filter, measure, limit, output, save ) :

	'''Output network graph based on bigram collocations in <carrel>

	This is an additional way of answering the questions: 1) what words are spoken in the same breath as other words, and 2) what words taken together connote themes. Given a study carrel of about 200,000 words, the default values ought to generate a network graph with enough depth to be interesting. Specify the -o option to output a Graph Modeling Language (GML) file, and load the result into a visualizer like Gephi. If the image output by the Toolbox is not very dense, then iteratively increase or decrease the values of -l and -f until the density is appealing. The various measures are used to denote the significance of collocations.

	Examples:

	\b
	  rdr networks homer
	  rdr networks homer -o gml > homer.gml
	  rdr networks homer -l 2000 -f 18 -w 5
	  rdr networks homer -l 2000 -f 18 -w 5 -o gml > homer.gml
	  rdr networks pride -l 1600 -f 8'''

	# do the work
	collocate( carrel, window, filter, measure, limit, output, save )