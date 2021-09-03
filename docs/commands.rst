Commands in depth
=================

This section describes each Toolbox command in greater detail. They are listed, more or less, in the order they ought to be executed when wanting to do your analysis.

set
---

Use the ``set`` subcommand to tell the Toolbox two things: 1) the location of your locally cached study carrels, and 2) the location of an external tool called MALLET. For example, to set the location of your local cache of study carrels, enter: ::

  rdr set local

By default, the location of your study carrels is set to ``reader-library`` in your home directory, but this setting does not take effect until you run ``set``. You can move your collection of carrels anywhere you desire. In fact, you might consider having more than one collection. Just tell the Toolbox which cache you want to use.

When you initially run the ``tm`` command, and if the subsystem called MALLET is not configured, then the Toolbox will download MALLET, save it in your home directory, and automatically update the configuration. Like above, you can move MALLET any where you desire, but you need to tell the Toolbox where it is located: ::

  rdr set mallet


get
---

Use ``get`` to echo the values denoting the location of your local cache of study carrels as well as the location of MALLET. More than anything, this command is used for debugging purposes. 

People using Linux or Macintosh computers can run the following command, and the result will change the working directory to the location of the local cache of study carrels: ::

  # change directories to local collection of carrels
  cd $(rdr get)

This makes it easier to manage your local collection, and it will also make command line completion easier. There is most likely a similar command for people using Windows computers, and I will give $5 to the first person who tells me what the command is. Really. I promise.


catalog
-------

Use the ``catalog`` subcommand to list study carrels.

By default this subcommand will output a very simple list of the locally saved carrels: ::

  rdr catalog

As your collection grows, you will probably use this version of the subcommand more and more often.

When you are just starting out, you will probably want to learn what carrels have been previously created and available for downloading. As of this writing, there are about 3,000 publicly available items. Thus, you will use want to use the ``-l`` option to see what carrels exist: ::

  rdr catalog -l remote
  
The remote list of carrels is returned as a tab-delimited stream of text with seven columns:

1. name
2. date created
3. keywords
4. number of items
5. number of words
6. average readability score
7. size of compressed carrel measured in bytes

The student, researcher, or scholar can then use their computer's operating sytem functionality to parse, sort, filter, etc, the catalog data. For example, the following may work for you: ::

  rdr catalog -l remote | cut -f1,3 | grep love | less -x42 -S

Alternatively, one can use the ``-h`` (human) option. Thus, the catalog data will be formatted and presented in a paged layout. From there a person can navigate and search the list for items of interest. For example, search the result for "love", "war", or "justice" and you will be surprised how many carrels have these words as keywords. Try: ::

  rdr catalog -l remote -h

Finally, you might also consider outputting the catalog to a file, like this: ::

  rdr catalog -l remote > catalog.tsv
  
You can then open ``catalog.tsv`` in your favorite spreadsheet application and from there you can search, filter, sort, and group.


read
----

Use the ``read`` subcommand to look through and peruse the contents of a local or remote study carrel. Two examples include: ::

  rdr read homer
  rdr read -l remote homer

Study carrels are data sets. A subset of the datasets are HTML files intended for traditional reading purposes. These HTML files are narrative in nature but there are a number of interactive tables as well. The use of the ``read`` subcommand is a great way to become familiar with a study carrel's provenance, breadth, depth, and content. 


browse
------

The ``browse`` subcommand is very similar to ``read`` but the view of the study carrel is more akin to perusing a computer's directory structure. Using the ``browse`` command against a remote study carrel returns a manifest, a sort of directory listing. For example: ::

  rdr browse -l remote homer

Using ``browse`` on a carrel in your local collection is facilitated through a terminal-based Web browser called Lynx. Don't laugh. Lynx is full-fledged browser. It just does not support Javascript. There are many things Lynx can do that Chrome, Safari, nor FireFox can. For example, it can open files with non-standard file extensions, such as pos, ent, or wrd.

If you do not have Lynx installed, then consider using your computer's native tools to browse your collection. Remember, 99% of the files in a study carrel are plain text files, and you can open them in your word processor, text editor, spreadsheet, or database program.

When doing your analysis, it is very important to become familiar with your data. The purposes of ``read`` and ``browse`` are complementary, and they go a long way to helping you answer your research questions.


download
--------

The ``download`` command is used to cache a study carrel from the public collection to your local computer. Begin by using variations of the ``catalog`` command to identify the name of a study carrel of interest. And then use the ``download`` command: ::

  rdr download homer

If you have not configured the Toolbox to denote the location of your local cache, then this operation will gracefully fail. You will then be prompted to make the configuration.

Unlike traditional libraries, once you check something out of the Reader's library, you do not have to return it. :)


ngrams
------

This is one of the strongest subcommands in the Toolbox. Use it to comprehend the breadth, depth, and scope of a carrel. Begin by simply giving ``ngrams`` the name of a carrel, and the result will be a stream of all the words in the carrel, sans stopwords: ::

  rdr ngrams homer

You can do the same thing but this time, you can use the ``-s`` option to denote the size of the ngram, for example, two-word phrases: ::

  rdr ngrams -s 2 homer
  
If you specify a size greater than 2, then stop words will not be removed: ::

  rdr ngrams -s 3 homer
  
At this point, you may want to redirect the output of ngrams to a file, and then use another application for further analysis. For example, save the result to a file named ``bigrams.tsv``, and then open ``bigrams.tsv`` in your spreadsheet application for searching, sorting, and grouping purposes: ::

  rdr ngrams -s 2 homer > bigrams.tsv
  
It is possible to query (filter) the results of the ``ngrams`` subcommand with the ``-q`` option. Queries are expected to be regular expressions so the results of the following command will be a list of all bigrams containing the characters l-o-v-e: ::

  rdr ngrams -s 2 -q love homer
  
You might enhance the query to return all bigrams beginning with the characters l-o-v-e: ::
  
  rdr ngrams -s 2 -q "^love" homer

Or only the bigrams beginning with the word "love": ::

  rdr ngrams -s 2 -q "^love\b" homer

The student, researcher, or scholar will often want to count the occurances of ngrams, and that is what the ``-c`` option is for. For example, to count and tabulate the most frequent unigrams in a carrel you can: ::

  rdr ngrams -c homer

You can probably pipe the results through to an operating system utility called "more" in order to page through the results: ::

  rdr ngrams -c homer | more

Do the same thing but with bigrams: ::

  rdr ngrams -c -s 2 homer | more
  
Or list the most frequent bigrams containing the letters l-o-v-e: ::

  rdr ngrams -c -s 2 -q love homer | more

At this point you may want to redirect the output to a file, and then, again, use another application to do additional analysis. For example, find all bigrams containing l-o-v-e, redirect the output to a file, and then import the result into a network analysis program (like Gephi) to illustrate relationships: ::

  rdr ngrams -s 2 -q love homer > love.tsv
  
Finally, ``ngrams`` filters results using a stop word list contained in very study carrel. The given stop word list may be too restrictive or not restrictive enough. That is what the ``edit`` subcommand is for; the ``edit`` subcommand makes it easy to modify a carrel's stop word list, and consequently make the output of ``ngrams`` more meaningful. See the section on ``edit`` for more detail.

edit
----


concordance
-----------

Developed in the 13th century, concordances are the oldest form of text mining, and now-a-days they are often called keyword-in-context (KWIC) indexes. Concordances are the poor man's search engine. 

Use ``concordance`` to see what words are used in the same breath as a given word. Used without any options, the ``concordance`` tool will query the given carrel for the word "love", and the result will be a number of lines where each line contains about 40 characters prior to the word "love", the word "love", and about 40 characters after the word "love": ::

  rdr concordance homer
  
You can query (filter) the results with the ``-q`` option, and the query must be a word for phrase, not a regular expression. Thus, the following command is identical to the default: ::

  rdr concordance -q love homer

Alternatively, the query can be a phrase, and it is often interesting to associate a noun with a verb, such as: ::

  rdr concordance -q "war is" homer

Or: ::

  rdr concordance -q "hector had" homer

By default, ``concordance`` will output as many 999 lines. Using the ``-l`` option you can configure the number of lines. For example, to output only 5 lines, try: ::

  rdr concordance -l 5 homer
  
You can also configure the size of each line's width -- the number of characters on either side of the query. To see very short snippets, try: ::

  rdr concordance -w 24 homer

It is useful to first exploit the ``ngrams`` command to identify words or phrases of interest, then use the results as input for the ``concordance`` command.

Like many of the other subcommands, the output of ``concordance`` is designed to be used by other applications or tools. Moreover, a word is often known by the company it keeps. Output the results of ``concordance`` to a file, and then use the file as input to a wordcloud tool (like Wordle) to visualize the results: ::

  rdr concordance homer > homer.txt
  
Initially, the cloud will be dominated by the value of ``-q``, but you can use your text editor to find/replace the query with nothingness. The visualization will be quite insightful, I promise.


cluster
-------

Use the ``cluster`` subcommand to get an idea of a given carrel's homogeneity. 

The Toolbox supports two types of clustering. The first (and default) is ``dendrogram`` where the underlying algorithm will reduce the carrel to two dimensions and plot them as a dendrogram. For example: ::

  rdr cluster homer

The following command is equivalent: ::

  rdr cluster -t dendrogram homer

The second type of clustering (``cube``) reduces the carrel to three dimensions and plots the results: ::

  rdr cluster -t cube homer

If your carrel contains sets of journal articles, all of the chapters of a given book, or all the works by a given author, then the ``cluster`` subcommand may give you a good idea of how each item in your carrel is related to every other item. It is quite likely you will observe patterns. The ``cluster`` subcommand is also useful when using the ``tm`` (topic modeling) subcommand, because ``cluster`` will give you an idea of how many latent themes may exist in a carrel. On the other hand, if your carrel contains too many items (say, a few hundred), then the result will most likely not be very readable.


tm
--

Use this subcommand to do topic modeling.

Topic modeling is an unsupervised machine learning process used to enumerate latent themes in a corpora. The process is every useful for denoting the aboutness of a study carrel; it is useful for answering the question, "What N things is the carrel about, and how might each N thing be described?" But be forewarned, there is no absolutely correct value for N. After all, how many N things is the sum of Shakespeare's works about?

This subcommand builds on the good work of three different subsystems. The first is the venerable MALLET system. If the Toolbox has not been configured to know the location of MALLET on your computer, then the Toolbox will download MALLET, and update your configurations accordingly. The second is Gensim, a Python library which includes a front-end to MALLET. The third is pyLDAvis which takes the output of MALLET to visualize the results.

When using the ``tm`` command, start with a small number of topics, say seven, which is the default: ::

  rdr tm homer

If there are many overlapping circles in the results, then consider reducing the number of topics: ::

  rdr tm homer -t 5

Many people find topic modeling to be confusing, and this is because they specify too many words to denote a topic. By default, the Toolbox uses seven words to describe each topic, but increasing the number may prove to be more illuminating: ::

  rdr tm homer -t 5 -w 24

If you observe words in the output which you deem as useless, then consider using the ``edit`` subcommand to denote those words as stop words. When running ``tm`` again, those words ought not be in the output.

The larger the study carrel, the more important it is to allow the underlying subsystems to iterate over the corpus. The results ought to be more accurate. For smaller carrels, such as a single book, then the default (2400 iterations) is probably good enough, but for a larger carrel, then twice as many iterations or more may be in order. For example: ::

  rdr tm homer -t 5 -w 24 -i 4800

Knowing the correct value for ``-i`` is determined by the size of your carrel, the size of your computer, and your patience.


grammars
--------

Langauges follow patterns, and these patterns are called grammars. Through the use of machine learning computing techniques, it is possible to apply grammars to a text and extract matching sentence fragments. The results are more meaningful than simple ngram and concordance outputs because the patterns (grammars) assume relationships between words, not mere frequencies nor proximities.

In order to exploit grammars, a specific language model must be installed, and if it has not been installed, then the Toolbox will do so. Moreover, applying the model to the carrel can be a time consuming process, and the Toolbox will do this work, if it has not already been done.

The Toolbox supports four different grammars. The first is subject-verb-object (svo) -- rudimentary sentences.  To extract svo-like fragments from a given study carrel, enter: ::

  rdr grammars homer

The result is usually lengthy, and consequently you may want to pipe the results through to a pager such as "more": ::

  rdr grammars homer | more
  
The default grammar (svo) can be explicitly articulated on the command line: ::

  rdr grammars -g svo homer
  
The other three grammars include:

1. ``nouns`` - all nouns and noun chunks
2. ``quotes`` - things people say
3. ``sss`` - semi-structured sentences; this is the most complicated grammar

To list all the nouns and noun chunks in a carrel, enter: ::

  rdr grammars -g nouns homer

To list all the direct quotes in a carrel, enter: ::

  rdr grammars -g quotes homer
  
Semi-structured sentences (sss) are the most complicated grammar, and it requires at least one additional option, ``-n`` where the value is some sort of noun. This grammar includes an optional option, ``-l`` for the lemma of a verb. By default, the value of ``-l`` is the lemma "be". Thus, to list all sentence fragments where the subject of the sentences is "war", and the predicate is a form of "be", enter: ::

  rdr grammars -g sss -n war homer

The following command is equivalent: ::

  rdr grammars -g sss -n war -l be homer
  
Using the semi-structured grammars is sometimes more accurate than filtering concordances. For example, in Homer's works, one can ask, "What are horses?" ::

  rdr grammars -g sss -n horses -l be homer

Using the ``-q`` option, the student, researcher, or scholar can filter the output of ``grammars``. Like most of the other filters, this one takes a regular expression as an argument. Thus, to filter the ``svo`` option with the letters l-o-v-e, try: ::

  rdr grammars -g svo -q love homer
  
The same thing can be quite useful when it comes to the ``noun`` grammar: ::

  rdr grammars -g nouns -q love homer
  
As well as the ``quotes`` grammar: ::

  rdr grammars -g quotes -q love homer

Use the ``-s`` and ``-c`` options to make the output more meaningful. The ``-s`` option sorts the results alphabetically, and by doing so, patterns may emerge. For example: ::

 rdr grammars -s homer | more
 
Similarly, the ``-c`` option counts and tabulates the results, and this is quite useful for determining what nouns and noun phrases are frequently mentioned in a carrel: ::

  rdr grammars -g nouns -c homer | more
  

sql
---

This subcommand launches a subsystem called Datasette, and through its use the student, researcher, or scholar can easily query the given carrel's underlying SQLite relational database file.

The underlying database's structure is defined in each carrel's ``etc/reader.sql`` file, and the database is essentially a distillation of all the content found in the ``adr``, ``bib``, ``ent``, ``pos``, ``urls``, and ``wrd`` directories of each carrel. Thus, the database includes email addresses, bibliographics, named-entities, parts-of-speech, URLs, and statistically significant keywords extracted from each and every text-based file found in the carrel's ``cache`` directory.

Given this database, it is possible to exact all sorts of information through the use of SQL (structured query language). For example, begin to work with the carrel named homer: ::

  rdr sql homer

Then query the database in a number of different ways: ::

  -- list all identifiers
  SELECT id FROM bib;
  
  -- count & tabulate the keywords
  SELECT COUNT( keyword ) AS c, keyword FROM wrd GROUP BY keyword ORDER BY c DESC;
  
  -- list all items "about" Trojans; notice whence each book comes
  SELECT b.id FROM bib AS b, wrd AS w WHERE w.keyword IS 'Trojans' AND b.id IS w.id;
  
  -- list all items "about" Ulysses; again, notice whence each book comes; what does that tell you about the books?
  SELECT b.id FROM bib AS b, wrd AS w WHERE w.keyword IS 'Ulysses' AND b.id IS w.id;
  
  -- create a rudimentary bibliography
  SELECT b.id, GROUP_CONCAT( w.keyword, '; ' ) AS keywords, b.summary FROM bib AS b, wrd AS w WHERE b.id = w.id GROUP BY b.id ORDER BY b.id;

  -- count & tabulate the people
  SELECT COUNT( entity ) AS c, entity FROM ent WHERE type IS 'PERSON' GROUP BY entity ORDER BY c DESC;

  -- count & tabulate the locations
  SELECT COUNT( entity ) AS c, entity FROM ent WHERE type IS 'LOC' GROUP BY entity ORDER BY c DESC;

  -- list all the verbs
  -- what do things do, and in any carrel the vast majority of time it is always about being and having
  SELECT COUNT( lemma ) AS c, lemma FROM pos WHERE pos LIKE 'V%' GROUP BY lemma ORDER BY c DESC;

  -- list all the nouns; what things exist?
  SELECT COUNT( LOWER( lemma ) ) AS c, LOWER( lemma ) FROM pos WHERE pos LIKE 'N%' GROUP BY LOWER( lemma ) ORDER BY c DESC;

  -- list all the adjectives; how are things described?
  SELECT COUNT( LOWER( lemma ) ) AS c, LOWER( lemma ) FROM pos WHERE pos LIKE 'J%' GROUP BY LOWER( lemma ) ORDER BY c DESC;

The different types of queries are almost limitless, and the key to using the database is less about knowing SQL and more about being able to articulate the type of information one wants to extract. 

For more ideas of how to exploit the database see ``etc/queries.sql`` found in every study carrel. That file is used to create ``etc/report.txt``.


play
----

Use this subcommand to play hangman. It is that simple. 

