def reverse_seq(n):
    lista = []
    for i in range(0,n):
        lista.append(n-i)
    return lista
        

print(reverse_seq(5))