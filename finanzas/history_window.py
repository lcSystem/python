import tkinter as tk
from tkinter import ttk
from logic import read_history

def open_history_window():
    def filter_transactions():
        selected_name = combo_person.get()
        filtered_transactions = [transaction for transaction in transactions if transaction[3] == selected_name]
        show_transactions(filtered_transactions)

    def show_transactions(transactions_to_show):
        tree.delete(*tree.get_children())
        for index, (transaction_type, amount, description, name, date, creation_date) in enumerate(transactions_to_show):
            tree.insert("", "end", iid=index, values=(transaction_type, f"{amount:.2f}", description, name, date, creation_date))

    window = tk.Toplevel()
    window.title("Historial de Transacciones")
    window.geometry("1200x400")
    window.configure(bg='#e0f7fa')

    # Combo box para seleccionar la persona
    persons = set(transaction[3] for transaction in read_history())
    combo_person = ttk.Combobox(window, values=list(persons))
    combo_person.pack(pady=10)
    combo_person.bind("<<ComboboxSelected>>", lambda event: filter_transactions())

    # Crear y configurar Treeview para mostrar el historial
    tree = ttk.Treeview(window, columns=("Tipo", "Monto", "Descripción", "Nombre", "Fecha", "Fecha de Creación"), show="headings")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Monto", text="Monto")
    tree.heading("Descripción", text="Descripción")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Fecha de Creación", text="Fecha de Creación")
    tree.pack(fill="both", expand=True)

    # Cargar todos los datos del historial
    transactions = read_history()
    show_transactions(transactions)

    window.mainloop()

