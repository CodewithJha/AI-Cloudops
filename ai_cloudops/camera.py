from typing import List
import cv2


def apply_filter(frame, filter_type: str):
    if filter_type == "grayscale":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if filter_type == "invert":
        return cv2.bitwise_not(frame)
    return frame


def filter_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    filters: List[str] = ["original", "grayscale", "invert"]
    current_filter_index = 0

    print("Press 's' to switch filter, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame.")
            break

        current_filter = filters[current_filter_index]
        filtered_frame = apply_filter(frame, current_filter)
        cv2.imshow("Filtered", filtered_frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if key == ord("s"):
            current_filter_index = (current_filter_index + 1) % len(filters)

    cap.release()
    cv2.destroyAllWindows()

