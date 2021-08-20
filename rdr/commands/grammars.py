
# grammars - output different types of features found in a text

# require
from rdr import *


# handle model not found error
def modelNotFound() :
	
	# notify
	click.echo( "Error: Langauge model not found.", err=True )
	click.echo()
	click.echo( f"This functions requires a spaCy langauge model ({ MODEL}) to be installed. This only has to be done once, and after the model has been installed you can run the command again.", err=True )
	click.echo()
	click.echo( 'Do you want to install the model now? [yn] ', err=True, nl=False )
	
	# get input
	c = click.getchar()
	click.echo()
	
	# branch accordingly; yes
	if c == 'y' :

		# require and do the work
		from os import system
		system( 'python -m spacy download ' + MODEL )
	
	# no
	elif c == 'n' : click.echo( "Okay, but installing the model is necessary for this function to work. You'll be asked again next time.", err=True )

	# error
	else : click.echo( '???' )
	
	# done
	exit()


# given a carrel, return a spacy doc
def carrel2doc( carrel ) :

	# configure
	PICKLE = 'reader.spacy'

	# require
	from os        import path, stat
	from spacy     import load
	import textacy
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	pickle       = localLibrary/carrel/ETC/PICKLE

	# check to see if we've previously been here
	if path.exists( pickle ) :
		
		# read the pickle file
		try            : doc = next( textacy.io.spacy.read_spacy_docs( pickle, lang=MODEL ) )
		except OSError : modelNotFound()
			
	# otherwise
	else :
	
		# warn
		click.echo( '''Modeling study carrel data for future use. This may take many
minutes, but it will only have to be done once. In the meantime,
ask yourself, "Self, what is justice?"''', err=True )

		# initialize 
		file           = localLibrary/carrel/ETC/CORPUS
		text           = open( str( file ) ).read()
		size           = ( stat( file ).st_size ) + 1
		
		# initialize some more
		try            : nlp  = load( MODEL )
		except OSError : modelNotFound()
		
		# do the work
		nlp.max_length = size
		doc            = nlp( text )

		# save it for future use
		textacy.io.spacy.write_spacy_docs( doc, filepath=pickle )

	# done
	return doc


# filter
def applyFilter ( query, features ) :

	# require
	from re import search
	
	# initialize and process each feature
	filtered = []
	for feature in features :
				
		# branch according to type; span
		if str( type( feature ) ) == "<class 'spacy.tokens.span.Span'>" : string = feature.text

		# hope for a tuple with three elements; these need to be functions
		else :
		
			if str( type( feature ) ) == "<class 'textacy.extract.triples.SVOTriple'>" :		

				# parse and stringify
				subject = [ token.text_with_ws for token in feature.subject ]
				verb    = [ token.text_with_ws for token in feature.verb ]
				object  = [ token.text_with_ws for token in feature.object ]
				string  = ( ' '.join( [ ''.join( subject ), ''.join( verb ), ''.join( object ) ] ) )

			elif str( type( feature ) ) == "<class 'textacy.extract.triples.DQTriple'>" :		

				# parse and stringify
				speaker = [ token.text_with_ws for token in feature.speaker ]
				cue     = [ token.text_with_ws for token in feature.cue ]
				content = feature.content.text_with_ws
				string  = ( ' '.join( [ ''.join( speaker ), ''.join( cue ), content ] ) )

			elif str( type( feature ) ) == "<class 'textacy.extract.triples.SSSTriple'>" :		

				# parse and stringify
				entity   = [ token.text_with_ws for token in feature.entity ]
				cue      = [ token.text_with_ws for token in feature.cue ]
				fragment = [ token.text_with_ws for token in feature.fragment ]
				string  = ( ' '.join( [ ''.join( entity ), ''.join( cue ), ''.join( fragment ) ] ) )

			# error
			else :
			
				# get the type of feature, output, and quit
				feature = str( type( feature ) )
				click.echo( f"Error: Unknown value for type of feature { feature }. Call Eric.", err=True )
				exit()

		# do the work
		if ( search( query, string ) ) : filtered.append( feature )

	# done
	return ( filtered )


# output
def outputFeatures( features ) :

	# process each feature
	for feature in features :
			
		# branch accordingly; nouns
		if str( type( feature ) ) == "<class 'spacy.tokens.span.Span'>" : click.echo( feature.text )
		
		# subject-verb-object; svo
		elif str( type( feature ) ) == "<class 'textacy.extract.triples.SVOTriple'>" :
		
			# parse
			subject = [ token.text_with_ws for token in feature.subject ]
			verb    = [ token.text_with_ws for token in feature.verb ]
			object  = [ token.text_with_ws for token in feature.object ]
						
			# output; a bit obtuse
			click.echo( '\t'.join( [ ''.join( subject ), ''.join( verb ), ''.join( object ) ] ) )

		# direct quotes
		elif str( type( feature ) ) == "<class 'textacy.extract.triples.DQTriple'>" :
		
			# parse
			speaker = [ token.text_with_ws for token in feature.speaker ]
			cue     = [ token.text_with_ws for token in feature.cue ]
			content = feature.content.text_with_ws
			
			# output; still a bit obtuse
			click.echo( '\t'.join( [ ''.join( speaker ), ''.join( cue ), content ] ) )
			
		# direct quotes
		elif str( type( feature ) ) == "<class 'textacy.extract.triples.SSSTriple'>" :
		
			# parse
			entity   = [ token.text_with_ws for token in feature.entity ]
			cue      = [ token.text_with_ws for token in feature.cue ]
			fragment = [ token.text_with_ws for token in feature.fragment ]
			
			# output; a bit obtuse some more
			click.echo( '\t'.join( [ ''.join( entity ), ''.join( cue ), ''.join( fragment ) ] ) )
		
		# error
		else :
			
			# get the type of feature, output, and quit
			feature = str( type( feature ) )
			click.echo( f"Error: Unknown value for type of feature { feature }. Call Eric.", err=True )
			exit()


# grammars
@click.command( options_metavar='<options>' )
@click.option('-q', '--query', type=click.STRING, help="filter results using the given regular expression")
@click.option('-n', '--noun',  type=click.STRING, help="only applicable to sss; a noun or noun phrase")
@click.option('-l', '--lemma', default='be', help="only applicable to sss; the lemma of a verb, such as 'be' (default), 'have', or 'say'")
@click.option('-g', '--grammar', default='svo', type=click.Choice( [ 'svo', 'sss', 'nouns', 'quotes' ], case_sensitive=True ), help="the desired grammatical structure")
@click.argument( 'carrel', metavar='<carrel>' )
def grammars( carrel, grammar, query, noun, lemma ) :

	"""Extract sentence fragments from <carrel> where fragments are one of:
	
	\b
	  * nouns - all the nouns and noun chunks
	  * quotes - things people say
	  * svo - fragments in the form of subject-verb-object (the default)
	  * sss - a more advanced version of svo; fragments beginning
	    with an entity, are co-occur with a verb, and are followed
	    by a phrase
	
	This is very useful for the purposes of listing complete ideas from a text.
	
	Examples:
	
	\b
	  * rdr grammars homer
	  * rdr grammars -q horse homer
	  * rdr grammars -g sss -n hector -l have homer"""

	# require
	from textacy import extract
	from os      import system
		
	# sanity check
	checkForCarrel( carrel )

	# initialize
	doc = carrel2doc( carrel )

	# get the features
	if   grammar == 'svo'    : features = list( extract.subject_verb_object_triples( doc ) )
	elif grammar == 'quotes' : features = list( extract.direct_quotations( doc ) )
	elif grammar == 'nouns'  : features = list( extract.noun_chunks( doc ) )
	elif grammar == 'sss'    :

		# sanity check
		if not noun :
		
			click.echo( "Error: When specifying sss, the -n option is required. See 'rdr grammars --help'.", err=True )
			exit()
			
		# do the work
		features = list( extract.semistructured_statements( doc, entity=noun, cue=lemma ) )

	# filter, conditionally
	if query : features = applyFilter( query, features )
	
	# output
	outputFeatures( features )
	

