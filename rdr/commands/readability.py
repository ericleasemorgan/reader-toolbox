
# readability - given a study carrel, output readability (Flesch) scores

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='score', type=click.Choice( [ 'id', 'score' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def readability( carrel, sort, output, save ) :

	"""Report on the readability (Flesch score) of items in <carrel>
	
	It is possible to denote how difficult a text is to read by measuring things like number of words, density of the vocabulary, the length of a document, etc. Such calculations have been done against <carrel>, and this subcommand will output the results. If the returned values are wide-ranging, then this will tell you one thing about <carrel>. For example, some of the documents are either difficult to read, very long, or poorly transcribed ("OCR'ed"). If the measurements are homogeneous, then your carrel is more sane than not.
	
	Example: rdr readability homer -o boxplot"""

	# do the work
	if not save : click.echo( flesch( carrel, sort, output ) )
	else        : flesch( carrel, sort, output, save )