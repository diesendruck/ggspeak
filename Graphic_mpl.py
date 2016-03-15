#!/usr/bin/python

# Title: Graphic Object Class Definition
# Author: Maurice Diesendruck
# Last updated: 2015-09-01
#
# Class for general graph object.
#
# Note: Changed ggplot source code. See link: http://bit.ly/1UkFZCO

from matplotlib import pyplot as plt
plt.style.use('ggplot')
plt.ion()


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
        self.data_cols = []
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

    def make_gg_plot(self):
        """Builds graph with matplotlib.

        Assembles characteristics in the syntax of the graphic library.
        """
        if self.geom in ['point']:
            print 'Plot scatter plot'
        elif self.geom in ['histogram']:
            plt.hist(self.dataset[self.data_cols[0]], normed=1, alpha=0.5)
            plt.xlabel(self.data_cols[0])
        else:
            print('Unsure how to build plot.')
        return None

    def is_valid_graph(self):
        if self.geom is None:
            self.valid_graph = False
        elif self.geom in ['point', 'line']:
            if all([len(self.data_cols) == 2,
                    self.dataset[self.data_cols[0]].dtype in ['float64',
                                                              'int64'],
                    self.dataset[self.data_cols[1]].dtype in ['float64',
                                                              'int64']]):
                self.valid_graph = True
        elif self.geom in ['histogram', 'bar']:
            if len(self.data_cols) == 1:
                self.valid_graph = True
        return self.valid_graph

    def summarize(self):
        print(' - Summary - ')
        print('Dataset: '+self.filename)
        print('Geom: '+str(self.geom))
        print('Datacols: '+str(self.data_cols))
        if len(self.data_cols) == 1:
            print('Type data 0: '+str(self.dataset[self.data_cols[0]].dtype))
        if len(self.data_cols) == 2:
            print('Type data 1: '+str(self.dataset[self.data_cols[1]].dtype))
        print('Valid status: '+str(self.is_valid_graph()))
        return self
