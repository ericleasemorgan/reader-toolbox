#!/usr/bin/env python

# server.py - an HTTP front-end to the Reader Toolbox

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 14, 2022 - first cut; "Thanks Don!"
# July 15, 2022 - adding many routes


# configure
CARREL = 'homer'

# require
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import abort
import os
import rdr

# initialize
server = Flask( __name__ )


# home page
@server.route( '/' )
def home() : return render_template( 'index.htm', error=None )


# catalog
@server.route( '/catalog' )
def catalog() :

	# do the work and return it
	result = rdr.catalog()
	return( '<pre>%s</pre>' % result )


# concordance
@server.route( '/concordance' )
def concordance() :

	# configure
	carrel = CARREL
	query  = 'love'
	width  = 80
	
	# get input
	carrel = request.args.get( 'carrel', carrel )
	query  = request.args.get( 'query', query )
	width  = request.args.get( 'width', width )

	# do the work and return it
	result = rdr.concordance( carrel, query=query, width=int( width ) )
	return render_template( 'concordance.htm', result=result, carrel=carrel, query=query )


# ngrams
@server.route( '/ngrams' )
def ngrams() :

	# configure
	carrel = CARREL
	count  = True
	size   = 1
	query  = None

	# get input
	carrel = request.args.get( 'carrel', carrel )
	count  = request.args.get( 'count', count )
	size   = request.args.get( 'size', size )
	query  = request.args.get( 'query', query )

	# do the work and return it
	result = rdr.ngrams( carrel, count=count, size=int( size ), query=query )
	return render_template( 'ngrams.htm', result=result, carrel=carrel, size=size, count=count, query=query )


@server.route('/<path:carrel>')
def browse( carrel ) :

	localLibrary = str( rdr.configuration( 'localLibrary' ) )

	# Joining the base and the requested path
	path = os.path.join( localLibrary, carrel )

	# Return 404 if path doesn't exist
	if not os.path.exists( path ) : return abort( 404 )

	# Check if path is a file and serve
	if os.path.isfile( path ) : return send_file( path )

	# Show directory contents
	files = os.listdir( path )
	files.sort()
	return render_template( 'files.htm', files=files )


# full text search
@server.route( '/search' )
def search() :

	# configure
	carrel = CARREL
	query  = 'love'
	output = 'human'

	# get input
	carrel = request.args.get( 'carrel', carrel )
	query  = request.args.get( 'query', query )
	output = request.args.get( 'output', output )

	# do the work and return it
	result = rdr.search( carrel, query=query, output=output )
	return render_template( 'search.htm', result=result, carrel=carrel, query=query )


# info
@server.route( '/info' )
def info() :

	# configure
	carrel = CARREL

	# get input
	carrel = request.args.get( 'carrel', carrel )

	# do the work
	process     = rdr.provenance( carrel, 'process' )
	originalID  = rdr.provenance( carrel, 'originalID' )
	dateCreated = rdr.provenance( carrel, 'dateCreated' )
	timeCreated = rdr.provenance( carrel, 'timeCreated' )
	creator     = rdr.provenance( carrel, 'creator' )
	input       = rdr.provenance( carrel, 'input' )
	items       = rdr.extents( carrel, 'items' )
	words       = rdr.extents( carrel, 'words' )
	flesch      = rdr.extents( carrel, 'flesch' )
	
	# return it
	return render_template( 'info.htm', carrel=carrel, process=process, originalID=originalID, dateCreated=dateCreated, timeCreated=timeCreated, creator=creator, input=input, items=items, words=words, flesch=flesch )


# keywords
@server.route( '/wrd' )
def wrd() :

	# configure
	carrel    = CARREL
	output    = 'count'
	
	# get input
	carrel = request.args.get( 'carrel', carrel )
	output = request.args.get( 'output', output )

	# do the work and return it
	results = rdr.keywords( carrel, count=True  )
				
	if output == 'count' : return render_template( 'keywords.htm', carrel=carrel, results=results )
	else :
			
		results = results.split( '\n' )

		# coerce the result into a dictionary of frequencies
		frequencies = {}
		for result in results :

			keyword = result.split( '\t' )[ 0 ]
			count   = int( result.split( '\t' )[ 1 ] )
			frequencies[ keyword ] = count
						
		rdr.cloud( frequencies, file='/Users/eric/Desktop/image.jpeg' )
		exit() 


