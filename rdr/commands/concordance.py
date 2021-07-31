
# require
from rdr import *

import nltk

# list
@click.command()
@click.argument( 'carrel' )
@click.argument( 'word' )
def concordance( carrel, word ) :

	"""Given a CARREL and a WORD, implement a key-word-in-context index"""

	file   = LOCALLIBRARY + '/' + carrel + '/' + ETC + '/' + CORPUS
	
	text = nltk.Text( nltk.word_tokenize( open( file ).read( ) ) )
	text.concordance( word, width=os.get_terminal_size().columns )

