    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error

    def encontrar_mejor_modelo(datos):
        modelos = {
            "Regresión lineal": LinearRegression(),
            "K Vecinos más cercanos": KNeighborsRegressor(),
            "Árbol de decisión": DecisionTreeRegressor(),
            "Bosque aleatorio": RandomForestRegressor()
        }
        mejor_modelo = None
        mejor_error = float('inf')

        for nombre, modelo in modelos.items():
            modelo.fit(np.arange(len(datos)).reshape(-1, 1), datos)
            predicciones = modelo.predict(np.arange(len(datos)).reshape(-1, 1))
            error = mean_squared_error(datos, predicciones)
            if error < mejor_error:
                mejor_error = error
                mejor_modelo = nombre

        return mejor_modelo

    def predecir_siguiente_numero(datos):
        modelo = LinearRegression()
        modelo.fit(np.arange(len(datos)).reshape(-1, 1), datos)
        siguiente_numero = modelo.predict(np.array([[len(datos)]]))
        return siguiente_numero[0]

    # Datos de entrenamiento
    datos_entrenamiento = np.array([1.74,2.01,1.17,3.09,3.09,1.18,1.44,1.27,1.74,1.25,4.29,1.02,9.28,1.15,1.25,36.59,1.57,6.68,3.27,2.45,1.84,1.20,13.65,2.60,10.41,1.69,1.10,4.35,11.02,1.38,4.23,1.05,1.31,1.20,13.98,1.17,1.05,5.16,1.15,2.42,3.04,3.18,3.09,9.28,20.96,3.46,8.89,9.28,65.74,1.02,3.82,4.23,2.75,1.05,1.23,1.20,4.95,1.82,1.77,2.53,1.02,1.15,1.98,1.20,4.54,1.15,1.64,1.13,14.75,1.79,3.94,4.88,1.98,1.64,29.96,1.23,70.60,6.40,1.20,2.87,1.31,1.53,1.20,1.44,1.29,20.66,7.49,1.02,1.08,1.95,1.47,1.15,2.71,1.90,1.07,1.25,1.42,1.13,52.40,5.63,2.53,1.27,2.07,2.87,4.81,1.57,1.33,1.08,7.71,3.72,7.93,16.44,6.04,1.20,4.23,17.41,2.45,4.54,1.36,1.13,1.00,16.21,8.05,1.02,3.04,1.18,3.18,1.74,1.22,1.64,1.69,1.00,1.47,2.35,3.88,1.64,6.49,1.05,1.47,1.62,1.20,1.27,5.71,1.12,9.69,3.46,2.96,2.19,1.25,15.75,16.21,1.08,2.91,1.02,2.75,9.28,6.40,3.04,3.99,7.60,1.53,3.99,1.25,1.95,1.90,5.55,3.32,1.01,2.87,6.49,1.40,3.94,1.01,1.13,1.00,5.87,16.85,1.10,1.27,1.13,1.55,6.40,1.49,2.79,12.00,3.99,3.32,1.12,1.49,3.18,1.18,6.22,1.34,1.10,3.94,1.51,5.79,1.18,1.69,1.25,1.00])

    # Encontrar el mejor modelo para los datos
    mejor_modelo = encontrar_mejor_modelo(datos_entrenamiento)
    print("El mejor modelo para los datos es:", mejor_modelo)

    # Predecir el siguiente número en la secuencia
    siguiente_numero = predecir_siguiente_numero(datos_entrenamiento)
    print("El siguiente número en la secuencia es:", siguiente_numero)
