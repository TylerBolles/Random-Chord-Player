''' pitchHelper.py is a collection of methods and data related to computing 
	with the pitches on the piano or the 12 pitch classes C, Db, ... Bb, B.'''
import numpy as np
import itertools
import matplotlib.pyplot as plt
import re

def encode_custum_chords(chords):
	''' chords is a list of strings representing chords. new_chords will
		break up alphabetical and symbolic parts of the chord symbol into
		a format other methods can understand, such as the get_triad_chord_tones
		method. '''
	new_chords = []
	for chord in chords:
		symbol = re.findall('\W+', chord)
		# print(symbol)
		if symbol != []:
			s = symbol[0]
		else:
			s = ''
		new_chords += [[re.sub(r'\W+', '', chord), s]]
	return new_chords
	
def get_triad_chord_tones(chord):
	''' converts a triadic chord symbol, i.e., Bb+ into the spelling in root
		position. Bb+ = [10,2,6] '''
	ind = np.argwhere(letters == chord[0])[0][0]
	if chord[1] == '': 
		inds = np.asarray([ind, ind+4, ind+7])
	elif chord[1] == '-':
		inds = np.asarray([ind, ind+3, ind+7])
	elif chord[1] == u'\N{DEGREE SIGN}':
		inds = np.asarray([ind, ind+3, ind+6])
	elif chord[1] == '+':
		inds = np.asarray([ind, ind+4, ind+8])
	inds = inds % 12
	return inds
	
def permutate_all_48_triads_randomly():
	''' generates a random permutation of all 48 triads '''
	chords = []
	for letter in letters:
		for symbol in symbols:
			chords += [[letter,symbol]]
	random_chords = np.random.permutation(chords)
	chord_tones = np.zeros([48,3], dtype = int)
	for i in range(48):
		chord_tones[i, :] = get_triad_chord_tones(random_chords[i])
	return random_chords, chord_tones
	
def generate_random_triads(num_triads):
	''' generates a random permutation of all 48 triads '''
	chords = []
	chord_tones = np.zeros([num_triads,3], dtype = int)
	for i in range(num_triads):
		letter = letters[np.random.randint(12)]
		symbol = symbols[np.random.randint(4)]
		chords +=  [[letter,symbol]]
		chord_tones[i, :] = get_triad_chord_tones(chords[i])
	return chords, chord_tones
	
def get_7th_chords(num_chords = 30, probabilities = [.2, .5, .2, .1]):
	''' generates a random cycle of 4-note dominant functioning chords using
		the family of dominants principle. Chords are given in root position, 
		spelled	with integers 0-11. The probabilities are that of switching	
		families and -- minor 6th's and dominant 7th's. Most musical 
		situations would have high probability of remaining in the same family,
		corresponding to root motion by 4th or 5th. Here the array represents
		the probability of 
		     [going up a m3, staying, going down a m3, going up a tritone].
		Thus get_7th_chords give the trajectory of a is a markov chain on a 
		3d rectangular lattice where the transition probabilities satisfy 
		p(x to y) = 0 for most x, y, unlike the triadic generators and p is 
		translationally invariant, i.e., p(x to y) = p(x+z to y+z) for all z. '''
	chord_tones = np.zeros([num_chords, 4], dtype = int)
	master_arr = np.empty([2, 4, 3], dtype = list) # 7th chords on top, 
						       # m6 chords on bottom
	xyz = np.zeros([num_chords, 3], dtype = int) # multiindex of master_arr
	for i in range(12):
		master_arr[0, int(np.floor(i/3)), i % 3] = [letters[5 * i % 12], '7']
		master_arr[1, int(np.floor(i/3)), i % 3] = [letters[5 * (i + 1) % 12], 'm6']
	random_chords = [['C', '7']] # begin with C7
	chord_tones[0, :] = np.asarray([0, 4, 7, 10])
	for i in range(1, num_chords):
		xyz[i, 0] = np.random.choice(2) # major = 0, minor = 1
		switch_family = np.random.choice([-1, 0, 1, 2], p = probabilities)
		if xyz[i, 0] == 0 and xyz[i-1, 0] == 0: # if staying major
			xyz[i, 2] += [(xyz[i - 1, 2] + 1) % 3] # go dowth a 5th
			xyz[i, 1] = (xyz[i - 1, 1] + switch_family) % 4 # choose a family
		if xyz[i, 0] == 1 and xyz[i-1, 0] == 1: # if staying minor
			xyz[i, 2] = (xyz[i - 1, 2] - 1) % 3 # go down a 4th
			xyz[i, 1] = (xyz[i - 1, 1] + switch_family) % 4 # choose a family
		if xyz[i, 0] != xyz[i-1, 0]:# if change minor to major or major to 
			xyz[i,1:] = xyz[i-1,1:] # minor, do nothing else, so for example,
						# C7 goes to Fm6 and no other minor chord.
		random_chords += [master_arr[tuple(xyz[i, :].T)]]
		ind = np.argwhere(letters == master_arr[tuple(xyz[i, :].T)][0])[0][0]
		if xyz[i, 0] == 0:
			chord_tones[i, :] = np.asarray([ind, ind+4, ind+7, ind+10]) % 12
		elif xyz[i, 0] == 1:
			chord_tones[i, :] = np.asarray([ind, ind+3, ind+7, ind+9]) % 12
	return random_chords, chord_tones
	
def get_distance(next_chord_tones, current_chord_tones):
	''' get_change computes the signed distance to the nearest voicing of the 
		next chord. The distance metric used on the pitch circle is the minimum
		of all distances. The inputs are numerical (0-11) lists of tones of the
		same length.'''
	size_chord = len(current_chord_tones)
	# all possible distances in chord tones which get from current to next chord
	distances = np.zeros([np.math.factorial(size_chord), size_chord], dtype = int)
	for i, voicing in enumerate(list(itertools.permutations(next_chord_tones))):
		distances[i, :] = voicing - current_chord_tones
		distances[i, :] = (distances[i, :] + 6) % 12 - 6 # sends to a range [-tritone, +4th] = [-6,5]
		new_inds2 = (current_chord_tones + distances[i, :]) % 12
	# choose distance with smallest norm
	distance = distances[np.argmin(np.linalg.norm(distances, ord = 1, axis = 1))] 
	return distance	

def get_voiceleading_of_chord_sequence(chord_tones):
	''' chord tones are the array of chords spelled with integers
		0-11 in root position. For example, Bb = [10, 2, 4]. The absolute
		pitches as integers (c0 = 0) of the optimal voioceleading is returned'''
	num_chords, size_chords = chord_tones.shape
	absolute_pitches = np.zeros([num_chords, size_chords], dtype = int)
	# initialize the first voicing as a semi-open voicing around c3
	absolute_pitches[0, :] = chord_tones[0] + 3 * 12
	absolute_pitches[0, 1:2] += 12 # opens the voicing
	for k in range(1, num_chords):
		# the signed distance to the nearest voicing of the next chord. 
		distance = get_distance(chord_tones[k], absolute_pitches[k - 1, :])
		absolute_pitches[k, :] = absolute_pitches[k - 1] + distance
	return absolute_pitches

def plot_music(absolute_pitches):
	''' plots music a la piano roll notation'''
	plt.plot(absolute_pitches, 'o')
	plt.title('Sheet Music', fontsize = 20)
	plt.ylabel('Pitch', fontsize = 18)
	plt.xlabel('Chord number', fontsize = 18)
	plt.ylim([20, 72])
	plt.draw()
	plt.pause(.001)
	
letters = np.asarray(['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A',
                      'Bb', 'B'])
dim_symbol = u'\N{DEGREE SIGN}'
symbols = ['', '-', dim_symbol, '+']

c0 = 16.35 # freqeuency of c0
num_pitches = 7*12 # build all pitchs up to B7
pitches = np.asarray([c0 * 2**(i / 12) for i in range(num_pitches)])
pitch_names = np.empty(num_pitches, dtype = 'U3') # letter names of pitches
for i in range(num_pitches):
    pitch_names[i] = letters[i % 12] + str(int(np.floor(i / 12)))
	
	
