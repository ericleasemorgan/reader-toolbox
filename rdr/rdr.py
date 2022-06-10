

# rdr.py - a command-line interface for using Distant Reader study carrels

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 30, 2021 - in Three Oaks with Pat; first real working version

# require
from rdr import *
#import rdr.commands.about         as about
#import rdr.commands.adr           as adr
#import rdr.commands.bib           as bib
#import rdr.commands.catalog       as catalog
#import rdr.commands.cluster       as cluster
#import rdr.commands.collocations  as collocations
#import rdr.commands.concordance   as concordance
#import rdr.commands.download      as download
#import rdr.commands.ent           as ent
#import rdr.commands.grammars      as grammars
#import rdr.commands.ngrams        as ngrams
#import rdr.commands.pos           as pos
#import rdr.commands.readability   as readability
#import rdr.commands.search        as search
#import rdr.commands.semantics     as semantics
#import rdr.commands.sizes         as sizes
#import rdr.commands.url           as url
#import rdr.commands.wrd           as wrd
import rdr.commands.browse        as browse
import rdr.commands.build         as build
import rdr.commands.documentation as documentation
import rdr.commands.edit          as edit
import rdr.commands.get           as get
import rdr.commands.info          as info
import rdr.commands.notebooks     as notebooks
import rdr.commands.play          as play
import rdr.commands.read          as read
import rdr.commands.set           as set
import rdr.commands.sql           as sql
import rdr.commands.summarize     as summarize
import rdr.commands.tm            as tm

# initialize 
@click.group()
def rdr() :

	# require
	from configparser import ConfigParser
	from pathlib      import Path

	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE

	# create configuration file, conditionally
	if not configurationFile.exists() : initializeConfigurations()

	# continue
	pass


# about
@click.command( options_metavar='<options>' )
def about() :

	"""Output a brief description of the Reader Toolbox (rdr) application."""

	# configure
	ABOUT = '''
  The Reader Toolbox (rdr) is a command-line application used to create
  and model data sets called Distant Reader study carrels.
'''

	# do the work and done
	click.echo( ABOUT )


# addresses
@click.command( options_metavar='<options>' )
@click.option('-l', '--like',   type=click.STRING, help="filter results using the given pattern")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def adr( carrel, count, like ) :

	"""Filter email addresses from <carrel>

	Who are you gonna call? 

	Examples:

	\b
	  rdr adr ital
	  rdr adr -c ital
	  rdr adr -c -l gmail ital

	See also: rdr url --help"""

	# do the work and return it
	click.echo( addresses( carrel, count, like ) )


# bibliographics
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-f', '--format', default='text', type=click.Choice( [ 'text', 'html', 'json' ] ), help='type of output')
@click.option('-v', '--save', is_flag=False, help='save result in default location')
def bib( carrel, format, save ) :

	"""Output rudimentary bibliographics from <carrel>

	Use this subcommand to output metadata regarding the specific items in <carrel>. Metadata on the items includes: identifier, author, title, date, size in words, readability (Flesch) score, summary, keywords, location of cached original, and location of derived plain text. Because of the characteristics of the original input used to create <carrel>, some metadata fields may not have values. Author and date are the best examples. Moreover, the value for title be derived. The combined use of the info command and the bib command will garaner you a good understanding of <carrel>'s breadth and depth.

	Example: rdr bib homer

	See also:
	
	\b
	  rdr info --help
	  rdr search --help"""

	if save : bibliography( carrel, format, save )
	else    : click.echo( bibliography( carrel, format ) )


# download
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
def download( carrel ) :

	"""Cache <carrel> from the public library of study carrels

	A collection of about 3,000 pre-created study carrels is available at http://library.distantreader.org. Given <carrel>, this function will download the remote carrel and save it to your local library. You can then use the Toolbox commands to read it.

	Examples:
	
	\b
	  rdr download homer
	  rdr download pride
	  rdr download sonnets

	See also:
	
	\b
	  rdr catalog --help
	  rdr set --help"""
			
	# do the work and give a hint
	downloads( carrel )
	click.echo( ( '''  INFO: You may now any of the RDR commands. For example:

	* rdr info %s
	* rdr bib %s
	* rdr cluster %s
	* rdr ngrams %s -s 2 -c
	* rdr wrd %s -c
	* rdr tm %s
''' ) % ( carrel, carrel, carrel, carrel, carrel, carrel, ), err=True )

# catalog
@click.command( options_metavar='<options>' )
@click.option('-h', '--human', is_flag=True, help='output in a more human-readable form')
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='output in a more human-readable form')
def catalog( human, location ) :

	"""List study carrels
	
	Use this command to enumerate the study carrels cached locally or remotely available at http://library.distantreader.org. The remote option, by default, returns a tab-delimited stream very amenable to post processing with utilities such as cut, grep, sort, and less.
	
	Examples:
	
	\b
	  rdr catalog
	  rdr catalog -l remote
	  rdr catalog -l remote -h

	See also: rdr download --help"""
	
	# do the work and done
	click.echo( catalogs( location, human ) )


# search
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


# word2vec
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-t', '--type', default='similarity', type=click.Choice( [ 'similarity', 'distance', 'analogy', 'scatter' ], case_sensitive=True ), help="query type")
@click.option('-q', '--query', default='love', help='the word(s) to be used for search')
@click.option('-s', '--size', default=10, help='number of results to return')
def semantics( carrel, type, query, size ) :

	'''Apply semantic indexing against <carrel>
	
	Sometimes called "word embedding", use this subcommand to learn: 1) what words are similar to a given word, 2) how close in meaning sets of words are, or 3) what words compare to three other words. In order to work accurately, semantic indexing requires larger rather than smaller corpora; results from corpora less than 1,500,000 words in size ought to be considered dubious at best.
	
	This command requires a Python module called "word2vec", which is not installed by default. This is because the module needs to be compiled and doing so on Windows computers is challenging. Linux and Macintosh users can probably do 'pip install word2vec', but Windows users will have to go through additional hoops. But please be consoled when you remember that corpora less than 1.5 million words do not return accurate results. Is <carrel> 1.5 million words long?
	
	Examples:
	
	\b
	  rdr semantics -t similarity -q war homer
	  rdr semantics -t distance -q "king queen prince love war" homer
	  rdr semantics -t analogy -q "king queen prince" homer'''

	# do the work and done
	click.echo( word2vec( carrel, type, query, size ) )

	
# collocations
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-f', '--filter',  default=4, help="least number of occurances of bigram")
@click.option('-m', '--measure', default='chisqr', type=click.Choice( [ 'fisher', 'chisqr', 'jaccard', 'likelihood', 'raw' ], case_sensitive=True ), help="type of measure")
@click.option('-l', '--limit',   default=4000, help="number of features")
@click.option('-w', '--window',  default=4, help="size of window")
@click.option('-o', '--output',  default='image', type=click.Choice( [ 'image', 'gml' ], case_sensitive=True ), help="type of output")
@click.option('-v', '--save',    is_flag=True, help='save graph to default location')
def collocations( carrel, window, filter, measure, limit, output, save ) :

	'''Output network graph based on bigram collocations in <carrel>

	This is an additional way of answering the questions: 1) what words are spoken in the same breath as other words, and 2) what words taken together connote themes. Given a study carrel of about 200,000 words, the default values ought to generate a network graph with enough depth to be interesting. Specify the -o option to output a Graph Modeling Language (GML) file, and load the result into a visualizer like Gephi. If the image output by the Toolbox is not very dense, then iteratively increase or decrease the values of -l and -f until the density is appealing. The various measures are used to denote the significance of collocations.

	Examples:

	\b
	  rdr networks homer
	  rdr networks homer -o gml > homer.gml
	  rdr networks homer -l 2000 -f 18 -w 5
	  rdr networks homer -l 2000 -f 18 -w 5 -o gml > homer.gml
	  rdr networks pride -l 1600 -f 8'''

	# do the work
	collocate( carrel, window, filter, measure, limit, output, save )

	
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
	

# cluster
@click.command( options_metavar='[<options>]' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-t', '--type', default='dendrogram', type=click.Choice( [ 'dendrogram', 'cube' ] ), help='denote the shape of the output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def cluster( carrel, type, save ) :

	"""Apply dimension reduction to <carrel> and visualize the result
	
	This is useful for determining how holistic <carrel> is. A carrel with many clusters is less holistic and probably means the number of latent topics (think "subjects") is high. On the other hand, you may observe clusters falling into distinct groups surrounding authors, titles, or sources. In other words, use this subcommand to learn the degree <carrel> is a hodgepodge of items or a collection of related items. 
	
	Example: rdr cluster homer
	
	See also: rdr tm --help"""

	# do the work
	clusters( carrel, type, save )


# named entities
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


# parts-of-speech
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

# ngrams
@click.command( options_metavar='<options>' )
@click.option('-q', '--query',     type=click.STRING, help="filter results to include the given regular expression")
@click.option('-c', '--count',     is_flag=True, help='count and tabulate the result')
@click.option('-l', '--location',  default='local', type=click.Choice( [ 'local', 'remote' ] ), help='where is the study carrel')
@click.option('-s', '--size',      default=1, help='denote unigrams, bigrams, trigrams, etc')
@click.option('-w', '--wordcloud', is_flag=True, help='given -c, output a wordcloud')
@click.option('-v', '--save',      is_flag=True, help='given -c and -w, save cloud to default location')
@click.argument( 'carrel', metavar='<carrel>' )
def ngrams( carrel, size, query, count, location, wordcloud, save ) :

	"""Output and list words or phrases found in <carrel>

	This is almost always one of the first places to start when doing your analysis, and it can be applied to local as well as remote study carrels. Ngrams with sizes (-s) greater than 2 will include stopwords because ngrams of three or more words often do not make sense without them. Use the -c option to count and tabulate the result. Use the query (-q) to filter the result with a regular expression. 

	Examples:

	\b
	  rdr ngrams homer
	  rdr ngrams -s 2 homer
	  rdr ngrams -s 2 -c homer
	  rdr ngrams -s 2 -c -q love homer
	  rdr ngrams -s 2 -c -q love homer | more
	  rdr ngrams -s 2 -c -q love -l remote sonnets | more

	See also: rdr concordance --help"""

	if not save : click.echo( ngramss( carrel, size, query, count, location, wordcloud ) )
	else        : ngramss( carrel, size, query, count, location, wordcloud, save )


# readability
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='score', type=click.Choice( [ 'id', 'score' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def readability( carrel, sort, output, save ) :

	"""Report on the readability (Flesch score) of items in <carrel>
	
	It is possible to denote how difficult a text is to read by measuring things like number of words, density of the vocabulary, the length of a document, etc. Such calculations have been done against <carrel>, and this subcommand will output the results. If the returned values are wide-ranging, then this will tell you one thing about <carrel>. For example, some of the documents are either difficult to read, very long, or poorly transcribed ("OCR'ed"). If the measurements are homogeneous, then your carrel is more sane than not.
	
	Example: rdr readability homer -o boxplot"""

	# do the work
	if not save : click.echo( flesch( carrel, sort, output ) )
	else        : flesch( carrel, sort, output, save )


# sizes
@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-s', '--sort', default='words', type=click.Choice( [ 'id', 'words' ] ), help='order result')
@click.option('-o', '--output', default='list', type=click.Choice( [ 'list', 'histogram', 'boxplot' ] ), help='type of output')
@click.option('-v', '--save', is_flag=True, help='save result in default location')
def sizes( carrel, sort, output, save ) :

	"""Report on the sizes (in words) of items in <carrel>"""

	# do the work
	click.echo( size( carrel, sort, output, save ) )

# concordance
@click.command( options_metavar='[<options>]' )
@click.option('-w', '--width', default=80, help='number of characters in each line of output')
@click.option('-l', '--lines', default=999, help='number of lines of text to output')
@click.option('-q', '--query', default='love', help='a word for phrase')
@click.argument( 'carrel', metavar='<carrel>' )
def concordance( carrel, query, width, lines ) :

	"""A poor man's search engine
	
	Given a query, this subcommand will search <carrel> and return a list of results where each result is a set of words to the left of query, the query, and a set of words to the right of query -- a keyword-in-context index. This is useful for answering the question, "What words are used in the same breath as the given word?" The query can be a phrase, but it can not be a regular expression. Consider creating a word cloud from the output of this command to visualize the "words used in the same breath". 
	
	Examples:
	
	\b
	  rdr concordance homer -q hector
	  rdr concordance homer -q 'hector was'

	See also: rdr ngrams --help"""
	
	# do the work
	click.echo( concordancing( carrel, query ) )


# keywords
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


# urls
@click.command( options_metavar='<options>' )
@click.option('-s', '--select', default='url', type=click.Choice( [ 'url', 'domain' ] ), help='full URLs or just domain')
@click.option('-l', '--like',   type=click.STRING, help="filter results using the expression")
@click.option('-c', '--count', is_flag=True, help='count and tabulate the result')
@click.argument( 'carrel', metavar='<carrel>' )
def url( carrel, select, count, like ) :

	"""Filter URLs and domains from <carrel>

	Use this subcommand to learn what is hyperlinked from <carrel>. To the best of its ability, the Distant Reader extracted all the URLs found in <carrel>. This information was saved in sets of files located in the urls directory of <carrel>. This information as has been saved in a relational database file. This subcommand queries that database. Use this command to learn what URLs are in the carrel and from what domains do the URLs emanate. Through this process you may identify URLs of extreme importance or characterize the URLs as coming from governments, companies, organizations. Alternatively, you may create lists of URLs that can be fed to Internet spiders for harvesting or feeding back into the Reader for additional carrel creation. Be forewarned. The plain text whence these URLs came is ugly, thus producing ugly URLs; not all values for URLs are valid.

	Examples:

	\b
	  rdr url ital
	  rdr url -s url ital
	  rdr url -s url -l .pdf ital
	  rdr url -s domain -c ital

	See also: rdr adr --help"""

	# do the work and return it
	click.echo( urls( carrel, select, count, like ) )


# update the list of commands
rdr.add_command( about )
rdr.add_command( adr )
rdr.add_command( bib )
rdr.add_command( browse.browse )
rdr.add_command( build.build )
rdr.add_command( catalog )
rdr.add_command( cluster )
rdr.add_command( documentation.documentation )
rdr.add_command( collocations )
rdr.add_command( concordance )
rdr.add_command( download )
rdr.add_command( edit.edit )
rdr.add_command( ent )
rdr.add_command( get.get )
rdr.add_command( grammars )
rdr.add_command( info.info )
rdr.add_command( ngrams )
rdr.add_command( play.play )
rdr.add_command( notebooks.notebooks )
rdr.add_command( pos )
rdr.add_command( read.read )
rdr.add_command( readability )
rdr.add_command( search )
rdr.add_command( semantics )
rdr.add_command( set.set )
rdr.add_command( sizes )
rdr.add_command( sql.sql )
rdr.add_command( tm.tm )
rdr.add_command( url )
rdr.add_command( wrd )
rdr.add_command( summarize.summarize )


# do the work
if __name__ == '__main__' : rdr()
