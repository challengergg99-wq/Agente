def operador(valor1,valor2,operador):
    if operador == "+":
        return valor1 + valor2
    elif operador == "-":
        return valor1 - valor2
    elif operador == "*":
        return valor1 * valor2
    elif operador == "/":
        return valor1 / valor2
    else:
        return "Operador inválido"