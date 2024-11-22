import subprocess
import tkinter as tk
import os
import webbrowser
from tkinter import messagebox

CONFIG_FILE = "config.txt"

class TomcatController:
    def __init__(self, root):
        self.root = root

        # Crear la interfaz de usuario
        self.create_ui()

        # Cargar la ruta de Tomcat desde el archivo de configuración
        self.load_tomcat_path()

    def create_ui(self):
        self.label = tk.Label(self.root, text="Ruta de Tomcat:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.os_label = tk.Label(self.root, text="Seleccione el sistema operativo:")
        self.os_label.pack()

        self.os_listbox = tk.Listbox(self.root, height=2)
        self.os_listbox.insert(1, "Windows")
        self.os_listbox.insert(2, "Linux")
        self.os_listbox.pack()

        self.detect_button = tk.Button(self.root, text="Detectar Tomcat", command=self.detect_tomcat)
        self.detect_button.pack()

        self.start_button = tk.Button(self.root, text="Iniciar Tomcat", command=self.start_tomcat)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Detener Tomcat", command=self.stop_tomcat)
        self.stop_button.pack()

        self.open_cargue_war_button = tk.Button(self.root, text="Abrir Cargue War", command=self.open_cargue_war)
        self.open_cargue_war_button.pack()

    def load_tomcat_path(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.entry.insert(0, f.read())
        except FileNotFoundError:
            pass

    def save_tomcat_path(self):
        with open(CONFIG_FILE, 'w') as f:
            f.write(self.entry.get())

    def open_cargue_war(self):
        try:
            subprocess.Popen(["python3", "cargue_war.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def detect_tomcat(self):
        tomcat_path = self.entry.get()

        if not tomcat_path:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            tomcat_path = os.path.join(directorio_actual, 'tomcat')
            if not os.path.exists(tomcat_path):
                messagebox.showerror("Error", "La carpeta 'tomcat' no existe en la ruta actual.")
                return
            else:
                messagebox.showinfo("Éxito", "Carpeta 'tomcat' local encontrada.")
        else:
            if not os.path.exists(tomcat_path):
                messagebox.showerror("Error", "La ruta de Tomcat no es válida.")
                return

            try:
                selected_os = self.os_listbox.get(self.os_listbox.curselection())
            except tk.TclError:
                messagebox.showerror("Error", "Por favor, seleccione un sistema operativo.")
                return

            startup_script = "startup.bat" if selected_os == "Windows" else "startup.sh"
            startup_script_path = os.path.join(tomcat_path, 'bin', startup_script)

            if os.path.exists(startup_script_path):
                messagebox.showinfo("Detección de Tomcat", "Tomcat detectado en la ruta proporcionada.")
            else:
                messagebox.showerror("Error", f"No se encontró el script de inicio ({startup_script}) en la ruta proporcionada.")
                return

        # Guardar la ruta del Tomcat
        self.save_tomcat_path()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, tomcat_path)



    def start_tomcat(self):
        self.save_tomcat_path()
        tomcat_path = self.entry.get()

        if not os.path.exists(tomcat_path):
            messagebox.showerror("Error", "La ruta de Tomcat no es válida.")
            return

        try:
            selected_os = self.os_listbox.get(self.os_listbox.curselection())
        except tk.TclError:
            messagebox.showerror("Error", "Por favor, seleccione un sistema operativo.")
            return

        startup_script = "startup.bat" if selected_os == "Windows" else "startup.sh"
        startup_script_path = os.path.join(tomcat_path, 'bin', startup_script)

        if not os.path.exists(startup_script_path):
            messagebox.showerror("Error", f"No se encontró el script de inicio: {startup_script_path}")
            return

        try:
            subprocess.Popen([startup_script_path], cwd=os.path.join(tomcat_path, 'bin'))
            messagebox.showinfo("Éxito", "Tomcat iniciado correctamente.")
            # Abrir el navegador después de iniciar Tomcat
          #  webbrowser.open("http://localhost:8080")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el script: {e}")

    def stop_tomcat(self):
        self.save_tomcat_path()
        tomcat_path = self.entry.get()

        if not os.path.exists(tomcat_path):
            messagebox.showerror("Error", "La ruta de Tomcat no es válida.")
            return

        try:
            selected_os = self.os_listbox.get(self.os_listbox.curselection())
        except tk.TclError:
            messagebox.showerror("Error", "Por favor, seleccione un sistema operativo.")
            return

        shutdown_script = "shutdown.bat" if selected_os == "Windows" else "shutdown.sh"
        shutdown_script_path = os.path.join(tomcat_path, 'bin', shutdown_script)

        if not os.path.exists(shutdown_script_path):
            messagebox.showerror("Error", f"No se encontró el script de detención: {shutdown_script_path}")
            return

        try:
            subprocess.Popen([shutdown_script_path], cwd=os.path.join(tomcat_path, 'bin'))
            subprocess.Popen([shutdown_script_path], cwd=os.path.join(tomcat_path, 'bin'))
            messagebox.showinfo("Éxito", "Tomcat detenido correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el script: {e}")

def main():
    root = tk.Tk()
    root.geometry("300x250+300+300")
    root.title("Controlador de Tomcat")

    app = TomcatController(root)

    root.mainloop()

if __name__ == "__main__":
    main()
