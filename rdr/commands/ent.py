
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

	# do the work
	if not wordcloud : click.echo( entities( carrel, select, like, count ) )
	else             : entities( carrel, select, like, count, wordcloud, save )