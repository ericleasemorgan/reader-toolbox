Exercise: Building carrels
==========================

Simple carrel
--------------

   1. download the Iliad and the Odyssey from https://distantreader.org/apps/homer.zip
   2. uncompress the downloaded zip file and save the result on your desktop
   3. open your terminal application
   4. change directories to the desktop
   5. use the following Toolbox command to create a carrel named homer from the homer directory:::
   
	rdr build homer homer -s -e

   6. Once your carrel is built, you ought to be able to apply just about any Toolbox command to it. I suggest the following:::

	rdr info homer
	rdr ngrams homer -c -s 2
	rdr cluster homer -v
	rdr summarize homer
	rdr read homer

Your first carrel
-----------------

   1. create a new folder on your desktop and calle it practice-carrel
   2. find between six to twelve PDF files on your computer, and copy them to practice-carrel
   3. open your terminal application
   4. change directories to the desktop
   5. use the following Toolbox command to create a carrel named practice-carrel from the practice-carrel directory::
   
	rdr build practice-carrel practice-carrel -s -e

   6. like before, you can now use any Toolbox command against practice-carrel::

	rdr info practice-carrel
	rdr ngrams practice-carrel -c -s 2
	rdr cluster practice-carrel -v
	rdr summarize practice-carrel
	rdr read practice-carrel

Now you can ask yourself, "How is my newly created carrel similar as well as different from the carrel named homer". 


With secret sauce
-----------------

Study carrels can be created from just about any individual folder/directory filled with files. It does not matter how many files there are. It does not matter what type of files they are. It does not matter what the names of the files are. Put a bunch o' files in a directory, and use the Toolbox's build command against the directory.

But your carrels will take on a much greater meaning if you add the Toolbox "secret sauce" to your directory of source files. That secret sauce is a file, or more specifically, a comma-separted value (.csv) file named metadata.csv. If a directory contains a file named metadata.csv, and if the file is a comma-separated values file, and if the file contains colums named "author", "title", "date", and/or "file", and if the value of file is a... file in the given directory, then the Toolbox will read the metadata file as it imports the data, and each of your files will be associated with author, title, and date values. This become indespesible when you want to compare extracted features (ngrams, named-entities, parts-of-speech, topics, etc.) to... authors, titles, and dates. In this way you will be able to ask questdions like: How do the authors' ideas compare, or how does an idea ebb & flow over time or throughout the corpus?

As an example try this:

   1. download the zip file at https://distantreader.org/apps/homer-austen-thoreau.zip; the file includes Homer's Illiad and Odyssey, Jane Austen's Emma, and Henry David Thoreau's Walden.
   2. uncompress the downloaded zip file and save the result on your desktop
   3. inside the newly uncompressed folder ought to be a file called "metadata.csv"; open metadata.csv with your spreadsheet applcation and notice how there are four colums: file, author, title, and date
   4. open your terminal application
   5. change directories to the desktop
   6. use the following Toolbox command to create a carrel named homer-austen-thoreau from the homer-austen-thoreau directory:::
   
	rdr build homer-austen-thoreau homer-austen-thoreau -s -e

   7. once your carrel is built, you ought to do every as before, but some of the Toolbox's output be more meaningful. For example, the bib command will list the authors, titles, and dates from the metadata file. You will be able to search via author's name using the search command. After doing topic modeling, you will be able to pivot the underlying model and see how things compare to authors or dates. Try the following comands to see what I mean:::

	rdr info homer-austen-thoreau
	rdr bib homer-austen-thoreau
	rdr search homer-austen-thoreau -q author:homer | more
	rdr tm homer-austen-thoreau
	rdr tm homer-austen-thoreau -p read -o chart -y barh -f author

After you run the last command, you ought to see a horizontal bar chart illustrating the degree each author wrote about the computed topics. Notice how each author's writings are distinct. Put another way, what did Austen write about, what did Homer write about, and what did Thoreau write about?

Adding a metadata.csv file literally adds four new dimenstions to your study carrel, dimensions that are often take for granted. Creating a metadata.csv file can be challenging though. On the other hand, everybody has a spreadsheet application at their disposal, and it is not difficult to identify the author, title, date, and file name of each of your files. Right?  :)




	