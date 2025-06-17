import datetime
import os
import cv2
import numpy as np

def SnapShot():
    camera_snapshot = cv2.VideoCapture(0)

    if not camera_snapshot.isOpened():
        print("Error: Cannot open webcam.")
        return

    print("\n🖐 Move your hand to take a snapshot.")
    print("❌ Press 'q' to quit.\n")

    image_output_path = "Output/Images/"
    os.makedirs(image_output_path, exist_ok=True)

    backSub = cv2.createBackgroundSubtractorMOG2()

    photo_timer = 0
    photo_taken = False

    while True:
        ret, frame = camera_snapshot.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        fg_mask = backSub.apply(frame)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        gesture_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if w > 100 and h > 100:
                gesture_detected = True
                photo_timer += 1
                if photo_timer >= 10 and not photo_taken:
                    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
                    filepath = os.path.join(image_output_path, filename)
                    cv2.imwrite(filepath, frame)
                    print(f"📸 Snapshot saved: {filepath}")
                    photo_taken = True
                    photo_timer = 0

        if not gesture_detected:
            photo_timer = 0
            photo_taken = False

        cv2.imshow("🖼️ SnapShot - Press 'q' to quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("👋 Exiting...")
            break

    camera_snapshot.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    SnapShot()
