
# require
from rdr import *

# config
@click.command()
@click.argument( 'carrel', metavar='<carrel>' )
def edit( carrel ) :

	'''Edit <carrel>'s stopword list
	
	When using subcommands such as ngrams or tm, you will notice words of no importance to your analysis. Iteratively use this subcommand to update the <carrel>'s stop word list and ultimately remove them. Change the value of your shell's EDITOR environment variable to define what text editor you want to use.

    Example: rdr edit homer'''
    
	# sanity check
	checkForCarrel( carrel )

	# initialize and do the work
	file = str( configuration( 'localLibrary' )/carrel/ETC/STOPWORDS )
	click.edit( filename=file )