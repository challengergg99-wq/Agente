"""Pregunta 3 (algoritmos): Escribe una función buscar(numeros, objetivo) que reciba una lista de enteros ordenada de menor a mayor y devuelva el índice de objetivo, o -1 si no está. Ejemplo: con [1, 3, 5, 7, 9, 11] y objetivo = 7, devuelve 3. No puedes recorrer toda la lista de principio a fin."""

def buscar(numeros,objetivos):
    for i in range(len(numeros)):
        if numeros[i] == objetivos:
            return i
    return -1

print(buscar([1, 3, 5, 7, 9, 11], 7)) # Devuelve 3

#complejidad O(n) ya que recorre toda la lista de principio a fin.
#la lista debe estar ordenada de menor a mayor, si no lo está, la función no funcionará correctamente.
#si la lista tuviera 1.000.000 elementos, la función tardaría 1 segundo en recorrer toda la lista y encontrar el objetivo.


def buscar_binario(numeros, objetivo):
    izquierda = 0
    derecha = len(numeros) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if numeros[medio] == objetivo:
            return medio
        elif numeros[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return -1
print(buscar_binario([1, 3, 5, 7, 9, 11], 7)) # Devuelve 3

#complejidad O(log n) ya que divide la lista en dos partes en cada iteración, reduciendo el número de elementos a buscar a la mitad en cada paso.
#la lista debe estar ordenada de menor a mayor, si no lo está, la función no funcionará correctamente.
#si la lista tuviera 1.000.000 elementos, la función tardaría 20 iteraciones en encontrar el objetivo, ya que 2^20 = 1.048.576, lo que significa que en cada iteración se reduce a la mitad el número de elementos a buscar.