
# build; create a study carrel

# require
from rdr import *

# configure
VERBOSE = 0

# create carrel skeleton
def initialize( carrel, cache ) :
	
	# configure
	ADR       = 'adr'
	BIB       = 'bib'
	CACHE     = 'cache'
	ENT       = 'ent'
	ETC       = 'etc'
	POS       = 'pos'
	TXT       = 'txt'
	URLS      = 'urls'
	WRD       = 'wrd'

	# require
	from   pathlib import Path
	import shutil
	import os

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

	# process each item in the cache
	cache = Path( cache )
	for source in cache.glob( '*' ) :

		# copy the file
		destination = localLibrary/carrel/CACHE/(os.path.basename( source ) )
		shutil.copyfile( source, destination )

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
	text = re.sub( ' +', ' ',  text )
	
	# done
	return text


# given a file, extract and save plain text
def file2txt( carrel, file ) :

	# configure
	EXTENSION = '.txt'
	TXT       = 'txt'
	
	# require
	from tika import parser

	# initialize
	key          = name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )
	
	# pass the file on to tika and parse the content; again, assume Tika server is running
	parsed  = parser.from_file( file )
	content = parsed[ 'content' ]
	
	# check for content
	if content : 

		# configure output and output
		output = localLibrary/carrel/TXT/( key + EXTENSION )
		with open( output, 'w' ) as handle : handle.write( content )


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
	nlp = spacy.load( MODEL, max_length=( len( text ) + 1 ) )
	doc = nlp( text )

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
	nlp = spacy.load( MODEL, max_length=( len( text ) + 1 ) )
	doc = nlp( text )

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
					word  = str( token.text )
					lemma = str( token.lemma_.lower() )
					pos   = token.pos_
					handle.write( '\t'.join( [  key, str( s + 1 ), str( t + 1 ), word, lemma, pos ] ) + '\n' )


# given a file, domains and urls
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

	# open output
	output = localLibrary/carrel/URLS/( key + EXTENSION )
	with open( output, 'w' ) as handle :

		# initialize the output
		handle.write( '\t'.join( HEADER ) + '\n' )

		# get and process each url, to the best of my ability
		urls = re.findall( PATTERN, text )
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
	EXTENSION = '.wrd'
	WRD       = 'wrd'
	NGRAMS    = 1
	TOPN      = 0.005
	HEADER    = [ 'id', 'keyword' ]

	# require
	from  textacy.ke import yake
	import spacy
	import os
	
	# initialize
	key          = name2key( file )
	localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file ) as handle : text = normalize( handle.read() )

	# model the text
	nlp = spacy.load( MODEL, max_length=( os.path.getsize( file ) + 1 ) )
	doc = nlp( text )

	# open output
	output = localLibrary/carrel/WRD/( key + EXTENSION )
	with open( output, 'w' ) as handle :
	
		# initialize the output
		handle.write( '\t'.join( HEADER ) + '\n' )
		
		# do the extraction
		for keyword, score in ( yake( doc, ngrams=NGRAMS, topn=TOPN, normalize='lemma' ) ) :

			# do the simplest of normalization and output
			if len( keyword ) < 3 : continue
			keyword = keyword.lower()
			handle.write( '\t'.join( ( key, keyword ) ) + '\n' )


# config
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'cache', metavar='<cache>' )
def build( carrel, cache ) :

	"""Make <carrel>"""

	# configure
	CACHE = 'cache'
	TXT   = 'txt'

	# require
	from multiprocessing import Pool
	import os
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	pool         = Pool()

	# build skeleton
	click.echo( '(Step #1 of 8) Initializing %s with %s' % ( carrel, cache ), err=True )
	initialize( carrel, cache )
	
	# create a list of filenames to process
	filenames = []
	cache     = localLibrary/carrel/CACHE
	for filename in os.listdir( cache ) : filenames.append( os.path.join( cache, filename ) )

	# extract plain text
	click.echo( '(Step #2 of 8) Converting cached documents to plain text', err=True )
	pool.starmap( file2txt, [ [ carrel, filename ] for filename in filenames ] )
	
	# bag of words
	click.echo( '(Step #3 of 8) Creating bag-of-words', err=True )
	txt2bow( carrel )
	
	# re-create a list of filenames to process
	filenames = []
	txt       = localLibrary/carrel/TXT
	for filename in os.listdir( txt ) : filenames.append( os.path.join( txt, filename ) )

	# extract email addresses
	click.echo( '(Step #4 of 8) Extracting (email) addresses', err=True )
	pool.starmap( txt2adr, [ [ carrel, filename ] for filename in filenames ] )
	
	# extract named entities
	click.echo( '(Step #5 of 8) Extracting (named) entities', err=True )
	pool.starmap( txt2ent, [ [ carrel, filename ] for filename in filenames ] )
	
	# extract parts-of-speech
	click.echo( '(Step #6 of 8) Extracting parts-of-speech', err=True )
	pool.starmap( txt2pos, [ [ carrel, filename ] for filename in filenames ] )

	# extract urls
	click.echo( '(Step #7 of 8) Extracting URLs', err=True )
	pool.starmap( txt2url, [ [ carrel, filename ] for filename in filenames ] )

	# extract keywords
	click.echo( '(Step #8 of 8) Extracting (key) words', err=True )
	pool.starmap( txt2wrd, [ [ carrel, filename ] for filename in filenames ] )

	# clean up
	pool.close()

	
	