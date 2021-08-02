
# name of application and basename of configuration file
APPLICATION   = 'rdr'
CONFIGURATION = '.rdrrc'

REMOTELIBRARY = 'foo'
LOCALLIBRARY  = 'bar'

# local carrel
ETC           = 'etc'
CORPUS        = 'reader.txt'
STOPWORDS     = 'stopwords.txt'
TXT           = 'txt'

# spacy
MODEL         = 'en_core_web_sm'

# mallet
MALLETHOME = "/Users/eric/Desktop/mallet"
MODELDIR   = MALLETHOME + '/' + 'tmp'
VECTORS    = 'model.vec'

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
import pathlib


