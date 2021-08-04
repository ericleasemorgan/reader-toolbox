
# features - output different types of features found in a text

# require
from rdr import *

# features
@click.command()
@click.argument( 'carrel' )
@click.argument( 'feature' )
def features( carrel, feature ) :

	"""Given the name of a CARREL, extract FEATURES where they one of 'svo','sss', 'noun-chunks',' quotations'"""

	# require
	from textacy import extract
	from os      import system
	
	# subjects-verbs-objects
	if feature == 'svo' :
	
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
	elif feature == 'noun-chunks' :

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
	elif feature == 'sss' :

		# get additional input
		entity = sys.argv[ 3 ]
		cue    = sys.argv[ 4 ]
	
		# initialize
		doc      = carrel2doc( carrel )
		features = list( extract.semistructured_statements( doc, entity=entity, cue=cue ) )

		# process each one
		for feature in features : 
		
			# parse and output
			entity   = feature[ 0 ].text
			cue      = feature[ 1 ].text
			fragment = feature[ 2 ].text

			# output
			click.echo( "\t".join( ( entity, cue, fragment ) ) )
	
	# direct quotes
	elif feature == 'quotations' :

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

	
	# error
	else : 
		click.echo( f"Error: Unknown value for FEATURE: { feature }" )
		system( 'rdr features --help' )		
