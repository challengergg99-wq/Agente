def count(s):
    resultado = {}
    for char in s:
        if char in resultado:
            resultado[char] += 1
        else:
            resultado[char] = 1
    return resultado