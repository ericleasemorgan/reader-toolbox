
# read - open the root of a study carrel in a Web browser

# require
from rdr import *

# read
@click.command( options_metavar='<options>' )
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='where is the carrel')
@click.argument( 'carrel', metavar='<carrel>' )
def read( carrel, location ) :

	"""Open <carrel> in your Web browser.
	
	Use this subcommand to peruse the narrative texts and interactive reports found in <carrel>; use this command to become familiar with the content of <carrel>.
	
	Examples:
	
	\b
	  rdr read homer
	  rdr read -l remote homer
	  rdr read -l remote sonnets
	  rdr read -l remote pride
	
	See also: rdr browse --help"""
		
	# require
	from webbrowser import open
	
	if location == 'local' :
	
		# sanity check
		checkForCarrel( carrel )

		localLibrary  = configuration( 'localLibrary' )
		url = 'file://' + str( localLibrary/carrel/INDEX )
		open( url )
		
	elif location == 'remote' :
	
		url = REMOTELIBRARY + '/' + CARRELS + '/' + carrel
		open( url )
