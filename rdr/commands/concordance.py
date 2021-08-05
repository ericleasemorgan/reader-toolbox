
# concordance - given a carrel and a word, output rudimentary keyword-in-context

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'query', metavar='<query>'  )
def concordance( carrel, query ) :

	"""Output matching lines from <carrel> where <query> is a word or phrase
	
	Developed in the 12th Century, concordancing is the oldest of text mining tools and the poor man's search engine. Sometimes it is called a keyword-in-context (KWIC) index. Given <query>, this is a quick and easy way to see how it is used in the same breath as other words. Use 'rdr ngrams' to identify words or phrases of interest.
	
	Examples:
	
	\b
	  * rdr concordance homer hector
	  * rdr concordance homer 'hector was'
	
	See also: rdr ngrams"""

	# configure
	WIDTH = 80
	LINES = 9999
	
	# require
	from nltk import Text, word_tokenize

	# initialize, read, and normalize; ought to save the Text object for future use
	localLibrary = configuration( 'localLibrary' )
	corpus       = localLibrary/carrel/ETC/CORPUS
	text         = Text( word_tokenize( open( corpus ).read( ) ) )
	
	if ' ' in query : query = query.split( ' ' )
		
	# do the work and output
	concordance = text.concordance_list( query, width=WIDTH, lines=LINES )
	for line in concordance : click.echo( line.line )
	