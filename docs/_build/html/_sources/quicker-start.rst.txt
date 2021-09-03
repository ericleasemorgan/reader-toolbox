Quicker start
=============

Here is a quicker start, sans much elaboration: ::

  # install
  pip install reader-toolbox --upgrade
  
  # configure; accept the default
  rdr set local
  
  # add an item to your library
  rdr download homer
  
  # read homer
  rdr read homer

  # list all words
  rdr ngrams homer
  
  # list all bigrams
  rdr ngrams -s 2 homer
  
  # list all bigrams and count them
  rdr ngrams -s 2 -c homer
  
  # list all bigrams, count them, and filter the results
  rdr ngrams -s 2 -c -q love homer
  
  # same as the above, but pipe the result through a pager
  rdr ngrams -s 2 -c -q love homer | more
  
  # search
  rdr concordance homer
    
  # search again, but specify a query
  rdr concordance -q war homer
    
  # same as the above, but pipe the result through a pager
  rdr concordance -q war homer | more
    
  # list subject-verb-object fragments; please be patient
  rdr grammars homer
  
  # list noun phrases
  rdr grammars -g nouns homer
  
  # same as the above, but tabulate the results, look for love, and page the results
  rdr grammars -g nouns -c -q love homer | more
  
  # cluster; do the items in the carrel group themselves?
  rdr cluster homer
    
  # topic model; similar to cluster but with more detail
  rdr tm homer
  
  # play hangman
  rdr play
  
  # page through additional carrels for downloading
  rdr catalog -l remote -h
  
  # read a remote study carrel
  rdr read -l remote pride
  
  # browse the content of a remote study carrel
  rdr browse -l remote pride

  # download another carrel
  rdr download pride
  
  # download yet another carrel
  rdr download sonnets
  
  # list your carrels
  rdr catalog
    
  # search for love
  rdr concordance -q love pride

  # find a lot of love
  rdr concordance -q love sonnets



