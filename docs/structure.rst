Structure of a carrel
=====================

It can not be stated strongly enough, *the Distant Reader Toolbox takes a set of unstructured data (files of narrative text) as input, and it outputs a set of structured data -- a "study carrel" -- intended to be computed against.*

Each study carrel is a data set, and like other all other data sets, they are purposely designed to address research questions. Once you understand the strucuture and content of study carrels, you will be able to address research questions not explicitly addressed by the various Toolbox commands and functions. Thus, the purpose of this section is to explicitly outline the types of content a study carrel contains as well as how the data is origanized so you can address more interesting research questions.

First and foremost, the vast majority of the files in a study carrel are plain text files. The only files you can not open and make sense with in your text editor are the various images files found in the figures directory and the SQLite relational database file (reader.db) found in the etc directory. Consequently, given any study carrel, the student, researcher, or scholar can compute against it (ask it questions) using a myriad of applications or programming languages. The most obvious applications include any spreadsheet or database application. Specific examples include OpenRefine for tabular data analysis, Wordle for creating word clouds, AntConc for concordancing, Gephi for network analysis and visualization, or Topic Modeling Tool for topic modeling. Since most of the data contained in a study carrel is tabular in nature -- meaning it is constituted in the form of rows and columns -- study carrel content can be read by any programming language (R, Python, C, Java, Ruby, Bash, etc.) and computed against in the manner of other data science techniques. The unstructured plain text files found in every carrel (such as all the files found in the the txt directory or the reader.txt file found in the etc directory) are computable as well, but the techqiues fall more into the category of natural language processing and less into traditional data science.

Second, each study carrel is contained in a single directory with a number of consistently named subdirectories and files, as the following list illustrates:

  * adr
  * bib
  * cache
  * ent
  * etc
  * figures
  * pos
  * provenance.tsv
  * txt
  * urls
  * wrd    

The following sections describe the type of content found in each subdirectory and outlines ways it can be used.

adr
---

Email addresses

This subdirectory contains a set of tab-delimited files. Each file contains a set of email addresses extracted from the documents in your corpus. While the files' names end in .adr, they are plain text files that can be imported into for favorite spreadsheet, database, or analysis application. The files have two columns:

   1. **id** - the unique identifer of a document in the carrel

   2. **address** - an email address
   
The files in this directory can humorously answer the question "Who are you gonna call?", but you might also use it to learn who might be commonly mentioned across your carrel.


bib
---

Bibliographics

This subdirectory contains a set of tab-delimited files. Each file contains a set of rudimentary bibliographic information from a given document in your corpus. While the files' names end in .bib, they are plain text files that can be imported into for favorite spreadsheet, database, or analysis application. The files have thirteen columns: 

   1. **id** - the unique identifer of a document in the carrel; this value is rooted in the name of the original document sans its extension

   2. **author** - the name(s) of the creators of the document; this value comes from the optionally included metadata.csv file when the carrel was created, or it is extracted from the original document by the Tika server, or this value will be empty

   3. **title** - the title of the document; this value comes from the optionally included metadata.csv file when the carrel was created, or it extracted from the original document by the Tika server, or it is the name of the original file sans the file's extension 

   4. **date** - the date of the document; this value comes from the optionally included metadata.csv file when the carrel was created, or it extracted from the original document by the Tika server, or this value will be empty

   5. **page** - 
 
   6. **extension**

   7. **mime**

   8. **words**

   9. **sentences**

   10. **flesch**

   11. **summary**

   12. **cache**

   13. **txt**

These files help answer the question "What items are in my corpus, and how can they be described?"


cache
-----

Original Input Files

This subdirectory contains original copies of the files you intended for analysis. It is populated by harvesting content from URLs or were supplied in the zip file you uploaded to the Reader. Each file is named with a unique and somewhat meaningful name and an extension. These files are intended for reading on your computer, or better yet, printed and then read in the more traditional manner.


ent
---

Named Entities

This subdirectory contains a set of tab-delimited files, and each file contains a set of named entities from a given document in your corpus. While the files' names end in .ent, they are plain text files that can be imported into for favorite spreadsheet, database, or analysis application. The files have five columns:

   1. **id** - the unique identifer of a document in the carrel

   2. **sid**

   3. **eid**

   4. **entity**

   5. **type**

These files help answer questions regarding who, what, when, where, how, and how many.


etc
---

Miscellaneous

This subdirectory contains a set of ancillary files, and each are described below:
 
   1. **reader.db**

   2. **reader.txt**

   3. **stopwords.txt**


figures
-------

Graphics And Visualizations


pos
---

Parts-Of-Speach

This subdirectory contains a set of tab-delimited files, and each file contains a set of part-of-speech files from a given document in your corpus. While the files' names end in .pos, they are plain text files that can be imported into for favorite spreadsheet, database, or analysis application. The files have six columns:

   1. **id** - the unique identifer of a document in the carrel
 
   2. **sid**
 
   3. **tid**

   4. **token**

   5. **lemma**

   6. **pos**

These files help answer question regarding who, what, how, how many, and actions as well as grammer and style.


provenance.tsv
--------------


This file is a nod towards whence the carrel came - provenance. It is a tab-delimited file with five unlabeled columns:

   1. the process used to create the carrel, and this value will usually be "toolbox"
   2. the name of the carrel when it was origainally created
   3. the date when the carrel was created and in the form of yyyy-mm-dd
   4. the local time when the carrel was created and in the form of hh:mm
   5. the username of the person who created the carrel
   6. the path to where the original files where found to create the carrel
   

txt
---

Plain text versions of cached items

This subdirectory contains plain text versions of the files stored in the cache directory. A plain text version of each &amp; every item in the cache directory ought to exist in this directory. The contents of this directory is what was used to do the Reader's analysis. The contents of this directory are excellent candidates for further analysis with tools such as concordances, indexers, or topic modelers.

urls
----

Universal Resource Locators

This subdirectory contains a set of tab-delimited files, and each file contains a set of URLs from a given document in your corpus. While the files' names end in .url, they are plain text files that can be imported into for favorite spreadsheet, database, or analysis application. The files have three columns:

   1. **id** - the unique identifer of a document in the carrel

   2. **domain** - the domain of a URL; everthing after the pair of slashes ("//") and before the initial slash ("/")

   3. **url** - Universal Resource Locator
   
These files help answer questions regarding document provenance and relationships as well as addressing the perenial issue of "finding more like this one".


wrd
---

Statistically Significant Keywords

This subdirectory contains a set of tab-delimited files, and each file contains a set of computed keywords from a given document in your corpus. While the files' names end in .wrd, they are plain text files that can be imported into your favorite spreadsheet, database, or analysis application. The files have two columns:

   1. **id** - the unique identifer of a document in the carrel

   2. **keyword** - a statistically computed keyword or phrase; this word/phrase was computed using a variation of the venerable TF/IDF algorigthm
  
These files help answer questions such as "What is this document about?"
