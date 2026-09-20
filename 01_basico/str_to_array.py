def string_to_array(s):
    return s.split(" ")


def your_orden(order):
    separadas = order.split()
    for char in separadas:
        if char.isdigit():
            return int(char)

def order(words):
    if not words:
        return ""
    palabras = words.split()
    palabras_ordenadas = sorted(palabras, key=your_orden)
    return " ".join(palabras_ordenadas)


def order_2(words):
    if not words:
        return ""
    
    palabras = words.split()
    resultado = [None] * len(palabras)
    
    for palabra in palabras:
        for char in palabra:
            if char.isdigit():
                posicion = int(char) - 1
                resultado[posicion] = palabra
    return " ".join(resultado)

print(order_2("is2 Thi1s T4est 3a"))

