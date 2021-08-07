
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

# spacy's default model
MODEL         = 'en_core_web_sm'

# mallet
MALLETHOME = "/Users/eric/Desktop/reader-mallet"
MODELDIR   = MALLETHOME + '/' + 'tmp'
VECTORS    = 'model.vec'

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
