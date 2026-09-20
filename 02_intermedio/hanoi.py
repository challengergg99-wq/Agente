def towe_hanoi(n):
    torres ={
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": []
    }

    almacenar = []

    def torre_actual():
        almacenar.append(f"Torres: A: {torres['A']}, B: {torres['B']}, C: {torres['C']}")

        return torre_actual()



    def mover_disco(n, origen, destino, auxiliar):
        if n == 1:
            disco = torres[origen].pop()
            torres[destino].append(disco)
            almacenar.append(f"Mover disco {disco} de {origen} a {destino}")
            return

        mover_disco(n - 1, origen, auxiliar, destino)

        disco = torres[origen].pop()
        torres[destino].append(disco)
        torre_actual()

        mover_disco(n - 1, auxiliar, destino, origen)
    
    mover_disco(n, "A", "C", "B")

    return "\n".join(almacenar)
