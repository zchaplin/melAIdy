
# ---- Play sounds ---
# major chords
chord_to_midi = {
    "A": [57, 61, 64],
    "B": [59, 63, 66],
    "C": [60, 64, 67],
    "D": [62, 66, 69],
    "E": [64, 68, 71],
    "F": [65, 69, 72],
    "G": [67, 71, 74],

    # minor chords
    "A:min": [57, 60, 64],
    "B:min": [59, 62, 66],
    "C:min": [60, 63, 67],
    "D:min": [62, 65, 69],
    "E:min": [64, 67, 71],
    "F:min": [65, 68, 72],
    "G:min": [67, 70, 74],

    # flat chords
    "Ab": [56, 60, 63],
    "Bb": [58, 62, 65],
    "Db": [61, 65, 68],
    "Eb": [63, 67, 70],
    "Gb": [66, 70, 73],

    # flat minor chords
    "Ab:min": [56, 59, 63],
    "Bb:min": [58, 61, 65],
    "Db:min": [61, 64, 68],
    "Eb:min": [63, 66, 70],
}

import random
n=15
notes = []
for i in range(n):
    notes.append(random.choice(list(chord_to_midi.values())))
print("FINAL NOTES TO PLAY:" , notes)

# init pygame
import pygame.midi
import time
pygame.midi.init()


def play_chords(notes, duration):
    # Open the default MIDI output port
    port = pygame.midi.get_default_output_id()
    midi_output = pygame.midi.Output(port, 0)
    instrument = 0
    midi_output.set_instrument(instrument)
    
    for chord in notes:
        # Start playing the note (144 = note on, note = MIDI note number, 127 = velocity)
        midi_output.note_on(chord[0], 127)
        midi_output.note_on(chord[1], 127)
        midi_output.note_on(chord[2], 127)

        midi_output.note_on(chord[0], 127)
        time.sleep(duration/3)
        midi_output.note_on(chord[1], 127)
        time.sleep(duration/3)
        midi_output.note_on(chord[2], 127)
        time.sleep(duration/3)

        # Stop playing the note (128 = note off)
        midi_output.note_off(chord[0], 127)
        midi_output.note_off(chord[1], 127)
        midi_output.note_off(chord[2], 127)
    
    # Close the MIDI output
    midi_output.close()

play_chords(notes, 1)