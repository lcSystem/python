import face_recognition
import cv2
import numpy as np
import os
from Xlib import display, X
from Xlib.ext.xtest import fake_input
from threading import Thread
import time

# Cargar las imágenes de referencia del dueño
owner_images_path = "owner_images"
owner_encodings = []

for image_name in os.listdir(owner_images_path):
    image_path = os.path.join(owner_images_path, image_name)
    owner_image = face_recognition.load_image_file(image_path)
    owner_encoding = face_recognition.face_encodings(owner_image)[0]
    owner_encodings.append(owner_encoding)

# Inicializar la cámara
video_capture = cv2.VideoCapture(0)

authenticated = False

def block_input():
    d = display.Display()
    root = d.screen().root

    while not authenticated:
        root.grab_pointer(True, X.ButtonPressMask, X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE, X.CurrentTime)
        root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
        time.sleep(1)
        fake_input(d, X.KeyPress, 0)

def authenticate():
    global authenticated
    while not authenticated:
        ret, frame = video_capture.read()
        if not ret:
            continue
        
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(owner_encodings, face_encoding)
            if True in matches:
                authenticated = True
                return

        time.sleep(1)

if __name__ == "__main__":
    block_thread = Thread(target=block_input)
    auth_thread = Thread(target=authenticate)

    block_thread.start()
    auth_thread.start()

    auth_thread.join()  # Esperar a que termine el hilo de autenticación

    video_capture.release()
    cv2.destroyAllWindows()

    # Liberar el bloqueo de entrada
    d = display.Display()
    root = d.screen().root
    root.ungrab_pointer(X.CurrentTime)
    root.ungrab_keyboard(X.CurrentTime)

