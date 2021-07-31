
# configure

# require
from rdr import *
import webbrowser

# read
@click.command()
@click.argument( 'carrel' )
def read( carrel ) :

	"""Open the study carrel in a web browser"""
		
	url = 'file://' + LOCALLIBRARY + '/' + carrel + '/index.htm'
	webbrowser.open( url )