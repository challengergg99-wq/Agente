def acumular_por_categoria(transacciones):
    """
    Agrupa las transacciones por categoría y acumula sus montos.

    Args:
        transacciones (list): Lista de diccionarios con las transacciones.

    Returns:
        dict: Diccionario con categorías como claves y la suma de montos como valores."""

    resultado = {}
    for transaccion in transacciones:
        categoria = transaccion.get("categoria")
        monto = transaccion.get("monto", 0)
        # resultado[categoria] = resultado.get(categoria, 0) + monto
        if categoria in resultado:
            resultado[categoria] += monto
        else:
            resultado[categoria] = monto
    return resultado


