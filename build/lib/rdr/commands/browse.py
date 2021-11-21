
# browse - given a carrel, use lynx to navigate its file system

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='the location of the carrel')
@click.argument( 'carrel', metavar='<carrel>' )
def browse( carrel, location ) :

	"""Peruse <carrel> as a file system.
	
	Study carrels are sets of HTML files, other plain text files, a whole lot of tab-delimited files, and an SQLite database file all organized in a file system -- a data set. This command uses a two different techniques for browsing the file systems. If the study carrel is saved locally, then it will try to use a terminal-based Web browser call Lynx. If the carrel is remote, then you will be directed to a dynamically generated HTML page. Because all study carrels have the same layout, this subcommand is useful for learning how many files and of what type are contained in <carrel>.
	
	Examples:
	
	\b
	  rdr browse homer
	  rdr browse -l remote homer
	
	See also: rdr read --help"""

	# configure
	LYNX = 'lynx'
	
	# require
	from os import system
	import webbrowser
	
	# local carrel
	if location == 'local' :
	
		# sanity check
		checkForCarrel( carrel )

		# initialize, create a URL, and do the work
		localLibrary = str( configuration( 'localLibrary' ) )
		url          = 'file://' + localLibrary + '/' + carrel
		system( LYNX + ' ' + url )

	# remote carrel
	elif location == 'remote' :
	
		url = '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, MANIFEST ] )
		webbrowser.open( url )
