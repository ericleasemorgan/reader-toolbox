
# features - output different types of features found in a text

# require
from rdr import *

# features
@click.command( options_metavar='<options>' )
@click.option('-e', '--entity', type=click.STRING, help="only applicable to grammar sss; a noun or noun phrase")
@click.option('-v', '--verb', default='be', help="only applicable to grammar sss; the lemma of a verb, such as 'be', 'have', or 'say'")
@click.argument( 'carrel', metavar='<carrel>' )
@click.argument( 'grammar', type=click.Choice( [ 'svo', 'sss', 'nouns', 'quotes' ], case_sensitive=False ) )
def grammars( carrel, grammar, entity, verb ) :

	"""Extract grammatical sentence fragments from <carrel> where fragments are one of:
	
	  \b
	  * nouns - all the nouns and noun chunks
	  * quotes - things people say
	  * svo - fragments in the form of subject-verb-object
	  * sss - fragments beginning with an entity, are connected with a
	    verb, and are followed by a phrase; a more advanced version of
	    svo

	The use of language requires patterns and rules. We call theses things grammars. Unlike the tabulation of ngrams, parts-of-speech, named-entities, etc., the use of grammars enables one to extract complete thoughts. The results of theses functions are tab-delimited lists, and therefore they are amenable to post-processing with utilities such as sort, grep, and less. Use 'rdr pos' to identify interesting values for the sss grammar.
	
	Examples:
	
	\b
	  * rdr grammars homer svo
	  * rdr grammars homer svo | sort | less
	  * rdr grammars homer svo | sort | less -x18
	  * rdr grammars -e hector homer sss 
	  * rdr grammars -e she -v have homer sss 
	  * rdr grammars homer quotes
	  * rdr grammars homer nouns
	  * rdr grammars homer nouns | sort | uniq -c | sort -rn | less
	"""

	# require
	from textacy import extract
	from os      import system
	
	# subjects-verbs-objects
	if grammar == 'svo' :
	
		# initialize and get the features
		doc      = carrel2doc( carrel )
		features = list( extract.subject_verb_object_triples( doc ) )
	
		# process each one
		for feature in features : 
		
			# parse and output
			subject = feature[ 0 ].text
			verb    = feature[ 1 ].text
			object  = feature[ 2 ].text

			# output
			click.echo( "\t".join( ( subject, verb, object ) ) )
	
	# noun chunks
	elif grammar == 'nouns' :

		# initialize
		doc      = carrel2doc( carrel )
		features = list( extract.noun_chunks( doc ) )

		# process each one
		for feature in features : 
		
			# parse and output
			chunk = feature.text

			# output
			click.echo( chunk )
	
	# semistructured statements
	elif grammar == 'sss' :

		# sanity check
		if not entity :
		
			click.echo( "Error: When specifyig type sss, the -e option is required.", err=True )
			system( 'rdr grammars --help' )
			exit()
			
		# initialize
		doc      = carrel2doc( carrel )
		features = list( extract.semistructured_statements( doc, entity=entity, cue=verb ) )

		# process each one
		for feature in features : 
		
			# parse and output
			entity   = feature[ 0 ].text
			cue      = feature[ 1 ].text
			fragment = feature[ 2 ].text

			# output
			click.echo( "\t".join( ( entity, cue, fragment ) ) )
	
	# direct quotes
	elif grammar == 'quotations' :

		# initialize
		doc      = carrel2doc( carrel )
		features = list( extract.direct_quotations( doc ) )
	
		# process each one
		for feature in features : 
		
			# parse and output
			speaker   = feature[ 0 ].text
			verb      = feature[ 1 ].text
			quotation = feature[ 2 ].text

			# output
			click.echo( "\t".join( ( speaker, verb, quotation ) ) )
