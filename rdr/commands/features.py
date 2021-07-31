
# require
from rdr import *


# given a carrel, return a spacy doc
def __carrel2doc( carrel ) :

	# configure
	PICKLE  = 'etc/reader.bin'
	CORPUS  = 'etc/reader.txt'

	# initialize
	pickle = LOCALLIBRARY + '/' + carrel + '/' + PICKLE

	# check to see if we've previously been here
	if os.path.exists( pickle ) :
		
		# read the pickle file
		doc = next( textacy.io.spacy.read_spacy_docs( pickle ) )
	
	# otherwise
	else :
	
		# warn
		click.echo( 'Reading and formatting data for future use. This may take many minutes. Please be patient...\n', err=True )

		# create a doc
		file = LIBRARY + '/' + carrel + '/' + CORPUS
		text = open( file ).read()
		size = ( os.stat( file ).st_size ) + 1
		nlp  = spacy.load( MODEL, max_length=size )
		doc  = nlp( text )

		# save it for future use
		textacy.io.spacy.write_spacy_docs( doc, filepath=pickle )

	# done
	return doc


# features
@click.command()
@click.argument( 'carrel' )
@click.argument( 'feature' )
def features( carrel, feature ) :

	"""Given the name of a CARREL, extract FEATURES where they one of 'svo','sss', 'noun-chunks',' quotations'"""

	# subjects-verbs-objects
	if feature == 'svo' :
	
		# initialize
		doc = __carrel2doc( carrel )
	
		# get the features
		features = list( textacy.extract.subject_verb_object_triples( doc ) )
	
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
		doc = __carrel2doc( carrel )
	
		# get the features
		features = list( textacy.extract.noun_chunks( doc ) )

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
		doc = __carrel2doc( carrel )
	
		# get the features
		features = list( textacy.extract.semistructured_statements( doc, entity=entity, cue=cue ) )

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
		doc = __carrel2doc( carrel )
	
		# get the features
		features = list( textacy.extract.direct_quotations( doc ) )
	
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
		os.system( 'rdr feature --help' )		
