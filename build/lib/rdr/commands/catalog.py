
# catalog - given a location, output a list of study carrels

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.option('-h', '--human', is_flag=True, help='output in a more human-readable form')
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='output in a more human-readable form')
def catalog( human, location ) :

	"""List study carrels.
	
	Use this command to enumerate the study carrels cached locally or remotely available at http://library.distantreader.org. The remote option, by default, returns a tab-delimited stream very amenable to post processing with utilities such as cut, grep, sort, and less.
	
	Examples:
	
	\b
	  rdr catalog
	  rdr catalog -l remote
	  rdr catalog -l remote -h

	See also: rdr download --help"""
	
	# configure
	TSV    = 'catalog/catalog.tsv'
	RECORD = "      item: ##ITEM##\n      name: ##NAME##\n      date: ##DATE##\n  keywords: ##KEYWORDS##\n     items: ##ITEMS##\n     words: ##WORDS##\n     score: ##SCORE##\n     bytes: ##BYTES##\n\n"
	HEADER = "\nThe catalog includes ##COUNT## items, and each is listed below:\n\n"

	# require
	from requests import get
		
	# branch accordingly; local
	if location == 'local' :
		
		# initialize
		localLibrary = configuration( 'localLibrary' )
		
		# read, sort, and output
		carrels = [ carrel.name for carrel in localLibrary.iterdir() if carrel.is_dir() ]
		carrels.sort()
		for carrel in carrels : click.echo( carrel )
	
	# remote
	elif location == 'remote' :
	
		# create person-amenable output
		if human :
		
			# create a rudimentary catalog
			catalog = ''
			count   = 0
			
			records = get( REMOTELIBRARY + '/' + TSV ).text 
			for item, record in enumerate( records.split( '\n' ) ) :
			
				# delimit and sanity check
				fields = record.split( '\t' )
				if len( fields ) != 7 : break
			
				# parse
				name     = fields[ 0 ]
				date     = fields[ 1 ]
				keywords = fields[ 2 ]
				items    = fields[ 3 ]
				words    = fields[ 4 ]
				score    = fields[ 5 ]
				bytes    = fields[ 6 ]
			
				# increment
				count += 1
				item  += 1
				
				# update
				record   = RECORD.replace( '##ITEM##', str( item ) )
				record   = record.replace( '##NAME##', name )
				record   = record.replace( '##DATE##', date )
				record   = record.replace( '##KEYWORDS##', keywords )
				record   = record.replace( '##ITEMS##', items )
				record   = record.replace( '##WORDS##', words )
				record   = record.replace( '##SCORE##', score )
				record   = record.replace( '##BYTES##', bytes )
				catalog += record
				
			# add the header and output
			header  = HEADER.replace( '##COUNT##', str( count ) )
			catalog = header + catalog
			click.echo_via_pager( catalog )
				
		# get the raw data and hope the results get piped to utilities like sort, grep, cut, less, etc.
		else : click.echo( get( REMOTELIBRARY + '/' + TSV ).text  )

