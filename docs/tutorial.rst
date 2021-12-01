Tutorial
========

This is a short introduction to some of the Toolbox subcommands. It is not a complete listing of all subcommands, just a few of them to get you started. See `Commands in depth <./commands.html>`_ for more thorough documentation.

Your first command
------------------

The Toolbox is run from the command-line with the command ``rdr``, and the command is made up of many subcommands. List all the subcommands by opening your terminal and entering: ::

  rdr

The result ought to look something like this: ::

  Usage: rdr [OPTIONS] COMMAND [ARGS]...

  Options:
	--help  Show this message and exit.

  Commands:
	adr          Filter email addresses from <carrel>.
	bib          Output rudimentary bibliographics from <carrel>.
	browse       Peruse <carrel> as a file system.
	catalog      List study carrels.
	cluster      Apply dimension reduction to <carrel> and visualize the...
	concordance  A poor mans search engine.
	download     Cache <carrel> from the public library of study carrels.
	edit         Modify the stop word list of <carrel>.
	ent          Filter out named entities and types of entities found in...
	get          Echo the values denoted by the set subcommand.
	grammars     Extract sentence fragments from <carrel> where fragments are...
	info         Output metadata describing <carrel>.
	ngrams       Output and list words or phrases found in <carrel>.
	play         Play the word game called hangman.
	pos          Filter out parts-of-speech, words, and lemmas found in...
	read         Open <carrel> in your Web browser.
	search       Perform a full text query against <carrel>.
	semantics    Apply semantic indexing against <carrel>.
	set          Configure the location of study carrels and a subsystem...
	sql          Use SQL queries against the database of <carrel>.
	tm           Apply topic modeling against <carrel>.
	url          Filter URLs and domains from <carrel>.
	wrd          Filter statistically computed keywords from <carrel>.

To output details regarding a subcommand append ``--help``, for example: ::

  rdr ngrams --help


List words
----------

List of all the words (unigrams) from a study carrel in the remote library: ::

  rdr ngrams -l remote homer

Do the same thing, but this time request bigrams (two-word phrases): ::

  rdr ngrams -l remote -s 2 homer

There are many more options, including the ability to count and tabulate the results, filter (query) the results using regular expressions, and more importantly, apply these same techniques to study carrels saved locally.


Browse the public library
-------------------------

There are about 3,000 previously created and freely available study carrels available for downloading. To page through a human-readable list of them enter: ::

  rdr catalog -l remote -h

The raw, unprocessed listing of remote study carrels is a tab-delimited stream, and consequently the previous command, sans the ``-h`` option, is very amenable to post-processing. For example, pipe the results to a pager: ::

  rdr catalog -l remote | more

Or save the results to a file: ::

  rdr catalog -l remote > catalog.tsv


Build your library
------------------

When you create a local collection of study carrels -- your library, then there are many more things you can do. To configure the location of your local collection, use the ``set`` command, and you will be prompted for the name of a folder/directory: ::

  rdr set local

Now you can download a study carrel from the remote library and add it to your local collection: ::

  rdr download homer

Add a couple more items to your local collection: ::

  rdr download sonnets
  rdr download pride
  
You can now list the study carrels in your local collection: ::

  rdr catalog

List words, revisited
---------------------

Now that you have created a local library, you can apply the ``ngrams`` function to them with any of the following commands: ::

  # all unigrams
  rdr ngrams homer
  
  # all bigrams
  rdr ngrams -s2 homer
  
  # count and tabulate bigrams
  rdr ngrams -s 2 -c homer | more
  
  # just like above, but filter with the word "love"
  rdr ngrams -s 2 -c -q love homer | more
  

Search
------

Once you have identified words or ngrams of interest, you use a concordance (a poor man's search engine) to see how the words are used within the context of a study carrel. For example: ::

  rdr concordance homer -q horse
  
The ``-q`` option can also be a phrase: ::

  rdr concordance homer -q 'fleet horses'


List sentence-like phrases
--------------------------

Many times sentences are written using well-understood grammars, and it is easy to extract sentence fragments matching those grammars. For example, to extract all the fragments whose sentences are in the form of subject-verb-object, enter: ::

  rdr grammars homer

(In order to use this function, you may need to install a language model, and if you do, then you will be asked to do so, but you will only have to do it once. Moreover, the given carrel will need to be modeled, and that only has to be done once as well.)

You can also list the noun phrases in a carrel: ::

  rdr grammars -g nouns homer
  
You can also count such things: ::

  rdr grammars -g nouns -c homer

The list of grammars may be long, so you might want to pipe the result through a pager: ::

  rdr grammars -g nouns -c homer | more


Next steps
----------

Now that you have gotten this far, see `Commands in depth <./commands.html>`_ for a complete listing of all the commands and how to use them.

Happy reading!



