import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_squared_error

def encontrar_mejor_modelo(datos):
    modelos = {
        "Red Neuronal": crear_red_neuronal()
    }
    mejor_modelo = None
    mejor_error = float('inf')

    for nombre, modelo in modelos.items():
        modelo.fit(np.arange(len(datos)).reshape(-1, 1), datos, epochs=100, verbose=0)
        predicciones = modelo.predict(np.arange(len(datos)).reshape(-1, 1))
        error = mean_squared_error(datos, predicciones)
        if error < mejor_error:
            mejor_error = error
            mejor_modelo = nombre

    return mejor_modelo

def predecir_siguiente_numero(datos):
    modelo = crear_red_neuronal()
    modelo.fit(np.arange(len(datos)).reshape(-1, 1), datos, epochs=100, verbose=0)
    siguiente_numero = modelo.predict(np.array([[len(datos)]]))
    return siguiente_numero[0][0]

def crear_red_neuronal():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(1,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Datos de entrenamiento
datos_entrenamiento = np.array([])

# Encontrar el mejor modelo para los datos
mejor_modelo = encontrar_mejor_modelo(datos_entrenamiento)
print("El mejor modelo para los datos es:", mejor_modelo)

# Predecir el siguiente número en la secuencia
siguiente_numero = predecir_siguiente_numero(datos_entrenamiento)
print("El siguiente número en la secuencia es:", siguiente_numero)

