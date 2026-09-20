# Implement a pseudo-encryption algorithm which given a string S and an integer N concatenates all the odd-indexed characters of S with all the even-indexed characters of S, this process should be repeated N times.

# Together with the encryption function, you should also implement a decryption function which reverses the process.

# If the string S is an empty value or the integer N is not positive, return the first argument without changes.

from itertools import zip_longest


def encrypt(encrypted_text,n):
    if not encrypted_text or n <= 0:
        return encrypted_text

    for _ in range(n):
        impar = encrypted_text[1::2]
        par = encrypted_text[0::2]
        encrypted_text = par + impar
    return encrypted_text

print(encrypt("This is a test!", 1))  # "hsi  etTi sats!"


def decrypt(encrypted_text, n):
    if not encrypted_text or n <= 0:
        return encrypted_text

    for _ in range(n):
        mid = len(encrypted_text) // 2
        impares = encrypted_text[:mid]
        pares = encrypted_text[mid:]
        decrypted_text = []
        
        for par,impar in zip_longest(pares, impares, fillvalue=''):
            decrypted_text.append(par)
            decrypted_text.append(impar)  
            encrypted_text = ''.join(decrypted_text)      
    return ''.join(decrypted_text)


print(decrypt("hsi  etTi sats!", 1))  # "This is a test!"

print(decrypt(encrypt("01234", 1), 1))