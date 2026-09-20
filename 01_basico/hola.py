import random
import statistics
import math
from datetime import datetime


# resultado = 0
# for i in [3,3,5]:
#     if i > 3:
#         resultado = resultado -i    
#     else:
#         resultado = resultado + i
# print(resultado)


# name = "bryan"
# lastname = "carreño"

# print(f"hola: {name} {lastname}")


# topping1 = "Peanut Butter"
# topping2 = "Jelly"
# print("I like " + topping1 + " and " + topping2 + " on my sandwich.")



# numero1 = float(input("Ingrese un numero: "))
# numero2 = float(input("Ingrese un numero: "))
# operacion = input("Ingrese la operacion (+, -, *, /): ")
        
# if operacion == "+":
#     resulado = numero1 + numero2
# elif operacion == "-":
#     resulado = numero1 - numero2
# elif operacion == "*":
#     resulado = numero1 * numero2
# elif operacion == "/":
#     if numero2 == 0:
#         print("Error: Division por cero")
#     else:
#         resulado = numero1 / numero2
# else:
#     print("Operacion no valida")

# print(f"El resultado es: {resulado}")



# año = int(input("Ingrese un año: DD/MM/AAAA:"))
# if (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0):
#     print(f"El año {año} es bisiesto")
# else:
#     print(f"El año {año} no es bisiesto")



# bebe = int(input("Ingrese la edad del bebe: "))
# if bebe >= 0 and bebe <= 2:
#     print("es un recien nacido")
# elif bebe >= 3 and bebe <= 12:
#     print("Es Niño")
# elif bebe >= 13 and bebe <= 17:
#     print("Es Adolescente")
# elif bebe >= 18 and bebe <= 64:
#     print("Es Adulto")
# elif bebe >= 65:
#     print("Es Adulto mayor")


#listas 

# mensaje = ["C", "o", "d", "i", "g", "o", " ", "s", "e", "c", "r", "e", "t", "o"]
# cadena = "".join(mensaje)
# print(cadena)


# numeros = [10, 20, 30, 40, 50]
# numeros[0], numeros[4] = numeros[4], numeros[0]
# print(numeros)


# pan = ["pan arriba"]
# ingredientes = ["jamón", "queso", "tomate"]
# pan_abajo = ["pan abajo"]
# print(f"{pan}\n {ingredientes}\n {pan_abajo}")

# lista = [1, 2, 3]
# lista += lista
# print(lista)

# listaimpar = [1, 3, 5, 7, 9]
# centro = len(listaimpar) // 2
# print(listaimpar[centro])

# inversa = [1, 2, 3, 4, 5, 6]
# reves = len(inversa) // 2
# listainversa = inversa[:reves][::-1] + inversa[reves:]
# print(listainversa)


#listas con metodos

# lista1 = [1,2,3,4,5]
# lista1.append(6),lista1.insert(2,10)
# lista1[0] = 0
# print(lista1)

# lista_a = [1, 2, 3]
# lista_b = [4, 5, 6, 1, 2]
# lista_a.extend(lista_b)
# lista_a.remove(1)
# elementoeliminado = lista_a.pop(3)
# lista_b.clear()
# print(f"elemento eliminado: {elementoeliminado}")
# print(f"lista final: {lista_a}")
# print(f"lista final: {lista_b}")


# lista = [1,2,3,4,5,6,7,8,9,10]
# del lista[2:5]
# print(lista)

# numeros = [5, 2, 8, 1, 9, 4, 2]
# numeros.sort()
# contados = numeros.count(2)
# print(f"se encontraros: {contados} numeros 2 en la lista")
# print(7 in numeros)
# print(f"lista ordenada {numeros}")


# original = [1,2,3]
# copia = original[:]
# otracopia = copia.copy()
# referencia = original
# referencia[0] = 10
# print(f"copia de la original: {copia}")
# print(f"segunda copia:{otracopia}")
# print(f"ultima lista de referencia:{referencia}")


# frutas = ["Manzana", "pera", "BANANA", "naranja"]
# frutas.sort(key=str.lower)
# print(frutas)



# ciclo while

# contador = 10
# while contador >= 1:
#     print(contador)
#     contador -=1


# Ejercicio 2: Suma de números pares (while)
# Calcula la suma de los números pares entre 1 y 20 (inclusive) usando un bucle while.

# numero = 1
# pares = 0

# while numero <= 20:
#     if numero % 2 == 0:
#         pares += numero
#     numero +=1
#     print(f"cuantos:{pares}")


# Ejercicio 3: Factorial de un número
# Pide al usuario que introduzca un número entero positivo.
# Calcula su factorial usando un bucle while.
# El factorial de un número entero positivo es el producto de todos los números del 1 al ese número. Por ejemplo, el factorial de 5
# 5! = 5 x 4 x 3 x 2 x 1 = 120.

# contador = 1
# factorial = 1
# try:
#     numero = int(input("ingrese un numero positivo:"))
#     while contador <= numero:
#         factorial *= contador
#         contador +=1
#         print(f"el factorial del numero {numero} es {factorial}")
# except ValueError:
#     print("ingrese un numero:")


# Ejercicio 4: Validación de contraseña
# Pide al usuario que introduzca una contraseña.
# La contraseña debe tener al menos 8 caracteres.
# Usa un bucle while para seguir pidiendo la contraseña hasta que cumpla con los requisitos.
# Si la contraseña es válida, imprime "Contraseña válida".

# contraseña = ""

# while len(contraseña) < 8:
#     contraseña = (input("ingrese una contaseña maximo 8 caracteres:"))
#     if len(contraseña) < 8:
#         print("ingrese una contraseña valida")
# print("contraseña valida:")


# Ejercicio 5: Tabla de multiplicar
# Pide al usuario que introduzca un número.
# Imprime la tabla de multiplicar de ese número (del 1 al 10) usando un bucle while.

# multiplicador = 1
# numero = int(input("ingrese un numero a multiplicar:"))

# while multiplicador <= 10:
#     resultado = numero * multiplicador
#     print(f" {numero} x {multiplicador} = {resultado}")
#     multiplicador += 1


# Ejercicio 6: Números primos hasta N
# Pide al usuario que introduzca un número entero positivo N.
# Imprime todos los números primos menores o iguales que N usando un bucle while.


# contador = 2
# n = int(input("ingrese un numero positivo:"))

# while contador <= n:
#     es_primo = True
#     divisor = 2
#     while divisor * divisor <= contador:
#         if contador % divisor == 0:
#             es_primo = False
#             break
#         divisor += 1
#     if es_primo:
#         print(contador)
#     contador += 1



# contador = 1
# n = int(input("ingrese un numero positivo:"))
# if n < 1:
#     print("ingrese un valor mayor a 0")
# else:
#     while contador <= n:
#         print(contador)
#         contador += 1



# contador = 0
# while True:
#     n = int(input("ingrese un numero positivo:"))
#     if n == 0:
#         break
#     contador += n
#     print(f"suma total {contador}")
# print(f"resultado final {contador}")



# contador = 0
# m = abs(int(input("ingrese un numero positivo:")))
# if m == 0:
#     contador = 1 
# else:
#     while m > 0:
#         m = m // 10
#         contador += 1
# print(f"valor es: {contador}")
    
  


# secreto = random.randint(1,100)
# intentos = 0
# intentos_realizados = 0
# limite = 10
# print("He pensado en un numero entre el 1 al 100")
# while intentos != secreto and  intentos_realizados < limite:
#     intentos = int(input("que numero eliges para intentar adivinar:"))
#     intentos_realizados += 1
#     if intentos > secreto:
#         print(f"es mayor a tu {intentos}")
#     elif intentos < secreto:
#         print(f"es menor a tu {intentos}")
#     else:
#         print(f"adivinaste el numero secreto en tantos intentos: {intentos_realizados}")
# if intentos != secreto:
#     print(f"perdiste el valor secreto era: {secreto}")


# t = int(input("ingrese el limite de su multiplicacion:"))
# m = int(input("ingrese un numero para obtener su tabla:"))
# numero = 1

# while numero <= t:
#     resultado = m * numero
#     print(f"{m} x {numero} = {resultado}")
#     numero +=1



# a,b = 0,1
# contador = 0
# n = int(input("ingrese cuantos numeros quiere ver:"))
# print(f"fibonacci:{n}")
# while contador < n:
#     print(a,end="")
#     a,b = b,a + b
#     contador +=1
    


#ciclo for 
# pares = [1,2,3,4,5,6,7,8,9]
# for idx in pares:
#     if idx % 2 == 0:
#         print(idx)



# numeros = [10, 20, 30, 40, 50]
# suma = 0
# for idx in numeros:
#     suma += idx
# media = suma / len(numeros) 
# print(f"la media de los valores: {media}")

# numeros = [15, 5, 25, 10, 20]
# maximo = numeros[0]
# for idx in numeros:
#     if idx > maximo:
#         maximo = idx
# print(maximo)


# palabras = ["casa", "arbol", "sol", "elefante", "luna"]
# lista = [idx for idx in palabras if len(idx) > 5]
# print(lista)

#Contar palabras que empiezan con una letra
# palabras = ["casa", "arbol", "sol", "elefante", "luna", "coche"]
# letra = input("Introduce una letra: ") 
# contador = 0
# for idx in palabras:
#     if idx.lower().startswith(letra):
#         contador+=1
#         print(f"Hay {contador} palabras que empiezan con la letra {letra}")




# palabras = ["casa", "arbol", "sol", "elefante", "luna", "coche"]
# letra = input("Introduce una letra: ") 
# total = sum(1 for p in palabras if p.lower().startswith(letra))
# print(f"Total: {total}")


# palabras = ["casa", "arbol", "sol", "elefante", "luna", "coche"]
# letra = input("Filtrar palabras que empiecen con: ").lower()
# filtrar = []

# for palabra in palabras:
#     if palabra.lower().startswith(letra):
#         filtrar.append(palabra)
#         print(f"Palabras encontradas: {filtrar}")
#     else:
#         print("palabra no encontrada")

        

#range 

# for i in range(10):
#     print(i)


# for i in range(1,100):
#     if i % 3 == 0:
#         print(i)


# def es_palindromo(texto_limpio):
#     texto_filtrado = ""
#     for i in texto_limpio:
#         if i.isalpha():
#             texto_filtrado += i.lower()

#     reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
#     for a , b in reemplazos:
#         texto_filtrado = texto_filtrado.replace(a,b)

#     es_igual = texto_filtrado == texto_filtrado[::-1]
#     return es_igual

# texto = ("Adivina ya te opina, ya ni miles origina, ya ni cetro me domina, ya ni monarcas, a repaso ni mulato carreta, acaso nicotina, ya ni cita vecino, anima cocina, pedazo gallina, cedazo terso nos retoza de canilla goza, de pánico camina, ónice vaticina, ya ni tocino saca, a terracota luminosa pera, sacra nómina y ánimo de mortecina, ya ni giros elimina, ya ni poeta, ya ni vida")

# if es_palindromo(texto):
#     print("es un palindromo")
# else:
#     print("no es un palindromo")



# numero = 5
# if numero < 0:
#     print("no es factorial")
# else:
#     resultado = math.factorial(numero)
#     print(f"el factorial de: {numero} es {resultado}")



# def caso_factorial(n):
#     if n < 0:
#         return "no numeros negativos"

#     if n == 0 or n == 1:
#         return 1
#     else:
#         return n * caso_factorial(n -1)
    
# print(f"el factorial de 5 es {caso_factorial(5)}")
# print(f"el factorial de -3 es {caso_factorial(-3)}")


# def armstrong(n):
#     conv = str(n)
#     potencia = len(conv)
#     acum = 0
#     for numero in conv:
#         acum += int(numero) ** potencia
#         return acum == int(n)
    
# print(armstrong("128"))
# print(armstrong("9"))


# def armstrong1(n):
#     nuevo = str(n)
#     potencia = len(nuevo)
#     acum = sum(int(digito) ** potencia for digito in nuevo)
#     return acum == n

# nueva_potencia = 1000
# resultados = []

# for i in range(1,nueva_potencia + 1):
#     if armstrong1(i):
#         resultados.append(i)

# print(f"los numero de armstrong son:{nueva_potencia}")
# print(resultados)



# def limpiar_texto(texto):
#     texto = texto.lower()
#     for simbolo in ",.?!":
#         texto = texto.replace(simbolo,"")
#     palabras = texto.split()
#     frecuencias = {}

#     for p in palabras:
#         if p in frecuencias:
#             frecuencias[p] += 1
#         else:
#             frecuencias[p] = 1

#     return frecuencias

# parrafos = "Python es genial, porque Python es simple y Python es potente."
# resultados = limpiar_texto(parrafos)

# print("frecuencia de palabras")
# for palabra, conteo in resultados.items():
#     print(f"-{palabra}: {conteo}")


# def dias_contados(fecha1,fecha2):
#     formato = "%d-%m-%Y"
#     try:
#         f1 = datetime.strptime(fecha1,formato)
#         f2 = datetime.strptime(fecha2,formato)

#         diferencia = abs(f1-f2).days
#         return diferencia
    
#     except ValueError:
#         raise ValueError("Una de las fechas tiene un formato incorrecto o no existe.")
# try:
#     resultado = dias_contados("18-05-1920", "29-01-2026")
#     print(f"la diferencia de dias es:{resultado}")
# except ValueError as e:
#     print(e)



# def mayusculas(texto):
#     palabra = texto.split()
#     resultado = []
#     for p in palabra:
#         if len(p) >0:
#             nueva_palabra = p[0].upper() + p[1:].lower()
#             resultado.append(nueva_palabra)
#     return " ".join(resultado)

# texto = "hOlA mUnDo, eStOy aPrEndIenDo pYtHoN."
# print(mayusculas(texto))



# def carreras_y_saltos(acciones,pista,energia):
#     pista_final = ""
#     superado = True
#     for i, (accion, tramo) in enumerate(zip(acciones,pista)):
#         if energia > 0:
#             print(f"el atleta se ha quedado sin energia en el tramo:{i}")
#             superado =  False
#             break
#         if accion == "correr" and tramo == "_":
#             pista_final += "🏃"
#             energia -= 1
#         elif accion == "saltar" and tramo == "|":
#             pista_final += "🤸"
#             energia -= 3
#         elif accion == "correr" and tramo == "|":
#             pista_final += "💥"
#             energia -= 5
#             superado =  False
#         elif accion == "saltar" and tramo == "_":
#             pista_final += "x"
#             energia -= 7
#             superado = False
#     print(f"el tramo {i}: energía restante {energia}")

#     if superado and energia > 0:
#         print(f"¡Felicidades! Has completado la pista:{pista_final}")
#         return True
#     else:
#         print(f"no has podido completar la carrera:{pista_final}")
#         return False
# carreras_hechas = ["correr", "saltar", "correr", "correr", "saltar"]
# pista = ["_","|","|","_","_"]
# energia_inicial = 15

# resultado = carreras_y_saltos(carreras_hechas,pista,energia_inicial)
# print(f"el resultado final es:{resultado}")


# def analizar_matriz(matriz):
#     def verificar_ganador(simbolo):
#         for fila in matriz:
#             if all(celda == simbolo for celda in fila):
#                 return True
#         for col in range(3):
#             if all(matriz[fila][col] == simbolo for fila in range(3)):
#                 return True
#         if all(matriz[i][i] == simbolo for i in range(3)):
#             return True
#         if all(matriz[i][2 - i] == simbolo for i in range(3)):
#             return True
#         return False

#     conteo_x = sum(fila.count("X") for fila in matriz)
#     conteo_o = sum(fila.count("O") for fila in matriz)
#     total_celdas = sum(len(fila) for fila in matriz)

#     if conteo_x < conteo_o or conteo_x > conteo_o + 1:
#         return "Nulo"

#     x_gana = verificar_ganador("X")
#     o_gana = verificar_ganador("O")

#     if x_gana and o_gana:
#         return "Nulo"
#     if x_gana:
#         return "X"
#     if o_gana:
#         return "O"
#     if conteo_x + conteo_o == total_celdas:
#         return "Empate"
#     return "Nulo"


# number = 27
# power_of_two = 1

# while power_of_two <= number:
#     power_of_two *= 2

# print(power_of_two)


def calcular_milisegundos(dias, horas, minutos, segundos):
    total_milisegundos = (dias * 24 * 60 * 60 * 1000) + (horas * 60 * 60 * 1000) + (minutos * 60 * 1000) + (segundos * 1000)
    return total_milisegundos
print(calcular_milisegundos(1, 2, 30, 45))


def otra_forma(dias,horas,minutos,segundos):
    ms_segundos = 1000
    ms_minutos = 60 * ms_segundos
    ms_horas = 60 * ms_minutos
    ms_dias = 24 * ms_horas
    total = (dias * ms_dias) + (horas * ms_horas) + (minutos * ms_minutos) + (segundos * ms_segundos)
    return total
print(otra_forma(1, 2, 30, 45))