
# require
from rdr import *

# config
@click.command()
@click.argument( 'topics' )
@click.argument( 'dimensions' )
@click.argument( 'topdocs' )
def malletUse( topics, dimensions, topdocs ) :

	"""Use model tool"""

	click.echo( topics )
	click.echo( dimensions )
	click.echo( topdocs )

	cmd = MALLETHOME + '/bin/mallet train-topics --input ' + MODELDIR + '/' + VECTORS + ' --num-topics ' + topics + ' --num-top-words ' + dimensions + ' --num-top-docs ' + topdocs + ' --num-iterations 1200 ' +  '--num-threads 10 ' + '--optimize-interval 10 ' + '--output-doc-topics ' + MODELDIR + '/topics.tsv ' + '--output-topic-docs ' + MODELDIR + '/documents.txt ' + ' --output-topic-keys ' + MODELDIR + '/keys.tsv ' + ' --random-seed 42 ' + '--topic-word-weights-file ' + MODELDIR + '/weights.tsv' + ' --word-topic-counts-file ' + MODELDIR + '/counts.txt ' + ' --xml-topic-phrase-report ' + MODELDIR + '/phrases.xml ' + '--xml-topic-report ' + MODELDIR + '/topics.xml'

	click.echo( cmd, err=True)
	os.system( cmd )
