
# require
from rdr import *
import nltk

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

	file   = localLibrary + '/' + carrel + '/' + ETC + '/' + CORPUS
	ngrams = list( nltk.ngrams( open( file ).read().split(), int( n ) ) )
	for ngram in ngrams : click.echo( "\t".join( list( ngram ) ) )