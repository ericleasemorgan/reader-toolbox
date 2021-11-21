
# download - given the name of a remote carrel, cache it locally

# require
from rdr import *

# harvest
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def download( carrel ) :

	"""Cache <carrel> from the public library of study carrels.

	A collection of about 3,000 pre-created study carrels is available at http://library.distantreader.org. Given <carrel>, this function will download the remote carrel and save it locally.

	Example: rdr download homer

	See also:
	
	\b
	  rdr catalog --help
	  rdr set --help"""
			
	# configure
	ZIPFILE = 'study-carrel.zip'
	CARRELS = 'carrels'

	# require
	from requests import get
	from tempfile import TemporaryFile
	from zipfile  import ZipFile

	# initialize
	localLibrary  = configuration( 'localLibrary' )

	# get the remote zip file; needs error checking
	click.echo( "Getting study carrel... ", err=True )
	response = get( REMOTELIBRARY + '/' + CARRELS + '/' + carrel + '/' + ZIPFILE )
	
	# initialize a temporary file and write to it
	click.echo( "Saving study carrel... ", err=True )
	handle = TemporaryFile()
	handle.write( response.content )
	
	# unzip the temporary file and close it, which also deletes it
	click.echo( "Unziping study carrel... " )
	with ZipFile( handle, 'r' ) as zip : zip.extractall( str( localLibrary ) )
	handle.close()

	# done
	click.echo( "Done." )
