
# download - given the name of a remote carrel, cache it locally

# require
from rdr import *

# harvest
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def download( carrel ) :

	"""Cache <carrel> from the public library of study carrels

	A collection of about 3,000 pre-created study carrels is available at http://library.distantreader.org. Given <carrel>, this function will download the remote carrel and save it to your local library. You can then use the Toolbox commands to read it.

	Examples:
	
	\b
	  rdr download homer
	  rdr download pride
	  rdr download sonnets

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
	click.echo( "\n  INFO: Downloading remote study carrel... ", err=True )
	response = get( REMOTELIBRARY + '/' + CARRELS + '/' + carrel + '/' + ZIPFILE )
	
	# initialize a temporary file and write to it
	click.echo( "  INFO: Saving study carrel... ", err=True )
	handle = TemporaryFile()
	handle.write( response.content )
	
	# unzip the temporary file and close it, which also deletes it
	click.echo( "  INFO: Unziping study carrel... ", err=True )
	with ZipFile( handle, 'r' ) as zip : zip.extractall( str( localLibrary ) )
	handle.close()

	# done
	click.echo( ( '''  INFO: Done. You may now any of the RDR commands. For example:

	* rdr info %s
	* rdr bib %s
	* rdr cluster %s
	* rdr ngrams %s -s 2 -c
	* rdr wrd %s -c
	* rdr tm %s
''' ) % ( carrel, carrel, carrel, carrel, carrel, carrel, ), err=True )
