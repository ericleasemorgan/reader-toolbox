
# tm - do topic modeling

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.option('-t', '--topics', default=7, help="number of topics to generate")
@click.option('-d', '--dimensions', default=7, help="number of words used to describe topic")
@click.option('-i', '--iterations', default=2400, help="number of iterations")
@click.argument( 'carrel', metavar='<carrel>' )
def tm( carrel, topics, dimensions, iterations ) :

	"""Apply topic modeling to <carrel>"""

	# configure
	HTML       = 'topic-model.htm'
	MALLETHOME = '/Users/eric/Desktop/reader-mallet'
	MALLETPATH = '/Users/eric/Desktop/reader-mallet/bin/mallet'
	RANDOMSEED = 42
	WORKERS    = 6

	# require
	from gensim.models.wrappers import LdaMallet, ldamallet
	from nltk                   import word_tokenize
	from os                     import environ
	from pathlib                import Path
	import gensim.corpora       as     corpora
	import pyLDAvis
	import pyLDAvis.gensim_models
	import webbrowser
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	stopwords    = open( localLibrary/carrel/ETC/STOPWORDS ).read().split()
	files        = Path( localLibrary/carrel/TXT ).glob( '*.txt' )
	#environ.update( { 'MALLET_HOME': MALLETHOME } )

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

	# use mallet to model the data, and convert it to something gensim can understand
	model = LdaMallet( MALLETPATH, corpus=corpus, num_topics=topics, id2word=id2word, workers=WORKERS, iterations=iterations, random_seed=RANDOMSEED )
	model = ldamallet.malletmodel2ldamodel( model )

	# create, save, and open the visualization
	html = str( localLibrary/carrel/HTM/HTML )
	visualization = pyLDAvis.gensim_models.prepare( model, corpus, id2word, sort_topics=True, R=dimensions )
	pyLDAvis.save_html( visualization, html )
	webbrowser.open( 'file://' + html )
