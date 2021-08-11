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

# configure; name of application and basename of configuration file
APPLICATIONDIRECTORY = 'rdr'
CONFIGURATIONFILE    = '.rdrrc'

# remote library
REMOTELIBRARY = 'http://library.distantreader.org'
CARRELS       = 'carrels'

# local carrel file system
ETC       = 'etc'
TXT       = 'txt'
CORPUS    = 'reader.txt'
STOPWORDS = 'stopwords.txt'
DATABASE  = 'reader.db'
INDEX     = 'index.htm'
HTM       = 'htm'
MANIFEST  = 'MANIFEST.xml'

# spacy's default model
MODEL         = 'en_core_web_sm'

# require
import click

# read configurations
def configuration( name ) :

	# require
	from configparser import ConfigParser
	from pathlib      import Path

	applicationDirectory = Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'RDR' ][ 'localLibrary' ] 
	malletHome     = configurations[ 'RDR' ][ 'malletHome' ] 
	
	# done
	if   name == 'localLibrary'  : return( Path( localLibrary ) )
	elif name == 'malletHome'    : return( Path( malletHome ) )
	else :
		click.echo( f"Error: Unknown value for configuration name: { name }. Call Eric.", err=True )
		exit()
		
		
# given a carrel, return a spacy doc
def carrel2doc( carrel ) :

	# configure
	PICKLE = 'reader.bin'

	# require
	from os    import path, stat
	from spacy import load
	import textacy
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	pickle       = localLibrary/carrel/ETC/PICKLE

	# check to see if we've previously been here
	if path.exists( pickle ) :
		
		# read the pickle file
		doc = next( textacy.io.spacy.read_spacy_docs( pickle ) )
	
	# otherwise
	else :
	
		# warn
		click.echo( 'Reading and formatting model data for future use. This may take many minutes...', err=True )

		# create a doc
		file           = localLibrary/carrel/ETC/CORPUS
		text           = open( str( file ) ).read()
		size           = ( stat( file ).st_size ) + 1
		nlp            = load( MODEL )
		nlp.max_length = size
		doc            = nlp( text )

		# save it for future use
		textacy.io.spacy.write_spacy_docs( doc, filepath=pickle )

	# done
	return doc


# requirements
#from mpl_toolkits.mplot3d import Axes3D
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.manifold import MDS
#from sklearn.metrics.pairwise import cosine_similarity
#from tempfile import TemporaryFile
#from zipfile  import ZipFile
#import matplotlib.pyplot as plt
#import networkx as nx
#import os
#import pathlib
#import requests
#import spacy
#import sys
#import textacy
