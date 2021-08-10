
# ngrams - given a study carrel and an integer, output... ngrams

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-f', '--filter', type=click.STRING, help="limit results to include the given word")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.option('-s', '--size', default=1, help='output in a more human-readable form')
@click.argument( 'carrel', metavar='<carrel>' )
def ngrams( carrel, size, filter, count ) :

	"""Output ngrams of the given <size> from <carrel>"""

	# require
	from re     import search
	import nltk
	
	# initialize
	size         = int( size )
	localLibrary = configuration( 'localLibrary' )
	stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ) ).read().split()

	# read, tokenize, and normalize the text
	text   = open( str( localLibrary/carrel/ETC/CORPUS ) ).read()
	tokens = nltk.word_tokenize( text, preserve_line=True )
	tokens = [ token.lower() for token in tokens if token.isalpha() ]
	
	# create the set of ngrams
	ngrams = list( nltk.ngrams( tokens, size ) )
	
	# filter, conditionally
	if filter :
	
		# initialize and process each ngram
		filtered = []
		for ngram in ngrams :
			
			# check and update
			if search( filter, ' '.join( ngram ) ) : filtered.append( ngram )
		
		# done
		ngrams = filtered

	# remove stopwords from unigrams or bigrams
	if size < 3 :
	
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
		
	# output; human
	if count :
	
		# initialize a dictionary and process each ngram
		items = {}
		for ngram in ngrams :

			# update the dictionary
			if ngram in items : items[ ngram ] += 1
			else              : items[ ngram ]  = 1

		# sort the dictionary; return the ngrams
		ngrams = sorted( items.items(), key=lambda x:x[ 1 ], reverse=True )
		
		# process each ngram
		for ngram in ngrams :
			
			# create a record and output
			record = str( ngram[ 1 ] ) + '\t' + '\t'.join( list( ngram[ 0 ] ) )
			click.echo( record )
		
	# output raw data, and hope sort, uniq, grep, and less are used
	else :
		for ngram in ngrams : click.echo( "\t".join( list( ngram ) ) )