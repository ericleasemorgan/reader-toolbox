
# datasette - given a carrel, browse its database

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def datasette( carrel ) :

	"""Use Datasette to query <carrel>'s database
	
	Datasette is an browser-based interface to SQLite database files. Each study carrel includes such a file, and it contains information regarding parts-of-speech, named-entities, bibliographics, keywords, etc. Through the use of Datasette and a knowledge of SQL, the underlying database can be queried and results returned in ways not possible by merely browsing the given reports.
	
	Example: rdr datasette homer"""

	# configure
	DATASETTE = 'datasette'
		
	# require
	from os import system
	
	# sanity check
	checkForCarrel( carrel )

	# initialize
	localLibrary = configuration( 'localLibrary' )

	# build the shell command and go
	database = localLibrary/carrel/ETC/DATABASE
	system( DATASETTE + ' ' + str( database ) + ' -o' )

