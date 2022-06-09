
# cluster 

# require
from rdr import *

# config
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-t', '--type', default='dendrogram', type=click.Choice( [ 'dendrogram', 'cube' ] ), help='denote the shape of the output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def cluster( carrel, type, save ) :

	"""Apply dimension reduction to <carrel> and visualize the result
	
	This is useful for determining how holistic <carrel> is. A carrel with many clusters is less holistic and probably means the number of latent topics (think "subjects") is high. On the other hand, you may observe clusters falling into distinct groups surrounding authors, titles, or sources. In other words, use this subcommand to learn the degree <carrel> is a hodgepodge of items or a collection of related items. 
	
	Example: rdr cluster homer
	
	See also: rdr tm --help"""

	# do the work
	clusters( carrel, type, save )