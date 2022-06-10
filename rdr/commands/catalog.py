
# catalog - given a location, output a list of study carrels

# require
from rdr import *

@click.command( options_metavar='<options>' )
@click.option('-h', '--human', is_flag=True, help='output in a more human-readable form')
@click.option('-l', '--location', default='local', type=click.Choice( [ 'local', 'remote' ] ), help='output in a more human-readable form')
def catalog( human, location ) :

	"""List study carrels
	
	Use this command to enumerate the study carrels cached locally or remotely available at http://library.distantreader.org. The remote option, by default, returns a tab-delimited stream very amenable to post processing with utilities such as cut, grep, sort, and less.
	
	Examples:
	
	\b
	  rdr catalog
	  rdr catalog -l remote
	  rdr catalog -l remote -h

	See also: rdr download --help"""
	
	# do the work and done
	click.echo( catalogs( location, human ) )