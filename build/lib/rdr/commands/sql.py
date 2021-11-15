
# datasette - given a carrel, browse its database

# require
from rdr import *

@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def sql( carrel ) :

	"""Use SQL queries against the database of <carrel>.
	
	Study carrels are made up of many files. One of those files is an SQLite database file (etc/reader.db). Use this subcommand to query the database. Because the database is relational in design, the use of SQL can draw information from many different tables and address almost any question about <carrel>. An excellent query that an be applied to any carrel includes:
	
	\b
	  SELECT b.id, GROUP_CONCAT( w.keyword, '; ' ) AS keywords, b.summary
	  FROM bib AS b, wrd AS w
	  WHERE b.id = w.id
	  GROUP BY b.id
	  ORDER BY b.id;
	
	Example: rdr sql homer"""

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

