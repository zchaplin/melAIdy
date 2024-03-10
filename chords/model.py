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

# One-hot encode the labels
train_answer_one_hot = to_categorical(train_answer)
test_answer_one_hot = to_categorical(test_answer)

# print(f"train: {train}\n\ntrain answer: {train_answer}\n\ntest: {test}\n\ntest answer: {test_answer}")
num_classes = test_answer_one_hot.shape[1]
input_shape = (len(train[0]),)
print("num classes:" , num_classes)

# Define the model
model = Sequential()
# model.add(Rescaling(1/255, input_shape=input_shape))
model.add(Reshape((1, 3, 1), input_shape=(3,)))  # reshape it so we could use the Conv2D
model.add(Conv2D(filters=64, kernel_size=(1, 1), activation='relu'))
model.add(Conv2D(128,(1,1), activation='relu'))

model.add(DepthwiseConv2D(kernel_size=(1, 1), activation='relu', padding='valid'))

model.add(Conv2D(filters=128,kernel_size=(1,1)))
model.add(Conv2D(32,kernel_size=(1, 1), activation='relu'))

model.add(SpatialDropout2D(0.2))

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(BatchNormalization())

model.add(Dense(32, activation='relu'))
model.add(Dense(64, activation='relu'))

model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(
            # optimizer=RMSprop(learning_rate=1e-05),
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy'],
        )
# Train the model
model.fit(train, train_answer_one_hot, epochs=10, batch_size=32, validation_data=(train, train_answer_one_hot))

# Evaluate the model
loss, accuracy = model.evaluate(test, test_answer_one_hot)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# predict next chord
predictions = model.predict(test)
print("PREDICTION: ", predictions)
# Find index of class with highest probability for each sample
predicted_indices = np.argmax(predictions, axis=1)

print(predicted_indices)


# ------ PLAY CHORDS OF TEST IN ORDER -----
predicted_chord_progression = []
for i in range(0,len(test)-1):
    predicted_chord_progression.extend(test[i])
    predicted_chord_progression.append(predicted_indices[i])
print("AI answer: ", predicted_chord_progression)

# Get the actual chords from the map:
converted_chords = []
for chord in predicted_chord_progression:
    for c, n in map.items():
        if n == chord:
            converted_chords.append(c)
print("converted chords: ", converted_chords)
print("map", map)


# ---- Play sounds ---
chord_to_midi = {
    "A": [57, 61, 64],
    "B": [59, 63, 66],
    "C": [60, 64, 67],
    "D": [62, 66, 69],
    "E": [64, 68, 71],
    "F": [65, 69, 72],
    "G": [67, 71, 74],
}

notes = []
for chord in converted_chords:
    notes.append(chord_to_midi[chord])
print("FINAL NOTES TO PLAY:" , notes)
