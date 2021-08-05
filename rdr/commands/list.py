
# list - given a location, output a list of study carrels

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.argument( 'location', metavar='<location>' )
def list( location ) :

	"""List the items in a library where <location> is either 'local' or 'remote'
	
	Use this function to learn what items are saved in your local library of study carrels or what items are available in the library of about 3,000 pre-created study carrels at http://library.distantreader.org/. The local option returns a simple list. The remote option returns a tab-delimited list along with some metadata describing each item. In either case, you might want to pipe the results to utilities such as sort, grep, cut, or less in order to make the most of the result.
	
	Examples:
	
	\b
	  * rdr list local
	  * rdr list remote | less -S
	  * rdr list remote | grep love | less -S -x32
	  * rdr list remote | grep love | cut -f1 | less
	  
	See also: rdr download"""
	
	# configure
	TSV = '/catalog/catalog.tsv'

	# require
	from os       import listdir, system
	from requests import get

	# initialize
	localLibrary  = configuration( 'localLibrary' )
	remoteLibrary = configuration( 'remoteLibrary' )
	
	# branch accordingly; local
	if location == 'local' :
		
		# read, sort, and output
		carrels = listdir( localLibrary )
		carrels.sort()
		for carrel in carrels : click.echo( carrel )
	
	# remote; get, and output
	elif location == 'remote' : click.echo( get( remoteLibrary + TSV ).text )
	
	# error
	else : 
		click.echo( f"Error: Unknown value for location: { location }" )
		system( 'rdr list --help' )		

