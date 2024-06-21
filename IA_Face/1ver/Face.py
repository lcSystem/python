import face_recognition
import cv2
import numpy as np
import os
from Xlib import display, X
from Xlib.ext.xtest import fake_input
from threading import Thread
import time

# Cargar la imagen de referencia del dueño
owner_image = face_recognition.load_image_file("owner.jpg")
owner_encoding = face_recognition.face_encodings(owner_image)[0]

# Inicializar la cámara
video_capture = cv2.VideoCapture(0)

def block_input():
    d = display.Display()
    root = d.screen().root

    while not authenticated:
        root.grab_pointer(True, X.ButtonPressMask, X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE, X.CurrentTime)
        root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
        time.sleep(1)
        fake_input(d, X.KeyPress, 0)

authenticated = False

def authenticate():
    global authenticated
    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([owner_encoding], face_encoding)
            if match[0]:
                authenticated = True
                return

        time.sleep(1)

if __name__ == "__main__":
    Thread(target=block_input).start()
    Thread(target=authenticate).start()

    while not authenticated:
        pass

    video_capture.release()
    cv2.destroyAllWindows()

