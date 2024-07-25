import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os

def main():
    basepath = "D:/P/100% new Land class for satellite image"

    # Initializing the CNN
    classifier = Sequential()

    # Step 1 - Convolution Layer
    classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    classifier.add(BatchNormalization())
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding second convolution layer
    classifier.add(Conv2D(64, (3, 3), activation='relu'))
    classifier.add(BatchNormalization())
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding third convolution layer
    classifier.add(Conv2D(128, (3, 3), activation='relu'))
    classifier.add(BatchNormalization())
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Step 3 - Flattening
    classifier.add(Flatten())

    # Step 4 - Full Connection
    classifier.add(Dense(256, activation='relu'))
    classifier.add(Dropout(0.5))
    classifier.add(Dense(7, activation='softmax'))  # Change class no.

    # Compiling The CNN with Adam optimizer
    classifier.compile(
        optimizer=Adam(learning_rate=0.0001),  # Lower learning rate for smoother convergence
        loss='categorical_crossentropy',
        metrics=['accuracy'])

    # Part 2 - Fitting the CNN to the image
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./255)

    training_set = train_datagen.flow_from_directory(
        os.path.join(basepath, 'train_set'),
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical')

    test_set = test_datagen.flow_from_directory(
        os.path.join(basepath, 'test_set'),
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical')

    steps_per_epoch = int(np.ceil(training_set.samples / 32))
    val_steps = int(np.ceil(test_set.samples / 32))

    # Increased epochs for better training
    model = classifier.fit_generator(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=100,
        validation_data=test_set,
        validation_steps=val_steps
    )

    # Saving the model with proper file naming
    classifier.save(os.path.join(basepath, 'land1_model.h5'))

    # Evaluate model performance
    scores = classifier.evaluate(test_set, verbose=1)
    testing_accuracy = "Testing Accuracy: %.2f%%" % (scores[1]*100)
    print(testing_accuracy)
    
    scores = classifier.evaluate(training_set, verbose=1)
    training_accuracy = "Training Accuracy: %.2f%%" % (scores[1]*100)
    print(training_accuracy)

    # Plotting model accuracy
    plt.plot(model.history['accuracy'])
    plt.plot(model.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(os.path.join(basepath, 'accuracy.png'), bbox_inches='tight')
    plt.show()

    # Plotting model loss
    plt.plot(model.history['loss'])
    plt.plot(model.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(os.path.join(basepath, 'loss.png'), bbox_inches='tight')
    plt.show()

    return testing_accuracy + '\n' + training_accuracy

if __name__ == "__main__":
    main()
