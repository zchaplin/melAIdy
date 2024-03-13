NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]

import random

#----------------------#
#   Nodes + Synapses   #
#----------------------#

class Synapse:
    def __init__(self, weight, source, target):
        self.weight = weight
        self.source = source
        self.target = target

    def forward(self, data):
        pass

class Chord:
    def __init__(self, name, notes):
        self.notes = notes
        self.name = name

    def __str__(self):
        string = f"{self.name} chord: "
        for note in self.notes:
            string += f"{str(note)},"

        return string
        
class Note:
    def __init__(self, note, name):
        self.cost = 0
        self.note = note
        self.name = name

    def __str__(self):
        return f"{self.name}:{self.note}"





#----------------------#
#        Graph         #
#----------------------#

class Graph:
    def __init__(self):
        self.chords = []
        self.chordSynapses = []

        self.notes = []
        self.noteSynapses = []

        self.key = 2 
        self.mode = "major"

        self.song = []

        self.lastNote = None
        self.lastChord = None

        self.start()

    def start(self):
        self.ScaleNotes()
        self.ScaleChords()
        self.notes.append(Note(-1, "None"))
        
        print("Graph started")



    # GENERATE THE NOTES AND CHORDS

    def ScaleNotes(self):
        for i in range(12):
            if self.mode == "major":
                if i in MAJOR:
                    i+=self.key
                    if i > 11: # treat notes as circular
                        i -= 12

                    self.notes.append(Note(i, NOTES[i]))
            elif self.mode == "minor":
                if i in MINOR:
                    i+=self.key
                    if i > 11: # treat notes as circular
                        i -= 12

                    self.notes.append(Note(i, NOTES[i]))

        # create synapses between notes
        for note in self.notes:
            for target in self.notes:
                if note.note != target.note:
                    self.noteSynapses.append(Synapse(1, note, target))

    def ScaleChords(self):
        # create triad chords
        # treat notes as circular
        # just major for now
        for i in range(7):
            if self.mode == "major":
                notes = []
                notes.append(self.notes[i])
                notes.append(self.notes[(i+2)%7])
                notes.append(self.notes[(i+4)%7])
                self.chords.append(Chord(f"{self.notes[i].name} Major", notes))
            elif self.mode == "minor":
                notes = []
                notes.append(self.notes[i])
                notes.append(self.notes[(i+3)%7])
                notes.append(self.notes[(i+5)%7])
                self.chords.append(Chord(f"{self.notes[i].name} Minor", notes))

        # create synapses between chords
        for chord in self.chords:
            for target in self.chords:
                if chord.name != target.name:
                    self.chordSynapses.append(Synapse(1, chord, target))



    # FORWARD ON THE NOTES, UPDATING WEIGHTS

    def NoteForward(self):
        note = self.lastNote

        if note == None:
            note = self.notes[0]

        for synapse in self.noteSynapses: 
            if synapse.source == note:
                if abs(synapse.target.note - note.note) <= 3: # if next note is within 2 semitones, decrease weight
                    synapse.weight -= 0.3
                else:
                    synapse.weight += 0.3
            if synapse.target == note: 
                synapse.weight -= 0.5

            if len(self.song) > 5:
                for i in range(5):
                    if self.song[-i] == synapse.target:
                        synapse.weight -= 0.3 # if in the past 5 notes, the note was played, decrease the weight
            
            synapse.weight += random.uniform(-0.1, 0.1) # randomize the weight ever so slightly



    def WalkNotes(self):
        self.NoteForward()

        self.noteSynapses.sort(key=lambda x: x.weight, reverse=True)
        self.song.append(self.noteSynapses[0].target)
        self.lastNote = self.noteSynapses[0].target
        
        return self.lastNote



    def ChordForward(self):
        chord = self.lastChord

        if chord == None:
            chord = self.chords[0]


        for synapse in self.noteSynapses:
            if synapse.source == chord.notes[0]:
                if abs(synapse.target.note - chord.notes[0].note) <= 2: # decrease weights of the root note of the chord (melody should not be too close to the root note of the chord)
                    synapse.weight -= 0.3 
                else:
                    synapse.weight += 0.3

            for synapse in self.chordSynapses:
                if synapse.source == chord:
                    if abs(synapse.target.notes[0].note - chord.notes[0].note) <= 2: # if next chord root is within 2 semitones, decrease weight
                        synapse.weight -= 0.3
                    else:
                        synapse.weight += 0.3

                if synapse.target == chord: # decrease weight of to the current chord
                    synapse.weight -= 0.5

                # if in the past 5 notes, the note was played, decrease the weight
                if len(self.song) > 5:
                    for i in range(5):
                        if self.song[-i] == synapse.target:
                            synapse.weight -= 0.3
                # randomize the weight ever so slightly
                synapse.weight += random.uniform(-0.1, 0.1)


    def WalkChords(self):
        
        self.ChordForward()
            
        self.chordSynapses.sort(key=lambda x: x.weight, reverse=True)
        self.song.append(self.chordSynapses[0].target)
        self.lastChord = self.chordSynapses[0].target
        return self.lastChord
        



        
import pygame.midi
import time
import random

pygame.midi.init()

device_id = pygame.midi.get_default_output_id()
midi_output = pygame.midi.Output(device_id)

melody_instrument = 0  # Piano
chord_instrument = 48  # String Ensemble

# MIDI channels
melody_channel = 0
chord_channel = 1

# Set instruments for each channel
midi_output.set_instrument(melody_instrument, melody_channel)
midi_output.set_instrument(chord_instrument, chord_channel)

g = Graph()
g.start()



count = 4
swing = [1,.5,.5]
held_note = 0
skip = False
while True:
    # randomly choose between 2 and 4
    bar = random.choice([2, 4])
    if count%4 == 0:
        if g.lastChord != None:
            for note in chord.notes:
                midi_note = note.note+60
                print(note.name, note.note, midi_note)
                velocity = 30  # MIDI velocity (volume) range is 0-127. Adjust as needed.
                midi_output.note_off(midi_note, velocity, chord_channel)
        if count % 4 == 0:
            g.WalkChords()
        chord = g.lastChord
        # if has instance chord, play it
        
        for note in chord.notes:
            midi_note = note.note+60
            print(note.name, note.note, midi_note)
            velocity = 30  # MIDI velocity (volume) range is 0-127. Adjust as needed.
            midi_output.note_on(midi_note, velocity, chord_channel)
            # time.sleep(0.5)  # Short delay to stagger chord notes
            # midi_output.note_off(midi_note, velocity)
        print("^chord\n")

    g.WalkNotes()
    note = g.lastNote
    if not skip and held_note != 0:
        midi_output.note_off(held_note, velocity, melody_channel)
        held_note = 0

    if not skip:
        if note.note != -1:
            midi_note = note.note + 72
            print(note.name, note.note, midi_note)
            velocity = 64
            midi_output.note_on(midi_note, velocity, melody_channel)
    
    time.sleep(.5)

    next_skip = (random.choice(swing) == 1)
    held_note = note.note + 72
    if not skip and not next_skip: 
        midi_output.note_off(midi_note, velocity, melody_channel)

    skip = next_skip

    count += 1

# swing = [1,.5]
# track = 2
# while True:
#     # randomly choose between 2 and 4
#     bar = random.choice([1])
#     if track >= 2:
#         track = 0       
#         # if has instance chord, play it
#         if g.lastChord != None:
#             for note in chord.notes:
#                 midi_note = note.note+60
#                 print(note.name, note.note, midi_note)
#                 velocity = 30  # MIDI velocity (volume) range is 0-127. Adjust as needed.
#                 midi_output.note_off(midi_note, velocity, chord_channel)
            
#         g.WalkChords()
#         chord = g.lastChord

#         for note in chord.notes:
#             midi_note = note.note+60
#             print(note.name, note.note, midi_note)
#             velocity = 30  # MIDI velocity (volume) range is 0-127. Adjust as needed.
#             midi_output.note_on(midi_note, velocity, chord_channel)
#             # time.sleep(0.5)  # Short delay to stagger chord notes
#             # midi_output.note_off(midi_note, velocity)
#         print("^chord\n")

#     g.WalkNotes()
#     note = g.lastNote

#     if note.note != -1:
#         midi_note = note.note + 72
#         print(note.name, note.note, midi_note)
#         velocity = 64
#         midi_output.note_on(midi_note, velocity, melody_channel)
#     rand = swing[random.randint(0,1)]
#     time.sleep(rand)
#     track += rand
#     midi_output.note_off(midi_note, velocity, melody_channel)




