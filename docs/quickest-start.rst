Quickest start
==============

This is the tersest I can make it: ::

  # install
  pip install reader-toolbox --upgrade
  
  # configure; accept the defaults
  rdr set local
  
  # download
  rdr download homer
  
  # read homer
  rdr read homer

  # list all words
  rdr ngrams homer
  
  # search
  rdr concordance homer
  
  # enhance toolbox
  python -m spacy download en_core_web_sm
  
  # list subject-verb-object fragments
  rdr grammars homer svo
  
  # cluster
  rdr cluster homer
  
  # enhance toolbox some more
  [INSERT KEWL MALLET INSTALLATION COMMANDS HERE.]
  
  # configure some more
  rdr set mallet
  
  # topic model
  rdr tm homer
  
  # play a game
  rdr play hangman
  
  # download another carrel
  rdr download sonnets
  
  # list your carrels
  rdr catalog
  
  # list additional carrels for downloading
  rdr catalog -l remote -h
  
  # read a remote study carrel
  rdr read -l remote pride
  
  # browse the content of a remote study carrel
  rdr browse -l remote pride

  # download a third study carrel
  rdr download pride
  
  # list your carrels
  rdr catalog
  
  