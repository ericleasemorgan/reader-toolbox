
# require
from rdr import *

# datasette
@click.command()
@click.argument( 'carrel' )
def datasette( carrel ) :

	"""Use Datasette to search & browse the given carrel's database"""

	# configure
	DATABASE  = 'reader.db'
	ETC       = 'etc'
	DATASETTE = 'datasette'
		
	# build the shell command and go
	database = LOCALLIBRARY + '/' + carrel + '/' + ETC + '/' + DATABASE
	os.system( DATASETTE + ' ' + database + ' -o' )

