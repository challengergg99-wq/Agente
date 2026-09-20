def es_anagrama(a: str, b: str) -> bool:
    if a is None or b is None:
        return False
    a_clean = "".join(c for c in a.lower() if c.isalnum())
    b_clean = "".join(k for k in b.lower() if k.isalnum())
    if len(a_clean) != len(b_clean):
        return False
    return sorted(a_clean) == sorted(b_clean)

print(es_anagrama("hola", "roma"))  # True




# if __name__ == "__main__":
#     casos = [
#         ("amor", "roma", True),
#         ("amor", "amor", False),
#         ("listen", "silent", True),
#         ("Dormitory", "dirty room", True),
#         ("hello", "bello", False),
#         ("aab", "aba", True),
#     ]
#     for x, y, esperado in casos:
#         resultado = es_anagrama(x, y)
#         print(f"{x!r} , {y!r} -> {resultado} (esperado: {esperado})")
