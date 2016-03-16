#!/usr/bin/python

# Title: Graphic Object Class Definition
# Author: Maurice Diesendruck
# Last updated: 2015-09-01
#
# Class for general graph object.
#
# Note: Changed ggplot source code. See link: http://bit.ly/1UkFZCO

import numpy as np
from copy import copy
from collections import Counter
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
        self.grouping = None
        self.geom = None
        self.color = 'steelblue'
        self.xscale = [None, None]
        self.yscale = [None, None]
        self.xlab = None
        self.ylab = None
        self.title = None
        self.base = False
        self.add_smooth = False
        self.valid_graph = False

    def has_base(self):
        if self.geom in ['point', 'line']:
            if len(self.data_cols) == 2:
                self.base = True
                return True
        elif self.geom in ['hist', 'bar']:
            if len(self.data_cols) == 1:
                self.base = True
                return True
        else:
            self.base = False
            return False

    def make_gg_plot(self):
        """Builds graph with matplotlib.

        Assembles characteristics in the syntax of the graphic library.
        """
        # Make a scatter plot.
        if self.geom in ['point']:
            d1_name = str(self.data_cols[0])
            d2_name = str(self.data_cols[1])
            d1 = self.dataset[d1_name]
            d2 = self.dataset[d2_name]

            plt.xlabel(d1_name)
            plt.ylabel(d2_name)
            plt.title('Scatter plot of {} and {}'.format(d1_name, d2_name))

            # Make grouped plot, if necessary.
            if self.grouping is None:
                plt.scatter(d1, d2, alpha=0.5)
            else:
                d_temp = copy(self.dataset)
                grouping_name = self.grouping
                grouping_type = d_temp[grouping_name].dtype
                if grouping_type not in ['float64', 'int64']:
                    categories = np.unique(d_temp[grouping_name])
                    colors = np.linspace(0, 1, len(categories))
                    colordict = dict(zip(categories, colors))

                    d_temp['CategoryColor'] = d_temp[grouping_name].apply(
                        lambda x: colordict[x])
                    plt.scatter(d1, d2, c=d_temp.CategoryColor)

        # Make a histogram or bar chart.
        elif self.geom in ['hist', 'bar']:

            d_name = str(self.data_cols[0])
            d = self.dataset[d_name]
            d_type = d.dtype

            # If geom is hist and data is numeric, make a histogram.
            if (self.geom == 'hist' and d_type in ['float64', 'int64']):
                plt.hist(d, alpha=0.5)
                plt.xlabel(d_name)
                plt.ylabel('Count')
                plt.title('Histogram of '+d_name)
            else:
                # If geom is bar or data is categorical, make a bar chart.
                freqs = Counter(d)
                f = sorted(freqs.items(), key=lambda (k, v): -v)
                names = [i for (i, j) in f]
                counts = [j for (i, j) in f]
                positions = np.arange(len(f))
                plt.bar(positions, counts, align='center', alpha=0.5)
                plt.xticks(positions, names)
                plt.xlabel(d_name)
                plt.ylabel('Count')
                plt.title('Bar chart of '+d_name)

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
            else:
                print 'Cannot plot if a variable is not numeric.'
        elif self.geom in ['hist', 'bar']:
            if len(self.data_cols) == 1:
                d_name = str(self.data_cols[0])
                d = self.dataset[d_name]
                d_type = d.dtype
                if not (self.geom == 'hist' and d_type not in ['float64',
                                                               'int64']):
                    self.valid_graph = True
                else:
                    print 'Cannot make histogram from categorical variable.'
        else:
            self.valid_graph = False

        return self.valid_graph

    def summarize(self):
        print ' - Summary - '
        print 'Dataset: {}'.format(self.filename)
        print 'Geom: {}'.format(str(self.geom))
        print 'Datacols: {}'.format(str(self.data_cols))
        print 'Grouping: {}'.format(str(self.grouping))
        if len(self.data_cols) == 1:
            print('Type data 0: '+str(self.dataset[self.data_cols[0]].dtype))
        if len(self.data_cols) == 2:
            print('Type data 0: '+str(self.dataset[self.data_cols[0]].dtype))
            print('Type data 1: '+str(self.dataset[self.data_cols[1]].dtype))
        print 'Valid status: {}'.format(str(self.is_valid_graph()))
        return self
