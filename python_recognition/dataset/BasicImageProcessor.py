"""
Processes image datasets of hand gestures to extract and normalize MediaPipe landmarks.

This script iterates through specified dataset directories, reads image files,
detects hand landmarks using MediaPipe Hands, preprocesses these landmarks
(calculates relative coordinates, normalizes), and saves the resulting feature
vectors along with their corresponding labels into a single CSV file suitable
for training machine learning models.

Input: Image files (.jpg) organized in subdirectories named after labels (e.g., 'a', 'b', 'ch').
Output: A CSV file ('processed_dataset.csv') with columns: 'label' (numeric index), 'f1'...'f42' (normalized landmark features).
"""

import os
import copy
import itertools

import cv2
import mediapipe as mp


# --- MediaPipe Hands Configuration Constants ---
STATIC_IMAGE_MODE = False
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# --- Label Mapping ---
LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'ch', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
          'v', 'w', 'x', 'y', 'z', 'none']


def run():
    """
       Main function to orchestrate the dataset processing pipeline.
       Iterates through datasets, processes images, and writes features to CSV.
    """
     # List of directories containing the input image datasets
    datasets = ["./dataset_f_left_100perSign/",
                "./dataset_f_right_100perSign/",
                "./dataset_m_left_25perSign/",
                "./dataset_m_right_25perSign/"]

    # Output CSV file path
    output_file = "./processed_dataset.csv"

    # Initialize MediaPipe Hands
    hands = setup()

    # Open the output file in write mode
    with open(output_file, "w") as f:
        # Write the CSV header row (label + 42 features)
        f.write("label,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42\n")

        # Iterate through each dataset directory path
        for offset_path in datasets:
             # Iterate through each label
            for i, letter in enumerate(LABELS):
                if not os.path.exists(offset_path + letter):
                    continue

                # Process each image file found in the label subdirectory
                for file in get_files(offset_path + letter):
                    # Extract and preprocess landmarks from the image
                    data = process_image(hands, offset_path + letter + '/' + file)
                    print(data)
                    if data:
                        # Write the label index and the 42 features to the CSV
                        f.write(f"{i},")
                        for index, num in enumerate(data):
                            if(index == len(data) - 1):
                                f.write(f"{num}")
                            else:
                                f.write(f"{num},")
                        f.write("\n")
                    print(f"Processed {letter}/{file}")


def setup():
    """
        Initializes and returns the MediaPipe Hands solution object.
        Uses constants defined at the module level for configuration.
    """
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=STATIC_IMAGE_MODE,
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )
    return hands


def get_files(directory):
    """
        Generator function to yield filenames ending with '.jpg' from a given directory.

        Args:
            directory: The path to the directory to scan.

        Yields:
            Filenames ending with '.jpg'.
    """
    for dir_file in os.listdir(directory):
        if dir_file.endswith(".jpg"):
            yield dir_file


def calc_landmark_list(image, landmarks):
    """
        Converts MediaPipe landmarks into
        absolute pixel coordinates based on the image dimensions.

        Args:
            image: The input image (NumPy array).
            landmarks: The LandmarkList object from MediaPipe results.

        Returns:
            A list of [x, y] coordinates for each landmark in pixels.
    """
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    """
        Preprocesses the list of landmark pixel coordinates.
        1. Calculates coordinates relative to the wrist (landmark 0) for translation invariance.
        2. Flattens the list of [x, y] pairs into a single vector [x0, y0, x1, y1, ...].
        3. Normalizes the vector by dividing all values by the maximum absolute value

        Args:
            landmark_list: A list of [x, y] pixel coordinates for the hand landmarks.

        Returns:
            A list of 42 floating-point numbers representing the normalized feature vector.
    """
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def process_image(hands_arg, file_path):
    """
        Loads an image file, detects hand landmarks using MediaPipe, calculates
        pixel coordinates, preprocesses them (relative coords, normalization),
        and returns the final feature vector.

        Args:
            hands_arg: The initialized MediaPipe Hands object.
            file_path: The path to the image file.

        Returns:
            A list of 42 normalized landmark features if a hand is detected,
            otherwise None.
    """
    img = cv2.imread(file_path)
    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands_arg.process(img)

    if not results.multi_hand_landmarks:
        print(f"No hand landmarks detected: {file_path}")
        return None

    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
        landmark_list = calc_landmark_list(img, hand_landmarks)
        return pre_process_landmark(landmark_list)


if __name__ == "__main__":
    run()

