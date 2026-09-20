#$O(n^2)$)
def duplicate(word):
    word = word.lower()
    result = ""
    for char in word:
        if word.count(char) > 1:
            result += ")"
        else:
            result += "("
    return result

print(duplicate("holaa"))


#($O(n)$), 
def duplicate(word):
    word = word.lower()
    conteo = word.count()
    resultado = ""
    for i in word:
        if conteo[i] > 0:
            resultado += ")"
        else:
            resultado += "("
    return resultado