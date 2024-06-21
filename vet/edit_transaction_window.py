import tkinter as tk
from tkinter import ttk, messagebox
from logic import read_transactions, update_transaction, add_transaction_to_history

def open_edit_transaction_window(root, selected_index, load_transactions, update_totals):
    transactions = read_transactions()
    transaction = transactions[selected_index]
    transaction_type, amount, description, name, date = transaction

    window = tk.Toplevel(root)
    window.title("Editar Transacción")
    window.geometry("400x350")
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
    var_transaction_type = tk.StringVar(value=transaction_type)
    radio_ingreso = ttk.Radiobutton(frame, text="Ingreso", variable=var_transaction_type, value="ingreso", state=tk.DISABLED)
    radio_gasto = ttk.Radiobutton(frame, text="Gasto", variable=var_transaction_type, value="gasto", state=tk.DISABLED)
    radio_ingreso.grid(row=0, column=0, padx=5, pady=5)
    radio_gasto.grid(row=0, column=1, padx=5, pady=5)

    # Campo para el nombre
    label_name = ttk.Label(frame, text="Nombre:")
    entry_name = ttk.Entry(frame, state=tk.DISABLED)
    entry_name.insert(0, name)
    label_name.grid(row=1, column=0, padx=5, pady=5)
    entry_name.grid(row=1, column=1, padx=5, pady=5)

    # Monto
    label_amount = ttk.Label(frame, text="Monto:")
    entry_amount = ttk.Entry(frame, state=tk.DISABLED)
    entry_amount.insert(0, str(amount))
    label_amount.grid(row=2, column=0, padx=5, pady=5)
    entry_amount.grid(row=2, column=1, padx=5, pady=5)

    # Descripción
    label_description = ttk.Label(frame, text="Descripción:")
    entry_description = ttk.Entry(frame)
    entry_description.insert(0, description)
    label_description.grid(row=3, column=0, padx=5, pady=5)
    entry_description.grid(row=3, column=1, padx=5, pady=5)

    # Botón para editar transacción
    def edit_transaction_event():
        try:
            new_description = entry_description.get()
            update_transaction(selected_index, transaction_type, amount, new_description, name)
            messagebox.showinfo("Éxito", "Transacción editada exitosamente")
            load_transactions()
            update_totals()
            window.destroy()  # Cerrar la ventana después de editar la transacción
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un monto válido")

    button_edit = ttk.Button(frame, text="Editar", command=edit_transaction_event)
    button_edit.grid(row=4, column=0, columnspan=2, pady=10)

    # Botón para abonar
    def abonar_event():
        abonar_window = tk.Toplevel(window)
        abonar_window.title("Abonar")
        abonar_window.geometry("300x150")

        label_monto = ttk.Label(abonar_window, text="Monto:")
        entry_monto = ttk.Entry(abonar_window)
        label_monto.grid(row=0, column=0, padx=5, pady=5)
        entry_monto.grid(row=0, column=1, padx=5, pady=5)

        label_descripcion = ttk.Label(abonar_window, text="Descripción:")
        entry_descripcion = ttk.Entry(abonar_window)
        label_descripcion.grid(row=1, column=0, padx=5, pady=5)
        entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

        def confirmar_abono():
            try:
                abono_monto = float(entry_monto.get())
                abono_descripcion = entry_descripcion.get()
                new_amount = amount - abono_monto
                update_transaction(selected_index, transaction_type, new_amount, description, name)
                add_transaction_to_history(transaction_type, -abono_monto, abono_descripcion, name, date)
                messagebox.showinfo("Éxito", "Abono registrado exitosamente")
                load_transactions()
                update_totals()
                abonar_window.destroy()
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa un monto válido")

        button_confirmar_abono = ttk.Button(abonar_window, text="Confirmar Abono", command=confirmar_abono)
        button_confirmar_abono.grid(row=2, column=0, columnspan=2, pady=10)

    button_abonar = ttk.Button(frame, text="Abonar", command=abonar_event)
    button_abonar.grid(row=5, column=0, padx=5, pady=10)

    # Botón para prestar más
    def prestar_mas_event():
        prestar_mas_window = tk.Toplevel(window)
        prestar_mas_window.title("Prestar Más")
        prestar_mas_window.geometry("300x150")

        label_monto = ttk.Label(prestar_mas_window, text="Monto:")
        entry_monto = ttk.Entry(prestar_mas_window)
        label_monto.grid(row=0, column=0, padx=5, pady=5)
        entry_monto.grid(row=0, column=1, padx=5, pady=5)

        label_descripcion = ttk.Label(prestar_mas_window, text="Descripción:")
        entry_descripcion = ttk.Entry(prestar_mas_window)
        label_descripcion.grid(row=1, column=0, padx=5, pady=5)
        entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

        def confirmar_prestamo():
            try:
                prestamo_monto = float(entry_monto.get())
                prestamo_descripcion = entry_descripcion.get()
                new_amount = amount + prestamo_monto
                update_transaction(selected_index, transaction_type, new_amount, description, name)
                add_transaction_to_history(transaction_type, prestamo_monto, prestamo_descripcion, name, date)
                messagebox.showinfo("Éxito", "Préstamo registrado exitosamente")
                load_transactions()
                update_totals()
                prestar_mas_window.destroy()
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa un monto válido")

        button_confirmar_prestamo = ttk.Button(prestar_mas_window, text="Confirmar Préstamo", command=confirmar_prestamo)
        button_confirmar_prestamo.grid(row=2, column=0, columnspan=2, pady=10)

    button_prestar_mas = ttk.Button(frame, text="Prestar Más", command=prestar_mas_event)
    button_prestar_mas.grid(row=5, column=1, padx=5, pady=10)

