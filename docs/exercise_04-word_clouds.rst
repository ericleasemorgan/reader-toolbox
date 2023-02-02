Exercise: Word Clouds
=====================

Word clouds are often considered sophmoric, but given the proper context and implemented intelligently, they can be quite informative. Remember, the problem to solve is to communicate a plausible and compelling story. Sometimes a simplistic visualization -- like a word cloud -- perfectly fits the bill.


With the Toolbox
----------------

A number of the Toolbox commands support the generation of word clouds. They include: ent, ngrams, pos, and wrd. More specifically, add both the -c and -w options to ent, ngrams, pos, or wrd, and the Toolbox will output a simple word cloud. Use the -q ("query") or a combination of the -s and -l ("select" and "like") options to refine the illustration. Examples include::

	# normalized and lemmatized nouns from homer
	rdr pos homer -s lemmas -l N -c -n -w 

	# persons from homer
	rdr ent homer -s entity -l PERSON -c -w

	# keywords from homer
	rdr wrd homer -c -w

	# bigrams from homer containing the word horse
	rdr ngrams homer -s 2 -c -q horse -w


With Wordle
-----------

Simple wordcloud
------------------

[INSERT HERE DIRECTIONS HOW TO CREATE A WORDCLOUD WITH PLAIN TEXT FILES.]

Redux
-----

[INSERT HERE DIRECTIONS HOW TO CREATE A WORDCLOUD WITH MORE SOPHISITCIATED FREQUECIES.]


