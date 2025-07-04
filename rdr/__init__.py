"""
a library for the purposes of distant reading

rdr -- shorthand for Reader Toolbox -- is a command-line tool for
interacting with Distant Reader study carrels.

The Distant Reader (https:/distantreader.org) takes an almost arbitrary
amount of unstructured data (text) as input, does text mining and
natural language processing against it, and outputs sets of structured
data affectionatly called "study carrels".

As you may or may not know, a library study carrel is a little table or
room assigned to individual students. The students are then authorized
to collect thing from around the library, bring them to their study
carrel, organize them in any way they so desire, and persue their
research. Distant Reader study carrels are a modern-day version of the
venerable library study carrel.

This tool -- rdr -- enables the student, researcher, or scholar to
quickly and easily digest the content of carrels to address questions
from the mundane to the sublime. 

Eric Lease Morgan <emorgan@nd.edu>
(c) University of Notre Dame; distributed under a GNU Public License

"""

VERBOSE   = 2

# configure; name of application, basename of configuration file, and default basename of local library
APPLICATIONDIRECTORY = 'rdr'
CONFIGURATIONFILE    = '.rdrrc'
READERLIBRARY        = 'reader-library'
MALLETHOME           = 'mallet'
TIKAHOME             = 'tika-server.jar'
NOTEBOOKSHOME        = 'reader-notebooks'

# remote library
REMOTELIBRARY = 'http://carrels.distantreader.org'
CARRELS       = '/'

# documentation
DOCUMENTATION = 'https://reader-toolbox.readthedocs.io'

# file system mappings
AUTHORS              = 'carrel.authors'
BIB                  = 'bib'
BIBLIOGRAPHYJSON     = 'index.json'
BIBLIOGRAPHYTEXT     = 'index.txt'
BIGRAMSCLOUD         = 'bigrams-cloud.png'
CACHE                = 'cache'
CLUSTERCUBE          = 'cluster-cube.png'
CLUSTERDENDROGRAM    = 'cluster-dendrogram.png'
COLLOCATIONS         = 'carrel.gml'
CORPUS               = 'carrel.txt'
DATABASE             = 'carrel.db'
ENTITIESANY          = 'entities-any.png'
ENTITIESGPE          = 'entities-gpe.png'
ENTITIESORG          = 'entities-org.png'
ENTITIESPERSON       = 'entities-person.png'
ETC                  = 'etc'
FIGURES              = 'figures'
HTM                  = 'htm'
GML                  = 'index.gml'
INDEX                = 'index.htm'
INDEXRDF             = 'index.rdf'
KEYWORDSCLOUD        = 'keywords-cloud.png'
LEXICON              = 'lexicon.txt'
MANIFEST             = 'MANIFEST.xml'
METADATA             = 'index.csv'
POSADJ               = 'pos-adjective.png'
POSADV               = 'pos-adverb.png'
POSNOUN              = 'pos-noun.png'
POSPRON              = 'pos-pronoun.png'
POSPROPN             = 'pos-propernoun.png'
POSVERB              = 'pos-verb.png'
PROVENANCE           = 'index.tsv'
READABILITYBOXPLOT   = 'readability-boxplot.png'
READABILITYHISTOGRAM = 'readability-histogram.png'
READMEFILE           = 'readme.txt'
SENTENCES            = 'carrel.sents'
SIZESBOXPLOT         = 'sizes-boxplot.png'
SIZESHISTOGRAM       = 'sizes-histogram.png'
STOPWORDS            = 'stopwords.txt'
TXT                  = 'txt'
UNIGRAMSCLOUD        = 'unigrams-cloud.png'
VECTORS              = 'carrel.vec'
WRD                  = 'wrd'
WRDS                 = 'carrel.wrds'
ZIP                  = 'index.zip'

# spacy langauge model
MODELSMALL   = 'en_core_web_sm'
MODELMEDIUM  = 'en_core_web_md'

# mallet
MALLETZIP = 'https://distantreader.org/apps/mallet.zip'
MALLETBIN = 'bin/mallet'

# tika server
TIKADOWNLOAD = 'https://distantreader.org/apps/tika-server.jar'

# xhtml template for bibliography (index.xhtml)
XHTML = '''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head><title>Bibliography</title></head>
<body style="margin:3%">
<h1>Bibliography</h1>
<p>This is an automatically generated bibliography describing the content of this study carrel.</p>
<ol>##ITEMS##</ol>
</body>
</html>
'''

# readme.txt
READMEWORDS = '''


About Distant Reader Study Carrels
==================================

tl;dnr - Distant Reader study carrels are data sets, and they are designed to be read by computers as well as people. The purposes of study carrels are to: 1) address the problem of information overload, and 2) faciliate reading at scale. See the Distant Reader home page (https://distantreader.org) for more detail.


Introduction
------------

The Distant Reader and the Distant Reader Toolbox take collections of files as input, and they output data sets called "study carrels". Through the use of study carrels, students, researchers, and scholars can analyze, use, and understand -- read -- large corpora of narrative text, where "large" is anything from a dozen journal articles to hundreds of books. Through this process you can quickly and easily address research questions ranging from the mundane to the sublime:

  * How many items are in this carrel; is the size of this corpus
    big or small?
  
  * What are the things mentioned in this carrel, what do they do,
    and how do they do it?
  
  * In more than a few sentences, what is the content of this
    carrel about and provide specific examples.
  
  * What are the over-arching themes in the carrel, and how have
    they ebbed and flowed over time?
  
  * What is St. Augustine's definition of love, and how does it
    compare to Rousseau's?

  * How do the sum of writings by Plato and Aristotle compare?
  
The balance of this document outlines the structure of every study carrel and introduces you on how to use them.


Layout
------

Study carrels are directories made up of many subdirectories and files. Each study carrel contains these two directories:

  1. cache - original documents used to create the carrel

  2. txt - plain text versions of the cached content; almost all
     analysis is done against the files in this directory
  
There are additional subdirectories filled with tab-delimited files of extracted features:

  1. adr - email addresses
  2. bib - bibliographics (authors, titles, dates, etc.)
  2. ent - named-entities (people, organizations, places, etc.)
  3. pos - parts-of-speech (nouns, verbs, adjectives, etc.)
  4. urls - URLs and their domains
  5. wrd - statistically signficant keywords
  
Even though none of the files in the subdirectories have extensions of .tsv or .tab, they are all tab-delimited files, and therefore they can be imported into any spreadsheet, database, or programming language.

Each study carrel includes two more subdirectories:

  1. figures - where images are saved

  2. etc - everything else, and of greatest importance is the
     carrel's stop word list, bag-of-word representation of the
     carrel, and the carrel's SQLite database file
  
Depending on how the carrel was computed against (modeled), there may be a number of files at the root of each study carrel, and these files are readable by a wide variety of desktop applications and programming languages:

  * index.csv - if the study carrel creation process was augmented
    with a metadata values file (authors, titles, dates, etc.), then
    that file is echoed here

  * index.gml - a Graph Modeling Language file of the carrel's
    author(s), titles, and computed keywords, and useful for
    visualizing their relationships

  * index.htm - an HTML file summarizing the characteristics of the
    extracted features; start here

  * index.json - same as the index.txt file, but in a JSON form

  * index.rdf - bibliographic characteristics encoded in the form
    of the Resource Description Framework, and intended for the
    purposes of supporting the Semantic Web

  * index.tsv - a very very rudimentary list of characateristics
    denoting whence the carrel came and when

  * index.txt - a bibliographic report in the form of a plain text
    file

  * index.xml - a browsable interface to the study carrel; renders
    much easier on the Web than on your local computer

  * index.zip - the whole study carrel compressed into a single
    file for the purposes of collaborating, sharing, and downloading


Desktop Applications
--------------------

Study carrels are designed to be platform- and network-independent. What does this mean? It means two things: 1) no special software is needed to read study carrel data, and 2) if the study carrel is saved on your local computer, then no Internet connection is needed to analyze it. That said, you will want to employ the use of a variety of desktop applications (or programming languages) in order to get the most out of a study carrel.


Text Editors

Text editors are not word processors. While text editors and word processors both work with text, the former are more about the manipulation of the text, and the later are more about graphic design. The overwhelming majority of data found in study carrels is in the form of plain text, and you will find the use of a descent text editor indispensible. Using a text editor, you can open and read just about any file found in a study carrel. That's very important!

A good text editor supports powerful find and replace functionality, supports regular expressions, has the ability to open multi-megabyte files with ease, can turn on and off line wrapping, and reads text files created on different computer platforms. The following two text editors are recommended. Don't rely on Microsoft Word nor Google Docs, they are word processors.

  * BBEdit (https://www.barebones.com/products/bbedit/)
  * NotePad++ (https://notepad-plus-plus.org/)


Word Cloud Applications

The use of words clouds is often viewed as sophmoric. This is true because they are to often used to illustrate the frequency of all words in a text. On the other hand, if word clouds illustrate the frequencies of specific things -- keywords, parts-of-speech, or named entities -- then word clouds become much more complelling. After all, "A picture is worth a thousand words."

A program called Wordle is an excellent word cloud program. It takes raw text as input. It also accepts delimited data as input. The resulting images are colorful, configurable, and exportable. Unfortunately, it is no longer supported; while it will run on most Macintosh comuters, it will no longer run (easily) on Windows computers. (I would pay a fee to have Wordle come back to life and brought up-to-date.) If Wordle does not work for you, then there are an abundance of Web-based word cloud applications.

  * Wordle (https://web.archive.org/web/20191115162244/http://www.wordle.net/)
  

Concordances

Developed in the 13th Century, concordances are all but the oldest of text mining tools. They function like the rudimentary find function you see in many applications. Think control-f on steroids.

Concordances locate a given word in a text, display the text surrounding the word, and help you understand what other words are used in the same context. After all, to paraphrase a linguist named John Firth, "One shall know a word by the company it keeps." The following is a link to a concordance application that is worth way more than what you pay for it, which is nothing.

  * AntConc (https://www.laurenceanthony.net/software/antconc/)
  

Spreadsheet-Like Applications

The overwhelming majority of the content found in study carrels is in the form of plain text, and most of this plain text is structured in the form of tab-delimited text files -- matrixes or sometimes called "data frames". These files are readable by any spreadsheet, database, or programming language. Microsoft Excel, Google Sheets, or Macintosh Numbers can import Reader study carrel delimited data, but these programs are more about numerical analysis and less about analyzing text.

Thus, if you want to do analysis against Reader study carrel data, and if you do not want to write your own software, then the use of an analysis program called OpenRefine is highly recommended. OpenRefine eats delimited data for lunch. Once data is imported, OpenRefine supports powerful find and replace functions, counting and tabulating functions, faceting, sorting, exporting, etc. While text editors and concordances supplement traditional reading functions, OpenRefine supplements the process of understanding study carrels as data.

  * OpenRefine (https://openrefine.org/)


Topic Modeling Applications

Topic modeling is a type of machine learning process called "clustering". Given an integer (I), a topic modeler will divide a corpus into I clusters, and each cluster is akin to a theme. Thus, after practicing with a topic modeler, you can address questions like: what are the things this corpus is about, to what degee are themes manifested across the corpus, and which documents are best represented by the themes. After supplementing the corpus with metadata (authors, titles, dates, keywords, geners, etc.) Topic modeling becomes even more useful because you can address additional questions, such as: how did these themes ebb and flow over time, who wrote about what, and how is this style of writting different from that style. 

A venerable MALLET application is the grand-daddy of topic modeling tools, but is a command-line driven thing. On the other hand, a program called Topic Modeling Tool, which is rooted in MALLET, brings topic modeling to the desktop. Like all the applications listed here, it's use requires practice, but it works well, it works quickly, and the data it outputs can be used in a variety of ways.

  * MALLET (https://mimno.github.io/Mallet/)
  * Topic Modeling Tool (https://github.com/senderle/topic-modeling-tool)
  

Network Analysis Applications

Texts can be modeled in the form of networks -- nodes and edges. For example, there are authors (nodes), there are written works (additional nodes), and specific authors write specific works (edges). Similarly, there are works (nodes), there are keywords (additional nodes), and specific works are described with keywords (edges). Given these sorts of networks you can address -- and visualize -- all sorts of questions: who wrote what, what author wrote the most, what keywords dominate the collection, or what keywords are highly significant (central) to many works and therefore authors? 

Network analysis is rooted in graph theory, and it is not a trivial process. On the other hand, a program called Gephi makes the process easier. Import one of any number of different graph formats or specifically shaped matrixes, apply any number layout options to visualize the graph, filter the graph, visualize again, apply clustering or calcuate graph characteristics, and visualize a third time. The process requires practice, some knowledge of graph theory, and an aesthetic sensibility. In the end, you will garnder a greater understanding of the content in your carrel.

  * Gephi (https://gephi.org)


Command-Line (Shell) Interface
------------------------------

The Distant Reader and its companion, the Distant Reader Toolbox, are implemented as a set of Python modules. If you have Python installed, then from the command line you can install the modules -- the Toolbox:

  pip install reader-toolbox

If you are a developer, then you may want to use GitHub to install from source:

  git clone https://github.com/ericleasemorgan/reader-toolbox.git
  cd reader-toolbox
  pip install -e .

Once installed, you can run variations of the rdr ("reader") command. For example, running rdr without any arguments returns a menu:
  
  Usage: rdr [OPTIONS] COMMAND [ARGS]...

  Options:
    --help  Show this message and exit.
  
  Commands:
    about          Output a brief description and version number of the...
    adr            Filter email addresses from <carrel>
    bib            Output rudimentary bibliographics from <carrel>
    browse         Peruse <carrel> as a file system
    build          Create <carrel> from files in <directory>
    catalog        List study carrels
    cluster        Apply dimension reduction to <carrel> and visualize the...
    collocations   Output network graph based on bigram collocations in...
    concordance    A poor man's search engine
    documentation  Use your Web browser to read the Toolbox (rdr) online...
    download       Cache <carrel> from the public library of study carrels
    edit           Modify the stop word list of <carrel>
    ent            Filter named entities and types of entities found in...
    get            Echo the values denoted by the set subcommand
    grammars       Extract sentence fragments from <carrel> as in:
    info           Output metadata describing <carrel>
    ngrams         Output and list words or phrases found in <carrel>
    notebooks      Download, list, and run Toolbox-specific Jupyter Notebooks
    play           Play the word game called hangman
    pos            Filter parts-of-speech, words, and lemmas found in <carrel>
    rdfgraph       Create RDF (Linked Data) file against <carrel>
    read           Open <carrel> in your Web browser
    readability    Report on the readability (Flesch score) of items in...
    search         Perform a full text query against <carrel>
    semantics      Apply semantic indexing against <carrel>
    sentences      Given <carrel> save, output, and process sentences
    set            Configure the location of study carrels, the subsystem...
    sizes          Report on the sizes (in words) of items in <carrel>
    sql            Use SQL queries against the database of <carrel>
    summarize      Summarize <carrel>
    tm             Apply topic modeling against <carrel>
    url            Filter URLs and domains from <carrel>
    web            Experimental Web interface to your Distant Reader study...
    wrd            Filter statistically computed keywords from <carrel>
    zip            Create an archive (index.zip) file of <carrel>

Use the rdr command to build study carrels and do analysis against them. For example: 1) create a directory on your desktop and call it "practice", 2) copy a few PDF files into the directory, 3) open your terminal, 4) change directories to the desktop, and 5) run the following command to create your a carrel named "my-first-carrel":

  rdr build my-first-carrel practice -s

Once you get this far, you can run many other rdr commands:

  * rdr info my-first-carrel
  * rdr bib my-first-carrel
  * rdr concordance my-first-carrel
  * rdr tm my-first-carrel
  
For more detail, run the rdr command with the --help flag. See also the documentation: https://reader-toolbox.readthedocs.io/

Power-user hints: The output of many rdr commands are designed to be post-processed by the command line shell. For example, suppose you have a study carrel named "homer", then the following command will display the results of the bib command one screen at a time:

  rdr bib homer | more

A carrel's bibliographics can also be output as a JSON stream, and by piping the output to many additional commands, you can create a prettier bibliography:

  rdr bib homer -f json              | \\
  jq -r '.[]|[.title,.summary]|@tsv' | \\
  sed "s/\\t/ -- /"                   | \\
  sed "s/$/\\n/"                      | \\
  fold -s                            | \\
  less

Suppose you wanted to extract rudimentary definitions of the word "whales" from a carrel named "moby", then the following is a quick and dirty way to get the job done:

  Q='whales are'; rdr concordance moby -q "$Q" -w 60 | sed "s/^.*$Q/$Q/"
  
Creating a nice list of sentences is similar:

  Q='whales are'; rdr sentences moby -p filter -q "$Q" | \\
  sed "s/$/\\n/"                                        | \\
  fold -s                                              | \\
  less -i --pattern="$Q"
  

Write your own software
-----------------------

The Reader Toolbox can also be imported into Python scripts, and consequently you can combine its functionality with other Python modules. For example the power-user concordance command, above, can be written as a Python script:

  # configure
  CARREL = 'moby'
  QUERY  = 'whales are'
  WIDTH  = 60
  
  # require
  from rdr import concordance
  from re  import sub
  
  # do the work, output, and done
  lines = concordance(CARREL, query=QUERY, width=WIDTH)
  [print(sub('^.*{}'.format(QUERY), QUERY, line)) for line in lines]
  exit()

Use pydoc to learn more: pydoc rdr


Summary
-------

Distant Reader and the Distant Reader Toolbox take sets of narrative text as input, and they output data sets called study carrels. The content of study carrels are intended to be read by computers as well as people. Study carrels are platform- as well as network-independent, and therefore they are designed to stand the test of time.

Use desktop software and/or the Reader Toolbox to build, download, search, browse, peruse, investigate, and report on the content of study carrels. Use the extracted features as if they were items found in a back-of-the-book index, and use them as input to concordances for the purpose of closer reading. Topic model study carrels to enumerate latent themes and address the question, "How do themes ebb and flow over time?" Import the index.gml files into Gephi (or any other network graph application) to visualize how authors, titles, and dates are related. All of this is just the tip of the iceberg; study carrels can do much more.

Study carrels are intended to address the problem of information overload. They make it easier to use and understand large volumes of text -- dozens of books or hundreds of journal articles. Through the process you can address all sorts of research questions, and in the end you will have supplemented your traditional reading process and you will have been both more thorough and more comprehensive in your research.

--
Eric Lease Morgan <emorgan@nd.edu>
Navari Family Center for Digital Scholarship
Hesburgh Libraries
University of Notre Dame

##DATE##

'''

# html template for summarize command
TEMPLATE = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>##CARREL##</title>
	<style type="text/css">
		.first { text-align: right; }
		.second { text-align: left; }
		.third { text-align: left; }
		tr:nth-child(even) { background-color: #f2f2f2;}
	</style>
</head>
<body style='margin: 7%'>

	<h1>##CARREL##</h1>
	
	<p>This is an automatically generated overview of the Distant Reader study carrel called <strong>##CARREL##</strong>.</p>
	<p>Given a corpus of narrative text, the <a href="https://distantreader.org/">Distant Reader</a> and the <a href="https://reader-toolbox.readthedocs.io/en/latest/">Distant Reader Toolbox</a> create data sets, and these data sets are affectionately called "study carrels". As data sets, study carrels are intended to be read by people as well as computers, and <em>their purpose is to supplement the reading process, to increase use &amp; understanding</em>.</p>
	<p>Study carrels are designed to be computable, and this Web page is the result of one such computing process; here you will find a simple analysis of the carrel's extracted features. Use the features to characterize the content of the carrel, and then use them like items in a back-of-the-book index for more in-depth analysis.</p>
	
	<h2>Basic characteristics</h2>
	
		<p>Outlined below are some introductory features of the carrel:</p>
		<table>
			 <tr>
				<th class='first'>Feature</th>
				<th class='first'>Value</th>
				<th class='third'>Description</th>
			</tr>
			<tr>
				<td class='first'>creator</td>
				<td class='first'>##CREATOR##</td>
				<td class='third'>Under what username was this carrel created?</td>
			</tr>
			<tr>
				<td class='first'>date created</td>
				<td class='first'>##DATECREATED##</td>
				<td class='third'>When was this carrel created?</td>
			</tr>
			<tr>
				<td class='first'>size in items</td>
				<td class='first'>##ITEMS##</td>
				<td class='third'>How many items are in the carrel?</td>
			</tr>
			<tr>
				<td class='first'>size in words</td>
				<td class='first'>##WORDS##</td>
				<td class='third'>Measured in words, how big is this carrel? By comparison, the <cite>Bible</cite> is about 800,000 words long.</td></tr>
			<tr>
				<td class='first'>readability score</td>
				<td class='first'>##FLESCH##</td>
				<td class='third'>Where 0 denotes impossible and 100 denotes easy, how difficult is this carrel to read?</td>
			</tr>
			<tr>
				<td class='first'>other files</td>
				<td class='first'><a href="./etc/stopwords.txt">stopwords</a></td>
				<td class='third'>What words have been denoted as function words such as "the", "a", and "an"?</td>
			</tr>
			<tr>
				<td class='first'>other files</td>
				<td class='first'><a href="./etc/carrel.txt">entire corpus</a></td>
				<td class='third'>What does a bag-of-words form of the carrel look like?</td>
			</tr>
		</table>
		
	<h2>Sizes</h2>
	
		<p>Measured in words, how big are the items in this carrel? To what degree are they of similar size? Are any of the items particularly large or small? In general, the typical scholarly journal article is between 5,000 and 8,000 words long.</p>
		<p style='text-align: center'><img alt='sizes-boxplot' src='./figures/sizes-boxplot.png' width='49%' /> <img alt='sizes-histogram' src='./figures/sizes-histogram.png' width='49%' /></p>

	<h2>Readability</h2>
	
		<p>Using a metric called Flesch -- where 0 means nobody can read the item, and 100 means everybody can read it -- how difficult are the items in this carrel to read? Shakespeare's <cite>Sonnets</cite> are relatively easy to read (with a score of about 90) because their vocabulary is small and the sentences are short. The typical novel by Jane Austen or Herman Melville have scores in the 70's. Scholarly articles are more difficult (scores between 50-70) because their langauge is more specialized. Texts of poor optical character recognition quality typically have very low scores.</p>
		<p style='text-align: center'><img alt='readability-boxplot' src='./figures/readability-boxplot.png' width='49%' /> <img alt='readability-histogram' src='./figures/readability-histogram.png' width='49%' /></p>

	<h2>Ngrams</h2>
	
		<p>Excluding <a href="./etc/stopwords.txt">stop words</a>, what are the most frequent individual words and two-word combinations in the corpus, thus addressing the question, "What are the items in this study carrel about?"</p>
		<table>
			<tr align='center'>
				<td><img alt='unigrams-cloud' src='./figures/unigrams-cloud.png' width='100%' /><br /><br />unigrams</td>
				<td><img alt='bigrams-cloud' src='./figures/bigrams-cloud.png' width='100%' /><br /><br />bigrams</td>
			</tr>
		</table>

	<h2>Parts-of-speech</h2>
	
		<p>The most frequent extracted parts-of-speech features address questions of "What is discussed in this corpus, what do they do, and how are they described?"</p>
		<table>
			<tr align='center'>
				<td><img alt='pos-noun' src='./figures/pos-noun.png' width='100%' /><br /><br />nouns<br /><br /><br /></td>
				<td><img alt='pos-propernoun' src='./figures/pos-propernoun.png' width='100%'  /><br /><br />proper nouns<br /><br /><br /></td>
			</tr>
			<tr align='center'>
				<td><img alt='pos-pronoun' src='./figures/pos-pronoun.png' width='100%'  /><br /><br />pronouns<br /><br /><br /></td>
				<td><img alt='pos-verb' src='./figures/pos-verb.png' width='100%'  /><br /><br />verbs<br /><br /><br /></td>
			</tr>
			<tr align='center'>
				<td><img alt='pos-adjective' src='./figures/pos-adjective.png' width='100%'  /><br /><br />adjectives<br /><br /></td>
				<td><img alt='pos-adverb' src='./figures/pos-adverb.png' width='100%'  /><br /><br />adverbs<br /><br /></td>
			</tr>
		</table>
	
	<h2>Entities</h2>
	
		<p>Similar to nouns, named-entities are real-world things but they are more specific. They help address questions of who, where, and how many.</p>
		<table>
			<tr align='center'>
				<td><img alt='entities-any' src='./figures/entities-any.png' width='100%' /><br /><br />any entity<br /><br /><br /></td>
				<td><img alt='entities-person' src='./figures/entities-person.png' width='100%' /><br /><br />persons<br /><br /><br /></td>
			</tr>
			<tr align='center'>
				<td><img alt='entities-gpe' src='./figures/entities-gpe.png' width='100%' /><br /><br />geo-political entities</td>
				<td><img alt='entities-org' src='./figures/entities-org.png' width='100%' /><br /><br />organizations</td>
			</tr>
		</table>

	<h2>Clusters</h2>

		<p>Through the use of a variation of the principle component analysis alogorithm, it is possible to plot the location of study carrel items in two- and three-dimentional spaces, thus addressing the questions, "To what degree is this study carrel holistic; to what degree are the items in this carrel easily subdivided into smaller group?"</p>
		<p style='text-align: center'><img alt='cluster-dendrogram' src='./figures/cluster-dendrogram.png' width='49%' /> <img alt='cluster-cube' src='./figures/cluster-cube.png' width='49%' /></p>

	<h2>Keywords</h2>
	
		<p>Excluding <a href="./etc/stopwords.txt">stop words</a>, and through the use of a variation of the term frequency-inverse document frequency algorithm, the set of computed keywords are akin to subject terms, and they help address the questions of, "What are the items in this carrel about and to what degree?"</p>
		<p style='text-align: center'><img alt='keywords-cloud' src='./figures/keywords-cloud.png' width='66%' /></p>

	<h2>Additional models</h2>
	
		<p>Depending on how the carrel was computed against, the following point to additional models:</p>
		<ul>
			<li><a href="./index.html">analysis</a> - if a person used the modeling tools to analyze this carrel and wrote up their observations, then those observations ought to be here</li>
			<li><a href="./index.txt">bibliographics (txt)</a> - authors, titles, dates, extents, summaries, and keywords in a simple human-readable form</li>
			<li><a href="./index.json">bibliographics (JSON)</a> - same as the above but formatted as a JSON stream</li>
			<li><a href="./index.zip">compressed</a>- the whole study carrel compressed into a single file for the purposes of collaboration, sharing, and downloading</li>
			<li><a href="./index.xml">manifest</a> - a browsable interface to the study carrel</li>
			<li><a href="./index.csv">metadata</a> - if the study carrel creation process was augmented with metadata values (authors, titles, dates, etc.) file, then that file is available here</li>
			<li><a href="./index.gml">network graph</a> - a Graph Modeling Language file of the carrel's author(s), titles, and computed keywords, and it is useful for visualizing their relationships</li>
			<li><a href="./index.tsv">provenance</a> - a very very rudimentary list of characateristics denoting whence the carrel came and when</li>
			<li><a href="./index.rdf">semantic triples</a> - bibliographic characteristics encoded in the form of the Resource Description Framework, and intended for the purposes of supporting the Semantic Web</li> 
			<li><a href="./index.htm">summary</a> - this file</li>
		</ul>
		
		<p>For more detail about study carrels, their structure, and how they can be used, start with the <a href="./readme.txt">read me</a> file.</p>

	<h2>Subdirectories</h2>

		<p>Each and every study carrel contains a number of subdirectories (folders). The first two are about the carrel's content:</p>
		<ul>
			<li><a href="./cache/">cache</a> - here you will find the original content used to create the carrel</li>
			<li><a href="./txt/">txt</a> - this subdirectory contains plain text versions of original content; all analysis is done against the content in this directory</li>
		</ul>
		<p>The next few subdirectories contain extracted features in the form of tab-delimited text files:</p>
		<ul>
			<li><a href="./adr/">adr</a> - email addresses, if they exist</li>
			<li><a href="./bib/">bib</a> - bibliographics (authors, titles, dates, extents, and summaries)</li>
			<li><a href="./ent/">ent</a> - named-entities (real world things such as people, places, organizations, dates, times, etc.)</li>
			<li><a href="./pos/">pos</a> - parts-of-speech (each and every word from each and every item described as a noun, verb, adjective, etc.)	</li>
			<li><a href="./urls/">urls</a> - Universal Resource Locators, if they exist</li>
			<li><a href="./wrd/">wrd</a> - statistically significant computed keywords</li>
		</ul>
		<p><em>Very important.</em> All of the content in the subdirectories above are readable by any spreadsheet application, database program, or programming language. Therefore, you do not need special software to do analysis.</p>
		<p>There are two additional subdirectories in every study carrel:</p>
		<ul>
			<li><a href="./figures/">figures</a> - where images are saved</li>
			<li><a href="./etc/">etc</a> - the subdirectory for everything else, and of greatest importance is the carrel's stop word list, bag-of-word representation of the carrel, and the carrel's SQLite database file</li>
		</ul>
		<p>All of this is just the beginning. For more detail about study carrels, their structure, and how they can be used, begin with the <a href="./readme.txt">read me</a> file.</p>
	
	<hr />
	
	<p style='text-align: right'>Date created: ##DATE##</p>

</body>
</html>
'''

# require
import click

# create a Sentences iterator
class Sentences( object ) :

	'''Given a file name pointing to a line-delimited list of
	tokenized sentences, generate an iterator over the
	sentences.'''
	
	# initialize
	def __init__( self, file ) : self.file = file

	# iterate
	def __iter__( self ) :
			
		# return each sentence
		for sentence in open( self.file ) : yield sentence


# return the object of a given subject/predicate pair
def rdfSearchForObject ( graph, subject, predicate ) :
	sparql = 'SELECT ?object WHERE {<' + str( subject ) + '> <' + predicate + '> ?object}'
	object = graph.query( sparql ).bindings[ 0 ][ 'object' ]
	return object
	

# return the English label of a given object
def rdfSearchForLabel ( graph, object ) :
	sparql = 'SELECT ?label WHERE {<' + str( object ) + '> rdfs:label ?label . FILTER(LANG(?label) = "en")}'
	try : label  = graph.query( sparql ).bindings[ 0 ][ 'label' ]
	except IndexError : label = 'nan'
	return label

	
# given the name of a carrel, return GML
def graph2gml( carrel, output='gml', save=False, erase=False, localLibrary=None ) :

	'''Given the name of a carrel, and an optional output type ('gml' or 'chart'), return GML or its visualization.'''
	
	# configure
	FORMAT  = 'xml'
	CARREL  = 'http://carrels.distantreader.org/carrel#'
	WDP     = 'http://www.wikidata.org/prop/direct/'
	DCTITLE = 'http://purl.org/dc/terms/title'
	OUTPUTS = [ 'gml', 'chart' ]
	
	# require
	from rdflib.namespace import DCTERMS, RDFS
	import networkx
	import rdflib
	import sys
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check #0
	if output not in OUTPUTS :
	
		click.echo( "Error: Unsupported value for output (" + str( output ) + "); exiting.", err=True )
		exit()
		
	# sanity check #1
	checkForCarrel( carrel, localLibrary )
	
	# initialize
	graph   = rdflib.Graph()

	# sanity check #2
	authors  = localLibrary/carrel/ETC/AUTHORS
	keywords = localLibrary/carrel/ETC/WRDS
	if not authors.exists()  : reconcile( carrel, 'authors', localLibrary, erase=False )
	if not keywords.exists() : reconcile( carrel, 'keywords', localLibrary, erase=False )

	# more configuration and santity checks
	rdf = localLibrary/carrel/INDEXRDF
	if not rdf.exists() : carrel2graph( carrel, localLibrary )

	# yet more initialization
	graph  = graph.parse( rdf, format=FORMAT )
	CARREL = rdflib.Namespace( CARREL )
	WDP    = rdflib.Namespace( WDP )
	nodes  = []
	edges  = []

	# process all keywords
	for subject, predicate, object in graph.triples( ( None, CARREL.keyword, None ) ) :
	
		# get the subject's corresponding title
		subject = rdfSearchForObject( graph, subject, DCTITLE )
		
		# update
		nodes.append( ( subject, { 'types' : 'item' } ) )
		nodes.append( ( object, { 'types' : 'keyword' } ) )
		edges.append( ( subject, object, { 'types' : 'keyword' } ) )

	# process all subjects
	for subject, predicate, object in graph.triples( ( None, DCTERMS.subject, None ) ) :
							
		# get the subject's title and the object's label
		subject = rdfSearchForObject( graph, subject, DCTITLE )
		object  = rdfSearchForLabel( graph, object )
					
		# update
		nodes.append( ( subject, { 'types' : 'item' } ) )
		nodes.append( ( object, { 'types' : 'subject' } ) )
		edges.append( ( subject, object, { 'types' : 'subject' } ) )

	# process all authors
	for subject, predicate, object in graph.triples( ( None, CARREL.hasAuthor, None ) ) :
	
		# get the subject's corresponding title
		subject = rdfSearchForObject( graph, subject, DCTITLE )

		# update 
		nodes.append( ( subject, { 'types' : 'item' } ) )
		nodes.append( ( object, { 'types' : 'author' } ) )
		edges.append( ( subject, object, { 'types' : 'author' } ) )

	# process all creators
	for subject, predicate, object in graph.triples( ( None, DCTERMS.creator, None ) ) :
	
		# get the subject's corresponding title
		subject = rdfSearchForObject( graph, subject, DCTITLE )
		object  = rdfSearchForLabel( graph, object )

		# update 
		nodes.append( ( subject, { 'types' : 'item' } ) )
		nodes.append( ( object, { 'types' : 'creator' } ) )
		edges.append( ( subject, object, { 'types' : 'creator' } ) )

	# build the graph; very smart
	graph = networkx.Graph()
	graph.add_nodes_from( nodes )
	graph.add_edges_from( edges )

	# GML output
	if output == 'gml' :
	
		# save
		if save == True :
		
			gml = localLibrary/carrel/GML
			networkx.write_gml( graph, gml )

		# send to STDOUT
		else : networkx.write_gml( graph, sys.stdout.buffer )

	# chart output
	if output == 'chart' : click.echo( "Warning: The output value of chart is not implemented, yet.", err=True )


# given the name of a carrel, output sentences
def sentences( carrel, process='list', query='love', save=True ) :

	# configure
	PATTERN = '*.txt'
	
	# require
	import rdr
	import multiprocessing
	from nltk.wsd import lesk

	# configure
	library   = configuration( 'localLibrary' )
	filenames = library/carrel/rdr.TXT
	sentences = library/carrel/( rdr.ETC )/( rdr.SENTENCES )

	checkForCarrel( carrel )

	if not sentences.exists() :
	
		# parallel process each plain text file in the given corpus
		pool    = multiprocessing.Pool()
		click.echo( 'Step #1 of 2: Reading sentences', err=True )
		results = pool.starmap( rdr.extractSentences, [ [ filename ] for filename in filenames.glob( PATTERN ) ] )
		pool.close()

		# save the result
		click.echo( 'Step #2 of 2: Saving sentences', err=True )
		with open( sentences, 'w' ) as handle :

			# get all sentences and process each one
			for result in results :

				# output
				for sentence in result : handle.write( '%s\n' % sentence )

		# done
		click.echo( 'Done.', err=True )

	if process == 'list' and save == False :
		
		# output each sentence
		for sentence in Sentences( sentences ) : click.echo( sentence, nl=False )

	if process == 'define' :
	
		# output each sentence
		for sentence in Sentences( sentences ) : 
		
			# filter
			if query in sentence :
				
				# disambiguate
				synset = lesk( sentence.split(), query )
	
				# output, conditionally
				if synset :
	
					# debug
					click.echo( '       query: ' + query)
					click.echo( '      synset: ' + synset.name() )
					click.echo( '    sentence: ' + sentence, nl=False )
					click.echo( '  definition: ' + synset.definition() )
					click.echo()

	if process == 'filter' :
	
		# output each sentence
		for sentence in Sentences( sentences ) : 
		
			if query in sentence : click.echo( sentence, nl=False )


# given the name of a carrel, create an RDF file describing it
def carrel2graph( carrel, localLibrary=None ) :

	'''Given the name of a carrel, create an RDF file (index.rdr) describing it.'''
	
	# configure
	NAMESPACE = 'http://carrels.distantreader.org/carrel#'
	PREFIX    = 'carrel'
	FORMAT    = 'xml'
	GRAPHROOT = 'http://carrels.distantreader.org/'
	CREATOR   = { 'name':"Eric Lease Morgan", 'qnumber':'https://www.wikidata.org/wiki/Q102275801' }
	TEMPLATE  = '''PREFIX wd: <http://www.wikidata.org/entity/> CONSTRUCT { wd:##QNUMBER## ?p ?o } WHERE { SERVICE <https://query.wikidata.org/bigdata/namespace/wdq/sparql> { wd:##QNUMBER## ?p ?o }}'''
	WIKIDATA  = 'http://www.wikidata.org/entity/'

	# require
	from rdflib           import Graph, URIRef, Literal, Namespace
	from rdflib.namespace import RDF, DCTERMS, DCMITYPE, RDFS
	import pandas as pd
	import json
	import rdr
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	studyCarrel = carrel
	graph       = Graph()
	CARREL      = Namespace( NAMESPACE )
	graph.bind( PREFIX, CARREL )

	# denote a carrel and update the graph
	carrel  = URIRef( GRAPHROOT + studyCarrel )
	graph.add( ( carrel, RDF.type,        CARREL.carrel ) )
	graph.add( ( carrel, RDF.type,        DCMITYPE.Dataset ) )
	graph.add( ( carrel, RDF.type,        DCMITYPE.Collection ) )
	graph.add( ( carrel, DCTERMS.title,   Literal( studyCarrel ) ) )

	# add the carrel's creator (me)
	#qnumber = URIRef( CREATOR[ 'qnumber' ] )
	#graph.add( ( carrel, DCTERMS.creator, qnumber ) )
	#graph.add( ( qnumber, RDFS.label,     Literal( CREATOR[ 'name' ] ) ) )

	# get provenance and extents...
	dateCreated      = provenance( studyCarrel, 'dateCreated', localLibrary )
	process          = provenance( studyCarrel, 'process', localLibrary )
	totalSizeInItems = extents( studyCarrel,    'items', localLibrary )
	totalSizeInWords = extents( studyCarrel,    'words', localLibrary )
	averageFlesch    = extents( studyCarrel,    'flesch', localLibrary )

	# ...and update the graph
	graph.add( ( carrel, DCTERMS.created,            Literal( dateCreated ) ) )
	graph.add( ( carrel, CARREL.hasCreationProcess,  Literal( process ) ) )
	graph.add( ( carrel, CARREL.hasTotalSizeInItems, Literal( totalSizeInItems ) ) )
	graph.add( ( carrel, CARREL.hasTotalSizeInWords, Literal( totalSizeInWords ) ) )
	graph.add( ( carrel, CARREL.hasAverageFlesch,    Literal( averageFlesch ) ) )

	# get the name of the keywords reconciliation file, and check
	keywords = localLibrary/studyCarrel/ETC/WRDS
	if not keywords.exists() :
	
		click.echo( "The keywords reconciliation file does not exist. Please create one. Exiting.", err=True )
		exit()
		
	# reconciliation file exists
	else :
	
		# get and process all keyword qunumbers; update the graph with reconciled values
		keywords = pd.read_csv( keywords, sep='\t', dtype={'id': str} )
		qnumbers = set( keywords[ keywords[ 'qnumber' ].notnull() ][ 'qnumber' ].tolist() )

	# get wikidata qnumbers, if they exist
	qnumbers = sorted( qnumbers)
	length   = len( qnumbers )
	for index, qnumber in enumerate( qnumbers ) :

		# debug, create SPARQL query, search, get result, and update graph
		click.echo( "Getting Wikidata for keyword " + qnumber + ' (#' + str( index + 1 ) + ' of ' + str( length) + ')', err=True )
		sparql = TEMPLATE.replace( '##QNUMBER##', qnumber )
		rdf    = graph.query( sparql ).serialize( format=FORMAT )
		graph.parse( rdf, format=FORMAT )	

	# get the name of the authors reconciliation file, and check
	authors = localLibrary/studyCarrel/ETC/AUTHORS
	if not authors.exists() :
	
		click.echo( "The authors reconciliation file does not exist. Please create one. Exiting.", err=True )
		exit()

	# reconciliation file exists
	else :
	
		# get and process all author qunumbers; update the graph with reconciled values
		authors  = pd.read_csv( authors, sep='\t' )
		qnumbers = set( authors[ authors[ 'qnumber' ].notnull() ][ 'qnumber' ].tolist() ) 

	# process all author qunumbers; update the graph with reconciled values some more
	qnumbers = sorted( qnumbers)
	length   = len( qnumbers )
	for index, qnumber in enumerate( qnumbers ) :

		# debug, create SPARQL query, search, get result, and update graph
		click.echo( "Getting Wikidata for author " + qnumber + ' (#' + str( index + 1 ) + ' of ' + str( length) + ')', err=True )
		sparql = TEMPLATE.replace( '##QNUMBER##', qnumber )
		rdf    = graph.query( sparql ).serialize( format=FORMAT )
		graph.parse( rdf, format=FORMAT )	

	# get and process each bibliographic item
	bibliographics = json.loads( bibliography( studyCarrel, localLibrary, format='json' ) )
	length         = len( bibliographics )
	for index, bibliographic in enumerate( bibliographics ) :
		
		# debug
		click.echo( 'Adding item ' + str( index ) + ' of ' + str( length ) + '\r', nl=False, err=True )
	
		# get the item's id and update the graph
		idItem = str( bibliographic[ 'id' ] )
		item   = URIRef( idItem )
		graph.add( ( carrel, DCTERMS.hasPart, item ) )
	
		# process authors, conditionally
		if not authors.empty :
	
			# iterate over the keywords
			for _, author in authors.iterrows() :
			
				# update the graph, conditionally
				if str( author[ 'id' ] ) == idItem :
				
					# get the qnumber and update the graph, conditionally
					qnumber = author[ 'qnumber' ]
					if type( qnumber ) is str : graph.add( ( item, DCTERMS.creator, URIRef( WIKIDATA + qnumber ) ) )
					else : graph.add( ( item, CARREL.hasAuthor, Literal( author[ 'author' ] ) ) )

		# add title
		graph.add( ( item, DCTERMS.title, Literal( bibliographic[ 'id' ] ) ) )

		# add date
		graph.add( ( item, DCTERMS.date, Literal( bibliographic[ 'date' ] ) ) )

		# add extents; using try is a hack for bogus data
		try : graph.add( ( item, CARREL.hasFlesch, Literal( int( bibliographic[ 'flesch' ] ) ) ) )
		except TypeError : continue
		graph.add( ( item, CARREL.hasSizeInWords, Literal( int( bibliographic[ 'words' ] ) ) ) )

		# add cache and text
		if bibliographic[ 'extension' ] : cache = URIRef( GRAPHROOT + studyCarrel + '/' + ( CACHE ) + '/' + idItem + bibliographic[ 'extension' ] )
		else                            : cache = URIRef( GRAPHROOT + studyCarrel + '/' + ( CACHE ) + '/' + idItem )
		text  = URIRef( GRAPHROOT + studyCarrel + '/' + ( TXT )   + '/' + idItem + '.txt' )
		graph.add( ( item,  CARREL.hasCache,     cache ) )
		graph.add( ( item,  CARREL.hasPlainText, text ) )
		graph.add( ( cache, DCTERMS.type,        Literal( bibliographic[ 'mime' ] ) ) )
		graph.add( ( text,  DCTERMS.type,        Literal( 'text/plain' ) ) )
	
		# process keywords, conditionally
		if not keywords.empty :
			
			# iterate over the keywords
			for _, keyword in keywords.iterrows() :
						
				# update the graph, conditionally
				if str( keyword[ 'id' ] ) == idItem :
				
				
					# get the qnumber and update the graph, conditionally
					qnumber = keyword[ 'qnumber' ]
					if type( qnumber ) is str : graph.add( ( item, DCTERMS.subject, URIRef( WIKIDATA + qnumber ) ) )
					else : graph.add( ( item, CARREL.keyword, Literal( keyword[ 'keyword' ] ) ) )

	# output and done
	rdf = localLibrary/studyCarrel/INDEXRDF
	with open( rdf, 'w' ) as handle : handle.write( graph.serialize( format=FORMAT ) )



# given a carrel and a type, (re-)create reconciliation file(s)
def reconcile( carrel, type, localLibrary=None, erase=False ) :

	'''Given the name of a carrel and a type ('author' or 'keyword'), (re-)initialize a recoconciliation file'''

	# configure
	PATTERN  = '*'
	AUTHORS  = [ 'id', 'author', 'qnumber' ]
	KEYWORDS = [ 'id', 'keyword', 'qnumber' ]
	TYPES    = [ 'authors', 'keywords' ]
	
	# require
	from   glob import glob
	from   pathlib import Path
	import pandas as pd
	import rdr
	import sys
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# sanity check #1
	checkForCarrel( carrel, localLibrary )
	
	# sanity check #2
	if type not in TYPES :
	
		click.echo( "Error: Unknown value for type (" + str( type ) + "); exiting", err=True )
		exit()
	
	# debug
	click.echo( 'Reconciling ' + type + " of " + carrel, err=True )

	# initialize
	authors  = localLibrary/carrel/( rdr.ETC )/( rdr.AUTHORS )
	keywords = localLibrary/carrel/( rdr.ETC )/( rdr.WRDS )
	with open( localLibrary/carrel/( rdr.ETC )/( rdr.STOPWORDS ) ) as handle : stopwords = handle.read().splitlines()	

	# check whether or not we've already been here, and get files to reconcile, conditionally
	if type == 'authors' :
			
		# check to see if the file ought to be overwritten
		if authors.exists() and erase == False :
	
			click.echo( "Warning: Authors reconciliation exists and erase is false, thus, not overwriting; exiting.\n", err=True )
			exit()
	
		# delete the existing reconcilation
		else: authors.unlink( missing_ok=True )

		# get the files to process
		files = glob( str( localLibrary/carrel/( rdr.BIB )/PATTERN ) )

	# check whether or we've already been here, and get files to reconcile, conditionally
	if type == 'keywords' :
			
		# check to see if the file ought to be overwritten
		if keywords.exists() and erase == False :
	
			click.echo( "Warning: Keywords reconciliation exists and erase is false, thus, not overwriting; exiting.\n", err=True )
			exit()
	
		# delete the existing reconcilation
		else: keywords.unlink( missing_ok=True )

		# get the files to process
		files   = glob( str( localLibrary/carrel/( rdr.WRD )/PATTERN ) )

	# create a dataframe of all records and process each; reconcile
	# see: https://stackoverflow.com/questions/48023061/pandas-read-csv-eof-inside-string-starting-at-line
	reconciliations = []
	records         = pd.concat( ( pd.read_csv( file, quoting=3, sep='\t', dtype={ 'id': str } ) for file in files ) )
	for index, record in records.iterrows() :
	
		
		# reconcile; here is where we add qnumbers from a dictionary
		if type == 'authors'  :
		
			reconciliation = [ record[ 'id' ], record[ 'author' ], '' ]
			reconciliations.append( reconciliation )

		if type == 'keywords' : 
		
			# check for stopwords
			if record[ 'keyword' ] not in stopwords :
			
				reconciliation = [ record[ 'id' ], record[ 'keyword' ], '' ]
				reconciliations.append( reconciliation )
		
	# create a dataframe of reconciliations, output, and done
	if type == 'authors' :
		reconciliations = pd.DataFrame( reconciliations, columns=AUTHORS )
		with open( authors, 'w' ) as handle : handle.write( reconciliations.to_csv( sep='\t', index=False ) )

	if type == 'keywords' :
		reconciliations = pd.DataFrame( reconciliations, columns=KEYWORDS )
		with open( keywords, 'w' ) as handle : handle.write( reconciliations.to_csv( sep='\t', index=False ) )


# given the name of a carrel, create zip file (index.zip) in its root
def carrel2zip( carrel, localLibrary=None ) :

	'''Given then name of a carrel, create a zip file (index.zip)
	in its root.'''

	# configure
	PERMISSION = 0o755

	# I don't know were to require these, here or at the root?
	from   pathlib import Path
	from   zipfile import ZipFile
	import os
	import rdr
	import shutil
	import tempfile
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# sanity check
	rdr.checkForCarrel( carrel, localLibrary )
	
	# initialize
	zip     = localLibrary/carrel/ZIP
	staging = tempfile.NamedTemporaryFile( delete=False ).name
	
	# debug
	click.echo( "Creating archive (index.zip) file of " + carrel, err=True )
	
	# make sane
	zip.unlink( missing_ok=True )
	os.chdir( localLibrary )
	
	# create an archive
	with ZipFile( staging, 'w' ) as handle :

		# find all files
		for root, _, files in os.walk( carrel ) :

			# process each file
			for file in files:
			
				# create full path name, debug, and do the work
				file = os.path.join( root, file )
				click.echo( file, err=True )
				handle.write( file )

	# put the archive into place and make it readable
	shutil.move( staging, zip )
	os.chmod( zip, PERMISSION )


# given a sentence, parser, and lexicon return matching sentences
def matchModal( sentence, parser, lexicon ) :
		
	'''Given a sentence, an NLTK RegexpParser object (a grammar), and a
	lexicon (a set of strings), return the sentence if it matches the
	object's grammar, otherwise return None.'''
	
	# require
	import nltk
	
	# normalize and tokenize
	tokens = nltk.word_tokenize( sentence.lower() )

	# check for given lexicon words
	if lexicon.intersection( set( tokens ) ) :

		# get parts-of-speech and create an NLTK tree
		pos  = nltk.pos_tag( tokens )
		tree = parser.parse( pos )
	
		# process matching branches of the tree
		for branch in tree.subtrees( lambda t : t.label() == 'GRAMMAR' ) :
		
			# get all subject words; re-check for words
			subjects = []
			leaves   = branch[ 0 ].leaves()
			for leaf in leaves : subjects.append( leaf[ 0 ] )
			if lexicon.intersection( set( subjects ) ) : return( sentence )
	

# given a sentence, parser, return matching sentences
def matchSVO( sentence, parser ) :
			
	'''Given a sentence and an NLTK RegexpParser parser object denoting
	a subject-verb-object grammar, return a list of subject-verb-object
	snippets if the grammar was found, otherwise return None.'''
	
	# require
	import nltk

	# initialize
	results = []
	
	# normalize and tokenize
	tokens = nltk.word_tokenize( sentence.lower() )

	# get parts-of-speech and create an NLTK tree
	pos  = nltk.pos_tag( tokens )
	tree = parser.parse( pos )

	# process each branch
	for branch in tree.subtrees( lambda t : t.label() == 'GRAMMAR' ) : 
			
		# process each limb
		for limb in [ branch[ 0 ], branch[ 1 ], branch[ 2 ] ] :
		
			# parse
			words  = []
			leaves = limb.leaves()
			for leaf in leaves : words.append( leaf[ 0 ] )
			results.append( ' '.join( words ) )
			
		# done
		return( results )
	

# given a file, return a line-delimited set of sentences
def extractSentences( file ) :

	'''Given a file name, return a list of strings where each
	string is a sentence.'''

	# require
	import nltk
	import re

	# initialize
	results = []
	
	# slurp up the given file; read the text
	with open( file, encoding='utf-8' ) as handle : text = handle.read()

	# get and process all sentences in the text
	sentences = nltk.sent_tokenize( text )
	for sentence in sentences : 
	
		# do rudimentary normalization and tokenization
		sentence = re.sub( '\n', ' ', sentence )
		sentence = re.sub( '\t', ' ', sentence )
		sentence = re.sub( ' +$', '', sentence )
		sentence = re.sub( '^ +', '', sentence )
		sentence = re.sub( ' +', ' ', sentence )
		sentence = re.sub( '- ', '',  sentence )
		sentence = re.sub( '- ', '',  sentence )
		
		# output
		results.append( sentence  )
	
	# done
	return( results )


# create or re-create the preferences/settings
def initializeConfigurations() :

	'''Given zero input, create or re-create the Toolbox's
	preferences/settings. Returns nothing.'''

	# require
	from configparser import ConfigParser
	from pathlib      import Path

	# initialize
	configurations       = ConfigParser()
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE

	# define defaults, and...
	configurations[ "RDR" ] = { "localLibrary"  : Path.home()/READERLIBRARY, 
								"malletHome"    : Path.home()/MALLETHOME,
								"notebooksHome" : Path.home()/NOTEBOOKSHOME,
								"tikaHome"      : Path.home()/TIKAHOME }

	# save them
	with open( str( configurationFile ), 'w', encoding='utf-8'  ) as handle : configurations.write( handle )

	# create the library directory
	( Path.home()/READERLIBRARY ).mkdir( exist_ok=True )


def configuration( name ) :

	'''Given a configuration name (localLibrary, malletHome,
	tikaHome, or notebooksHome) return the configuration's
	value.'''

	# require
	from configparser import ConfigParser
	from pathlib      import Path

	# initialize
	applicationDirectory = Path.home()
	configurationFile    = applicationDirectory/CONFIGURATIONFILE	
	configurations       = ConfigParser()
	
	# read configurations file
	configurations.read( str( configurationFile ) )
	
	# get configurations
	localLibrary  = configurations[ 'RDR' ][ 'localLibrary' ]
	malletHome    = configurations[ 'RDR' ][ 'malletHome' ] 
	tikaHome      = configurations[ 'RDR' ][ 'tikaHome' ] 
	notebooksHome = configurations[ 'RDR' ][ 'notebooksHome' ] 
	
	# done
	if   name == 'localLibrary'  : return( Path( localLibrary ) )
	elif name == 'malletHome'    : return( Path( malletHome ) )
	elif name == 'tikaHome'      : return( Path( tikaHome ) )
	elif name == 'notebooksHome' : return( Path( notebooksHome ) )
	else :
	
		# unknown configuration
		click.echo( f"Error: Unknown value for configuration name: { name }. Call Eric.", err=True )
		exit()
		

def modelNotFound() :

	'''When a spaCy model (as defined by the contants
	MODELSMALL and MODELMEDIUIM) is not found, this function is
	called. It prompts the user for a y or n answer, and if the
	answer is y, then the models are downloaded and installed. This
	function exits the application after being called.'''
	
	# notify
	click.echo( "Error: Langauge models not found.", err=True )
	click.echo()
	click.echo( f"This functions requires one of two different spaCy langauge models ({ MODELSMALL } and { MODELMEDIUM }) to be installed. This only has to be done once, and after the models have been installed you can run the command again.", err=True )
	click.echo()
	click.echo( 'Do you want to install the models now? [yn] ', err=True, nl=False )
	
	# get input
	c = click.getchar()
	click.echo()
	
	# branch accordingly; yes
	if c == 'y' :

		# require and do the work
		from os import system
		system( 'python -m spacy download ' + MODELSMALL )
		system( 'python -m spacy download ' + MODELMEDIUM )
	
	# no
	elif c == 'n' : click.echo( "Okay, but installing the model is necessary for this function to work. You'll be asked again next time.", err=True )

	# error
	else : click.echo( '???' )
	
	# done
	exit()


# make sure a study carrel exists
def checkForCarrel( carrel, localLibrary=None ) :

	'''Given the name of a study carrel, return True if it exists or False
	if it does not, but really, if the carrel does not exist, then execution
	is aborted.'''

	# require
	from pathlib import Path
	
	# initialize and do the work
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	directory = localLibrary/carrel
	if not directory.is_dir() :
		
		# error
		click.echo( ('''
  WARNING: The carrel, %s, does not seem to be in your local
  library. Are you sure you entered its name correctly? Try 'rdr
  catalog' to make sure.

  Alternatively, maybe you have moved the library and your settings
  are not up-to-date. If so, then use 'rdr get -s local' and/or
  'rdr set -s local' to rectify the issue.
''' % carrel ), err=True )
		exit()

	
# create a word cloud
def cloud( frequencies, **kwargs ) :

	'''Given a dictionary of tokens and their frequencies, create a word
	cloud in the form of a PNG file. If the optional file argument is
	supplied, then save the image accordingly. If not, then return the image
	itself.'''

	# configure
	HEIGHT = 960
	WIDTH  = 1280
	COLOR  = 'white'
	
	# require
	from wordcloud           import WordCloud
	import matplotlib.pyplot as plt

	# read optional arguments
	file = kwargs.get( 'file', None )

	# build the cloud
	wordcloud = WordCloud( width=WIDTH, height=HEIGHT, background_color=COLOR )
	wordcloud.generate_from_frequencies( frequencies )

	# save
	if file : wordcloud.to_file( file )
		
	# display
	else :
	
		# plot
		plt.figure()
		plt.imshow( wordcloud )
		plt.axis( "off" )
		plt.show()

	# done
	return True


# read and parse provenance data
def provenance( carrel, field, localLibrary=None ) :

	'''Given the name of a study carrel and a provenance element (process,
	originalID, dateCreated, timeCreated, creator, or input), return the
	provenance value.'''
	
	# require
	from pathlib import Path
	
	# initialize
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel, localLibrary )

	# read provenance file
	with open( localLibrary/carrel/PROVENANCE, encoding='utf-8'  ) as handle : provenance = handle.read().split( '\t' )
	
	# parse it
	process     = provenance[ 0 ]
	originalID  = provenance[ 1 ]
	dateCreated = provenance[ 2 ]
	timeCreated = provenance[ 3 ]
	creator     = provenance[ 4 ]
	input       = provenance[ 5 ][:-1]

	# map
	if field   == 'process'     : value = process
	elif field == 'originalID'  : value = originalID
	elif field == 'dateCreated' : value = dateCreated
	elif field == 'timeCreated' : value = timeCreated
	elif field == 'creator'     : value = creator
	elif field == 'input'       : value = input
	
	# done
	return value
	
	
# return various extents
def extents( carrel, type, localLibrary=None ) :

	'''Given the name of a study carrel and a type of extent (items, words,
	or flesch) return the extent value.'''
	
	# require
	import sqlite3
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row

	# get extents
	sql = 'SELECT COUNT( id ) AS items, SUM( words ) AS words, AVG( flesch ) AS flesch FROM bib;'
	rows = connection.execute( sql )
	for row in rows :

		items  = row[ 'items' ]
		words  = row[ 'words' ]
		flesch = str( int( row[ 'flesch' ] ) )

	if type == 'items'    : value = int( items )
	elif type == 'words'  : value = int( words )
	elif type == 'flesch' : value = int( flesch )
	
	return value


# escape ampersands
def escape( s ) :

	from html import escape
	if not s : return
	return escape( s )

# output a rudimentary bibliography
def bibliography( carrel, localLibrary=None, format='text', save=False ) :

	'''Given the name of a study carrel, and a format (text or
	json), create a rudimentary bibliography. If the value for save is
	True, then the bibliography will be saved in the carrel's etc
	directory/folder, otherwise the bibliography is returned.'''

	# require
	import sqlite3
	from pathlib import Path
	import json
	
	# initialize
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row

	# query database
	sql  = '''SELECT b.id, b.words, b.extension, b.flesch, b.author, b.title, b.date, GROUP_CONCAT( LOWER( w.keyword ), '; ') AS keywords, b.summary, b.mime
			  FROM bib AS b, wrd AS w
			  WHERE b.id = w.id
			  GROUP BY b.id
			  ORDER BY b.id, LOWER( b.author );'''
	rows  = connection.execute( sql )
	rows  = rows.fetchall()
	connection.close()

	# branch according to format
	if format   == 'json' : bibliography = json.dumps( [ dict( row ) for row in rows ] )
		
	elif format == 'text' :
	
		# initialize
		total        = len( rows )
		bibliography = ''
		
		# process each row
		for item, row in enumerate( rows ) :

			# parse
			id        = str( row[ 'id' ] )
			author    = row[ 'author' ]
			title     = row[ 'title' ]
			date      = row[ 'date' ]
			words     = row[ 'words' ]
			flesch    = row[ 'flesch' ]
			summary   = row[ 'summary' ]
			keywords  = row[ 'keywords' ]

			# normalize; unescape
			if summary : summary = summary.replace( "''", "'" )
	
			# a hack for the lack of an extension
			if not row[ 'extension' ] : extension = ''
			else                      : extension = row[ 'extension' ]
			
			# build cache and plain text
			#cache = str( locallibrary/carrel/CACHE/id ) + extension
			#text  = str( locallibrary/carrel/TXT/id )   + '.txt'
	
			if format == 'text' :
			
				#cache = str( localLibrary/carrel/CACHE/id ) + extension
				#text  = str( localLibrary/carrel/TXT/id )   + '.txt'
				
				cache = id + extension
				text  = id + '.txt'
				
				# build the bibliography
				bibliography = bibliography + ( '        item: #%s of %s\n' % ( str( item + 1 ), total ) )
				bibliography = bibliography + ( '          id: %s\n' % id )
				bibliography = bibliography + ( '      author: %s\n' % author )
				bibliography = bibliography + ( '       title: %s\n' % title )
				bibliography = bibliography + ( '        date: %s\n' % date )
				bibliography = bibliography + ( '       words: %s\n' % words )
				bibliography = bibliography + ( '      flesch: %s\n' % flesch )
				bibliography = bibliography + ( '     summary: %s\n' % summary )
				bibliography = bibliography + ( '    keywords: %s\n' % keywords )
				bibliography = bibliography + ( '       cache: %s\n' % cache )
				bibliography = bibliography + ( '  plain text: %s\n' % text )
				bibliography = bibliography + '\n'
	else : exit( "Unknown value for format (" + str( format ) + ") in call to bibliography. Call Eric." )
	
	if save :

		if format == 'text' : file = localLibrary/carrel/BIBLIOGRAPHYTEXT
		if format == 'html' : file = localLibrary/carrel/BIBLIOGRAPHYHTML
		if format == 'json' : file = localLibrary/carrel/BIBLIOGRAPHYJSON
		
		with open( file, 'w', encoding='utf-8' ) as handle : handle.write( bibliography )
		
	else : return bibliography
	

# get email addresses
def addresses( carrel, count=False, like=None ) :

	'''Given the name of a study carrel, a value for count (True or
	False), and a like statement (a string), return a line-delimited
	list of email addresses. The like statement is expected to be
	something such as ".com" or "gmail", and it is intended as a
	filtering device. If the value for count is True, then the result
	will delimited by a tab character where the first column is an email
	address and the second column is the address's frequency.'''

	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# dump a sorted list of all email addresses
	if not count :

		# articulate sql
		if like :
		
			sql = ( '''SELECT DISTINCT( LOWER( address ) ) AS address
			           FROM adr
			           WHERE address LIKE "%s"
			           ORDER BY address;''' % ('%' + like + '%' ) )
			
		else :
		
			sql  = '''SELECT DISTINCT( LOWER( address ) ) AS address
			          FROM adr
			          ORDER BY address;'''

		# do the work and build the result
		rows = connection.execute( sql )
		for row in rows : items.append( row[ 'address' ]  )

	# count and tabulate the dump
	else :
	
		# articulate sql
		if like :
		
			sql = ( '''SELECT LOWER( address ) AS address, COUNT( LOWER( address ) ) AS count
			           FROM adr
			           WHERE address LIKE "%s"
			           GROUP BY LOWER( address )
			           ORDER BY count DESC, address;''' % ('%' + like + '%' ) )
			
		else :
		
			sql  = '''SELECT LOWER( address ) AS address, COUNT( LOWER( address ) ) AS count
			          FROM adr
			          GROUP BY LOWER( address )
			          ORDER BY count DESC, address;'''

		# do the work and build the result
		rows = connection.execute( sql )
		for row in rows : items.append( "\t".join( [ row[ 'address' ], str( row[ 'count' ] ) ] ) )		

	# clean up and done
	connection.close()
	return '\n'.join( items )


def urls( carrel, select='url', count=False, like=None ) :

	'''Given the name of a study carrel, a select value (url or domain),
	a value for count (True or False), and a like statement (a string),
	return a line-delimited list of urls or domains.'''
	
	# require
	import sqlite3

	# sanity check
	checkForCarrel( carrel )

	# initialize
	locallibrary           = configuration( 'localLibrary' )
	connection             = sqlite3.connect( str( locallibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# dump a sorted list of all urls
	if select == 'url' :
	
		# don't count
		if not count :
		
			# simple filter
			if like :
			
				# articulate sql
				sql = ( '''SELECT DISTINCT( url ) AS url
				           FROM url
				           WHERE url LIKE "%s"
				           ORDER BY url;''' % ( '%' + like + '%' ) )

			# just dump; articulate sql
			else : sql = 'SELECT DISTINCT( url ) AS url FROM url ORDER BY url;'

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : items.append( row[ 'url' ] )

		# count
		else :
		
			# simple filtering
			if like :
			
				# articulate sql
				sql = ( '''SELECT DISTINCT( url ) AS url, COUNT( DISTINCT( url ) ) AS count
				           FROM url
				           WHERE url LIKE '%s'
				           GROUP BY url
				           ORDER BY count DESC;''' % ( '%' + like + '%' ) )
				            
			# no filtering
			else :

				# articulate sql
				sql = '''SELECT DISTINCT( url ) AS url, COUNT( DISTINCT( url ) ) As count
				         FROM url
				         GROUP BY url
				         ORDER BY count DESC;'''

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'url' ], str( row[ 'count' ] ) ] ) )
			
	# domains; count and tabulate the dump
	else :
	
		# no counting
		if not count :
		
			# filter
			if like :
			
				# articulate sql, search, and output
				sql = ( '''SELECT LOWER( DISTINCT( domain ) ) AS domain
				           FROM url
				           WHERE url LIKE '%s'
				           ORDER BY domain;''' % ( '%' + like + '%' ) )

			# no filtering
			else : sql = 'SELECT LOWER( DISTINCT( domain ) ) AS domain FROM url ORDER BY domain;'

			# do the work and output
			rows = connection.execute( sql )
			for row in rows : item.append( row[ 'domain' ] )
		
		# count and tabulate
		else :
		
			# filter
			if like :
			
				# articulate sql, search, and output
				sql = ( '''SELECT LOWER( DISTINCT( domain ) ) AS domain, COUNT( LOWER( DISTINCT( domain ) ) ) AS count
				           FROM url
				           WHERE domain LIKE '%s'
				           GROUP BY domain
				           ORDER BY count DESC, domain;''' % ( '%' + like + '%' ) )

			# no filtering
			else :
			
				# articulate sql, search, and output
				sql = '''SELECT LOWER( DISTINCT( domain ) ) AS domain, COUNT( LOWER( DISTINCT( domain ) ) ) AS count
				         FROM url
				         GROUP BY domain
				         ORDER BY count DESC, domain;'''
				         
			# do the work and output
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'domain' ], str( row[ 'count' ] ) ] ) )
			
	# clean up and done
	connection.close()
	return '\n'.join( items )


def keywords( carrel, localLibrary=None, count=False, wordcloud=False, save=False ) :

	'''Given the name of a study carrel, return a new-line delimited
	list of keywords denoted by the build process. If count it True,
	then the list of keywords is counted, tabulated, and sorted in
	descending order by frequency. If count is True and wordcloud is
	True, then a visualization of the frequencies is returned. If count
	is True, wordcloud is True, and save is True, then the visualization
	is saved in the given carrel's etc directory as defined by the
	constant KEYWORDSCLOUD.

	Admittedly, this function, like many of the functions, is convoluted;
	this function ought to return more standard data structures, not
	line-delimited lists containing tab-delimited values. My bad. '''

	# require
	import sqlite3
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	stopwords              = open( str( localLibrary/carrel/ETC/STOPWORDS ), encoding='utf-8' ).read().splitlines()

	# dump a sorted list of all keywords
	if not count :

		# articulate sql, search, and output
		sql  = 'SELECT DISTINCT( LOWER( keyword ) ) AS keyword FROM wrd ORDER BY LOWER( keyword );'
		rows = connection.execute( sql )
		for row in rows : items.append( row[ 'keyword' ] )

	# count and tabulate the dump
	else :
	
		# articulate sql, search, and output
		sql  = 'SELECT LOWER( keyword ) AS keyword, COUNT( LOWER( keyword ) ) AS count FROM wrd GROUP BY LOWER( keyword ) ORDER BY count DESC, keyword;'
		rows = connection.execute( sql )
		
		# output a simple list
		if not wordcloud :
			
			for row in rows : 
		
				# output, conditionally; weird
				if row[ 'keyword' ] : 
				
					# make sure the value is not in the stopwords
					if row[ 'keyword' ] not in stopwords : items.append( "\t".join( [ row[ 'keyword' ], str( row[ 'count' ] ) ] ) )			

		# output a word cloud
		else :
			
			# create a list of frequencies
			frequencies = {}
			for row in rows :
			
				# make sure the row has a value
				if row[ 'keyword' ] :
				
					# make sure the value is not in the stopwords
					if row[ 'keyword' ] not in stopwords : frequencies[ row[ 'keyword' ] ] = row[ 'count' ]
			
			if not save : cloud( frequencies )
			else :
			
				file = localLibrary/carrel/FIGURES/KEYWORDSCLOUD
				cloud( frequencies, file=file )

	# clean up and done; the result might be empty, which is sort of bogus
	connection.close()
	return '\n'.join( items )


# poor man's search engine
def concordance( carrel, localLibrary=None, query='love', width=40 ) :

	'''Given the name of a study carrel, a query, and a window, return a
	list of lines matching the query fro the given carrel'''

	# require
	import re
	import rdr
	from pathlib import Path
	
	# slurp up the corpus
	if localLibrary : library = Path( localLibrary )
	else            : library = rdr.configuration( 'localLibrary' )
		
	# sanity check
	checkForCarrel( carrel, localLibrary )
	
	with open( library/carrel/rdr.ETC/rdr.CORPUS, encoding='utf-8'  ) as handle : corpus = handle.read()


	# initialize
	snippets = []

	# find and process all positions matching the query; finditer does the magic
	matches = re.finditer( '\\b' + query + '\\b', corpus )
	for match in matches :
	
		# re-initialize
		start = match.start()
		end   = match.end()
		
		# get the characters before and after the query
		before = corpus[ start - width : start ]
		after  = corpus[ end            : end + width ]

		# build the whole snippet and update
		snippet = before + ' ' + query + ' ' + after
		snippet = snippet.replace( '  ' , ' ' )
		snippets.append( snippet )	
	
	# done
	return( snippets )


# get sizes (measured in words) of documents
def sizes( carrel, localLibrary=None, sort='words', output='list', save=False ) :

	'''Given a the name of study carrel, output a newline-delimited list of
	study carrel item identifiers and the number of words (size) of the
	given item. Each item/number of words combination is a tab-delimited
	value. The value of sort can be "words" or anything else. If it is
	anything else, then the output is sorted by item identifier. The value
	of "output" can be list, histogram, or boxplot. If the value is
	histogram or boxplot, then the the result is visualized. If the value of
	output is histogram or boxplot, and the value of save is True, then the
	result is saved in the carrel's figures directory as specified by the
	constants SIZESHISTOGRAM or SIZESBOXPLOT.

	Like many of the functions in this library, this function ought to be
	re-written to return more Pythonic data structures as opposed to
	newline-delimited lists subdivided into tab-delimited pairs. Such works
	will in a terminal environment, but not so well as an application
	programmer interface. My bad.'''

	# configure
	WORDS   = 'SELECT id, words FROM bib ORDER BY words DESC'
	ID      = 'SELECT id, words FROM bib ORDER BY id ASC'
	COLUMNS = [ 'sizes in words' ]
	
	# require
	import matplotlib.pyplot as plt
	import pandas as pd
	import sqlite3
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# find all rows
	if sort == 'words' : rows = connection.execute( WORDS )
	else               : rows = connection.execute( ID )
		
	# branch according to given output; simple list
	if output == 'list' :
	
		# process each row; output tab-delimited list
		for row in rows : items.append( '\t'.join( [ str( row[ 'id' ] ), str( row[ 'words' ] ) ]) )   
   
	# output charts
	else :
			
		# create a simple list of words, and store it in a dataframe
		records = []
		for row in rows :
		
			if not row[ 'words' ] : words = 0
			else                  : words = row[ 'words' ]
			
			# using try is a hack; need to fix this
			#records.append( int( row[ 'words' ] ) )
			try : records.append( int( words ) )
			except ValueError : continue
		df = pd.DataFrame( records, columns=COLUMNS )

		# initialize the plot
		figure, axis = plt.subplots()
		
		# plot
		if output == 'histogram' : 
		
			df.hist( ax=axis )
			if save : plt.savefig( localLibrary/carrel/FIGURES/SIZESHISTOGRAM )
			else    : plt.show()

		else :
		
			df.boxplot( ax=axis )		
			if save : plt.savefig( localLibrary/carrel/FIGURES/SIZESBOXPLOT )
			else    : plt.show()
		
	# clean up
	connection.close()
	return '\n'.join( items )


# get readability scores
def flesch( carrel, localLibrary=None, sort='score', output='list', save=False) :

	'''Given the name of study carrel, output a newline-delimited list of
	study carrel item identifiers and the readability (Flesch) score of each
	item. Each item/score combination is a tab-delimited value. The value of
	sort can be "score" or anything else. If it is anything else, then the
	output is sorted by item identifier. The value of "output" can be list,
	histogram, or boxplot. If the value is histogram or boxplot, then the
	the result is visualized. If the value of output is histogram or
	boxplot, and the value of save is True, then the result is saved in the
	carrel's figures directory as specified by the constants
	READABILITYHISTOGRAM or READABILITYBOXPLOT.

	Like many of the functions in this library, this function ought to be
	re-written to return more Pythonic data structures as opposed to
	newline-delimited lists subdivided into tab-delimited pairs. Such works
	will in a terminal environment, but not so well as an application
	programmer interface. My bad.'''

	# configure
	SCORE   = 'SELECT id, flesch FROM bib ORDER BY flesch DESC'
	ID      = 'SELECT id, flesch FROM bib ORDER BY id ASC'
	COLUMNS = [ 'readability' ]
	
	# require
	import matplotlib.pyplot as plt
	import pandas as pd
	import sqlite3
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# find all rows
	if sort == 'score' : rows = connection.execute( SCORE )
	else               : rows = connection.execute( ID )
		
	# branch according to given output; simple list
	if output == 'list' :
	
		# process each row; output tab-delimited list
		for row in rows : items.append( '\t'.join( [ row[ 'id' ], str( row[ 'flesch' ] ) ] ) )   
   
	# output charts
	else :
			
		# create a simple list of words, and store it in a dataframe
		records = []
		for row in rows : 
		
			# a hack for keough; be forewarned
			try : records.append( int( row[ 'flesch' ] ) )
			except ValueError : pass
			except TypeError : pass
			
		df = pd.DataFrame( records, columns=COLUMNS )

		# initialize the plot
		figure, axis = plt.subplots()

		# plot
		if output == 'histogram' : 
		
			df.hist( ax=axis )
			if save : plt.savefig( localLibrary/carrel/FIGURES/READABILITYHISTOGRAM )
			else    : plt.show()

		else :
		
			df.boxplot( ax=axis )		
			if save : plt.savefig( localLibrary/carrel/FIGURES/READABILITYBOXPLOT )
			else    : plt.show()

	# clean up
	connection.close()
	return '\n'.join( items )


# compute ngrams
def ngrams( carrel, localLibrary=None, size=1, query=None, count=False, location='local', wordcloud=False, save=False ) :

	'''Given the name of a study carrel, output a newline-delimited list of
	ngrams in the carrel. The value of size denotes the number of ngrams to
	output on each line. If the value of size is 1 or 2, then stopwords are
	removed from the output. The output can be filtered using the query
	parameter, which supports regular expressions. If the value of count is
	True, then each item in the resulting list of ngrams is counted and
	tabulated. The value of location can be "local" or "remote". If the
	value is local, then the given carrel is expected to be on the local
	file system. If the value is "remote", then the carrel is expected to be
	available on the Distant Reader Library as defined by the constant
	REMOTELIBRARY. If the value of count is True and the value of wordcloud
	is True, then the result is visualized. If the value of count is True,
	wordcloud is True, and save is True, then the visualization is saved in
	the carrel's figures directory as denoted by the constants UNIGRAMSCLOUD
	or BIGRAMSCLOUD. The automatic saving of visualization's of ngrams
	greater than 2 is not supported.''' 

	# configure
	LIMIT = 200
	
	# require
	from re       import search
	from requests import get
	import nltk
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# branch according to location; local
	if location == 'local' :
	
		# sanity check
		checkForCarrel( carrel, localLibrary )
		
		# read local data
		stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ), encoding='utf-8' ).read().split()
		text         = open( str( localLibrary/carrel/ETC/CORPUS ), encoding='utf-8' ).read()
	
	# remote
	elif location == 'remote' :
	
		# read remote data; needs error checking
		stopwords = get( '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, ETC, STOPWORDS ] ) ).text.split()
		text      = get( '/'.join ( [ REMOTELIBRARY, CARRELS, carrel, ETC, CORPUS ] ) ).text
		
	# error
	else :
	
		# click ought to prevent this, but just in case
		click.echo( "Error: Unknown value for location: { location }. Call Eric.", err=True )
		exit()
			
	# read, tokenize, and normalize the text
	tokens = nltk.word_tokenize( text, preserve_line=True )
	tokens = [ token.lower() for token in tokens if token.isalpha() ]
	
	# create the set of ngrams
	ngrams = list( nltk.ngrams( tokens, size ) )
	
	# filter, conditionally
	if query :
	
		# initialize and process each ngram
		filtered = []
		for ngram in ngrams :
			
			# check and update
			if search( query, ' '.join( ngram ) ) : filtered.append( ngram )
		
		# done
		ngrams = filtered

	# remove stopwords from unigrams or bigrams
	if size < 3 :
	
		# initialize
		results = []
		
		# process each ngram
		for ngram in ngrams :

			# re-initialize
			found = False
			
			# process each token in the ngram
			for token in ngram :

				# check for stopword
				if token in stopwords : found = True
	
			# conditionally update the results
			if not found : results.append( ngram )

		# done; make it read pretty
		ngrams = results
		
	# output; human
	if count :
	
		# initialize a dictionary and process each ngram
		frequencies = {}
		for ngram in ngrams :

			# update the dictionary
			if ngram in frequencies : frequencies[ ngram ] += 1
			else                    : frequencies[ ngram ]  = 1

		# sort the dictionary
		ngrams = sorted( frequencies.items(), key=lambda x:x[ 1 ], reverse=True )
		
		if not wordcloud :
		
			results = []
			
			# process each ngram
			for ngram in ngrams :
			
				# create a record and output
				results.append( '\t'.join( list( ngram[ 0 ] ) ) + '\t' + str( ngram[ 1 ] ) )
				
			return '\n'.join( results )
							
		else :
		
			# limit the number of ngrams; we can't visualize a huge number
			ngrams = ngrams[ :LIMIT ]
			
			# coerce the result into a dictionary of frequencies
			frequencies = {}
			for ngram in ngrams : frequencies[ ' '.join( ngram[ 0 ] ) ] = ngram[ 1 ]
			
			# simply output
			if not save : cloud( frequencies )

			# save to the corresponding figures directory
			else :
			
				# unigrams
				if size == 1 :
				
					# configure and save
					file = localLibrary/carrel/FIGURES/UNIGRAMSCLOUD
					cloud( frequencies, file=file )
					
				# bigrams
				elif size == 2 :
				
					# configure and save
					file = localLibrary/carrel/FIGURES/BIGRAMSCLOUD
					cloud( frequencies, file=file )
				
				# unsupported
				else : click.echo( "The save option is only valid for unigrams and bigrams; there is no default location for anything else.", err=True )
				
	# power user
	else :
		
		results = []
	
		# output raw data, and hope sort, uniq, grep, and less are used
		for ngram in ngrams : results.append( "\t".join( list( ngram ) ) )
		return '\n'.join( results )


# process parts-of-speech
def pos( carrel, localLibrary=None, select='parts', like='any', count=False, normalize=True, wordcloud=False, save=False ) :

	'''Given the name of a study carrel, return various
	incarnations of parts-of-speech (pos) values.

	If the value of select is "parts" (the default), then a
	newline-delimited list of pos values are returned for each
	and every word in the carrel. If the value of select is
	"words", then all of the words (tokens) are returned. If the
	value of select is anything else, then the lemmas of each
	token is returned.

	The value of like is akin to an SQL LIKE commands enabling
	the developer to limit the shape of the select value. For
	eample, if the value of select is "parts", then only nouns
	can be returned if the value for like is "N".

	If count is True, then the result is counted, tabulated, and
	sorted by frequency in descending order.

	If normalize is True, the values of select are lower-cased.

	If count is True and wordcloud is True, then the frequencies
	are visualized as a wordcloud.

	If count is True, wordcloud is True, and save is True, then
	the resulting wordcloud is saved in the carrel's etc
	directory, but only for a limited number of values for like
	(NOUN, VERB, PRON, ADJ, PROPN, and ADV).'''
	
	# require
	import sqlite3
	from pathlib import Path
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# branch accordingly; parts-of-speech
	if select == 'parts' :
	
		# initialize like
		if like == 'any' : like = '%'
		else             : like = like.upper() + '%'
		
		# dump parts-of-speech tags
		if not count :

			# articulate sql, search, and output
			sql  = ( "SELECT pos FROM pos WHERE pos LIKE '%s';" % like )
			rows = connection.execute( sql )
			for row in rows : items.append( row[ 'pos' ] )

		# count and tabulate the dump
		else :
		
			# articulate sql, search, and output
			sql  = ( "SELECT pos, COUNT( pos ) AS count FROM pos WHERE pos LIKE '%s' GROUP BY pos ORDER BY count DESC;" % like )
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'pos' ], str( row[ 'count' ] ) ] ) )			
			
	# words or lemmas
	else : 
	
		# initialize select
		if select == 'words' : select = 'token'
		else                 : select = 'lemma'
		
		# initialize like
		if like == 'any' : like = '%'
		else             : like = like.upper() + '%'
		
		# simply dump the desired content
		if not count :
		
			# build sql
			if not normalize : sql = ( 'SELECT %s FROM pos WHERE pos LIKE "%s";' % ( select, like ) )
			else : sql = ( 'SELECT LOWER( %s ) AS %s FROM pos WHERE pos LIKE "%s";' % ( select, select, like ) )
						
			# search and process each resulting row
			rows = connection.execute( sql )
			for row in rows : items.append( row[ select ] )
		
		# count and tabulate the result
		else:

			# do not lower-case words or lemmas
			if not normalize : sql = ( '''SELECT %s AS %s, COUNT( %s ) AS count
			                              FROM pos
			                              WHERE pos LIKE "%s"
			                              GROUP BY %s
			                              ORDER BY count DESC;''' % ( select, select, select, like, select ) )
				
			# lower-case words or lemmas
			else: sql = ( '''SELECT LOWER( %s ) AS %s, COUNT( %s ) AS count
			                 FROM pos
			                 WHERE pos LIKE "%s"
			                 GROUP BY LOWER( %s )
			                 ORDER BY count DESC;''' % ( select, select, select, like, select ) )
				
			# search and process each resulting row
			rows = connection.execute( sql )

			# output simple tabulation
			if not wordcloud :
			
			
				# dump
				for row in rows :
				
					if row[ select ] : items.append( "\t".join( [ row[ select ], str( row[ 'count' ] ) ] ) )
			
			# output word cloud
			else :
			
				# create a dictionary of frequencies
				frequencies = {}
				for row in rows : frequencies[ row[ select ] ] = row[ 'count' ]

				# simply output
				if not save : cloud( frequencies )
			
				# save to the corresponding figures directory
				else :
			
					# configure
					#localLibrary = configuration( 'localLibrary' )

					# nouns
					if like == 'NOUN%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSNOUN
						cloud( frequencies, file=file )
				
					# org
					elif like == 'VERB%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSVERB
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'PRON%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSPRON
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'ADJ%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSADJ
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'PROPN%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSPROPN
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'ADV%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/POSADV
						cloud( frequencies, file=file )
				
					# unsupported
					else : click.echo( "The save option is only valid for types NOUN, VERB, PRON, ADJ, PROPN, and ADV; there is no default location for anything else.", err=True )

				# return nothing when wordclouding
				return
		
	# clean up and done
	connection.close()
	return '\n'.join( items )


# process named entities
def entities( carrel, localLibrary=None, select='type', like='any', count=False, wordcloud=False, save=False ) :

	'''Given the name of a study carrel, return various
	incarnations of named-entity values.

	If the value of select is "type" (the default), then a
	newline-delimited list of entity values are returned for each
	and every word in the carrel. If the value of select is
	"entity", then all of the named-entities are returned.

	The value of like is akin to an SQL LIKE command enabling the
	developer to limit the shape of the select value. For
	example, if the value of select is "entity", then only
	people's names will be returned if the value for like is
	"PERSON".

	If count is True, then the result is counted, tabulated, and
	sorted by frequency in descending order.

	If count is True and wordcloud is True, then the frequencies
	are visualized as a wordcloud.

	If count is True, wordcloud is True, and save is True, then
	the resulting wordcloud is saved in the carrel's etc
	directory, but only for a limited number of values for like
	(any, PERSON, ORG, and GPE).'''

	# require
	import sqlite3
	from pathlib import Path

	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# sanity check
	checkForCarrel( carrel, localLibrary )

	# initialize
	connection             = sqlite3.connect( str( localLibrary/carrel/ETC/DATABASE )  )
	connection.row_factory = sqlite3.Row
	items                  = []
	
	# branch accordingly; types of entities
	if select == 'type' :
	
		# dump
		if not count :

			# articulate sql, search, and output
			sql  = 'SELECT type FROM ent;'
			rows = connection.execute( sql )
			for row in rows : items.append( row[ 'type' ] )

		# count and tabulate the dump
		else :
		
			# articulate sql, search, and output
			sql  = 'SELECT type, COUNT( type ) AS count FROM ent GROUP BY type ORDER BY count DESC;'
			rows = connection.execute( sql )
			for row in rows : items.append( "\t".join( [ row[ 'type' ], str( row[ 'count' ] ) ] ) )			
			
	# entities
	else : 
			
		# initialize like
		if like == 'any' : like = '%'
		else             : like == like.upper()
		
		# simply dump the desired content
		if not count :
		
			# build sql, search, and output
			sql  = ( 'SELECT entity FROM ent WHERE type LIKE "%s";' % ( like ) )
			rows = connection.execute( sql )
			for row in rows : items.append( row[ select ] )
		
		# count and tabulate the result
		else:

			# build sql, search, and output
			sql  = ( 'SELECT entity, COUNT( entity ) AS count FROM ent WHERE type LIKE "%s" GROUP BY entity ORDER BY count DESC;' % ( like ) )
			rows = connection.execute( sql )
			
			# output simple tabulation
			if not wordcloud :
			
				# dump
				for row in rows :
				
					# make sure the row value is sane; a hack
					if ( row[ select ] ) : items.append( "\t".join( [ row[ select ], str( row[ 'count' ] ) ] ) )
			
			# output word cloud
			else :
			
				# create a dictionary of frequencies
				frequencies = {}
				for row in rows : frequencies[ row[ select ] ] = row[ 'count' ]

				# simply output
				if not save : cloud( frequencies )
			
				# save to the corresponding figures directory
				else :
			
					# any
					if like == '%' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESANY
						cloud( frequencies, file=file )
					
					# persons
					elif like == 'PERSON' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESPERSON
						cloud( frequencies, file=file )
				
					# org
					elif like == 'ORG' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESORG
						cloud( frequencies, file=file )
				
					# geo-political entities (places)
					elif like == 'GPE' :
				
						# configure and save
						file = localLibrary/carrel/FIGURES/ENTITIESGPE
						cloud( frequencies, file=file )
				
					# unsupported
					else : click.echo( "The save option is only valid for entities of type any, PERSON, ORG, or GPE; there is no default location for anything else.", err=True )

				# when wordclouding, return nothing
				return
				
	# clean up
	connection.close()
	return '\n'.join( items )


# do feature reduction and visualize
def cluster( carrel, localLibrary=None, type='dendrogram', save=False ) :

	'''Given the name of a study carrel, use PCA to reduce the
	carrel's content to two or three dimensions and then
	visualize the result. If the value of type is "dendrogram",
	then reducd to two dimensions, and if the value of type is
	"cube", then reduce to three dimensions. If the value of save
	is True, then save the resulting image in the carrel's
	figures directory.'''
	
	# configure
	MAXIMUM   = 0.95
	MINIMUM   = 2
	EXTENSION = '.txt'

	# require
	from os                              import path, system, listdir
	from scipy.cluster.hierarchy         import ward, dendrogram
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.manifold                import MDS
	from sklearn.metrics.pairwise        import cosine_similarity
	import matplotlib.pyplot             as     plt
	from pathlib import Path
	
	# ignore warnings; probably not the greatest idea
	import warnings
	warnings.filterwarnings("ignore")

	# initialize
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel, localLibrary )

	stopwords    = open( str( localLibrary/carrel/ETC/STOPWORDS ), encoding='utf-8' ).read().split()
	directory    = localLibrary/carrel/TXT
	filenames    = [ path.join( directory, filename ) for filename in listdir( directory ) ]
	vectorizer   = TfidfVectorizer( input='filename', max_df=MAXIMUM, min_df=MINIMUM, stop_words=stopwords )
	matrix       = vectorizer.fit_transform( filenames ).toarray()
	distance     = 1 - cosine_similarity( matrix )
	keys         = [ path.basename( filename ).replace( EXTENSION, '' ) for filename in filenames ] 

	# branch according to type; dendrogram
	if type == 'dendrogram' :
		linkage_matrix = ward( distance )
		dendrogram( linkage_matrix, orientation="right", labels=keys )
		plt.tight_layout() 

	# cube
	elif type == 'cube' :
		mds = MDS( n_components=3, dissimilarity="precomputed", random_state=1 )
		pos = mds.fit_transform( distance )
		fig = plt.figure()
		ax  = fig.add_subplot( 111, projection='3d' )
		ax.scatter( pos[ :, 0 ], pos[ :, 1 ], pos[ :, 2 ] )
		for x, y, z, s in zip( pos[ :, 0 ], pos[ :, 1 ], pos[ :, 2 ], keys ) : ax.text( x, y, z, s )

	# save, or not
	if save :
	
		if type == 'dendrogram' : plt.savefig( localLibrary/carrel/FIGURES/CLUSTERDENDROGRAM )
		else                    : plt.savefig( localLibrary/carrel/FIGURES/CLUSTERCUBE )
		
	else : plt.show()

	# done
	return
	
# process collocations
def collocate( carrel, window=4, filter=4, measure='chisqr', limit=4000, output='image', save=False ) :

	'''Given the name of study carrel, collocate carrel's content
	and output either an image or a Graph Modeling Language (GML)
	file. This function is an implementation of the
	nltk.collocations.BigramAssocMeasures method.

	The value of window denotes the number of words on either
	side of a given word.

	The value of filter is used to denote the number of times a
	collocation must appear in order to be retained.

	The value of measure can be any one of 'chisqr', 'jaccard',
	'likelihood', 'raw', or 'fisher'. They are used to measure
	the significance of each collocation. See the NLTK
	documentation for details.

	The value of limit is used to approxmiate the total number of
	collocations desired.

	If the value of output is "image", then the collocations are
	internally manifested as a GML file, and a visualization is
	returned. If the value is "gml", then the GML file is
	returned.

	If the value of output is "gml", and the value of save is
	True, then the resulting GML file is saved in the carrel's
	etc directory with the value of the constant named
	COLLOCATIONS. The resulting GML file is intended to be
	visualized with something like Gephi.'''
	
	# require
	from   nltk.collocations import BigramAssocMeasures
	import matplotlib.pyplot as plt
	import networkx as nx
	import nltk
	import sys
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	corpus       = str( localLibrary/carrel/ETC/CORPUS )
	stopwords    = str( localLibrary/carrel/ETC/STOPWORDS )

	# sanity checks
	checkForCarrel( carrel )
		
	# read the stop words and the carrel
	with open( stopwords, encoding='utf-8' ) as handle : stopwords = handle.read().split( '\n' )
	with open( corpus, encoding='utf-8' )    as handle : corpus    = handle.read()

	# featurize the carrel
	features = nltk.word_tokenize( corpus )
	features = [ feature for feature in features if feature.isalpha() ]
	features = [ feature.lower() for feature in features ]
	features = [ feature for feature in features if feature not in stopwords ]

	# collocate
	finder = nltk.BigramCollocationFinder.from_words( features, window_size=window )
	
	# filter
	if filter > 0 : finder.apply_freq_filter( filter )
	
	# measure
	if   measure == 'chisqr'     : records = finder.score_ngrams( BigramAssocMeasures.chi_sq )
	elif measure == 'jaccard'    : records = finder.score_ngrams( BigramAssocMeasures.jaccard )
	elif measure == 'likelihood' : records = finder.score_ngrams( BigramAssocMeasures.likelihood_ratio )
	elif measure == 'raw'        : records = finder.score_ngrams( BigramAssocMeasures.raw_freq )
	elif measure == 'fisher'     : records = finder.score_ngrams( BigramAssocMeasures.fisher )
	
	# create a network from the scores
	G = nx.Graph()
	for index, record in enumerate( records ) :
	
		# parse
		source = record[ 0 ][ 0 ]
		target = record[ 0 ][ 1 ]
		weight = record[ 1 ]
	
		# update
		G.add_edge( source, target, weight=weight )
	
		# continue, conditionally
		if index > limit : break
	
	# debug
	sys.stderr.write( 'Parameters:' + '\n' )
	sys.stderr.write( '  * carrel: '  + carrel + '\n' )
	sys.stderr.write( '  * limit: '   + str( limit ) + '\n' )
	sys.stderr.write( '  * measure: ' + measure + '\n' )
	sys.stderr.write( '  * filter: '  + str( filter ) + '\n' )
	sys.stderr.write( '  * window: '  + str( window) + '\n' )
	sys.stderr.write( '\n' )
	sys.stderr.write( 'Result:' + '\n' )
	sys.stderr.write( '  * number of nodes: ' + str( G.number_of_nodes() ) + '\n' )
	sys.stderr.write( '  * number of edges: ' + str( G.number_of_edges() ) + '\n' )
	
	# output image
	if output == 'image' :
	
		# visualize
		plt.figure()
		nx.draw( G, with_labels=True, node_size=10, font_size=9, edge_color='silver' )
		plt.show()
		
	# standard out
	else: 
	
		# save
		if save :

			# configure and save
			file = localLibrary/carrel/ETC/COLLOCATIONS
			nx.write_gml( G, file )

		# standard output
		else : nx.write_gml( G, sys.stdout.buffer )
		
	# done
	return

# given a carrel, return a spacy doc
def _carrel2doc( carrel ) :

	# configure
	PICKLE = 'reader.spacy'

	# require
	from os        import path, stat
	from spacy     import load
	import                textacy
	import sys
	
	# initialize
	localLibrary = configuration( 'localLibrary' )
	pickle       = localLibrary/carrel/ETC/PICKLE

	# check to see if we've previously been here
	if path.exists( pickle ) :
		
		# read the pickle file
		try            : doc = next( textacy.io.spacy.read_spacy_docs( pickle, lang=MODELSMALL ) )
		except OSError : modelNotFound()
			
	# otherwise
	else :
	
		# warn
		sys.stderr.write( '''Modeling study carrel data for future use. This may take many
minutes, but it will only have to be done once. In the meantime,
ask yourself, "Self, what is justice?"\n''' )

		# initialize 
		file           = localLibrary/carrel/ETC/CORPUS
		text           = open( str( file ) ).read()
		size           = ( stat( file ).st_size ) + 1
		
		# initialize some more
		try            : nlp  = load( MODELSMALL )
		except OSError : modelNotFound()
		
		# do the work
		nlp.max_length = size
		doc            = nlp( text )

		# save it for future use
		textacy.io.spacy.write_spacy_docs( doc, filepath=pickle )

	# done
	return doc


# process grammars
def grammars( carrel, grammar='svo', query=None, noun=None, lemma='be', sort=False, count=False ) :

	# require
	from textacy import extract
	from os      import system
	from re      import search
	
	# sanity check
	checkForCarrel( carrel )

	# initialize
	doc = _carrel2doc( carrel )

	# get the features; svo
	if grammar == 'svo' :
			
		# do the work
		features = list( extract.subject_verb_object_triples( doc ) )
				
		# simplify the result
		items = []
		for feature in features :
		
			#print( help(feature ) )
			#exit()

			subject = feature.subject[ 0 ].text			
			verb    = feature.verb[ 0 ].text
			object  = feature.object[ 0 ].text
			items.append(' \t'.join( [ ''.join( subject ), ''.join( verb ), ''.join( object ) ] ) )

		# done
		features = items
				
	# quotes
	elif grammar == 'quotes' :
	
		# do the work
		features = list( extract.direct_quotations( doc ) )
		
		# simplify the result
		items = []
		for feature in features :
		
			# parse and stringify
			speaker = [ token.text for token in feature.speaker ]
			cue     = [ token.text for token in feature.cue ]
			content = feature.content.text
			items.append( '\t'.join( [ ''.join( speaker ), ''.join( cue ), content ] ) )

		# done
		features = items

	# noun chunks
	elif grammar == 'nouns' :
	
		# do the work and simplify the result
		features = list( extract.noun_chunks( doc ) )
		features = [ feature.text for feature in features ]
		
	# semi-structured sentences
	elif grammar == 'sss' :

		# sanity check
		if not noun :
		
			sy.stderr.write( "Error: When specifying sss, the -n option is required. See 'rdr grammars --help'\n" )
			exit()
			
		# do the work
		features = list( extract.semistructured_statements( doc, entity=noun, cue=lemma ) )

		# simplify the result
		items = []
		for feature in features :
		
			entity   = [ token.text for token in feature.entity ]
			cue      = [ token.text for token in feature.cue ]
			fragment = [ token.text for token in feature.fragment ]
			items.append( '\t'.join( [ ''.join( entity ), ''.join( cue ), ' '.join( fragment ) ] ) )

		# done
		features = items

	# filter, conditionally
	if query : features = [ feature for feature in features if ( search( query, feature ) ) ]
	
	# sort, conditionally
	if sort : features.sort()
	
	# count, conditionally
	if count :
	
		# initialize a dictionary and process each feature
		items = {}
		for feature in features :

			# update the dictionary
			if feature in items : items[ feature ] += 1
			else                : items[ feature ]  = 1

		# sort the dictionary; return the features
		features = sorted( items.items(), key=lambda x:x[ 1 ], reverse=True )
		
		# process each feature, again
		items = []
		for feature in features :
			
			# create a record and update
			record = str( feature[ 1 ] ) + '\t' + feature[ 0 ]
			items.append( record )
		
		# done
		features = items
	
	# done
	return '\n'.join( features )
	

# given a file, return a set of tokenized sentences
def extractTokenizedSentences( file, stopwords ) :

	# initialize
	results = []
	
	# require
	import nltk
	import re
	
	# slurp up the given file; read the text
	with open( file, encoding='utf-8'  ) as handle : text = handle.read()

	# get and process all sentences in the text
	sentences = nltk.sent_tokenize( text )
	for sentence in sentences : 
	
		# do rudimentary normalization and tokenization
		sentence = re.sub( '\n', ' ', sentence )
		sentence = re.sub( '\t', ' ', sentence )
		sentence = re.sub( ' +', ' ', sentence )
		sentence = re.sub( '- ', '',  sentence )
		sentence = re.sub( '- ', '',  sentence )
		
		# tokenize and normalize
		tokens = nltk.word_tokenize( sentence.lower() )
		tokens = [ token for token in tokens if token.isalpha() ]
		tokens = [ token for token in tokens if token not in stopwords ]

		# output
		results.append( ' '.join( tokens )  )
	
	# done
	return( results )


# make sure the carrel has been indexed
def checkForSemanticIndex( carrel, localLibrary ) :

	# configure; not quite right
	VECTORS = 'carrel.vec'
	PATTERN = '*.txt'
	TOKENS  = 'carrel.tok'
	
	# require
	from multiprocessing import Pool
	from pathlib         import Path
	import gensim
	import sys

	# configure
	#localLibrary = configuration( 'localLibrary' )
	vectors      = localLibrary/carrel/ETC/VECTORS
	tokens       = localLibrary/carrel/ETC/TOKENS
	
	# see if we have been here previously
	if not vectors.exists() :

		filenames    = localLibrary/carrel/TXT
		stopwords    = localLibrary/carrel/ETC/STOPWORDS
		with open( stopwords, encoding='utf-8'  ) as handle : stopwords = handle.read().split( '\n' )

		# parallel process each plain text file in the given corpus; fast!
		pool = Pool()
		sys.stderr.write( 'Step #1 of 3: Reading sentences\n' )
		results = pool.starmap( extractTokenizedSentences, [ [ filename, stopwords ] for filename in filenames.glob( PATTERN ) ] )
		pool.close()
		
		# save the result
		sys.stderr.write( 'Step #2 of 3: Saving sentences\n' )
		with open( tokens, 'w', encoding='utf-8'  ) as handle :
		
			# get all sentences and process each one
			for sentences in results :
			
				# output
				for sentence in sentences : handle.write( '%s\n' % sentence )
				
		# model; do the real work
		sys.stderr.write( 'Step #3 of 3: Modeling\n' )
		model = gensim.models.Word2Vec( corpus_file=str( tokens ), workers=8 )

		# save and done
		model.wv.save( str( vectors ) )

	# done
	return	


# implement semantic (word2vec) indexing
def word2vec( carrel, localLibrary=None, type='similarity', query='love', topn=10 ) :

	'''types = similarity|distance|analogy|scatter'''

	# configure
	VECTORS  = 'carrel.vec'
	
	# require
	import sys
	import gensim
	from pathlib import Path
	
	# initialize
	if localLibrary : library = Path( localLibrary )
	else            : library = configuration( 'localLibrary' )
	vectors      = str( library/carrel/ETC/VECTORS )
	
	# sanity checks
	checkForCarrel( carrel, library )
	checkForSemanticIndex( carrel, library )
		
	# load model
	model = gensim.models.KeyedVectors.load( vectors )

	# similarity
	if type == 'similarity' :
	
		# sanity check
		if len( query.split() ) != 1 :
		
			# error
			sys.stderr.write( "The query for similarity requires exactly one word.\n" )
			exit()

		# search and output
		try :
			items = []
			
			similarities = model.most_similar_cosmul( query, topn=topn )
			for similarity in similarities : 
				
				word  = similarity[ 0 ]
				score = similarity[ 1 ]
				items.append( '\t'.join( [ word, str( score ) ] ) )
	
			return '\n'.join( items )
			
		# word not found
		except KeyError as word : sys.stderr.write ( ( 'The word -- %s -- is not in the index.\n' % word ) )

	# distance
	elif type == 'distance' :

		# get the query words
		words = query.split()

		# sanity check
		if len( words ) < 2 :
		
			# error
			sys.stderr.write( "The query for distance requires at least two words.\n" )
			exit()

		# create a distance command; hacky!
		queries     = query.split()
		word        = queries[ 0 ]
		other_words = queries[ 1: ]
				
		# try to compute
		try :
		
			# initialize
			items = []
			
			# search, reshape, sort, output, and done
			distances = model.distances( word, other_words )
			distances = zip( other_words, distances )
			distances = list( set( distances ) )
			distances.sort( key=lambda i: i[ 1 ], reverse=True )
			for distance in distances : items.append( '\t'.join( [ distance[ 0 ], str( distance[ 1 ] ) ] ) )

			return '\n'.join( items )

		# error
		except KeyError as word : 
			sys.stderr.write( ( 'A word in your query -- %s -- is not in the index. Please remove it.\n' % word ) )

	# analogy
	elif type == 'analogy' :
	
		# get the query words
		words = query.split()
		
		# sanity check
		if len( words ) != 3 :
		
			# error
			sys.stderr.write( "The query for analogy requires exactly three words.\n" )
			exit()
		
		# try to compute
		try :
		
			positive = [ words[ 0 ], words[ 2 ] ]
			negative = words[ 1 ]
			items    = []
			
			similarities = model.most_similar( positive=positive, negative=negative, topn=topn )
			#for similarity in similarities : print( similarity )
			return( similarities )
			
		# error
		except KeyError as word : sys.stderr.write( ( 'A word in your query -- %s -- is not in the index. Please remove it.\n' % word ) )


# make sure the carrel has been indexed; sqlite++
def _checkForIndex( carrel, localLibrary ) :

	# configure
	SANITYCHECK    = "SELECT * FROM sqlite_master WHERE type='table' AND name='fulltext';"
	DROPFULLTEXT   = 'DROP TABLE IF EXISTS fulltext;'
	CREATEFULLTEXT = 'CREATE TABLE fulltext ( id TEXT, fulltext TEXT );\n'
	TEMPLATE       = "INSERT INTO fulltext ( id, fulltext ) VALUES ( '##ID##', '##FULLTEXT##' );\n"
	DROPINDX       = 'DROP TABLE IF EXISTS indx;'

	# these are what we want
	CREATEINDX     = 'CREATE VIRTUAL TABLE indx USING FTS5( id, author, title, date, summary, keyword, words, sentence, flesch, cache, txt, fulltext );'
	INDEX          = 'INSERT INTO indx SELECT b.id, b.author, b.title, b.date, b.summary, group_concat( LOWER( w.keyword ), "; " ), b.words, b.sentence, b.flesch, b.id || b.extension, b.id || ".txt", f.fulltext FROM bib AS b, fulltext AS f, wrd AS w WHERE b.id IS f.id AND b.id IS w.id GROUP BY w.id;';

	# these work when "database is full"; no full text
	#CREATEINDX     = 'CREATE VIRTUAL TABLE indx USING FTS5( id, author, title, date, summary, keyword, words, sentence, flesch, cache, txt );'
	#INDEX          = 'INSERT INTO indx SELECT b.id, b.author, b.title, b.date, b.summary, group_concat( LOWER( w.keyword ), "; " ), b.words, b.sentence, b.flesch, b.id || b.extension, b.id || ".txt" FROM bib AS b, fulltext AS f, wrd AS w WHERE b.id IS f.id AND b.id IS w.id GROUP BY w.id;';

	# require
	import os
	import re
	import sqlite3
	import tempfile
	import sys
	
	# initialize
	db           = str( localLibrary/carrel/ETC/DATABASE )
	txt          = localLibrary/carrel/TXT
	transaction  = tempfile.NamedTemporaryFile( delete=False ).name
	
	# connect to database
	connection                 = sqlite3.connect( db )
	connection.isolation_level = None
	cursor                     = connection.cursor()
		
	# check to see if we've been here previously
	results = cursor.execute( SANITYCHECK ).fetchall()
	if results == [] :
		
		# nope; create full text table
		sys.stderr.write( 'Indexing; the carrel must be set up for full text searching.\n' )
		sys.stderr.write( 'Step #1 of 4: Creating table to contain full text...\n' )
		connection.execute( DROPFULLTEXT )
		connection.execute( CREATEFULLTEXT )

		# read full text
		sys.stderr.write( 'Step #2 of 4: Reading full text; please be patient...\n' )
		with open( transaction, 'w', encoding='utf-8'  ) as handle : handle.write( 'BEGIN TRANSACTION;\n' )
		files = txt.glob( '*.txt' )
		for file in files :

			# get identifier
			id = file.stem
			id = id.replace( "'", "''" )
	
			# get full text
			with open( file, encoding='utf-8' ) as handle : fulltext = handle.read()
			fulltext = fulltext.replace( '\r', '\n' )
			fulltext = fulltext.replace( '\n', ' ' )
			fulltext = fulltext.replace( "'",  "''")
			fulltext = re.sub( ' +' , ' ', fulltext )
	
			# sql
			sql = TEMPLATE
			sql = sql.replace( '##ID##', id )
			sql = sql.replace( '##FULLTEXT##', fulltext )

			# debug
			#click.echo( '  file: ' + str( file ), err=True )
			#click.echo( '    id: ' + id, err=True )
			#click.echo( err=True )
	
			# update
			with open( transaction, 'a', encoding='utf-8'  ) as handle : handle.write( sql )

		# close the transaction
		with open( transaction, 'a', encoding='utf-8'  ) as handle : handle.write( 'END TRANSACTION;\n' )

		# write full text
		sys.stderr.write( 'Step #3 of 4: Writing full text to database...\n' )
		with open( transaction, encoding='utf-8'  ) as handle :

			# repeat forever, almost
			while True :
				sql = handle.readline()
				if not sql : break
				connection.execute( sql )


		# clean up
		os.remove( transaction )
		
		# index; do the actual work
		sys.stderr.write( 'Step #4 of 4: Indexing; please be patient...\n' )
		connection.execute( DROPINDX )
		connection.execute( CREATEINDX )
		connection.execute( INDEX )

		# done
		sys.stderr.write( 'Done. Happy searching!\n' )
		return
		
# do full text indexing and search
def search( carrel, localLibrary=None, query='love', output='human' ) :
	'''output = csv|tsv|json|human|count'''

	# configure
	SQL = "SELECT id, author, title, date, summary, keyword, words, sentence, flesch, '##CACHE##' || cache AS cache, '##TXT##' || txt AS txt FROM indx WHERE indx MATCH '##QUERY##' ORDER BY RANK;"

	# configure
	RESULTS = '\nYour search (##QUERY##) against the study carrel named "##CARREL##" returned ##COUNT## record(s):\n\n##RECORDS##'
	RECORD  = '          id: ##ID##\n      author: ##AUTHOR##\n       title: ##TITLE##\n        date: ##DATE##\n     summary: ##SUMMARY##\n  keyword(s): ##KEYWORD##\n       words: ##WORDS##\n    sentence: ##SENTENCE##\n      flesch: ##FLESCH##\n       cache: ##CACHE##\n         txt: ##TXT##\n\n'
	COUNT   = '##CARREL##\t##QUERY##\t##COUNT##'

	# require
	import sqlite3
	import pandas as pd
	import sys
	from pathlib import Path
	
	# initialize
	if localLibrary : library = Path( localLibrary )
	else            : library = configuration( 'localLibrary' )

	# sanity checks
	checkForCarrel( carrel, library )
	_checkForIndex( carrel, library )

	txt          = str( library/carrel/TXT ) + '/'
	cache        = str( library/carrel/CACHE ) + '/'
	db           = str( library/carrel/ETC/DATABASE )	
	connection   = sqlite3.connect( db )

	# build sql
	sql = SQL.replace( '##CACHE##', cache )
	sql = sql.replace( '##TXT##', txt )
	sql = sql.replace( '##QUERY##', query )

	# search
	rows = pd.read_sql_query( sql, connection, index_col='id' )
	
	# output; csv
	if output   == 'csv' : return( rows.to_csv() )
	
	# tsv
	elif output == 'tsv' : return( rows.to_csv( header=False, sep='\t' ) )
	
	# json
	#elif output == 'json' : return( rows.to_json( orient='records' ) )
	elif output == 'json' : return( rows.to_json( orient='index' ) )
	
	# count; tsv stream of metadata
	elif output == 'count' :
	
		# build
		results = COUNT.replace( '##CARREL##', carrel )
		results = results.replace( '##QUERY##', query )
		results = results.replace( '##COUNT##', str( rows.shape[ 0 ] ) )
		
		# output
		return( results )
	
	# paged
	elif output == 'human' : 
			
		# initialize the results
		results = RESULTS.replace( '##QUERY##', query )
		results = results.replace( '##CARREL##', carrel )
		results = results.replace( '##COUNT##', str( rows.shape[ 0 ] ) )
		
		# process each row
		records = ''
		for id, row in rows.iterrows() :
								
			# parse
			author   = row[ 'author' ]
			if not author : author = ''
			title    = row[ 'title' ]
			if not title : title = ''
			date     = row[ 'date' ]
			if not date : date = ''
			summary  = row[ 'summary' ]
			keyword  = row[ 'keyword' ]
			words    = row[ 'words' ]
			sentence = row[ 'sentence' ]
			flesch   = row[ 'flesch' ]
			cache    = row[ 'cache' ]
			txt      = row[ 'txt' ]
			
			if not summary : summary = ' '
			if not cache   : cache   = ' '
			
			# create a record
			record = RECORD.replace( '##ID##', str( id ) )
			record = record.replace( '##AUTHOR##', author )
			record = record.replace( '##TITLE##', title )
			record = record.replace( '##DATE##', str( date ) )
			record = record.replace( '##SUMMARY##', summary )
			record = record.replace( '##KEYWORD##', keyword )
			record = record.replace( '##WORDS##', str( words ) )
			record = record.replace( '##SENTENCE##', str( sentence ) )
			record = record.replace( '##FLESCH##', str( flesch ) )
			record = record.replace( '##CACHE##', cache )
			record = record.replace( '##TXT##', txt )
		
			# update
			records += record
		
		results = results.replace( '##RECORDS##', records )
		return( results )


# get an inventory of available study carrels
def catalog( location='local', human=True ) :

	'''location = local|remote'''

	# configure
	INDEX    = 'index.csv'
	RECORD   = "         item: ##ITEM##\n   identifier: ##IDENTIFIER##\n        title: ##TITLE##\n         type: ##TYPE##\n       source: ##SOURCE##\n        items: ##ITEMS##\n        words: ##WORDS##\n  readability: ##SCORE##\n     keywords: ##KEYWORDS##\n         read: ##READ##\n       browse: ##BROWSE##\n     download: ##DOWNLOAD##\n\n"
	HEADER   = "\nThe catalog includes ##COUNT## items, and each is listed below:\n\n"

	# require
	from requests import get
	from pandas   import read_csv
	from io       import StringIO
	
	# branch accordingly; local
	if location == 'local' :
		
		# initialize
		localLibrary = configuration( 'localLibrary' )
		items        = []
		
		# read, sort, and output
		carrels = [ carrel.name for carrel in localLibrary.iterdir() if carrel.is_dir() ]
		carrels.sort()
		for carrel in carrels : items.append( carrel )
	
		return '\n'.join( items )
		
	# remote
	elif location == 'remote' :
	
		# create person-amenable output
		if human :
		
			# create a rudimentary catalog
			catalog = ''
			count   = 0
						
			# get all the remote records and process each; convoluted
			carrels = read_csv( StringIO( get( REMOTELIBRARY + '/' + INDEX ).text ) )
			for item, carrel in carrels.iterrows() :
										
				# increment
				count += 1
				item  += 1
				
				# update
				record   = RECORD.replace( '##ITEM##',       str( item ) )
				record   = record.replace( '##IDENTIFIER##', carrel[ 'id' ] )
				record   = record.replace( '##TITLE##',      carrel[ 'title' ] )
				record   = record.replace( '##KEYWORDS##',      carrel[ 'keywords' ] )
				record   = record.replace( '##ITEMS##',      str( carrel[ 'items' ] ) )
				record   = record.replace( '##WORDS##',      str( carrel[ 'words' ] ) )
				record   = record.replace( '##SCORE##',      str( carrel[ 'flesch' ] ) )
				record   = record.replace( '##TYPE##',      str( carrel[ 'type' ] ) )
				record   = record.replace( '##SOURCE##',      str( carrel[ 'source' ] ) )
				record   = record.replace( '##READ##',      str( carrel[ 'read' ] ) )
				record   = record.replace( '##BROWSE##',      str( carrel[ 'browse' ] ) )
				record   = record.replace( '##DOWNLOAD##',      str( carrel[ 'download' ] ) )
				catalog += record
				
			# add the header and output
			header  = HEADER.replace( '##COUNT##', str( count ) )
			catalog = header + catalog
			return( catalog )
				
		# get the raw data and hope the results get piped to utilities like sort, grep, cut, less, etc.
		else : return( get( REMOTELIBRARY + '/' + INDEX ).text  )

	
# locally cache a carrel from the public library
def download( carrel ) :
			
	# configure
	ZIPFILE = 'index.zip'
	CARRELS = ''

	# require
	from requests import get
	from tempfile import TemporaryFile
	from zipfile  import ZipFile
	import sys
	
	# initialize
	localLibrary  = configuration( 'localLibrary' )

	# get the remote zip file; needs error checking
	sys.stderr.write( "\n  INFO: Downloading remote study carrel...\n" )
	response = get( REMOTELIBRARY + '/' + carrel + '/' + ZIPFILE )
	
	# initialize a temporary file and write to it
	sys.stderr.write( "  INFO: Saving study carrel...\n" )
	handle = TemporaryFile()
	handle.write( response.content )
	
	# unzip the temporary file and close it, which also deletes it
	sys.stderr.write( "  INFO: Unziping study carrel...\n" )
	with ZipFile( handle, 'r' ) as zip : zip.extractall( str( localLibrary ) )
	handle.close()

	# done
	sys.stderr.write( ( '''  INFO: Done.\n''' ) )
	return


# open the html root of a study carrel
def read( carrel, location='local', localLibrary=None, ) :

	# require
	from webbrowser import open
	import sys
	from pathlib import Path
	
	if location == 'local' :
	
		if localLibrary : localLibrary = Path( localLibrary )
		else            : localLibrary = configuration( 'localLibrary' )
		
		# sanity check
		checkForCarrel( carrel, localLibrary )

		#localLibrary  = configuration( 'localLibrary' )
		url = 'file://' + str( localLibrary/carrel/INDEX )
		open( url )
		
	elif location == 'remote' :
	
		url = REMOTELIBRARY + '/' + CARRELS + '/' + carrel
		open( url )

# make sure tika server has been downloaded
def _checkForTika( tika ) :
	
	# require
	from configparser import ConfigParser
	from pathlib      import Path
	from requests     import get
	
	# install tika, conditionally
	if not Path( tika ).exists() :
	
		click.echo( "\n  WARNING: Tika server not found. Downoading... ", err=True )
		response = get( TIKADOWNLOAD )
		file     = Path( tika ) 
		with open( file, 'wb' ) as handle : handle.write( response.content )
		click.echo( "\n  INFO: Downloaded", err=True )

		# _initialize
		click.echo( "\n  INFO: Updating configurations... " )
		configurations          = ConfigParser()
		applicationDirectory    = Path.home()
		configurationFile       = applicationDirectory/CONFIGURATIONFILE
		localLibrary            = configuration( 'localLibrary' )
		malletHome              = configuration( 'malletHome' )
		tikaHome                = Path.home()/TIKAHOME
		configurations[ "RDR" ] = { "localLibrary"  : localLibrary, "malletHome" : malletHome, "tikaHome" : tikaHome }
		with open( configurationFile, 'w', encoding='utf-8'  ) as handle : configurations.write( handle )

		# done
		click.echo( '''
  INFO: Tika server (tika-server.jar) has been downloaded to your
  home directory and configured for future use. You can move Tika
  server to another location but once you do so you will need to
  run 'rdr set -s tika'.
''', err=True )

		# start tika server
		_startTika()


# check to see if tika is running
def _tikaIsRunning () :

	# configure, require, and _initialize
	TIKA    = 'http://localhost:9998/'
	import requests
	running = False

	# give it a go
	try :

		# check for success
		if requests.get( TIKA ).ok : running = True
	
	# error
	except requests.ConnectionError : pass
	
	# done
	return( running )
	
	
# create carrel skeleton
def _initialize( carrel, directory, localLibrary=None ) :
	
	# require
	from datetime import datetime
	
	# configure
	ADR      = 'adr'
	BIB      = 'bib'
	CACHE    = 'cache'
	ENT      = 'ent'
	ETC      = 'etc'
	POS      = 'pos'
	TXT      = 'txt'
	URLS     = 'urls'
	WRD      = 'wrd'
	WORDS    = '''http\nhttps\n0\n1\n2\n3\n4\n5\n6\n7\n8\n9\na\na\nabout\nabove\nafter\nagain\nagainst\nall\nalso\nam\nan\nand\nany\nare\naren't\nas\nat\nb\nbe\nbecause\nbeen\nbefore\nbeing\nbelow\nbetween\nboth\nbut\nby\nc\ncan\ncan't\ncannot\ncould\ncouldn't\nd\ndid\ndidn't\ndo\ndoes\ndoesn't\ndoing\ndon't\ndown\nduring\ne\neach\nf\nfew\nfor\nfrom\nfurther\ng\nh\nhad\nhadn't\nhas\nhasn't\nhast\nhath\nhave\nhaven't\nhaving\nhe'd\nhe'll\nhe's\nher\nhere\nhere's\nhers\nherself\nhim\nhimself\nhis\nhow\nhow's\ni'd\ni'll\ni'm\ni've\nif\nin\ninto\nis\nisn't\nit\nit's\nits\nitself\nj\nk\nl\nlet's\nm\nme\nmore\nmost\nmustn't\nmy\nmyself\nn\nno\nnor\nnot\no\nof\noff\non\nonce\none\nonly\nor\nother\nought\nour\nours\nourselves\nout\nover\nown\np\nq\nr\ns\nsaid\nsame\nshan't\nshe'd\nshe'll\nshe's\nshould\nshouldn't\nso\nsome\nsuch\nt\nthan\nthat\nthat's\nthe\nthee\ntheir\ntheirs\nthem\nthemselves\nthen\nthere\nthere's\nthese\nthey'd\nthey'll\nthey're\nthey've\nthis\nthose\nthou\nthrough\nthus\nthy\nto\ntoo\nu\nunder\nuntil\nunto\nup\nupon\nv\nvery\nw\nwas\nwasn't\nwe'd\nwe'll\nwe're\nwe've\nwere\nweren't\nwhat\nwhat's\nwhen\nwhen's\nwhere\nwhere's\nwhich\nwhile\nwho\nwho's\nwhom\nwhy\nwhy's\nwill\nwith\nwon't\nwould\nwouldn't\nx\ny\nyou'd\nyou'll\nyou're\nyou've\nyour\nyours\nyourself\nyourselves\nz\n'''
	PROCESS  = 'toolbox'

	# require
	from   datetime import datetime
	from   getpass  import getuser
	from   pathlib  import Path
	import shutil
	
	# create the library, the carrel, and the carrel's sub-directories
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	Path.mkdir( localLibrary,                exist_ok=True )
	Path.mkdir( localLibrary/carrel,         exist_ok=True )
	Path.mkdir( localLibrary/carrel/ADR,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/BIB,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/CACHE,   exist_ok=True )
	Path.mkdir( localLibrary/carrel/ENT,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/ETC,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/FIGURES, exist_ok=True )
	Path.mkdir( localLibrary/carrel/POS,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/TXT,     exist_ok=True )
	Path.mkdir( localLibrary/carrel/URLS,    exist_ok=True )
	Path.mkdir( localLibrary/carrel/WRD,     exist_ok=True )

	# configure provenance and output it
	process     = PROCESS
	originalID  = carrel
	dateCreated = datetime.today().strftime( '%Y-%m-%d' )
	timeCreated = datetime.now().strftime("%H:%M")
	creator     = getuser()
	input       = directory
	record      = [ PROCESS, originalID, dateCreated, timeCreated, creator, input ]
	output      = localLibrary/carrel/PROVENANCE
	with open( output, 'w', encoding='utf-8' ) as handle : handle.write( '\t'.join( record ) + '\n' )
	
	# process each item in the given directory
	directory = Path( directory )
	for source in directory.glob( '*' ) :

		# check for metadata file; look for a very specific file
		if source.name == 'metadata.csv' :
		
			# copy the metadata file to the root of the carrel
			destination = localLibrary/carrel/METADATA
			shutil.copyfile( source, destination )

		else :
		
			# copy the file to the cache directory
			destination = localLibrary/carrel/CACHE/( source.name )
			shutil.copyfile( source, destination )

	# add stop words; there is probably a better way
	output = localLibrary/carrel/ETC/STOPWORDS
	with open( output, 'w', encoding='utf-8' ) as handle : handle.write( WORDS )

	# add readme
	output      = localLibrary/carrel/READMEFILE
	readmewords = READMEWORDS.replace( '##DATE##', datetime.today().strftime("%B %-d, %Y") )
	with open( output, 'w', encoding='utf-8' ) as handle : handle.write( readmewords )


# given a file, create some bibliographics and save plain text
def _file2bib( carrel, file, metadata=None, localLibrary=None ) :
		
	# configure
	BIB          = 'bib'
	TXT          = 'txt'
	CACHE        = 'cache'
	COUNT        = 24
	EXTENSION    = '.txt'
	BIBEXTENSION = '.bib'
	HEADER       = [ 'id', 'author', 'title', 'date', 'pages', 'extension', 'mime', 'words', 'sentence', 'flesch', 'summary', 'cache', 'txt' ]
	PROCESS      = 'textrank'

	# require
	from   pathlib              import Path
	from   textacy              import text_stats
	from   tika                 import detector
	from   tika                 import parser
	import os
	import spacy
	import pytextrank
	
	# _initialize
	authorFound  = False
	dateFound    = False
	titleFound   = False
	title        = _name2key( file )
	extension    = os.path.splitext( os.path.basename( file ) )[ 1 ]
	key          = _name2key( file )
	pages        = ''
	summary      = ''
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# get the text, and if not, then return; the whole point is to have content to read!
	parsed = parser.from_file( file )
	text   = parsed[ 'content' ]	
	if not text : return
	
	# get metadata from the metadata file	
	if str( type( metadata ) ) == "<class 'pandas.core.frame.DataFrame'>" :
		
		# parse
		index = Path( file ).name
		
		# check to see if the index value exists
		if index in metadata.index :
		
			if 'author' in metadata :
		
				author      = str( metadata.loc[ index ][ 'author' ] )
				authorFound = True
			
			if 'title'  in metadata : 
		
				title  = metadata.loc[ index ][ 'title' ]
				titleFound = True
			
			if 'date'   in metadata : 
		
				date      = str( metadata.loc[ index ][ 'date' ] )
				dateFound = True
		
	# get metadata from the source file
	metadata = parsed[ 'metadata' ] 
	mimetype = detector.from_file( file )

	# author
	if authorFound == False : 
	
		if 'creator' in metadata :
			author = metadata[ 'creator' ]
			if ( isinstance( author, list ) ) : author = author[ 0 ]
			
		else : author = ''
		
	# title
	if titleFound == False : 
	
		if 'title' in metadata :
			title = metadata[ 'title' ]
			if ( isinstance( title, list ) ) : title = title[ 0 ]
			title = ' '.join( title.split() )

	# date
	if dateFound == False : 
	
		if 'date' in metadata :
			date = metadata[ 'date' ]
			if ( isinstance( date, list ) ) : date = date[ 0 ]
			date = date[:date.find( 'T' )]
		
		else : date = ''

	# number of pages
	if 'xmpTPg:NPages' in metadata :
		pages = metadata[ 'xmpTPg:NPages' ]
		if ( isinstance( pages, list ) ) : pages = pages[ 0 ]
		
	# model the text
	nlp            = spacy.load( MODELSMALL )
	nlp.max_length = ( len( text ) + 1 )
	nlp.add_pipe( PROCESS )
	doc            = nlp( text )

	# _summarize
	summary = _summarize( doc )
	
	# parse out only the desired statistics
	words      = text_stats.n_words( doc )
	sentences  = text_stats.n_sents( doc )
	syllables  = text_stats.n_syllables( doc )
	flesch     = int( text_stats.readability.flesch_reading_ease( doc ) )

	# cache and text locations
	txt   = Path( TXT )/( str( key ) + EXTENSION )
	cache = Path( CACHE )/( str( key ) + extension )

	# debug
	if VERBOSE == 2 :
	
		# provide a review
		click.echo( '        key: ' + key,              err=True )
		click.echo( '     author: ' + author,           err=True )
		click.echo( '      title: ' + str( title ),     err=True )
		click.echo( '       date: ' + date,             err=True )
		click.echo( '  extension: ' + extension,        err=True )
		click.echo( '      pages: ' + pages,            err=True )
		click.echo( '  mime-type: ' + mimetype,         err=True )
		click.echo( '    summary: ' + summary,          err=True )
		click.echo( '      words: ' + str( words ),     err=True )
		click.echo( '  sentences: ' + str( sentences ), err=True )
		click.echo( '     flesch: ' + str( flesch ),    err=True )
		click.echo( '      cache: ' + str( cache ),     err=True )
		click.echo( '        txt: ' + str( txt ),       err=True )
		click.echo( '',                                 err=True )
	
	# open output
	output = localLibrary/carrel/BIB/( key + BIBEXTENSION )
	
	with open( output, 'w', encoding='utf-8' ) as handle :
	
		try :
		
			# output the header and the data
			handle.write( '\t'.join( HEADER ) + '\n' )
			handle.write( '\t'.join( [ str( key ), author, str( title ), str( date ), pages, extension, mimetype, str( words ), str( sentences ), str( flesch ), summary, str( cache ), str( txt ) ] ) + '\n' )
		
		# trap weird TypeError
		except TypeError : click.echo( ( "\nWARNING (TypeError): Probably weird author value extracted from PDF file (key: %s). Call Eric.\n" % key ), err=True )
			
	# check for text, and it should exist; famous last words
	if text : 

		# configure output and output
		output = localLibrary/carrel/TXT/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8' ) as handle : handle.write( text )


# create key from filename
def _name2key( file ) :

	# require, do the work, and done; inefficient
	import os
	key = str( os.path.splitext( os.path.basename( file ) )[ 0 ] )
	return key


# given a spaCy doc which has been enhanced by pytextrank, return a summary
def _summarize( doc ) :

	# see: https://derwen.ai/docs/ptr/explain_summ/
	
	# configure
	PHRASELIMIT   = 4
	SENTENCELIMIT = 2

	# require
	from   math       import sqrt
	from   operator   import itemgetter
	import pytextrank
	import re
	
	boundries   = [ [ sentence.start, sentence.end, set( [] ) ] for sentence in doc.sents ]
	phrase_id   = 0
	unit_vector = []

	# process each phrase
	for phrase in doc._.phrases :

		unit_vector.append( phrase.rank )

		for chunk in phrase.chunks:

			for start, end, vector in boundries :
		
				if chunk.start >= start and chunk.end <= end :

					vector.add( phrase_id )
					break
				
		phrase_id    += 1
		if phrase_id == PHRASELIMIT : break

	sum_ranks   = sum( unit_vector )

	# trap for a document that is too small
	try : unit_vector = [ rank/sum_ranks for rank in unit_vector ]
	except ZeroDivisionError : return doc.text
	
	rankings    = {}
	sent_id     = 0

	for start, end, vector in boundries:

		# re-_initialize
		sum_sq = 0.0

		for identifier in range( len( unit_vector ) ) :
		
			if identifier not in vector : sum_sq += unit_vector[ identifier ] ** 2.0

		rankings[ sent_id ] =  sqrt( sum_sq )
		sent_id             += 1

	# create a dictionary of sentences
	sentences = {}
	for index, sentence in enumerate( doc.sents ) : sentences[ index ] = sentence.text

	# process each ranking
	summary = []
	for index, sentence in enumerate( sorted( rankings.items(), key=itemgetter( 1 ) ) ) :

		# output, and conditionally continue
		summary.append( sentences[ sentence[ 0 ] ] )
		if ( index + 1 ) == SENTENCELIMIT : break

	# _normalize
	summary = ' '.join( summary )
	summary = summary.replace( '"', '' )
	summary = re.sub( '\r', ' ', summary )
	summary = re.sub( '\t+', ' ', summary )
	summary = re.sub( '\n+', ' ', summary )
	summary = re.sub( ' +', ' ',  summary )
	summary = re.sub( '^\s', '',  summary )
	summary = re.sub( '\s$', '',  summary )

	# done
	return summary

# create bag of words
def _txt2bow( carrel, localLibrary=None ) :

	# configure; not quite right
	PATTERN = '*.txt'
	BOW     = 'carrel.txt'
	TXT     = 'txt'
	ETC     = 'etc'
	
	# require
	from pathlib import Path

	# _initialize
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# process each text file in the given directory
	txt = localLibrary/carrel/TXT
	bow = ''
	for file in txt.glob( PATTERN ) :
	
		# create/increment the bag of words
		with open( file, encoding='utf-8' ) as handle : bow += handle.read()
	
	# _normalize
	bow = _normalize( bow )
	
	# configure output, output, and done
	output = localLibrary/carrel/ETC/BOW
	with open( output, 'w', encoding='utf-8' ) as handle : handle.write( bow )



# _normalize text, a poor man's version
def _normalize( text ) :

	# require
	import re
	
	# _normalize the text in the bag-of-words
	text = text.lower()
	text = re.sub( '\r', '\n', text )
	text = re.sub( '\n+', ' ', text )
	text = re.sub( '^\W+', '', text )
	text = re.sub( '\t', ' ',  text )
	text = re.sub( '- ', '',   text )
	text = re.sub( ' +', ' ',  text )
	text = re.sub( '\t', ' ',  text )

	# done
	return text


# extract email addresses
def _txt2adr( carrel, file, localLibrary ) :
	
	# configure
	ADR       = 'adr'
	EXTENSION = '.adr'
	HEADER    = [ 'id', 'address' ]
	PATTERN   = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

	# require
	import re
	from pathlib import Path
	
	# _initialize
	key          = _name2key( file )
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )

	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open ( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )
	
	# get and process each address, to the best of my ability
	addresses = re.findall( PATTERN, text )

	# check for addresses
	if len( addresses ) > 0 :

		# open output
		output = localLibrary/carrel/ADR/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8'  ) as handle :

			# _initialize the output
			handle.write( '\t'.join( HEADER ) + '\n' )

			# process each address
			for address in addresses : 
			
				# clean up some more
				address = re.sub( '\/', '', address )
				address = re.sub( '{',  '', address )
				address = re.sub( '}',  '', address )
				
				# output
				handle.write( '\t'.join( [ key, address ] ) + '\n' )


# extract named entities
def _txt2ent( carrel, file, localLibrary=None ) :

	# configure
	EXTENSION = '.ent'
	ENT       = 'ent'
	HEADER    = [ 'id', 'sid', 'eid', 'entity', 'type' ]

	# require
	import spacy
	from pathlib import Path
	
	# _initialize
	key          = _name2key( file )
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# model the text
	nlp            = spacy.load( MODELMEDIUM )
	nlp.max_length = ( len( text ) + 1 )
	doc            = nlp( text )

	# open output
	output = localLibrary/carrel/ENT/( key + EXTENSION )
	with open( output, 'w', encoding='utf-8' ) as handle :

		# _initialize the output
		handle.write( '\t'.join( HEADER ) + '\n' )

		# process each sentence
		for s, sentence in enumerate( doc.sents ) :
		
			# process each entity
			for e, entity in enumerate( sentence.ents ) :
			
				# parse and output
				value = entity.text
				type  = entity.label_
				handle.write( '\t'.join( [ key, str( s + 1 ), str( e + 1 ), value, type ] ) + '\n' )


# extract parts-of-speech
def _txt2pos( carrel, file, localLibrary=None ) :

	# configure
	EXTENSION = '.pos'
	POS       = 'pos'
	HEADER    = [ 'id', 'sid', 'tid', 'token', 'lemma', 'pos' ]

	# require
	import spacy
	from pathlib import Path
	
	# _initialize
	key          = _name2key( file )
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# model the text
	nlp            = spacy.load( MODELMEDIUM )
	nlp.max_length = ( len( text ) + 1 )
	doc            = nlp( text )

	# open output
	output = localLibrary/carrel/POS/( key + EXTENSION )
	with open( output, 'w', encoding='utf-8' ) as handle :

		# _initialize the output
		handle.write( '\t'.join( HEADER ) + '\n' )
		
		# process each sentence
		for s, sentence in enumerate( doc.sents ) :
			
			# process each token
			for t, token in enumerate( sentence ) :

				# process non-spaces
				if token.text > ' ' :
	
					# parse and output
					feature = str( token.text )
					lemma   = str( token.lemma_.lower() )
					pos     = token.pos_
					handle.write( '\t'.join( [  key, str( s + 1 ), str( t + 1 ), feature, lemma, pos ] ) + '\n' )


# given a file, extract domains and urls
def _txt2url( carrel, file, localLibrary ) :

	# configure
	EXTENSION = '.url'
	URLS      = 'urls'
	HEADER    = [ 'id', 'domain', 'url']
	PATTERN   = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

	# require
	import re
	from pathlib import Path
	
	# _initialize
	key          = _name2key( file )
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# get and process each url, to the best of my ability
	urls = re.findall( PATTERN, text )
	
	# check for addresses
	if len( urls ) > 0 :

		# open output
		output = localLibrary/carrel/URLS/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8' ) as handle :

			# _initialize the output
			handle.write( '\t'.join( HEADER ) + '\n' )

			# process each url
			for url in urls :

				# remove white space from end of url
				url = re.sub( '\W$', '', url )
	
				# parse out the domain, to the best of my ability
				domain = re.sub( '.*:\/\/', '', url )
				domain = re.sub( '\/.*',    '', domain )
				domain = re.sub( '\W$',     '', domain )
	
				# output
				handle.write( '\t'.join( [ key, domain, url ] ) + '\n' )


# given a file, output keywords
def _txt2wrd( carrel, file, localLibrary=None ) :

	# configure
	EXTENSION  = '.wrd'
	WRD        = 'wrd'
	NGRAMS     = ( 1, 2 )
	TOPN       = 0.0125
	HEADER     = [ 'id', 'keyword' ]
	NORMALIZE  = 'lower'
	WINDOWSIZE = 5
	POS        = ( 'NOUN', 'PROPN' )

	# require
	from   pathlib                  import Path
	from   textacy.extract.keyterms import yake
	import os
	import spacy
	
	# _initialize
	key          = _name2key( file )
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# debug 
	if VERBOSE : click.echo( ( '\t%s' % key ), err=True )

	# slurp up the file
	with open( file, encoding='utf-8' ) as handle : text = _normalize( handle.read() )

	# model the text and get the keywords
	nlp            = spacy.load( MODELMEDIUM )
	nlp.max_length = os.path.getsize( file ) + 1 
	doc            = nlp( text )

	# do the extraction
	try    : records = ( yake( doc, ngrams=NGRAMS, window_size=WINDOWSIZE, topn=TOPN, normalize=NORMALIZE, include_pos=POS ) )
	except : records = []
	
	# check for records
	if len( records ) > 0 :
	
		# open output
		output = localLibrary/carrel/WRD/( key + EXTENSION )
		with open( output, 'w', encoding='utf-8' ) as handle :

			# _initialize the output
			handle.write( '\t'.join( HEADER ) + '\n' )

			# process each record
			for record in records :

				# do the simplest of normalization and output
				keyword = record[ 0 ]
				if len( keyword ) < 3 : continue
				handle.write( '\t'.join( ( key, keyword ) ) + '\n' )

# start tika
def _startTika() :

	# configure
	JAVA  = 'java'
	JAR   = '-jar'
	SLEEP = 20
	
	# require
	import time
	import subprocess
	
	# _initialize
	started = False
	
	# double check to see if we've already been here
	if _tikaIsRunning() : started = True
	
	# try to start tika
	else :
	
		# get the location of tika-server.jar; needs validation
		tikaHome = str( configuration( 'tikaHome' ) )	
		
		# run the server and conditionally ignore STDERR; set VERBOSE to choose
		if VERBOSE == 3 : subprocess.Popen( [ JAVA, JAR, tikaHome ] )
		else            : subprocess.Popen( [ JAVA, JAR, tikaHome ], stderr=subprocess.DEVNULL )	
		
		# hang out
		time.sleep( SLEEP )
		
		# one last time, check again
		if _tikaIsRunning() : started = True
		
	# done
	return( started )



# given a few configurations, reduce extracted features to a database
def _tsv2db( directory, extension, table, connection ) :

	# require
	import pandas as pd
	
	# debug
	if VERBOSE : click.echo( '\tProcessing ' + table, err=True )
	
	# _initialize
	found = False
	
	# process each file in the given directory
	for index, file in enumerate( directory.glob( extension ) ) :

		# more debugging
		if VERBOSE == 2 : click.echo( '\t' + str( file ), err=True )
		
		# read the file
		df = pd.read_csv( file, sep='\t', header=0, low_memory=False, on_bad_lines='warn', quoting=3, dtype='string' )
			
		# _initialize the features or append to it
		if index == 0 : features = df
		else          : features = pd.concat( [ features, df ], sort=False )

		# update
		found = True
		
	# fill the database, conditionally
	if found : features.to_sql( table, connection, if_exists='replace', index=False )


def build( carrel, directory, erase=False, start=False, localLibrary=None ) :

	"""Create <carrel> from files in <directory>

	Use this command to build a data set ("study carrel") based on the files
	saved in a directory. Once the data set is created the other Toolbox
	commands can be applied to the result. The files can be of any type
	(PDF, Microsoft Word, HTML, etc.), and they can be of any kind (books,
	articles, reports, etc.), and they can be of any number (1, 2, 12, a few
	dozen, hundreds, etc.). The Toolbox is designed to read about a dozen
	journal articles in the form of PDF files. This command requires a Java
	tool called Tika, and it is used to convert the input files into plain
	text as well as extract authors, titles, and dates. If the Toolbox has
	not been configured and/or Tika is not installed, then the Toolbox will
	try to install it on your behalf. If the given directory contains a file
	named 'metadata.csv', then this command will use the file as the source
	of author, title, and date metadata values. This is often very helpful
	because sans metadata it is very difficult to make comparison between
	documents. Please see the full-blown documentation for details."""

	# configure
	CACHE     = 'cache'
	TXT       = 'txt'
	SCHEMA    = '''-- parts-of-speech\ncreate table pos (\n    id    TEXT,\n    sid   INT,\n    tid   INT,\n    token TEXT,\n    lemma TEXT,\n    pos   TEXT\n);\n\n-- name entitites\ncreate table ent (\n    id     TEXT,\n    sid    INT,\n    eid    INT,\n    entity TEXT,\n    type   TEXT\n);\n\n-- keywords\ncreate table wrd (\n    id      TEXT,\n    keyword TEXT\n);\n\n-- email addresses\ncreate table adr (\n    id      TEXT,\n    address TEXT\n);\n\n-- questions\ncreate table questions (\n    id       TEXT,\n    question TEXT\n);\n\n-- urls\ncreate table url (\n    id     TEXT,\n    domain TEXT,\n    url    TEXT\n);\n\n-- bibliographics, such as they are\ncreate table bib (\n    id        TEXT,\n    words     INT,\n    sentence  INT,\n    flesch    INT,\n    summary   TEXT,\n    title     TEXT,\n    author    TEXT,\n    date      TEXT,\n    txt       TEXT,\n    cache     TEXT,\n    pages     INT,\n    extension TEXT,\n    mime      TEXT,\n    genre     TEXT\n);'''
	POS       = 'pos'
	ENT       = 'ent'
	WRD       = 'wrd'
	ADR       = 'adr'
	URL       = 'urls'
	BIB       = 'bib'
	POOLSMALL = 8
	POOLBIG   = 8
	
	# require
	from   multiprocessing import Pool
	from   pathlib         import Path
	import os
	import shutil
	import sqlite3
	import pandas as pd
	import spacy
	
	# _initialize
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	pool         = Pool( POOLSMALL )
	
	# make sure we have Tika Server
	_checkForTika( str( configuration( 'tikaHome' ) ) )
	
	# start tika; the toolbox's secret sauce
	if start :
	
		# debug
		click.echo( '(Step #-1 of 9) Starting Tika server at http://localhost:9998/; please be patient.', err=True )
		
		# go
		if _startTika() == False :
		
			# bummer
			click.echo( "Can't start Tika. Call Eric.", err=True )
			exit()

	# check for tika
	if not _tikaIsRunning() :
	
		click.echo( '''
  WARNING: Tika server at http://localhost:9998/ is not running;
  please start Tika by hand, or add -s to this command.
''', err=True )
		exit()
	
	
	# check tika version here
	
	
	# check to see if the language model has been installed
	try            : nlp  = spacy.load( MODELSMALL )
	except OSError : modelNotFound()

	# check for pre-existing carrel
	if ( localLibrary/carrel ).is_dir() :
	
		# check for erase
		if erase :
		
			# debug and do the work
			click.echo( ( '(Step #0 of 9) Deleting %s' % ( localLibrary/carrel ) ), err=True )
			shutil.rmtree( localLibrary/carrel )
			
		# carrel exists and erasing was not specified
		else :
		
			# warn and exit
			click.echo( ( '''
  WARNING: Carrel exists; specify a name other than "%s" or add -e
  to erase it.''' % carrel ), err=True )
			exit()

	# build skeleton
	click.echo( '(Step #1 of 9) Initializing %s with %s and stop words' % ( carrel, directory ), err=True )
	_initialize( carrel, directory, localLibrary )
		
	# create a list of filenames to process
	filenames = []
	cache     = localLibrary/carrel/CACHE
	for filename in os.listdir( cache ) :
	
		# update list, conditionally
		if filename[ 0 ] == '.' : continue
		else                    : filenames.append( os.path.join( cache, filename ) )
	
	# conditionally slurp up the metadata file and submit 
	click.echo( '(Step #2 of 9) Extracting bibliographics and converting documents to plain text', err=True )
	
	# check for metadata file
	if ( localLibrary/carrel/METADATA ).exists() :
	
		try : metadata = pd.read_csv( localLibrary/carrel/METADATA, index_col='file' )
		except ValueError :
			click.echo( ( '\n  Error: The metadata file (metadata.csv) does not have a\n  column named "file". Remove metadata.csv from the original\n  input directory:\n\n    %s\n\n  Alternatively, edit the metadata file accordingly. Exiting.\n' % directory ), err=True )
			exit()

		pool.starmap( _file2bib, [ [ carrel, filename, metadata, localLibrary ] for filename in filenames ] )
		
	# no metadata file; just do the work
	else : pool.starmap( _file2bib, [ [ carrel, filename, None, localLibrary ] for filename in filenames ] )
		
	# clean up
	pool.close()
	pool = Pool( POOLBIG )

	# bag of words
	click.echo( '(Step #3 of 9) Creating bag-of-words', err=True )
	_txt2bow( carrel, localLibrary )
	
	# output hint
	click.echo( ( "\n  Hint: Now that the bag-of-words has been created, you can begin\n  to use many of the other Reader Toolbox commands while the\n  building process continues. This is especially true for larger\n  carrels. Open a new terminal window and try:\n\n    rdr cluster %s\n    rdr ngrams %s -c | more\n    rdr concordance %s\n    rdr collocations %s\n" % ( carrel, carrel, carrel, carrel ) ), err=True )
	
	# re-create a list of filenames to process
	filenames = []
	txt       = localLibrary/carrel/TXT
	for filename in os.listdir( txt ) : filenames.append( os.path.join( txt, filename ) )

	# extract email addresses
	click.echo( '(Step #4 of 9) Extracting (email) addresses', err=True )
	pool.starmap( _txt2adr, [ [ carrel, filename, localLibrary ] for filename in filenames ] )
	
	# clean up
	pool.close()
	pool = Pool( POOLBIG )

	# extract named entities
	click.echo( '(Step #5 of 9) Extracting (named) entities', err=True )
	pool.starmap( _txt2ent, [ [ carrel, filename, localLibrary ] for filename in filenames ] )
	
	# clean up
	pool.close()
	pool = Pool( POOLBIG )

	# extract parts-of-speech
	click.echo( '(Step #6 of 9) Extracting parts-of-speech', err=True )
	pool.starmap( _txt2pos, [ [ carrel, filename, localLibrary ] for filename in filenames ] )

	# clean up
	pool.close()
	pool = Pool( POOLBIG )

	# extract urls
	click.echo( '(Step #7 of 9) Extracting URLs', err=True )
	pool.starmap( _txt2url, [ [ carrel, filename, localLibrary ] for filename in filenames ] )

	# clean up
	pool.close()
	pool = Pool( POOLBIG )

	# extract keywords
	click.echo( '(Step #8 of 9) Extracting (key) words', err=True )
	pool.starmap( _txt2wrd, [ [ carrel, filename, localLibrary ] for filename in filenames ] )

	# clean up
	pool.close()

	# create database
	click.echo( '(Step #9 of 9) Creating and filling database (reducing)', err=True )
	database   = str( localLibrary/carrel/ETC/DATABASE )
	connection = sqlite3.connect( database )
	cursor     = connection.cursor()
	cursor.executescript( SCHEMA )
	
	# reduce; fill it with content
	_tsv2db( localLibrary/carrel/BIB, '*.bib', 'bib', connection )
	_tsv2db( localLibrary/carrel/ADR, '*.adr', 'adr', connection )
	_tsv2db( localLibrary/carrel/URL, '*.url', 'url', connection )
	_tsv2db( localLibrary/carrel/WRD, '*.wrd', 'wrd', connection )
	_tsv2db( localLibrary/carrel/ENT, '*.ent', 'ent', connection )
	_tsv2db( localLibrary/carrel/POS, '*.pos', 'pos', connection )

	# output another hint
	click.echo( ( '\n  Another hint: The build process is done, and now you ought to\n  be able to use any Toolbox command. For example:\n\n    rdr info %s\n    rdr bib %s | more\n    rdr tm %s\n' % ( carrel, carrel, carrel ) ), err=True )

def summarize( carrel, look=False, localLibrary=None ) :

	'''Summarize <carrel>

	The use of this command will generate a set of reports and save them in
	specific locations in <carrel>'s file system. If you specify the -l
	(look) option, then <carrel>'s index.htm file will be opened in your Web
	browser. You can subsequently use rdr read <carrel> to open the
	index.htm file.'''

	from pathlib import Path
	from datetime import datetime
	
	if localLibrary : localLibrary = Path( localLibrary )
	else            : localLibrary = configuration( 'localLibrary' )
	
	# sanity check
	checkForCarrel( carrel, localLibrary )
	
	# save bibliography
	click.echo( "Creating bibliographies", err=True )
	bibliography( carrel, localLibrary, 'text', save=True )
	bibliography( carrel, localLibrary, 'json', save=True  )
			
	# save sizes	
	click.echo( "Graphing sizes", err=True )
	sizes( carrel, localLibrary, output='boxplot',   save=True )
	sizes( carrel, localLibrary, output='histogram', save=True )
		
	# save readability	
	click.echo( "Graphing readability", err=True )
	flesch( carrel, localLibrary, output='boxplot',   save=True )
	flesch( carrel, localLibrary, output='histogram', save=True )
	
	# save cluster	
	click.echo( "Graphing clusters", err=True )
	cluster( carrel, localLibrary, type='cube', save=True )
	#ctx.invoke( cluster.cluster, carrel=carrel, type='dendrogram', save=True )
	
	# save ngrams	
	click.echo( "Graphing ngrams", err=True )
	ngrams( carrel, localLibrary, count=True, size=1, wordcloud=True, save=True )
	ngrams( carrel, localLibrary, count=True, size=2, wordcloud=True, save=True )
	
	# save entities	
	click.echo( "Graphing entities", err=True )
	entities( carrel, localLibrary, count=True, select='entity', like='any',    wordcloud=True, save=True )
	entities( carrel, localLibrary, count=True, select='entity', like='PERSON', wordcloud=True, save=True )
	entities( carrel, localLibrary, count=True, select='entity', like='GPE',    wordcloud=True, save=True )
	entities( carrel, localLibrary, count=True, select='entity', like='ORG',    wordcloud=True, save=True )
	
	# save pos	
	click.echo( "Graphing parts-of-speach", err=True )
	pos( carrel, localLibrary, count=True, select='lemmas', like='NOUN',  wordcloud=True, save=True )
	pos( carrel, localLibrary, count=True, select='lemmas', like='VERB',  wordcloud=True, save=True )
	pos( carrel, localLibrary, count=True, select='lemmas', like='ADJ',   wordcloud=True, save=True )
	pos( carrel, localLibrary, count=True, select='lemmas', like='ADV',   wordcloud=True, save=True )
	pos( carrel, localLibrary, count=True, select='lemmas', like='PRON',  wordcloud=True, save=True )
	pos( carrel, localLibrary, count=True, select='lemmas', like='PROPN', wordcloud=True, save=True )
	
	# save keywords	
	click.echo( "Graphing keywords", err=True )
	keywords( carrel, localLibrary, count=True, wordcloud=True, save=True )
	
	# create html
	click.echo( "Building HTML page", err=True )
	html = TEMPLATE.replace( '##CARREL##', carrel )
	html = html.replace( '##ITEMS##', str( f"{ extents( carrel, 'items', localLibrary ) :,}" ) )
	html = html.replace( '##WORDS##', str( f"{ extents( carrel, 'words', localLibrary ) :,}" ) )
	html = html.replace( '##FLESCH##', str( extents( carrel, 'flesch', localLibrary ) ) )
	html = html.replace( '##DATECREATED##', str( provenance( carrel, 'dateCreated', localLibrary ) ) )
	html = html.replace( '##CREATOR##', str( provenance( carrel, 'creator', localLibrary ) ) )
	html = html.replace( '##DATE##', datetime.today().strftime('%Y-%m-%d') )
	
	# save html
	#locallibrary = configuration( 'localLibrary' )
	with open( localLibrary/carrel/INDEX, 'w', encoding='utf-8' ) as handle : handle.write( html )
	
	# read, 
	if look : read( carrel, localLibrary )

