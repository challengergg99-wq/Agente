def x_o(s):
    texto = s.lower()
    contador_x = texto.count("x")
    contador_o = texto.count("o")
    if contador_x == contador_o:
        return True
    else:
        return False