from create_datasets import converted_training, converted_testing, converted_training_label, converted_testing_label, map
from tensorflow.keras import Sequential
from keras.layers import *
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import RMSprop, Adam
from keras.utils import to_categorical

# All data sets need to have the same length, which is a problem becuase our datasets chose random number of chords for each progression
# So we use padding to make sure all the lists have the same range
max_sequence_length = 3  # max of 8 chords in a progression
train_padded = pad_sequences(converted_training, maxlen=max_sequence_length, padding='post', truncating='post')
train_answer_padded = pad_sequences(converted_training_label, maxlen=1, padding='post', truncating='post') 
test_padded = pad_sequences(converted_testing, maxlen=max_sequence_length, padding='post', truncating='post')
test_answer_padded = pad_sequences(converted_testing_label, maxlen=1, padding='post', truncating='post')
# switch to np arrays because that's what keras uses
train = np.array(train_padded)
train_answer = np.array(train_answer_padded)
test = np.array(test_padded)
test_answer = np.array(test_answer_padded)
print("TRAIN IS ", train)
print("train label is", train_answer)
# One-hot encode the labels
train_answer_one_hot = to_categorical(train_answer)
test_answer_one_hot = to_categorical(test_answer)

# print(f"train: {train}\n\ntrain answer: {train_answer}\n\ntest: {test}\n\ntest answer: {test_answer}")
num_classes = test_answer_one_hot.shape[1]
input_shape = (len(train[0]),)
print("num classes:" , num_classes)
print("input shape: ", input_shape)

# Define the model
model = Sequential()

model.add(Embedding(input_dim=num_classes, output_dim=200, input_length=max_sequence_length))
model.add(LSTM(units=64))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.20))
model.add(Dense(64, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(
            # optimizer=RMSprop(learning_rate=1e-05),
            optimizer=Adam(learning_rate=0.00005),
            loss='categorical_crossentropy',
            metrics=['accuracy'],
        )
# Train the model
model.fit(train, train_answer_one_hot, epochs=45, batch_size=32, validation_data=(train, train_answer_one_hot))

# Evaluate the model
loss, accuracy = model.evaluate(test, test_answer_one_hot)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# predict next chord

# pick the first chord from the test set, keep predicting the next chord until we have n chords
n = 20
gen_chords = list(test[0])
for i in range(n):
    test_num = []
    for chord in gen_chords[-3:]:
        test_num.append(chord)
        # test_num.append(map[chord])
    test_num = np.array(test_num).reshape(1, -1)
    print("test_num: ", test_num)
    predictions = model.predict(test_num)
    predicted_indices = np.argmax(predictions, axis=1)
    if predicted_indices[0] in gen_chords[-2:]:
        # give a random chord if the predicted chord is already in the progression
        predicted_indices[0] = np.random.choice([i for i in range(0, num_classes) if i not in gen_chords[-3:]])
    print("Predictions: ", predicted_indices)
    gen_chords.append(predicted_indices[0])

print("Generated chords: ", gen_chords)

# Get the actual chords from the map:
converted_chords = []
for chord in gen_chords:
    for c, n in map.items():
        if n == chord:
            converted_chords.append(c)
# print("converted chords: ", converted_chords)
# print("map", map)


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

notes = []
for chord in converted_chords:
    notes.append(chord_to_midi[chord])
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