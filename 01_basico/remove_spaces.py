def no_space(x):
    contador = 0
    texto_limpio = ""
    for i in range(len(x)):
        if x[i] == " ":
            contador += 1
        else:
            texto_limpio += x[i]
    return texto_limpio, contador

print(no_space("H e l l o   W o r l d"))


def no_space2(x):
    texto_limpio = ""
    for i in range(len(x)):
        if x[i] != " ":
            texto_limpio += x[i]
    return texto_limpio