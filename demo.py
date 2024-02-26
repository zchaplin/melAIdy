import pygame
import pygame.midi
import time
import random

def createTriad(root_note):
    # Adjust the root note down by an octave
    root_note = root_note - 12
    # Major third is 4 semitones above the root
    major_third = root_note + 3
    # Perfect fifth is 7 semitones above the root
    perfect_fifth = root_note + 7
    return [root_note, major_third, perfect_fifth]

def createScale(root_note):
    pattern = [2, 1 , 2, 2, 2, 2, 1]
    scale = [root_note]  # Start the scale with the root note
    for step in pattern:  # Calculate the rest of the scale based on the pattern
        scale.append(scale[-1] + step)
    return scale

# Initialize pygame and the midi module
pygame.init()
pygame.midi.init()

# Open a new MIDI output
port = pygame.midi.get_default_output_id()
midi_output = pygame.midi.Output(port, 0)

# Set up instrument (0 is usually the grand piano)
instrument = 0
midi_output.set_instrument(instrument)

# Choose two random root notes for the song
song = [random.choice(createScale(60)) for _ in range(2)]

for note in song:
    triad = createTriad(note)
    scale = createScale(note)
    
    # Play the triad notes and hold them
    for triad_note in triad:
        midi_output.note_on(triad_note, 127)
    
    # Play scale notes over the held triad
    for scale_note in scale:
        midi_output.note_on(scale_note, 127)
        time.sleep(0.25)  # Note duration
        midi_output.note_off(scale_note, 127)
    
    # Turn off the triad notes
    for triad_note in triad:
        midi_output.note_off(triad_note, 127)

# Close the MIDI output and quit pygame
midi_output.close()
pygame.quit()
