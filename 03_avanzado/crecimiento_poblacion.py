def crecimiento(p0,porcentaje,aug,p):
    años = 0
    while p0 < p:
        p0 = int(p0 + p0 * porcentaje / 100 + aug)
        años += 1
    return años

print(crecimiento(1500, 5, 100, 5000))
print(crecimiento(1500000, 2.5, 10000, 2000000))
print(crecimiento(1500000, 0.25, 1000, 2000000))


