
# tm - do topic modeling

# require
from rdr import *

def checkForMallet( mallet ) :
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	from requests     import get
	from tempfile     import TemporaryFile
	from zipfile      import ZipFile
	
	# install mallet, conditionally
	if not Path( mallet ).exists() :
	
		click.echo( "MALLET not found. Downoading MALLET... ", err=True )
		response = get( MALLETZIP )

		# initialize a temporary file and write to it
		click.echo( "Saving zip file... ", err=True )
		handle = TemporaryFile()
		handle.write( response.content )

		# unzip the temporary file and close it, which also deletes it
		click.echo( "Unziping zip file... " )
		with ZipFile( handle, 'r' ) as zip : zip.extractall( Path.home() )
		
		# initialize
		click.echo( "Updating configurations... " )
		configurations          = ConfigParser()
		applicationDirectory    = Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
		configurationFile       = applicationDirectory/CONFIGURATIONFILE
		localLibrary            = configuration( 'localLibrary' )
		malletHome              = Path.home()/'mallet'
		configurations[ "RDR" ] = { "localLibrary"  : localLibrary, "malletHome" : malletHome }
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )

		# make mallet executable
		click.echo( "Making MALLET executable... " )
		(malletHome/MALLETBIN).chmod( 0x755 )
		

		# done
		click.echo('''Done. MALLET has been downloaded to your home directory and configured
for future use. You can move MALLET to another location but once you do
so you will need to run 'rdr set -s mallet'.''', err=True )


@click.command( options_metavar='<options>' )
@click.option('-t', '--topics', default=7, help="number of topics to generate")
@click.option('-w', '--words', default=7, help="number of words used to describe topic")
@click.option('-i', '--iterations', default=2400, help="number of iterations")
@click.argument( 'carrel', metavar='<carrel>' )
def tm( carrel, topics, words, iterations ) :

	"""Apply topic modeling against <carrel>.
	
	Topic modeling is the process of enumerating latent themes from a corpus, and it is yet another way to describe a corpus's aboutness. It is suggested you start out small when it comes to the values for -t and -w. Repeat the modeling process and gradually increase the values. Increase the value of -i as the size of your carrel increases. 
	
	Remember, there is no such thing as the correct value of -t. After all, exactly how many things is the sum of Shakespeare's works about?
	
	Examples:
	
	\b
	  rdr tm homer
	  rdr tm -t 7 -w 12 homer
	  rdr tm -t 7 -w 24 -i 4800 homer"""

	# configure
	HTML       = 'topic-model.htm'
	RANDOMSEED = 42
	WORKERS    = 6

	# require
	from gensim                 import corpora
	from gensim.models.wrappers import LdaMallet, ldamallet
	from nltk                   import word_tokenize
	from os                     import environ
	from pathlib                import Path
	import pyLDAvis
	import pyLDAvis.gensim_models
	import webbrowser

	# sanity checks
	checkForCarrel( carrel )
	checkForMallet( str( configuration( 'malletHome' ) ) + '/' + MALLETBIN )
	checkForPunkt()

	# initialize
	localLibrary = configuration( 'localLibrary' )
	mallet       = str( configuration( 'malletHome' ) ) + '/' + MALLETBIN
	stopwords    = open( localLibrary/carrel/ETC/STOPWORDS ).read().split()
	files        = Path( localLibrary/carrel/TXT ).glob( '*.txt' )

	# create a list of normalized texts
	texts = []
	for file in files :

		tokens = open( file ).read()
		tokens = word_tokenize( tokens )
		tokens = [ token.lower() for token in tokens if token.isalpha() ]
		tokens = [ token for token in tokens if token not in stopwords ]
		texts.append( tokens )

	# create a dictionary and term-document matrix
	id2word = corpora.Dictionary( texts )
	corpus  = [ id2word.doc2bow( text ) for text in texts ]

	# use mallet to model the data and convert it to something gensim can understand
	model = LdaMallet( mallet, corpus=corpus, num_topics=topics, id2word=id2word, workers=WORKERS, iterations=iterations, random_seed=RANDOMSEED )
	model = ldamallet.malletmodel2ldamodel( model )

	# create, save, and open the visualization
	html          = str( localLibrary/carrel/HTM/HTML )
	visualization = pyLDAvis.gensim_models.prepare( model, corpus, id2word, sort_topics=True, R=words )
	pyLDAvis.save_html( visualization, html )
	webbrowser.open( 'file://' + html )
