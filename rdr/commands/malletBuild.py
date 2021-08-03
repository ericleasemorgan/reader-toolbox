
# require
from rdr import *

# config
@click.command()
@click.argument( 'carrel' )
def malletBuild( carrel ) :

	"""Create MALLET vectors file"""

	# initialize
	applicationDirectory = pathlib.Path( click.get_app_dir( APPLICATIONDIRECTORY ) )
	configurationFile    = applicationDirectory / CONFIGURATIONFILE
	configurations       = ConfigParser()
	
	# read configurations
	configurations.read( str( configurationFile ) )
	localLibrary   = configurations[ 'LOCALLIBRARY' ][ 'locallibrary' ] 

	# initialize
	corpus    = localLibrary + '/' + carrel  + '/' + TXT
	stopwords = localLibrary + '/' + carrel  + '/' + ETC + '/' + STOPWORDS
	vectors   = MODELDIR     + '/' + VECTORS

	cmd = MALLETHOME + '/bin/mallet import-dir --input ' + corpus + ' --output ' + vectors + ' --keep-sequence TRUE --stoplist-file ' + stopwords
	click.echo( cmd, err=True )
	os.system( cmd )
