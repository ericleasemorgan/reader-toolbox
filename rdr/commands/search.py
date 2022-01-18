
# search - given query, do a full text search against the content of a carrel

# require
from rdr import *

# make sure the carrel has been indexed; sqlite++
def checkForIndex( carrel ) :

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
		click.echo( 'Indexing; the carrel must be set up for full text searching.', err=True )
		click.echo( 'Step #1 of 4: Creating table to contain full text...', err=True )
		connection.execute( DROPFULLTEXT )
		connection.execute( CREATEFULLTEXT )

		# read full text
		click.echo( 'Step #2 of 4: Reading full text; please be patient...', err=True )
		with open( transaction, 'w' ) as handle : handle.write( 'BEGIN TRANSACTION;\n' )
		files = txt.glob( '*.txt' )
		for file in files :

			# get identifier
			id = file.stem
			id = id.replace( "'", "''" )
	
			# get full text
			with open( file ) as handle : fulltext = handle.read()
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
		click.echo( 'Step #3 of 4: Writing full text to database...', err=True )
		with open( transaction ) as handle :

			# repeat forever, almost
			while True :
				sql = handle.readline()
				if not sql : break
				connection.execute( sql )


		# clean up
		os.remove( transaction )
		
		# index; do the actual work
		click.echo( 'Step #4 of 4: Indexing; please be patient...', err=True )
		connection.execute( DROPINDX )
		connection.execute( CREATEINDX )
		connection.execute( INDEX )

		# done
		click.echo( 'Done. Happy searching!', err=True )


@click.command( options_metavar='<options>' )
@click.option('-o', '--output', default='human', type=click.Choice( [ 'human', 'csv', 'tsv', 'json', 'count' ] ), help='the format of the results')
@click.option('-q', '--query', default='love', help='a full text query')
@click.argument( 'carrel', metavar='<carrel>' )
def search( query, output, carrel ) :

	'''Perform a full text query against <carrel>.
	
	Given words, phrases, fields, and Boolean operators, use this subcommand to find and describe specific items in <carrel>. The query language is quite extensive, but in general, enter words and/or phrases, and a list of matching documents ought to be returned. For more detail, please see: https://reader-toolbox.rtfd.io/en/latest/commands.html#search
	
	Examples:
	
	\b
	  rdr search -q 'truth beauty war love' homer
	  rdr search -q 'title:iliad AND summary:war' homer
	  rdr search -q '"keep his anger"' homer'''

	# configure
	SQL = "SELECT id, author, title, date, summary, keyword, words, sentence, flesch, '##CACHE##' || cache AS cache, '##TXT##' || txt AS txt FROM indx WHERE indx MATCH '##QUERY##' ORDER BY RANK;"

	# configure
	RESULTS = '\nYour search (##QUERY##) against the study carrel named "##CARREL##" returned ##COUNT## record(s):\n\n##RECORDS##'
	RECORD  = '          id: ##ID##\n      author: ##AUTHOR##\n       title: ##TITLE##\n        date: ##DATE##\n     summary: ##SUMMARY##\n  keyword(s): ##KEYWORD##\n       words: ##WORDS##\n    sentence: ##SENTENCE##\n      flesch: ##FLESCH##\n       cache: ##CACHE##\n         txt: ##TXT##\n\n'
	COUNT   = '##CARREL##\t##QUERY##\t##COUNT##'

	# require
	import sqlite3
	import pandas as pd
	
	# sanity checks
	checkForCarrel( carrel )
	checkForIndex( carrel )
	
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
	if output   == 'csv' : click.echo( rows.to_csv() )
	
	# tsv
	elif output == 'tsv' : click.echo( rows.to_csv( header=False, sep='\t' ) )
	
	# json
	elif output == 'json' : click.echo( rows.to_json( orient='records' ) )
	
	# count; tsv stream of metadata
	elif output == 'count' :
	
		# build
		results = COUNT.replace( '##CARREL##', carrel )
		results = results.replace( '##QUERY##', query )
		results = results.replace( '##COUNT##', str( rows.shape[ 0 ] ) )
		
		# output
		click.echo( results )
	
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
			record = RECORD.replace( '##ID##', id )
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
		click.echo_via_pager( results )
		
		
	