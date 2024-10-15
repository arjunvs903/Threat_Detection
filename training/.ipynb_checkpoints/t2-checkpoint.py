import cv2

def get_available_cameras():
    available_cameras = []

    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        else:
            available_cameras.append(index)
            cap.release()
        index += 1

    return available_cameras

if __name__ == "__main__":
    cameras = get_available_cameras()
    if cameras:
        print("Available cameras:")
        for idx in cameras:
            print(f"Camera {idx}")
    else:
        print("No cameras found.")
