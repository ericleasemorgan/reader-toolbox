

# rdr.py - a command-line interface for using Distant Reader study carrels

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 30, 2021 - in Three Oaks with Pat; first real working version

# require
from rdr import *
import rdr.commands.browse      as browse
import rdr.commands.cluster     as cluster
import rdr.commands.concordance as concordance
import rdr.commands.sql   as sql
import rdr.commands.download    as download
import rdr.commands.get         as get
import rdr.commands.grammars    as grammars
import rdr.commands.catalog     as catalog
import rdr.commands.ngrams      as ngrams
import rdr.commands.play        as play
import rdr.commands.read        as read
import rdr.commands.edit         as edit
import rdr.commands.set         as set
import rdr.commands.tm          as tm

# initialize 
@click.group()
def rdr() : pass

# update the list of commands
rdr.add_command( browse.browse )
rdr.add_command( cluster.cluster )
rdr.add_command( concordance.concordance )
rdr.add_command( sql.sql )
rdr.add_command( download.download )
rdr.add_command( get.get )
rdr.add_command( edit.edit )
rdr.add_command( grammars.grammars )
rdr.add_command( catalog.catalog )
rdr.add_command( ngrams.ngrams )
rdr.add_command( play.play )
rdr.add_command( read.read )
rdr.add_command( set.set )
rdr.add_command( tm.tm )

# do the work
if __name__ == '__main__' : rdr()
