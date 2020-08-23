"""
Simple Keyboard Player
Use keys: 0,1,2,3,4,5,6,7,8,s,g
(no numpad support)

Arash Mohtat
Aug 23rd, 2020
"""

from playCMDmusic import extractNotes, sa_play
from pynput import keyboard

notes = extractNotes(outputMode='dic')
print(list(notes.keys()))
melody = []

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char.upper()  # single-char keys
    except:
        k = key.name  # other keys
    if k in list(notes.keys()):  # keys of interest
        print('Key pressed: ' + k)
        melody.append(k)
        sa_play(notes[k],fs=44100, normalize=False, wait=False)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys
print(melody)