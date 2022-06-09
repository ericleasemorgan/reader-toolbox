
# grammars - output different types of features found in a text

# require
from rdr import *

# grammars
@click.command( options_metavar='<options>' )
@click.option('-g', '--grammar', default='svo', type=click.Choice( [ 'svo', 'sss', 'nouns', 'quotes' ], case_sensitive=True ), help="the desired grammatical structure")
@click.option('-q', '--query',   type=click.STRING, help="filter results using the given regular expression")
@click.option('-n', '--noun',    type=click.STRING, help="only applicable to sss; a noun or noun phrase")
@click.option('-l', '--lemma',   default='be', help="only applicable to sss; the lemma of a verb, such as 'be' (default), 'have', or 'say'")
@click.option('-s', '--sort',    is_flag=True, help='order the results alphabetically')
@click.option('-c', '--count',   is_flag=True, help='tabulate the items in the result')
@click.argument( 'carrel', metavar='<carrel>' )
def grammars( carrel, grammar, query, noun, lemma, sort, count ) :

	"""Extract sentence fragments from <carrel> as in:
	
	\b
	  nouns - all the nouns and noun chunks
	  quotes - things people say
	  svo - fragments in the form of subject-verb-object (the default)
	  sss - a more advanced version of svo; fragments beginning
	    with an entity, co-occur with a verb, and are followed
	    by a phrase
	
	This is very useful for the purposes of listing more complete ideas from a text; the default output will list bunches o' snippets listing what things do to what. Sort the result to more easily identify patterns and anomalies.
	
	Examples:
	
	\b
	  rdr grammars homer
	  rdr grammars -g nouns homer
	  rdr grammars -g sss -n hector -l be homer"""
	
	# do the work
	click.echo( grammarss( carrel, grammar, query, noun, lemma, sort, count ) )