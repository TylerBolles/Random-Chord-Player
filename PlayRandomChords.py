''' PlayRandomChords use the pyo module to play randomly generated chords. 
	Currently 3 types of random generation are usable: a random permutation
	all 48 triads, a random sequence of traids of any length and a random 
	chain of dominant functioning chords.  '''
import numpy as np
from pitchHelper import *
from soundHelper import *


# play all triads in random order 
random_chords, chord_tones = permutate_all_48_triads_randomly()
absolute_pitches = get_voiceleading_of_chord_sequence(chord_tones)
play_chords(random_chords, absolute_pitches, num_chords_to_play = 48,
			time_per_chord = 1, arppeggiate = True) 

# play any random triads
num_chords = 10
random_chords, chord_tones = generate_random_triads(num_chords)
absolute_pitches = get_voiceleading_of_chord_sequence(chord_tones)
play_chords(random_chords, absolute_pitches,  num_chords, 0.5, False)

# play a random chain of dominant chords			
num_chords = 10
random_chords, chord_tones = get_7th_chords(num_chords = num_chords)
absolute_pitches = get_voiceleading_of_chord_sequence(chord_tones)
play_chords(random_chords, absolute_pitches, num_chords, 1, True)

# play custom list of chords
chords = ['D', 'D-', 'A', 'A' + dim_symbol, 'B-', 'E', 'A-'] # use only flat accidentals
chords = encode_custum_chords(chords)
chord_tones = np.zeros([len(chords), 3], dtype = int)
for i, chord in enumerate(chords):
	chord_tones[i, :] = get_triad_chord_tones(chord)
absolute_pitches = get_voiceleading_of_chord_sequence(chord_tones)
play_chords(chords, absolute_pitches, len(chords), 1, True)

	











