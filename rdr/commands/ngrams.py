
# ngrams - given a study carrel and an integer, output... ngrams

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-q', '--query', type=click.STRING, help="filter results to include the given regular expression")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='where is the study carrel')
@click.option('-s', '--size', default=1, help='denote unigrams, bigrams, trigrams, etc')
@click.argument( 'carrel', metavar='<carrel>' )
def ngrams( carrel, size, query, count, location ) :

	"""Output and list words or phrases found in <carrel>.

	This is almost always the first place to start when doing your analysis.

	Examples:

	\b
	  rdr ngrams homer
	  rdr ngrams -s 2 homer
	  rdr ngrams -s 2 -c homer
	  rdr ngrams -s 2 -c -q love homer
	  rdr ngrams -s 2 -c -q love homer | more
	  rdr ngrams -s 2 -c -q love -l remote sonnets | more

	See also: rdr concordance --help"""

	# require
	from re       import search
	from requests import get
	import nltk

	# branch according to location; local
	if location == 'local' :
	
		# sanity check
		checkForCarrel( carrel )
		
		# read local data
		localLibrary = configuration( 'localLibrary' )
		stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ) ).read().split()
		text         = open( str( localLibrary/carrel/ETC/CORPUS ) ).read()
	
	# remote
	elif location == 'remote' :
	
		# read remote data; needs error checking
		stopwords = get( '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, ETC, STOPWORDS ] ) ).text.split()
		text      = get( '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, ETC, CORPUS ] ) ).text
		
	# error
	else :
	
		# click ought to prevent this, but just in case
		click.echo( "Error: Unknown value for location: { location }. Call Eric.", err=True )
		exit()
			
	# read, tokenize, and normalize the text
	tokens = nltk.word_tokenize( text, preserve_line=True )
	tokens = [ token.lower() for token in tokens if token.isalpha() ]
	
	# create the set of ngrams
	ngrams = list( nltk.ngrams( tokens, size ) )
	
	# filter, conditionally
	if query :
	
		# initialize and process each ngram
		filtered = []
		for ngram in ngrams :
			
			# check and update
			if search( query, ' '.join( ngram ) ) : filtered.append( ngram )
		
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
		
	# power user
	else :
	
		# output raw data, and hope sort, uniq, grep, and less are used
		for ngram in ngrams : click.echo( "\t".join( list( ngram ) ) )

