# ROT13 is a simple letter substitution cipher that replaces a letter with the letter 13 letters after it in the alphabet. ROT13 is an example of the Caesar cipher.

# Create a function that takes a string and returns the string ciphered with Rot13. If there are numbers or special characters included in the string, they should be returned as they are. Only letters from the latin/english alphabet should be shifted, like in the original Rot13 "implementation".



def rot13(message):
    result = ""
    for i in message:
        if i.isalpha():
            shift = 13
            if i.islower():
                base = ord('a')
            else:
                base = ord('A')
            new_char = chr((ord(i) - base + shift) % 26 + base)
            result += new_char
        else:
            result += i
    return result

print(rot13("Hello, World!"))  # Uryyb, Jbeyq!