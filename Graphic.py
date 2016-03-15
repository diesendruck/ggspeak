#!/usr/bin/python

# Title: Graphic Object Class Definition
# Author: Maurice Diesendruck
# Last updated: 2015-09-01
#
# Class for general graph object.
#
# Note: Changed ggplot source code. See link: http://bit.ly/1UkFZCO

from ggplot import *


class Graphic(object):
    """A general graph template.

    Declares all the attributes that a graphing library would need, to build
    the string used to plot the graph.
    """

    def __init__(self):
        """Defines characteristics of graph.

        Sets values for graph characteristics. Some are None, others are
        strings or numbers.
        """
        self.dataset = None
        self.filename = None
        self.data_cols = [None]
        self.geom = None
        self.color = 'steelblue'
        self.xscale = [None, None]
        self.yscale = [None, None]
        self.xlab = None
        self.ylab = None
        self.title = None
        self.add_smooth = False
        self.valid_graph = False

    def has_base(self):
        if self.geom in ['point', 'line']:
            if len(self.data_cols) == 1:
                return True
        elif self.geom in ['histogram', 'bar']:
            if len(self.data_cols) == 2:
                return True
        else:
            return False

    def _make_gg_string(self):
        """Builds string to graph with ggplot package.

        Assembles characteristics in the syntax of the graphic library, in this
        case, ggplot.
        """
        if self.geom in ['point', 'line']:
            plot_string = ("ggplot(self.dataset, aes(self.data_cols[0], "
                           "self.data_cols[1])) + geom_{0}(colour=self.color)"
                           "").format(self.geom)
            if self.add_smooth:
                plot_string += '+ stat_smooth()'
        elif self.geom in ['histogram', 'bar']:
            plot_string = ("ggplot(self.dataset, aes(self.data_cols[0])) "
                           "+ geom_{0}(colour=self.color)").format(self.geom)
        else:
            print('Unsure how to build string.')
        return plot_string

    def make_gg_plot(self):
        """Builds ggplot graph object.

        Uses characteristics to make graph object.
        """
        if self.valid_graph:
            plot = eval(self._make_gg_string())
            print ('Plotting...')
            print plot
        else:
            print("Graph not valid. Try again.")
