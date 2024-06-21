import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from datetime import datetime

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MemorieSave")
        self.root.configure(bg="#2E2E2E")

        self.create_widgets()
        self.load_file_list()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg="#1E1E1E", fg="green", insertbackground="green")
        self.text_area.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.file_listbox = tk.Listbox(self.root, bg="#1E1E1E", fg="green")
        self.file_listbox.grid(row=1, column=0, sticky="ns", padx=10, pady=10)
        self.file_listbox.bind("<<ListboxSelect>>", self.load_selected_file)
        self.file_listbox.bind("<ButtonRelease-1>", self.load_selected_file)

        self.add_button = tk.Button(self.root, text="+", command=self.add_new_file, bg="#2E2E2E", fg="green", width=2)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.name_entry = tk.Entry(self.root, bg="#1E1E1E", fg="green", insertbackground="green")
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_file, bg="#2E2E2E", fg="green")
        self.save_button.grid(row=2, column=1, sticky="ew", padx=10)

        self.delete_button = tk.Button(self.root, text="Eliminar", command=self.delete_file, bg="#2E2E2E", fg="green")
        self.delete_button.grid(row=3, column=1, sticky="ew", padx=10)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def load_file_list(self):
        self.file_listbox.delete(0, tk.END)
        if not os.path.exists("notas"):
            os.makedirs("notas")
        for filename in os.listdir("notas"):
            if filename.endswith(".txt"):
                self.file_listbox.insert(tk.END, filename)

    def load_selected_file(self, event):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            with open(os.path.join("notas", selected_file), "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_file.replace(".txt", ""))

    def save_file(self):
        content = self.text_area.get(1.0, tk.END).strip()
        filename = self.name_entry.get().strip()

        if filename:
            if self.file_listbox.curselection():
                selected_file = self.file_listbox.get(tk.ACTIVE)
                if filename + ".txt" == selected_file:
                    filepath = os.path.join("notas", selected_file)
                    with open(filepath, "w") as file:
                        file.write(content)
                else:
                    self.save_as_new_file(content, filename)
            else:
                self.save_as_new_file(content, filename)
        else:
            messagebox.showwarning("Nombre del archivo", "Por favor, ingrese un nombre para el archivo.")

    def save_as_new_file(self, content, filename=None):
        if not filename:
            filename = simpledialog.askstring("Nombre del archivo", "Ingrese el nombre del archivo:")
        if filename:
            current_time = datetime.now().strftime("%d-%m-%Y")
            new_filename = f"{filename}_{current_time}.txt"
            filepath = os.path.join("notas", new_filename)
            with open(filepath, "w") as file:
                file.write(content)
            self.load_file_list()
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Nombre del archivo", "Por favor, ingrese un nombre válido para el archivo.")

    def add_new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.file_listbox.selection_clear(0, tk.END)

    def delete_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            confirm = messagebox.askyesno("Eliminar archivo", f"¿Está seguro de que desea eliminar {selected_file}?")
            if confirm:
                filepath = os.path.join("notas", selected_file)
                os.remove(filepath)
                self.load_file_list()
                self.text_area.delete(1.0, tk.END)
                self.name_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()

