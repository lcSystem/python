import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import subprocess

def listar_dispositivos():
    try:
        # Ejecutar el comando arp-scan y capturar la salida
        output = subprocess.check_output(["sudo", "arp-scan", "--localnet"])
        # Decodificar la salida y dividirla en líneas
        output_lines = output.decode("utf-8").split("\n")
        # Filtrar solo las líneas que contienen direcciones IP y direcciones MAC
        dispositivos = [line for line in output_lines if "." in line and ":" in line]
        # Limpiar el área de texto antes de mostrar los dispositivos
        text_area.delete("1.0", tk.END)
        # Mostrar los dispositivos en el cuadro de texto
        for dispositivo in dispositivos:
            text_area.insert(tk.END, dispositivo + "\n")
    except Exception as e:
        messagebox.showerror("Error", "Error al listar dispositivos: " + str(e))

def desconectar_dispositivo():
    # Obtener el texto seleccionado
    seleccion = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
    # Si no hay texto seleccionado, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
        return
    # Obtener la dirección IP del dispositivo seleccionado
    ip_seleccionada = seleccion.split()[0]
    try:
        # Ejecutar el comando arp-scan para desconectar el dispositivo
        subprocess.run(["sudo", "arp-scan", "-interface", "INTERFACE", "-I", ip_seleccionada, "-s", "0.0.0.0", "-t", "1"])
        messagebox.showinfo("Desconectado", f"Dispositivo {ip_seleccionada} desconectado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo desconectar el dispositivo: {str(e)}")

# Configuración de la ventana
window = tk.Tk()
window.title("Lista de Dispositivos de Red")

# Crear un área de texto desplazable para mostrar los dispositivos
text_area = scrolledtext.ScrolledText(window, width=50, height=20, wrap=tk.WORD)
text_area.pack(expand=True, fill='both')

# Botón para listar dispositivos
list_button = tk.Button(window, text="Listar Dispositivos", command=listar_dispositivos)
list_button.pack(pady=10)

# Botón para desconectar dispositivo
disconnect_button = tk.Button(window, text="Desconectar Dispositivo", command=desconectar_dispositivo)
disconnect_button.pack(pady=10)

# Ejecutar la ventana
window.mainloop()

