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

People using Linux or Macintosh computers can run the following command, and the result will change the working directory to the location of the local cache of study carrels: ::

  # change directories to local collection of carrels
  cd $(rdr get)

This makes it easier to manage your collection of study carrels, and it will also make command line completion easier. There is most likely a similar command for Windows computers. I'll give $5 to the first person who tells me what the command is. Really. I promise.


``catalog``
-----------

Use the ``catalog`` subcommand to create lists of study carrels.

By default this subcommand will output a very simple list of the locally saved carrels: ::

  rdr catalog

As your collection grows, you will probably use this version of the subcommand more and more often.

When you are just starting out, you will probably want to learn what carrels have been previously created and available for downloading. As of this writing, there are about 3,000 publicly items. Thus, you will use want to use the ``-l`` option to see what carrels exist: ::

  rdr catalog -l remote
  
The remote list of carrels is returned as a tab-delimited stream of text with seven fields:

1. name
2. date created
3. keywords
4. number of items
5. number of words
6. average readability score
7. size of compressed carrel measured in bytes

The student, researcher, or scholar can then use their computer's operating sytem functionality to parse, sort, filter, etc, the catalog data. For example: ::

  rdr catalog -l remote | cut -f1,3 | grep love | less -x42 -S

Alternatively, one can use the ``-h`` (human) option. Thus, the catalog data will be formatted and presented in a paged layout. From there a person can navigate and search the list for items of interest. For example, search the result for "love", "war", or "justice" and you will be surprised how many carrels have these words as keywords. Try: ::

  rdr catalog -l remote -h

Finally, you might also consider outputting the catalog to a file, like this: ::

  rdr catalog -l remote > catalog.tsv
  
You can then open catalog.tsv in your favorite spreadsheet application and from there you can search, filter, and sort.


``read``
--------

Use the ``read`` subcommand to look through and peruse the contents of a local or remote study carrel. Two examples include: ::

  rdr read homer
  rdr read -l remote homer

Study carrels are data sets. A subset of the datasets are HTML files intended for traditional reading purpose. These HTML files are narrative in nature but there are a number of interactive tables as well. The use of the ``read`` subcommand is a great way to become familiar with a study carrel's provenance, breadth, depth, and content. 


``browse``
----------

The ``browse`` subcommand is very similar ``read`` but the view of the study carrel is more akin to perusing a computer's directory structure. Using the ``browse`` command against a remote study carrel returns a manifest, a sort of directory listing. For example: ::

  rdr browse -l remote homer

Using the ``browse`` on a carrel in your local collection is facilitated through a terminal-based Web browser called Lynx. Don't laugh. Lynx is full-fledged browser. It just does not support Javascript. There are many things Lynx can do that Chrome, Safari, or FireFox can not. For example, it can open files with non-standard file extension, such as pos, ent, or wrd.

If you do not have Lynx installed, then consider using your computer's native tools to browse your collection. Remember, 99% of the files in a study carrel are plain text files, and you can open them in your word processor, text editor, spreadsheet, or database program.

When doing your analysis, it is very important to become familiar with your data. The purposes of ``read`` and ``browse`` are complementary, and they go a long way to helping you answer your research questions.


``download``
------------

The ``download`` command is used to cache a study carrel from the public collection to your local computer. Begin by using variations of the ``catalog`` command to identify the name of a study carrel of interest. And then use the ``download`` command: ::

  rdr download homer

If you have not configured the Toolbox to denote the location of your local cache, then this operation will gracefully fail. You will then be prompted to make the configuration.

Unlike traditional libraries, once you check something out of the Reader's library, you do not have to return it. :)


ngrams
------

This is one of the strongest subcommands in the Toolbox. Use it to comprehend the breadth, depth, and scope of a carrel. Begin by simply giving the subcommand the name of a carrel, and the result will be a stream of all the words in the carrel, sans stopwords: ::

  rdr ngrams homer

You can do the same thing but this time, you can use the ``-s`` option to denote the size of the ngram, for example, two-word phrases: ::

  rdr ngrams -s 2 homer
  
If you specify a size greater than 2, then stop words will not be removed:

  rdr ngrams -s 3 homer
  
At this point, you may want to redirect the output of ngrams to a file, and then use another application for further analysis. For example, save the result as a file named bigrams.tsv, and then open bigrams.tsv in your spreadsheet application for filtering and purposes: ::

  rdr ngrams -s 2 homer > bigrams.tsv
  

concordance
-----------

grammars
--------

cluster
-------

tm
--

sql
---

play
----




