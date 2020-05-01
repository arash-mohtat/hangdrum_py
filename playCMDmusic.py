import sys
import numpy as np
import soundfile as sf
from analyzeRecordings import sa_play


def extractNotes(outputMode='lst'):

    # load recorded data
    data_dir = './recordings/'
    recording, samplerate = sf.read(data_dir+'Notes_Mallet.wav')
    data = (recording[:,0]+recording[:,1])/2
    
    # isolate notes sequences [N0,N1,...,N8,T]
    start_idx = [117753,362230,667470,1007450,1297510,1548040,1777330,2009480,2295930,2791970]
    L_notes = 100000 # samples sequence length per note
    notes = [data[idx:idx+L_notes] for idx in start_idx]
    notes.append(0.025*notes[-1])  # appending the Ghost note (G=0.1*T)

    # prepare the output
    if outputMode == 'lst':
        return notes
    elif outputMode == 'dic':
        keys = [str(k) for k in range(0,9)]
        keys.extend(['T','G'])
        return dict(zip(keys, notes))
    else:
        raise ValueError('Unrecognized output mode requested')

def parseUserInput2Music(userInString):
    N0,N1,N2,N3,N4,N5,N6,N7,N8,T,G = extractNotes(outputMode='lst')
    try:
        notesSeq = eval(userInString) # assuming the user's input is safe!!!
        return notesSeq
    except:
        print('Some exception happened.')
        print('Only notes N0,N1,N2,N3,N4,N5,N6,N7,N8,T,G are allowed.')
        print('The notes should be seperated by commas with the entire sequence enclosed in [].')

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