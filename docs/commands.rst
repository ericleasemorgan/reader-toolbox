Commands in depth
=================

This section describes each Toolbox command in greater detail. They are listed, more or less, in the order they ought to be executed when wanting to do your analysis.

``set``
-------

Use the ``set`` subcommand to tell the Toolbox two things: 1) the location of your locally cached study carrels, and 2) the location of an external tool called MALLET.

By default, the location of your study carrels is set to reader-library in your home directory, but this setting does not take effect until you run ``set``. You can move your collection of carrels anywhere you desire. In fact, you might consider having more than one collection. Just tell the Toolbox which cache you want to use.

When you initially run the ``tm`` command, and if the subsystem called MALLET is not configured, then the Toolbox will download MALLET, save it in your home directory, and automatically update the configuration. Like above, you can move MALLET any where you desire, but you need to tell the Toolbox where it is located. Otherwise, the Toolbox will download an additional copy.


``get``
-------

Use ``get`` to echo the values denoting the location of your local cache of study carrels as well as the location of MALLET. More than anything, this command is used for debugging purposes. 

People using Linux or Macintosh computers can run the following command, and the result will change the working directory to the location of the local cache of study carrels:

  ``cd $(rdr get)``

This makes it easier to manage your collection of study carrels, and it will also make command line completion easier. There is most likely a similar command for Windows computers. I'll give $5 to the first person who tells me what the command is. Really. I promise.


``catalog``
-----------

Use the ``catalog`` subcommand to create lists of study carrels.

By default (``rdr catalog``) will output a very simple list of the locally saved carrels. As your collection grows, you will probably use this version of the subcommand more and more.

When you are just starting out, you will probably want to learn what carrels have been previously created and available for downloading. As of this writing, there are about 3,000 publicly available study carrels. Thus you will use want to use the ``-l`` option to see what carrels exist:

  ``rdr catalog -l remote``
  
The remote list of carrels is formatted as a tab-delimited stream of text with seven fields:

1. name
2. date created
3. keywords
4. number of items
5. number of words
6. average readability score
7. size of compressed carrel measured in bytes

The student, researcher, or scholar can then use their computer's operating sytem functionality to parse, sort, filter, etc, the catalog data. Alternatively, one can use the ``-h`` (human) option. Thus, the catalog data will be formatted and presented in a paged layout. From there a person can navigate and search the list for items of interest. For example, search the result for "love", "war", or "justice" and you will be surprised how many carrels have these words as keywords.

You might also consider outputting the catalog to a file, like this:

  ``rdr catalog -l remote > catalog.tsv``
  
You can then open catalog.tsv in your favorite spreadsheet application and there you can search, filter, and sort.


read
----

browse
------

download
--------

ngrams
------

concordance
-----------

grammars
--------

cluster
-------

tm
--

datasette
---------

play
----




