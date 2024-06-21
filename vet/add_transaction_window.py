import tkinter as tk
from tkinter import ttk, messagebox
from logic import add_transaction

def open_add_transaction_window(root, load_transactions, update_totals):
    window = tk.Toplevel(root)
    window.title("Añadir Transacción")
    window.geometry("400x300")
    window.configure(bg='#e0f7fa')

    # Estilo de los widgets
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=10)
    style.configure("TLabel", font=("Arial", 10), background='#e0f7fa')
    style.configure("TEntry", font=("Arial", 10))
    style.configure("TFrame", background='#e0f7fa')

    frame = ttk.Frame(window)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Tipo de transacción
    var_transaction_type = tk.StringVar(value="Ingreso")
    radio_ingreso = ttk.Radiobutton(frame, text="Ingreso", variable=var_transaction_type, value="ingreso")
    radio_gasto = ttk.Radiobutton(frame, text="Gasto", variable=var_transaction_type, value="gasto")
    radio_ingreso.grid(row=0, column=0, padx=5, pady=5)
    radio_gasto.grid(row=0, column=1, padx=5, pady=5)

    # Campo para el nombre
    label_name = ttk.Label(frame, text="Nombre:")
    entry_name = ttk.Entry(frame)
    label_name.grid(row=1, column=0, padx=5, pady=5)
    entry_name.grid(row=1, column=1, padx=5, pady=5)

    # Monto
    label_amount = ttk.Label(frame, text="Monto:")
    entry_amount = ttk.Entry(frame)
    label_amount.grid(row=2, column=0, padx=5, pady=5)
    entry_amount.grid(row=2, column=1, padx=5, pady=5)

    # Descripción
    label_description = ttk.Label(frame, text="Descripción:")
    entry_description = ttk.Entry(frame)
    label_description.grid(row=3, column=0, padx=5, pady=5)
    entry_description.grid(row=3, column=1, padx=5, pady=5)

    # Botón para añadir transacción
    def add_transaction_event():
        try:
            name = entry_name.get()
            amount = float(entry_amount.get())
            description = entry_description.get()
            if var_transaction_type.get() == "ingreso":
                add_transaction("ingreso", amount, description, name)
            else:
                add_transaction("gasto", amount, description, name)
            entry_name.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            entry_description.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Transacción añadida exitosamente")
            load_transactions()
            update_totals()  # Actualizar los totales
            window.destroy()  # Cerrar la ventana después de añadir la transacción
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un monto válido")

    button_add = ttk.Button(frame, text="Añadir", command=add_transaction_event)
    button_add.grid(row=4, column=0, columnspan=2, pady=10)

    window.mainloop()

