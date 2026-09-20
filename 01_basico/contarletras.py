texto = "hola mundo, cómo estás, bienvenido a la programación en Python"
palabras = texto.lower().split()
conteo = {}

for i in palabras:
        if palabras in palabras:
            conteo[i] += 1
        else:
            conteo[i] = 1
print(conteo)