def Diferenciacimetrica(array1, array2):
    parte1= [x for x in array1 if x not in array2]
    parte2= [x for x in array2 if x not in array1]
    return parte1 + parte2

print(Diferenciacimetrica([1, 2, 3], [2, 3, 4]))

def sym(*args):
    resultadoacumulado = []
    for i in range(1,len(args)):
        resultadoacumulado = Diferenciacimetrica(resultadoacumulado, args[i])
    return resultadoacumulado

resultadoacumulado = sym([1, 2, 3], [5, 2, 1, 4])
print(resultadoacumulado)