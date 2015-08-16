#!/usr/bin/python

# Title: Graphic Object Class Definition
# Author: Maurice Diesendruck
# Last updated: 2015-08-15
#
# Class for general graph object.

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
		self.dataset = 'diamonds'
		self.filename = None
		self.xvar = None
		self.yvar = None
		self.geom = 'point'
		self.color = 'steelblue'
		self.xscale = [None, None]
		self.yscale = [None, None]
		self.xlab = None
		self.ylab = None
		self.title = None

	def make_gg_string(self):
		"""Builds string to graph with ggplot package.

		Assembles characteristics in the syntax of the graphic library, in this
		case, ggplot.
		"""
		plot_string = 'ggplot({0}, aes("{1}", "{2}")) + '.format(
			self.dataset, self.xvar, self.yvar)
		plot_string += 'geom_{0}(colour="{1}")'.format(self.geom, self.color)

		return plot_string
		
	def make_gg_plot(self):
		"""Builds ggplot graph object.

		Uses characteristics to make graph object.
		"""
		plot = eval(self.make_gg_string())
		return plot



	