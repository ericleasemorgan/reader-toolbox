
# pos - given a study carrel, output... parts-of-speech

# require
from rdr import *

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-s', '--select',    default='parts', type=click.Choice( [ 'parts', 'words', 'lemmas' ] ), help='the type of output')
@click.option('-l', '--like',      default='any', help='the part-of-speech')
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-n', '--normalize', is_flag=True, help='lower-case the words or lemmas')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, output a wordcloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save cloud to default location')
@click.argument( 'carrel', metavar='<carrel>' )
def pos( carrel, select, like, count, normalize, wordcloud, save ) :

	"""Filter parts-of-speech, words, and lemmas found in <carrel>

	Use this subcommand to address questions such as: what is mentioned in <carrel>, what do those things do, and how are they described. A spaCy language model was applied to every item in <carrel>. The model was used to denote nouns, verbs, adjectives, punctuation, etc. It was also used to denote the lemma values (think "root") of each word. This information was saved in files in the pos directory of <carrel>, but it has also been saved in a relational database. This subcommand queries that database. Using this commmand, you can begin to characterize an author's style, learn to what degree the action about saying, examining, or doing, and more importantly, put words into context because they have been associated with specific parts-of-speech values. Finally, the spaCy model works well, most of the time. Please don't let the perfect be the enemy of the good.

	Examples:

	\b
	  rdr pos homer
	  rdr pos -c homer
	  rdr pos -s words -l N -c homer
	  rdr pos -s lemmas -l N -c -n homer
	  rdr pos -s lemmas -l V -c -n homer

	See also:
	
	\b
	  rdr ngrams --help
	  rdr ent --help"""

	# do the work and done
	if not wordcloud : click.echo( partsofspeech( carrel, select, like, count, normalize ) )
	else             : partsofspeech( carrel, select, like, count, normalize, wordcloud, save )