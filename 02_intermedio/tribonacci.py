def tribonacci(signature, n):
    if n == 0:
        return []
    elif n < 3:
        return signature[:n]
    
    result = signature[:]
    for i in range(3, n):
        next_value = result[i-1] + result[i-2] + result[i-3]
        result.append(next_value)
    
    return result

print(tribonacci([1, 1, 1], 10))  