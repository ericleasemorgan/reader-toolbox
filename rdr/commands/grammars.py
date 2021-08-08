
# features - output different types of features found in a text

# require
from rdr import *


# filter
def applyFilter ( filter, features ) :

	# initialize and process each feature
	filtered = []
	for feature in features :
				
		# branch according to type; Span
		if str( type( feature ) ) == "<class 'spacy.tokens.span.Span'>" : 
		
			# update, conditionally
			if filter in feature.text : filtered.append( feature )

		# hope for a tuple with three elements
		else :
		
			# update, conditionally
			if ( ( filter in feature[ 0 ].text ) or
			     ( filter in feature[ 1 ].text ) or 
			     ( filter in feature[ 2 ].text ) ) : filtered.append( feature )
		
	# done
	return ( filtered )


# output
def outputFeatures( features ) :

	# process each feature
	for feature in features :
			
		# branch accordingly
		if str( type( feature ) ) == "<class 'spacy.tokens.span.Span'>" : click.echo( feature.text )
		else : click.echo( "\t".join( ( feature[ 0 ].text, feature[ 1 ].text, feature[ 2 ].text ) ) )


# grammars
@click.command( options_metavar='<options>' )
@click.option('-f', '--filter', type=click.STRING, help="limit results to include the given word")
@click.option('-n', '--noun', type=click.STRING, help="only applicable to sss; a noun or noun phrase")
@click.option('-v', '--verb', default='be', help="only applicable to sss; the lemma of a verb, such as 'be', 'have', or 'say'")
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'grammar', type=click.Choice( [ 'svo', 'sss', 'nouns', 'quotes' ], case_sensitive=True ) )
def grammars( carrel, grammar, filter, noun, verb ) :

	"""Extract grammatical sentence fragments from <carrel> where fragments are one of:
	
	\b
	  * nouns - all the nouns and noun chunks
	  * quotes - things people say
	  * svo - fragments in the form of subject-verb-object
	  * sss - a more advanced version of svo; fragments beginning
	    with an entity, are connected with a verb, and are followed
	    by a phrase
	
	Examples:
	
	\b
	  * rdr grammars homer svo
	  * rdr grammars -f horse homer svo
	"""

	# require
	from textacy import extract
	from os      import system
		
	# initialize
	doc = carrel2doc( carrel )

	# get the features
	if   grammar == 'svo'    : features = list( extract.subject_verb_object_triples( doc ) )
	elif grammar == 'quotes' : features = list( extract.direct_quotations( doc ) )
	elif grammar == 'nouns'  : features = list( extract.noun_chunks( doc ) )
	elif grammar == 'sss'    :

		# sanity check
		if not noun :
		
			click.echo( "Error: When specifying grammar sss, the -n option is required.", err=True )
			system( 'rdr grammars --help' )
			exit()
			
		# do the work
		features = list( extract.semistructured_statements( doc, entity=noun, cue=verb ) )

	# filter, conditionally
	if filter : features = applyFilter( filter, features )
	
	# output
	outputFeatures( features )
	

