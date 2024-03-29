

# Distant Reader Toolbox

A command-line interface for creating and interacting with [Distant Reader](https://distantreader.org) study carrels


## Installation

```
  pip install reader-toolbox
```

## Quick start

```  
  # configure; accept the default
 rdr set -s local

  # add an item to your library
  rdr download homer

  # read homer
  rdr read homer

  # list all words
  rdr ngrams homer

  # list all bigrams
  rdr ngrams homer -s 2

  # list all bigrams and count them
  rdr ngrams homer -s 2 -c

  # search
  rdr concordance homer

  # search again, but specify a query
  rdr concordance homer -q war

  # list subject-verb-object fragments; please be patient
  rdr grammars homer

  # list noun phrases
  rdr grammars homer -g nouns

  # cluster; do the items in the carrel group themselves?
  rdr cluster homer

  # topic model; similar to cluster but with more detail
  rdr tm homer

  # page through additional carrels for downloading
  rdr catalog -l remote -h

  # download another carrel
  rdr download pride

  # download yet another carrel
  rdr download sonnets

  # list your carrels
  rdr catalog
```

## Description and background

The Reader Toolbox -- run from the command-line as ``rdr`` -- is designed to create and interact with Distant Reader study carrels. Using the Toolbox you can do things such as but not limited to:

   * search and browse the collection of more than 3,000 publicly available study carrels
   * download study carrels from the public collection and add them to your own collection
   * count & tabulate the most frequent ngrams (one-word, two-word, etc. phrases) occurring in study carrels
   * apply concordancing (keyword-in-context searching) against study carrels
   * apply topic modeling (extracting latent themes) against study carrels
   * extract information from your study carrels matching specific grammars
   * create your own study carrels
   * and more

In the end, the Toolbox empowers you to read, use, and understand large volumes of text quickly and easily.

## Links

   * download: [https://pypi.org/project/reader-toolbox](https://pypi.org/project/reader-toolbox)
   * documentation: [https://reader-toolbox.readthedocs.io](https://reader-toolbox.readthedocs.io)
   * source code: [https://github.com/ericleasemorgan/reader-toolbox](https://github.com/ericleasemorgan/reader-toolbox)
   * bug tracker: [https://github.com/ericleasemorgan/reader-toolbox/issues](https://github.com/ericleasemorgan/reader-toolbox/issues)

---
Eric Lease Morgan &lt;emorgan@nd.edu&gt;  
January 5, 2023
