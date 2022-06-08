
# wrd - given a study carrel, output keywords

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, visualize as word cloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save result in defaul location')
@click.argument( 'carrel', metavar='<carrel>' )
def wrd( carrel, count, wordcloud, save ) :

	"""Filter statistically computed keywords from <carrel>

	Use this subcommand to address the question, "What is <carrel> about?" Algorithms akin to the venerable TF/IDF and Google's PageRank were used against each item in <carrel> to extract statistically significant keywords (think "subject terms"). These words were saved in files in the wrd directory of <carrel>, and they have been saved to a relational database as well. This command queries that database. The results of this command help you describe the "aboutness" of <carrel> and the keywords can be used to increase precision/recall when doing full text searches. Consider also the use of the resulting keywords as input to the concordance subcommand.

	Examples:

	\b
	  rdr wrd homer
	  rdr wrd -c homer

	See also:
	
	\b
	  rdr concordance --help
	  rdr search --help"""

	# do the work and conditionally output
	if not wordcloud : click.echo( keywords( carrel, count ) )
	else             : keywords( carrel, count, wordcloud, save )