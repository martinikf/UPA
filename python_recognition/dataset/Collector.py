import os

import cv2
import mediapipe as mp


# MediaPipe Hands constants
STATIC_IMAGE_MODE = False
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# BUFFER constants
FRAME_BUFFER_SIZE = 5  # Capacity of buffer, when key is pressed the most recent usable frame is used
frame_buffer = []

# CROP constants
CROP = True  # If True, crop the hand region and resize to target size. If False, use the whole frame
TARGET_SIZE = (250, 250)  # Target size for cropped image
PADDING = 50  # Padding around hand in pixels


# Global variable for MediaPipe Hands
hands = None


def setup_mediapipe():
    global hands
    hands = mp.solutions.hands.Hands(
        static_image_mode=STATIC_IMAGE_MODE,
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )

    if hands is None:
        raise "Error: Could not initialize MediaPipe Hands"


def keydown(key):
    global hands

    label = key_to_label(key)
    print(f"Key pressed: {key} ({label})")

    # Find most recent frame where hands are detected
    best_frame = None

    for frame in reversed(frame_buffer):  # Reverse to get the most recent frame
        results = process_frame(frame)
        if results.multi_hand_landmarks:
            best_frame = frame

            if CROP:
                best_frame = crop_frame(best_frame, results)
                if best_frame is None:
                    continue  # Skip this frame if hand is not in cropped image
                print("Hand detected in cropped image")

            break

    if best_frame is None:
        return

    # Save image
    save(best_frame, label)


def crop_frame(frame, best_results):
    x_min, y_min, x_max, y_max = get_box(frame, best_results)
    cropped = frame[y_min:y_max, x_min:x_max]
    resized = cv2.resize(cropped, TARGET_SIZE)

    # Check if hand is detected in the cropped image
    result = hands.process(resized)
    if not result.multi_hand_landmarks:
        print("Hand detected, but not in the cropped image")
        return None

    return resized


def get_box(frame, results):
    frame_height, frame_width, _ = frame.shape
    x_coordinates = []
    y_coordinates = []

    # Get all landmark coordinates
    for landmark in results.multi_hand_landmarks[0].landmark:
        x_coordinates.append(min(int(landmark.x * frame_width), frame_width - 1))
        y_coordinates.append(min(int(landmark.y * frame_height), frame_height - 1))

    # Calculate bounding box with padding
    x_min = max(min(x_coordinates) - PADDING, 0)
    x_max = min(max(x_coordinates) + PADDING, frame_width)
    y_min = max(min(y_coordinates) - PADDING, 0)
    y_max = min(max(y_coordinates) + PADDING, frame_height)

    # Make the crop square
    width = x_max - x_min
    height = y_max - y_min
    size = max(width, height)

    # Adjust coordinates to make square crop
    x_center = (x_min + x_max) // 2
    y_center = (y_min + y_max) // 2

    x_min = max(x_center - size // 2, 0)
    x_max = min(x_center + size // 2, frame_width)
    y_min = max(y_center - size // 2, 0)
    y_max = min(y_center + size // 2, frame_height)

    return x_min, y_min, x_max, y_max


def key_to_label(key):
    key = key.lower()
    if not key.isalnum() and key not in ['+', '-']:
        raise "Invalid key was pressed"

    if key == '+':
        key = 'ch'
    elif key == '-':
        key = 'none'
    return key


def save(frame, label):
    directory = f"dataset/{label}"
    os.makedirs(directory, exist_ok=True)

    file_count = len([name for name in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory, name))])

    cv2.imwrite(f"{directory}/{file_count + 1}.jpg", frame)

    print(f"Saved image to {directory}/{file_count + 1}.jpg")


def process_frame(frame):
    global hands
    # Convert frame to RGB for mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    return results


def loop():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()

        # Flip frame
        frame = cv2.flip(frame, 1)

        if not ret:
            print("Error: Could not read frame.")
            break

        add_to_buffer(frame)

        # Show frame
        cv2.imshow('Webcam Feed', frame)

        # Check for ESC key to exit
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            break
        elif (65 <= key <= 90) or (97 <= key <= 122) or key == 43 or key == 45:  # A-Z, a-z, +, -
            keydown(chr(key))

    cap.release()
    cv2.destroyAllWindows()


def add_to_buffer(frame):
    global frame_buffer
    frame_buffer.append(frame.copy())
    if len(frame_buffer) > FRAME_BUFFER_SIZE:
        frame_buffer = frame_buffer[1:]


setup_mediapipe()
loop()
