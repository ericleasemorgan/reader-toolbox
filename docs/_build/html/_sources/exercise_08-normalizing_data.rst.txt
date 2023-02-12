Exercise: Normalizing
=====================

The Reader Toolbox takes sets of narrative text as input, and it outputs sets of extracted features. As detailed in another section of the documentation, these extracted features include: bibliographics, parts-of-speech, named-entities, email addresses, URLs, an statistically significant keywords. The features have been saved as tab-delimited files as well as reduced to an SQLite relational database file. Thus, analysis against a study carrel can be done through Toolbox commands, through various application programmer interfaces, or through any number of graphical user interface (GUI) applications. A free and cross-platform application called OpenRefine is one such GUI application, and this section outlines how to exploit it for the purposes of using and understanding any carrel.


Keywords
--------

Let's use OpenRefine to address the question, "What are Homer's works about, and how is this aboutness manifested over the corpus?". To address this question, we can analyze the files in the wrd directory, where the keyword files are saved. Here's how:

1. download, install, and lauch OpenRefine

2. choose all 48 files from the homer study carrel wrd directory

3. accept the defaults as you continue configure parsing and creating your OpenRefine project; remember that every file in the wrd directory is a tab-delimited file and you must use the "CSV / TSV / separater-based files" option to complete importing the data 

4. after the data has been imported, create a text-based facet on the keywords column

5. select a keyword of interest, and then create a text-based facet on the id column

6. in the end a list of identifiers will be displayed denoting which items in the carrel are about the selected keyword

7. select different keywords, and notice how the list of faceted identifiers changes

.. image:: ./figures/normalizing-01.png
.. image:: ./figures/normalizing-02.png
.. image:: ./figures/normalizing-03.png
.. image:: ./figures/normalizing-04.png
.. image:: ./figures/normalizing-05.png
.. image:: ./figures/normalizing-06.png
.. image:: ./figures/normalizing-07.png
.. image:: ./figures/normalizing-08.png
.. image:: ./figures/normalizing-09.png

The same thing can be done the other way around, and you can ask yourself, "What is a given item about?" Here's how:

1. use the Remove All button to return your project to the default state

2. create a text-based facet on the id column

3. select an id of interest, and notice how the keywwords associated with the item are displayed

.. image:: ./figures/normalizing-10.png
.. image:: ./figures/normalizing-11.png
.. image:: ./figures/normalizing-12.png


The tab-delimited files found in the wrd folder/directory are easy use because they contain a small number of columns with simple data types. The other delimited files are more complex, but by extension, they offer the ability to address more complex questions.


Named entities
--------------

The named enity files afford the ability to adress questions regarding people, places, organizations, and other things. Let's address the question, "Who are the people mentioned in the Iliad and the Odyssey, and how often?" Here's how:

1. use the Open... button to create a new project

2. import all the files found the homer study carrel pos directory; remember that every file in the wrd directory is a tab-delimited file and you must use the "CSV / TSV / separater-based files" option to complete importing the data 

3. create a text-based facet on column named type

4. select the PERSON type, and create a text-based facet on the entity column

5. sort the result based on count, and the result addresses the question; Jove is the most frequently mentioned person

.. image:: ./figures/normalizing-13.png
.. image:: ./figures/normalizing-14.png
.. image:: ./figures/normalizing-15.png
.. image:: ./figures/normalizing-16.png

You can then ask, "In what items is Jove mentioned and how often?" To answer this question, you:

6. select a person of intered (Jove)

7. create a text-based facet on the id column

8. sort the result on count; Jove appears in many items, and he appears in the eigth book of the Iliad the most

.. image:: ./figures/normalizing-17.png
.. image:: ./figures/normalizing-18.png




