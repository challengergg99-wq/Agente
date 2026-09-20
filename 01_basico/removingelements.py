def remove_every_other(my_list):
    lista = []
    for i in range(len(my_list)):
        if i % 2 == 0:
            lista.append(my_list[i])
    return lista