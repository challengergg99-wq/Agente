def triangulo(a,b,c):
    """Ejecuta la lógica de triangulo.

    Args:
            a: Descripción del parámetro a.
            b: Descripción del parámetro b.
            c: Descripción del parámetro c.

    Returns:
        Resultado de la operación.
    """
    if a + b > c and a + c > b and b + c > a:
        return True
    else:
        return False
