# rdr.py - a command-line interface for using Distant Reader study carrels

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 30, 2021 - in Three Oaks with Pat; first real working version

# require
from rdr import *
import rdr.commands.config    as config
import rdr.commands.list      as list
import rdr.commands.datasette as datasette
import rdr.commands.harvest   as harvest
import rdr.commands.cluster   as cluster
import rdr.commands.features  as features
import rdr.commands.ngrams    as ngrams

# initialize 
@click.group()
def rdr() : pass

# update the list of commands
rdr.add_command( config.config )
rdr.add_command( list.list )
rdr.add_command( datasette.datasette )
rdr.add_command( harvest.harvest )
rdr.add_command( cluster.cluster )
rdr.add_command( features.features )
rdr.add_command( ngrams.ngrams )

# do the work
if __name__ == '__main__' : rdr()
