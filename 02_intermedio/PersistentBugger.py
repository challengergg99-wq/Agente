import math 
def persistence(n):
    contador = 0
    while n >= 10:
        producto = math.prod([int(d) for d in str(n)])
        n = producto
        contador += 1
    return contador


def persistence(n):
    contador = 0
    while n >=10:
        total = 1
        for d in str(n):
            total *= int(d)
        n = total
        contador += 1
    return contador