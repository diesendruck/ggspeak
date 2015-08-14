# Title: Demo of ggspeak
# Author: Maurice Diesendruck
# Last updated: 2015-08-14
#
# Use speech recognition to graph.

from ggplot import *
import speech_recognition as sr
import time
import unicodedata

# Select only numerical columns.
diamonds = diamonds[['carat', 'depth', 'table', 'price', 'x', 'y', 'z']]

# Set up prompt.
print('\n\n ----------- DEMO ------------ ')
print('\n  Here are your available variables  ')
print(' [' + ', '.join(list(diamonds.columns.values)) + ']')
time.sleep(3)
print('\n\n  What do you want to plot?  ')

# Ask for command.
r = sr.Recognizer()
with sr.Microphone() as source:
  r.adjust_for_ambient_noise(source)
  audio = r.listen(source)
try:
  print('  You said: ' + r.recognize(audio))
except LookupError:
  print('  could not understand audio')

# Reformat command.
said = r.recognize(audio)
said = unicodedata.normalize('NFKD', said).encode('ascii', 'ignore')
said = said.lower()
terms = said.split(' ')

# Handle misunderstandings.
carat_mis = ['carrot', 'karat', 'current', 'parrot']
terms = ['carat' if i in carat_mis else i for i in terms]

# Extract variables.
plot_framework = ['plot', 'versus', 'vs']
x, y = [t for t in terms if t in diamonds.columns.values]

# Print variables and plot graph.
print('  x = ' + x)
print('  y = ' + y)
p = ggplot(diamonds, aes(x, y)) + geom_point(colour='steelblue')
print p 
