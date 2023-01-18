Structure of a study carrel
===========================

It can not be stated strongly enough, *the Distant Reader Toolbox takes a set of unstructured data (files of narrative text) as input, and it outputs a set of structured data -- a "study carrel" -- intended to be computed against.*

Each study carrel is a data set, and like other all other data sets, they are purposely designed to address research questions. Once you understand the strucuture and content of study carrels, you will be able to address research questions not explicitly addressed by the various Toolbox commands and functions. Thus, the purpose of this section is to explicitly outline the types of content a study carrel contains as well as how the data is origanized so you can address more interesting research questions.

First and foremost, the vast majority of the files in a study carrel are plain text files. The only files you can not open and make sense with in your text editor are the various images files found in the figures directory and the SQLite relational database file (reader.db) found in the etc directory. Consequently, given any study carrel, the student, researcher, or scholar can compute against it (ask it questions) using a myriad of applications or programming languages. The most obvious applications include any spreadsheet or database application. Specific examples include OpenRefine for tabular data analysis, Wordle for creating word clouds, AntConc for concordancing, Gephi for network analysis and visualization, or Topic Modeling Tool for topic modeling. Since most of the data contained in a study carrel is tabular in nature -- meaning it is constituted in the form of rows and columns -- study carrel content can be read by any programming language (R, Python, C, Java, Ruby, Bash, etc.) and computed against in the manner of other data science techniques. The unstructured plain text files found in every carrel (such as all the files found in the the txt directory or the reader.txt file found in the etc directory) are computable as well, but the techqiues fall more into the category of natural language processing and less into traditional data science.

Second, each study carrel is contained in a single directory with a number of consistently named subdirectories and files, as the following diagram illustrates.

[INSERT IMAGE OF FILE SYSTEM HERE.]

