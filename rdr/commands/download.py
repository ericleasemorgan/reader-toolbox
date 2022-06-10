
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
			
	# do the work and give a hint
	downloads( carrel )
	click.echo( ( '''  INFO: You may now any of the RDR commands. For example:

	* rdr info %s
	* rdr bib %s
	* rdr cluster %s
	* rdr ngrams %s -s 2 -c
	* rdr wrd %s -c
	* rdr tm %s
''' ) % ( carrel, carrel, carrel, carrel, carrel, carrel, ), err=True )
