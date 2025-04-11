# Environment: 4.22 tensorflow js python 3.11 linux

"""
Trains a Gradient Boosted Trees model using TensorFlow Decision Forests (TFDF)
for hand gesture classification based on landmark data.

This script performs the following steps:
1. Loads landmark data from a CSV file.
2. Splits the data into training and testing sets.
3. Converts the data into TensorFlow Datasets suitable for TFDF.
4. Initializes and trains a GradientBoostedTreesModel.
5. Evaluates the trained model on the test set using various metrics.
6. Saves the trained model in TensorFlow's SavedModel format.
7. Converts the SavedModel into the TensorFlow.js format for web deployment.
"""

import os
# Keep using Keras 2 - Required for compatibility with certain TF/TFJS versions
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import numpy as np
import pandas as pd
import tensorflow_decision_forests as tfdf
import tensorflowjs as tfjs

# --- Configuration Constants ---
DATASET_FILENAME = 'dataset.csv'
OUTPUT_TFDF_MODEL_PATH = 'model' # Directory to save the trained TFDF SavedModel
OUTPUT_TFJS_MODEL_PATH = 'tfjs' # Directory to save the converted TensorFlow.js model
RANDOM_SEED = 42
TRAIN_SIZE = 0.9

# Set the random seed for NumPy operations (like dataset splitting
np.random.seed(RANDOM_SEED)


def split_dataset(dataset, test_ratio=0.10):
    """
        Splits a Pandas DataFrame into training and testing sets based on a ratio.

        Args:
            dataset: The input Pandas DataFrame.
            test_ratio: The proportion of the dataset to allocate to the test set.

        Returns:
            A tuple containing the training DataFrame and the testing DataFrame.
        """

    test_indices = np.random.rand(len(dataset)) < test_ratio
    return dataset[~test_indices], dataset[test_indices]


def run():
    """Loads data, trains, evaluates, saves, and converts the TFDF model."""

    # Load the dataset from the specified CSV file
    dataset_df = pd.read_csv(DATASET_FILENAME)
    print(dataset_df.head(3))

    # Split the dataset into training and testing sets
    train_ds_pd, test_ds_pd = split_dataset(dataset_df, 1-TRAIN_SIZE)
    print("{} examples in training, {} examples for testing.".format(
        len(train_ds_pd), len(test_ds_pd)))

    # Convert the Pandas DataFrames into TensorFlow Datasets
    # The label column is specified as "label"
    train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(train_ds_pd, label="label")
    test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(test_ds_pd, label="label")

    # Configure the tuner.
    tuner = tfdf.tuner.RandomSearch(num_trials=50)
    tuner.choice("num_candidate_attributes_ratio", [0.6, 0.8, 1.0])
    tuner.choice("subsample", [0.7, 0.8, 0.9, 1.0])
    tuner.choice("min_examples", [1, 3, 5, 10, 15])

    tuner.choice("use_hessian_gain", [True, False])
    tuner.choice("num_trees", [100, 200, 300, 400])

    local_search_space = tuner.choice("growing_strategy", ["LOCAL"])
    local_search_space.choice("max_depth", [3, 4, 5, 6, 7])

    global_search_space = tuner.choice(
        "growing_strategy", ["BEST_FIRST_GLOBAL"], merge=True)
    global_search_space.choice("max_num_nodes", [16, 32, 64, 128, 256])

    SHRINKAGE_VALUE = 0.1  # Try 0.1, 0.05
    # Initialize the Gradient Boosted Trees model from TFDF
    # verbose=2 provides detailed logs during training
    model = tfdf.keras.GradientBoostedTreesModel(shrinkage=SHRINKAGE_VALUE, verbose=2, tuner=tuner)

    # Train the model on the training dataset
    model.fit(train_ds)

    # Compile the model with desired evaluation metrics
    model.compile(metrics=["accuracy"])
    # Evaluate the trained model on the test dataset
    evaluation = model.evaluate(test_ds, return_dict=True)

    print()
    for name, value in evaluation.items():
        print(f"{name}: {value:.4f}")

    # Save the trained model in TensorFlow's SavedModel format
    model.save(OUTPUT_TFDF_MODEL_PATH)

    # Convert the SavedModel to TensorFlow.js format
    tfjs.converters.tf_saved_model_conversion_v2.convert_tf_saved_model(OUTPUT_TFDF_MODEL_PATH, OUTPUT_TFJS_MODEL_PATH)


if __name__ == "__main__":
    print("Starting model training process...")
    run()
    print("\nModel training process finished.")

