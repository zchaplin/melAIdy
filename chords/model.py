from create_datasets import converted_training, converted_testing, converted_training_label, converted_testing_label, map
from tensorflow.keras import Sequential
from keras.layers import *
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import RMSprop, Adam
from keras.utils import to_categorical

# All data sets need to have the same length, which is a problem becuase our datasets chose random number of chords for each progression
# So we use padding to make sure all the lists have the same range
max_sequence_length = 2  # max of 8 chords in a progression
train_padded = pad_sequences(converted_training, maxlen=max_sequence_length, padding='post', truncating='post')
train_answer_padded = pad_sequences(converted_training_label, maxlen=1, padding='post', truncating='post') 
test_padded = pad_sequences(converted_testing, maxlen=max_sequence_length, padding='post', truncating='post')
test_answer_padded = pad_sequences(converted_testing_label, maxlen=1, padding='post', truncating='post')
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

# One-hot encode the labels
train_one_hot = to_categorical(train)
test_one_hot = to_categorical(test)

train_answer_one_hot = to_categorical(train_answer)
test_answer_one_hot = to_categorical(test_answer)


print(f"train: {train}\n\ntrain answer: {train_answer}\n\ntest: {test}\n\ntest answer: {test_answer}")
num_classes = test_answer_one_hot.shape[1]
input_shape = (len(train[0]),)
print("num classes:" , num_classes)

# Define the model

model = Sequential()

# model.add(Rescaling(1/255, input_shape=input_shape))
# model.add(Dense(32, activation='relu'))
# model.add(Conv2D(64,kernel_size=(3, 3), dilation_rate=(2, 2), activation='relu', padding='same'))
# model.add(DepthwiseConv2D(kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# model.add(Conv2D(32,kernel_size=(2,2)))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Conv2D(32,kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D())

model.add(Reshape((1, 2, 1), input_shape=(2,)))  # reshape it so we could use the Conv2D
model.add(Conv2D(filters=32, kernel_size=(1, 1), activation='relu'))
model.add(Conv2D(num_classes,(1,1), activation='relu'))
model.add(MaxPooling2D(pool_size=(1, 1)))
model.add(SpatialDropout2D(0.1))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(32, activation='relu'))
model.add(BatchNormalization())

# model.add(Embedding(input_dim=num_classes, output_dim=50, input_length=2))

model.add(Dense(64, activation='relu'))
model.add(Flatten())
# model.add(Dense(256, activation='relu'))

model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(
            optimizer=RMSprop(learning_rate=1e-05),
            # optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy'],
        )
# Train the model
model.fit(train, train_answer_one_hot, epochs=20, batch_size=32, validation_data=(train, train_answer_one_hot))

# Evaluate the model
print("Shape of test:", test.shape)
print("Shape of test_answer_one_hot:", test_answer_one_hot.shape)

loss, accuracy = model.evaluate(test, test_answer_one_hot)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# predict next chord
predictions = model.predict(test)

# Find index of class with highest probability for each sample
predicted_indices = np.argmax(predictions, axis=1)

print(predicted_indices)
