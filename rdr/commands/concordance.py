
# concordance - given a carrel and a word, output rudimentary keyword-in-context

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.option('-w', '--width', default=80, help='number of characters in each line of output')
@click.option('-l', '--lines', default=999, help='number of lines of text to output')
@click.option('-q', '--query', default='love', help='output in a more human-readable form')
@click.argument( 'carrel', metavar='<carrel>' )
def concordance( carrel, query, width, lines ) :

	"""Output matching lines from <carrel> where <query> is a word or phrase
	
	Developed in the 12th Century, concordancing is the oldest of text mining tools and the poor man's search engine. Sometimes it is called a keyword-in-context (KWIC) index. Given <query>, this is a quick and easy way to see how it is used in the same breath as other words. Use 'rdr ngrams' to identify words or phrases of interest.
	
	Examples:
	
	\b
	  * rdr concordance homer hector
	  * rdr concordance homer 'hector was'
	
	See also: rdr ngrams"""
	
	# require
	from nltk import Text, word_tokenize

	# sanity check
	checkForCarrel( carrel )

	# initialize and read
	localLibrary = configuration( 'localLibrary' )
	corpus       = localLibrary/carrel/ETC/CORPUS
	
	# try to create an NLTK Text object; normalize, and ought to save the result for future use
	try : text = Text( word_tokenize( open( corpus ).read( ) ) )
	
	# error
	except LookupError :
		
		# debug and get input
		click.echo( "Oops! A Python resource called 'punkt' does not seem to be installed. Do you want to install it now? [y/n]", err=True )
		c = click.getchar()
		click.echo()

		# branch accordingly; yes
		if c == 'y' :

			# require and do the work; would be nice to save it in a less out-of-the way location
			import nltk
			nltk.download( 'punkt' )
			
			# debug
			click.echo( "Thank you. Please run the concordance command again. If the error persists, then call Eric.", err=True )
			
		# no
		elif c == 'n' : click.echo( "Okay, but installing punkt is necessary for this function to work. You'll be asked again next time.", err=True )

		# error
		else : click.echo( '???' )

		# done
		exit()
				
	# split query into a list, conditionally
	if ' ' in query : query = query.split( ' ' )
		
	# do the work and output
	lines = text.concordance_list( query, width=width, lines=lines )
	for line in lines : click.echo( line.line )
	