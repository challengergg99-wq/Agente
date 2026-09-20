# Task
# Sum all the numbers of a given array ( cq. list ), except the highest and the lowest element ( by value, not by index! ).

# The highest or lowest element respectively is a single element at each edge, even if there are more than one with the same value.

# Mind the input validation.

def sum_array(arr):
    if arr is None or len(arr) < 3:
        return 0
    return sum(arr) - max(arr) - min(arr)

print(sum_array([6, 2, 1, 8, 10]))  # Output: 16