def eliminar_caracteres(str1: str, str2: str) -> tuple:
    """
    Devuelve una tupla (out1, out2) donde:
    - out1 contiene los caracteres de `str1` que NO aparecen en `str2`.
    - out2 contiene los caracteres de `str2` que NO aparecen en `str1`.

    La comparación es insensible a mayúsculas (se compara por `lower()`),
    pero la salida preserva la capitalización original de cada carácter.

    Args:
        str1: Primera cadena.
        str2: Segunda cadena.

    Returns:
        Tuple (out1, out2).
    """
    if not isinstance(str1, str) or not isinstance(str2, str):
        raise TypeError("Ambos argumentos deben ser strings")

    set1 = {ch.lower() for ch in str1}
    set2 = {ch.lower() for ch in str2}
    comunes = set1 & set2

    out1 = ''.join(ch for ch in str1 if ch.lower() not in comunes)
    out2 = ''.join(ch for ch in str2 if ch.lower() not in comunes)

    print(f"{str1} -> {out1}")
    print(f"{str2} -> {out2}")

    return out1, out2


if __name__ == "__main__":
    print(eliminar_caracteres("Hola Mundo", "Python"))
    print(eliminar_caracteres("abcdef", "defghij"))
    print(eliminar_caracteres("Apple", "Pineapple"))
    print(eliminar_caracteres("12345", "34567"))