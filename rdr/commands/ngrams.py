
# require
from rdr import *

import nltk

# list
@click.command()
@click.argument( 'carrel' )
@click.argument( 'n' )
def ngrams( carrel, n ) :

	"""Given a CARREL, output ngrams of size N"""

	file   = LOCALLIBRARY + '/' + carrel + '/' + ETC + '/' + CORPUS
	ngrams = list( nltk.ngrams( open( file ).read().split(), int( n ) ) )
	for ngram in ngrams : click.echo( "\t".join( list( ngram ) ) )