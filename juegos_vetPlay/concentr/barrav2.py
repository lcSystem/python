import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog
from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("prediccion - arbol-ramdom")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label_datos = QLabel("Ingresa un número:")
        self.layout.addWidget(self.label_datos)

        self.line_edit_datos = QLineEdit()
        self.layout.addWidget(self.line_edit_datos)
        self.line_edit_datos.returnPressed.connect(self.agregar_al_grafico)

        self.label_archivo = QLabel("Selecciona fuente de datos:")
        self.layout.addWidget(self.label_archivo)

        self.button_archivo = QPushButton("Cargar Datos")
        self.button_archivo.clicked.connect(self.cargar_desde_archivo)
        self.layout.addWidget(self.button_archivo)

        self.button_calcular = QPushButton("Calcular próximo número")
        self.button_calcular.clicked.connect(self.calcular_proximo_numero)
        self.layout.addWidget(self.button_calcular)

        self.text_edit_log = QTextEdit()
        self.text_edit_log.setStyleSheet("color: black; background-color: #FFFFFF")
        self.text_edit_log.setReadOnly(True)
        self.layout.addWidget(self.text_edit_log)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Índice')
        self.ax.set_ylabel('Valor')
        self.ax.set_title('Diagrama de Barras')

        self.datos = []

    def color_barra(self, valor):
        if valor <= 1.3:
            return 'red'
        elif valor >= 2.5:
            return 'green'
        else:
            return 'orange'

    def cargar_desde_archivo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo", "", "Archivos de Texto (*.txt)")
        if filename:
            with open(filename, 'r') as file:
                datos_str = file.read()
                try:
                    self.datos = [float(x.strip()) for x in datos_str.split(',')]
                    self.actualizar_grafico()
                    self.log("Datos cargados desde el archivo: {}".format(filename), color='green')
                except ValueError:
                    self.log("Error: El archivo seleccionado no contiene datos válidos.", color='red')

    def agregar_al_grafico(self):
        texto = self.line_edit_datos.text()
        if texto.strip():
            try:
                numero = float(texto)
                self.datos.append(numero)
                self.line_edit_datos.clear()
                self.actualizar_grafico()
                self.log("Número {} agregado al gráfico.".format(numero), color='green')
            except ValueError:
                self.log("Error: Por favor, ingresa un número válido.", color='red')

    def encontrar_mejor_modelo(self):
        if len(self.datos) < 3:
            self.log("Error: No hay suficientes datos para encontrar el mejor modelo.", color='red')
            return None

        modelos = {
            "Regresión lineal": LinearRegression(),
            "K Vecinos más cercanos": KNeighborsRegressor(),
            "Árbol de decisión": DecisionTreeRegressor(),
            "Bosque aleatorio": RandomForestRegressor()
        }
        mejor_modelo = None
        mejor_error = float('inf')

        for nombre, modelo in modelos.items():
            try:
                modelo.fit(np.arange(len(self.datos)).reshape(-1, 1), self.datos)
                predicciones = modelo.predict(np.arange(len(self.datos)).reshape(-1, 1))
                error = mean_squared_error(self.datos, predicciones)
                if error < mejor_error:
                    mejor_error = error
                    mejor_modelo = nombre
            except Exception as e:
                self.log("Error al entrenar modelo {}: {}".format(nombre, e), color='red')

        return mejor_modelo

    def predecir_siguiente_numero(self):
        if len(self.datos) < 1:
            self.log("Error: No hay suficientes datos para predecir el siguiente número.", color='red')
            return None

        modelo = LinearRegression()
        modelo.fit(np.arange(len(self.datos)).reshape(-1, 1), self.datos)
        siguiente_numero = modelo.predict(np.array([[len(self.datos)]]))
        return siguiente_numero[0]

    def calcular_proximo_numero(self):
        mejor_modelo = self.encontrar_mejor_modelo()
        if mejor_modelo:
            self.log("El mejor modelo para los datos es: {}".format(mejor_modelo), color='green')
            siguiente_numero = self.predecir_siguiente_numero()
            if siguiente_numero is not None:
                self.log("El siguiente número en la secuencia es: {}".format(siguiente_numero), color='green')

    def log(self, mensaje, color='black'):
        self.text_edit_log.setTextColor(QtGui.QColor(color))
        self.text_edit_log.append(mensaje)

    def actualizar_grafico(self):
        self.ax.clear()
        self.ax.bar(range(1, len(self.datos) + 1), self.datos, color=[self.color_barra(valor) for valor in self.datos])
        self.ax.set_xlabel('Índice')
        self.ax.set_ylabel('Valor')
        self.ax.set_title('Diagrama de Barras')
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

