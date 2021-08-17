Quicker start
=============

This is more terse quickstart: ::

  # output menu
  rdr
  
  # configure where your study carrels will go
  rdr set local
  
  # cache a study carrel named homer
  rdr download homer
  
  # output all the words in homer
  rdr ngrams homer
  
  # see how the word love is used in homer
  rdr concordance -q love homer
  
  # cache a study carrel named sonnets
  rdr download sonnets
  
  # output all the words in sonnets
  rdr ngrams sonnets
  
  # see how the word love is used in sonnets
  rdr concordance -q love sonnets
  
  # cache a study carrel named pride
  rdr download pride
  
  # see how the word love is used on pride
  rdr concordance -q love pride

