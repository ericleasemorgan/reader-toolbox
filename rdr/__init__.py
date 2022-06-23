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

VERBOSE   = 2

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

# html template for summarize command
TEMPLATE = '''
<html>
<head>
<title>Index of ##CARREL##</title>
</head>
<body style='margin: 7%'>

	<h1>Index of ##CARREL##</h1>

	<h2>Basic characteristics</h2>

		<table>
		<tr><td>Creator</td><td>##CREATOR##</td></tr>
		<tr><td>Date created</td><td>##DATECREATED##</td></tr>
		<tr><td>Number of items</td><td>##ITEMS##</td></tr>
		<tr><td>Number of words</td><td>##WORDS##</td></tr>
		<tr><td>Average readability score</td><td>##FLESCH##</td></tr>
		<tr><td>Bibliography</td><td><a href="./etc/bibliography.txt">plain text</a>; <a href="./etc/bibliography.htm">HTML</a>; <a href="./etc/bibliography.json">JSON</a></td></tr>
		</table>
		
		<h3>Sizes</h3>
			<p style='text-align: center'>
			<img src='./figures/sizes-boxplot.png' width='49%' /> <img src='./figures/sizes-histogram.png' width='49%' />
			</p>

		<h3>Readability</h3>
			<p style='text-align: center'>
			<img src='./figures/readability-boxplot.png' width='49%' /> <img src='./figures/readability-histogram.png' width='49%' />
			</p>

		<h3>Clusters</h3>
			<p style='text-align: center'>
			<img src='./figures/cluster-dendrogram.png' width='49%' /> <img src='./figures/cluster-cube.png' width='49%' />
			</p>

		<h3>Ngrams</h3>
			<p style='text-align: center'>
			<img src='./figures/unigrams-cloud.png' width='49%' /> <img src='./figures/bigrams-cloud.png' width='49%' />
			</p>

		<h3>Parts-of-speech</h3>
			<p style='text-align: center'>
			<img src='./figures/pos-noun.png' width='49%' /> <img src='./figures/pos-propernoun.png' width='49%' />
			</p>
			<p style='text-align: center'>
			<img src='./figures/pos-pronoun.png' width='49%' /> <img src='./figures/pos-verb.png' width='49%' />
			</p>
			<p style='text-align: center'>
			<img src='./figures/pos-adjective.png' width='49%' /> <img src='./figures/pos-adverb.png' width='49%' />
			</p>

		<h3>Entities</h3>
			<p style='text-align: center'>
			<img src='./figures/entities-any.png' width='49%' /> <img src='./figures/entities-person.png' width='49%' />
			</p>
			<p style='text-align: center'>
			<img src='./figures/entities-gpe.png' width='49%' /> <img src='./figures/entities-org.png' width='49%' />
			</p>

		<h3>Keywords</h3>
			<p style='text-align: center'>
			<img src='./figures/keywords-cloud.png' width='66%' />
			</p>
			
</body>
</html>
'''

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
	'''fields = process|originalID|dateCreated|timeCreated|creator|input'''
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
	'''Types = items|words|flesch'''
	
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
	
			# a hack for the lack of an extension
			if not row[ 'extension' ] : extension = ''
			else                      : extension = row[ 'extension' ]
			
			# build cache and plain text
			cache = str( locallibrary/carrel/CACHE/id ) + extension
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
def concordance( carrel, query='love', width=80, lines=999 ) :

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
def sizes( carrel, sort='words', output='list', save=False ) :

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
		for row in rows :
		
			if not row[ 'words' ] : words = 0
			else                  : words = row[ 'words' ]
			records.append( int( row[ 'words' ] ) )
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
		for row in rows : 
		
			# a hack for keough; be forewarned
			try : records.append( int( row[ 'flesch' ] ) )
			except ValueError : pass
			
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
def ngrams( carrel, size=1, query=None, count=False, location='local', wordcloud=False, save=False ) :

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
def pos( carrel, select='parts', like='any', count=False, normalize=True, wordcloud=False, save=False ) :

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
def cluster( carrel, type='dendrogram', save=False ) :

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
def grammars( carrel, grammar='svo', query=None, noun=None, lemma='be', sort=False, count=False ) :

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
	

# elaborate about the lack of word2vec
def word2vecwarning() :

	import sys
	
	sys.stderr.write( "By default, Word2vec not installed, which is required for this subcommand. Linux and Macintosh users can probably run 'pip install word2vec' and then give this subcommand another go. Windows users will have to go through many hoops because the underling word2vec software needs to be compiled. Please see the word2vec home page for more detail: https://github.com/danielfrg/word2vec\n" )
	exit()


# make sure the carrel has been indexed; word2vec++
def checkForSemanticIndex( carrel ) :

	# configure
	MODEL   = 'reader.bin'
	TXT     = 'model.txt'
	PHRASES = 'model.phrases'
	
	# require
	from pathlib  import Path
	from word2vec import word2vec, word2phrase
	import               os
	import sys
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	model        = localLibrary/carrel/ETC/MODEL
	
	# see if we have been here previously
	if not model.exists() :

		# initialize some more
		stopwords = localLibrary/carrel/ETC/STOPWORDS
		corpus    = localLibrary/carrel/ETC/CORPUS
		txt       = str( Path.home()/TXT )
		phrases   = str( Path.home()/PHRASES )
		
		# tokenize
		sys.stderr.write( 'Indexing. This needs to be done only once.\n' )
		sys.stderr.write( 'Step #1 of 6: Tokenizing corpus....\n' )
		tokens = open( corpus ).read().split()

		# normalize
		sys.stderr.write( 'Step #2 of 6: Normalizing tokens...\n' )
		tokens = [ token.lower() for token in tokens if token.isalpha() ]

		# remove stop words
		sys.stderr.write( 'Step #3 of 6: Removing stop words...\n' )
		stopwords = open( stopwords ).read().split()
		tokens    = [ token for token in tokens if token not in stopwords ]

		# save
		sys.stderr.write( 'Step #4 of 6: Saving tokens...\n' )
		with open( txt, 'w' ) as handle : handle.write( ' '.join( tokens ) )
		
		# create phrases
		sys.stderr.write( 'Step #5 of 6: Creating phrases...\n' )
		word2phrase( txt, phrases, verbose=True )

		# do the work
		sys.stderr.write( 'Step #6 of 6: Indexing....\n' )
		word2vec( phrases, str( model ), size=100, binary=True, verbose=True)

		# clean up and done
		os.remove( txt )
		os.remove( phrases )
		sys.stderr.write( '\nDone. Happy searching!\n' )


# implement semantic (word2vec) indexing
def word2vec( carrel, type='similarity', query='love', size=10 ) :
	'''types = similarity|distance|analogy|scatter'''

	# configure
	MODEL    = 'reader.bin'
	DISTANCE = 'model.distance( ##QUERY## )'

	# try to import word2vec
	try    : import word2vec
	except : word2vecwarning()
	
	# require
	import matplotlib.pyplot as plot
	import sys

	# initialize
	localLibrary = configuration( 'localLibrary' )
	model        = str( localLibrary/carrel/ETC/MODEL )

	# sanity checks
	checkForCarrel( carrel )
	checkForSemanticIndex( carrel )
		
	# load model
	model = word2vec.load( model )

	# similarity
	if type == 'similarity' :
	
		# sanity check
		if len( query.split() ) != 1 :
		
			# error
			sys.stderr.write( "The query for similarity requires exactly one word.\n" )
			exit()

		# search and output
		try :
	
			items = []
			
			indexes, metrics = model.similar( query, n=size )
			similarities = model.generate_response( indexes, metrics ).tolist()
			for similarity in similarities : items.append( '\t'.join( [ similarity[ 0 ], str( similarity[ 1 ] ) ] ) )
		
			return '\n'.join( items )
			
		# word not found
		except KeyError as word : sys.stderr.write ( ( 'The word -- %s -- is not in the index.\n' % word ) )

	# scatter
	elif type == 'scatter' :
	
		from sklearn.manifold import TSNE
		import numpy as np

		words              = ['love', 'horse', 'house', 'son', 'war', 'man', 'woman', 'spear', 'achilles' ]
		embedding_clusters = []
		word_clusters      = []
		for word in words :
			embeddings = []
			words      = []
			indexes, metrics = model.similar( word, n=20 )
			similarities = model.generate_response( indexes, metrics ).tolist()
			for similarity in similarities :
			
				words.append(similarity[ 0 ])
				embeddings.append( ( similarity[ 0 ], similarity[ 1 ] ) )
		
			embedding_clusters.append( embeddings )
			word_clusters.append( words )

		clusters = np.array( embedding_clusters )	
		print( clusters )
		exit()
					
		tsne     = TSNE( perplexity=2, n_components=2, init='pca'  )
		model    = tsne.fit_transform( clusters )

		# plot
		x = model[ :, 0 ]
		y = model[ :, 1 ]
		plot.scatter( x, y )
		plot.show()

	# distance
	elif type == 'distance' :

		# get the query words
		words = query.split()

		# sanity check
		if len( words ) < 2 :
		
			# error
			sys.stderr.write( "The query for distance requires at least two words.\n" )
			exit()

		# create a distance command; hacky!
		queries = [ ( "'%s'" % word ) for word in words ]
		command = DISTANCE.replace( '##QUERY##', ', '.join( queries ) )
		
		# try to compute
		try :
		
			items = []
			
			# search, sort, output, and done
			distances = eval( command )
			distances.sort( key=lambda i: i[ 2 ], reverse=True )
			for distance in distances : items.append( '\t'.join( [ distance[ 0 ], distance[ 1 ], str( distance[ 2 ] ) ] ) )

			return '\n'.join( items )
			
		# error
		except KeyError as word : 
			sys.stderr.write( ( 'A word in your query -- %s -- is not in the index. Please remove it.\n' % word ) )

	# analogy
	elif type == 'analogy' :
	
		# get the query words
		words = query.split()
		
		# sanity check
		if len( words ) != 3 :
		
			# error
			sys.stderr.write( "The query for analogy requires exactly three words.\n" )
			exit()
		
		# try to compute
		try :
		
			items = []
			
			# search, sort, output, and done
			indexes, metrics = model.analogy( pos=[ words[ 0 ], words[ 1 ] ], neg=[ words[ 2 ] ], n=size )
			analogies = model.generate_response( indexes, metrics ).tolist()
			for analogy in analogies : items.append( '\t'.join( [ analogy[ 0 ], str( analogy[ 1 ] ) ] ) )

			return '\n'.join( items )
			
		# error
		except KeyError as word : sys.stderr.write( ( 'A word in your query -- %s -- is not in the index. Please remove it.\n' % word ) )


# make sure the carrel has been indexed; sqlite++
def _checkForIndex( carrel ) :

	# configure
	SANITYCHECK    = "SELECT * FROM sqlite_master WHERE type='table' AND name='fulltext';"
	DROPFULLTEXT   = 'DROP TABLE IF EXISTS fulltext;'
	CREATEFULLTEXT = 'CREATE TABLE fulltext ( id TEXT, fulltext TEXT );\n'
	TEMPLATE       = "INSERT INTO fulltext ( id, fulltext ) VALUES ( '##ID##', '##FULLTEXT##' );\n"
	DROPINDX       = 'DROP TABLE IF EXISTS indx;'
	CREATEINDX     = 'CREATE VIRTUAL TABLE indx USING FTS5( id, author, title, date, summary, keyword, words, sentence, flesch, cache, txt, fulltext );'
	INDEX          = 'INSERT INTO indx SELECT b.id, b.author, b.title, b.date, b.summary, group_concat( LOWER( w.keyword ), "; " ), b.words, b.sentence, b.flesch, b.id || b.extension, b.id || ".txt", f.fulltext FROM bib AS b, fulltext AS f, wrd AS w WHERE b.id IS f.id AND b.id IS w.id GROUP BY w.id;';

	# require
	import os
	import re
	import sqlite3
	import tempfile
	import sys
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	db           = str( localLibrary/carrel/ETC/DATABASE )
	txt          = localLibrary/carrel/TXT
	transaction  = tempfile.NamedTemporaryFile( delete=False ).name
	
	# connect to database
	connection                 = sqlite3.connect( db )
	connection.isolation_level = None
	cursor                     = connection.cursor()
		
	# check to see if we've been here previously
	results = cursor.execute( SANITYCHECK ).fetchall()
	if results == [] :
		
		# nope; create full text table
		sys.stderr.write( 'Indexing; the carrel must be set up for full text searching.\n' )
		sys.stderr.write( 'Step #1 of 4: Creating table to contain full text...\n' )
		connection.execute( DROPFULLTEXT )
		connection.execute( CREATEFULLTEXT )

		# read full text
		sys.stderr.write( 'Step #2 of 4: Reading full text; please be patient...\n' )
		with open( transaction, 'w' ) as handle : handle.write( 'BEGIN TRANSACTION;\n' )
		files = txt.glob( '*.txt' )
		for file in files :

			# get identifier
			id = file.stem
			id = id.replace( "'", "''" )
	
			# get full text
			with open( file, encoding='utf-8' ) as handle : fulltext = handle.read()
			fulltext = fulltext.replace( '\r', '\n' )
			fulltext = fulltext.replace( '\n', ' ' )
			fulltext = fulltext.replace( "'",  "''")
			fulltext = re.sub( ' +' , ' ', fulltext )
	
			# sql
			sql = TEMPLATE
			sql = sql.replace( '##ID##', id )
			sql = sql.replace( '##FULLTEXT##', fulltext )

			# debug
			#click.echo( '  file: ' + str( file ), err=True )
			#click.echo( '    id: ' + id, err=True )
			#click.echo( err=True )
	
			# update
			with open( transaction, 'a' ) as handle : handle.write( sql )

		# close the transaction
		with open( transaction, 'a' ) as handle : handle.write( 'END TRANSACTION;\n' )

		# write full text
		sys.stderr.write( 'Step #3 of 4: Writing full text to database...\n' )
		with open( transaction ) as handle :

			# repeat forever, almost
			while True :
				sql = handle.readline()
				if not sql : break
				connection.execute( sql )


		# clean up
		os.remove( transaction )
		
		# index; do the actual work
		sys.stderr.write( 'Step #4 of 4: Indexing; please be patient...\n' )
		connection.execute( DROPINDX )
		connection.execute( CREATEINDX )
		connection.execute( INDEX )

		# done
		sys.stderr.write( 'Done. Happy searching!\n' )
		return
		
# do full text indexing and search
def search( carrel, query='love', output='human' ) :
	'''output = csv|tsv|json|human|count'''

	# configure
	SQL = "SELECT id, author, title, date, summary, keyword, words, sentence, flesch, '##CACHE##' || cache AS cache, '##TXT##' || txt AS txt FROM indx WHERE indx MATCH '##QUERY##' ORDER BY RANK;"

	# configure
	RESULTS = '\nYour search (##QUERY##) against the study carrel named "##CARREL##" returned ##COUNT## record(s):\n\n##RECORDS##'
	RECORD  = '          id: ##ID##\n      author: ##AUTHOR##\n       title: ##TITLE##\n        date: ##DATE##\n     summary: ##SUMMARY##\n  keyword(s): ##KEYWORD##\n       words: ##WORDS##\n    sentence: ##SENTENCE##\n      flesch: ##FLESCH##\n       cache: ##CACHE##\n         txt: ##TXT##\n\n'
	COUNT   = '##CARREL##\t##QUERY##\t##COUNT##'

	# require
	import sqlite3
	import pandas as pd
	import sys
	
	# sanity checks
	checkForCarrel( carrel )
	_checkForIndex( carrel )
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	txt          = str( localLibrary/carrel/TXT ) + '/'
	cache        = str( localLibrary/carrel/CACHE ) + '/'
	db           = str( localLibrary/carrel/ETC/DATABASE )
	connection   = sqlite3.connect( db )

	# build sql
	sql = SQL.replace( '##CACHE##', cache )
	sql = sql.replace( '##TXT##', txt )
	sql = sql.replace( '##QUERY##', query )

	# search
	rows = pd.read_sql_query( sql, connection, index_col='id' )
	
	# output; csv
	if output   == 'csv' : return( rows.to_csv() )
	
	# tsv
	elif output == 'tsv' : return( rows.to_csv( header=False, sep='\t' ) )
	
	# json
	elif output == 'json' : return( rows.to_json( orient='records' ) )
	
	# count; tsv stream of metadata
	elif output == 'count' :
	
		# build
		results = COUNT.replace( '##CARREL##', carrel )
		results = results.replace( '##QUERY##', query )
		results = results.replace( '##COUNT##', str( rows.shape[ 0 ] ) )
		
		# output
		return( results )
	
	# paged
	elif output == 'human' : 
			
		# initialize the results
		results = RESULTS.replace( '##QUERY##', query )
		results = results.replace( '##CARREL##', carrel )
		results = results.replace( '##COUNT##', str( rows.shape[ 0 ] ) )
		
		# process each row
		records = ''
		for id, row in rows.iterrows() :
								
			# parse
			author   = row[ 'author' ]
			if not author : author = ''
			title    = row[ 'title' ]
			if not title : title = ''
			date     = row[ 'date' ]
			if not date : date = ''
			summary  = row[ 'summary' ]
			keyword  = row[ 'keyword' ]
			words    = row[ 'words' ]
			sentence = row[ 'sentence' ]
			flesch   = row[ 'flesch' ]
			cache    = row[ 'cache' ]
			txt      = row[ 'txt' ]
			
			if not summary : summary = ' '
			if not cache   : cache   = ' '
			
			# create a record
			record = RECORD.replace( '##ID##', str( id ) )
			record = record.replace( '##AUTHOR##', author )
			record = record.replace( '##TITLE##', title )
			record = record.replace( '##DATE##', str( date ) )
			record = record.replace( '##SUMMARY##', summary )
			record = record.replace( '##KEYWORD##', keyword )
			record = record.replace( '##WORDS##', str( words ) )
			record = record.replace( '##SENTENCE##', str( sentence ) )
			record = record.replace( '##FLESCH##', str( flesch ) )
			record = record.replace( '##CACHE##', cache )
			record = record.replace( '##TXT##', txt )
		
			# update
			records += record
		
		results = results.replace( '##RECORDS##', records )
		return( results )


# get an inventory of available study carrels
def catalog( location='local', human=True ) :
	'''location = local|remote'''

	# configure
	TSV    = 'catalog/catalog.tsv'
	RECORD = "      item: ##ITEM##\n      name: ##NAME##\n      date: ##DATE##\n  keywords: ##KEYWORDS##\n     items: ##ITEMS##\n     words: ##WORDS##\n     score: ##SCORE##\n     bytes: ##BYTES##\n\n"
	HEADER = "\nThe catalog includes ##COUNT## items, and each is listed below:\n\n"

	# require
	from requests import get
		
	# branch accordingly; local
	if location == 'local' :
		
		# initialize
		localLibrary = configuration( 'localLibrary' )
		items        = []
		
		# read, sort, and output
		carrels = [ carrel.name for carrel in localLibrary.iterdir() if carrel.is_dir() ]
		carrels.sort()
		for carrel in carrels : items.append( carrel )
	
		return '\n'.join( items )
		
	# remote
	elif location == 'remote' :
	
		# create person-amenable output
		if human :
		
			# create a rudimentary catalog
			catalog = ''
			count   = 0
			
			records = get( REMOTELIBRARY + '/' + TSV ).text 
			for item, record in enumerate( records.split( '\n' ) ) :
			
				# delimit and sanity check
				fields = record.split( '\t' )
				if len( fields ) != 7 : break
			
				# parse
				name     = fields[ 0 ]
				date     = fields[ 1 ]
				keywords = fields[ 2 ]
				items    = fields[ 3 ]
				words    = fields[ 4 ]
				score    = fields[ 5 ]
				bytes    = fields[ 6 ]
			
				# increment
				count += 1
				item  += 1
				
				# update
				record   = RECORD.replace( '##ITEM##', str( item ) )
				record   = record.replace( '##NAME##', name )
				record   = record.replace( '##DATE##', date )
				record   = record.replace( '##KEYWORDS##', keywords )
				record   = record.replace( '##ITEMS##', items )
				record   = record.replace( '##WORDS##', words )
				record   = record.replace( '##SCORE##', score )
				record   = record.replace( '##BYTES##', bytes )
				catalog += record
				
			# add the header and output
			header  = HEADER.replace( '##COUNT##', str( count ) )
			catalog = header + catalog
			return( catalog )
				
		# get the raw data and hope the results get piped to utilities like sort, grep, cut, less, etc.
		else : return( get( REMOTELIBRARY + '/' + TSV ).text  )

	
# locally cache a carrel from the public library
def download( carrel ) :
			
	# configure
	ZIPFILE = 'study-carrel.zip'
	CARRELS = 'carrels'

	# require
	from requests import get
	from tempfile import TemporaryFile
	from zipfile  import ZipFile
	import sys
	
	# initialize
	localLibrary  = configuration( 'localLibrary' )

	# get the remote zip file; needs error checking
	sys.stderr.write( "\n  INFO: Downloading remote study carrel...\n" )
	response = get( REMOTELIBRARY + '/' + CARRELS + '/' + carrel + '/' + ZIPFILE )
	
	# initialize a temporary file and write to it
	sys.stderr.write( "  INFO: Saving study carrel...\n" )
	handle = TemporaryFile()
	handle.write( response.content )
	
	# unzip the temporary file and close it, which also deletes it
	sys.stderr.write( "  INFO: Unziping study carrel...\n" )
	with ZipFile( handle, 'r' ) as zip : zip.extractall( str( localLibrary ) )
	handle.close()

	# done
	sys.stderr.write( ( '''  INFO: Done.\n''' ) )
	return


# open the html root of a study carrel
def read( carrel, location='local' ) :

	# require
	from webbrowser import open
	import sys
	
	if location == 'local' :
	
		# sanity check
		checkForCarrel( carrel )

		localLibrary  = configuration( 'localLibrary' )
		url = 'file://' + str( localLibrary/carrel/INDEX )
		sys.stderr.write( url + '\n' )
		open( url )
		
	elif location == 'remote' :
	
		url = REMOTELIBRARY + '/' + CARRELS + '/' + carrel
		open( url )

# make sure tika server has been downloaded
def _checkForTika( tika ) :
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	from requests     import get
	
	# install tika, conditionally
	if not Path( tika ).exists() :
	
		click.echo( "\n  WARNING: Tika server not found. Downoading... ", err=True )
		response = get( TIKADOWNLOAD )
		file     = Path( tika ) 
		with open( file, 'wb' ) as handle : handle.write( response.content )
		click.echo( "\n  INFO: Downloaded", err=True )

		# _initialize
		click.echo( "\n  INFO: Updating configurations... " )
		configurations          = ConfigParser()
		applicationDirectory    = Path.home()
		configurationFile       = applicationDirectory/CONFIGURATIONFILE
		localLibrary            = configuration( 'localLibrary' )
		malletHome              = configuration( 'malletHome' )
		tikaHome                = Path.home()/TIKAHOME
		configurations[ "RDR" ] = { "localLibrary"  : localLibrary, "malletHome" : malletHome, "tikaHome" : tikaHome }
		with open( configurationFile, 'w' ) as handle : configurations.write( handle )

		# done
		click.echo( '''
  INFO: Tika server (tika-server.jar) has been downloaded to your
  home directory and configured for future use. You can move Tika
  server to another location but once you do so you will need to
  run 'rdr set -s tika'.
''', err=True )

		# start tika server
		_startTika()


# check to see if tika is running
def _tikaIsRunning () :

	# configure, require, and _initialize
	TIKA    = 'http://localhost:9998/'
	import requests
	running = False

	# give it a go
	try :

		# check for success
		if requests.get( TIKA ).ok : running = True
	
	# error
	except requests.ConnectionError : pass
	
	# done
	return( running )
	
	
# create carrel skeleton
def _initialize( carrel, directory ) :
	
	# configure
	ADR      = 'adr'
	BIB      = 'bib'
	CACHE    = 'cache'
	ENT      = 'ent'
	ETC      = 'etc'
	POS      = 'pos'
	TXT      = 'txt'
	URLS     = 'urls'
	WRD      = 'wrd'
	WORDS    = '''0\n1\n2\n3\n4\n5\n6\n7\n8\n9\na\na\nabout\nabove\nafter\nagain\nagainst\nall\nam\nan\nand\nany\nare\naren't\nas\nat\nb\nbe\nbecause\nbeen\nbefore\nbeing\nbelow\nbetween\nboth\nbut\nby\nc\ncan\ncan't\ncannot\ncould\ncouldn't\nd\ndid\ndidn't\ndo\ndoes\ndoesn't\ndoing\ndon't\ndown\nduring\ne\neach\nf\nfew\nfor\nfrom\nfurther\ng\nh\nhad\nhadn't\nhas\nhasn't\nhast\nhath\nhave\nhaven't\nhaving\nhe\nhe'd\nhe'll\nhe's\nher\nhere\nhere's\nhers\nherself\nhim\nhimself\nhis\nhow\nhow's\ni\ni'd\ni'll\ni'm\ni've\nif\nin\ninto\nis\nisn't\nit\nit's\nits\nitself\nj\nk\nl\nlet's\nm\nme\nmore\nmost\nmustn't\nmy\nmyself\nn\nno\nnor\nnot\no\nof\noff\non\nonce\none\nonly\nor\nother\nought\nour\nours\nourselves\nout\nover\nown\np\nq\nr\ns\nsaid\nsame\nshan't\nshe\nshe'd\nshe'll\nshe's\nshould\nshouldn't\nso\nsome\nsuch\nt\nthan\nthat\nthat's\nthe\nthee\ntheir\ntheirs\nthem\nthemselves\nthen\nthere\nthere's\nthese\nthey\nthey'd\nthey'll\nthey're\nthey've\nthis\nthose\nthou\nthrough\nthus\nthy\nto\ntoo\nu\nunder\nuntil\nunto\nup\nupon\nv\nvery\nw\nwas\nwasn't\nwe\nwe'd\nwe'll\nwe're\nwe've\nwere\nweren't\nwhat\nwhat's\nwhen\nwhen's\nwhere\nwhere's\nwhich\nwhile\nwho\nwho's\nwhom\nwhy\nwhy's\nwill\nwith\nwon't\nwould\nwouldn't\nx\ny\nyou\nyou'd\nyou'll\nyou're\nyou've\nyour\nyours\nyourself\nyourselves\nz\n'''
	PROCESS  = 'toolbox'

	# require
	from   datetime import datetime
	from   getpass  import getuser
	from   pathlib  import Path
	import shutil
	
	# create the library, the carrel, and the carrel's sub-directories
	localLibrary = configuration( 'localLibrary' )
	Path.mkdir( localLibrary,                exist_ok=True )
	Path.mkdir( localLibrary/carrel,         exist_ok=True )
	Path.mkdir( localLibrary/carrel/ADR,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/BIB,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/CACHE,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/ENT,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/ETC,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/FIGURES, exist_ok=True )
	Path.mkdir( localLibrary/carrel/POS,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/TXT,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/URLS,    exist_ok=True )
	Path.mkdir( localLibrary/carrel/WRD,     exist_ok=True )

	# configure provenance and output it
	process     = PROCESS
	originalID  = carrel
	dateCreated = datetime.today().strftime( '%Y-%m-%d' )
	timeCreated = datetime.now().strftime("%H:%M")
	creator     = getuser()
	input       = directory
	record      = [ PROCESS, originalID, dateCreated, timeCreated, creator, input ]
	output      = localLibrary/carrel/PROVENANCE
	with open( output, 'w', encoding='utf-8' ) as handle : handle.write( '\t'.join( record ) + '\n' )
	
	# process each item in the given directory
	directory = Path( directory )
	for source in directory.glob( '*' ) :

		# check for metadata file
		if source.name == METADATA :
		
			# copy the metadata file to the root of the carrel
			destination = localLibrary/carrel/( source.name )
			shutil.copyfile( source, destination )

		else :
		
			# copy the file to the cache directory
			destination = localLibrary/carrel/CACHE/( source.name )
			shutil.copyfile( source, destination )

	# add stop words; there is probably a better way
	output = localLibrary/carrel/ETC/STOPWORDS
	with open( output, 'w', encoding='utf-8' ) as handle : handle.write( WORDS )


# given a file, create some bibliographics and save plain text
def _file2bib( carrel, file, metadata=None ) :
		
	# configure
	BIB          = 'bib'
	TXT          = 'txt'
	CACHE        = 'cache'
	COUNT        = 24
	EXTENSION    = '.txt'
	BIBEXTENSION = '.bib'
	HEADER       = [ 'id', 'author', 'title', 'date', 'pages', 'extension', 'mime', 'words', 'sentence', 'flesch', 'summary', 'cache', 'txt' ]
	PROCESS      = 'textrank'

	# require
	from   pathlib              import Path
	from   textacy              import text_stats
	from   tika                 import detector
	from   tika                 import parser
	import os
	import spacy
	import pytextrank

	# _initialize
	authorFound  = False
	dateFound    = False
	titleFound   = False
	title        = _name2key( file )
	extension    = os.path.splitext( os.path.basename( file ) )[ 1 ]
	key          = _name2key( file )
	pages        = ''
	summary      = ''
	localLibrary = configuration( 'localLibrary' )

	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# get the text, and if not, then return; the whole point is to have content to read!
	parsed = parser.from_file( file )
	text   = parsed[ 'content' ]	
	if not text : return
	
	# get metadata from the metadata file	
	if str( type( metadata ) ) == "<class 'pandas.core.frame.DataFrame'>" :
		
		# parse
		index = Path( file ).name
		
		# check to see if the index value exists
		if index in metadata.index :
		
			if 'author' in metadata :
		
				author      = str( metadata.loc[ index ][ 'author' ] )
				authorFound = True
			
			if 'title'  in metadata : 
		
				title  = metadata.loc[ index ][ 'title' ]
				titleFound = True
			
			if 'date'   in metadata : 
		
				date      = str( metadata.loc[ index ][ 'date' ] )
				dateFound = True
		
	# get metadata from the source file
	metadata = parsed[ 'metadata' ] 
	mimetype = detector.from_file( file )

	# author
	if authorFound == False : 
	
		if 'creator' in metadata :
			author = metadata[ 'creator' ]
			if ( isinstance( author, list ) ) : author = author[ 0 ]
			
		else : author = ''
		
	# title
	if titleFound == False : 
	
		if 'title' in metadata :
			title = metadata[ 'title' ]
			if ( isinstance( title, list ) ) : title = title[ 0 ]
			title = ' '.join( title.split() )

	# date
	if dateFound == False : 
	
		if 'date' in metadata :
			date = metadata[ 'date' ]
			if ( isinstance( date, list ) ) : date = date[ 0 ]
			date = date[:date.find( 'T' )]
		
		else : date = ''

	# number of pages
	if 'xmpTPg:NPages' in metadata :
		pages = metadata[ 'xmpTPg:NPages' ]
		if ( isinstance( pages, list ) ) : pages = pages[ 0 ]
		
	# model the text
	nlp            = spacy.load( MODEL )
	nlp.max_length = ( len( text ) + 1 )
	nlp.add_pipe( PROCESS )
	doc            = nlp( text )

	# _summarize
	summary = _summarize( doc )
	
	# parse out only the desired statistics
	words      = text_stats.n_words( doc )
	sentences  = text_stats.n_sents( doc )
	syllables  = text_stats.n_syllables( doc )
	flesch     = int( text_stats.readability.flesch_reading_ease( doc ) )

	# cache and text locations
	txt   = Path( TXT )/( str( key ) + EXTENSION )
	cache = Path( CACHE )/( str( key ) + extension )

	# debug
	if VERBOSE == 2 :
	
		# provide a review
		click.echo( '        key: ' + key,              err=True )
		click.echo( '     author: ' + author,           err=True )
		click.echo( '      title: ' + str( title ),     err=True )
		click.echo( '       date: ' + date,             err=True )
		click.echo( '  extension: ' + extension,        err=True )
		click.echo( '      pages: ' + pages,            err=True )
		click.echo( '  mime-type: ' + mimetype,         err=True )
		click.echo( '    summary: ' + summary,          err=True )
		click.echo( '      words: ' + str( words ),     err=True )
		click.echo( '  sentences: ' + str( sentences ), err=True )
		click.echo( '     flesch: ' + str( flesch ),    err=True )
		click.echo( '      cache: ' + str( cache ),     err=True )
		click.echo( '        txt: ' + str( txt ),       err=True )
		click.echo( '',                                 err=True )
	
	# open output
	output = localLibrary/carrel/BIB/( key + BIBEXTENSION )
	with open( output, 'w', encoding='utf-8' ) as handle :
	
		try :
		
			# output the header and the data
			handle.write( '\t'.join( HEADER ) + '\n' )
			handle.write( '\t'.join( [ str( key ), author, str( title ), str( date ), pages, extension, mimetype, str( words ), str( sentences ), str( flesch ), summary, str( cache ), str( txt ) ] ) + '\n' )
		
		# trap weird TypeError
		except TypeError : click.echo( ( "\nWARNING (TypeError): Probably weird author value extracted from PDF file (key: %s). Call Eric.\n" % key ), err=True )
			
	# check for text, and it should exist; famous last words
	if text : 

		# configure output and output
		output = localLibrary/carrel/TXT/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8' ) as handle : handle.write( text )


# create key from filename
def _name2key( file ) :

	# require, do the work, and done; inefficient
	import os
	key = str( os.path.splitext( os.path.basename( file ) )[ 0 ] )
	return key


# given a spaCy doc which has been enhanced by pytextrank, return a summary
def _summarize( doc ) :

	# see: https://derwen.ai/docs/ptr/explain_summ/
	
	# configure
	PHRASELIMIT   = 4
	SENTENCELIMIT = 2

	# require
	from   math       import sqrt
	from   operator   import itemgetter
	import pytextrank
	import re
	
	boundries   = [ [ sentence.start, sentence.end, set( [] ) ] for sentence in doc.sents ]
	phrase_id   = 0
	unit_vector = []

	# process each phrase
	for phrase in doc._.phrases :

		unit_vector.append( phrase.rank )

		for chunk in phrase.chunks:

			for start, end, vector in boundries :
		
				if chunk.start >= start and chunk.end <= end :

					vector.add( phrase_id )
					break
				
		phrase_id    += 1
		if phrase_id == PHRASELIMIT : break

	sum_ranks   = sum( unit_vector )

	# trap for a document that is too small
	try : unit_vector = [ rank/sum_ranks for rank in unit_vector ]
	except ZeroDivisionError : return doc.text
	
	rankings    = {}
	sent_id     = 0

	for start, end, vector in boundries:

		# re-_initialize
		sum_sq = 0.0

		for identifier in range( len( unit_vector ) ) :
		
			if identifier not in vector : sum_sq += unit_vector[ identifier ] ** 2.0

		rankings[ sent_id ] =  sqrt( sum_sq )
		sent_id             += 1

	# create a dictionary of sentences
	sentences = {}
	for index, sentence in enumerate( doc.sents ) : sentences[ index ] = sentence.text

	# process each ranking
	summary = []
	for index, sentence in enumerate( sorted( rankings.items(), key=itemgetter( 1 ) ) ) :

		# output, and conditionally continue
		summary.append( sentences[ sentence[ 0 ] ] )
		if ( index + 1 ) == SENTENCELIMIT : break

	# _normalize
	summary = ' '.join( summary )
	summary = summary.replace( '"', '' )
	summary = re.sub( '\r', ' ', summary )
	summary = re.sub( '\t+', ' ', summary )
	summary = re.sub( '\n+', ' ', summary )
	summary = re.sub( ' +', ' ',  summary )
	summary = re.sub( '^\s', '',  summary )
	summary = re.sub( '\s$', '',  summary )

	# done
	return summary

# create bag of words
def _txt2bow( carrel ) :

	# configure
	PATTERN = '*.txt'
	BOW     = 'reader.txt'
	TXT     = 'txt'
	ETC     = 'etc'
	
	# require
	from pathlib import Path

	# _initialize
	localLibrary = configuration( 'localLibrary' )

	# process each text file in the given directory
	txt = localLibrary/carrel/TXT
	bow = ''
	for file in txt.glob( PATTERN ) :
	
		# create/increment the bag of words
		with open( file, encoding='utf-8' ) as handle : bow += handle.read()
	
	# _normalize
	bow = _normalize( bow )
	
	# configure output, output, and done
	output = localLibrary/carrel/ETC/BOW
	with open( output, 'w', encoding='utf-8' ) as handle : handle.write( bow )



# _normalize text, a poor man's version
def _normalize( text ) :

	# require
	import re
	
	# _normalize the text in the bag-of-words
	text = text.lower()
	text = re.sub( '\r', '\n', text )
	text = re.sub( '\n+', ' ', text )
	text = re.sub( '^\W+', '', text )
	text = re.sub( '\t', ' ',  text )
	text = re.sub( '- ', '',   text )
	text = re.sub( ' +', ' ',  text )
	text = re.sub( '\t', ' ',  text )

	# done
	return text


# extract email addresses
def _txt2adr( carrel, file ) :
	
	# configure
	ADR       = 'adr'
	EXTENSION = '.adr'
	HEADER    = [ 'id', 'address' ]
	PATTERN   = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

	# require
	import re
	
	# _initialize
	key          = _name2key( file )
	localLibrary = configuration( 'localLibrary' )

	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )
	
	# get and process each address, to the best of my ability
	addresses = re.findall( PATTERN, text )

	# check for addresses
	if len( addresses ) > 0 :

		# open output
		output = localLibrary/carrel/ADR/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8'  ) as handle :

			# _initialize the output
			handle.write( '\t'.join( HEADER ) + '\n' )

			# process each address
			for address in addresses : 
			
				# clean up some more
				address = re.sub( '\/', '', address )
				address = re.sub( '{',  '', address )
				address = re.sub( '}',  '', address )
				
				# output
				handle.write( '\t'.join( [ key, address ] ) + '\n' )


# extract named entities
def _txt2ent( carrel, file ) :

	# configure
	EXTENSION = '.ent'
	ENT       = 'ent'
	HEADER    = [ 'id', 'sid', 'eid', 'entity', 'type' ]

	# require
	import spacy

	# _initialize
	key          = _name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# model the text
	nlp            = spacy.load( MODEL )
	nlp.max_length = ( len( text ) + 1 )
	doc            = nlp( text )

	# open output
	output = localLibrary/carrel/ENT/( key + EXTENSION )
	with open( output, 'w', encoding='utf-8' ) as handle :

		# _initialize the output
		handle.write( '\t'.join( HEADER ) + '\n' )

		# process each sentence
		for s, sentence in enumerate( doc.sents ) :
		
			# process each entity
			for e, entity in enumerate( sentence.ents ) :
			
				# parse and output
				value = entity.text
				type  = entity.label_
				handle.write( '\t'.join( [ key, str( s + 1 ), str( e + 1 ), value, type ] ) + '\n' )


# extract parts-of-speech
def _txt2pos( carrel, file ) :

	# configure
	EXTENSION = '.pos'
	POS       = 'pos'
	HEADER    = [ 'id', 'sid', 'tid', 'token', 'lemma', 'pos' ]

	# require
	import spacy

	# _initialize
	key          = _name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# model the text
	nlp            = spacy.load( MODEL )
	nlp.max_length = ( len( text ) + 1 )
	doc            = nlp( text )

	# open output
	output = localLibrary/carrel/POS/( key + EXTENSION )
	with open( output, 'w', encoding='utf-8' ) as handle :

		# _initialize the output
		handle.write( '\t'.join( HEADER ) + '\n' )
		
		# process each sentence
		for s, sentence in enumerate( doc.sents ) :
			
			# process each token
			for t, token in enumerate( sentence ) :

				# process non-spaces
				if token.text > ' ' :
	
					# parse and output
					feature = str( token.text )
					lemma   = str( token.lemma_.lower() )
					pos     = token.pos_
					handle.write( '\t'.join( [  key, str( s + 1 ), str( t + 1 ), feature, lemma, pos ] ) + '\n' )


# given a file, extract domains and urls
def _txt2url( carrel, file ) :

	# configure
	EXTENSION = '.url'
	URLS      = 'urls'
	HEADER    = [ 'id', 'domain', 'url']
	PATTERN   = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

	# require
	import re
	
	# _initialize
	key          = _name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# get and process each url, to the best of my ability
	urls = re.findall( PATTERN, text )
	
	# check for addresses
	if len( urls ) > 0 :

		# open output
		output = localLibrary/carrel/URLS/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8' ) as handle :

			# _initialize the output
			handle.write( '\t'.join( HEADER ) + '\n' )

			# process each url
			for url in urls :

				# remove white space from end of url
				url = re.sub( '\W$', '', url )
	
				# parse out the domain, to the best of my ability
				domain = re.sub( '.*:\/\/', '', url )
				domain = re.sub( '\/.*',    '', domain )
				domain = re.sub( '\W$',     '', domain )
	
				# output
				handle.write( '\t'.join( [ key, domain, url ] ) + '\n' )


# given a file, output keywords
def _txt2wrd( carrel, file ) :

	# configure
	EXTENSION  = '.wrd'
	WRD        = 'wrd'
	NGRAMS     = 1
	TOPN       = 0.005
	HEADER     = [ 'id', 'keyword' ]
	NORMALIZE  = 'lower'
	WINDOWSIZE = 5
	
	# require
	from  textacy.extract.keyterms.yake import yake
	import spacy
	import os
	
	# _initialize
	key          = _name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# model the text and get the keywords
	nlp            = spacy.load( MODEL )
	nlp.max_length = os.path.getsize( file ) + 1 
	doc            = nlp( text )

	# do the extraction
	try    : records = ( yake( doc, ngrams=( 1, 2 ), window_size=WINDOWSIZE, topn=TOPN, normalize=NORMALIZE ) )
	except : records = []
	
	# check for records
	if len( records ) > 0 :
	
		# open output
		output = localLibrary/carrel/WRD/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8' ) as handle :

			# _initialize the output
			handle.write( '\t'.join( HEADER ) + '\n' )

			# process each record
			for record in records :

				# do the simplest of normalization and output
				keyword = record[ 0 ]
				if len( keyword ) < 3 : continue
				handle.write( '\t'.join( ( key, keyword ) ) + '\n' )

# start tika
def _startTika() :

	# configure
	JAVA  = 'java'
	JAR   = '-jar'
	SLEEP = 20
	
	# require
	import time
	import subprocess
	
	# _initialize
	started = False
	
	# double check to see if we've already been here
	if _tikaIsRunning() : started = True
	
	# try to start tika
	else :
	
		# get the location of tika-server.jar; needs validation
		tikaHome = str( configuration( 'tikaHome' ) )	
		
		# run the server and conditionally ignore STDERR; set VERBOSE to choose
		if VERBOSE == 3 : subprocess.Popen( [ JAVA, JAR, tikaHome ] )
		else            : subprocess.Popen( [ JAVA, JAR, tikaHome ], stderr=subprocess.DEVNULL )	
		
		# hang out
		time.sleep( SLEEP )
		
		# one last time, check again
		if _tikaIsRunning() : started = True
		
	# done
	return( started )



# given a few configurations, reduce extracted features to a database
def _tsv2db( directory, extension, table, connection ) :

	# require
	import pandas as pd
	
	# debug
	if VERBOSE : click.echo( '\tProcessing ' + table, err=True )
	
	# _initialize
	found = False
	
	# process each file in the given directory
	for index, file in enumerate( directory.glob( extension ) ) :

		# more debugging
		if VERBOSE == 2 : click.echo( '\t' + str( file ), err=True )
		
		# read the file
		df = pd.read_csv( file, sep='\t', header=0, low_memory=False, on_bad_lines='warn', quoting=3, dtype='string' )
			
		# _initialize the features or append to it
		if index == 0 : features = df
		else          : features = pd.concat( [ features, df ], sort=False )

		# update
		found = True
		
	# fill the database, conditionally
	if found : features.to_sql( table, connection, if_exists='replace', index=False )


def build( carrel, directory, erase=False, start=False ) :

	"""Create <carrel> from files in <directory>

Use this command to build a data set ("study carrel") based on the files saved in a directory. Once the data set is created the other Toolbox commands can be applied to the result. The files can be of any type (PDF, Microsoft Word, HTML, etc.), and they can be of any kind (books, articles, reports, etc.), and they can be of any number (1, 2, 12, a few dozen, hundreds, etc.). The Toolbox is designed to read about a dozen journal articles in the form of PDF files. This command requires a Java tool called Tika, and it is used to convert the input files into plain text as well as extract authors, titles, and dates. If the Toolbox has not been configured and/or Tika is not installed, then the Toolbox will try to install it on your behalf. If the given directory contains a file named 'metadata.csv', then this command will use the file as the source of author, title, and date metadata values. This is often very helpful because sans metadata it is very difficult to make comparison between documents. Please see the full-blown documentation for details."""

	# configure
	CACHE  = 'cache'
	TXT    = 'txt'
	SCHEMA = '''-- parts-of-speech\ncreate table pos (\n    id    TEXT,\n    sid   INT,\n    tid   INT,\n    token TEXT,\n    lemma TEXT,\n    pos   TEXT\n);\n\n-- name entitites\ncreate table ent (\n    id     TEXT,\n    sid    INT,\n    eid    INT,\n    entity TEXT,\n    type   TEXT\n);\n\n-- keywords\ncreate table wrd (\n    id      TEXT,\n    keyword TEXT\n);\n\n-- email addresses\ncreate table adr (\n    id      TEXT,\n    address TEXT\n);\n\n-- questions\ncreate table questions (\n    id       TEXT,\n    question TEXT\n);\n\n-- urls\ncreate table url (\n    id     TEXT,\n    domain TEXT,\n    url    TEXT\n);\n\n-- bibliographics, such as they are\ncreate table bib (\n    id        TEXT,\n    words     INT,\n    sentence  INT,\n    flesch    INT,\n    summary   TEXT,\n    title     TEXT,\n    author    TEXT,\n    date      TEXT,\n    txt       TEXT,\n    cache     TEXT,\n    pages     INT,\n    extension TEXT,\n    mime      TEXT,\n    genre     TEXT\n);'''
	POS    = 'pos'
	ENT    = 'ent'
	WRD    = 'wrd'
	ADR    = 'adr'
	URL    = 'urls'
	BIB    = 'bib'
	
	# require
	from   multiprocessing import Pool
	import os
	import shutil
	import sqlite3
	import pandas as pd
	import spacy
	
	# _initialize
	localLibrary = configuration( 'localLibrary' )
	pool         = Pool()

	# make sure we have Tika Server
	_checkForTika( str( configuration( 'tikaHome' ) ) )
	
	# start tika; the toolbox's secret sauce
	if start :
	
		# debug
		click.echo( '(Step #-1 of 9) Starting Tika server at http://localhost:9998/; please be patient.', err=True )
		
		# go
		if _startTika() == False :
		
			# bummer
			click.echo( "Can't start Tika. Call Eric.", err=True )
			exit()

	# check for tika
	if not _tikaIsRunning() :
	
		click.echo( '''
  WARNING: Tika server at http://localhost:9998/ is not running;
  please start Tika by hand, or add -s to this command.
''', err=True )
		exit()
	
	
	# check tika version here
	
	
	# check to see if the language model has been installed
	try            : nlp  = spacy.load( MODEL )
	except OSError : modelNotFound()

	# check for pre-existing carrel
	if ( localLibrary/carrel ).is_dir() :
	
		# check for erase
		if erase :
		
			# debug and do the work
			click.echo( ( '(Step #0 of 9) Deleting %s' % ( localLibrary/carrel ) ), err=True )
			shutil.rmtree( localLibrary/carrel )
			
		# carrel exists and erasing was not specified
		else :
		
			# warn and exit
			click.echo( ( '''
  WARNING: Carrel exists; specify a name other than "%s" or add -e
  to erase it.''' % carrel ), err=True )
			exit()

	# build skeleton
	click.echo( '(Step #1 of 9) Initializing %s with %s and stop words' % ( carrel, directory ), err=True )
	_initialize( carrel, directory )
		
	# create a list of filenames to process
	filenames = []
	cache     = localLibrary/carrel/CACHE
	for filename in os.listdir( cache ) :
	
		# update list, conditionally
		if filename[ 0 ] == '.' : continue
		else                    : filenames.append( os.path.join( cache, filename ) )
	
	# conditionally slurp up the metadata file and submit 
	click.echo( '(Step #2 of 9) Extracting bibliographics and converting documents to plain text', err=True )
	
	# check for metadata file
	if ( localLibrary/carrel/METADATA ).exists() :
	
		try : metadata = pd.read_csv( localLibrary/carrel/METADATA, index_col='file' )
		except ValueError :
			click.echo( ( '\n  Error: The metadata file (metadata.csv) does not have a\n  column named "file". Remove metadata.csv from the original\n  input directory:\n\n    %s\n\n  Alternatively, edit the metadata file accordingly. Exiting.\n' % directory ), err=True )
			exit()

		pool.starmap( _file2bib, [ [ carrel, filename, metadata ] for filename in filenames ] )
		
	# no metadata file; just do the work
	else : pool.starmap( _file2bib, [ [ carrel, filename ] for filename in filenames ] )
		
	# bag of words
	click.echo( '(Step #3 of 9) Creating bag-of-words', err=True )
	_txt2bow( carrel )
	
	# output hint
	click.echo( ( "\n  Hint: Now that the bag-of-words has been created, you can begin\n  to use many of the other Reader Toolbox commands while the\n  building process continues. This is especially true for larger\n  carrels. Open a new terminal window and try:\n\n    rdr cluster %s\n    rdr ngrams %s -c | more\n    rdr concordance %s\n    rdr collocations %s\n" % ( carrel, carrel, carrel, carrel ) ), err=True )
	
	# re-create a list of filenames to process
	filenames = []
	txt       = localLibrary/carrel/TXT
	for filename in os.listdir( txt ) : filenames.append( os.path.join( txt, filename ) )

	# extract email addresses
	click.echo( '(Step #4 of 9) Extracting (email) addresses', err=True )
	pool.starmap( _txt2adr, [ [ carrel, filename ] for filename in filenames ] )
	
	# extract named entities
	click.echo( '(Step #5 of 9) Extracting (named) entities', err=True )
	pool.starmap( _txt2ent, [ [ carrel, filename ] for filename in filenames ] )
	
	# extract parts-of-speech
	click.echo( '(Step #6 of 9) Extracting parts-of-speech', err=True )
	pool.starmap( _txt2pos, [ [ carrel, filename ] for filename in filenames ] )

	# extract urls
	click.echo( '(Step #7 of 9) Extracting URLs', err=True )
	pool.starmap( _txt2url, [ [ carrel, filename ] for filename in filenames ] )

	# extract keywords
	click.echo( '(Step #8 of 9) Extracting (key) words', err=True )
	pool.starmap( _txt2wrd, [ [ carrel, filename ] for filename in filenames ] )

	# clean up
	pool.close()

	# create database
	click.echo( '(Step #9 of 9) Creating and filling database (reducing)', err=True )
	database   = str( localLibrary/carrel/ETC/DATABASE )
	connection = sqlite3.connect( database )
	cursor     = connection.cursor()
	cursor.executescript( SCHEMA )
	
	# reduce; fill it with content
	_tsv2db( localLibrary/carrel/POS, '*.pos', 'pos', connection )
	_tsv2db( localLibrary/carrel/ENT, '*.ent', 'ent', connection )
	_tsv2db( localLibrary/carrel/WRD, '*.wrd', 'wrd', connection )
	_tsv2db( localLibrary/carrel/ADR, '*.adr', 'adr', connection )
	_tsv2db( localLibrary/carrel/URL, '*.url', 'url', connection )
	_tsv2db( localLibrary/carrel/BIB, '*.bib', 'bib', connection )

	# output another hint
	# out hint
	click.echo( ( '\n  Another hint: The build process is done, and now you ought to\n  be able to use any Toolbox command. For example:\n\n    rdr info %s\n    rdr bib %s | more\n    rdr tm %s\n' % ( carrel, carrel, carrel ) ), err=True )

def summarize( carrel, look=False ) :

	'''Summarize <carrel>
	
	The use of this command will generate a set of reports and save them in specific locations in <carrel>'s file system. If you specify the -l (look) option, then <carrel>'s index.htm file will be opened in your Web browser. You can subsequently use rdr read <carrel> to open the index.htm file.'''

	# sanity check
	checkForCarrel( carrel )
	
	# save bibliography
	click.echo( "Creating bibliography", err=True )
	bibliography( carrel, 'text', save=True )
	bibliography( carrel, 'html', save=True )
	bibliography( carrel, 'json', save=True )
			
	# save sizes	
	click.echo( "Graphing sizes", err=True )
	sizes( carrel, output='boxplot',   save=True )
	sizes( carrel, output='histogram', save=True )
		
	# save readability	
	click.echo( "Graphing readability", err=True )
	flesch( carrel, output='boxplot',   save=True )
	flesch( carrel, output='histogram', save=True )
	
	# save cluster	
	click.echo( "Graphing clusters", err=True )
	cluster( carrel, type='cube',       save=True )
	#ctx.invoke( cluster.cluster, carrel=carrel, type='dendrogram', save=True )
	
	# save ngrams	
	click.echo( "Graphing ngrams", err=True )
	ngrams( carrel, count=True, size=1, wordcloud=True, save=True )
	ngrams( carrel, count=True, size=2, wordcloud=True, save=True )
	
	# save entities	
	click.echo( "Graphing entities", err=True )
	entities( carrel, count=True, select='entity', like='any',    wordcloud=True, save=True )
	entities( carrel, count=True, select='entity', like='PERSON', wordcloud=True, save=True )
	entities( carrel, count=True, select='entity', like='GPE',    wordcloud=True, save=True )
	entities( carrel, count=True, select='entity', like='ORG',    wordcloud=True, save=True )
	
	# save pos	
	click.echo( "Graphing parts-of-speach", err=True )
	pos( carrel, count=True, select='lemmas', like='NOUN',  wordcloud=True, save=True )
	pos( carrel, count=True, select='lemmas', like='VERB',  wordcloud=True, save=True )
	pos( carrel, count=True, select='lemmas', like='ADJ',   wordcloud=True, save=True )
	pos( carrel, count=True, select='lemmas', like='ADV',   wordcloud=True, save=True )
	pos( carrel, count=True, select='lemmas', like='PRON',  wordcloud=True, save=True )
	pos( carrel, count=True, select='lemmas', like='PROPN', wordcloud=True, save=True )
	
	# save keywords	
	click.echo( "Graphing keywords", err=True )
	keywords( carrel, count=True, wordcloud=True, save=True )
	
	# create html
	click.echo( "Building HTML page", err=True )
	html = TEMPLATE.replace( '##CARREL##', carrel )
	html = html.replace( '##ITEMS##', str( extents( carrel, 'items' ) ) )
	html = html.replace( '##WORDS##', str( extents( carrel, 'words' ) ) )
	html = html.replace( '##FLESCH##', str( extents( carrel, 'flesch' ) ) )
	html = html.replace( '##DATECREATED##', str( provenance( carrel, 'dateCreated' ) ) )
	html = html.replace( '##CREATOR##', str( provenance( carrel, 'creator' ) ) )
	
	# save html
	locallibrary = configuration( 'localLibrary' )
	with open( locallibrary/carrel/INDEX, 'w', encoding='utf-8' ) as handle : handle.write( html )
	
	# read, 
	if look : read( carrel )

