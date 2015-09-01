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
import os
from Graphic import Graphic
from Tkinter import Tk
from tkFileDialog import askopenfilename
import pandas as pd

def main():
	# Give introduction to program and goal.
	introduction()

	# Get recognizer and microphone objects.
	r, mic = prepare_mic()

	# Instantiate empty graph object.
	g = Graphic()

	# Set dataset and filename values of graph object by choosing dataset.
	g = choose_dataset(g)

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
	print('Graph by voice.')
	time.sleep(2)

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

def choose_dataset(g):
	print 'First choose file.'
	filename = os.getcwd()+'/'+raw_input('Filename: '+os.getcwd()+'/')
	dataset = pd.read_csv(filename)

	# Set dataset as the chosen file.
	g.dataset = dataset
	g.filename = filename

	# Select only numerical columns.	
	# Specific to diamonds.
	names = '[' + ', '.join(list(g.dataset.columns.values)) + ']'
	names = names.upper()
	print('\nYou are using the dataset ' + g.filename)
	print('Data preview:')
	print(g.dataset.head(5))
	print
	time.sleep(3)

	return g

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

def extract_data_cols(g, terms):
	try:
		g.data_cols = [t for t in terms if t in g.dataset.columns.values]
		print('Relevant variables: ' + str(g.data_cols))
	except:
		print('Did not catch any matching variable names.')
	return g

def extract_geom(g, terms):
	if 'histogram' in terms:
		g.geom = 'histogram'
	elif 'bar' in terms or 'barplot' in terms:
		g.geom = 'bar'
	elif 'density' in terms:
		g.geom = 'density'
	elif 'line' in terms:
		g.geom = 'line'
	elif 'point' in terms:
		g.geom = 'point'
	elif len(g.data_cols) == 1:
		g.geom = 'histogram'
	elif len(g.data_cols) == 2:
		g.geom = 'point'
	else:
		print("Couldn't identify geometry of graph.")
	return g

def extract_stat_functions(g, terms):
	if 'smooth' in terms:
		g.add_smooth = True
	return g

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
	# Search the command for instructions about specific graph attributes.
	g = extract_data_cols(g, terms)
	g = extract_geom(g, terms)
	g = extract_stat_functions(g, terms)
	
	# Handle misunderstandings.
	# TODO: Do this with phonetic/edit distance.
	p = g.make_gg_plot()
	print p
	
if __name__ == "__main__":
	main()


	