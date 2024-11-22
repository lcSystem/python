import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class Formulario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label_numero_tarea = QLabel("Número de Tarea:")
        self.entry_numero_tarea = QLineEdit()
        layout.addWidget(label_numero_tarea)
        layout.addWidget(self.entry_numero_tarea)

        label_componente = QLabel("Componente:")
        self.entry_componente = QLineEdit()
        layout.addWidget(label_componente)
        layout.addWidget(self.entry_componente)

        label_descripcion = QLabel("Descripción:")
        self.entry_descripcion = QLineEdit()
        layout.addWidget(label_descripcion)
        layout.addWidget(self.entry_descripcion)

        boton_enviar = QPushButton("Enviar")
        boton_enviar.clicked.connect(self.validar_entrada)
        layout.addWidget(boton_enviar)

        self.setLayout(layout)

    def validar_entrada(self):
        numero_tarea = self.entry_numero_tarea.text()
        componente = self.entry_componente.text()
        descripcion = self.entry_descripcion.text()

        if len(numero_tarea) != 5 or not numero_tarea.isdigit():
            self.mostrar_mensaje_error("El número de tarea debe ser de 5 caracteres numéricos.")
            return

        if len(componente) != 2:
            self.mostrar_mensaje_error("El componente debe ser de 2 caracteres.")
            return

        if len(descripcion) > 80:
            self.mostrar_mensaje_error("La descripción debe tener máximo 80 caracteres.")
            return

        print("Número de tarea:", numero_tarea)
        print("Componente:", componente)
        print("Descripción:", descripcion)

    def mostrar_mensaje_error(self, mensaje):
        mensaje_box = QMessageBox()
        mensaje_box.setIcon(QMessageBox.Warning)
        mensaje_box.setText(mensaje)
        mensaje_box.setWindowTitle("Error")
        mensaje_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    formulario = Formulario()
    formulario.show()
    sys.exit(app.exec_())
