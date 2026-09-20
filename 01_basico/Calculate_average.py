
#Calculate_average
def find_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

#Beginner - Reduce but Grow
def grow(arr):
    result = 1
    for num in arr:
        result *= num
    return result


#Area or Perimeter
def area_or_perimeter(l, w):
    if l == w:
        return l * w
    else:
        return 2 * (l + w)
    

#Sum of the first nth term of Series
def series_sum(n):
    if n == 0:
        return "0.00"
    total = 0 
    for i in range(n):
        total += 1 / (1 + 3 * i)
    return "{:.2f}".format(total)

print(find_average([1, 2, 3, 4, 5]))  


#Remove the minimum
def remove_smallest(numbers):
    if not numbers:
        return []
    copia = numbers.copy()
    min_value = min(numbers)
    copia.remove(min_value)
    
    return copia

print(remove_smallest([5, 3, 2, 1, 4]))


#will you make it?
def zero_fuel(distance_to_pump, mpg, fuel_left):
    if distance_to_pump <= mpg * fuel_left:
        return True
    else:
        return False


#unique in order
def unique_in_order(iterable):
    ultimo_visto = None
    resultado = []
    for item in iterable:
        if item != ultimo_visto:
            resultado.append(item)
            ultimo_visto = item
    return resultado

#double char
def double_char(s):
    resultado = ""
    for char in s:
        resultado += char * 2
    return resultado


