import os,sys

from pycvsanaly.plugins import Plugin, register_plugin
from pycvsanaly.FindProgram import find_program

import pycvsanaly.database as database

# Local import only for graph plugin
import intermediate_tables as intmodule
import tables_skeleton as tables

import graph_global as g_global
import graph_pie as g_pie
import graph_gini as g_gini
import graph_activity as g_activity
import graph_inequality as g_inequality
import graph_heatmaps as g_heatmaps
import graph_evolution as g_evolution
#import graph_generations as g_generations

class GraphsPlugin (Plugin):

    def __init__ (self, db = None, opts = []):
        Plugin.__init__ (self, db)

        self.output_dir = None
        for opt, value in opts:
            if opt in ("--output-dir"):
                self.output_dir = value

        self.name = "graphs"
        self.author = "Alvaro Navarro and Alvaro del Castillo"
        self.description = "Graphs and intermediate tables for cvsanaly-web"
        self.date = "23/01/07"

    def get_options (self):
        return ["output-dir="]

    def usage (self):
        print """Graphs:

  --output-dir      Output directory [./graphs]
"""

    def run (self):
        ploticus = find_program ("ploticus")
        gnuplot = find_program ("gnuplot")

        # Fun starts here. We received a database descriptor.
        self.db.create_table('commiters_module', tables.commiters_module)
        #db.create_table('comments', tables.comments)
        self.db.create_table('cvsanal_fileTypes', tables.cvsanal_fileTypes)
        self.db.create_table('cvsanal_temp_commiters',tables.cvsanal_temp_commiters)
        self.db.create_table('cvsanal_temp_modules', tables.cvsanal_temp_modules)
        self.db.create_table('cvsanal_temp_inequality',tables.cvsanal_temp_inequality)

        #intmodule.intermediate_table_commitersmodules(db)
        intmodule.intermediate_table_commiters(self.db)
        intmodule.intermediate_table_fileTypes(self.db)
        intmodule.intermediate_table_modules(self.db)
        intmodule.intermediate_table_commiters_id(self.db)

        # Create and change
        if self.output_dir is None:
            graphs_directory = 'graphs'
        else:
            graphs_directory = self.output_dir

        if not os.path.isdir (graphs_directory):
            os.mkdir (graphs_directory)

        try:
            os.chdir (graphs_directory)
        except:
            pass

        # Print graphs
        print "Plotting globals grahps"
        if gnuplot is not None:
            g_global.plot (self.db)
        else:
            print "gnuplot not found, skipping global graphs"

        if gnuplot is not None:
            g_evolution.plot (self.db)
        else:
            print "gnuplot not found, skipping evolution graphs"

        if ploticus is not None:
            g_pie.plot (self.db)
        else:
            print "ploticus not found, skipping pie graphs"

        if gnuplot is not None:
            if ploticus is not None:
                g_gini.plot (self.db)
            else:
                print "ploticus not found, skipping gini graphs"
        else:
            print "gnuplot not found, skipping gini graphs"

        if ploticus is not None:
            g_activity.plot (self.db)
        else:
            print "ploticus not found, skipping activity graphs"

        if gnuplot is not None:
            g_inequality.plot (self.db)
        else:
            print "gnuplot not found, skipping inequality graphs"

        if ploticus is not None:
            g_heatmaps.plot (self.db)
        else:
            print "ploticus not found, skipping heatmaps graphs"

register_plugin ('graphs', GraphsPlugin)
