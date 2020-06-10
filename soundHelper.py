# -*- coding: utf-8 -*-
''' soundHelper.py is a library of methods to use with PlayRandomChords.py'''
import numpy as np
import time
import pyo as pyo
from pitchHelper import *

def my_overtone_synth(fundemental_freq):
	''' plays the decaying overtone series of the fundemental freqeuncy'''
	num_overtones = 10
	amps = [1/n for n in range(1, num_overtones)] 
	freqs = [fundemental_freq * n for n in range(1, num_overtones)]
	signal = []
	for n in range(num_overtones - 1):
		b = pyo.Sine([freqs[n]], mul = amps[n])
		signal += [pyo.Pan(b, outs=2, pan=.5).out()] # panning to both sides
	return signal

def arppeggiate1(freqs, wait_time):
	''' plays the arppeggio of the given chord by cycling through the provided 
		frequencies, freqs, once. wait_time is the time between each note.'''
	audio = []
	for freq in freqs:
		audio = my_overtone_synth(freq) 
		time.sleep(wait_time)
	return audio

def arppeggiate2(freqs, wait_time, max_time):
	''' plays the arppeggio of the given chord by repeatedly cycling through
`		the provided freqeuncies, freqs. wait_time is the time between each
		note while max_time is the maximum time of arppeggiation. '''
	audio = []
	total_time = 0
	i = 0
	while(total_time < max_time):
		audio = my_overtone_synth(freqs[i % len(freqs)]) 
		time.sleep(wait_time)
		i += 1
		total_time += wait_time
	return audio
 
def play_chords(chords, absolute_pitches, num_chords_to_play = 1,
				time_per_chord = 2, arppeggiate = True):  
	''' playes chords. absolute_pitches are integer representations of pitch.'''
	plot_music(absolute_pitches[:num_chords_to_play]) # visualization
	# pyo initializations
	s = pyo.Server()
	s.boot()
	s.amp = .1
	s.start()
	for k in range(num_chords_to_play):
		freqs = pitches[absolute_pitches[k]]                          
		freqs = np.hstack([freqs])				   
		print(chords[k][0]+chords[k][1], end = '\t')
		print(pitch_names[absolute_pitches[k]]) # optional
		# build audio signal
		if arppeggiate:
			audio = arppeggiate2(freqs, time_per_chord / 8, time_per_chord)
			audio = None
		else:
			audio = []
			for freq in freqs:
				audio += [my_overtone_synth(freq)] 
			time.sleep(time_per_chord)
		if (k+1) % 4 == 0: print() # for ease of reading
	s.stop()
	s.shutdown()
	plt.close() # closes visualization