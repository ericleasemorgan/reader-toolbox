
# require
from rdr import *

# list
@click.command()
@click.argument( 'location' )
def list( location ) :

	"""
    Output a list of study carrels where LOCATION is either 'local' or 'remote'. Consider piping the results through your pager, such a less. For example:

      rdr list local | less

    The resulting list can be quite long. Consider filtering the output using grep, such as:

      rdr list local | grep subject
	"""

	# configure
	TSV = '/catalog/catalog.tsv'
	
	# local list
	if ( location == 'local' ) :
		carrels = os.listdir( LOCALLIBRARY )
		carrels.sort()
		for carrel in carrels : click.echo( carrel )
	
	# remote list
	elif ( location == 'remote' ) : click.echo( requests.get( REMOTELIBRARY + TSV ).text )
	
	# error
	else : 
		click.echo( f"Error: Unknown value for location: { location }" )
		os.system( 'rdr list --help' )		

