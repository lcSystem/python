import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import webbrowser

CONFIG_FILE = "config.txt"

class WarManager:
    def __init__(self, root):
        self.root = root

        # Crear la interfaz de usuario
        self.create_ui()

    def create_ui(self):
        # Frame principal para organizar los elementos
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20)

        # Etiqueta y entrada para la ruta de Tomcat
        self.label = tk.Label(main_frame, text="Ruta de Tomcat:")
        self.label.grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.entry = tk.Entry(main_frame, width=40)
        self.entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))

        # Botón para cargar WAR
        self.load_button = tk.Button(main_frame, text="Cargar WAR", command=self.load_war)
        self.load_button.grid(row=0, column=2, padx=(0, 5))

        # Botón para listar WARs
        self.list_button = tk.Button(main_frame, text="Listar WARs", command=self.list_wars, bg="lightblue")
        self.list_button.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        # Botón para eliminar WAR seleccionado
        self.delete_button = tk.Button(main_frame, text="Eliminar WAR Seleccionado", command=self.delete_war, bg="lightcoral")
        self.delete_button.grid(row=1, column=1, sticky="ew", pady=(10, 0))

        # Listbox para mostrar WARs
        self.war_listbox = tk.Listbox(main_frame, width=60)
        self.war_listbox.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Botón para lanzar WAR
        self.launch_button = tk.Button(main_frame, text="Lanzar", command=self.launch_war)
        self.launch_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        # Cargar la ruta de Tomcat desde el archivo de configuración
        self.load_tomcat_path()

    def load_tomcat_path(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                tomcat_path = f.readline().strip()
                self.entry.insert(0, tomcat_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de configuración.")

    def load_war(self):
        tomcat_path = self.entry.get()
        if not os.path.exists(tomcat_path):
            messagebox.showerror("Error", "La ruta de Tomcat no es válida.")
            return

        webapps_path = os.path.join(tomcat_path, 'webapps')
        if not os.path.exists(webapps_path):
            messagebox.showerror("Error", "La ruta de webapps no es válida.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("WAR files", "*.war")])
        if file_path:
            try:
                shutil.copy(file_path, webapps_path)
                messagebox.showinfo("Éxito", "Archivo WAR cargado correctamente.")
                self.list_wars()  # Actualizar la lista de WARs
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo WAR: {e}")

    def list_wars(self):
        tomcat_path = self.entry.get()
        webapps_path = os.path.join(tomcat_path, 'webapps')
        if not os.path.exists(webapps_path):
            messagebox.showerror("Error", "La ruta de webapps no es válida.")
            return

        wars = [f for f in os.listdir(webapps_path) if f.endswith('.war')]

        self.war_listbox.delete(0, tk.END)
        for war in wars:
            self.war_listbox.insert(tk.END, war)

    def delete_war(self):
        tomcat_path = self.entry.get()
        webapps_path = os.path.join(tomcat_path, 'webapps')
        if not os.path.exists(webapps_path):
            messagebox.showerror("Error", "La ruta de webapps no es válida.")
            return

        try:
            selected_war = self.war_listbox.get(self.war_listbox.curselection())
            war_path = os.path.join(webapps_path, selected_war)
            os.remove(war_path)
            messagebox.showinfo("Éxito", "Archivo WAR eliminado correctamente.")
            self.list_wars()  # Actualizar la lista de WARs
        except tk.TclError:
            messagebox.showerror("Error", "Por favor, seleccione un archivo WAR para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el archivo WAR: {e}")

    def launch_war(self):
        selected_war = self.war_listbox.get(self.war_listbox.curselection())
        if not selected_war:
            messagebox.showerror("Error", "Por favor, seleccione un archivo WAR para lanzar.")
            return

        tomcat_path = self.entry.get()
        war_url = f"http://localhost:8080/{selected_war.split('.war')[0]}"
        webbrowser.open(war_url)

def main():
    root = tk.Tk()
    root.title("Gestor de WARs para Tomcat")
    root.geometry("700x350+300+300")
    app = WarManager(root)

    root.mainloop()

if __name__ == "__main__":
    main()
