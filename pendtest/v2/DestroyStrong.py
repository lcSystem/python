import tkinter as tk
from tkinter import scrolledtext, messagebox
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

def mostrar_dispositivo_seleccionado(event):
    try:
        # Obtener la línea seleccionada
        seleccion = text_area.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        # Limpiar la caja de información
        info_area.delete("1.0", tk.END)
        # Mostrar la información del dispositivo seleccionado
        info_area.insert(tk.END, seleccion)
    except tk.TclError:
        pass

def desconectar_dispositivo():
    # Obtener el texto seleccionado
    seleccion = info_area.get("1.0", tk.END).strip()
    # Si no hay texto seleccionado, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
        return
    # Obtener la dirección IP del dispositivo seleccionado
    ip_seleccionada = seleccion.split()[0]
    try:
        # Ejecutar el comando iptables para bloquear el dispositivo
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip_seleccionada, "-j", "DROP"])
        subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-s", ip_seleccionada, "-j", "DROP"])
        messagebox.showinfo("Desconectado", f"Dispositivo {ip_seleccionada} desconectado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo desconectar el dispositivo: {str(e)}")

# Configuración de la ventana
window = tk.Tk()
window.title("Lista de Dispositivos de Red")

# Configuración de estilos terroríficos
window.configure(bg="black")

# Crear una caja de texto para mostrar la información del dispositivo seleccionado
info_area = tk.Text(window, height=1, wrap=tk.WORD, bg="black", fg="red", font=("Helvetica", 12, "bold"))
info_area.pack(pady=5, padx=10, expand=True, fill='both')

# Crear un área de texto desplazable para mostrar los dispositivos
text_area = scrolledtext.ScrolledText(window, width=70, height=15, wrap=tk.WORD, bg="black", fg="white", font=("Helvetica", 12))
text_area.pack(pady=5, padx=10, expand=True, fill='both')

# Asociar el evento de selección de texto con la función mostrar_dispositivo_seleccionado
text_area.bind("<<Selection>>", mostrar_dispositivo_seleccionado)

# Botón para listar dispositivos
list_button = tk.Button(window, text="Listar Dispositivos", command=listar_dispositivos, bg="red", fg="black", font=("Helvetica", 12, "bold"))
list_button.pack(pady=10)

# Botón para desconectar dispositivo
disconnect_button = tk.Button(window, text="Desconectar Dispositivo", command=desconectar_dispositivo, bg="red", fg="black", font=("Helvetica", 12, "bold"))
disconnect_button.pack(pady=10)

# Ejecutar la ventana
window.mainloop()

