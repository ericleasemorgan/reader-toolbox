Quick start
===========

The Toolbox is run from the command-line with the command ``rdr``, and the command is made up of many subcommands.

Your first command
------------------

List all Toolbox subcommands by opening your terminal and entering: ::

  rdr

The result ought to look something like this: ::

  Usage: rdr [OPTIONS] COMMAND [ARGS]...

  Options:
	--help  Show this message and exit.

  Commands:
	browse       Peruse <carrel> as a file system Study carrels are sets of...
	catalog      List study carrels Use this command to enumerate the study...
	cluster      Apply dimension reduction to <carrel> and visualize the...
	concordance  A poor man's search engine Given a query, this subcommand...
	download     Download <carrel> from the public library of study carrels A...
	edit         Edit <carrel>'s stopword list When using subcommands such as...
	get          Echo the values denoted by the set subcommand This is useful...
	grammars     Extract sentence fragments from <carrel> where fragments are...
	ngrams       Given <carrel>, output ngrams Examples: * rdr ngrams homer...
	play         Play the word game called hangman.
	read         Open <carrel> in your default Web browser where the location...
	set          Set the location of various items
	sql          Use Datasette to query <carrel>'s database Datasette is an...
	tm           Apply topic modeling against <carrel> Topic modeling is the...

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


Create your library
-------------------

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
