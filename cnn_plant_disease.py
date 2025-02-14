# -*- coding: utf-8 -*-
"""cnn plant disease.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_yp4uPXEwsje16FRlb2flL7FVtGbxAHT
"""

import tensorflow as tf
from tensorflow.keras import models,layers
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf

# Define the main directory
main_dir = '/content/drive/MyDrive/PlantVillage'

# Load the dataset
dataset = tf.keras.preprocessing.image_dataset_from_directory(
    main_dir,
    image_size=(255, 255),  # Resize images to 128x128
    batch_size=32,          # Process images in batches of 32
    label_mode='categorical',  # Labels will be one-hot encoded
    seed=123,
    shuffle=True
)

# Print class names
class_names = dataset.class_names
print("Classes:", class_names)

BATCH_SIZE= 32
IMAGE_SIZE= 255
CHANNEL= 3
EPOCHS= 20

print(dataset.class_names)

len(dataset)

class_names= dataset.class_names

import numpy as np
for batch_size, label_size in dataset.take(1):
    print("image shape:", batch_size.shape)  # Correct variable usage
    print("label:",label_size.numpy)
    print("image",batch_size[0])

plt.figure(figsize=(10, 10))
for image_batch, labels_batch in dataset.take(1):  # Take one batch of data
    for i in range(12):  # Loop through the first 12 images
        ax = plt.subplot(3, 4, i + 1)
        plt.imshow(image_batch[i].numpy().astype("uint8"))  # Convert image tensor to NumPy
        plt.axis("off")

        # Handle different label formats
        if len(labels_batch[i].shape) > 0:  # If the label is multi-dimensional
            label = tf.argmax(labels_batch[i]).numpy()  # Get the index of the max value
        else:  # If the label is a scalar
            label = labels_batch[i].numpy().item()

        plt.title(class_names[label])  # Add the class name as title

train_size = 0.8
len(dataset) * train_size

train_ds = dataset.take(54)
len(train_ds)

test_ds = dataset.skip(54)
len(test_ds)

val_size = 0.1
len(dataset)*val_size

val_ds = test_ds.take(6)
len(val_ds)

test_ds = test_ds.skip(6)
len(test_ds)

def get_dataset_partitions_tf(ds, train_split=0.8, val_split=0.1, test_split=0.1, shuffle=True, shuffle_size=10000):
    assert (train_split + test_split + val_split) == 1

    ds_size = len(ds)

    if shuffle:
        ds = ds.shuffle(shuffle_size, seed=12)

    train_size = int(train_split * ds_size)
    val_size = int(val_split * ds_size)

    train_ds = ds.take(train_size)
    val_ds = ds.skip(train_size).take(val_size)
    test_ds = ds.skip(train_size).skip(val_size)

    return train_ds, val_ds, test_ds
train_ds, val_ds, test_ds = get_dataset_partitions_tf(dataset)

len(train_ds)

len(val_ds)

len(test_ds)

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
val_ds = val_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
test_ds = test_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)

import tensorflow as tf
from tensorflow.keras import layers

IMAGE_SIZE = 255

resize_and_rescale = tf.keras.Sequential([
    layers.Resizing(IMAGE_SIZE, IMAGE_SIZE),
    layers.Rescaling(1./255),
])

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
])

train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y)
).prefetch(buffer_size=tf.data.AUTOTUNE)

from tensorflow.keras import layers, models

input_shape = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL)
n_classes = 3

# Define resizing and rescaling layer (if missing)
resize_and_rescale = layers.Rescaling(1./255)  # Normalize pixel values to [0, 1]

model = models.Sequential([
    resize_and_rescale,
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(n_classes, activation='softmax'),
])

model.build(input_shape=input_shape)

input_shape = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL)
n_classes = 3

model = models.Sequential([
    resize_and_rescale,
    layers.Conv2D(32, kernel_size = (3,3), activation='relu', input_shape=input_shape),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64,  kernel_size = (3,3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64,  kernel_size = (3,3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(n_classes, activation='softmax'),
])

model.build(input_shape=input_shape)

model.summary()

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20
)

scores = model.evaluate(test_ds)

model.save("model.h5")

print(history)
print(history.params)
print(history.history.keys())

history.history['loss'][:5] # show loss for first 5 epochs

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(range(EPOCHS), acc, label='Training Accuracy')
plt.plot(range(EPOCHS), val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(range(EPOCHS), loss, label='Training Loss')
plt.plot(range(EPOCHS), val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

model = tf.keras.models.load_model('model.h5')

import numpy as np
import matplotlib.pyplot as plt

# Take a single batch from the test dataset
for images_batch, labels_batch in test_ds.take(1):
    # Convert the first image to numpy format
    first_image = images_batch[0].numpy().astype('uint8')

    # Decode the one-hot encoded label to its index
    first_label_index = np.argmax(labels_batch[0].numpy())

    print("First image to predict:")
    plt.imshow(first_image)
    plt.axis("off")
    plt.show()

    # Print actual label
    print("Actual label:", class_names[first_label_index])

    # Predict the labels for the batch
    batch_prediction = model.predict(images_batch)

    # Decode the predicted label for the first image
    predicted_label_index = np.argmax(batch_prediction[0])
    print("Predicted label:", class_names[predicted_label_index])

def predict(model, img):
    img_array = tf.keras.preprocessing.image.img_to_array(images[i].numpy())
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence

plt.figure(figsize=(15, 15))

# Iterate through a batch of test data
for images, labels in test_ds.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))

        # Convert the tensor to its class index if one-hot encoded
        actual_class_index = np.argmax(labels[i].numpy())
        actual_class = class_names[actual_class_index]

        # Predict the class and confidence
        predictions = model.predict(images[i][tf.newaxis, ...])  # Add batch dimension
        predicted_class_index = np.argmax(predictions[0])
        predicted_class = class_names[predicted_class_index]
        confidence = round(100 * np.max(predictions[0]), 2)

        # Set the title
        plt.title(f"Actual: {actual_class},\nPredicted: {predicted_class}.\nConfidence: {confidence}%")
        plt.axis("off")

