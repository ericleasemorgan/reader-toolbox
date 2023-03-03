Exercise: Searching
=====================

Concordancing
-------------

The Toolbox supports rudimentary concordancing, but from the shell, there are a number of ways to quickly and easily extract meaning. For example, the student, researcher, or scholar might output rudimentary definintions of a given person::

	rdr concordance homer -q 'hector is|hector was' -w 60 | sed "s/^.*hector is|hector was//" | sort
	
Advanced concordancing
----------------------

A graphical-user interface (GUI) concordance application -- callled AntConc -- is easier to use than the Reader's concordance application and it supports more functionality than the Toolbox's interface.


Full text searching
-------------------

The Toolbox full-text searching via the search subcommand.


SQL
---

Just about all the content of a study carrel -- full text content, parts-of-speech, URLs, addresses, named-entities, etc. -- has been reduced to an SQLite relational database file (./etc/reader.db) with the following structure:

[INSERT STRUCTURE HERE.]

Using any SQLite client, one ought to be able to query the database to output more refined and specialized reports. 

