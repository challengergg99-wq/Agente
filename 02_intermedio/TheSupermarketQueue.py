import heapq

def queue_time(customers, n):
    cajas = [0] * n
    heapq.heapify(cajas)
    for cliente in customers:
        heapq.heappushpop(cajas, heapq.heappop(cajas) + cliente)
        heapq.heappush(cajas, heapq.heappop(cajas))
    return cajas


def queue_time(customers, n):
    if n == 1:
        return sum(customers)
    if n >= len(customers):
        return max(customers)

    cajas = [0] * n
    for cliente in customers:
        min_caja = cajas.index(min(cajas))
        cajas[min_caja] += cliente

    return max(cajas)

def queue_time(customers, n):
    cajas = [0] * n
    for cliente in customers:
        min_caja = cajas.index(min(cajas))
        cajas[min_caja] += cliente
    return max(cajas)