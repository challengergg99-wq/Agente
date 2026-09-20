def wave(people):
    lista = []
    for letra in range(len(people)):
        if people[letra] == " ":
            continue
        else:
            lista.append(people[:letra] + people[letra].upper() + people[letra + 1:])
    return lista

print(wave("hello world"))