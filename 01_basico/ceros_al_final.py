def ceros_ultimos(n):
    nueva_lista = []
    for i in range(len(n)):
        if n[i] == 0:
            nueva_lista.append(n[i])
    return nueva_lista

print(1,0,2,3,0)