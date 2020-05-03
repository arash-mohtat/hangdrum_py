# playGroove.py

import os
import sys
from playCMDmusic import play_music, parseUserInput2Music

def readGrooveFile(file_name):
    """ reads the text file in directory 'grooves' that contains the groove to play."""
    
    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    groove_file = os.path.join(os.path.join(current_dir, 'grooves'), file_name)
    with open(groove_file,'r') as f:  
        input_string = "".join(line.rstrip().replace("^","") for line in f if not line.startswith('#')) 
    return input_string

if __name__ == "__main__":
    
    if len(sys.argv)==2:
        tempo = 200.0
    elif len(sys.argv)==3:
        tempo = float(sys.argv[2])
    else:
        print('ABORTING: Too few or many argv inputs.')

    input_string = readGrooveFile(sys.argv[1])
    _ = play_music(parseUserInput2Music(input_string),tempo)