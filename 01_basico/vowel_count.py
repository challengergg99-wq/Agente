def get_count(string):
    count = 0
    vowels = 'aeiouAEIOU'
    for char in string:
        if char in vowels:
            count += 1
    return count



def disemvowel(string_):
    vowels = 'aeiouAEIOU'
    for i in string_:
        if i in vowels:
            string_ = string_.replace(i, " ")
    return string_


def is_square(n):  
    if n < 0:
        return False
    test = int(n**0.5)
    return test * test == n


def square_sum(numbers):
    total = 0
    for i in numbers:
        resultado = int(i**2)
        total += resultado
    return total
print(square_sum([1, 2]))
    
    
# No floats or non-positive integers will be passed
def sum_two_smallest_numbers(numbers):
    sorted_numbers = sorted(numbers)
    return sorted_numbers[0] + sorted_numbers[1]







