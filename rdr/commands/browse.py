
# browse - given a carrel, use lynx to navigate its file system

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='where is the library')
@click.argument( 'carrel', metavar='<carrel>' )
def browse( carrel, location ) :

	"""Use a Web browser called Lynx to peruse <carrel>
	
	Study carrels are sets of HTML files, other plain text files, and a whole lot of tab-delimited files organized into a file system -- a data set. Lynx is very useful tool for inspecting the contents of these file systems from the terminal, especially if you are not accessing the carrel through a Web server.
	
	Example: rdr browse homer
	
	See also: rdr read"""

	# configure
	LYNX = 'lynx'
	
	# require
	from os import system
	import webbrowser
	
	# local carrel
	if location == 'local' :
	
		# initialize, create a URL, and do the work
		localLibrary = str( configuration( 'localLibrary' ) )
		url          = 'file://' + localLibrary + '/' + carrel
		system( LYNX + ' ' + url )

	# remote carrel
	elif location == 'remote' :
	
		url = '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, MANIFEST ] )
		webbrowser.open( url )
