
# ngrams - given a study carrel and an integer, output... ngrams

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-q', '--query',      type=click.STRING, help="filter results to include the given regular expression")
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

	# configure
	LIMIT = 200
	
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
		stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ), encoding='utf-8' ).read().split()
		text         = open( str( localLibrary/carrel/ETC/CORPUS ), encoding='utf-8' ).read()
	
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
		frequencies = {}
		for ngram in ngrams :

			# update the dictionary
			if ngram in frequencies : frequencies[ ngram ] += 1
			else                    : frequencies[ ngram ]  = 1

		# sort the dictionary
		ngrams = sorted( frequencies.items(), key=lambda x:x[ 1 ], reverse=True )
		
		if not wordcloud :
		
			# process each ngram
			for ngram in ngrams :
			
				# create a record and output
				record = '\t'.join( list( ngram[ 0 ] ) ) + '\t' + str( ngram[ 1 ] )
				click.echo( record )
				
		else :
		
			# limit the number of ngrams; we can't visualize a huge number
			ngrams = ngrams[ :LIMIT ]
			
			# coerce the result into a dictionary of frequencies
			frequencies = {}
			for ngram in ngrams : frequencies[ ' '.join( ngram[ 0 ] ) ] = ngram[ 1 ]
			
			# simply output
			if not save : cloud( frequencies )

			# save to the corresponding figures directory
			else :
			
				# unigrams
				if size == 1 :
				
					# configure and save
					file = localLibrary/carrel/FIGURES/UNIGRAMSCLOUD
					cloud( frequencies, file=file )
					
				# bigrams
				elif size == 2 :
				
					# configure and save
					file = localLibrary/carrel/FIGURES/BIGRAMSCLOUD
					cloud( frequencies, file=file )
				
				# unsupported
				else : click.echo( "The save option is only valid for unigrams and bigrams; there is no default location for anything else.", err=True )
				
				
			
	# power user
	else :
	
		# output raw data, and hope sort, uniq, grep, and less are used
		for ngram in ngrams : click.echo( "\t".join( list( ngram ) ) )

