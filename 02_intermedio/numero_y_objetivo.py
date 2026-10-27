def objetivo_de_suma(objetivo,lista):
    lista2 = []
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] + lista[j] == objetivo:
                lista2.append((lista[i], lista[j]))
    return lista2

print(objetivo_de_suma(10, [1, 2, 3, 4, 5, 6, 7, 8, 9])) #O(n^2)


def objetivo_de_suma_eficiente(objetivo, lista):
    numeros = set()
    lista2 = []
    for i in lista:
        complemento = objetivo - i
        if complemento in numeros:
            lista2.append((complemento, i))
        numeros.add(i)
    return lista2

print(objetivo_de_suma_eficiente(10, [1, 2, 3, 4, 5, 6, 7, 8, 9])) #O(n)


def dos_sumas(numeros, objetivo):
    vistos = {}  # número -> índice
    for i, x in enumerate(numeros):
        complemento = objetivo - x
        if complemento in vistos:
            return [vistos[complemento], i]
        vistos[x] = i
    return []