def narcisist(x):
    suma = 0
    for i in range(len(str(x))):
        suma += int(str(x)[i]) ** len(str(x))
    return suma == x

print(narcisist(255))  # True


def narcisist():
    numero = int(input("Ingrese un número: "))
    suma = 0
    for i in range(len(str(numero))):
        suma += int(str(numero)[i]) ** len(str(numero))
    return suma == numero

print(f"el número ingresado es{narcisist()}") 