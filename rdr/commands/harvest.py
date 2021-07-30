
# configure
ZIPFILE = 'study-carrel.zip'
CARRELS = 'carrels'

# require
from rdr import *

# harvest
@click.command()
@click.argument( 'carrel' )
def harvest( carrel ) :

	"""Download and install a study carrel from the remote library where CARREL is the name of a study carrel"""
			
	# get the remote zip file; needs error checking
	click.echo( "Getting study carrel... ", err=True, nl=False )
	response = requests.get( REMOTELIBRARY + '/' + CARRELS + '/' + carrel + '/' + ZIPFILE )
	
	# initialize a temporary file and write to it
	click.echo( "Saving study carrel... ", err=True, nl=False )
	handle = TemporaryFile()
	handle.write( response.content )
	
	# unzip the temporary file and close it, which also deletes it
	click.echo( "Unziping study carrel... ", err=True )
	with ZipFile( handle, 'r' ) as zip : zip.extractall( LOCALLIBRARY )
	handle.close()

	# done
	click.echo( f"Done. Now you might want to 'rdr info { carrel }'", err=True )
