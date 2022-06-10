
# semantics - given query, do word embedding (semantic indexing)

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-t', '--type', default='similarity', type=click.Choice( [ 'similarity', 'distance', 'analogy', 'scatter' ], case_sensitive=True ), help="query type")
@click.option('-q', '--query', default='love', help='the word(s) to be used for search')
@click.option('-s', '--size', default=10, help='number of results to return')
def semantics( carrel, type, query, size ) :

	'''Apply semantic indexing against <carrel>
	
	Sometimes called "word embedding", use this subcommand to learn: 1) what words are similar to a given word, 2) how close in meaning sets of words are, or 3) what words compare to three other words. In order to work accurately, semantic indexing requires larger rather than smaller corpora; results from corpora less than 1,500,000 words in size ought to be considered dubious at best.
	
	This command requires a Python module called "word2vec", which is not installed by default. This is because the module needs to be compiled and doing so on Windows computers is challenging. Linux and Macintosh users can probably do 'pip install word2vec', but Windows users will have to go through additional hoops. But please be consoled when you remember that corpora less than 1.5 million words do not return accurate results. Is <carrel> 1.5 million words long?
	
	Examples:
	
	\b
	  rdr semantics -t similarity -q war homer
	  rdr semantics -t distance -q "king queen prince love war" homer
	  rdr semantics -t analogy -q "king queen prince" homer'''

	# do the work and done
	click.echo( word2vec( carrel, type, query, size ) )