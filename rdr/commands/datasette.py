
# datasette - given a carrel, browse its database

# require
from rdr import *

@click.command()
@click.argument( 'carrel' )
def datasette( carrel ) :

	"""Use Datasette to search & browse the given carrel's database"""

	# configure
	DATASETTE = 'datasette'
		
	# require
	from os import system
	
	# initialize
	localLibrary = configuration( 'localLibrary' )

	# build the shell command and go
	database = localLibrary/carrel/ETC/DATABASE
	system( DATASETTE + ' ' + str( database ) + ' -o' )

