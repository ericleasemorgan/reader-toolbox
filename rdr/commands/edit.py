
# require
from rdr import *

# config
@click.command()
@click.option('-f', '--file', default='stopwords', type=click.Choice( [ 'stopwords', 'foobar' ] ), help='edit the given file')
@click.argument( 'carrel', metavar='<carrel>' )
def edit( carrel, file ) :

	'''Edit the stopword list of the given <carrel>'''
	
	# sanity check
	checkForCarrel( carrel )

	# branch accordingly
	if file == 'stopwords' :
		file = str( configuration( 'localLibrary' )/carrel/ETC/STOPWORDS )
		click.edit( filename=file )