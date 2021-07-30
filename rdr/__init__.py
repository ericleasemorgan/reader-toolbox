
# configurations/constants
LOCALLIBRARY  = '/Users/eric/Desktop/library'
REMOTELIBRARY = 'http://library.distantreader.org'

# requirements
from tempfile import TemporaryFile
from zipfile  import ZipFile
import click
import os
import requests
