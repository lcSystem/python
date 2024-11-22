import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def listar_archivos(directorio):
    """Listar los archivos visibles y ocultos en el directorio."""
    archivos_ocultos = []
    archivos_visibles = []
    for archivo in os.listdir(directorio):
        if archivo.startswith('.'):
            archivos_ocultos.append(archivo)
        else:
            archivos_visibles.append(archivo)
    actualizar_listas(archivos_visibles, archivos_ocultos)

def actualizar_listas(visibles, ocultos):
    """Actualizar los listboxes con los archivos visibles y ocultos."""
    lista_visibles.delete(0, tk.END)
    lista_ocultos.delete(0, tk.END)
    for archivo in visibles:
        lista_visibles.insert(tk.END, archivo)
    for archivo in ocultos:
        lista_ocultos.insert(tk.END, archivo)

def alternar_visibilidad(lista, ocultar):
    """Ocultar o mostrar el archivo/carpeta seleccionado según corresponda."""
    seleccion = lista.get(tk.ACTIVE)
    if seleccion:
        directorio = directorio_actual.get()
        origen = os.path.join(directorio, seleccion)
        if ocultar:
            destino = os.path.join(directorio, f".{seleccion}")
            mensaje = f"{seleccion} ahora está oculto."
        else:
            destino = os.path.join(directorio, seleccion[1:])
            mensaje = f"{seleccion} ahora es visible."
        os.rename(origen, destino)
        listar_archivos(directorio)
        messagebox.showinfo("Cambio de visibilidad", mensaje)

def seleccionar_directorio():
    """Abrir el diálogo para seleccionar un directorio."""
    ruta = filedialog.askdirectory()
    if ruta:
        directorio_actual.set(ruta)
        listar_archivos(ruta)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Archivos Ocultos")
ventana.geometry("700x500")
ventana.config(bg="#2E3440")

# Estilos para una interfaz moderna
estilo = ttk.Style()
estilo.theme_use('clam')
estilo.configure('TButton', background="#4C566A", foreground="#ECEFF4", font=("Helvetica", 12))
estilo.configure('TLabel', background="#2E3440", foreground="#D8DEE9", font=("Helvetica", 12))

directorio_actual = tk.StringVar()

# Widgets de la interfaz
ttk.Label(ventana, text="Directorio Actual:").pack(pady=10)
ttk.Entry(ventana, textvariable=directorio_actual, width=60).pack(pady=5)

ttk.Button(ventana, text="Seleccionar Directorio", command=seleccionar_directorio).pack(pady=10)

# Listas de archivos visibles y ocultos
ttk.Label(ventana, text="Archivos y Carpetas Visibles").pack(pady=5)
lista_visibles = tk.Listbox(ventana, width=60, height=8)
lista_visibles.pack(pady=5)

ttk.Label(ventana, text="Archivos y Carpetas Ocultos").pack(pady=5)
lista_ocultos = tk.Listbox(ventana, width=60, height=8)
lista_ocultos.pack(pady=5)

# Botones de acción
frame_botones = tk.Frame(ventana, bg="#2E3440")
frame_botones.pack(pady=20)

ttk.Button(frame_botones, text="Ocultar Selección", 
           command=lambda: alternar_visibilidad(lista_visibles, ocultar=True)).grid(row=0, column=0, padx=10)
ttk.Button(frame_botones, text="Mostrar Selección", 
           command=lambda: alternar_visibilidad(lista_ocultos, ocultar=False)).grid(row=0, column=1, padx=10)

# Ejecutar la aplicación
ventana.mainloop()

