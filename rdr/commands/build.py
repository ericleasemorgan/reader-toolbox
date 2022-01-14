
# build; create a study carrel

# require
from rdr import *

# configure
VERBOSE = 3

# create carrel skeleton
def initialize( carrel, directory ) :
	
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
	Path.mkdir( localLibrary,              exist_ok=True )
	Path.mkdir( localLibrary/carrel,       exist_ok=True )
	Path.mkdir( localLibrary/carrel/ADR,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/BIB,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/CACHE, exist_ok=True )
	Path.mkdir( localLibrary/carrel/ENT,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/ETC,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/POS,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/TXT,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/URLS,  exist_ok=True )
	Path.mkdir( localLibrary/carrel/WRD,   exist_ok=True )

	# configure provenance and output it
	process     = PROCESS
	originalID  = carrel
	dateCreated = datetime.today().strftime( '%Y-%m-%d' )
	timeCreated = datetime.now().strftime("%H:%M")
	creator     = getuser()
	input       = directory
	record      = [ PROCESS, originalID, dateCreated, timeCreated, creator, input ]
	output      = localLibrary/carrel/PROVENANCE
	with open( output, 'w' ) as handle : handle.write( '\t'.join( record ) + '\n' )
	
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
	with open( output, 'w' ) as handle : handle.write( WORDS )


# create key from filename
def name2key( file ) :

	# require, do the work, and done; inefficient
	import os
	key = os.path.splitext( os.path.basename( file ) )[ 0 ]
	return key


# normalize text, a poor man's version
def normalize( text ) :

	# require
	import re
	
	# normalize the text in the bag-of-words
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

# create bag of words
def txt2bow( carrel ) :

	# configure
	PATTERN = '*.txt'
	BOW     = 'reader.txt'
	TXT     = 'txt'
	ETC     = 'etc'
	
	# require
	from pathlib import Path

	# initialize
	localLibrary = configuration( 'localLibrary' )

	# process each text file in the given directory
	txt = localLibrary/carrel/TXT
	bow = ''
	for file in txt.glob( PATTERN ) :
	
		# create/increment the bag of words
		with open( file ) as handle : bow += handle.read()
	
	# normalize
	bow = normalize( bow )
	
	# configure output, output, and done
	output = localLibrary/carrel/ETC/BOW
	with open( output, 'w' ) as handle : handle.write( bow )


# extract email addresses
def txt2adr( carrel, file ) :
	
	# configure
	ADR       = 'adr'
	EXTENSION = '.adr'
	HEADER    = [ 'id', 'address' ]
	PATTERN   = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

	# require
	import re
	
	# initialize
	key          = name2key( file )
	localLibrary = configuration( 'localLibrary' )

	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file ) as handle : text = normalize( handle.read() )
	
	# get and process each address, to the best of my ability
	addresses = re.findall( PATTERN, text )

	# check for addresses
	if len( addresses ) > 0 :

		# open output
		output = localLibrary/carrel/ADR/( key + EXTENSION )
		with open( output, 'w' ) as handle :

			# initialize the output
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
def txt2ent( carrel, file ) :

	# configure
	EXTENSION = '.ent'
	ENT       = 'ent'
	HEADER    = [ 'id', 'sid', 'eid', 'entity', 'type' ]

	# require
	import spacy

	# initialize
	key          = name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file ) as handle : text = normalize( handle.read() )

	# model the text
	nlp            = spacy.load( MODEL )
	nlp.max_length = ( len( text ) + 1 )
	doc            = nlp( text )

	# open output
	output = localLibrary/carrel/ENT/( key + EXTENSION )
	with open( output, 'w' ) as handle :

		# initialize the output
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
def txt2pos( carrel, file ) :

	# configure
	EXTENSION = '.pos'
	POS       = 'pos'
	HEADER    = [ 'id', 'sid', 'tid', 'token', 'lemma', 'pos' ]

	# require
	import spacy

	# initialize
	key          = name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file ) as handle : text = normalize( handle.read() )

	# model the text
	nlp            = spacy.load( MODEL )
	nlp.max_length = ( len( text ) + 1 )
	doc            = nlp( text )

	# open output
	output = localLibrary/carrel/POS/( key + EXTENSION )
	with open( output, 'w' ) as handle :

		# initialize the output
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
def txt2url( carrel, file ) :

	# configure
	EXTENSION = '.url'
	URLS      = 'urls'
	HEADER    = [ 'id', 'domain', 'url']
	PATTERN   = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

	# require
	import re
	
	# initialize
	key          = name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file ) as handle : text = normalize( handle.read() )

	# get and process each url, to the best of my ability
	urls = re.findall( PATTERN, text )
	
	# check for addresses
	if len( urls ) > 0 :

		# open output
		output = localLibrary/carrel/URLS/( key + EXTENSION )
		with open( output, 'w' ) as handle :

			# initialize the output
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
def txt2wrd( carrel, file ) :

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
	
	# initialize
	key          = name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file ) as handle : text = normalize( handle.read() )

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
		with open( output, 'w' ) as handle :

			# initialize the output
			handle.write( '\t'.join( HEADER ) + '\n' )

			# process each record
			for record in records :

				# do the simplest of normalization and output
				keyword = record[ 0 ]
				if len( keyword ) < 3 : continue
				handle.write( '\t'.join( ( key, keyword ) ) + '\n' )

# given a spaCy doc which has been enhanced by pytextrank, return a summary
def summarize( doc ) :

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
	unit_vector = [ rank/sum_ranks for rank in unit_vector ]
	rankings    = {}
	sent_id     = 0

	for start, end, vector in boundries:

		# re-initialize
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

	# normalize
	summary = ' '.join( summary )
	summary = summary.replace( '"', '' )
	summary = re.sub( '\n+', ' ', summary )
	summary = re.sub( ' +', ' ',  summary )
	summary = re.sub( '^\s', '',  summary )
	summary = re.sub( '\s$', '',  summary )

	# done
	return summary


# given a file, create some bibliographics and save plain text
def file2bib( carrel, file, metadata=None ) :
		
	# configure
	BIB          = 'bib'
	TXT          = 'txt'
	CACHE        = 'cache'
	COUNT        = 24
	EXTENSION    = '.txt'
	BIBEXTENSION = '.bib'
	HEADER       = [ 'id', 'author', 'title', 'date', 'pages', 'extension', 'mime', 'words', 'sentence', 'flesch', 'summary', 'cache', 'txt' ]
	PROCESS       = 'textrank'

	# require
	from   pathlib              import Path
	from   textacy              import text_stats
	from   tika                 import detector
	from   tika                 import parser
	import os
	import spacy
	import pytextrank

	# initialize
	author       = ''
	title        = name2key( file )
	date         = ''
	extension    = os.path.splitext( os.path.basename( file ) )[ 1 ]
	key          = name2key( file )
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
		if 'author' in metadata : author = metadata.loc[ index ][ 'author' ]
		if 'title'  in metadata : title  = metadata.loc[ index ][ 'title' ]
		if 'date'   in metadata : date   = str( metadata.loc[ index ][ 'date' ] )
		
	# get metadata from the source file
	metadata = parsed[ 'metadata' ] 
	mimetype = detector.from_file( file )

	# author
	if author != '' : 
	
		if 'creator' in metadata :
			author = metadata[ 'creator' ]
			if ( isinstance( author, list ) ) : author = author[ 0 ]

	# title
	if title != '' : 
	
		if 'title' in metadata :
			title = metadata[ 'title' ]
			if ( isinstance( title, list ) ) : title = title[ 0 ]
			title = ' '.join( title.split() )

	# date
	if date != '' : 
	
		if 'date' in metadata :
			date = metadata[ 'date' ]
			if ( isinstance( date, list ) ) : date = date[ 0 ]
			date = date[:date.find( 'T' )]

	# number of pages
	if 'xmpTPg:NPages' in metadata :
		pages = metadata[ 'xmpTPg:NPages' ]
		if ( isinstance( pages, list ) ) : pages = pages[ 0 ]
		
	# model the text
	nlp            = spacy.load( MODEL )
	nlp.max_length = ( len( text ) + 1 )
	nlp.add_pipe( PROCESS )
	doc            = nlp( text )

	# summarize
	summary = summarize( doc )
	
	# parse out only the desired statistics
	words      = text_stats.n_words( doc )
	sentences  = text_stats.n_sents( doc )
	syllables  = text_stats.n_syllables( doc )
	flesch     = int( text_stats.readability.flesch_reading_ease( doc ) )

	# cache and text locations
	txt   = Path( TXT )/( key + EXTENSION )
	cache = Path( CACHE )/( key + extension )

	# debug
	if VERBOSE == 2 :
	
		# provide a review
		click.echo( '        key: ' + key,              err=True )
		click.echo( '     author: ' + author,           err=True )
		click.echo( '      title: ' + title,            err=True )
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
	with open( output, 'w' ) as handle :
	
		# output the header and the data
		handle.write( '\t'.join( HEADER ) + '\n' )
		handle.write( '\t'.join( [ key, str( author ), title, str( date ), pages, extension, mimetype, str( words ), str( sentences ), str( flesch ), summary, str( cache ), str( txt ) ] ) + '\n' )

	# check for text, and it should exist; famous last words
	if text : 

		# configure output and output
		output = localLibrary/carrel/TXT/( key + EXTENSION )
		with open( output, 'w' ) as handle : handle.write( text )


# given a few configurations, reduce extracted features to a database
def tsv2db( directory, extension, table, connection ) :

	# require
	import pandas as pd
	
	# debug
	if VERBOSE : click.echo( '\tProcessing ' + table, err=True )
	
	# process each file in the given directory
	for index, file in enumerate( directory.glob( extension ) ) :

		# more debugging
		if VERBOSE == 2 : click.echo( '\t' + str( file ), err=True )
		
		# read the file
		df = pd.read_csv( file, sep='\t', header=0, low_memory=False, on_bad_lines='warn', quoting=3 )

		# initialize the features or append to it
		if index == 0 : features = df
		else          : features = pd.concat( [ features, df ], sort=False )

		# do the work; fill the database
		features.to_sql( table, connection, if_exists='replace', index=False )


# config
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'directory', metavar='<directory>' )
@click.option('-e', '--erase', is_flag=True, help='delete pre-existing carrel')
def build( carrel, directory, erase ) :

	"""Make <carrel> with files in <directory>"""

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
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	pool         = Pool()

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
			click.echo( ( 'Carrel exists. Specify a name other than "%s" or add -e to erase it.' % carrel ), err=True )
			exit()

	# build skeleton
	click.echo( '(Step #1 of 9) Initializing %s with %s and stop words' % ( carrel, directory ), err=True )
	initialize( carrel, directory )
		
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

		pool.starmap( file2bib, [ [ carrel, filename, metadata ] for filename in filenames ] )
		
	# no metadata file; just do the work
	else : pool.starmap( file2bib, [ [ carrel, filename ] for filename in filenames ] )
		
	# bag of words
	click.echo( '(Step #3 of 9) Creating bag-of-words', err=True )
	txt2bow( carrel )
	
	# output hint
	click.echo( ( "\n  Hint: Now that the bag-of-words has been created, you can begin\n  to use many of the other Reader Toolbox commands while the\n  building process continues. This is especially true for larger\n  carrels. Open a new terminal window and try:\n\n    rdr cluster %s\n    rdr ngrams %s -c | more\n    rdr concordance %s\n    rdr collocations %s\n" % ( carrel, carrel, carrel, carrel ) ), err=True )
	
	# re-create a list of filenames to process
	filenames = []
	txt       = localLibrary/carrel/TXT
	for filename in os.listdir( txt ) : filenames.append( os.path.join( txt, filename ) )

	
	# extract email addresses
	click.echo( '(Step #4 of 9) Extracting (email) addresses', err=True )
	pool.starmap( txt2adr, [ [ carrel, filename ] for filename in filenames ] )
	
	# extract named entities
	click.echo( '(Step #5 of 9) Extracting (named) entities', err=True )
	pool.starmap( txt2ent, [ [ carrel, filename ] for filename in filenames ] )
	
	# extract parts-of-speech
	click.echo( '(Step #6 of 9) Extracting parts-of-speech', err=True )
	pool.starmap( txt2pos, [ [ carrel, filename ] for filename in filenames ] )

	# extract urls
	click.echo( '(Step #7 of 9) Extracting URLs', err=True )
	pool.starmap( txt2url, [ [ carrel, filename ] for filename in filenames ] )

	# extract keywords
	click.echo( '(Step #8 of 9) Extracting (key) words', err=True )
	pool.starmap( txt2wrd, [ [ carrel, filename ] for filename in filenames ] )

	# clean up
	pool.close()

	# create database
	click.echo( '(Step #9 of 9) Creating and filling database (reducing)', err=True )
	database   = str( localLibrary/carrel/ETC/DATABASE )
	connection = sqlite3.connect( database )
	cursor     = connection.cursor()
	cursor.executescript( SCHEMA )
	
	# reduce; fill it with content
	tsv2db( localLibrary/carrel/POS, '*.pos', 'pos', connection )
	tsv2db( localLibrary/carrel/ENT, '*.ent', 'ent', connection )
	tsv2db( localLibrary/carrel/WRD, '*.wrd', 'wrd', connection )
	tsv2db( localLibrary/carrel/ADR, '*.adr', 'adr', connection )
	tsv2db( localLibrary/carrel/URL, '*.url', 'url', connection )
	tsv2db( localLibrary/carrel/BIB, '*.bib', 'bib', connection )

	# output another hint
	# out hint
	click.echo( ( '\n  Another hint: The build process is done, and now you ought to\n  be able to use any Toolbox command. For example:\n\n    rdr info %s\n    rdr bib %s | more\n    rdr tm %s\n' % ( carrel, carrel, carrel ) ), err=True )

