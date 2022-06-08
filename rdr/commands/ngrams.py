
# ngrams - given a study carrel and an integer, output... ngrams

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-q', '--query',     type=click.STRING, help="filter results to include the given regular expression")
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-l', '--location',  default='local', type=click.Choice( [ 'local', 'remote' ] ), help='where is the study carrel')
@click.option('-s', '--size',      default=1, help='denote unigrams, bigrams, trigrams, etc')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, output a wordcloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save cloud to default location')
@click.argument( 'carrel', metavar='<carrel>' )
def ngrams( carrel, size, query, count, location, wordcloud, save ) :

	"""Output and list words or phrases found in <carrel>

	This is almost always one of the first places to start when doing your analysis, and it can be applied to local as well as remote study carrels. Ngrams with sizes (-s) greater than 2 will include stopwords because ngrams of three or more words often do not make sense without them. Use the -c option to count and tabulate the result. Use the query (-q) to filter the result with a regular expression. 

	Examples:

	\b
	  rdr ngrams homer
	  rdr ngrams -s 2 homer
	  rdr ngrams -s 2 -c homer
	  rdr ngrams -s 2 -c -q love homer
	  rdr ngrams -s 2 -c -q love homer | more
	  rdr ngrams -s 2 -c -q love -l remote sonnets | more

	See also: rdr concordance --help"""

	if not save : click.echo( ngramss( carrel, size, query, count, location, wordcloud ) )
	else        : ngramss( carrel, size, query, count, location, wordcloud, save )