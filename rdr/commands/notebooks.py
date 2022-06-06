
# notebooks - download and run Toolbox-specific Jupyter Notebooks

# require
from rdr import *
import pathlib
import os
import sys
import json
import fsspec

# define; launch
def launch( directory, jupyter ) :

	# initialize
	directory = pathlib.Path( directory )

	# make sane, launch jupyter, and done
	os.chdir( directory )
	os.system( jupyter )


# define; catalog
def catalog( directory, pattern ) :

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
def download( directory, protocol, organization, repository, remote ) :

	# initialize
	destination = pathlib.Path( directory )
	destination.mkdir( exist_ok=True, parents=True )
	filesystem  = fsspec.filesystem( protocol, org=organization, repo=repository )

	# do the work and done
	filesystem.get( filesystem.ls( remote ), destination.as_posix() )


# notebooks
@click.command( options_metavar='<options>' )
@click.option('-c', '--command', default='catalog', type=click.Choice( [ 'download', 'catalog', 'launch' ] ), help='command option')
def notebooks( command ) :

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
	if   command == 'launch'   : launch( notebooksHome, JUPYTER )
	elif command == 'catalog'  : catalog( notebooksHome, PATTERN )
	elif command == 'download' : 
	
		click.echo( "  Downloading Toolbox notebooks from GitHub.", err=True )
		download( notebooksHome, PROTOCOL, ORGANIZATION, REPOSITORY, REMOTE )
		click.echo( "  Done. Now, you want to list them ( -c catalog) or run them (-c launch).", err=True )


