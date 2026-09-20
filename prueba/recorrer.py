def triangulo(a,b,c):
    if a + b > c and a + c > b and b + c > a:
        return True
    else:
        return False


"""python
    def triangulo(a: float, b: float, c: float) -> bool:
    Verifica si los lados de un triángulo son válidos"""

"""Args:
        a (float): El primer lado del triángulo.
        b (float): El segundo lado del triángulo.
        c (float): El tercer lado del triángulo.

        Returns:
        bool: True si los lados forman un triángulo válido, False en caso contrario."""