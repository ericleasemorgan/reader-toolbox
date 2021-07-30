
# require
from rdr import *

# config
@click.command()
def config() :
	"""Get and set the configured location of your study carrels"""
	directory = click.get_app_dir( 'rdr' )
	click.echo( directory )
