Installation
============

The Reader Toolbox is a suite of Python scripts integrated into a single command-line interface. It ought to run on any computer with Python 3 or above installed. From the command line, installation is as simple as: ::

  pip install reader-toolbox --upgrade

Once you get this far, you ought to be able to run the Toolbox command -- ``rdr`` -- which is short for "reader": ::

  rdr

The result ought to be listing of all the ``rdr`` subcommands and looking something like this: ::

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

From here you can issue a subcommand like the following to display a human-readable catalog of all the Distant Reader study carrels remotely available in the Reader's public library: ::

  rdr catalog -h -l remote

See  `Quick start <./quick-start.html>`_ to learn more about the subcommands.
