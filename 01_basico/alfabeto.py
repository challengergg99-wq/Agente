def alfabeto_reverso(texto):
    lista_nueva = []
    letras = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
        "i": 9,
        "j": 10,
        "k": 11,
        "l": 12,
        "m": 13,
        "n": 14,
        "o": 15,
        "p": 16,    
        "q": 17,
        "r": 18,
        "s": 19,
        "t": 20,
        "u": 21,
        "v": 22,
        "w": 23,
        "x": 24,
        "y": 25,
        "z": 26
    }
    texto = texto.lower()
    for letra in texto:
        if letra in letras:
            lista_nueva.append(str(letras[letra]))
    return " ".join(lista_nueva)

print(alfabeto_reverso("Hola Mundo"))  # Output: "8 15 12 1 13 21 14 4 15"


name = "goku"
name = name.upper()

print(name)  # Output: "GOKU"