def is_pangram(s):
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    texto = s.lower()
    
    for letra in alfabeto:
        if letra not in texto:
            return False
    return True