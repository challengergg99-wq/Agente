def find_the_odd(seq):
    for num in seq:
        if seq.count(num) % 2 != 0:
            return num


print(find_the_odd([20, 1, 1, 2, 2, 3, 3, 5, 5, 4, 4, 6, 6]))


from functools import reduce
import operator

def find_the_odd(seq):
    return reduce(operator.xor, seq)