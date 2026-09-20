def find_even_index(arr):
    suma_izquierda = 0
    suma_derecha = sum(arr)
    for i, num in enumerate(arr):
        suma_derecha -= num
        if suma_izquierda == suma_derecha:
            return i
        suma_izquierda += num
    return -1

print(find_even_index([1, 2, 3, 4, 3, 2, 1]))  # Output: 3