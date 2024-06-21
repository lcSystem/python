from datetime import datetime

def read_transactions():
    transactions = []
    try:
        with open("finanzas.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 5:  # Verificar que la línea tiene los 5 valores esperados
                    transaction_type, amount, description, name, date = parts
                    transactions.append((transaction_type, float(amount), description, name, date))
                else:
                    print(f"Línea ignorada por formato incorrecto: {line.strip()}")
    except FileNotFoundError:
        print("El archivo 'finanzas.txt' no se encontró. Asegúrate de que existe.")
    return transactions

def add_transaction(transaction_type, amount, description, name):
    # Formatear el monto como una cadena con dos decimales
    formatted_amount = "{:.2f}".format(amount)
    with open("finanzas.txt", "a") as file:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{transaction_type},{formatted_amount},{description},{name},{date}\n")

def update_transaction(index, transaction_type, amount, description, name):
    transactions = read_transactions()
    if 0 <= index < len(transactions):
        transactions[index] = (transaction_type, amount, description, name, transactions[index][4])
        with open("finanzas.txt", "w") as file:
            for transaction in transactions:
                file.write(f"{transaction[0]},{transaction[1]:.2f},{transaction[2]},{transaction[3]},{transaction[4]}\n")

def delete_transaction(index):
    transactions = read_transactions()
    if 0 <= index < len(transactions):
        transactions.pop(index)
        with open("finanzas.txt", "w") as file:
            for transaction in transactions:
                file.write(f"{transaction[0]},{transaction[1]:.2f},{transaction[2]},{transaction[3]},{transaction[4]}\n")

def add_transaction_to_history(transaction_type, amount, description, name, original_date):
    # Registrar la operación adicional (abono o préstamo) en un archivo de historial
    formatted_amount = "{:.2f}".format(amount)
    with open("historial.txt", "a") as file:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{transaction_type},{formatted_amount},{description},{name},{date},{original_date}\n")

def calculate_totals():
    transactions = read_transactions()
    total_ingresos = sum(t[1] for t in transactions if t[0] == "ingreso")
    total_egresos = sum(t[1] for t in transactions if t[0] == "gasto")
    saldo_neto = total_ingresos - total_egresos
    return total_ingresos, total_egresos, saldo_neto

def read_history():
    history = []
    with open("historial.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 6:  # Verificar que la línea tiene los 6 valores esperados
                transaction_type, amount, description, name, date, creation_date = parts
                history.append((transaction_type, float(amount), description, name, date, creation_date))
            else:
                print(f"Línea ignorada por formato incorrecto: {line.strip()}")
    return history

def plot_transactions():
    import matplotlib.pyplot as plt
    transactions = read_transactions()
    
    dates = [datetime.strptime(t[4], "%Y-%m-%d %H:%M:%S") for t in transactions]
    amounts = [t[1] for t in transactions]
    transaction_types = [t[0] for t in transactions]
    
    incomes = [amounts[i] if transaction_types[i] == "ingreso" else 0 for i in range(len(amounts))]
    expenses = [-amounts[i] if transaction_types[i] == "gasto" else 0 for i in range(len(amounts))]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, incomes, label="Ingresos", color='green')
    plt.plot(dates, expenses, label="Gastos", color='red')
    plt.fill_between(dates, incomes, 0, alpha=0.3, color='green')
    plt.fill_between(dates, expenses, 0, alpha=0.3, color='red')
    plt.xlabel("Fecha")
    plt.ylabel("Monto")
    plt.title("Ingresos y Gastos")
    plt.legend()
    plt.grid(True)
    plt.show()

