
# browse - given a carrel, use lynx to navigate its file system

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def browse( carrel ) :

	"""Use a Web browser called Lynx to peruse <carrel>
	
	Study carrels are sets of HTML files, other plain text files, and a whole lot of tab-delimited files organized into file system. Lynx is very useful tool for inspecting the contents of these files from the terminal, especially if you are not accessing the carrel through a Web server.
	
	Example: rdr browse homer
	
	See also: rdr read"""

	# configure
	LYNX = 'lynx'
	
	# require
	from os import system
	
	# initialize, create a URL, and do the work
	localLibrary = str( configuration( 'localLibrary' ) )
	url          = 'file://' + localLibrary + '/' + carrel
	system( LYNX + ' ' + url )
