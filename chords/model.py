from create_datasets import converted_training, converted_testing, converted_training_label, converted_testing_label
from tensorflow import keras
from tensorflow.keras import layers, Sequential
from keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import numpy as np
from keras.preprocessing.sequence import pad_sequences

# ChatGPT did the encoding:
# All data sets need to have the same length, which is a problem becuase our datasets chose random number of chords for each progression
# So we use padding to make sure all the lists have the same range
max_sequence_length = 8  # max of 8 chords in a progression
train_padded = pad_sequences(converted_training, maxlen=max_sequence_length, padding='post', truncating='post')
train_answer_padded = pad_sequences(converted_training_label, maxlen=max_sequence_length, padding='post', truncating='post')
test_padded = pad_sequences(converted_testing, maxlen=max_sequence_length, padding='post', truncating='post')
test_answer_padded = pad_sequences(converted_testing_label, maxlen=max_sequence_length, padding='post', truncating='post')
# switch to np arrays because that's what keras uses
train = np.array(train_padded)
train_answer = np.array(train_answer_padded)
test = np.array(test_padded)
test_answer = np.array(test_answer_padded)
# [THIS IS A BUG: SIZE SHOULD ALWAYS BE THE SAME. IT'S A PROBLEM WITH THE CREATE_DATASETS.PY BUT I WANTED TO CHECK IF THIS DIRECTION IS GOOD BEFORE FIXING BUGS]
# same size between x and y
min_samples = min(len(train), len(train))
train = train[:min_samples]
train_answer = train_answer[:min_samples]
test = test[:min_samples]
test_answer = test_answer[:min_samples]
# Define the model
model = Sequential()
model.add(Dense(64, input_dim=train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(8, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(train, train_answer, epochs=10, batch_size=32)

# Evaluate the model
loss, accuracy = model.evaluate(test, test_answer)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
