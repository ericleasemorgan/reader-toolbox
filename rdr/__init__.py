"""
a command-line tool for interacting with Distant Reader study carrels

rdr -- shorthand for Reader Toolbox -- is a command-line tool for
interacting with Distant Reader study carrels.

The Distant Reader (https:/distantreader.org) takes an almost arbitrary
amount of unstructured data (text) as input, does text mining and
natural language processing against it, and outputs sets of structured
data affectionatly called "study carrels".

As you may or may not know, a library study carrel is a little table or
room assigned to individual students. The students are then authorized
to collect thing from around the library, bring them to their study
carrel, organize them in any way they so desire, and persue their
research. Distant Reader study carrels are a modern-day version of the
venerable library study carrel.

This tool -- rdr -- enables the student, researcher, or scholar to
quickly and easily digest the content of carrels to address questions
from the mundane to the sublime. 

Eric Lease Morgan <emorgan@nd.edu>
(c) University of Notre Dame; distributed under a GNU Public License
"""

# configure; name of application, basename of configuration file, and default basename of local library
APPLICATIONDIRECTORY = 'rdr'
CONFIGURATIONFILE    = '.rdrrc'
READERLIBRARY        = 'reader-library'
MALLETHOME           = 'mallet'
TIKAHOME             = 'tika-server.jar'

# remote library
REMOTELIBRARY = 'http://library.distantreader.org'
CARRELS       = 'carrels'

# file system mappings
CORPUS              = 'reader.txt'
DATABASE             = 'reader.db'
ETC                  = 'etc'
HTM                  = 'htm'
INDEX                = 'index.htm'
MANIFEST             = 'MANIFEST.xml'
STOPWORDS            = 'stopwords.txt'
TXT                  = 'txt'
CACHE                = 'cache'
PROVENANCE           = 'provenance.tsv'
METADATA             = 'metadata.csv'
INDEX                = 'index.htm'
BIBLIOGRAPHY         = 'bibliography.txt'
SIZESBOXPLOT         = 'sizes-boxplot.png'
SIZESHISTOGRAM       = 'sizes-histogram.png'
READABILITYHISTOGRAM = 'readability-histogram.png'
READABILITYBOXPLOT   = 'readability-boxplot.png'
CLUSTERDENDROGRAM    = 'cluster-dendrogram.png'
CLUSTERCUBE          = 'cluster-cube.png'
FIGURES              = 'figures'
KEYWORDSCLOUD        = 'keywords-cloud.png'
UNIGRAMSCLOUD        = 'unigrams-cloud.png'
BIGRAMSCLOUD         = 'bigrams-cloud.png'


# spacy langauge model
MODEL = 'en_core_web_sm'

# mallet
MALLETZIP = 'http://library.distantreader.org/apps/mallet.zip'
MALLETBIN = 'bin/mallet'

# tika server
TIKADOWNLOAD = 'http://library.distantreader.org/apps/tika-server.jar'


# require
import click


# create or re-create the preferences/settings
def initializeConfigurations() :

	# require
	from configparser import ConfigParser
	from pathlib      import Path

	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE

	# define defaults, and...
	configurations[ "RDR" ] = { "localLibrary" : Path.home()/READERLIBRARY, 
								"malletHome"   : Path.home()/MALLETHOME,
								"tikaHome"     : Path.home()/TIKAHOME }

	# save them
	with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )

	# create the library directory
	( Path.home()/READERLIBRARY ).mkdir( exist_ok=True )


# read configurations
def configuration( name ) :

	# require
	from configparser import ConfigParser
	from pathlib      import Path

	# initialize
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE	
	configurations       = ConfigParser()
	
	# read configurations file
	configurations.read( str( configurationFile ) )
	
	# get configurations
	localLibrary = configurations[ 'RDR' ][ 'localLibrary' ]
	malletHome   = configurations[ 'RDR' ][ 'malletHome' ] 
	tikaHome     = configurations[ 'RDR' ][ 'tikaHome' ] 
	
	# done
	if   name == 'localLibrary' : return( Path( localLibrary ) )
	elif name == 'malletHome'   : return( Path( malletHome ) )
	elif name == 'tikaHome'     : return( Path( tikaHome ) )
	else :
	
		# unknown configuration
		click.echo( f"Error: Unknown value for configuration name: { name }. Call Eric.", err=True )
		exit()
		

# handle model not found error
def modelNotFound() :
	
	# notify
	click.echo( "Error: Langauge model not found.", err=True )
	click.echo()
	click.echo( f"This functions requires a spaCy langauge model ({ MODEL}) to be installed. This only has to be done once, and after the model has been installed you can run the command again.", err=True )
	click.echo()
	click.echo( 'Do you want to install the model now? [yn] ', err=True, nl=False )
	
	# get input
	c = click.getchar()
	click.echo()
	
	# branch accordingly; yes
	if c == 'y' :

		# require and do the work
		from os import system
		system( 'python -m spacy download ' + MODEL )
	
	# no
	elif c == 'n' : click.echo( "Okay, but installing the model is necessary for this function to work. You'll be asked again next time.", err=True )

	# error
	else : click.echo( '???' )
	
	# done
	exit()

# make sure the NLTK is sane
def checkForPunkt() :

	# require
	import nltk
		
	try : nltk.data.find( 'tokenizers/punkt' )
	except LookupError : 
		click.echo( "Installing punkt. This ought to only happen once.", err=True )
		nltk.download( 'punkt', quiet=True )


# make sure a study carrel exists
def checkForCarrel( carrel ) :
	
	# initialize and do the work
	directory = configuration( 'localLibrary' )/carrel
	if not directory.is_dir() :
		
		# error
		click.echo( ('''
  WARNING: The carrel, %s, does not seem to be in your local
  library. Are you sure you entered its name correctly? Try 'rdr
  catalog' to make sure.

  Alternatively, maybe you have moved the library and your settings
  are not up-to-date. If so, then use 'rdr get -s local' and/or
  'rdr set -s local' to rectify the issue.
''' % carrel ), err=True )
		exit()

	
# create a word cloud
def cloud( frequencies, **kwargs ) :

	# configure
	HEIGHT = 960
	WIDTH  = 1280
	COLOR  = 'white'
	
	# require
	from wordcloud           import WordCloud
	import matplotlib.pyplot as plt

	# read optional arguments
	file = kwargs.get( 'file', None )

	# build the cloud
	wordcloud = WordCloud( width=WIDTH, height=HEIGHT, background_color=COLOR )
	wordcloud.generate_from_frequencies( frequencies )

	# save
	if file : wordcloud.to_file( file )
		
	# display
	else :
	
		# plot
		plt.figure()
		plt.imshow( wordcloud )
		plt.axis( "off" )
		plt.show()

	# done
	return True




