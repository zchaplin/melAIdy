import random, re

# -----------------------
# Creating datasets from text files
# -----------------------

# Look through the sound files and create training data
# training.txt is organized like that: timestamp1   timestamp2  chord
    # so we need to extract only the chords
training_path = "./sound_files/training.txt"
# training_path = "./sound_files/one_chord_training.txt"
testing_path = "./sound_files/testing.txt"
# testing_path = "./sound_files/one_chord_testing.txt"


# copied #120
max_length = 4
def create_dataset(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    # Last col has the chord info
    chords = []
    for line in lines:
        columns = line.split('\t')
        last_column = columns[2].strip()
        chords.append(last_column)

    # Choose a random number of chords (between 3-8) and save them as chord progression 
    chord_progression = []
    current_progression = []
    answer_chord = []
    length_of_progression = max_length # random.randint(3, 8)
    for chord in chords:
        # simplifying the dataset (before had 180 unique chords, which made it difficult to see any learning)
        if len(chord) > 1:
            chord = chord[:1]
        if "sus" in chord:
            chord = chord.replace("sus", "min")
        if "/b" in chord:
            chord = chord.replace("/b", "")
        if "/" in chord:
            chord = chord.replace("/", "")
        if ":maj" in chord:
            chord = chord.replace(":maj", "")
        if ":min" in chord:
            chord = chord.replace(":min", "")
        if ":aug" in chord:
            chord = chord.replace(":aug", "")
        if ":hdim" in chord:
            chord = chord.replace(":hdim", "")
        if "(b)" in chord:
            chord = chord.replace("(b)", "")
        if ":dim" in chord:
            chord = chord.replace(":dim", "")
        if "#" in chord:
            chord = chord.replace("#", "")
       
        chord = re.sub(r'\d', '', chord)
        current_progression.append(chord)
        # N appears at the beginning/end of each song, so to make sure the progression will only include chords from one song, we cut it off whenever we reach the N
        
        # ignore non chords
        if chord == "N" or not chord or len(chord) == 0: 
            current_progression.pop()
        
            # removing the last chord and saving it into the answers array
        if len(current_progression) > 0 and len(current_progression) == length_of_progression:
            answer_chord.append(current_progression.pop())

            chord_progression.append(current_progression)
            current_progression = []
            length_of_progression = max_length #random.randint(3, 8)

    # remove empty chords
    chord_progression = [x for x in chord_progression if x]
    answer_chord = [x for x in answer_chord if x]
    print ("comparing lengths: ", len(answer_chord), len(chord_progression))
    print(f"chord progression: {chord_progression}\n\nanswer chord: {answer_chord}\n\n")
    for i in range(0,len(chord_progression)-1):
        chord = chord_progression[i]
        if not chord or chord == "N":
            chord_progression.pop(i)
            answer_chord.pop(i)
    for i in range(0,len(answer_chord)-1):
        chord = answer_chord[i]
        if not chord or chord == "N":
            chord_progression.pop(i)
            answer_chord.pop(i)
    # chord_progression = [x for x in chord_progression if x]
    # answer_chord = [x for x in answer_chord if x]

    return chord_progression, answer_chord

# SIZING PROBLEM: IF ANSWER IS N, AND THEN WE REMOVE ALL N, WE NEED TO THROW AWAY THE CORRESPONDING


# -----------------------
# Convert to correct data type that could be used in keras
# -----------------------

# Find all the unique chords
def find_unique_chords(dataset):
    unique_chords = set()  # Using a set to store unique chords
    for progression in dataset:
        for chord in progression:
            unique_chords.add(chord)
    
    return unique_chords

def find_unique_chords_2(dataset, unique_chords):
    for chord in dataset:
        unique_chords.add(chord)
    
    return unique_chords


# Give a number for each unique chord
def map_chord_to_num(dataset):
    chord_mapping = {}  # Dictionary to store mapping between chords and numbers
    next_index = 0  # Counter to assign unique numbers to chords

    for chord in dataset:
        if chord not in chord_mapping:
            # Assign the next available index to the chord
            chord_mapping[chord] = next_index
            next_index += 1  # Move to the next available index
    return chord_mapping

# Create a new dataset, using the numbers rather than string for chords
    # Ex. if the chord is G:min7, switch it to 1
def convert_chord_to_num(dataset, map, isProgression):
    converted_dataset = []
    for progression in dataset:
        current_progression = []
        # Iterate over each chord in the progression
        # Training datasets have progressions
        if isProgression:
            for chord in progression:
                if chord in map:
                    current_progression.append(map[chord])
        # Testing datasets have only one chord
        else:
            if progression in map:
                current_progression.append(map[progression])
        converted_dataset.append(current_progression)
    return converted_dataset



training_dataset, training_label = create_dataset(training_path)
testing_dataset, testing_label = create_dataset(testing_path)

# print("\ntraining dataset:\n ", training_dataset, "\ntraining label:\n ", training_label)
# print("\ntesting dataset:\n ", testing_dataset, "\ntesting label:\n ", testing_label)
# print("are training len equal? ", len(training_dataset), " = ", len(training_label))
# print("are testing len equal? ", len(testing_dataset), " = ", len(testing_label))

unqiue = find_unique_chords(training_dataset+testing_dataset)
unqiue = find_unique_chords_2(training_label+testing_label, unqiue)
map = map_chord_to_num(unqiue)
print("\nmap: ", map, "\n")

# convert chords to numbers:
converted_training = convert_chord_to_num(training_dataset, map, True)
converted_training_label = convert_chord_to_num(training_label, map, False)
converted_testing = convert_chord_to_num(testing_dataset, map, True)
converted_testing_label = convert_chord_to_num(testing_label, map, False)

# print("\ntraining dataset:\n ", converted_training, "\ntraining label:\n ", converted_training_label)
# print("\ntesting dataset:\n ", converted_testing, "\ntesting label:\n ", converted_testing_label)
# print("are training len equal? ", len(converted_training), " = ", len(converted_training_label))
# print("are testing len equal? ", len(converted_testing), " = ", len(converted_testing_label))
