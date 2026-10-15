import base64
import zlib

texto = "hello world!"
magic = base64.b64encode(zlib.compress(texto.encode("utf-8")))

def greet():
    datos = base64.b64decode(magic, validate=True)
    return zlib.decompress(datos).decode("utf-8")

print(greet())