texto = "hola mundo"
invertido = texto[::-1]
print(invertido)


# Complete the function that accepts a string parameter, and reverses each word in the string. All spaces in the string should be retained.

def reverse_words(text):
    # Split the text into words, reverse each word, and join them back together with spaces
    return ' '.join(word[::-1] for word in text.split(' '))