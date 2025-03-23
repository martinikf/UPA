# Environment: 4.22 tensorflow js python 3.11 linux

import os
# Keep using Keras 2
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import numpy as np
import pandas as pd
import tensorflow_decision_forests as tfdf
import tensorflowjs as tfjs

DATASET_FILENAME = 'dataset.csv'
OUTPUT_TFDF_MODEL_PATH = 'model'
OUTPUT_TFJS_MODEL_PATH = 'tfjs'
RANDOM_SEED = 42
TRAIN_SIZE = 0.75

NUM_OF_FEATURES = 42

np.random.seed(RANDOM_SEED)


def split_dataset(dataset, test_ratio=0.10):
    """Splits a panda dataframe in two."""

    test_indices = np.random.rand(len(dataset)) < test_ratio
    return dataset[~test_indices], dataset[test_indices]


def run():
    dataset_df = pd.read_csv(DATASET_FILENAME)
    print(dataset_df.head(3))

    train_ds_pd, test_ds_pd = split_dataset(dataset_df, 1-TRAIN_SIZE)
    print("{} examples in training, {} examples for testing.".format(
        len(train_ds_pd), len(test_ds_pd)))

    train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(train_ds_pd, label="label")
    test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(test_ds_pd, label="label")

    model_1 = tfdf.keras.GradientBoostedTreesModel(verbose=2)
    model_1.fit(train_ds)
    model_1.compile(metrics=["accuracy", "Precision", "Recall"])
    evaluation = model_1.evaluate(test_ds, return_dict=True)
    print()
    for name, value in evaluation.items():
        print(f"{name}: {value:.4f}")

    model_1.save(OUTPUT_TFDF_MODEL_PATH)

    tfjs.converters.tf_saved_model_conversion_v2.convert_tf_saved_model(OUTPUT_TFDF_MODEL_PATH, OUTPUT_TFJS_MODEL_PATH)


run()
