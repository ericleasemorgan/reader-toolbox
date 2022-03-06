
# grammars - output different types of features found in a text

# require
from rdr import *



# given a carrel, return a spacy doc
def carrel2doc( carrel ) :

	# configure
	PICKLE = 'reader.spacy'

	# require
	from os        import path, stat
	from spacy     import load
	import                textacy
	
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
	
	# require
	from textacy import extract
	from os      import system
	from re      import search
	
	# sanity check
	checkForCarrel( carrel )

	# initialize
	doc = carrel2doc( carrel )

	# get the features; svo
	if grammar == 'svo' :
	
		# do the work
		features = list( extract.subject_verb_object_triples( doc ) )
		
		# simplify the result
		items = []
		for feature in features :
		
			#print( help(feature ) )
			#exit()

			subject = feature.subject[ 0 ].text			
			verb    = feature.verb[ 0 ].text
			object  = feature.object[ 0 ].text
			items.append(' \t'.join( [ ''.join( subject ), ''.join( verb ), ''.join( object ) ] ) )

		# done
		features = items
		
	# quotes
	elif grammar == 'quotes' :
	
		# do the work
		features = list( extract.direct_quotations( doc ) )
		
		# simplify the result
		items = []
		for feature in features :
		
			# parse and stringify
			speaker = [ token.text for token in feature.speaker ]
			cue     = [ token.text for token in feature.cue ]
			content = feature.content.text
			items.append( '\t'.join( [ ''.join( speaker ), ''.join( cue ), content ] ) )

		# done
		features = items

	# noun chunks
	elif grammar == 'nouns' :
	
		# do the work and simplify the result
		features = list( extract.noun_chunks( doc ) )
		features = [ feature.text for feature in features ]
		
	# semi-structured sentences
	elif grammar == 'sss' :

		# sanity check
		if not noun :
		
			click.echo( "Error: When specifying sss, the -n option is required. See 'rdr grammars --help'.", err=True )
			exit()
			
		# do the work
		features = list( extract.semistructured_statements( doc, entity=noun, cue=lemma ) )

		# simplify the result
		items = []
		for feature in features :
		
			entity   = [ token.text for token in feature.entity ]
			cue      = [ token.text for token in feature.cue ]
			fragment = [ token.text for token in feature.fragment ]
			items.append( '\t'.join( [ ''.join( entity ), ''.join( cue ), ' '.join( fragment ) ] ) )

		# done
		features = items

	# filter, conditionally
	if query : features = [ feature for feature in features if ( search( query, feature ) ) ]
	
	# sort, conditionally
	if sort : features.sort()
	
	# count, conditionally
	if count :
	
		# initialize a dictionary and process each feature
		items = {}
		for feature in features :

			# update the dictionary
			if feature in items : items[ feature ] += 1
			else                : items[ feature ]  = 1

		# sort the dictionary; return the features
		features = sorted( items.items(), key=lambda x:x[ 1 ], reverse=True )
		
		# process each feature, again
		items = []
		for feature in features :
			
			# create a record and update
			record = str( feature[ 1 ] ) + '\t' + feature[ 0 ]
			items.append( record )
		
		# done
		features = items
	
	# output
	for feature in features : click.echo( feature )
	

