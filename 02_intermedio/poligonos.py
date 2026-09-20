def area_poligono(tipo_poligono, **dimensiones):
    
    if not isinstance(tipo_poligono, dict):
        raise TypeError('El polígono debe ser un dict con clave "tipo" y dimensiones')

    tipo = tipo_poligono.get('tipo')
    if not tipo:
        raise ValueError('Falta la clave "tipo" en el dict del polígono')

    tipo = tipo.lower()
    if tipo == 'triangulo':
        base = tipo_poligono.get('base')
        altura = tipo_poligono.get('altura')
        if base is None or altura is None:
            raise ValueError('Triángulo requiere "base" y "altura"')
        return (base * altura) / 2
    elif tipo == 'cuadrado':
        lado = tipo_poligono.get('lado')
        if lado is None:
            raise ValueError('Cuadrado requiere "lado"')
        return lado * lado
    elif tipo == 'rectangulo':
        base = tipo_poligono.get('base')
        altura = tipo_poligono.get('altura')
        if base is None or altura is None:
            raise ValueError('Rectángulo requiere "base" y "altura"')
        return base * altura
    else:
        raise ValueError(f'Tipo de polígono no soportado: {tipo}')


if __name__ == '__main__':
    # Ejemplos: imprimir el área de un polígono de cada tipo
    triangulo = {'tipo': 'triangulo', 'base': 5, 'altura': 10}
    cuadrado = {'tipo': 'cuadrado', 'lado': 5}
    rectangulo = {'tipo': 'rectangulo', 'base': 4, 'altura': 6}

    print('Triángulo área =', area_poligono(triangulo))
    print('Cuadrado área =', area_poligono(cuadrado))
    print('Rectángulo área =', area_poligono(rectangulo))    