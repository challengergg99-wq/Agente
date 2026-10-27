def enteros(value):
    """ recibir una lista de enteros y devolver true si algun valor se repite, de lo contrario devolver false """
    if len(value) != len(set(value)):
        return True
    else:
        return False
print(enteros([1, 2, 3, 4, 5])) 


def tiene_duplicados(lista):
    vistos = set()
    for elemento in lista:
        if elemento in vistos:
            return True
        vistos.add(elemento)
    return False
print(tiene_duplicados([1, 2, 3, 4, 5]))  # Output: False