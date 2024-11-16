import os
import copy
import itertools

import cv2
import mediapipe as mp


# MediaPipe Hands constants
STATIC_IMAGE_MODE = False
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6


LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'ch', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
          'v', 'w', 'x', 'y', 'z', 'none']


def run():
    offset_path = "./dataset/"
    output_file = offset_path + "processed_dataset.csv"
    hands = setup()

    with open(output_file, "w") as f:
        f.write("letter_id,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42\n")
        for i, letter in enumerate(LABELS):
            if not os.path.exists(offset_path + letter):
                continue
            for file in get_files(offset_path + letter):
                data = process_image(hands, offset_path + letter + '/' + file)
                print(data)
                if data:
                    f.write(f"{i},")
                    for index, num in enumerate(data):
                        if(index == len(data) - 1):
                            f.write(f"{num}")
                        else:
                            f.write(f"{num},")
                    f.write("\n")
                print(f"Processed {letter}/{file}")


def setup():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=STATIC_IMAGE_MODE,
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )
    return hands


def get_files(directory):
    for dir_file in os.listdir(directory):
        if dir_file.endswith(".jpg"):
            yield dir_file


def calc_landmark_list(image, landmarks):
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


run()
