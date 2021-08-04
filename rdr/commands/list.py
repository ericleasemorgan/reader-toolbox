
# list - given a location, output a list of study carrels

# require
from rdr import *

@click.command()
@click.argument( 'location' )
def list( location ) :

	"""List contents of the library at the given LOCATION"""
	
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

