
# bib - given a study carrel, output rudimentary bibliographics

# require
from rdr import *

# ngrams
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