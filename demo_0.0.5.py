#!/usr/bin/python

# Title: Demo of ggspeak
# Author: Maurice Diesendruck
# Last updated: 2015-09-01
#
# Graph by voice.

from ggplot import *
from matplotlib import pyplot as plt
import speech_recognition as sr
import time
import unicodedata
import sys
import pyttsx
import os
from Graphic import Graphic
from Tkinter import Tk
from tkFileDialog import askopenfilename
from copy import copy
import pandas as pd

def main():
	# Give introduction to program and goal.
    introduction()

	# Get recognizer and microphone objects.
    r, mic = prepare_mic()

	# Instantiate empty graph object.
    g_empty = Graphic()

	# Set dataset and filename values of graph object by choosing dataset.
    g_base = choose_dataset(g_empty)
    g = copy(g_base)

	# Run speech recognition and graphing in a streaming format.
    attentive = True
    while attentive:
        with mic as source:
            audio = get_audio(r, source)
            try:
                text = r.recognize(audio)
                print('You said: ' + text)
            except LookupError:
                print("Didn't get audio.")
                continue
            # See if command is quit, reset, save, or edit.
            if text:
                terms = tokenize(text)
                attentive = is_attentive(terms)
                if not attentive:
                    print 'Goodbye'
                    return None
                elif is_reset(terms):
                    g = g_base
                elif is_save(terms):
                    continue
                else:
                    g = update_graph(g, terms)
                    g.make_gg_plot()

def introduction():
	print('\n\n----------- GGSPEAK: Graph by Voice ------------')

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
		r.adjust_for_ambient_noise(source, duration=2)
		r.pause_threshold = 1.5
	return r, m

def choose_dataset(g):
	print 'Type file name.'
	filename = os.getcwd()+'/'+raw_input('Filename: '+os.getcwd()+'/')
	try:
		dataset = pd.read_csv(filename)
	except LookupError:
		print("No document found.")

	# Set dataset as the chosen file.
	g.dataset = dataset
	g.filename = filename

	names = '[' + ', '.join(list(g.dataset.columns.values)) + ']'
	names = names.upper()
	print('\nYou are using the dataset ' + g.filename)
	print('Data preview:')
	print(g.dataset.head(5))
	print

	return g

def get_audio(r, source):
	print "\n Listening..."
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

def is_reset(terms):
	reset = False
	reset_words = ['reset']
	wants_to_reset = bool(set(reset_words) & set(terms))
	if wants_to_reset:
		reset = True
	return reset

def is_save(terms):
	save = False
	save_words = ['save']
	wants_to_save = bool(set(save_words) & set(terms))
	if wants_to_save:
		save = True
	return save

def is_valid_plot(g):
	if g.geom == None:
		print("No geometry found.")
	elif g.geom in ['point', 'line']:
		if all([len(g.data_cols) == 2,
		       g.dataset[g.data_cols[0]].dtype in ['float64', 'int64'],
		       g.dataset[g.data_cols[1]].dtype in ['float64', 'int64']]):
			g.valid_graph = True
	elif g.geom in ['histogram', 'bar']:
		if len(g.data_cols) == 1:
			g.valid_graph = True
	summarize_graph(g)
	return g

def summarize_graph(g):
	print(' - Summary - ')
	print('Dataset: '+g.filename)
	print('Geom: '+g.geom)
	print('Datacols: '+str(g.data_cols))
	if len(g.data_cols) >=1:
		print('type data 0: '+str(g.dataset[g.data_cols[0]].dtype))
	if len(g.data_cols) >=2:
		print('type data 1: '+str(g.dataset[g.data_cols[1]].dtype))
	print('Valid status: '+str(g.valid_graph))

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
	elif 'point' in terms or 'scatter' in terms:
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
	g = is_valid_plot(g)

	return g

if __name__ == "__main__":
	main()



