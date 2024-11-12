import numpy as np
import tensorflow as tf
import tensorflowjs as tfjs
from sklearn.model_selection import train_test_split


DATASET_FILENAME = 'dataset.csv'
OUTPUT_TFJS_FOLDER = 'tfjsmodel'
OUTPUT_KERAS_FILE = 'model.keras'
RANDOM_SEED = 42


def run():
    # Load dataset
    data = np.loadtxt(DATASET_FILENAME, delimiter=',', dtype='float32', usecols=range(43))
    features = data[:, 1:]
    labels = data[:, 0].astype('int32')

    num_of_classes = len(set(labels))

    features_train, features_test, labels_train, labels_test = train_test_split(features, labels, train_size=0.75, random_state=RANDOM_SEED)

    # Model definition
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(42,)),
        tf.keras.layers.Dropout(0.2, name="d1"),
        tf.keras.layers.Dense(20, activation='relu', name="dense1"),
        tf.keras.layers.Dropout(0.4, name="d2"),
        tf.keras.layers.Dense(10, activation='relu', name="dense2"),
        tf.keras.layers.Dense(num_of_classes, activation='softmax', name="dense3")
    ])
    model.summary()

    # Callback for early stopping
    es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)

    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Train model
    model.fit(
        features_train,
        labels_train,
        epochs=1000,
        batch_size=128,
        validation_data=(features_test, labels_test),
        callbacks=[es_callback]
    )

    # Save model
    model.save(OUTPUT_KERAS_FILE)
    tfjs.converters.save_keras_model(model, OUTPUT_TFJS_FOLDER)


run()
