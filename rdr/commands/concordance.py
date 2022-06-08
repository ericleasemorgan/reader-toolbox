# concordance - given a carrel and a word, output rudimentary keyword-in-context

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.option('-w', '--width', default=80, help='number of characters in each line of output')
@click.option('-l', '--lines', default=999, help='number of lines of text to output')
@click.option('-q', '--query', default='love', help='a word for phrase')
@click.argument( 'carrel', metavar='<carrel>' )
def concordance( carrel, query, width, lines ) :

	"""A poor man's search engine
	
	Given a query, this subcommand will search <carrel> and return a list of results where each result is a set of words to the left of query, the query, and a set of words to the right of query -- a keyword-in-context index. This is useful for answering the question, "What words are used in the same breath as the given word?" The query can be a phrase, but it can not be a regular expression. Consider creating a word cloud from the output of this command to visualize the "words used in the same breath". 
	
	Examples:
	
	\b
	  rdr concordance homer -q hector
	  rdr concordance homer -q 'hector was'

	See also: rdr ngrams --help"""
	
	# do the work
	click.echo( concordancing( carrel, query ) )