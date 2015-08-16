#!/usr/bin/python

# Title: Demo of ggspeak
# Author: Maurice Diesendruck
# Last updated: 2015-08-15
#
# Graph by voice.

from ggplot import *
import speech_recognition as sr
import time
import unicodedata
import sys
import pyttsx
from Graphic import Graphic

def main():
	# Give introduction to program and goal.
	introduction()

	# Get recognizer and microphone objects.
	r, mic = prepare_mic()

	# Instantiate empty graph object.
	g = Graphic()

	# Give orientation on data set.
	introduce_dataset(g)

	# Run speech recognition and graphing in a streaming format.
	attentive = True
	while attentive:	
		with mic as source:	
			audio = get_audio(r, source)
			
			try:
				text = r.recognize(audio)
				print('You said: ' + text)
				terms = tokenize(text)
				attentive = is_attentive(terms)
				if not attentive:
					print 'Goodbye'
					return None
				update_graph(g, terms)
			except LookupError:
				print 'could not understand audio'				

def introduction():
	print('\n\n----------- DEMO ------------')
	print('Graph a dataset using your voice.')
	print('e.g. "Give me a plot of _____ versus _____"')

def prepare_mic():
	"""Instantiates recognizer and microphone objects.

	These objects come from the speech_recognition package.

	Args:
		NA

	Returns:
		r: A recognizer object.
		m: A microphone object.
	"""

	r = sr.Recognizer()
	m = sr.Microphone()
	with m as source:
		r.adjust_for_ambient_noise(source)
	return r, m	

def introduce_dataset(g):
	dataset = eval(g.dataset)

	# Select only numerical columns.	
	# Specific to diamonds.
	dataset = dataset[['carat', 'depth', 'table', 'price', 'x', 'y', 'z']]
	names = '[' + ', '.join(list(dataset.columns.values)) + ']'
	names = names.upper()
	print('\nYou are using the dataset ' + g.dataset.upper())
	print('\nAvailable variables:')
	print(names)
	print
	time.sleep(3)

def get_audio(r, source):
	print "Listening..."
	audio = r.listen(source)
	return audio

def tokenize(text):
	text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
	text = text.lower()
	terms = text.split(' ')
	return terms

def is_attentive(terms):
	attentive = True
	quit_words = [
		'quit', 'stop', 'done', 'finish', 'finished', 'end', 'enough']
	wants_to_quit = bool(set(quit_words) & set(terms))
	if wants_to_quit:
		attentive = False
	return attentive

def update_graph(g, terms):
	"""Receives text data, and updates graph string.

	Pulls relevant instructions from terms, updates Graphic object with
	new values, and plots Graphic.

	Args:
		g: Graphic object.
		terms: Tokens from latest voice command.

	Returns:
		NA
	"""
	# Handle misunderstandings.
	# TODO: Do this with phonetic/edit distance.
	carat_mis = ['carrot', 'karat', 'current', 'parrot', 'ferret']
	depth_mis = ['death', 'def']
	price_mis = ['press']
	x_mis = ['ex']
	y_mis = ['why']
	terms = ['carat' if i in carat_mis else i for i in terms]
	terms = ['depth' if i in depth_mis else i for i in terms]
	terms = ['price' if i in price_mis else i for i in terms]
	terms = ['x' if i in x_mis else i for i in terms]
	terms = ['y' if i in y_mis else i for i in terms]

	# Extract variables.
	dataset = eval(g.dataset)
	plot_framework = ['plot', 'versus', 'vs']
	try:
		x, y = [t for t in terms if t in dataset.columns.values]
	except:
		print('Did not catch two variables.')
		return None

	# Print variables and plot graph.
	print('  x = ' + x)
	print('  y = ' + y)

	g.xvar = x
	g.yvar = y

	p = g.make_gg_plot()
	print p
	
if __name__ == "__main__":
	main()


	