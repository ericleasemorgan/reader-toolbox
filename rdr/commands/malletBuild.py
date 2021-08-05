
# require
from rdr import *

# config
@click.command()
@click.argument( 'carrel' )
def malletBuild( carrel ) :

	"""Create MALLET vectors file"""

	# require
	from os import system
	
	# initialize
	localLibrary = configuration( 'localLibrary' )

	# initialize
	txt       = localLibrary/carrel/TXT
	stopwords = localLibrary/carrel/ETC/STOPWORDS
	vectors   = MODELDIR + '/' + VECTORS

	cmd = MALLETHOME + '/bin/mallet import-dir --input ' + str( txt ) + ' --output ' + vectors + ' --keep-sequence TRUE --stoplist-file ' + str( stopwords )
	click.echo( cmd, err=True )
	system( cmd )
