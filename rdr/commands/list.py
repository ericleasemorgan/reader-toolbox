
# list - given a location, output a list of study carrels

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.option('-h', '--human', is_flag=True, help='output in a more human-readable form')
@click.argument( 'location', metavar='<location>' )
def list( human, location ) :

	"""List the items in a library where <location> is either 'local' or 'remote'
	
	Use this function to learn what items are saved in your local library of study carrels or what items are available in the library of about 3,000 pre-created study carrels at http://library.distantreader.org/. The local option returns a simple list. The remote option returns a tab-delimited list along with some metadata describing each item. In either case, you might want to pipe the results to utilities such as sort, grep, cut, or less in order to make the most of the result.
	
	Examples:
	
	\b
	  * rdr list local
	  * rdr list remote | less -S
	  * rdr list -h remote
	  * rdr list remote | grep love | less -S -x32
	  * rdr list remote | grep love | cut -f1 | less
	  
	See also: rdr download"""
	
	# configure
	TSV = 'catalog/catalog.tsv'

	# require
	from requests  import get
	import pathlib
		
	# branch accordingly; local
	if location == 'local' :
		
		# initialize
		localLibrary = configuration( 'localLibrary' )
		
		# read, sort, and output
		carrels = [ carrel.name for carrel in localLibrary.iterdir() if carrel.is_dir() ]
		carrels.sort()
		for carrel in carrels : click.echo( carrel )
	
	# remote; get, and output
	elif location == 'remote' :
	
		# create person-amenable output
		if human :
		
			# get the raw data and process each record 
			records = get( REMOTELIBRARY + '/' + TSV ).text 
			for record in records.split( '\n' ) :
			
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
			
				# output; should probably use pager
				click.echo( f'      name: {name}' )
				click.echo( f'      date: {date}' )
				click.echo( f'  keywords: {keywords}' )
				click.echo( f'     items: {items}' )
				click.echo( f'     words: {words}' )
				click.echo( f'     score: {score}' )
				click.echo( f'     bytes: {bytes}' )
				click.echo( )
	
		# get the raw data and hope the results get piped to utilities like sort, grep, cut, less, etc.
		else : click.echo( get( remoteLibrary + TSV ).text )

