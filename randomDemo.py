import pygame.midi
import random
import time

# Initialize Pygame MIDI
pygame.midi.init()

# Get default MIDI output ID and open it for output
device_id = pygame.midi.get_default_output_id()
midi_output = pygame.midi.Output(device_id)

# Set MIDI instruments (program numbers)
chord_instrument = 48  # Strings Ensemble
melody_instrument = 0  # Acoustic Grand Piano

# MIDI channels (0-15, where 9 is typically reserved for percussion)
chord_channel = 1
melody_channel = 0

# Set instruments for channels
midi_output.set_instrument(chord_instrument, chord_channel)
midi_output.set_instrument(melody_instrument, melody_channel)

# Define a function to play a single random note
def play_random_note(velocity=100, duration=0.5, channel=0):
    # Generate a random MIDI note (within a reasonable range)
    note = random.randint(48, 84)  # From C3 to C6
    midi_output.note_on(note, velocity, channel)
    time.sleep(duration)
    midi_output.note_off(note, velocity, channel)

# Define a function to play a chord made of random notes
def play_random_chord(velocity=100, duration=1, channel=1):
    notes = [random.randint(48, 84) for _ in range(3)]  # Generate 3 random notes for the chord
    for note in notes:
        midi_output.note_on(note, velocity, channel)
    time.sleep(duration)
    for note in notes:
        midi_output.note_off(note, velocity, channel)

# Play 8 random chords and random notes
for _ in range(8):
    play_random_chord(velocity=100, duration=1, channel=chord_channel)
    # After each chord, play 4 random notes
    for _ in range(4):
        play_random_note(velocity=100, duration=0.25, channel=melody_channel)

# Cleanup
midi_output.close()
pygame.midi.quit()
