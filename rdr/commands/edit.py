
# require
from rdr import *

# config
@click.command()
@click.argument( 'carrel', metavar='<carrel>' )
def edit( carrel ) :

	'''Modify the stop word list of <carrel>.

When using subcommands such as ngrams or tm, you may observe words of no importance to your analysis. Iteratively use this subcommand to update the stop word list of <carrel> and ultimately remove those words from view. Change the value of your shell's EDITOR environment variable to define what text editor you want to use. Alternatively, you can use your graphical text editor to edit the ./etc/stopwords.txt file found in every study carrel. Just remember, you MUST save the changes as plain text (.txt), not .doc, docx, nor .rtf.

Example: rdr edit homer'''
    
	# sanity check
	checkForCarrel( carrel )

	# initialize and do the work
	file = str( configuration( 'localLibrary' )/carrel/ETC/STOPWORDS )
	click.edit( filename=file )