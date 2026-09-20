def balance(expreciones: str) -> bool:
    simbolos = {'(': ')', '{': '}', '[': ']'}
    pila = []
    for char in expreciones:
        if char in simbolos:
            pila.append(char)
        elif char in simbolos.values():
            if not pila or simbolos[pila.pop()] != char:
                return False
    return len(pila) == 0

if __name__ == "__main__":
    print(balance("({[]})"))  # True
    print(balance("({[})"))   # False

