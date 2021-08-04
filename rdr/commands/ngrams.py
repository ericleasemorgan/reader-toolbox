
# require
from rdr import *

# initialize
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'n', metavar='<n>' )

# ngrams
def ngrams( carrel, n ) :

	"""Given a <carrel>, output ngrams of size <n>"""

	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 
	localLibrary   = pathlib.Path( localLibrary )
	file           = localLibrary / carrel / ETC / CORPUS
	
	data   = open( str( file ) ).read()
	tokens = nltk.word_tokenize( data, preserve_line=True )
	tokens = [ token.lower() for token in tokens if token.isalpha() ]
	
	stopwords = open( str( localLibrary/carrel/ETC/'stopwords.txt' ) ).read().split()
	
	ngrams = list( nltk.ngrams( tokens, int( n ) ) )
	mylist = []
	if int( n ) < 3 :
		for ngram in ngrams :

			found = False
			for index, token in enumerate( ngram ) :

				if ngram[ index - 1 ] in stopwords : found = True
	
			if not found : mylist.append( ngram )
	else : mylist = ngrams
	
	for ngram in mylist : click.echo( "\t".join( list( ngram ) ) )