
# tm - do topic modeling

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.option('-t', '--topics', default=7, help="number of topics to generate")
@click.option('-w', '--words', default=7, help="number of words used to describe topic")
@click.option('-i', '--iterations', default=2400, help="number of iterations")
@click.argument( 'carrel', metavar='<carrel>' )
def tm( carrel, topics, words, iterations ) :

	"""Apply topic modeling against <carrel>
	
	Topic modeling is the process of enumerating latent themes from a corpus, and it is yet another way to describe a corpus's aboutness. It is suggested you start out small when it comes to the values for --topics and --words. Repeat the modeling process an gradually increase the values."
	
	Example: rdr tm homer -t 3 -d 3
	"""

	# configure
	HTML       = 'topic-model.htm'
	RANDOMSEED = 42
	WORKERS    = 6
	MALLETBIN  = 'bin/mallet'

	# require
	from gensim                 import corpora
	from gensim.models.wrappers import LdaMallet, ldamallet
	from nltk                   import word_tokenize
	from os                     import environ
	from pathlib                import Path
	import pyLDAvis
	import pyLDAvis.gensim_models
	import webbrowser
	
	# sanity check
	checkForCarrel( carrel )
	
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
