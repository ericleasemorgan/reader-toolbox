
# ngrams - given a study carrel and an integer, output... ngrams

# require
from rdr import *

# initialize
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'n', metavar='<n>' )

# ngrams
def ngrams( carrel, n ) :

	"""Given a <carrel>, output ngrams of size <n>"""

	# require
	import nltk

	# initialize
	n            = int( n )
	localLibrary = configuration( 'localLibrary' )
	stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ) ).read().split()

	# read, tokenize, and normalize the text
	text   = open( str( localLibrary/carrel/ETC/CORPUS ) ).read()
	tokens = nltk.word_tokenize( text, preserve_line=True )
	tokens = [ token.lower() for token in tokens if token.isalpha() ]
	
	# create the set of ngrams
	ngrams = list( nltk.ngrams( tokens, n ) )
	
	# remove stopwords from unigrams or bigrams
	if n < 3 :
	
		# initialize
		results = []
		
		# process each ngram
		for ngram in ngrams :

			# re-initialize
			found = False
			
			# process each token in the ngram
			for token in ngram :

				# check for stopword
				if token in stopwords : found = True
	
			# conditionally update the results
			if not found : results.append( ngram )

		# done; make it read pretty
		ngrams = results
		
	# output; done
	for ngram in ngrams : click.echo( "\t".join( list( ngram ) ) )