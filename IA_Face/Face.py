import face_recognition
import cv2
import numpy as np
import os
from threading import Thread
import time

# Configuración
MAX_FAILED_ATTEMPTS = 5  # Número máximo de intentos fallidos antes de pedir la clave
UNLOCK_KEY = "1234"  # Clave de desbloqueo

# Cargar las imágenes de referencia del dueño
owner_images_path = "owner_images"
owner_encodings = []

for image_name in os.listdir(owner_images_path):
    image_path = os.path.join(owner_images_path, image_name)
    owner_image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(owner_image)
    if len(encodings) > 0:
        owner_encoding = encodings[0]
        owner_encodings.append(owner_encoding)
    else:
        print(f"Advertencia: No se encontró ningún rostro en {image_path}")

# Verificar que se hayan cargado codificaciones de rostro
if len(owner_encodings) == 0:
    raise ValueError("No se encontraron rostros en ninguna de las imágenes de referencia.")

# Inicializar la cámara
video_capture = cv2.VideoCapture(0)

authenticated = False
failed_attempts = 0

def authenticate():
    global authenticated, failed_attempts
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
                print("Usuario autenticado con éxito.")
                return

        failed_attempts += 1
        print(f"Intento fallido {failed_attempts} de {MAX_FAILED_ATTEMPTS}")
        if failed_attempts >= MAX_FAILED_ATTEMPTS:
            break

        time.sleep(1)

if __name__ == "__main__":
    auth_thread = Thread(target=authenticate)
    auth_thread.start()
    auth_thread.join()  # Esperar a que termine el hilo de autenticación

    if not authenticated:
        # Pedir clave de desbloqueo
        while not authenticated:
            unlock_key = input("Número máximo de intentos alcanzado. Ingresa la clave de desbloqueo: ")
            if unlock_key == UNLOCK_KEY:
                authenticated = True
                print("Clave correcta. Usuario autenticado.")
            else:
                print("Clave incorrecta. Inténtalo de nuevo.")

    video_capture.release()
    cv2.destroyAllWindows()
