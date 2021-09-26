Supporting software
===================

This Toolbox is really an amalgamation of other tools used to exploit Distant Reader study carrels. They are listed below:

   * `Click <https://palletsprojects.com/p/click/>`_ - implements the command-line interface to the Toolbox, and wonderful because its framework makes the interface consistent

   * `Datasette <https://datasette.io>`_ - used to implement the SQL interface to the Reader's underlying SQLite database file, and nice because it provides so many output formats

   * `gensim (version 3.8.3) <https://radimrehurek.com/gensim/>`_ - a broad and wide-ranging module for natural language processing, and this specific version supports interactions with the MALLET subsystem for topic modeling

   * `Matplotlib <https://matplotlib.org>`_ - used in the cluster subcommand to visualize the results

   * `Natural Langauge Toolkit (NLTK) <http://www.nltk.org>`_ - used in a number of places throughout the Toolbox, and makes it easy to tokenize a text into words, ngrams, sentences, and implementing the concordance

   * `pyLDAvis <https://github.com/bmabey/pyLDAvis>`_ - used in the tm subcommand to visualize the results

   * `scikit-learn <https://scikit-learn.org/>`_ - used in the cluster subcommand for feature extraction, calculating distances, and multidimensional scaling

   * `Scipy <https://www.scipy.org>`_ - used in the cluster subcommand to compute hierarchies

   * `textacy <https://github.com/chartbeat-labs/textacy>`_ - builds on the functionality of 	`spaCy <https://spacy.io>`_ and provides support for outputting sentence fragments matching particular grammars

   * `word2vec <https://github.com/danielfrg/word2vec>`_ - a front-end to the venerable word2vec application, and provides the necessary support for the semantics subcommand
