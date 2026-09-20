numero = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
resuelto = [x ** 2 for x in numero if x % 2 == 0]
print(resuelto)



mi_tupla = (1, 2, 3, 2, 4, 2)


print (mi_tupla.index(2))   # Salida: 1

print (mi_tupla.index(2, 2))   #Salida: 3

print (len(mi_tupla))   



def sumar3(x):
    return x + 3


lambda_sumar3 = lambda x: x + 3
print("sumar de a 3:", sumar3(5))  
print("sumar de a 3:", lambda_sumar3(5))  


def suma_variable(*numeros):
    total = 0
    for numero in numeros:
        total += numero
    return total


print(suma_variable(1, 2, 3))  # Imprime 6
print(suma_variable(4, 5, 6, 7))