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

# file system mappings
CORPUS    = 'reader.txt'
DATABASE  = 'reader.db'
ETC       = 'etc'
HTM       = 'htm'
INDEX     = 'index.htm'
MANIFEST  = 'MANIFEST.xml'
STOPWORDS = 'stopwords.txt'
TXT       = 'txt'

# spacy's default model
MODEL = 'en_core_web_sm'

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
		
		
