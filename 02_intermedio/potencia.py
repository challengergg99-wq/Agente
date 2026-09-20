def suma_digitos(numero):
    suma = 0
    n = str(numero)
    for i in range((len(n))):
        suma += int(n[i])
    return suma
def pow_sum_dig_term(n):
    numeros = set()
    for base in range(2,100):
        for exponente in range(2,100):
            potencia = base ** exponente
            if suma_digitos(potencia) == base and potencia >= 10:
                numeros.add(potencia)
                

            
    lista = sorted(list(numeros))
    return lista[n-1]

print(pow_sum_dig_term(1))