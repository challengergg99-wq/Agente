n = int(input("Ingrese un número entero no negativo: "))
def entero_a_binario(n):
    if n < 0:
        raise ValueError("El número debe ser un entero no negativo.")
    if n == 0:
        return "0"
    binario = ""
    while n > 0:
        binario = str(n % 2) + binario
        n = n // 2
    return binario
print(f"El número binario es: {entero_a_binario(n)}")
