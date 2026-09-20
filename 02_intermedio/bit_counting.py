def count_bits(n):
    n = input("Ingrese un número entero:")    
    texto = bin(int(n))[2:] 
    cantidad_unos = texto.count('1') 
    cantidad_ceros = texto.count('0') 
    return cantidad_unos + cantidad_ceros  

print(count_bits(0))


def count_bits(n):
    contador = 0
    while n > 0:
        if n % 2 == 1:
            contador += 1
        n = n // 2
    return contador
