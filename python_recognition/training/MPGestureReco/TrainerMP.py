# !pip install mediapipe-model-maker

import tensorflow as tf
# assert tf.__version__.startswith('2'), "TensorFlow version 2.x is required."

from mediapipe_model_maker import gesture_recognizer


dataset_path = "./dataset/"

hparams_dataload = gesture_recognizer.HandDataPreprocessingParams()

data = gesture_recognizer.Dataset.from_folder(
    dirname=dataset_path,
    hparams=hparams_dataload
)

train_data, rest_data = data.split(0.9)
validation_data, test_data = rest_data.split(0.5)

hparams_train = gesture_recognizer.HParams(export_dir="exported_gesture_model")

options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams_train)

model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options
)


loss, accuracy = model.evaluate(test_data, batch_size=1)

print(f"\n--- Evaluation Results ---")
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")


model.export_model()
