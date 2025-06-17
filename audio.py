import datetime
import os
import cv2
import numpy as np
import speech_recognition as sr
import threading
import pyaudio
import wave

# Shared voice command variable
voice_command = None
listening = False

def listen_command():
    global voice_command, listening
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for command: 'hello' or 'exit'")
        try:
            audio = recognizer.listen(source, phrase_time_limit=3)
            voice_command = recognizer.recognize_google(audio).lower()
            print(f"You said: {voice_command}")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Error with the recognition service.")
        finally:
            listening = False  # Mark listening complete

def SnapShot():
    global voice_command, listening

    # Start webcam
    camera_snapshot = cv2.VideoCapture(0)

    if not camera_snapshot.isOpened():
        print("Error: Cannot open webcam.")
        return

    print("\nSay 'hello' to take snapshot or 'exit' to quit\n")
    print("Or press 's' to take snapshot manually, 'q' to quit.\n")

    # Output path
    image_output_path = "Output/Images/"
    if not os.path.exists(image_output_path):
        os.makedirs(image_output_path)

    while True:
        ret, frame = camera_snapshot.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Show webcam frame
        cv2.imshow("OpenCV SnapShot with Voice", frame)

        # Start voice thread only if not already listening
        if not listening:
            listening = True
            threading.Thread(target=listen_command, daemon=True).start()

        # Check keyboard input
        key = cv2.waitKey(1) & 0xFF

        # Handle voice command or key press
        if voice_command == "hello" or key == ord('s'):
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
            filepath = os.path.join(image_output_path, filename)
            cv2.imwrite(filepath, frame)
            print(f"📸 Snapshot saved: {filepath}")
            voice_command = None

        elif voice_command == "exit" or key == ord('q'):
            print("👋 Exiting...")
            break

    # Clean up
    #camera_snapshot.release()
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    SnapShot()
