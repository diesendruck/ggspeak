#!/usr/bin/python

# Title: Demo of ggspeak
# Author: Maurice Diesendruck
# Last updated: 2015-09-01
#
# Graph by voice.

import speech_recognition as sr
import unicodedata
import os
import pandas as pd
from copy import copy
from Graphic_mpl import Graphic
from jellyfish import levenshtein_distance as ld
from nltk.corpus import stopwords as sw
from matplotlib import pyplot as plt
plt.style.use('ggplot')
plt.ion()


def main():
    # Give introduction to program and goal.
    introduction()

    # Get recognizer and microphone objects.
    r, mic = prepare_mic()

    # Instantiate empty graph object.
    g_empty = Graphic()

    # Set dataset and filename values of graph object by choosing dataset.
    g_data_only = choose_dataset(g_empty)
    g = copy(g_data_only)

    # Run speech recognition and graphing in a streaming format.
    while 1:
        raw_input('Tap ENTER to continue.')
        with mic as source:
            audio = get_audio(r, source)
            try:
                text = r.recognize(audio)
                print('You said: ' + text)
            except LookupError:
                print("Didn't get audio.")
                continue
            # See if command is quit, save, reset, or edit.
            if text:
                terms = tokenize(text)

                # Decide what the terms indicate, and do the actions.
                if is_quit(terms):
                    print 'Goodbye'
                    return None
                elif is_save(terms):
                    # TODO: Write save function.
                    continue
                elif is_reset(terms):
                    plt.clf()
                    g = copy(g_data_only)
                    data_preview(g)
                    print 'DEFINE a new graph.'
                elif is_summary(terms):
                    data_preview(g)
                    g.summarize()
                elif g.has_base():
                    g = update_graph(g, terms)
                    g = graph_if_valid(g, g_data_only)
                else:
                    g = create_graph(g, terms)
                    g = graph_if_valid(g, g_data_only)


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
        r.pause_threshold = 0.5
    return r, m


def choose_dataset(g):
    valid_file = False
    while not valid_file:
        try:
            print 'Type file name.'
            filename = os.getcwd()+'/'+raw_input('Filename: '+os.getcwd()+'/')
            dataset = pd.read_csv(filename)
            dataset.columns = [w.lower() for w in dataset.columns]
            valid_file = True

            # Set dataset as the chosen file.
            g.dataset = dataset
            g.filename = filename

            names = '[' + ', '.join(list(g.dataset.columns.values)) + ']'
            names = names.upper()
            print('\nYou are using the dataset ' + g.filename)
            data_preview(g)

        except Exception, e:
            print e
            print("No document found.")

    return g


def data_preview(g):
    print('Data preview:')
    print(g.dataset.head(5))


def get_audio(r, source):
    print "\n Listening..."
    audio = r.listen(source)
    return audio


def tokenize(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    text = text.lower()
    terms = text.split(' ')
    terms = [t for t in terms if t not in sw.words('english')]
    return terms


def is_quit(terms):
    quit_words = ['quit', 'stop', 'done', 'finish', 'finished', 'end', 'enough',
                  'exit', 'goodbye', 'close']
    wants_to_quit = bool(set(quit_words) & set(terms))
    return wants_to_quit


def is_summary(terms):
    summary_words = ['summary', 'summarize', 'describe', 'description']
    wants_summary = bool(set(summary_words) & set(terms))
    return wants_summary


def is_reset(terms):
    reset_words = ['reset', 'clear', 'new']
    wants_to_reset = bool(set(reset_words) & set(terms))
    return wants_to_reset


def is_save(terms):
    save_words = ['save']
    wants_to_save = bool(set(save_words) & set(terms))
    return wants_to_save


def create_graph(g, terms):
    """With terms, extracts basic graph elements.

    Gets data columns and geometry of graph.

    Args:
        g: Graphic object.
        terms: Terms from latest voice command.

    Returns:
        g: Graphic object.
    """
    # Search the command for instructions about specific graph attributes.
    g = extract_data_cols(g, terms)
    g = extract_geom(g, terms)
    return g


def update_graph(g, terms):
    """With terms, edits ancillary graph features, like titles and labels.

    Determines ancillary features, like titles, labels, smoothing functions,
    groupings, stackings, etc.

    Args:
        g: Graphic object.
        terms: Tokens from latest voice command.

    Returns:
        g: Graphic object.
    """
    if g.geom == 'point':
        g = extract_stat_functions(g, terms)
    g = extract_grouping(g, terms)
    plt.clf()
    return g


def graph_if_valid(g, g_data_only):
    # Graph the plot if it's valid, otherwise summarize.
    if g.is_valid_graph():
        g.make_gg_plot()
    else:
        print 'INVALID graph.'
        g.summarize()
        print 'Reseting graph.'
        g = copy(g_data_only)
    return g


def extract_data_cols(g, terms):
    # Get first data cols.
    if not g.has_base():
        try:
            targets = g.dataset.columns.values
            g.data_cols = [t for t in terms if t in targets]
            # Get fuzzy match for column names, respecting homophones.
            # g.data_cols = homophone_matches(terms, g.dataset.columns.values)
            print('Relevant variables: ' + str(g.data_cols))
        except:
            print('Did not catch any matching variable names.')

    # Already has base, so find grouping variables.
    else:
        try:
            targets = g.dataset.columns.values
            g.grouping = [t.lower() for t in terms if t in targets]
            # Take only last matching name.
            g.grouping = str(g.grouping[-1])
            # Get fuzzy match for column names, respecting homophones.
            # g.data_cols = homophone_matches(terms, g.dataset.columns.values)
            print('Relevant variables: ' + g.grouping)
        except:
            print('Did not catch any matching variable names.')
    return g


def homophone_matches(terms, targets):
    # Given two lists, return intersection (with lenience for homophones).
    excluded_words = ['vs']
    targets = [t for t in targets if t not in excluded_words]
    orig_targets = targets
    terms = map(unicode, terms)
    targets = map(unicode, targets)
    matches = []
    for i in range(len(terms)):
        for j in range(len(targets)):
            if ld(terms[i], targets[j]) <= 1:
                matches.append(orig_targets[j])
    return matches


def extract_geom(g, terms):
    # Simple keyword detection.
    if 'histogram' in terms:
        g.geom = 'hist'
    elif 'density' in terms:
        g.geom = 'density'
    elif 'line' in terms:
        g.geom = 'line'
    elif 'bar' in terms or 'barplot' in terms:
        g.geom = 'bar'
    elif 'point' in terms or 'scatter' in terms:
        g.geom = 'point'
    else:
        g = infer_geom(g, terms)
    return g


def infer_geom(g, terms):
    # Infer based on number of data columns and their types.
    if len(g.data_cols) == 1:
        print('Inferring graph geometry.')
        d_example = g.dataset[g.data_cols[0]][0]
        if is_numeric(d_example):
            g.geom = 'hist'
        else:
            g.geom = 'bar'
    elif len(g.data_cols) == 2:
        print('Inferring graph geometry.')
        d1_name = g.data_cols[0]
        d2_name = g.data_cols[1]
        d1_example = g.dataset[d1_name][0]
        d2_example = g.dataset[d2_name][0]
        # Case of both numeric.
        if is_numeric(d1_example) and is_numeric(d2_example):
            g.geom = 'point'
        # Case where one is numeric.
        elif is_numeric(d1_example) or is_numeric(d2_example):
            g.geom = 'hist'
            if is_numeric(d1_example):
                g.data_cols = [d1_name]
                g.grouping = d2_name
            else:
                g.data_cols = [d2_name]
                g.grouping = d1_name
        # Case where both are categorical.
        else:
            g.geom = 'bar'
            g.data_cols = [d1_name]
            g.grouping = d2_name

    else:
        print("Couldn't identify geometry of graph.")
    return g


def is_numeric(v):
    return isinstance(v, (int, long, float))


def extract_stat_functions(g, terms):
    if 'smooth' in terms:
        g.add_smooth = True
    return g


def extract_grouping(g, terms):
    bi = bigrams(terms)
    if any([['group', 'by'] in bi, ['group', 'x'] in bi,
            ['color', 'by'] in bi, ['color', 'x']]):
        extract_data_cols(g, terms)
    return g


def bigrams(terms):
    bigrams = [[terms[i], terms[i+1]] for i in range(len(terms)-1)]
    return bigrams


if __name__ == "__main__":
    main()
