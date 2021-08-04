
# concordance - given a carrel and a word, output rudimentary keyword-in-context

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'word', metavar='<word>'  )
def concordance( carrel, word ) :

	"""Find <word> in <carrel> and output tokens to the left and right of <word>
	
	Developed in the 12th Century, concordancing is the oldest of text mining tools and the poor man's search engine. Sometimes it is called a keyword-in-context (KWIC) index. Given <word>, this is a quick and easy way to see how it is used in the same breath as other words. Use 'rdr ngrams' to identify possible words of interest.
	
	Example: rdr concordance homer war
	
	See also: rdr ngrams"""

	# require
	from nltk import Text, word_tokenize
	from os   import get_terminal_size

	# initialize, read, and normalize; ought to save the Text object for future use
	localLibrary = configuration( 'localLibrary' )
	corpus       = localLibrary/carrel/ETC/CORPUS
	text         = Text( word_tokenize( open( str( corpus ) ).read( ) ) )
	
	# output
	text.concordance( word, width=get_terminal_size().columns )

