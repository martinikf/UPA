import os

import cv2
import mediapipe as mp

STATIC_IMAGE_MODE = False
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

FRAME_BUFFER_SIZE = 5
frame_buffer = []

hands = None


def setup_mediapipe():
    global hands
    hands = mp.solutions.hands.Hands(
        static_image_mode=STATIC_IMAGE_MODE,
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )


def keydown(key):
    global hands

    label = key_to_label(key)

    # Find most recent frame where hands are detected
    best_frame = None
    for frame in reversed(frame_buffer):  # Reverse to get the most recent frame
        results = process_frame(frame)
        if results.multi_hand_landmarks:
            best_frame = frame
            break

    if best_frame is None:
        return

    # Save image
    save(best_frame, label)


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


def process_frame(frame):
    global hands
    # Flip frame
    frame = cv2.flip(frame, 1)

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
        elif (65 <= key <= 90) or (97 <= key <= 122) or key == 43 or key == 45:
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
