import subprocess
from tkinter import messagebox

def listar_dispositivos(listbox_dispositivos):
    try:
        # Ejecutar el comando arp-scan y capturar la salida
        output = subprocess.check_output(["sudo", "arp-scan", "--localnet"])
        # Decodificar la salida y dividirla en líneas
        output_lines = output.decode("utf-8").split("\n")
        # Filtrar solo las líneas que contienen direcciones IP y direcciones MAC
        dispositivos = [line for line in output_lines if "." in line and ":" in line]
        # Limpiar el Listbox antes de mostrar los dispositivos
        listbox_dispositivos.delete(0, END)
        # Mostrar los dispositivos en el Listbox
        for dispositivo in dispositivos:
            listbox_dispositivos.insert(END, dispositivo)
    except Exception as e:
        messagebox.showerror("Error", "Error al listar dispositivos: " + str(e))

def desconectar_dispositivo(ip_seleccionada):
    try:
        # Ejecutar el comando iptables para bloquear el dispositivo
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip_seleccionada, "-j", "DROP"])
        subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-s", ip_seleccionada, "-j", "DROP"])
        messagebox.showinfo("Desconectado", f"Dispositivo {ip_seleccionada} desconectado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo desconectar el dispositivo: {str(e)}")

