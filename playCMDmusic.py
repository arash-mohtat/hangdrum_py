""" This script plays the hang drum based on the sequence of notes entered by the user
in the command line. The notes are recorded from a hang drum in the D minor scale.
The allowable notes are: N0, N1, N2, N3, N4, N5, N6, N7, N8, S, G which stand for 
the zeroth note (the ding: lower octave D) and 1 to 8 correspond to A, B, C, D 
(one octave higher than the Ding), E, F, G, and A. S and G stand for slap (when the
handpan is not hit on any specific note but on the side wall) and ghost notes.
The notes should be seperated by commas with the entire sequence enclosed in [].

Here is an example of how the script can be called:
>> python playCMDmusic.py [N1, N2, N3, N4, N5, N6, N7]*2 160
which will play A to G twice (*2) at a tempo of 160. The default tempo is 200 if
the 2nd commandline argument is not specified.
Another more melodic example:
>> python playCMDmusic.py [N0,N2,N7,N6,N0,N4,N5,N6,N0,N2+N4,G,N0,S,N1,G,N4]*3
Notice how you can have the script play a chord using summation, e.g. N2+N4!

Dependencies: numpy, simpleaudio and soundfile

Arash Mohtat
May 1st, 2020
"""

import sys
import numpy as np
import simpleaudio as sa
import soundfile as sf

def sa_play(data,fs=44100, normalize=False): 
    """ plays the audio data, i.e. a numpy array of shape (N,2), on the
    audio device and waits for the playback to finish. If the audio data
    has a single channel, that channel is duplicated on right and left."""
    
    if len(data.shape)==1:
        data = np.column_stack((data,data))
    
    # Ensure that highest value is in 16-bit range
    if normalize:
        audio = np.empty_like(data)
        audio[:,0] = data[:,0] * (2**15 - 1) / np.max(np.abs(data[:,0]))
        audio[:,1] = data[:,1] * (2**15 - 1) / np.max(np.abs(data[:,1]))
    else:
        audio = data * (2**15 - 1)
        if np.max(np.absolute(data))>1:
            print('WARNING: abs(data)>1 for')
    
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    
    # Start playback
    play_obj = sa.play_buffer(audio, 2, 2, fs) # 2 bytes per sample with int16!
    
    # Wait for playback to finish before exiting
    play_obj.wait_done()

def extractNotes(outputMode='lst'):

    # load recorded data
    data_dir = './recordings/'
    recording, samplerate = sf.read(data_dir+'Notes_Mallet.wav')
    data = (recording[:,0]+recording[:,1])/2
    
    # isolate notes sequences [N0,N1,...,N8,S]
    start_idx = [117753,362230,667470,1007450,1297510,1548040,1777330,2009480,2295930,2791970]
    L_notes = 100000 # samples sequence length per note
    notes = [data[idx:idx+L_notes] for idx in start_idx]
    notes.append(0.025*notes[-1])  # appending the Ghost note (G=0.1*S)

    # prepare the output
    if outputMode == 'lst':
        return notes
    elif outputMode == 'dic':
        keys = [str(k) for k in range(0,9)]
        keys.extend(['S','G'])
        return dict(zip(keys, notes))
    else:
        raise ValueError('Unrecognized output mode requested')

def parseUserInput2Music(userInString):
    N0,N1,N2,N3,N4,N5,N6,N7,N8,S,G = extractNotes(outputMode='lst')
    try:
        notesSeq = eval(userInString) # assuming the user's input is safe!!!
        return notesSeq
    except:
        print('Only notes N0,N1,N2,N3,N4,N5,N6,N7,N8,S,G are allowed.')
        print('The notes must be seperated by commas with no empty spaces and the entire sequence enclosed in [].')

def play_music(notesSeq,tempo=200.0):
    
    bps = 60.0/tempo
    fs = 44100
    spacing = int(fs*bps) # samples before each new note is superposed on the previous
    L = spacing*(len(notesSeq)-1)+fs*3 # overall number of samples (3s for last note)
    music = np.zeros(L)
    for i in range(len(notesSeq)):
        j = i*spacing
        music[j:j+100000]=music[j:j+100000]+0.5*notesSeq[i]

    sa_play(music.copy()) # sa_play mutates music (fix)
    return music

if __name__ == "__main__":
    
    if len(sys.argv)==2:
        tempo = 200.0
    elif len(sys.argv)==3:
        tempo = float(sys.argv[2])
    else:
        print('ABORTING: Too few or many argv inputs.')

    notesSeq = parseUserInput2Music(sys.argv[1])
    _ = play_music(notesSeq,tempo)  # creates repetitions