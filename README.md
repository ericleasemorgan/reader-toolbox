

# Distant Reader Toolbox

A command-line interface for interacting with Distant Reader study carrels


## Installation

> `pip install reader-toolbox`


## Description and background

A freely accessible Web-based system called the [Distant Reader](https:/distantreader.org) takes an almost arbitrary amount of unstructured data (text) as input, does text mining and natural language processing against it, and outputs structured data sets designed for more in-depth analysis -- "reading". These data sets are affectionally called "study carrels", you know, those little tables or rooms found in libraries were students, researchers, or scholars are authorized to collect materials for their own private use.

Distant Reader study carrels include a wealth of data and information useful for generating knowledge. For example, study carrels include a cache of the original documents because links break and printing documents can be quite useful for traditional reading purposes. They contain plain text versions of the original documents because text mining and natural language processing is not possible without it. Study carrels include listings each and every word in each and every document, and each word is described by its position in the document, its lemma (root word), and part-of-speech. Carrels include similar listings for named entities, email addresses, URLs, keywords, and bibliographics. All of this data has been distilled into a single, platform-independent relational database file which is also available in a study carrel.

Given the information organized in a study carrel, one can address questions from the mundane to the sublime. Examples include:

   * What words are in a study carrel?
   * What are the most frequent words?
   * What are the most frequent two-word phrases? Three-word phrase? Four-word phrases? Etc?
   * What are the items (the simple nouns ) of discussion? 
   * What do things do -- the verbs?
   * How are things described -- the adjectives and adverbs?
   * What people are mentioned in a corpus?
   * What places are mentioned in a corpus?
   
The Reader Toolbox -- run from the command-line as 'rdr' -- is designed to interact with Distant Reader study carrels. Using the Toolbox you can things such as but not limited to:

   * search and browse the collection of more than 3,000 publicly available study carrels
   * download study carrels from the public collection and add them to your own collection
   * count & tabulate the most frequent ngrams (one-word, two-word, etc. phrases) occurring in study carrels
   * apply concordancing (keyword-in-context searching) against study carrels
   * apply topic modeling (extracting latent themes) against study carrels
   * extract information from your study carrels matching specific grammars
   * and more

## Links

   * download: [https://pypi.org/project/reader-toolbox](https://pypi.org/project/reader-toolbox)
   * documentation: [https://reader-toolbox.readthedocs.io](https://reader-toolbox.readthedocs.io)
   * source code: [https://github.com/ericleasemorgan/reader-toolbox](https://github.com/ericleasemorgan/reader-toolbox)
   * bug tracker: [https://github.com/ericleasemorgan/reader-toolbox/issues](https://github.com/ericleasemorgan/reader-toolbox/issues)




---
Eric Lease Morgan &lt;emorgan@nd.edu&gt;  
August 15, 2021
