
# adr - given a study carrel, output email addresses

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='words', type=click.Choice( [ 'id', 'words' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def sizes( carrel, sort, output, save ) :

	"""Report on the sizes (in words) of items in <carrel>"""

	# do the work
	click.echo( size( carrel, sort, output, save ) )