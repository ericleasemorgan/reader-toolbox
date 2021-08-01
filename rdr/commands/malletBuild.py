
# require
from rdr import *

# config
@click.command()
@click.argument( 'carrel' )
def malletBuild( carrel ) :

	"""Create MALLET vectors file"""

	# initialize
	corpus    = LOCALLIBRARY + '/' + carrel  + '/' + TXT
	stopwords = LOCALLIBRARY + '/' + carrel  + '/' + ETC + '/' + STOPWORDS
	vectors   = MODELDIR     + '/' + VECTORS

	cmd = MALLETHOME + '/bin/mallet import-dir --input ' + corpus + ' --output ' + vectors + ' --keep-sequence TRUE --stoplist-file ' + stopwords
	click.echo( cmd, err=True )
	os.system( cmd )
