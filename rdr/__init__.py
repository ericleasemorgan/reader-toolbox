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
NOTEBOOKSHOME        = 'reader-notebooks'

# remote library
REMOTELIBRARY = 'http://library.distantreader.org'
CARRELS       = 'carrels'

# documentation
DOCUMENTATION = 'https://reader-toolbox.readthedocs.io'

# file system mappings
CORPUS               = 'reader.txt'
COLLOCATIONS         = 'reader.gml'
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
BIBLIOGRAPHYTEXT     = 'bibliography.txt'
BIBLIOGRAPHYHTML     = 'bibliography.htm'
BIBLIOGRAPHYJSON     = 'bibliography.json'
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
ENTITIESANY          = 'entities-any.png'
ENTITIESPERSON       = 'entities-person.png'
ENTITIESGPE          = 'entities-gpe.png'
ENTITIESORG          = 'entities-org.png'
POSNOUN              = 'pos-noun.png'
POSVERB              = 'pos-verb.png'
POSPRON              = 'pos-pronoun.png'
POSADJ               = 'pos-adjective.png'
POSADV               = 'pos-adverb.png'
POSPROPN             = 'pos-propernoun.png'


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
	configurations[ "RDR" ] = { "localLibrary"  : Path.home()/READERLIBRARY, 
								"malletHome"    : Path.home()/MALLETHOME,
								"notebooksHome" : Path.home()/NOTEBOOKSHOME,
								"tikaHome"      : Path.home()/TIKAHOME }

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
	localLibrary  = configurations[ 'RDR' ][ 'localLibrary' ]
	malletHome    = configurations[ 'RDR' ][ 'malletHome' ] 
	tikaHome      = configurations[ 'RDR' ][ 'tikaHome' ] 
	notebooksHome = configurations[ 'RDR' ][ 'notebooksHome' ] 
	
	# done
	if   name == 'localLibrary'  : return( Path( localLibrary ) )
	elif name == 'malletHome'    : return( Path( malletHome ) )
	elif name == 'tikaHome'      : return( Path( tikaHome ) )
	elif name == 'notebooksHome' : return( Path( notebooksHome ) )
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


# read and parse provenance data
def provenance( carrel, field ) :

	# initialize
	locallibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel )

	# read provenance file
	with open( locallibrary/carrel/PROVENANCE ) as handle : provenance = handle.read().split( '\t' )
	
	# parse it
	process     = provenance[ 0 ]
	originalID  = provenance[ 1 ]
	dateCreated = provenance[ 2 ]
	timeCreated = provenance[ 3 ]
	creator     = provenance[ 4 ]
	input       = provenance[ 5 ][:-1]

	# map
	if field   == 'process'     : value = process
	elif field == 'originalID'  : value = originalID
	elif field == 'dateCreated' : value = dateCreated
	elif field == 'timeCreated' : value = timeCreated
	elif field == 'creator'     : value = creator
	elif field == 'input'       : value = input
	
	# done
	return value
	
	
# return various extents
def extents( carrel, type ) :

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row

	# get extents
	sql = 'SELECT COUNT( id ) AS items, SUM( words ) AS words, AVG( flesch ) AS flesch FROM bib;'
	rows = connection.execute( sql )
	for row in rows :

		items  = row[ 'items' ]
		words  = row[ 'words' ]
		flesch = str( int( row[ 'flesch' ] ) )

	if type == 'items'    : value = items
	elif type == 'words'  : value = words
	elif type == 'flesch' : value = flesch
	
	return value


# output a rudimentary bibliography
def bibliography( carrel, format='text', save=False ) :

	# require
	import sqlite3
	from pathlib import Path
	import json
	
	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row

	# query database
	sql  = '''SELECT b.id, b.words, b.extension, b.flesch, b.author, b.title, b.date, GROUP_CONCAT( LOWER( w.keyword ), '; ') AS keywords, b.summary
			  FROM bib AS b, wrd AS w
			  WHERE b.id = w.id
			  GROUP BY b.id
			  ORDER BY b.id, LOWER( b.author );'''
	rows  = connection.execute( sql )
	rows  = rows.fetchall()
	connection.close()

	# branch according to format
	if format   == 'json' : bibliography = json.dumps( [ dict( row ) for row in rows ] )
		
	elif format == 'text' or format == 'html' :
	
		# initialize
		total = len( rows )
		bibliography = ''
		items = ''
		template = "<html><head><title>Bibliography</title></head><body style='margin:7%'><h1>Bibliography</h1><ol>##ITEMS##</ol></body></html>"
		
		# process each row
		for item, row in enumerate( rows ) :

			# parse
			id        = str( row[ 'id' ] )
			author    = row[ 'author' ]
			title     = row[ 'title' ]
			date      = row[ 'date' ]
			words     = row[ 'words' ]
			flesch    = row[ 'flesch' ]
			summary   = row[ 'summary' ]
			keywords  = row[ 'keywords' ]

			# normalize; unescape
			if summary : summary = summary.replace( "''", "'" )
	
			# build cache and plain text
			cache = str( locallibrary/carrel/CACHE/id ) + row[ 'extension' ]
			text  = str( locallibrary/carrel/TXT/id )   + '.txt'
	
			if format == 'text' :
			
				# build the bibliography
				bibliography = bibliography + ( '        item: #%s of %s\n' % ( str( item + 1 ), total ) )
				bibliography = bibliography + ( '          id: %s\n' % id )
				bibliography = bibliography + ( '      author: %s\n' % author )
				bibliography = bibliography + ( '       title: %s\n' % title )
				bibliography = bibliography + ( '        date: %s\n' % date )
				bibliography = bibliography + ( '       words: %s\n' % words )
				bibliography = bibliography + ( '      flesch: %s\n' % flesch )
				bibliography = bibliography + ( '     summary: %s\n' % summary )
				bibliography = bibliography + ( '    keywords: %s\n' % keywords )
				bibliography = bibliography + ( '       cache: %s\n' % cache )
				bibliography = bibliography + ( '  plain text: %s\n' % text )
				bibliography = bibliography + '\n'
	
			else :
			
				item = '<ul>'
				item = item + '<li>' + ( 'author: %s'    % author )   + '</li>'
				item = item + '<li>' + ( 'title: %s'     % title )    + '</li>'
				item = item + '<li>' + ( 'date: %s'      % date )     + '</li>'
				item = item + '<li>' + ( 'words: %s'     % words )    + '</li>'
				item = item + '<li>' + ( 'flesch: %s'    % flesch )   + '</li>'
				item = item + '<li>' + ( 'summary: %s'   % summary )  + '</li>'
				item = item + '<li>' + ( 'keywords: %s'  % keywords ) + '</li>'
				item = item + '<li>' + ( 'cache: %s'      % cache )   + '</li>'
				item = item + '<li>' + ( 'plain text: %s' % text )    + '</li>'
				item = item + '</ul>'
				
				items = items + "<li>" + id + item + "</li>"
				
	if format == 'html' : bibliography = template.replace( '##ITEMS##', items )
	
	if save :

		if format == 'text' : file = locallibrary/carrel/ETC/BIBLIOGRAPHYTEXT
		if format == 'html' : file = locallibrary/carrel/ETC/BIBLIOGRAPHYHTML
		if format == 'json' : file = locallibrary/carrel/ETC/BIBLIOGRAPHYJSON
		
		with open( file, 'w', encoding='utf-8' ) as handle : handle.write( bibliography )
		
	else : return bibliography
	

# get email addresses
def addresses( carrel, count=False, like=None ) :

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# dump a sorted list of all email addresses
	if not count :

		# articulate sql
		if like :
		
			sql = ( '''SELECT DISTINCT( LOWER( address ) ) AS address
			           FROM adr
			           WHERE address LIKE "%s"
			           ORDER BY address;''' % ('%' + like + '%' ) )
			
		else :
		
			sql  = '''SELECT DISTINCT( LOWER( address ) ) AS address
			          FROM adr
			          ORDER BY address;'''

		# do the work and build the result
		rows = connection.execute( sql )
		for row in rows : items.append( row[ 'address' ]  )

	# count and tabulate the dump
	else :
	
		# articulate sql
		if like :
		
			sql = ( '''SELECT LOWER( address ) AS address, COUNT( LOWER( address ) ) AS count
			           FROM adr
			           WHERE address LIKE "%s"
			           GROUP BY LOWER( address )
			           ORDER BY count DESC, address;''' % ('%' + like + '%' ) )
			
		else :
		
			sql  = '''SELECT LOWER( address ) AS address, COUNT( LOWER( address ) ) AS count
			          FROM adr
			          GROUP BY LOWER( address )
			          ORDER BY count DESC, address;'''

		# do the work and build the result
		rows = connection.execute( sql )
		for row in rows : items.append( "\t".join( [ row[ 'address' ], str( row[ 'count' ] ) ] ) )		

	# clean up and done
	connection.close()
	return '\n'.join( items )


def urls( carrel, select='url', count=False, like=None ) :

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# dump a sorted list of all urls
	if select == 'url' :
	
		# don't count
		if not count :
		
			# simple filter
			if like :
			
				# articulate sql
				sql = ( '''SELECT DISTINCT( url ) AS url
				           FROM url
				           WHERE url LIKE "%s"
				           ORDER BY url;''' % ( '%' + like + '%' ) )

			# just dump; articulate sql
			else : sql = 'SELECT DISTINCT( url ) AS url FROM url ORDER BY url;'

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : items.append( row[ 'url' ] )

		# count
		else :
		
			# simple filtering
			if like :
			
				# articulate sql
				sql = ( '''SELECT DISTINCT( url ) AS url, COUNT( DISTINCT( url ) ) AS count
				           FROM url
				           WHERE url LIKE '%s'
				           GROUP BY url
				           ORDER BY count DESC;''' % ( '%' + like + '%' ) )
				            
			# no filtering
			else :

				# articulate sql
				sql = '''SELECT DISTINCT( url ) AS url, COUNT( DISTINCT( url ) ) As count
				         FROM url
				         GROUP BY url
				         ORDER BY count DESC;'''

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'url' ], str( row[ 'count' ] ) ] ) )
			
	# domains; count and tabulate the dump
	else :
	
		# no counting
		if not count :
		
			# filter
			if like :
			
				# articulate sql, search, and output
				sql = ( '''SELECT LOWER( DISTINCT( domain ) ) AS domain
				           FROM url
				           WHERE url LIKE '%s'
				           ORDER BY domain;''' % ( '%' + like + '%' ) )

			# no filtering
			else : sql = 'SELECT LOWER( DISTINCT( domain ) ) AS domain FROM url ORDER BY domain;'

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : item.append( row[ 'domain' ] )
		
		# count and tabulate
		else :
		
			# filter
			if like :
			
				# articulate sql, search, and output
				sql = ( '''SELECT LOWER( DISTINCT( domain ) ) AS domain, COUNT( LOWER( DISTINCT( domain ) ) ) AS count
				           FROM url
				           WHERE domain LIKE '%s'
				           GROUP BY domain
				           ORDER BY count DESC, domain;''' % ( '%' + like + '%' ) )

			# no filtering
			else :
			
				# articulate sql, search, and output
				sql = '''SELECT LOWER( DISTINCT( domain ) ) AS domain, COUNT( LOWER( DISTINCT( domain ) ) ) AS count
				         FROM url
				         GROUP BY domain
				         ORDER BY count DESC, domain;'''
				         
			# do the work and output
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'domain' ], str( row[ 'count' ] ) ] ) )
			
	# clean up and done
	connection.close()
	return '\n'.join( items )


def keywords( carrel, count=False, wordcloud=False, save=False ) :

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# dump a sorted list of all keywords
	if not count :

		# articulate sql, search, and output
		sql  = 'SELECT DISTINCT( LOWER( keyword ) ) AS keyword FROM wrd ORDER BY LOWER( keyword );'
		rows = connection.execute( sql )
		for row in rows : items.append( row[ 'keyword' ] )

	# count and tabulate the dump
	else :
	
		# articulate sql, search, and output
		sql  = 'SELECT LOWER( keyword ) AS keyword, COUNT( LOWER( keyword ) ) AS count FROM wrd GROUP BY LOWER( keyword ) ORDER BY count DESC, keyword;'
		rows = connection.execute( sql )
		
		# output a simple list
		if not wordcloud :
			
			for row in rows : 
		
				# output, conditionally; weird
				if row[ 'keyword' ] : items.append( "\t".join( [ row[ 'keyword' ], str( row[ 'count' ] ) ] ) )			

		# output a word cloud
		else :
			
			# create a list of frequencies
			frequencies = {}
			for row in rows :
			
				if row[ 'keyword' ] : frequencies[ row[ 'keyword' ] ] = row[ 'count' ]
			
			if not save : cloud( frequencies )
			else :
			
				file = locallibrary/carrel/FIGURES/KEYWORDSCLOUD
				cloud( frequencies, file=file )

	# clean up and done; the result might be empty, which is sort of bogus
	connection.close()
	return '\n'.join( items )


# create and/or get the NTTK model
def getNLTKText( carrel ) :

	# configure
	MODEL = 'reader.nltk'

	# require
	from nltk import Text, word_tokenize
	from os   import path, stat
	import    pickle
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	file         = localLibrary/carrel/ETC/MODEL

	# check to see if we've previously been here
	if path.exists( file ) :
	
		# read the model
		with open( file, 'rb' ) as handle : model = pickle.load( handle )	
			
	else :

		# create the model and save it for future use
		corpus = localLibrary/carrel/ETC/CORPUS
		model  = Text( word_tokenize( open( corpus ).read( ) ) )
		with open( file, 'wb' ) as handle : pickle.dump( model, handle )

	# return the model
	return( model )


# poor man's search engine
def concordancing( carrel, query='love', width=80, lines=999 ) :

	# require
	from nltk import Text, word_tokenize

	# sanity checks
	checkForCarrel( carrel )
	checkForPunkt()
	
	# initialize, read, and normalize; ought to save the result for future use
	model = getNLTKText( carrel )
	items = []			
			
	# split query into a list, conditionally
	if ' ' in query : query = query.split( ' ' )
		
	# do the work and output
	lines = model.concordance_list( query, width=width, lines=lines )
	for line in lines : items.append( line.line )
	
	# done
	return '\n'.join( items )


# get sizes (measured in words) of documents
def size( carrel, sort='words', output='list', save=False ) :

	# configure
	WORDS   = 'SELECT id, words FROM bib ORDER BY words DESC'
	ID      = 'SELECT id, words FROM bib ORDER BY id ASC'
	COLUMNS = [ 'sizes in words' ]
	
	# require
	import matplotlib.pyplot as plt
	import pandas as pd
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# find all rows
	if sort == 'words' : rows = connection.execute( WORDS )
	else               : rows = connection.execute( ID )
		
	# branch according to given output; simple list
	if output == 'list' :
	
		# process each row; output tab-delimited list
		for row in rows : items.append( '\t'.join( [ str( row[ 'id' ] ), str( row[ 'words' ] ) ]) )   
   
	# output charts
	else :
			
		# create a simple list of words, and store it in a dataframe
		records = []
		for row in rows : records.append( int( row[ 'words' ] ) )
		df = pd.DataFrame( records, columns=COLUMNS )

		# initialize the plot
		figure, axis = plt.subplots()
		
		# plot
		if output == 'histogram' : 
		
			df.hist( ax=axis )
			if save : plt.savefig( locallibrary/carrel/FIGURES/SIZESHISTOGRAM )
			else    : plt.show()

		else :
		
			df.boxplot( ax=axis )		
			if save : plt.savefig( locallibrary/carrel/FIGURES/SIZESBOXPLOT )
			else    : plt.show()
		
	# clean up
	connection.close()
	return '\n'.join( items )


# get readability scores
def flesch( carrel, sort='score', output='list', save=False) :

	# configure
	SCORE   = 'SELECT id, flesch FROM bib ORDER BY flesch DESC'
	ID      = 'SELECT id, flesch FROM bib ORDER BY id ASC'
	COLUMNS = [ 'readability' ]
	
	# require
	import matplotlib.pyplot as plt
	import pandas as pd
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# find all rows
	if sort == 'score' : rows = connection.execute( SCORE )
	else               : rows = connection.execute( ID )
		
	# branch according to given output; simple list
	if output == 'list' :
	
		# process each row; output tab-delimited list
		for row in rows : items.append( '\t'.join( [ row[ 'id' ], str( row[ 'flesch' ] ) ] ) )   
   
	# output charts
	else :
			
		# create a simple list of words, and store it in a dataframe
		records = []
		for row in rows : records.append( int( row[ 'flesch' ] ) )
		df = pd.DataFrame( records, columns=COLUMNS )

		# initialize the plot
		figure, axis = plt.subplots()

		# plot
		if output == 'histogram' : 
		
			df.hist( ax=axis )
			if save : plt.savefig( locallibrary/carrel/FIGURES/READABILITYHISTOGRAM )
			else    : plt.show()

		else :
		
			df.boxplot( ax=axis )		
			if save : plt.savefig( locallibrary/carrel/FIGURES/READABILITYBOXPLOT )
			else    : plt.show()

	# clean up
	connection.close()
	return '\n'.join( items )


# compute ngrams
def ngramss( carrel, size=1, query=None, count=False, location='local', wordcloud=False, save=False ) :

	# configure
	LIMIT = 200
	
	# require
	from re       import search
	from requests import get
	import nltk

	# branch according to location; local
	if location == 'local' :
	
		# sanity check
		checkForCarrel( carrel )
		
		# read local data
		localLibrary = configuration( 'localLibrary' )
		stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ), encoding='utf-8' ).read().split()
		text         = open( str( localLibrary/carrel/ETC/CORPUS ), encoding='utf-8' ).read()
	
	# remote
	elif location == 'remote' :
	
		# read remote data; needs error checking
		stopwords = get( '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, ETC, STOPWORDS ] ) ).text.split()
		text      = get( '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, ETC, CORPUS ] ) ).text
		
	# error
	else :
	
		# click ought to prevent this, but just in case
		click.echo( "Error: Unknown value for location: { location }. Call Eric.", err=True )
		exit()
			
	# read, tokenize, and normalize the text
	tokens = nltk.word_tokenize( text, preserve_line=True )
	tokens = [ token.lower() for token in tokens if token.isalpha() ]
	
	# create the set of ngrams
	ngrams = list( nltk.ngrams( tokens, size ) )
	
	# filter, conditionally
	if query :
	
		# initialize and process each ngram
		filtered = []
		for ngram in ngrams :
			
			# check and update
			if search( query, ' '.join( ngram ) ) : filtered.append( ngram )
		
		# done
		ngrams = filtered

	# remove stopwords from unigrams or bigrams
	if size < 3 :
	
		# initialize
		results = []
		
		# process each ngram
		for ngram in ngrams :

			# re-initialize
			found = False
			
			# process each token in the ngram
			for token in ngram :

				# check for stopword
				if token in stopwords : found = True
	
			# conditionally update the results
			if not found : results.append( ngram )

		# done; make it read pretty
		ngrams = results
		
	# output; human
	if count :
	
		# initialize a dictionary and process each ngram
		frequencies = {}
		for ngram in ngrams :

			# update the dictionary
			if ngram in frequencies : frequencies[ ngram ] += 1
			else                    : frequencies[ ngram ]  = 1

		# sort the dictionary
		ngrams = sorted( frequencies.items(), key=lambda x:x[ 1 ], reverse=True )
		
		if not wordcloud :
		
			results = []
			
			# process each ngram
			for ngram in ngrams :
			
				# create a record and output
				results.append( '\t'.join( list( ngram[ 0 ] ) ) + '\t' + str( ngram[ 1 ] ) )
				
			return '\n'.join( results )
							
		else :
		
			# limit the number of ngrams; we can't visualize a huge number
			ngrams = ngrams[ :LIMIT ]
			
			# coerce the result into a dictionary of frequencies
			frequencies = {}
			for ngram in ngrams : frequencies[ ' '.join( ngram[ 0 ] ) ] = ngram[ 1 ]
			
			# simply output
			if not save : cloud( frequencies )

			# save to the corresponding figures directory
			else :
			
				# unigrams
				if size == 1 :
				
					# configure and save
					file = localLibrary/carrel/FIGURES/UNIGRAMSCLOUD
					cloud( frequencies, file=file )
					
				# bigrams
				elif size == 2 :
				
					# configure and save
					file = localLibrary/carrel/FIGURES/BIGRAMSCLOUD
					cloud( frequencies, file=file )
				
				# unsupported
				else : click.echo( "The save option is only valid for unigrams and bigrams; there is no default location for anything else.", err=True )
				
	# power user
	else :
		
		results = []
	
		# output raw data, and hope sort, uniq, grep, and less are used
		for ngram in ngrams : results.append( "\t".join( list( ngram ) ) )
		return '\n'.join( results )


# process parts-of-speech
def partsofspeech( carrel, select='parts', like='any', count=False, normalize=True, wordcloud=False, save=False ) :

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# branch accordingly; parts-of-speech
	if select == 'parts' :
	
		# initialize like
		if like == 'any' : like = '%'
		else             : like = like.upper() + '%'
		
		# dump parts-of-speech tags
		if not count :

			# articulate sql, search, and output
			sql  = ( "SELECT pos FROM pos WHERE pos LIKE '%s';" % like )
			rows = connection.execute( sql )
			for row in rows : items.append( row[ 'pos' ] )

		# count and tabulate the dump
		else :
		
			# articulate sql, search, and output
			sql  = ( "SELECT pos, COUNT( pos ) AS count FROM pos WHERE pos LIKE '%s' GROUP BY pos ORDER BY count DESC;" % like )
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'pos' ], str( row[ 'count' ] ) ] ) )			
			
	# words or lemmas
	else : 
	
		# initialize select
		if select == 'words' : select = 'token'
		else                 : select = 'lemma'
		
		# initialize like
		if like == 'any' : like = '%'
		else             : like = like.upper() + '%'
		
		# simply dump the desired content
		if not count :
		
			# build sql
			if not normalize : sql = ( 'SELECT %s FROM pos WHERE pos LIKE "%s";' % ( select, like ) )
			else : sql = ( 'SELECT LOWER( %s ) AS %s FROM pos WHERE pos LIKE "%s";' % ( select, select, like ) )
						
			# search and process each resulting row
			rows = connection.execute( sql )
			for row in rows : items.append( row[ select ] )
		
		# count and tabulate the result
		else:

			# do not lower-case words or lemmas
			if not normalize : sql = ( '''SELECT %s AS %s, COUNT( %s ) AS count
			                              FROM pos
			                              WHERE pos LIKE "%s"
			                              GROUP BY %s
			                              ORDER BY count DESC;''' % ( select, select, select, like, select ) )
				
			# lower-case words or lemmas
			else: sql = ( '''SELECT LOWER( %s ) AS %s, COUNT( %s ) AS count
			                 FROM pos
			                 WHERE pos LIKE "%s"
			                 GROUP BY LOWER( %s )
			                 ORDER BY count DESC;''' % ( select, select, select, like, select ) )
				
			# search and process each resulting row
			rows = connection.execute( sql )

			# output simple tabulation
			if not wordcloud :
			
				# dump
				for row in rows : items.append( "\t".join( [ row[ select ], str( row[ 'count' ] ) ] ) )
			
			# output word cloud
			else :
			
				# create a dictionary of frequencies
				frequencies = {}
				for row in rows : frequencies[ row[ select ] ] = row[ 'count' ]

				# simply output
				if not save : cloud( frequencies )
			
				# save to the corresponding figures directory
				else :
			
					# configure
					localLibrary = configuration( 'localLibrary' )

					# nouns
					if like == 'NOUN%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSNOUN
						cloud( frequencies, file=file )
				
					# org
					elif like == 'VERB%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSVERB
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'PRON%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSPRON
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'ADJ%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSADJ
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'PROPN%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSPROPN
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'ADV%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSADV
						cloud( frequencies, file=file )
				
					# unsupported
					else : click.echo( "The save option is only valid for types NOUN, VERB, PRON, ADJ, PROPN, and ADV; there is no default location for anything else.", err=True )

				# return nothing when wordclouding
				return
		
	# clean up and done
	connection.close()
	return '\n'.join( items )


# process named entities
def entities( carrel, select='type', like='any', count=False, wordcloud=False, save=False ) :

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	localLibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# branch accordingly; types of entities
	if select == 'type' :
	
		# dump
		if not count :

			# articulate sql, search, and output
			sql  = 'SELECT type FROM ent;'
			rows = connection.execute( sql )
			for row in rows : items.append( row[ 'type' ] )

		# count and tabulate the dump
		else :
		
			# articulate sql, search, and output
			sql  = 'SELECT type, COUNT( type ) AS count FROM ent GROUP BY type ORDER BY count DESC;'
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'type' ], str( row[ 'count' ] ) ] ) )			
			
	# entities
	else : 
			
		# initialize like
		if like == 'any' : like = '%'
		else             : like == like.upper()
		
		# simply dump the desired content
		if not count :
		
			# build sql, search, and output
			sql  = ( 'SELECT entity FROM ent WHERE type LIKE "%s";' % ( like ) )
			rows = connection.execute( sql )
			for row in rows : items.append( row[ select ] )
		
		# count and tabulate the result
		else:

			# build sql, search, and output
			sql  = ( 'SELECT entity, COUNT( entity ) AS count FROM ent WHERE type LIKE "%s" GROUP BY entity ORDER BY count DESC;' % ( like ) )
			rows = connection.execute( sql )
			
			# output simple tabulation
			if not wordcloud :
			
				# dump
				for row in rows : items.append( "\t".join( [ row[ select ], str( row[ 'count' ] ) ] ) )
			
			# output word cloud
			else :
			
				# create a dictionary of frequencies
				frequencies = {}
				for row in rows : frequencies[ row[ select ] ] = row[ 'count' ]

				# simply output
				if not save : cloud( frequencies )
			
				# save to the corresponding figures directory
				else :
			
					# any
					if like == '%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESANY
						cloud( frequencies, file=file )
					
					# persons
					elif like == 'PERSON' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESPERSON
						cloud( frequencies, file=file )
				
					# org
					elif like == 'ORG' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESORG
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'GPE' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESGPE
						cloud( frequencies, file=file )
				
					# unsupported
					else : click.echo( "The save option is only valid for entities of type any, PERSON, ORG, or GPE; there is no default location for anything else.", err=True )

				# when wordclouding, return nothing
				return
				
	# clean up
	connection.close()
	return '\n'.join( items )


# do feature reduction and visualize
def clusters( carrel, type='dendrogram', save=False ) :

	# configure
	MAXIMUM   = 0.95
	MINIMUM   = 2
	EXTENSION = '.txt'

	# require
	from os                              import path, system, listdir
	from scipy.cluster.hierarchy         import ward, dendrogram
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.manifold                import MDS
	from sklearn.metrics.pairwise        import cosine_similarity
	import matplotlib.pyplot             as     plt
	
	# ignore warnings; probably not the greatest idea
	import warnings
	warnings.filterwarnings("ignore")

	# sanity check
	checkForCarrel( carrel )

	# initialize
	localLibrary = configuration( 'localLibrary' )
	stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ), encoding='utf-8' ).read().split()
	directory    = localLibrary/carrel/TXT
	filenames    = [ path.join( directory, filename ) for filename in listdir( directory ) ]
	vectorizer   = TfidfVectorizer( input='filename', max_df=MAXIMUM, min_df=MINIMUM, stop_words=stopwords )
	matrix       = vectorizer.fit_transform( filenames ).toarray()
	distance     = 1 - cosine_similarity( matrix )
	keys         = [ path.basename( filename ).replace( EXTENSION, '' ) for filename in filenames ] 

	# branch according to type; dendrogram
	if type == 'dendrogram' :
		linkage_matrix = ward( distance )
		dendrogram( linkage_matrix, orientation="right", labels=keys )
		plt.tight_layout() 

	# cube
	elif type == 'cube' :
		mds = MDS( n_components=3, dissimilarity="precomputed", random_state=1 )
		pos = mds.fit_transform( distance )
		fig = plt.figure()
		ax  = fig.add_subplot( 111, projection='3d' )
		ax.scatter( pos[ :, 0 ], pos[ :, 1 ], pos[ :, 2 ] )
		for x, y, z, s in zip( pos[ :, 0 ], pos[ :, 1 ], pos[ :, 2 ], keys ) : ax.text( x, y, z, s )

	# save, or not
	if save :
	
		if type == 'dendrogram' : plt.savefig( localLibrary/carrel/FIGURES/CLUSTERDENDROGRAM )
		else                    : plt.savefig( localLibrary/carrel/FIGURES/CLUSTERCUBE )
		
	else : plt.show()

	# done
	return
	
# process collocations
def collocate( carrel, window=4, filter=4, measure='chisqr', limit=4000, output='image', save=False ) :

	# require
	from   nltk.collocations import BigramAssocMeasures
	import matplotlib.pyplot as plt
	import networkx as nx
	import nltk
	import sys
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	corpus       = str( localLibrary/carrel/ETC/CORPUS )
	stopwords    = str( localLibrary/carrel/ETC/STOPWORDS )

	# sanity checks
	checkForCarrel( carrel )
		
	# read the stop words and the carrel
	with open( stopwords, encoding='utf-8' ) as handle : stopwords = handle.read().split( '\n' )
	with open( corpus, encoding='utf-8' )    as handle : corpus    = handle.read()

	# featurize the carrel
	features = nltk.word_tokenize( corpus )
	features = [ feature for feature in features if feature.isalpha() ]
	features = [ feature.lower() for feature in features ]
	features = [ feature for feature in features if feature not in stopwords ]

	# collocate
	finder = nltk.BigramCollocationFinder.from_words( features, window_size=window )
	
	# filter
	if filter > 0 : finder.apply_freq_filter( filter )
	
	# measure
	if   measure == 'chisqr'     : records = finder.score_ngrams( BigramAssocMeasures.chi_sq )
	elif measure == 'jaccard'    : records = finder.score_ngrams( BigramAssocMeasures.jaccard )
	elif measure == 'likelihood' : records = finder.score_ngrams( BigramAssocMeasures.likelihood_ratio )
	elif measure == 'raw'        : records = finder.score_ngrams( BigramAssocMeasures.raw_freq )
	elif measure == 'fisher'     : records = finder.score_ngrams( BigramAssocMeasures.fisher )
	
	# create a network from the scores
	G = nx.Graph()
	for index, record in enumerate( records ) :
	
		# parse
		source = record[ 0 ][ 0 ]
		target = record[ 0 ][ 1 ]
		weight = record[ 1 ]
	
		# update
		G.add_edge( source, target, weight=weight )
	
		# continue, conditionally
		if index > limit : break
	
	# debug
	sys.stderr.write( 'Parameters:' + '\n' )
	sys.stderr.write( '  * carrel: '  + carrel + '\n' )
	sys.stderr.write( '  * limit: '   + str( limit ) + '\n' )
	sys.stderr.write( '  * measure: ' + measure + '\n' )
	sys.stderr.write( '  * filter: '  + str( filter ) + '\n' )
	sys.stderr.write( '  * window: '  + str( window) + '\n' )
	sys.stderr.write( '\n' )
	sys.stderr.write( 'Result:' + '\n' )
	sys.stderr.write( '  * number of nodes: ' + str( G.number_of_nodes() ) + '\n' )
	sys.stderr.write( '  * number of edges: ' + str( G.number_of_edges() ) + '\n' )
	
	# output image
	if output == 'image' :
	
		# visualize
		plt.figure()
		nx.draw( G, with_labels=True, node_size=10, font_size=9, edge_color='silver' )
		plt.show()
		
	# standard out
	else: 
	
		# save
		if save :

			# configure and save
			file = localLibrary/carrel/ETC/COLLOCATIONS
			nx.write_gml( G, file )

		# standard output
		else : nx.write_gml( G, sys.stdout.buffer )
		
	# done
	return

# given a carrel, return a spacy doc
def _carrel2doc( carrel ) :

	# configure
	PICKLE = 'reader.spacy'

	# require
	from os        import path, stat
	from spacy     import load
	import                textacy
	import sys
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	pickle       = localLibrary/carrel/ETC/PICKLE

	# check to see if we've previously been here
	if path.exists( pickle ) :
		
		# read the pickle file
		try            : doc = next( textacy.io.spacy.read_spacy_docs( pickle, lang=MODEL ) )
		except OSError : modelNotFound()
			
	# otherwise
	else :
	
		# warn
		sys.stderr.write( '''Modeling study carrel data for future use. This may take many
minutes, but it will only have to be done once. In the meantime,
ask yourself, "Self, what is justice?"\n''' )

		# initialize 
		file           = localLibrary/carrel/ETC/CORPUS
		text           = open( str( file ) ).read()
		size           = ( stat( file ).st_size ) + 1
		
		# initialize some more
		try            : nlp  = load( MODEL )
		except OSError : modelNotFound()
		
		# do the work
		nlp.max_length = size
		doc            = nlp( text )

		# save it for future use
		textacy.io.spacy.write_spacy_docs( doc, filepath=pickle )

	# done
	return doc


# process grammars
def grammarss( carrel, grammar='svo', query=None, noun=None, lemma='be', sort=False, count=False ) :

	# require
	from textacy import extract
	from os      import system
	from re      import search
	
	# sanity check
	checkForCarrel( carrel )

	# initialize
	doc = _carrel2doc( carrel )

	# get the features; svo
	if grammar == 'svo' :
			
		# do the work
		features = list( extract.subject_verb_object_triples( doc ) )
				
		# simplify the result
		items = []
		for feature in features :
		
			#print( help(feature ) )
			#exit()

			subject = feature.subject[ 0 ].text			
			verb    = feature.verb[ 0 ].text
			object  = feature.object[ 0 ].text
			items.append(' \t'.join( [ ''.join( subject ), ''.join( verb ), ''.join( object ) ] ) )

		# done
		features = items
				
	# quotes
	elif grammar == 'quotes' :
	
		# do the work
		features = list( extract.direct_quotations( doc ) )
		
		# simplify the result
		items = []
		for feature in features :
		
			# parse and stringify
			speaker = [ token.text for token in feature.speaker ]
			cue     = [ token.text for token in feature.cue ]
			content = feature.content.text
			items.append( '\t'.join( [ ''.join( speaker ), ''.join( cue ), content ] ) )

		# done
		features = items

	# noun chunks
	elif grammar == 'nouns' :
	
		# do the work and simplify the result
		features = list( extract.noun_chunks( doc ) )
		features = [ feature.text for feature in features ]
		
	# semi-structured sentences
	elif grammar == 'sss' :

		# sanity check
		if not noun :
		
			sy.stderr.write( "Error: When specifying sss, the -n option is required. See 'rdr grammars --help'\n" )
			exit()
			
		# do the work
		features = list( extract.semistructured_statements( doc, entity=noun, cue=lemma ) )

		# simplify the result
		items = []
		for feature in features :
		
			entity   = [ token.text for token in feature.entity ]
			cue      = [ token.text for token in feature.cue ]
			fragment = [ token.text for token in feature.fragment ]
			items.append( '\t'.join( [ ''.join( entity ), ''.join( cue ), ' '.join( fragment ) ] ) )

		# done
		features = items

	# filter, conditionally
	if query : features = [ feature for feature in features if ( search( query, feature ) ) ]
	
	# sort, conditionally
	if sort : features.sort()
	
	# count, conditionally
	if count :
	
		# initialize a dictionary and process each feature
		items = {}
		for feature in features :

			# update the dictionary
			if feature in items : items[ feature ] += 1
			else                : items[ feature ]  = 1

		# sort the dictionary; return the features
		features = sorted( items.items(), key=lambda x:x[ 1 ], reverse=True )
		
		# process each feature, again
		items = []
		for feature in features :
			
			# create a record and update
			record = str( feature[ 1 ] ) + '\t' + feature[ 0 ]
			items.append( record )
		
		# done
		features = items
	
	# done
	return '\n'.join( features )
	

	