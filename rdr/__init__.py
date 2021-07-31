
# configurations/constants
LOCALLIBRARY  = '/Users/eric/Desktop/library'
REMOTELIBRARY = 'http://library.distantreader.org'
MODEL         = 'en_core_web_sm'
ETC           = 'etc'
CORPUS        = 'reader.txt'

# requirements
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity
from tempfile import TemporaryFile
from zipfile  import ZipFile
import click
import matplotlib.pyplot as plt
import os
import requests
import spacy
import sys
import textacy


