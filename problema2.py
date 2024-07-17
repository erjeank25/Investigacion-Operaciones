import numpy as np
from scipy.optimize import linprog

def agregar_ficticia(ofertas, demandas, costos):
    oferta_total = sum(ofertas)
    demanda_total = sum(demandas)
    
    if oferta_total > demanda_total:
        # Agregar columna ficticia
        demandas.append(oferta_total - demanda_total)
        for fila in costos:
            fila.append(0)
    elif demanda_total > oferta_total:
        # Agregar fila ficticia
        ofertas.append(demanda_total - oferta_total)
        costos.append([0] * len(demandas))
    
    return ofertas, demandas, costos

def transporte_minimo_coste(ofertas, demandas, costos):
    """
    Calcula el costo mínimo de transporte y las rutas óptimas.
    
    Parámetros:
    ofertas (list): Lista de ofertas de cada almacén.
    demandas (list): Lista de demandas de cada centro de distribución.
    costos (2D list): Matriz de costos de transporte.
    
    Retorna:
    tuple: Costo total mínimo, matriz de transporte óptimo.
    """
    m = len(ofertas)
    n = len(demandas)
    
    # Convertimos las matrices y listas a numpy arrays
    ofertas = np.array(ofertas)
    demandas = np.array(demandas)
    costos = np.array(costos)
    
    # El vector de costes linealizado
    c = costos.flatten()
    
    # Creamos las restricciones de oferta (<=)
    A_eq = []
    for i in range(m):
        restriccion = [0] * (m * n)
        for j in range(n):
            restriccion[i * n + j] = 1
        A_eq.append(restriccion)
    b_eq = ofertas
    
    # Creamos las restricciones de demanda (>=)
    for j in range(n):
        restriccion = [0] * (m * n)
        for i in range(m):
            restriccion[i * n + j] = 1
        A_eq.append(restriccion)
    b_eq = np.concatenate([b_eq, demandas])
    
    # Los límites para las variables de decisión (>= 0)
    limites_x = [(0, None) for _ in range(m * n)]
    
    # Usamos linprog para resolver el problema
    resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=limites_x, method='highs')
    
    if resultado.success:
        # Obtenemos la matriz de transporte óptima
        X = resultado.x.reshape((m, n))
        costo_total_minimo = resultado.fun
        return costo_total_minimo, X
    else:
        raise ValueError("No se pudo encontrar una solución óptima.")

def main():
    # Introducir datos por consola
    almacenes = int(input("Introduce el número de almacenes: "))
    centros = int(input("Introduce el número de centros de distribución: "))

    ofertas = []
    for i in range(almacenes):
        oferta = int(input("Introduce la oferta del almacén {}: ".format(i + 1)))
        ofertas.append(oferta)

    demandas = []
    for j in range(centros):
        demanda = int(input("Introduce la demanda del centro de distribución {}: ".format(j + 1)))
        demandas.append(demanda)

    costos = []
    for i in range(almacenes):
        fila_costos = []
        for j in range(centros):
            costo = float(input("Introduce el costo de transporte del almacén {} al centro de distribución {}: ".format(i + 1, j + 1)))
            fila_costos.append(costo)
        costos.append(fila_costos)

    # Balancear el problema si es necesario
    ofertas, demandas, costos = agregar_ficticia(ofertas, demandas, costos)

    # Llamar a la función de transporte
    costo_total_minimo, X = transporte_minimo_coste(ofertas, demandas, costos)

    # Mostrar resultados
    print("\nCosto total mínimo de transporte: {}".format(costo_total_minimo))
    print("Envíos óptimos desde cada almacén a cada centro de distribución:")

    # Mostrar envíos correspondientes
    for i in range(len(ofertas)):
        for j in range(len(demandas)):
            if X[i][j] > 0:
                print("Almacén {} -> Centro de Distribución {}: {} unidades".format(i + 1, j + 1, X[i][j]))
main()