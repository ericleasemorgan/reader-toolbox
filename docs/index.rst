.. reader-toolbox documentation master file, created by
   sphinx-quickstart on Sun Aug 15 09:31:46 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Distant Reader Toolbox
**********************

A command-line tool for interacting with Distant Reader study carrels

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Quick start
===========

The Toolbox is run from the command-line with the command 'rdr', and the command is made up of many subcommands. To list all Toolbox subcommands open your terminal and enter: ::

  rdr

The result ought to look something like this: ::

  Usage: rdr [OPTIONS] COMMAND [ARGS]...

  Options:
	--help  Show this message and exit.

  Commands:
	browse       Use a Web browser called Lynx to peruse <carrel> Study...
	catalog      List the items in a library where <location> is either...
	cluster      Apply dimension reduction to <carrel> and visualize where...
	concordance  Output matching lines from <carrel> where <query> is a word...
	datasette    Use Datasette to query <carrel>'s database Datasette is an...
	download     Download <carrel> from the public library of study carrels A...
	get          Echo the full path to your local library of study carrels...
	grammars     Extract grammatical sentence fragments from <carrel> where...
	ngrams       Output ngrams of the given <size> from <carrel>
	play         Play a game
	read         Open <carrel> in your default Web browser where the location...
	set          Set the location of various items
	tm           Apply topic modeling against <carrel> Topic modeling is the...

To output the help text for any command append '--help' to any command, for example: ::

  rdr ngrams --help


Ngrams
------

List of all the words (unigrams) from a study carrel in the remote library: ::

  rdr ngrams -l remote author-homer-gutenberg

Do the same thing, but this time request bigrams (two-word phrases) ::

  rdr ngrams -l remote -s 2 author-homer-gutenberg

There are many more options, including the ability to count and tabulate the results, filter (query) the results using regular expressions, and apply these same techniques to study carrels saved locally.


Public library
--------------

There are about 3,000 previously created and freely available study carrels available for downloading. To page through a human-readable list of them enter: ::

  rdr catalog -l remote -h

The raw, unprocessed listing of remote study carrels is a tab-delimited stream, and consequently the previous command, sans the -h option, is very amenable to post-processing. For more detail, see the Tutorials.


Local library
-------------

If you create a local collection of study carrels, then there are many more things you can do. To configure the location of your local collection, use the 'set' command, and you will be prompted for the name of a folder/directory: ::

  rdr set local

Now you can download a study carrel from the remote library and add it to your local collection: ::

  rdr download author-homer-gutenberg

You can now list the study carrels in your local collection: ::

  rdr catalog


Concordancing, the poor man's search engine
-------------------------------------------

Once you have identified words or ngrams of interest, you use a concordance (a poor man's search engine) to see how the words are used within the context of a study carrel. For example: ::

  rdr concordance author-homer-gutenberg -q horse
  
The -q option can also be a phrase: ::

  rdr concordance author-homer-gutenberg -q 'fleet horses'


Grammars
--------

When sentences are constructed using well-defined grammars, it is easy to extract sentence fragments matching those grammars. For example, to extract all the sentence fragments whose sentences are in the form of subject-verb-object, enter the following command. In order to use this function, you may need to install a language model, and if you do, then you will be asked to do so: ::

  rdr grammars author-homer-gutenberg svo

There are many more grammars availble in the Toolbox.

Next steps
----------

This was only an introduction to the Reader Toolbox. Please see the Tutorials for more detail.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
