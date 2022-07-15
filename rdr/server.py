#!/usr/bin/env python

# reader-server.py - an HTTP front-end to the Reader Toolbox

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 14, 2022 - first cut; "Thanks Don!"

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
	return( '<pre>%s</pre>' % result )

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
	return( '<pre>%s</pre>' % result )


@server.route('/<path:carrel>')
def browse( carrel ) :

	localLibrary = str( rdr.configuration( 'localLibrary' ) )

	# Joining the base and the requested path
	abs_path = os.path.join( localLibrary, carrel )

	# Return 404 if path doesn't exist
	if not os.path.exists( abs_path ) : return abort( 404 )

	# Check if path is a file and serve
	if os.path.isfile( abs_path ) : return send_file( abs_path )

	# Show directory contents
	files = os.listdir( abs_path )
	files.sort()
	return render_template( 'files.htm', files=files )
