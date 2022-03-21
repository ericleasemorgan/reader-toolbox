
# summarize - given a study carrel, write a set of html files

TEMPLATE = '''
<html>
<head>
<title>Summary of ##CARREL##</title>
</head>
<body style='margin: 7%'>

	<h1>Summary of ##CARREL##</h1>

	<h2>Introduction</h2>

	<ol>
		<li>Creator</li>
		<li>Title</li>
		<li>Date</li>
		<li>Number of items</li>
		<li>Number of words</li>
		<li>Average readability score</li>
		<li><a href="./etc/bibliography.txt">Bibliography</a></li>
	</ol>

	<h2>Sizes</h2>
		<p style='text-align: center'>
		<img src='./figures/sizes-boxplot.png' width='49%' /> <img src='./figures/sizes-histogram.png' width='49%' />
		</p>

	<h2>Readability</h2>
		<p style='text-align: center'>
		<img src='./figures/readability-boxplot.png' width='49%' /> <img src='./figures/readability-histogram.png' width='49%' />
		</p>

	<h2>Clusters</h2>
		<p style='text-align: center'>
		<img src='./figures/cluster-dendrogram.png' width='49%' /> <img src='./figures/cluster-cube.png' width='49%' />
		</p>

	<h2>Ngrams</h2>
		<p style='text-align: center'>
		<img src='./figures/unigrams-cloud.png' width='49%' /> <img src='./figures/bigrams-cloud.png' width='49%' />
		</p>

	<h2>Keywords</h2>
		<p style='text-align: center'>
		<img src='./figures/keywords-cloud.png' width='66%' />
		</p>

</body>
</html>
'''

# require
from rdr          import *
from rdr.commands import *

@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-l', '--look', is_flag=True, help='when done, look at the result')
@click.pass_context
def summarize( ctx, carrel, look ) :

	'Summarize <carrel>'

	# sanity check
	checkForCarrel( carrel )
	
	# save bibliography
	click.echo( "Creating bibliography", err=True )
	ctx.invoke( bib.bib, carrel=carrel, save=True )
		
	# save sizes	
	click.echo( "Graphing sizes", err=True )
	ctx.invoke( sizes.sizes, carrel=carrel, output='boxplot',   save=True )
	ctx.invoke( sizes.sizes, carrel=carrel, output='histogram', save=True )
		
	# save readability	
	click.echo( "Graphing readability", err=True )
	ctx.invoke( readability.readability, carrel=carrel, output='boxplot',   save=True )
	ctx.invoke( readability.readability, carrel=carrel, output='histogram', save=True )
	
	# save cluster	
	click.echo( "Graphing clusters", err=True )
	ctx.invoke( cluster.cluster, carrel=carrel, type='cube',       save=True )
	#ctx.invoke( cluster.cluster, carrel=carrel, type='dendrogram', save=True )
	
	# save ngrams	
	click.echo( "Graphing ngrams", err=True )
	ctx.invoke( ngrams.ngrams, carrel=carrel, count=True, size=1, wordcloud=True, save=True )
	ctx.invoke( ngrams.ngrams, carrel=carrel, count=True, size=2, wordcloud=True, save=True )
	
	# save keywords	
	click.echo( "Graphing keywords", err=True )
	ctx.invoke( wrd.wrd, carrel=carrel, count=True, wordcloud=True, save=True )
	
	# create html
	html = TEMPLATE.replace( '##CARREL##', carrel )
	
	# save html
	locallibrary = configuration( 'localLibrary' )
	with open( locallibrary/carrel/INDEX, 'w' ) as handle : handle.write( html )
	
	# read, 
	if look : ctx.invoke( read.read, carrel=carrel )
	