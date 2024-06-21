import tkinter as tk
from tkinter import ttk
import keyboard
import mouse
import time
import threading

# Variable para definir el tiempo de bloqueo en minutos
BLOCK_TIME_MINUTES = 1  # Cambia este valor para configurar el tiempo de bloqueo

def block_inputs():
    keyboard.hook(block=True)  # Bloquea todas las teclas usando el método hook de keyboard
    mouse.hook(block=True)     # Bloquea el ratón usando el método hook de mouse

def unblock_inputs():
    keyboard.unhook_all()  # Desbloquea todas las teclas
    mouse.unhook_all()     # Desbloquea el ratón

def countdown_timer(minutes, label):
    seconds = minutes * 60
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        label.config(text=time_format)
        root.update()
        time.sleep(1)
    label.config(text='00:00')
    unblock_inputs()

def start_blocking():
    block_inputs()
    threading.Thread(target=countdown_timer, args=(BLOCK_TIME_MINUTES, label)).start()
    label.config(text=f'Bloqueado por {BLOCK_TIME_MINUTES} minutos')

# Función para configurar el estilo de la ventana principal
def set_window_style(root):
    root.title("Bloqueo de Teclado y Ratón")
    root.geometry("300x200")
    root.configure(bg='white')  # Fondo blanco para hacerlo más interactivo

# Configurar la ventana de Tkinter
root = tk.Tk()
set_window_style(root)

# Etiqueta de la cuenta regresiva
label = ttk.Label(root, font=("Helvetica", 48))
label.pack(pady=20)

# Botón para iniciar el bloqueo
button_style = ttk.Style()
button_style.configure('Custom.TButton', foreground='blue', background='lightblue', font=('Helvetica', 12, 'bold'))
button = ttk.Button(root, text="Iniciar Bloqueo", style='Custom.TButton', command=start_blocking)
button.pack(pady=10)

root.mainloop()
