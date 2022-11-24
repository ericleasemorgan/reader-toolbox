# rdr.py - a command-line interface for building and modeling Distant Reader study carrels

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 30, 2021 - in Three Oaks with Pat; first real working version
# June 14, 2022 - trying to consolidate everything into a single file



# constants for topic modeling
MODELDIR        = 'etc/topic-model'
VECTORS         = 'model.vec'
TXT2VEC         = "%s/bin/mallet import-dir --input %s --output %s --keep-sequence TRUE --stoplist-file %s"
VEC2MODEL       = "%s/bin/mallet train-topics --input %s --num-topics %s --num-top-words %s --num-top-docs %s --num-iterations %s --num-threads 48 --optimize-interval 10 --output-doc-topics %s/topics.tsv --output-state %s/model-state.gz --output-topic-docs %s/documents.txt --output-topic-keys %s/keys.tsv --topic-word-weights-file %s/weights.tsv --word-topic-counts-file %s/counts.txt --xml-topic-phrase-report %s/phrases.xml --xml-topic-report %s/topics.xml"
KEYS            = 'keys.tsv'
KEYSHEADER      = [ 'ids', 'weights', 'features' ]
DOCUMENTS       = 'documents.txt'
DOCUMENTSHEADER = [ 'ids', 'dids', 'files', 'proportions' ]
TOPDOCS         = 5
SCALE           = 100
PERCENTAGE      = '%1.0f%%'
SQL             = 'SELECT "file:%s/%s/txt/" || cast( id AS text ) || ".txt" AS file, %s FROM bib order by %s;'
METADATA        = 'metadata.csv'
TOPICS          = 'topics.tsv'
LABELS          = [ 'docId', 'file' ]


# require
from rdr import *

#####

def _makeSummary( keys, header ) :

	# require
	import pandas as pd

	# read and sort keys file
	keys = pd.read_csv( keys, sep='\t', names=header )
	keys.sort_values( by='weights', ascending=False, inplace=True )

	# create labels for each topic
	labels = []
	for index, row in keys.iterrows() :

		# parse
		features = row[ 'features' ].split()

		# loop through each feature
		for feature in features :

			# build the list, conditionally
			if feature in labels : continue
			labels.append( feature )
			break

	# add the labels, rearrange (just for fun)
	keys[ 'labels' ] = labels
	keys = keys[ [ 'labels', 'weights', 'features' ] ]

	# done
	return keys


def _checkForMallet( mallet ) :
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	from requests     import get
	from tempfile     import TemporaryFile
	from zipfile      import ZipFile
	
	# install mallet, conditionally
	if not Path( mallet ).exists() :
	
		click.echo( "\n  WARNING: MALLET not found. Downoading... ", err=True )
		response = get( MALLETZIP )

		# initialize a temporary file and write to it
		click.echo( "\n  INFO: Saving zip file... ", err=True )
		handle = TemporaryFile()
		handle.write( response.content )

		# unzip the temporary file and close it, which also deletes it
		click.echo( "\n  INFO: Unziping zip file... " )
		with ZipFile( handle, 'r' ) as zip : zip.extractall( Path.home() )
		
		# initialize
		click.echo( "\n  INFO: Updating configurations... " )
		configurations          = ConfigParser()
		applicationDirectory    = Path.home()
		configurationFile       = applicationDirectory/CONFIGURATIONFILE
		localLibrary            = configuration( 'localLibrary' )
		tikaHome                = configuration( 'tikaHome' )
		notebooksHome           = configuration( 'notebooksHome' )
		malletHome              = Path.home()/'mallet'
		configurations[ "RDR" ] = { "localLibrary"  : localLibrary, "malletHome" : malletHome, "tikaHome" : tikaHome, 'notebooksHome' : notebooksHome }
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )

		# make mallet executable
		click.echo( "\n  INFO: Making MALLET executable... " )
		(malletHome/MALLETBIN).chmod( 0x755 )

		# done
		click.echo('''
  INFO: MALLET has been downloaded to your home directory and
  configured for future use. You can move MALLET to another
  location but once you do so you will need to run 'rdr set -s
  mallet'.
''', err=True )


def _pivot( localLibrary, carrel, field, keys ) :

	# require
	import sqlite3
	import pandas as pd
	
	# initialize
	db         = str( localLibrary/carrel/ETC/DATABASE )
	sql        = ( SQL % ( str( localLibrary ), carrel, field, field ) )
	metadata   = str( localLibrary/carrel/MODELDIR/METADATA )
	topics     = str( localLibrary/carrel/MODELDIR/TOPICS )
	connection = sqlite3.connect( db )

	# search and save; should probably eliminate the I/O
	results    = pd.read_sql_query( sql, connection )
	results.to_csv( metadata, index=False )

	# read saved files
	topics   = pd.read_csv( topics, sep='\t' )	
	metadata = pd.read_csv( metadata )
	
	# create generic labels
	labels  = LABELS
	columns = topics.shape[ 1 ]
	for i in range( 0, columns - 2 ) :

		# compute and update list of column names
		i = str( i )
		labels.append( i )
	
	# create more meaningful labels; initialize some more
	keys = pd.read_csv( keys, sep='\t', names=KEYSHEADER )
	keys.sort_values( by='weights', ascending=False, inplace=True )
	
	# add labels, drop docId, and merge with metadata
	topics   = pd.read_csv( str( localLibrary/carrel/MODELDIR/TOPICS ), sep='\t', names=labels )	
	topics         = topics.drop( [ 'docId' ], axis=1 )
	topics         = pd.merge( topics, metadata )

	# create meaningful labels for each topic
	ids    = []
	labels = []
	for index, row in keys.iterrows() :

		# update the list of ids
		ids.append( index )

		# get and loop through each feature
		features = row[ 'features' ].split()
		for feature in features :

			# build the list, conditionally
			if feature in labels : continue
			labels.append( feature )
			break

	# update with generic labels
	keys[ 'labels' ] = labels

	# process each id; update with more meaningful labels
	for index, id in enumerate( ids ) :

		column = str( id )
		label  = labels[ index ]
		topics.rename( columns = { column:label }, inplace=True )

	# _pivot and return
	topics = topics.pivot_table( list( topics.columns ), index=field )
	return( topics )


# define; launch
def _launch( directory, jupyter ) :

	# require
	import pathlib
	import os
	
	# initialize
	directory = pathlib.Path( directory )

	# make sane, launch jupyter, and done
	os.chdir( directory )
	os.system( jupyter )


# define; catalog
def _catalog( directory, pattern ) :

	# require
	import pathlib
	import json

	# initialize
	directory = pathlib.Path( directory ).glob( pattern )
	notebooks = sorted( [ file for file in directory ] )

	# process each notebook
	for notebook in notebooks : 

		# read notebook
		with open( notebook ) as handle : data = json.loads( handle.read() )
		
		# parse and normalize
		name  = pathlib.PurePosixPath( notebook ).name
		title = data[ 'cells' ][ 0 ][ 'source' ][ 0 ].replace( '#', '' ).replace( '\n', ' ' )
		note  = data[ 'cells' ][ 1 ][ 'source' ][ 0 ].replace( '\n', ' ' )
		
		# output
		print( "  *%s (%s) - %s\n" % ( title, name, note ) )


# define; download
def _download( directory, protocol, organization, repository, remote ) :

	# require
	import fsspec
	import pathlib

	# initialize
	destination = pathlib.Path( directory )
	destination.mkdir( exist_ok=True, parents=True )
	filesystem  = fsspec.filesystem( protocol, org=organization, repo=repository )

	# do the work and done
	filesystem.get( filesystem.ls( remote ), destination.as_posix() )


# initialize 
@click.group()
def rdr() :

	# require
	from configparser import ConfigParser
	from pathlib      import Path

	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE

	# create configuration file, conditionally
	if not configurationFile.exists() : initializeConfigurations()

	# continue
	pass


# about
@click.command( options_metavar='<options>' )
def cmdAbout() :

	"""Output a brief description of the Reader Toolbox (rdr) application."""

	# configure
	ABOUT = '''
  The Reader Toolbox (rdr) is a command-line application used to create
  and model data sets called Distant Reader study carrels.
'''

	# do the work and done
	click.echo( ABOUT )


# addresses
@click.command( options_metavar='<options>' )
@click.option('-l', '--like',   type=click.STRING, help="filter results using the given pattern")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdAdr( carrel, count, like ) :

	"""Filter email addresses from <carrel>

	Who are you gonna call? 

	Examples:

	\b
	  rdr adr ital
	  rdr adr -c ital
	  rdr adr -c -l gmail ital

	See also: rdr url --help"""

	# do the work and return it
	click.echo( addresses( carrel, count, like ) )


# bibliographics
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-f', '--format', default='text', type=click.Choice( [ 'text', 'html', 'json' ] ), help='type of output')
@click.option('-v', '--save', is_flag=False, help='save result in default location')
def cmdBib( carrel, format, save ) :

	"""Output rudimentary bibliographics from <carrel>

	Use this subcommand to output metadata regarding the specific items in <carrel>. Metadata on the items includes: identifier, author, title, date, size in words, readability (Flesch) score, summary, keywords, location of cached original, and location of derived plain text. Because of the characteristics of the original input used to create <carrel>, some metadata fields may not have values. Author and date are the best examples. Moreover, the value for title be derived. The combined use of the info command and the bib command will garaner you a good understanding of <carrel>'s breadth and depth.

	Example: rdr bib homer

	See also:
	
	\b
	  rdr info --help
	  rdr search --help"""

	if save : bibliography( carrel, format, save )
	else    : click.echo( bibliography( carrel, format ) )


# download
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def cmdDownload( carrel ) :

	"""Cache <carrel> from the public library of study carrels

	A collection of about 3,000 pre-created study carrels is available at http://library.distantreader.org. Given <carrel>, this function will download the remote carrel and save it to your local library. You can then use the Toolbox commands to read it.

	Examples:
	
	\b
	  rdr download homer
	  rdr download pride
	  rdr download sonnets

	See also:
	
	\b
	  rdr catalog --help
	  rdr set --help"""
			
	# do the work and give a hint
	download( carrel )
	click.echo( ( '''  INFO: You may now any of the RDR commands. For example:

	* rdr info %s
	* rdr bib %s
	* rdr cluster %s
	* rdr ngrams %s -s 2 -c
	* rdr wrd %s -c
	* rdr tm %s
''' ) % ( carrel, carrel, carrel, carrel, carrel, carrel, ), err=True )


# catalog
@click.command( options_metavar='<options>' )
@click.option('-h', '--human', is_flag=True, help='output in a more human-readable form')
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='output in a more human-readable form')
def cmdCatalog( human, location ) :

	"""List study carrels
	
	Use this command to enumerate the study carrels cached locally or remotely available at http://library.distantreader.org. The remote option, by default, returns a tab-delimited stream very amenable to post processing with utilities such as cut, grep, sort, and less.
	
	Examples:
	
	\b
	  rdr catalog
	  rdr catalog -l remote
	  rdr catalog -l remote -h

	See also: rdr download --help"""
	
	# do the work and done
	click.echo( catalog( location, human ) )


# search
@click.command( options_metavar='<options>' )
@click.option('-o', '--output', default='human', type=click.Choice( [ 'human', 'csv', 'tsv', 'json', 'count' ] ), help='the format of the results')
@click.option('-q', '--query', default='love', help='a full text query')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdSearch( query, output, carrel ) :

	'''Perform a full text query against <carrel>
	
	Given words, phrases, fields, and Boolean operators, use this subcommand to find and describe specific items in <carrel>. The query language is quite extensive, but in general, use words and/or phrases, and a list of matching documents ought to be returned. For more detail, please see: https://reader-toolbox.rtfd.io/en/latest/commands.html#search
	
	Examples:
	
	\b
	  rdr search -q 'truth beauty war love' homer
	  rdr search -q 'title:iliad AND summary:war' homer
	  rdr search -q '"keep his anger"' homer'''

	# do the work and done
	click.echo( search( carrel, query, output ) )


# word2vec
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-t', '--type', default='similarity', type=click.Choice( [ 'similarity', 'distance', 'analogy', 'scatter' ], case_sensitive=True ), help="query type")
@click.option('-q', '--query', default='love', help='the word(s) to be used for search')
@click.option('-s', '--size', default=10, help='number of results to return')
def cmdSemantics( carrel, type, query, size ) :

	'''Apply semantic indexing against <carrel>
	
	Sometimes called "word embedding", use this subcommand to learn: 1) what words are similar to a given word, 2) how close in meaning sets of words are, or 3) what words compare to three other words. In order to work accurately, semantic indexing requires larger rather than smaller corpora; results from corpora less than 1,500,000 words in size ought to be considered dubious at best.
	
	This command requires a Python module called "word2vec", which is not installed by default. This is because the module needs to be compiled and doing so on Windows computers is challenging. Linux and Macintosh users can probably do 'pip install word2vec', but Windows users will have to go through additional hoops. But please be consoled when you remember that corpora less than 1.5 million words do not return accurate results. Is <carrel> 1.5 million words long?
	
	Examples:
	
	\b
	  rdr semantics -t similarity -q war homer
	  rdr semantics -t distance -q "king queen prince love war" homer
	  rdr semantics -t analogy -q "king queen prince" homer'''

	# do the work and done
	click.echo( word2vec( carrel, type, query, size ) )

	
# collocations
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-f', '--filter',  default=4, help="least number of occurances of bigram")
@click.option('-m', '--measure', default='chisqr', type=click.Choice( [ 'fisher', 'chisqr', 'jaccard', 'likelihood', 'raw' ], case_sensitive=True ), help="type of measure")
@click.option('-l', '--limit',   default=4000, help="number of features")
@click.option('-w', '--window',  default=4, help="size of window")
@click.option('-o', '--output',  default='image', type=click.Choice( [ 'image', 'gml' ], case_sensitive=True ), help="type of output")
@click.option('-v', '--save',    is_flag=True, help='save graph to default location')
def cmdCollocations( carrel, window, filter, measure, limit, output, save ) :

	'''Output network graph based on bigram collocations in <carrel>

	This is an additional way of answering the questions: 1) what words are spoken in the same breath as other words, and 2) what words taken together connote themes. Given a study carrel of about 200,000 words, the default values ought to generate a network graph with enough depth to be interesting. Specify the -o option to output a Graph Modeling Language (GML) file, and load the result into a visualizer like Gephi. If the image output by the Toolbox is not very dense, then iteratively increase or decrease the values of -l and -f until the density is appealing. The various measures are used to denote the significance of collocations.

	Examples:

	\b
	  rdr networks homer
	  rdr networks homer -o gml > homer.gml
	  rdr networks homer -l 2000 -f 18 -w 5
	  rdr networks homer -l 2000 -f 18 -w 5 -o gml > homer.gml
	  rdr networks pride -l 1600 -f 8'''

	# do the work
	collocate( carrel, window, filter, measure, limit, output, save )

	
# grammars
@click.command( options_metavar='<options>' )
@click.option('-g', '--grammar', default='svo', type=click.Choice( [ 'svo', 'sss', 'nouns', 'quotes' ], case_sensitive=True ), help="the desired grammatical structure")
@click.option('-q', '--query',   type=click.STRING, help="filter results using the given regular expression")
@click.option('-n', '--noun',    type=click.STRING, help="only applicable to sss; a noun or noun phrase")
@click.option('-l', '--lemma',   default='be', help="only applicable to sss; the lemma of a verb, such as 'be' (default), 'have', or 'say'")
@click.option('-s', '--sort',    is_flag=True, help='order the results alphabetically')
@click.option('-c', '--count',   is_flag=True, help='tabulate the items in the result')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdGrammars( carrel, grammar, query, noun, lemma, sort, count ) :

	"""Extract sentence fragments from <carrel> as in:
	
	\b
	  nouns - all the nouns and noun chunks
	  quotes - things people say
	  svo - fragments in the form of subject-verb-object (the default)
	  sss - a more advanced version of svo; fragments beginning
	    with an entity, co-occur with a verb, and are followed
	    by a phrase
	
	This is very useful for the purposes of listing more complete ideas from a text; the default output will list bunches o' snippets listing what things do to what. Sort the result to more easily identify patterns and anomalies.
	
	Examples:
	
	\b
	  rdr grammars homer
	  rdr grammars -g nouns homer
	  rdr grammars -g sss -n hector -l be homer"""
	
	# do the work
	click.echo( grammars( carrel, grammar, query, noun, lemma, sort, count ) )
	

# cluster
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-t', '--type', default='dendrogram', type=click.Choice( [ 'dendrogram', 'cube' ] ), help='denote the shape of the output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def cmdCluster( carrel, type, save ) :

	"""Apply dimension reduction to <carrel> and visualize the result
	
	This is useful for determining how holistic <carrel> is. A carrel with many clusters is less holistic and probably means the number of latent topics (think "subjects") is high. On the other hand, you may observe clusters falling into distinct groups surrounding authors, titles, or sources. In other words, use this subcommand to learn the degree <carrel> is a hodgepodge of items or a collection of related items. 
	
	Example: rdr cluster homer
	
	See also: rdr tm --help"""

	# do the work
	cluster( carrel, type, save )


# named entities
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--select',    default='type', type=click.Choice( [ 'type', 'entity' ] ), help='the type of output')
@click.option('-l', '--like',      default='any', help='the type of enity')
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, output a wordcloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save cloud to default location')
def cmdEnt( carrel, select, like, count, wordcloud, save ) :

	"""Filter named entities and types of entities found in <carrel>

	Use this subcommand to address who, what, when, and where questions regarding <carrel>. A spaCy language model was applied to each item in your study carrel. This process extracted named-entities (persons, places, organizations, dates, times, etc.) and saved them in files located in the ent directory of <carrel>. This same data was also distilled into a relational database file, and this subcommand queries that database file. Through the use of this subcommand, you can learn what people are mentioned, what places are mentioned, what dates and times are mentioned, etc. Based on these things, you will be able to characterize <carrel>. For example, are the mentioned people Platonists? Does most of the action take place in American or someplace in Europe, and if so, then where? Finally, the spaCy model works well, most of the time. There will be errors, but please don't let the perfect be the enemy of the good.

	Examples:
	
	\b
	  rdr ent homer
	  rdr ent -c homer
	  rdr ent -s entity -c homer
	  rdr ent -s entity -l PERSON -c homer
	  
	See also: rdr pos --help"""

	# do the work
	if not wordcloud : click.echo( entities( carrel, select, like, count ) )
	else             : entities( carrel, select, like, count, wordcloud, save )


# parts-of-speech
@click.command( options_metavar='<options>' )
@click.option('-s', '--select',    default='parts', type=click.Choice( [ 'parts', 'words', 'lemmas' ] ), help='the type of output')
@click.option('-l', '--like',      default='any', help='the part-of-speech')
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-n', '--normalize', is_flag=True, help='lower-case the words or lemmas')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, output a wordcloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save cloud to default location')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdPos( carrel, select, like, count, normalize, wordcloud, save ) :

	"""Filter parts-of-speech, words, and lemmas found in <carrel>

	Use this subcommand to address questions such as: what is mentioned in <carrel>, what do those things do, and how are they described. A spaCy language model was applied to every item in <carrel>. The model was used to denote nouns, verbs, adjectives, punctuation, etc. It was also used to denote the lemma values (think "root") of each word. This information was saved in files in the pos directory of <carrel>, but it has also been saved in a relational database. This subcommand queries that database. Using this commmand, you can begin to characterize an author's style, learn to what degree the action about saying, examining, or doing, and more importantly, put words into context because they have been associated with specific parts-of-speech values. Finally, the spaCy model works well, most of the time. Please don't let the perfect be the enemy of the good.

	Examples:

	\b
	  rdr pos homer
	  rdr pos -c homer
	  rdr pos -s words -l N -c homer
	  rdr pos -s lemmas -l N -c -n homer
	  rdr pos -s lemmas -l V -c -n homer

	See also:
	
	\b
	  rdr ngrams --help
	  rdr ent --help"""

	# do the work and done
	if not wordcloud : click.echo( pos( carrel, select, like, count, normalize ) )
	else             : pos( carrel, select, like, count, normalize, wordcloud, save )


# ngrams
@click.command( options_metavar='<options>' )
@click.option('-q', '--query',     type=click.STRING, help="filter results to include the given regular expression")
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-l', '--location',  default='local', type=click.Choice( [ 'local', 'remote' ] ), help='where is the study carrel')
@click.option('-s', '--size',      default=1, help='denote unigrams, bigrams, trigrams, etc')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, output a wordcloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save cloud to default location')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdNgrams( carrel, size, query, count, location, wordcloud, save ) :

	"""Output and list words or phrases found in <carrel>

	This is almost always one of the first places to start when doing your analysis, and it can be applied to local as well as remote study carrels. Ngrams with sizes (-s) greater than 2 will include stopwords because ngrams of three or more words often do not make sense without them. Use the -c option to count and tabulate the result. Use the query (-q) to filter the result with a regular expression. 

	Examples:

	\b
	  rdr ngrams homer
	  rdr ngrams -s 2 homer
	  rdr ngrams -s 2 -c homer
	  rdr ngrams -s 2 -c -q love homer
	  rdr ngrams -s 2 -c -q love homer | more
	  rdr ngrams -s 2 -c -q love -l remote sonnets | more

	See also: rdr concordance --help"""

	if not save : click.echo( ngrams( carrel, size, query, count, location, wordcloud ) )
	else        : ngrams( carrel, size, query, count, location, wordcloud, save )


# readability
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='score', type=click.Choice( [ 'id', 'score' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def cmdReadability( carrel, sort, output, save ) :

	"""Report on the readability (Flesch score) of items in <carrel>
	
	It is possible to denote how difficult a text is to read by measuring things like number of words, density of the vocabulary, the length of a document, etc. Such calculations have been done against <carrel>, and this subcommand will output the results. If the returned values are wide-ranging, then this will tell you one thing about <carrel>. For example, some of the documents are either difficult to read, very long, or poorly transcribed ("OCR'ed"). If the measurements are homogeneous, then your carrel is more sane than not.
	
	Example: rdr readability homer -o boxplot"""

	# do the work
	if not save : click.echo( flesch( carrel, sort, output ) )
	else        : flesch( carrel, sort, output, save )


# sizes
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='words', type=click.Choice( [ 'id', 'words' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def cmdSizes( carrel, sort, output, save ) :

	"""Report on the sizes (in words) of items in <carrel>"""

	# do the work
	click.echo( sizes( carrel, sort, output, save ) )


# concordance
@click.command( options_metavar='[<options>]' )
@click.option('-w', '--width', default=40, help='number of characters on each side of <query>')
@click.option('-q', '--query', default='love', help='a word, phrase, or regular expression')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdConcordance( carrel, query, width ) :

	"""A poor man's search engine
	
	Given a query, this subcommand will search <carrel> and return a list of results where each result is a set of words to the left of query, the query, and a set of words to the right of query -- a keyword-in-context index. This is useful for answering the question, "What words are used in the same breath as the given word?" The query can be a phrase, but it can not be a regular expression. Consider creating a word cloud from the output of this command to visualize the "words used in the same breath". 
	
	Examples:
	
	\b
	  rdr concordance homer -q hector
	  rdr concordance homer -q 'hector was'

	See also: rdr ngrams --help"""
	
	# do the work
	for line in concordance( carrel, query, width ) : click.echo( line )


# keywords
@click.command( options_metavar='<options>' )
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, visualize as word cloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save result in defaul location')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdWrd( carrel, count, wordcloud, save ) :

	"""Filter statistically computed keywords from <carrel>

	Use this subcommand to address the question, "What is <carrel> about?" Algorithms akin to the venerable TF/IDF and Google's PageRank were used against each item in <carrel> to extract statistically significant keywords (think "subject terms"). These words were saved in files in the wrd directory of <carrel>, and they have been saved to a relational database as well. This command queries that database. The results of this command help you describe the "aboutness" of <carrel> and the keywords can be used to increase precision/recall when doing full text searches. Consider also the use of the resulting keywords as input to the concordance subcommand.

	Examples:

	\b
	  rdr wrd homer
	  rdr wrd -c homer

	See also:
	
	\b
	  rdr concordance --help
	  rdr search --help"""

	# do the work and conditionally output
	if not wordcloud : click.echo( keywords( carrel, count ) )
	else             : keywords( carrel, count, wordcloud, save )


# urls
@click.command( options_metavar='<options>' )
@click.option('-s', '--select', default='url', type=click.Choice( [ 'url', 'domain' ] ), help='full URLs or just domain')
@click.option('-l', '--like',   type=click.STRING, help="filter results using the expression")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdUrl( carrel, select, count, like ) :

	"""Filter URLs and domains from <carrel>

	Use this subcommand to learn what is hyperlinked from <carrel>. To the best of its ability, the Distant Reader extracted all the URLs found in <carrel>. This information was saved in sets of files located in the urls directory of <carrel>. This information as has been saved in a relational database file. This subcommand queries that database. Use this command to learn what URLs are in the carrel and from what domains do the URLs emanate. Through this process you may identify URLs of extreme importance or characterize the URLs as coming from governments, companies, organizations. Alternatively, you may create lists of URLs that can be fed to Internet spiders for harvesting or feeding back into the Reader for additional carrel creation. Be forewarned. The plain text whence these URLs came is ugly, thus producing ugly URLs; not all values for URLs are valid.

	Examples:

	\b
	  rdr url ital
	  rdr url -s url ital
	  rdr url -s url -l .pdf ital
	  rdr url -s domain -c ital

	See also: rdr adr --help"""

	# do the work and return it
	click.echo( urls( carrel, select, count, like ) )


# read
@click.command( options_metavar='<options>' )
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='where is the carrel')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdRead( carrel, location ) :
	"""Open <carrel> in your Web browser
	
	Use this subcommand to peruse the narrative texts and interactive reports found in <carrel>; use this command to become familiar with the content of <carrel>. As of this writing, carrels created with the build command do not create the narrative reports, and consequently this command will fail ungracefully.
	
	Examples:
	
	\b
	  rdr read homer
	  rdr read -l remote homer
	  rdr read -l remote sonnets
	  rdr read -l remote pride
	
	See also: rdr browse --help"""

	read( carrel, location )


@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def cmdSql( carrel ) :

	"""Use SQL queries against the database of <carrel>
	
	Study carrels are made up of many files. One of those files is an SQLite database file (etc/reader.db). Use this subcommand to query the database. Because the database is relational in design, the use of SQL can draw information from many different tables and address almost any question about <carrel>. An excellent query that an be applied to any carrel includes:
	
	\b
	  SELECT b.id, GROUP_CONCAT( w.keyword, '; ' ) AS keywords, b.summary
	  FROM bib AS b, wrd AS w
	  WHERE b.id = w.id
	  GROUP BY b.id
	  ORDER BY b.id;
	
	Example: rdr sql homer"""

	# configure
	DATASETTE = 'datasette'
		
	# require
	from os import system
	
	# sanity check
	checkForCarrel( carrel )

	# initialize
	localLibrary = configuration( 'localLibrary' )

	# build the shell command and go
	database = localLibrary/carrel/ETC/DATABASE
	system( DATASETTE + ' ' + str( database ) + ' -o' )


@click.command( options_metavar='<options>' )
def cmdDocumentation() :

	"""Use your Web browser to read the Toolbox (rdr) online documentation."""

	# require
	from webbrowser import open

	click.echo( "Your Web browser is being used to open the Toolbox online documentation.", err=True )
	url = DOCUMENTATION
	open( url )


@click.command( options_metavar='[<options>]' )
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='the location of the carrel')
@click.argument( 'carrel', metavar='<carrel>' )
def cmdBrowse( carrel, location ) :

	"""Peruse <carrel> as a file system
	
	Study carrels are sets of HTML files, other plain text files, a whole lot of tab-delimited files, and an SQLite database file all organized in a file system -- a data set. This command uses a two different techniques for browsing the file systems. If the study carrel is saved locally, then it will try to use a terminal-based Web browser call Lynx. If the carrel is remote, then you will be directed to a dynamically generated HTML page. Because all study carrels have the same layout, this subcommand is useful for learning how many files and of what type are contained in <carrel>.
	
	Examples:
	
	\b
	  rdr browse homer
	  rdr browse -l remote homer
	
	See also: rdr read --help"""

	# configure
	LYNX = 'lynx'
	
	# require
	from os import system
	import webbrowser
	
	# local carrel
	if location == 'local' :
	
		# sanity check
		checkForCarrel( carrel )

		# initialize, create a URL, and do the work
		localLibrary = str( configuration( 'localLibrary' ) )
		url          = 'file://' + localLibrary + '/' + carrel
		system( LYNX + ' ' + url )

	# remote carrel
	elif location == 'remote' :
	
		url = '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, MANIFEST ] )
		webbrowser.open( url )


# config
@click.command()
@click.option('-s', '--setting', default='local', type=click.Choice( [ 'local', 'mallet', 'tika', 'notebooks' ] ), help='output the given setting')
def cmdGet( setting ) :

	"""Echo the values denoted by the set subcommand
	
	This is useful for verifying where your locally cached study carrels are saved as well as where you have saved either the MALLET subsystem or Tika. 
	
	Example: rdr get
	
	See also: rdr set --help"""
	
	# branch accordingly
	if   setting == 'local'     : click.echo( str( configuration( 'localLibrary' ) ) )
	elif setting == 'mallet'    : click.echo( str( configuration( 'malletHome' ) ) )
	elif setting == 'tika'      : click.echo( str( configuration( 'tikaHome' ) ) )
	elif setting == 'notebooks' : click.echo( str( configuration( 'notebooksHome' ) ) )
	
	
# config
@click.command()
@click.option('-s', '--setting', type=click.Choice( [ 'local', 'mallet', 'tika', 'notebooks' ] ), help='configure the given setting')
@click.option('-e', '--erase', is_flag=True, help='erase/restore default settings')
def cmdSet( setting, erase ) :

	"""Configure the location of study carrels, the subsystem called MALLET, and Tika
	
	In order to read study carrels, they need to be saved on your computer, and the primary purpose of this subcommand is to denote where that will be. By default, study carrels will be saved in your home directory under a subdirectory named reader-library. Trust me. This is a good starting point; run 'rdr set -s local', and accept the default. When you use the build command, the Toolbox will download a file named Tika, save it on your home directory, and update your configurations. You can use this subcommand to denote a location other than your home directory for Tika. The same thing is true for a subsystem called MALLET, which is used by the tm command.
	
	Examples:
	
	\b
	  rdr set -s local
	  rdr set -s mallet
	  rdr set -s tika
	  rdr set -s notebooks
	  rdr set -e
	
	See also: rdr get --help"""
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	
	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE
					
	# erase/restore configurations
	if erase : 
	
		# do the work and report
		initializeConfigurations()
		click.echo( '''
  INFO: Your settings have been restored to their defaults. If
  needed, use the 'rdr get' and 'rdr set' commands to customize
  them.
''', err=True )

	# branch
	if setting :
	
		# re-initialize
		localLibrary  = configuration( 'localLibrary' )
		malletHome    = configuration( 'malletHome' )
		tikaHome      = configuration( 'tikaHome' )
		notebooksHome = configuration( 'notebooksHome' )

		# branch accordingly, local
		if setting == 'local' :
	
			# get the desired library location
			click.echo( 'Where do you want to save your study carrels? Press enter to accept the default.' )
			localLibrary = input( 'Directory [%s]: ' % localLibrary ) or localLibrary
			localLibrary = Path( localLibrary )

			# try to create the directory and save the configuration
			try : localLibrary.mkdir( exist_ok=True )
			except FileNotFoundError : click.echo( "Error: File not found. Are you sure you entered a valid path?", err=True )		

		# mallet
		elif setting == 'mallet' :
	
			# get the desired library location
			click.echo( 'What is the full path to your MALLET distribution?' )
			malletHome = input( 'Directory [%s]: ' % malletHome ) or malletHome

		# notebooks
		elif setting == 'notebooks' :
	
			# get the desired notebook location
			click.echo( 'Where do you want to save the notebooks? Press enter to accept the default.' )
			notebooksHome = input( 'Directory [%s]: ' % notebooksHome ) or notebooksHome
			notebooksHome = Path( notebooksHome )

			# try to create the directory and save the configuration
			try : notebooksHome.mkdir( exist_ok=True )
			except FileNotFoundError : click.echo( "Error: File not found. Are you sure you entered a valid path?", err=True )		

		# tika
		elif setting == 'tika' :
	
			# get the desired library location
			click.echo( 'What is the full path to tika-server.jar?' )
			tikaHome = input( 'File [%s]: ' % tikaHome ) or tikaHome

		# update the configuration file
		configurations[ "RDR" ] = { "localLibrary"  : localLibrary,
		                            "malletHome"    : malletHome ,
		                            "tikaHome"      : tikaHome,
		                            "notebooksHome" : notebooksHome }
		with open( str( configurationFile ), 'w' ) as handle : configurations.write( handle )


# config
@click.command()
@click.argument( 'carrel', metavar='<carrel>' )
def cmdEdit( carrel ) :

	'''Modify the stop word list of <carrel>

When using subcommands such as ngrams or tm, you may observe words of no importance to your analysis. Iteratively use this subcommand to update the stop word list of <carrel> and ultimately remove those words from view. Change the value of your shell's EDITOR environment variable to define what text editor you want to use. Alternatively, you can use your graphical text editor to edit the ./etc/stopwords.txt file found in every study carrel. Just remember, you MUST save the changes as plain text (.txt), not .doc, docx, nor .rtf.

Example: rdr edit homer'''
    
	# sanity check
	checkForCarrel( carrel )

	# initialize and do the work
	file = str( configuration( 'localLibrary' )/carrel/ETC/STOPWORDS )
	click.edit( filename=file )


# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
def cmdInfo( carrel ) :

	"""Output metadata describing <carrel>

	Use this subcommand to output very low-level metadata regarding <carrel>. Metadata includes values for identifiers, a possible title, name and date of publisher and publication, Reader process and input used for carrel creation, various extents, and the most common keywords. This subcommand is useful for garnering the most rudimentary information about <carrel>.

	Example: rdr info homer

	See also: rdr catalog --help"""

	# require
	import sqlite3
	import re
	
	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row

	# get provenance data
	process     = provenance( carrel, 'process' )
	originalID  = provenance( carrel, 'originalID' )
	dateCreated = provenance( carrel, 'dateCreated' )
	timeCreated = provenance( carrel, 'timeCreated' )
	creator     = provenance( carrel, 'creator' )
	input       = provenance( carrel, 'input' )
	
	# parse identifier; extract type, title, and source
	parts = carrel.split( '-' )
	if len( parts ) == 3 :

		type   = parts[ 0 ]
	
		title  = parts[ 1 ]
		if not type == 'classification' :
	
			title  = title.replace( '_', ' ' )
			title  = re.sub( '[A-Z]',    lambda m: ' ' + m.group().lower(), title )
			title  = re.sub( r'\b[a-z]', lambda m: m.group().upper(), title )
			#title  = re.sub( r'[a-z]\d', lambda m: ' ', title )
			title  = re.sub( r'^ +', '', title )
	
		source = parts[ 2 ]
	
	else :

		type   = 'unknown'
		title  = carrel
		source = 'unknown'


	# get extents
	items  = extents( carrel, 'items' )
	words  = extents( carrel, 'words' )
	flesch = extents( carrel, 'flesch' )

 	# get keywords
	keywords = []
	sql      = '''SELECT LOWER( keyword ) AS keyword, COUNT( LOWER( keyword ) ) AS count
	              FROM wrd
	              GROUP BY LOWER( keyword )
	              ORDER BY count DESC, LOWER( keyword ) LIMIT 5;'''
	rows = connection.execute( sql )
	for row in rows :
	
		# parse result and update list
		keyword = row[ 'keyword' ]
		count   = str( row[ 'count' ] )
		keywords.append( '%s (%s)' % ( keyword, count ) )
 	
	# output
	click.echo( "     local identifier: %s" % carrel )
	click.echo( "  original identifier: %s" % originalID )
	click.echo( "                title: %s" % title )
	click.echo( "            publisher: %s, %s" % ( creator, dateCreated) )
	click.echo( "              process: %s (name); %s (input)" % ( process, input ) )
	click.echo( "              extents: %s items; %s words; %s readability" % ( items, words, flesch ) )
	click.echo( "           keyword(s): %s" % "; ".join( keywords ) )


@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-l', '--look', is_flag=True, help='when done, look at the result')
def cmdSummarize( carrel, look ) :

	'''Summarize <carrel>
	
	The use of this command will generate a set of reports and save them in specific locations in <carrel>'s file system. If you specify the -l (look) option, then <carrel>'s index.htm file will be opened in your Web browser. You can subsequently use rdr read <carrel> to open the index.htm file.'''

	# do the work
	summarize( carrel )
	if look : read( carrel )


def hangman() :

	# https://inventwithpython.com/invent4thed/chapter8.html

	import random
	HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''']

	words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()

	def getRandomWord(wordList):
	 # This function returns a random string from the passed list of strings.
	 wordIndex = random.randint(0, len(wordList) - 1)
	 return wordList[wordIndex]

	def displayBoard(missedLetters, correctLetters, secretWord):
	 print(chr(27) + "[2J")
	 print(HANGMAN_PICS[len(missedLetters)])
	 print()

	 print('Missed letters:', end=' ')
	 for letter in missedLetters:
		 print(letter, end=' ')
	 print()

	 blanks = '_' * len(secretWord)

	 for i in range(len(secretWord)): # Replace blanks with correctly guessed letters.
		 if secretWord[i] in correctLetters:
			 blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

	 for letter in blanks: # Show the secret word with spaces in between each letter.
		 print(letter, end=' ')
	 print()

	def getGuess(alreadyGuessed):
	 # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
	 while True:
		 print('Guess a letter.')
		 guess = input()
		 guess = guess.lower()
		 if len(guess) != 1:
			 print('Please enter a single letter.')
		 elif guess in alreadyGuessed:
			 print('You have already guessed that letter. Choose again.')
		 elif guess not in 'abcdefghijklmnopqrstuvwxyz':
			 print('Please enter a LETTER.')
		 else:
			 return guess

	def playAgain():
	 # This function returns True if the player wants to play again; otherwise, it returns False.
	 print('Do you want to play again? (yes or no)')
	 return input().lower().startswith('y')


	print('H A N G M A N')
	missedLetters = ''
	correctLetters = ''
	secretWord = getRandomWord(words)
	gameIsDone = False

	while True:
	 displayBoard(missedLetters, correctLetters, secretWord)

	 # Let the player enter a letter.
	 guess = getGuess(missedLetters + correctLetters)

	 if guess in secretWord:
		 correctLetters = correctLetters + guess

		 # Check if the player has won.
		 foundAllLetters = True
		 for i in range(len(secretWord)):
			 if secretWord[i] not in correctLetters:
				 foundAllLetters = False
				 break
		 if foundAllLetters:
			 print('Yes! The secret word is "' + secretWord +
				   '"! You have won!')
			 gameIsDone = True
	 else:
		 missedLetters = missedLetters + guess

		 # Check if player has guessed too many times and lost.
		 if len(missedLetters) == len(HANGMAN_PICS) - 1:
			 displayBoard(missedLetters, correctLetters, secretWord)
			 print('You have run out of guesses!\nAfter ' +
				   str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
			 gameIsDone = True

	 # Ask the player if they want to play again (but only if the game is done).
	 if gameIsDone:
		 if playAgain():
			 missedLetters = ''
			 correctLetters = ''
			 gameIsDone = False
			 secretWord = getRandomWord(words)
		 else:
			 break


# config
@click.command()
@click.option('-g', '--game', default='hangman', type=click.Choice( [ 'hangman' ] ) )
def cmdPlay( game ) :

	"""Play the word game called hangman"""

	if   game == 'hangman' : hangman()
	else : 
		click.echo( f"Error: Unknown value for GAME: { game }" )
		os.system( 'rdr play --help' )		


# notebooks
@click.command( options_metavar='<options>' )
@click.option('-c', '--command', default='catalog', type=click.Choice( [ 'download', 'catalog', 'launch' ] ), help='command option')
def cmdNotebooks( command ) :

	"""Download, list, and run Toolbox-specific Jupyter Notebooks"""
		
	# configure
	JUPYTER      = 'jupyter notebook'
	PATTERN      = '*.ipynb'
	PROTOCOL     = 'github'
	ORGANIZATION = 'ericleasemorgan'
	REPOSITORY   = 'reader-toolbox'
	REMOTE       = "notebooks"

	# initialize
	notebooksHome = configuration( 'notebooksHome' )
	
	# branch accordingly
	if   command == 'launch'   : _launch( notebooksHome, JUPYTER )
	elif command == 'catalog'  : _catalog( notebooksHome, PATTERN )
	elif command == 'download' : 
	
		click.echo( "  Downloading Toolbox notebooks from GitHub.", err=True )
		_download( notebooksHome, PROTOCOL, ORGANIZATION, REPOSITORY, REMOTE )
		click.echo( "  Done. Now, you want to list them ( -c catalog) or run them (-c launch).", err=True )



@click.command( options_metavar='<options>' )
@click.option('-p', '--process', default='model', type=click.Choice( [ 'model', 'read' ] ), help="type of work to do" )
@click.option('-t', '--topics', default=8, help="number of topics to generate" )
@click.option('-w', '--words', default=8, help="number of words used to describe topic" )
@click.option('-i', '--iterations', default=2400, help="number of times to cacluate" )
@click.option('-o', '--output', default='summary', type=click.Choice( [ 'summary', 'chart', 'topdocs', 'csv' ] ), help="type of report" )
@click.option('-f', '--field', type=click.Choice( [ 'author', 'title', 'date', 'track', 'category', 'type', 'year', 'journal' ] ), help="field for pivoting" )
@click.option('-y', '--type', default='pie', type=click.Choice( [ 'pie', 'bar', 'barh', 'line', 'scatter' ] ), help="type of chart" )
@click.argument( 'carrel', metavar='<carrel>' )
def cmdTm( carrel, process, topics, words, iterations, output, field, type ) :

	"""Apply topic modeling against <carrel>
	
	Topic modeling is the process of enumerating latent themes from a corpus, and it is yet another way to describe a corpus's aboutness. It is suggested you start out small when it comes to the values for -t and -w. Repeat the modeling process and gradually increase the values. Increase the value of -i as the size of your carrel increases. Remember, there is no such thing as the correct value of -t. After all, exactly how many things are the sum of Shakespeare's works about?
	
	Examples:
	
	\b
	  rdr tm homer
	  rdr tm homer -p read
	  rdr tm homer -p read -o chart -y line -f title"""

	# require
	from pathlib import Path
	import matplotlib.pyplot as plot
	import os
	import sys
	import pandas as pd
	from   sklearn.manifold  import TSNE

	# sanity checks
	checkForCarrel( carrel )
	_checkForMallet( str( configuration( 'malletHome' ) ) + '/' + MALLETBIN )

	# initialize
	localLibrary = configuration( 'localLibrary' )
	mallet       = str( configuration( 'malletHome' ) )
	stopwords    = str( localLibrary/carrel/ETC/STOPWORDS )
	corpus       = str( Path( localLibrary/carrel/TXT ) )
	modeldir     = str( localLibrary/carrel/MODELDIR )
	vectors      = str( localLibrary/carrel/MODELDIR/VECTORS )
	keys         = str( localLibrary/carrel/MODELDIR/KEYS )
	documents    = str( localLibrary/carrel/MODELDIR/DOCUMENTS )
	
	# make sane for Windows
	os.environ[ 'MALLET_HOME' ] = mallet
	
	# create a model
	if process == 'model' :
	
		#  make sane
		Path( modeldir ).mkdir( exist_ok=True )

		# create vectors
		command = ( TXT2VEC % ( mallet, corpus, vectors, stopwords ) )	
		os.system( command )
	
		# topic model
		command = ( VEC2MODEL % ( mallet, vectors, topics, words, TOPDOCS, iterations, modeldir, modeldir, modeldir, modeldir, modeldir, modeldir,  modeldir, modeldir ) )
		os.system( command )

		# summarize and output
		keys = _makeSummary( keys, KEYSHEADER )
		click.echo( keys )
			
	# read the model
	else : 
	
		# simple summary
		if output == 'summary' :
			
			# summarize and output
			summary = _makeSummary( keys, KEYSHEADER )
			click.echo( summary )

		# top documents
		if output == 'topdocs' :
	
			# output a summary
			keys = _makeSummary( keys, KEYSHEADER )
			click.echo( keys )
			click.echo()
		
			# create dictionary of labels (map), for future use
			map = keys[ 'labels' ].to_dict()

			# read the documents file
			documents = pd.read_csv( documents, sep=' ', names=DOCUMENTSHEADER, skiprows=1 )

			# map the ids to the documents, and add them to the data frame
			labels = []
			for index, row in documents.iterrows() : labels.append( map[ row[ 'ids' ] ] )
			documents[ 'labels' ] = labels

			# rearrange, just for fun
			documents = documents[ [ 'ids', 'labels', 'files', 'proportions' ] ]

			# process each label (topic) to 
			for id in map :

				# get the label and create a subset of documents
				label = map[ id ]
				files = documents.loc[ documents[ 'labels'] == label ]

				# re-initialize output
				click.echo( label )

				# process each item in the subset; output matching files
				for index, row in files.iterrows() : print( "  *", row[ 'files' ] )

				# delimit
				click.echo()

		# chart
		if output == 'chart' :
		
			# pie chart
			if type == 'pie' :
			
				# output a summary
				summary = _makeSummary( keys, KEYSHEADER )
				click.echo( summary, err=True )

				# visualize
				summary[ 'topics' ] = summary[ 'weights' ].apply( lambda x : x * SCALE )
				summary.plot( kind='pie', y='topics', autopct=PERCENTAGE, labels=summary[ 'labels' ], legend=False ) 
				plot.show()

			# scatter
			if type == 'scatter' :
			
				topics = str( localLibrary/carrel/MODELDIR/TOPICS )
				topics = pd.read_csv( topics, sep='\t' )

				# create generic labels
				labels  = LABELS
				columns = topics.shape[ 1 ]
				for i in range( 0, columns - 2 ) :

					# compute and update list of column names
					i = str( i )
					labels.append( i )
				
				# create more meaningful labels; initialize some more
				keys = pd.read_csv( keys, sep='\t', names=KEYSHEADER )
				keys.sort_values( by='weights', ascending=False, inplace=True )

				# add labels, and drop docId and file
				topics.columns = labels
				topics         = topics.drop( [ 'docId', 'file' ], axis=1 )
				
				# create meaningful labels for each topic
				ids    = []
				labels = []
				for index, row in keys.iterrows() :

					# update the list of ids
					ids.append( index )

					# get and loop through each feature
					features = row[ 'features' ].split()
					for feature in features :

						# build the list, conditionally
						if feature in labels : continue
						labels.append( feature )
						break
				
				# process each id; update with more meaningful labels
				for index, id in enumerate( ids ) :

					column = str( id )
					label  = labels[ index ]
					topics.rename( columns = { column:label }, inplace=True )
				
				# rotate the topics and convert to array
				topics = topics.T
				topics = topics.to_numpy()
				
				# specify type of TSNE modeling, and then model
				tsne   = TSNE( perplexity=1024, init='pca', learning_rate='auto' )
				model  = tsne.fit_transform( topics )
				
				# plot
				x = model[ :, 0 ]
				y = model[ :, 1 ]
				plot.scatter( x, y )
				for i, label in enumerate( labels ) : plot.annotate( label, ( x[ i ], y[ i ] ) )
				plot.show()
				
			if type == 'line' or type == 'bar' or type == 'barh' :
			
				# sanity check
				if not field :
					click.echo( "Error: When using chart of types 'barh', 'bar', or 'line' you must specify a field (-f). See 'rdr tm --help' for more detail.", err=True )
					exit()
				
				# output a summary
				summary = _makeSummary( keys, KEYSHEADER )
				click.echo( summary, err=True )

				# _pivot the model on the given field
				topics = _pivot( localLibrary, carrel, field, keys )
				
				# configure plot and show
				click.echo( topics, err=True )
				topics.plot( kind=type )
				plot.show()

		# csv
		if output == 'csv' :
		
			# sanity check
			if not field :
				click.echo( "Error: When specifying CSV output you must specify a field (-f). See 'rdr tm --help' for more detail.", err=True )
				exit()
			
			# summarize and output
			summary = _makeSummary( keys, KEYSHEADER )
			click.echo( summary, err=True )

			# _pivot the model on the given field
			topics = _pivot( localLibrary, carrel, field, keys )
			
			# configure plot and show
			click.echo( topics.to_csv() )

# config
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'directory', metavar='<directory>' )
@click.option('-e', '--erase', is_flag=True, help='delete pre-existing carrel')
@click.option('-s', '--start', is_flag=True, help='start Tika')
def cmdBuild( carrel, directory, erase, start ) :

	"""Create <carrel> from files in <directory>

Use this command to build a data set ("study carrel") based on the files saved in a directory. Once the data set is created the other Toolbox commands can be applied to the result. The files can be of any type (PDF, Microsoft Word, HTML, etc.), and they can be of any kind (books, articles, reports, etc.), and they can be of any number (1, 2, 12, a few dozen, hundreds, etc.). The Toolbox is designed to read about a dozen journal articles in the form of PDF files. This command requires a Java tool called Tika, and it is used to convert the input files into plain text as well as extract authors, titles, and dates. If the Toolbox has not been configured and/or Tika is not installed, then the Toolbox will try to install it on your behalf. If the given directory contains a file named 'metadata.csv', then this command will use the file as the source of author, title, and date metadata values. This is often very helpful because sans metadata it is very difficult to make comparison between documents. Please see the full-blown documentation for details."""

	build( carrel, directory, erase, start )

@click.command()
def cmdServer() :

	'''Experimental Web interface to your Distant Reader study carrels'''
	
	# configure; code for rdr
	PORT = 18418
	
	# require
	from .server import server
	import os

	# configure and go
	os.environ[ 'FLASK_ENV' ] = 'development'
	server.run( port=PORT, debug=True )
	
# create a list of commands
rdr.add_command( cmdAbout,         name='about' )
rdr.add_command( cmdAdr,           name='adr' )
rdr.add_command( cmdBib,           name='bib' )
rdr.add_command( cmdBrowse,        name='browse' )
rdr.add_command( cmdBuild,         name='build' )
rdr.add_command( cmdCatalog,       name='catalog' )
rdr.add_command( cmdCluster,       name='cluster' )
rdr.add_command( cmdCollocations,  name='collocations' )
rdr.add_command( cmdConcordance,   name='concordance' )
rdr.add_command( cmdDocumentation, name='documentation' )
rdr.add_command( cmdDownload,      name='download' )
rdr.add_command( cmdEdit,          name='edit' )
rdr.add_command( cmdEnt,           name='ent' )
rdr.add_command( cmdGet,           name='get' )
rdr.add_command( cmdGrammars,      name='grammars' )
rdr.add_command( cmdInfo,          name='info' )
rdr.add_command( cmdNgrams,        name='ngrams' )
rdr.add_command( cmdNotebooks,     name='notebooks' )
rdr.add_command( cmdPlay,          name='play' )
rdr.add_command( cmdPos,           name='pos' )
rdr.add_command( cmdRead,          name='read' )
rdr.add_command( cmdReadability,   name='readability' )
rdr.add_command( cmdSearch,        name='search' )
rdr.add_command( cmdSemantics,     name='semantics' )
rdr.add_command( cmdServer,        name='web' )
rdr.add_command( cmdSet,           name='set' )
rdr.add_command( cmdSizes,         name='sizes' )
rdr.add_command( cmdSql,           name='sql' )
rdr.add_command( cmdSummarize,     name='summarize' )
rdr.add_command( cmdTm,            name='tm' )
rdr.add_command( cmdUrl,           name='url' )
rdr.add_command( cmdWrd,           name='wrd' )

# do the work
if __name__ == '__main__' : rdr()
