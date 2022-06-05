
# ent - given a study carrel, output named entitites

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--select',    default='type', type=click.Choice( [ 'type', 'entity' ] ), help='the type of output')
@click.option('-l', '--like',      default='any', help='the type of enity')
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, output a wordcloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save cloud to default location')
def ent( carrel, select, like, count, wordcloud, save ) :

	"""Filter named entities and types of entities found in <carrel>

	Use this subcommand to address who, what, when, and where questions regarding <carrel>. A spaCy language model was applied to each item in your study carrel. This process extracted named-entities (persons, places, organizations, dates, times, etc.) and saved them in files located in the ent directory of <carrel>. This same data was also distilled into a relational database file, and this subcommand queries that database file. Through the use of this subcommand, you can learn what people are mentioned, what places are mentioned, what dates and times are mentioned, etc. Based on these things, you will be able to characterize <carrel>. For example, are the mentioned people Platonists? Does most of the action take place in American or someplace in Europe, and if so, then where? Finally, the spaCy model works well, most of the time. There will be errors, but please don't let the perfect be the enemy of the good.

	Examples:
	
	\b
	  rdr ent homer
	  rdr ent -c homer
	  rdr ent -s entity -c homer
	  rdr ent -s entity -l PERSON -c homer
	  
	See also: rdr pos --help"""

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	
	# branch accordingly; types of entities
	if select == 'type' :
	
		# dump
		if not count :

			# articulate sql, search, and output
			sql  = 'SELECT type FROM ent;'
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ 'type' ] )

		# count and tabulate the dump
		else :
		
			# articulate sql, search, and output
			sql  = 'SELECT type, COUNT( type ) AS count FROM ent GROUP BY type ORDER BY count DESC;'
			rows = connection.execute( sql )
			for row in rows : click.echo( "\t".join( [ row[ 'type' ], str( row[ 'count' ] ) ] ) )			
			
	# entities
	else : 
			
		# initialize like
		if like == 'any' : like = '%'
		else             : like == like.upper()
		
		# simply dump the desired content
		if not count :
		
			# build sql, search, and output
			sql  = ( 'SELECT entity FROM ent WHERE type LIKE "%s";' % ( like ) )
			rows = connection.execute( sql )
			for row in rows : click.echo( row[ select ] )
		
		# count and tabulate the result
		else:

			# build sql, search, and output
			sql  = ( 'SELECT entity, COUNT( entity ) AS count FROM ent WHERE type LIKE "%s" GROUP BY entity ORDER BY count DESC;' % ( like ) )
			rows = connection.execute( sql )
			
			# output simple tabulation
			if not wordcloud :
			
				# dump
				for row in rows : click.echo( "\t".join( [ row[ select ], str( row[ 'count' ] ) ] ) )
			
			# output word cloud
			else :
			
				# create a dictionary of frequencies
				frequencies = {}
				for row in rows : frequencies[ row[ select ] ] = row[ 'count' ]

				# simply output
				if not save : cloud( frequencies )
			
				# save to the corresponding figures directory
				else :
			
					# configure
					localLibrary = configuration( 'localLibrary' )

					# any
					if like == '%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESANY
						cloud( frequencies, file=file )
					
					# persons
					elif like == 'PERSON' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESPERSON
						cloud( frequencies, file=file )
				
					# org
					elif like == 'ORG' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESORG
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'GPE' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESGPE
						cloud( frequencies, file=file )
				
					# unsupported
					else : click.echo( "The save option is only valid for entities of type any, PERSON, ORG, or GPE; there is no default location for anything else.", err=True )



	# clean up
	connection.close()

