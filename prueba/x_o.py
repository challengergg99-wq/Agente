def x_o(s):
    """Ejecuta la lógica de x o.

    Args:
            s: Descripción del parámetro s.

    Returns:
        Resultado de la operación.
    """
    texto = s.lower()
    contador_x = texto.count("x")
    contador_o = texto.count("o")
    if contador_x == contador_o:
        return True
    else:
        return False
    