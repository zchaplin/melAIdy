from queue import PriorityQueue
import pygame
import pygame.midi
import time
pygame.init()
pygame.midi.init()
ALL_NOTES = [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68]


class Note:
    # Store notes as combination of note & octave
    # note letter = ALL_NOTES[note]
    # note octave = octave
    def __init__(self, note=0, octave=4):
        self.note = note
        self.octave = octave

        self.distance = float('inf')
        self.predecessor = None
        self.visited = False

        self.adj = {}

    def __repr__(self):
        return f"Node: MIDI {ALL_NOTES[self.note]}"

    def add_edge(self, other_note, weight):
        self.adj[other_note] = weight


class Graph:
    def __init__(self):
        self.nodes = {}

        self._init_graph()
        self._add_edges()
        self.path = []

    # Create a graph of all notes A1 - G#6
    def _init_graph(self):
        for octave in range(1, 7):  # scales 1-6 [A1, A2, A3...]
            for note_number in range(12):  # notes 0-11 [A1, A#1, B1...]
                self.nodes[(note_number, octave)] = Note(note_number, octave)

    def __repr__(self):
        return str(self.nodes)
        # return f"graph with {len(self.nodes)} notes"

    # Example: adds edges for a major third interval (4 semitones)
    def _add_edges(self):
        for key, note in self.nodes.items():
            target_note_number = (key[0] + 4) % 12
            target_octave = key[1] + ((key[0] + 4) // 12)
            if (target_note_number, target_octave) in self.nodes:
                note.add_edge(self.nodes[(target_note_number, target_octave)], 1)

    # Example: finds a path from the start to end note based on the major third edges
    def get_path(self, start_note, end_note):
        for note in self.nodes.values():
            note.distance = float('inf')
            note.predecessor = None
            note.visited = False

        start_node = self.nodes[start_note]
        start_node.distance = 0
        pq = PriorityQueue()
        pq.put((0, start_node))

        while not pq.empty():
            current_distance, current_node = pq.get()
            if current_node.visited:
                continue
            current_node.visited = True

            for adj_node, weight in current_node.adj.items():
                distance = current_distance + weight
                if distance < adj_node.distance:
                    adj_node.distance = distance
                    adj_node.predecessor = current_node
                    pq.put((distance, adj_node))

        # reconstruct path
        current_node = self.nodes[end_note]
        path = []
        while current_node:
            path.insert(0, current_node)
            current_node = current_node.predecessor
        self.path = path
        return path
    def get_midi_notes(self):
        song = []
        for i in self.path:
            song.append(ALL_NOTES[i.note])
        return song



# Function to play a MIDI note
def play_midi_notes(notes, duration):
    # Open the default MIDI output port
    port = pygame.midi.get_default_output_id()
    midi_output = pygame.midi.Output(port, 0)
    instrument = 0
    midi_output.set_instrument(instrument)
    
    for note in notes:
        # Start playing the note (144 = note on, note = MIDI note number, 127 = velocity)
        midi_output.note_on(note, 127)
        # Wait for the duration of the note
        time.sleep(duration)
        # Stop playing the note (128 = note off)
        midi_output.note_off(note, 127)
    
    # Close the MIDI output
    midi_output.close()
# Example usage: Play Middle C (MIDI number 60) for 1 second



graph = Graph()
print("Graph:")
print(graph, end='\n\n')

start_note = (0, 2)  # A2
end_note = (0, 5)  # E4
print("Path:")
path = graph.get_path(start_note, end_note)
#path_repr = [str(note) for note in path]
print(path)
print("\n\n\n")
midi_notes = graph.get_midi_notes()  # Get the list of MIDI notes
print(midi_notes)
play_midi_notes(midi_notes, 1)  # Play each note in the list for 1 second
