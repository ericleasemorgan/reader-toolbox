# rdr.py - a command-line interface for using Distant Reader study carrels

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 30, 2021 - in Three Oaks with Pat; first real working version

# require
from rdr import *
import rdr.commands.browse       as browse
import rdr.commands.cluster      as cluster
import rdr.commands.concordance  as concordance
import rdr.commands.config       as config
import rdr.commands.datasette    as datasette
import rdr.commands.features     as features
import rdr.commands.download     as download
import rdr.commands.list         as list
import rdr.commands.ngrams       as ngrams
import rdr.commands.read         as read
import rdr.commands.malletBuild  as malletBuild
import rdr.commands.malletUse    as malletUse
import rdr.commands.malletReport as malletReport

# initialize 
@click.group()
def rdr() : pass

# update the list of commands
rdr.add_command( browse.browse )
rdr.add_command( cluster.cluster )
rdr.add_command( concordance.concordance )
rdr.add_command( config.config )
rdr.add_command( datasette.datasette )
rdr.add_command( features.features )
rdr.add_command( download.download )
rdr.add_command( list.list )
rdr.add_command( ngrams.ngrams )
rdr.add_command( ngrams.ngrams )
rdr.add_command( read.read )
rdr.add_command( malletBuild.malletBuild )
rdr.add_command( malletUse.malletUse )
rdr.add_command( malletReport.malletReport )

# do the work
if __name__ == '__main__' : rdr()
