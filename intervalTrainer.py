import numpy as np
from pitchHelper import *
from soundHelper import *

ind1 = np.argwhere(pitch_names == 'G3')[0][0]
intervals = ['m2nd', 'M2nd', 'm3rd', 'M3rd', 'P4th', 'tritone', 'P5th', 'm6th', 
             'M6th', 'm7th', 'M7th', '8ve', 'm9th', 'M9th']
direction = ['up', 'down']            
s = pyo.Server()
s.boot()
s.amp = .1
s.start()

usr_input = 'n'
print('\n')
print('------ Interval Ear Training ------ ')
print('Press n to go on to the next interval, q to quit', '\n')
while usr_input == 'n':
    pitch1_as_int = np.random.randint(12)+ind1
    pitch1 = pitches[pitch1_as_int]
    interval_as_int = np.random.randint(len(intervals)) + 1
    
    audio = my_overtone_synth(pitch1)
    direction = np.random.randint(2)
    if direction == 0:
        print(pitch_names[pitch1_as_int], intervals[interval_as_int - 1], ' ', 'Up')
        usr_input = input()
        pitch2_as_int = pitch1_as_int + interval_as_int
    else:
        print(pitch_names[pitch1_as_int], intervals[interval_as_int - 1], ' ', 'Down')
        usr_input = input()
        pitch2_as_int = pitch1_as_int - interval_as_int
    if usr_input == 'q':
        break
    audio = my_overtone_synth(pitches[pitch2_as_int])
    time.sleep(1)
s.stop()
s.shutdown()