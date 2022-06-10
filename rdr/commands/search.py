
# search - given query, do a full text search against the content of a carrel

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.option('-o', '--output', default='human', type=click.Choice( [ 'human', 'csv', 'tsv', 'json', 'count' ] ), help='the format of the results')
@click.option('-q', '--query', default='love', help='a full text query')
@click.argument( 'carrel', metavar='<carrel>' )
def search( query, output, carrel ) :

	'''Perform a full text query against <carrel>
	
	Given words, phrases, fields, and Boolean operators, use this subcommand to find and describe specific items in <carrel>. The query language is quite extensive, but in general, use words and/or phrases, and a list of matching documents ought to be returned. For more detail, please see: https://reader-toolbox.rtfd.io/en/latest/commands.html#search
	
	Examples:
	
	\b
	  rdr search -q 'truth beauty war love' homer
	  rdr search -q 'title:iliad AND summary:war' homer
	  rdr search -q '"keep his anger"' homer'''

	# do the work and done
	click.echo( searching( carrel, query, output ) )