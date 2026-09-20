def high(x):
    palabras = x.split()
    palabra_ganadora = ""
    puntuacion_maxima = 0
    for palabra in palabras:
        puntos_actuales = 0
        for letra in palabra:
            puntos_actuales += ord(letra) - 96
        if puntos_actuales > puntuacion_maxima:
            puntuacion_maxima = puntos_actuales
            palabra_ganadora = palabra
    return palabra_ganadora

