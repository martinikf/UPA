"""
    Use keras version 2, tensorflow <= 2.15
"""

import numpy as np
import tensorflow as tf
import tensorflowjs as tfjs
from sklearn.model_selection import train_test_split


DATASET_FILENAME = 'dataset.csv'
OUTPUT_TFJS_FOLDER = 'tfjsmodel'
OUTPUT_KERAS_FILE = 'model.keras'
RANDOM_SEED = 42
TRAIN_SIZE = 0.75

NUM_OF_FEATURES = 42

def create_confusing_matrix(pred_labels, top_pred):
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix, classification_report

    labels = sorted(list(set(pred_labels)))
    cmx_data = confusion_matrix(pred_labels, top_pred, labels=labels)

    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(df_cmx, annot=True, fmt='g', square=False)
    ax.set_ylim(len(set(pred_labels)), 0)
    plt.show()


def run():
    # Load dataset
    data = np.loadtxt(DATASET_FILENAME, delimiter=',', dtype='float32', usecols=range(NUM_OF_FEATURES + 1))
    features = data[:, 1:]
    labels = data[:, 0].astype('int32')

    num_of_classes = len(set(labels))

    # Split dataset
    features_train, features_test, labels_train, labels_test = train_test_split(features, labels, train_size=TRAIN_SIZE, random_state=RANDOM_SEED)

    # Model definition
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(NUM_OF_FEATURES,)),
        tf.keras.layers.Dropout(0.2, name="d1"),
        tf.keras.layers.Dense(42, activation='relu', name="dense1"),
        tf.keras.layers.Dropout(0.2, name="d2"),
        tf.keras.layers.Dense(42, activation='relu', name="dense2"),
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
        batch_size=4,
        validation_data=(features_test, labels_test),
        callbacks=[es_callback]
    )

    # Show confusion matrix
    create_confusing_matrix(
        labels_test,
        np.argmax(model.predict(features_test), axis=1)
    )

    # Save model
    model.save(OUTPUT_KERAS_FILE)
    tfjs.converters.save_keras_model(model, OUTPUT_TFJS_FOLDER)


run()
