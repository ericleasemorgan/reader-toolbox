
# summarize - given a study carrel, write a set of html files

TEMPLATE = '''
<html>
<head>
<title>Index of ##CARREL##</title>
</head>
<body style='margin: 7%'>

	<h1>Index of ##CARREL##</h1>

	<h2>Contents</h2>
	
		<ul>
		<li>Preface</li>
		<li>Basic characteristics</li>
		</ul>

	<h2>Basic characteristics</h2>

		<table>
		<tr><td>Creator</td><td>##CREATOR##</td></tr>
		<tr><td>Date created</td><td>##DATECREATED##</td></tr>
		<tr><td>Number of items</td><td>##ITEMS##</td></tr>
		<tr><td>Number of words</td><td>##WORDS##</td></tr>
		<tr><td>Average readability score</td><td>##FLESCH##</td></tr>
		<tr><td>Bibliography</td><td><a href="./etc/bibliography.txt">plain text</a>; <a href="./etc/bibliography.htm">HTML</a>; <a href="./etc/bibliography.json">JSON</a></td></tr>
		</table>
		
		<h3>Sizes</h3>
			<p style='text-align: center'>
			<img src='./figures/sizes-boxplot.png' width='49%' /> <img src='./figures/sizes-histogram.png' width='49%' />
			</p>

		<h3>Readability</h3>
			<p style='text-align: center'>
			<img src='./figures/readability-boxplot.png' width='49%' /> <img src='./figures/readability-histogram.png' width='49%' />
			</p>

		<h3>Clusters</h3>
			<p style='text-align: center'>
			<img src='./figures/cluster-dendrogram.png' width='49%' /> <img src='./figures/cluster-cube.png' width='49%' />
			</p>

		<h3>Ngrams</h3>
			<p style='text-align: center'>
			<img src='./figures/unigrams-cloud.png' width='49%' /> <img src='./figures/bigrams-cloud.png' width='49%' />
			</p>

		<h3>Parts-of-speech</h3>
			<p style='text-align: center'>
			<img src='./figures/pos-noun.png' width='49%' /> <img src='./figures/pos-propernoun.png' width='49%' />
			</p>
			<p style='text-align: center'>
			<img src='./figures/pos-pronoun.png' width='49%' /> <img src='./figures/pos-verb.png' width='49%' />
			</p>
			<p style='text-align: center'>
			<img src='./figures/pos-adjective.png' width='49%' /> <img src='./figures/pos-adverb.png' width='49%' />
			</p>

		<h3>Entities</h3>
			<p style='text-align: center'>
			<img src='./figures/entities-any.png' width='49%' /> <img src='./figures/entities-person.png' width='49%' />
			</p>
			<p style='text-align: center'>
			<img src='./figures/entities-gpe.png' width='49%' /> <img src='./figures/entities-org.png' width='49%' />
			</p>

		<h3>Keywords</h3>
			<p style='text-align: center'>
			<img src='./figures/keywords-cloud.png' width='66%' />
			</p>



</body>
</html>
'''

# require
from rdr.commands import *
from rdr          import *

@click.command( options_metavar='<options>' )
@click.argument( 'carrel', metavar='<carrel>' )
@click.option('-l', '--look', is_flag=True, help='when done, look at the result')
@click.pass_context
def summarize( ctx, carrel, look ) :

	'''Summarize <carrel>
	
	The use of this command will generate a set of reports and save them in specific locations in <carrel>'s file system. If you specify the -l (look) option, then <carrel>'s index.htm file will be opened in your Web browser. You can subsequently use rdr read <carrel> to open the index.htm file.'''

	# sanity check
	checkForCarrel( carrel )
	
	# save bibliography
	click.echo( "Creating bibliography", err=True )
	bibliography( carrel, 'text', save=True )
	bibliography( carrel, 'html', save=True )
	bibliography( carrel, 'json', save=True )
			
	# save sizes	
	click.echo( "Graphing sizes", err=True )
	size( carrel, output='boxplot',   save=True )
	size( carrel, output='histogram', save=True )
		
	# save readability	
	click.echo( "Graphing readability", err=True )
	flesch( carrel, output='boxplot',   save=True )
	flesch( carrel, output='histogram', save=True )
	
	# save cluster	
	click.echo( "Graphing clusters", err=True )
	clusters( carrel, type='cube',       save=True )
	#ctx.invoke( cluster.cluster, carrel=carrel, type='dendrogram', save=True )
	
	# save ngrams	
	click.echo( "Graphing ngrams", err=True )
	ngramss( carrel, count=True, size=1, wordcloud=True, save=True )
	ngramss( carrel, count=True, size=2, wordcloud=True, save=True )
	
	# save entities	
	click.echo( "Graphing entities", err=True )
	entities( carrel, count=True, select='entity', like='any',    wordcloud=True, save=True )
	entities( carrel, count=True, select='entity', like='PERSON', wordcloud=True, save=True )
	entities( carrel, count=True, select='entity', like='GPE',    wordcloud=True, save=True )
	entities( carrel, count=True, select='entity', like='ORG',    wordcloud=True, save=True )
	
	# save pos	
	click.echo( "Graphing parts-of-speach", err=True )
	partsofspeech( carrel, count=True, select='lemmas', like='NOUN',  wordcloud=True, save=True )
	partsofspeech( carrel, count=True, select='lemmas', like='VERB',  wordcloud=True, save=True )
	partsofspeech( carrel, count=True, select='lemmas', like='ADJ',   wordcloud=True, save=True )
	partsofspeech( carrel, count=True, select='lemmas', like='ADV',   wordcloud=True, save=True )
	partsofspeech( carrel, count=True, select='lemmas', like='PRON',  wordcloud=True, save=True )
	partsofspeech( carrel, count=True, select='lemmas', like='PROPN', wordcloud=True, save=True )
	
	# save keywords	
	click.echo( "Graphing keywords", err=True )
	keywords( carrel, count=True, wordcloud=True, save=True )
	
	# create html
	click.echo( "Building HTML page", err=True )
	html = TEMPLATE.replace( '##CARREL##', carrel )
	html = html.replace( '##ITEMS##', str( extents( carrel, 'items' ) ) )
	html = html.replace( '##WORDS##', str( extents( carrel, 'words' ) ) )
	html = html.replace( '##FLESCH##', str( extents( carrel, 'flesch' ) ) )
	html = html.replace( '##DATECREATED##', str( provenance( carrel, 'dateCreated' ) ) )
	html = html.replace( '##CREATOR##', str( provenance( carrel, 'creator' ) ) )
	
	# save html
	locallibrary = configuration( 'localLibrary' )
	with open( locallibrary/carrel/INDEX, 'w', encoding='utf-8' ) as handle : handle.write( html )
	
	# read, 
	if look : reads( carrel )
	