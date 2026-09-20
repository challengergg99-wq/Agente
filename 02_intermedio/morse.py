textonatural = "comidad para humanos"
textotomorse = "-.-. --- -- .. -.. .- -.. / .--. .- .-. .- / .... ..- -- .- -. --- ..."

# Diccionario completo (letras, dígitos y símbolos comunes)
dict_morse = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# Inversa para decodificar morse => texto
inverse_morse = {v: k for k, v in dict_morse.items()}


def text_to_morse(text):
    """Convierte texto a código Morse. Espacios entre letras y '/' entre palabras."""
    if not isinstance(text, str):
        raise TypeError('Se esperaba una cadena')
    text = text.upper()
    parts = []
    for ch in text:
        morse = dict_morse.get(ch)
        if morse:
            parts.append(morse)
        else:
            parts.append('?')
    return ' '.join(parts)


def morse_to_text(morse):
    """Convierte código Morse a texto. Usa '/' para separar palabras."""
    if not isinstance(morse, str):
        raise TypeError('Se esperaba una cadena')
    tokens = morse.split()
    out_chars = []
    for tok in tokens:
        if tok == '/':
            out_chars.append(' ')
        else:
            ch = inverse_morse.get(tok)
            out_chars.append(ch if ch is not None else '?')
    return ''.join(out_chars).lower()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Codificar/decodificar Morse')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encode', metavar='TEXT', help='Texto a convertir a Morse')
    group.add_argument('-d', '--decode', metavar='MORSE', help='Morse a convertir a texto')
    args = parser.parse_args()


    if args.encode:
        print(text_to_morse(args.encode))
    elif args.decode:
        print(morse_to_text(args.decode))
    else:
        # modo detect automatico: si contiene solo . - / y espacios -> decodificar
        import sys
        data = ' '.join(sys.argv[1:]).strip()
        if data:
            if all(c in '.-/ 0123456789' or c.isalpha() for c in data) and any(c in '.-' for c in data):
                print(morse_to_text(data))
            else:
                print(text_to_morse(data))
        else:
            # Modo interactivo
            try:
                while True:
                    mode = input('Elija (E)ncode, (D)ecode o (Q)uit: ').strip().lower()
                    if not mode:
                        continue
                    if mode.startswith('q'):
                        break
                    if mode.startswith('e'):
                        txt = input('Texto a convertir a Morse: ')
                        print(text_to_morse(txt))
                    elif mode.startswith('d'):
                        mor = input("Morse a convertir a texto (use '/' para espacios entre palabras): ")
                        print(morse_to_text(mor))
                    else:
                        print('Opción desconocida. Use E, D o Q.')
            except (EOFError, KeyboardInterrupt):
                print('\nSaliendo...')