def move_zeros(lst):
    nueva_lista = []
    for i in range(len(lst)):
        if lst[i] != 0:
            nueva_lista.append(lst[i])
    return nueva_lista + [0] * (len(lst) - len(nueva_lista))

print(move_zeros([1, 0, 2, 0, 3, 0, 4])) 

