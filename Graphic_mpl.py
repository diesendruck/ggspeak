#!/usr/bin/python

# Title: Graphic Object Class Definition
# Author: Maurice Diesendruck
# Last updated: 2015-09-01
#
# Class for general graph object.
#
# Note: Changed ggplot source code. See link: http://bit.ly/1UkFZCO

import numpy as np
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
import matplotlib.colors as mplcolors
import matplotlib.cm as cmx
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

    def make_gg_plot(self):
        """Builds graph with matplotlib.

        Assembles characteristics in the syntax of the graphic library.
        """
        print self.summarize()

        # Make a scatter plot.
        if self.geom in ['point']:
            # Make some data shortcuts.
            d1_name = str(self.data_cols[0])
            d2_name = str(self.data_cols[1])
            d1 = self.dataset[d1_name]
            d2 = self.dataset[d2_name]
            # Prepare figure.
            plt.xlabel(d1_name)
            plt.ylabel(d2_name)
            plt.title('{} vs {}'.format(d1_name, d2_name))

            # Make regular scatterplot, if no grouping is defined.
            if self.grouping is None:
                plt.scatter(d1, d2, edgecolors='none', alpha=0.5)

            # Make grouped scatterplot, if grouping is defined.
            else:
                d = self.dataset
                grouping_name = self.grouping
                print 'Grouping name: {}'.format(grouping_name)
                try:
                    group_example = d[grouping_name][0]
                except:
                    print 'Group example caused problems. Try again.'
                    print d[grouping_name].head(3)
                    print grouping_name
                    return None

                # Categorical grouping.
                if not isinstance(group_example, (int, long, float)):
                    cat_vals = np.unique(d[grouping_name])
                    # Prepare color coding.
                    cmap = plt.get_cmap('Paired')
                    colors = mplcolors.Normalize(vmin=0, vmax=len(cat_vals))
                    colors = cmx.ScalarMappable(norm=colors, cmap=cmap)
                    for i in range(len(cat_vals)):
                        category_indices = (d[grouping_name] == cat_vals[i])
                        plt.scatter(d[d1_name][category_indices],
                                    d[d2_name][category_indices],
                                    c=colors.to_rgba(i), label=cat_vals[i],
                                    marker='o', edgecolors='none')
                    plt.legend()

                # Numerical grouping.
                else:
                    # Color using colorbar.
                    cmap = plt.get_cmap('YlGnBu')
                    p = plt.scatter(d[d1_name], d[d2_name], c=d[grouping_name],
                                    cmap=cmap, marker='o', edgecolors='none',
                                    vmin=min(d[grouping_name]),
                                    vmax=max(d[grouping_name]))
                    cb = plt.colorbar(p)
                    cb.set_label(grouping_name)

        # Make a histogram or bar chart.
        elif self.geom in ['hist', 'bar']:

            d = self.dataset
            d_name = str(self.data_cols[0])
            d_var_example = d[d_name][0]
            plt.xlabel(d_name)
            plt.ylabel('Count')
            plt.title('Distribution of {}'.format(d_name))

            # Make a histogram, if geom is hist and data is numeric.
            if (self.geom == 'hist' and isinstance(d_var_example, (int, long,
                                                                   float))):

                # Make regular histogram, if no grouping.
                if self.grouping is None:
                    pl = d[d_name].hist(alpha=0.5)
                    pl.set_xlabel(d_name)
                    pl.set_ylabel('Count')
                    pl.set_title('Distribution of {}'.format(d_name))
                # Make grouped histogram, if has grouping.
                else:
                    pl_list = d[d_name].hist(by=d[self.grouping], alpha=0.5)
                    pl_list = pl_list.ravel()
                    for hist in range(len(pl_list)):
                        pl_list[hist].set_xlabel(d_name)
                        pl_list[hist].set_ylabel('Count')

            # Make a bar chart, if geom is bar or data is categorical.
            else:

                # Make regular bar chart, if no grouping.
                if self.grouping is None:
                    freqs = Counter(d[d_name])
                    f = sorted(freqs.items(), key=lambda (k, v): -v)
                    names = [i for (i, j) in f]
                    counts = [j for (i, j) in f]
                    positions = np.arange(len(f))
                    plt.bar(positions, counts, align='center', alpha=0.5)
                    plt.xticks(positions, names)

                # Make grouped bar chart, if has grouping.
                else:
                    grouping_name = self.grouping
                    try:
                        group_example = d[grouping_name][0]
                    except:
                        print 'Group example caused problems. Try again.'
                        return None

                    # Categorical grouping.
                    if not isinstance(group_example, (int, long, float)):
                        ct = pd.crosstab(index=d[d_name],
                                         columns=d[self.grouping])
                        pl = ct.plot.bar()
                        pl.set_xlabel(d_name)
                        pl.set_ylabel('Count')
                    else:
                        print 'Not sure how to group by numeric vars.'

        else:
            print('Not yet sure how to build this plot.')

        return None

    def is_valid_graph(self):
        if self.geom is None:
            self.valid_graph = False
        elif self.geom in ['point', 'line']:
            try:
                if all([len(self.data_cols) == 2,
                        self.dataset[self.data_cols[0]].dtype in ['float64',
                                                                  'int64'],
                        self.dataset[self.data_cols[1]].dtype in ['float64',
                                                                  'int64']]):
                    self.valid_graph = True
                else:
                    print 'Cannot plot if a variable is not numeric.'
            except:
                print 'Cannot identify data_cols.'
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
