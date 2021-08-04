
# concordance - given a carrel and a word, output rudimentary keyword-in-context

# require
from rdr import *

@click.command()
@click.argument( 'carrel' )
@click.argument( 'word' )
def concordance( carrel, word ) :

	"""Given a CARREL and a WORD, implement a key-word-in-context index"""

	# require
	from nltk import Text, word_tokenize
	from os   import get_terminal_size

	# initialize, read, and normalize; ought to save the Text object for future use
	localLibrary = configuration( 'localLibrary' )
	corpus       = localLibrary/carrel/ETC/CORPUS
	text         = Text( word_tokenize( open( str( corpus ) ).read( ) ) )
	
	# output
	text.concordance( word, width=get_terminal_size().columns )

