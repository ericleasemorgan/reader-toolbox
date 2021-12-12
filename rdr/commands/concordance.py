# concordance - given a carrel and a word, output rudimentary keyword-in-context

# require
from rdr import *

# create and/or get the NTTK model
def getNLTKText( carrel ) :

	# configure
	MODEL = 'reader.nltk'

	# require
	from nltk import Text, word_tokenize
	from os   import path, stat
	import    pickle
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	file         = localLibrary/carrel/ETC/MODEL

	# check to see if we've previously been here
	if path.exists( file ) :
	
		# read the model
		with open( file, 'rb' ) as handle : model = pickle.load( handle )	
			
	else :

		# create the model and save it for future use
		corpus = localLibrary/carrel/ETC/CORPUS
		model  = Text( word_tokenize( open( corpus ).read( ) ) )
		with open( file, 'wb' ) as handle : pickle.dump( model, handle )

	# return the model
	return( model )


@click.command( options_metavar='[<options>]' )
@click.option('-w', '--width', default=80, help='number of characters in each line of output')
@click.option('-l', '--lines', default=999, help='number of lines of text to output')
@click.option('-q', '--query', default='love', help='a word for phrase')
@click.argument( 'carrel', metavar='<carrel>' )
def concordance( carrel, query, width, lines ) :

	"""A poor man's search engine.
	
	Given a query, this subcommand will search <carrel> and return a list of results where each result is a set of words to the left of query, the query, and a set of words to the right of query -- a keyword-in-context index. This is useful for answering the question, "What words are used in the same breath as the given word?" The query can be a phrase. Consider creating a word cloud from the output of this command to visualize the "words used in the same breath". 
	
	Examples:
	
	\b
	  rdr concordance homer -q hector
	  rdr concordance homer -q 'hector was'

	See also: rdr ngrams --help"""
	
	# require
	from nltk import Text, word_tokenize

	# sanity checks
	checkForCarrel( carrel )
	checkForPunkt()
	
	# initialize, read, and normalize; ought to save the result for future use
	model = getNLTKText( carrel )
					
	# split query into a list, conditionally
	if ' ' in query : query = query.split( ' ' )
		
	# do the work and output
	lines = model.concordance_list( query, width=width, lines=lines )
	for line in lines : click.echo( line.line )
	