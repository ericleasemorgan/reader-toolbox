Quick start
===========

This is a quick start for using the Toolbox, sans very much elaboration: ::

  # install
  pip install reader-toolbox --upgrade
  
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
  
  # list all bigrams, count them, and filter the results
  rdr ngrams homer -s 2 -c -q love 
  
  # same as the above, but pipe the result through a pager
  rdr ngrams homer -s 2 -c -q love | more
  
  # search
  rdr concordance homer
    
  # search again, but specify a query
  rdr concordance homer -q war 
    
  # same as the above, but pipe the result through a pager
  rdr concordance homer -q war | more
    
  # list subject-verb-object fragments; please be patient
  rdr grammars homer
  
  # list noun phrases
  rdr grammars homer -g nouns 
  
  # same as the above, but tabulate the results, look for love, and page the results
  rdr grammars homer -g nouns -c -q love | more
  
  # cluster; do the items in the carrel group themselves?
  rdr cluster homer
    
  # topic model; similar to cluster but with more detail
  rdr tm homer
  
  # play hangman
  rdr play
  
  # page through additional carrels for downloading
  rdr catalog -l remote -h
  
  # read a remote study carrel
  rdr read pride -l remote 
  
  # browse the content of a remote study carrel
  rdr browse pride -l remote 

  # download another carrel
  rdr download pride
  
  # download yet another carrel
  rdr download sonnets
  
  # list your carrels
  rdr catalog
    
  # search for love
  rdr concordance pride -q love 

  # find a lot of love
  rdr concordance sonnets -q love 

See  `Tutorial <./tutorial.html>`_ to learn how to use the Toolbox in greater detail.


