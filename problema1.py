from munkres import Munkres

def obtener_matriz():
    n = int(input("Ingrese el número de centros de distribución y rutas de entrega: "))
    matriz = []
    print("Ingrese la matriz de costos (solo números enteros):")
    for i in range(n):
        fila = input(f"Fila {i+1}: ").strip().split()
        try:
            fila = list(map(int, fila))
        except ValueError:
            raise ValueError("Por favor, ingrese solo números enteros separados por espacios.")
        
        if len(fila) != n:
            raise ValueError("Cada fila debe tener exactamente {} números.".format(n))
        
        matriz.append(fila)
    
    return matriz

def mostrar_matriz(matriz, mensaje):
    print(mensaje)
    for fila in matriz:
        print("\t".join(map(str, fila)))

def restar_minimos_filas(matriz):
    for i in range(len(matriz)):
        min_valor_fila = min(matriz[i])
        for j in range(len(matriz[i])):
            matriz[i][j] -= min_valor_fila

def restar_minimos_columnas(matriz):
    for j in range(len(matriz[0])):
        min_valor_columna = min(matriz[i][j] for i in range(len(matriz)))
        for i in range(len(matriz)):
            matriz[i][j] -= min_valor_columna

def resolver_problema(matriz, minimizar=True):
    m = Munkres()
    original = [fila[:] for fila in matriz]  # Copia de la matriz original
    mostrar_matriz(matriz, "\nMatriz inicial:")
    
    if not minimizar:
        max_valor = max(max(fila) for fila in matriz)
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                matriz[i][j] = max_valor - matriz[i][j]
        mostrar_matriz(matriz, "Matriz convertida para maximizar:")

    mostrar_matriz(matriz, "\nMatriz actual:\n")
    restar_minimos_filas(matriz)
    mostrar_matriz(matriz, "\nDespués de restar el valor mínimo de cada fila:\n")
    restar_minimos_columnas(matriz)
    mostrar_matriz(matriz, "\nDespués de restar el valor mínimo de cada columna:\n")

    # Obtener la asignación final
    indices = m.compute(matriz)
    # Mostrar la asignación final y el costo total
    costo_total = 0
    print("\n")
    for fila, columna in indices:
        valor = original[fila][columna]
        costo_total += valor
        print(f'Asignar centro {fila+1} a ruta {columna+1} - Costo: {valor}')
    
    print(f"Costo total {'mínimo' if minimizar else 'máximo'}: {costo_total}")

def main():
    try:
        matriz = obtener_matriz()
        modo = input("¿Desea minimizar (min) o maximizar (max) el costo total? ").strip().lower()
        if modo not in ['min', 'max']:
            raise ValueError("La opción debe ser 'min' o 'max'.")
        
        minimizar = modo == 'min'
        resolver_problema(matriz, minimizar)
    except ValueError as e:
        print(f"Error: {e}")
        main()  # Reiniciar el programa en caso de error
main()