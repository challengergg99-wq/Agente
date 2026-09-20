def ip_between(start, end):
    a ,b,c,d = [int(x) for x in start.split('.')]
    f,g,h,i = [int(x) for x in end.split('.')]
    inicio_entero =  (a * 256**3) + (b * 256**2) + (c * 256) + d
    fin_entero = (f * 256**3) + (g * 256**2) + (h * 256) + i

    return fin_entero - inicio_entero

print(ip_between("10.0.0.0", "10.0.0.5"))
print(ip_between("20.0.0.10", "20.0.1.0"))