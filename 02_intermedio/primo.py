index = int(input("ingresa un numero para verificar si es primo: "))
if index > 1:
    for i in range(2, index):
        if (index % i) == 0:
            print(f"{index} no es un numero primo")
            break
    else:
        print(f"{index} es un numero primo")