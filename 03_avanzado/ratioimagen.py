import urllib.request
import struct
import io
import math


def aspect_ratio_from_url(url: str) -> str:
    """Descarga la imagen desde `url` y devuelve el aspect ratio reducido como 'W:H'.

    Soporta PNG, JPEG y GIF.
    """
    with urllib.request.urlopen(url) as resp:
        data = resp.read()

    def _get_size(data_bytes: bytes):
        # PNG
        if data_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            # IHDR chunk: width and height are 4 bytes each big-endian at offset 16
            if len(data_bytes) >= 24:
                width, height = struct.unpack('>II', data_bytes[16:24])
                return width, height
        # GIF
        if data_bytes[:6] in (b'GIF87a', b'GIF89a'):
            width, height = struct.unpack('<HH', data_bytes[6:10])
            return width, height
        # JPEG: search for SOF0/SOF2 marker
        if data_bytes.startswith(b'\xff\xd8'):
            i = 2
            length = len(data_bytes)
            while i < length:
                if data_bytes[i] != 0xFF:
                    i += 1
                    continue
                # skip padding FFs
                while i < length and data_bytes[i] == 0xFF:
                    i += 1
                if i >= length:
                    break
                marker = data_bytes[i]
                i += 1
                # markers without length
                if marker == 0xD8 or marker == 0xD9:
                    continue
                if i + 1 >= length:
                    break
                seg_len = struct.unpack('>H', data_bytes[i:i+2])[0]
                if seg_len < 2:
                    break
                # SOF0, SOF1, SOF2 markers contain size
                if marker in (0xC0, 0xC1, 0xC2, 0xC3,
                              0xC5, 0xC6, 0xC7,
                              0xC9, 0xCA, 0xCB,
                              0xCD, 0xCE, 0xCF):
                    if i + 5 < length:
                        # precision = data[i+2], height = next two, width = next two
                        height = struct.unpack('>H', data[i+3:i+5])[0]
                        width = struct.unpack('>H', data[i+5:i+7])[0]
                        return width, height
                    else:
                        break
                # skip segment
                i += seg_len
        raise ValueError('Formato de imagen no soportado o no se pudieron leer dimensiones')

    width, height = _get_size(data)
    if width == 0 or height == 0:
        raise ValueError('Dimensiones no válidas')

    g = math.gcd(width, height)
    return f"{width//g}:{height//g}"


if __name__ == '__main__':
    ejemplo = 'https://raw.githubusercontent.com/mouredevmouredev/master/mouredev_github_profile.png'
    try:
        print('URL:', ejemplo)
        print('Aspect ratio:', aspect_ratio_from_url(ejemplo))
    except Exception as e:
        print('Error:', e)
        
ratio = "https://raw.githubusercontent.com/mouredevmouredev/master/mouredev_github_profile.png"
with open("ratioimagen.py", "w") as file:
    file.write(ratio)
import urllib.request
import struct
import io
import math


def aspect_ratio_from_url(url: str) -> str:
    """Descarga la imagen desde `url` y devuelve el aspect ratio reducido como 'W:H'.

    Soporta PNG, JPEG y GIF.
    """
    with urllib.request.urlopen(url) as resp:
        data = resp.read()

    def _get_size(data_bytes: bytes):
        # PNG
        if data_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            # IHDR chunk: width and height are 4 bytes each big-endian at offset 16
            if len(data_bytes) >= 24:
                width, height = struct.unpack('>II', data_bytes[16:24])
                return width, height
        # GIF
        if data_bytes[:6] in (b'GIF87a', b'GIF89a'):
            width, height = struct.unpack('<HH', data_bytes[6:10])
            return width, height
        # JPEG: search for SOF0/SOF2 marker
        if data_bytes.startswith(b'\xff\xd8'):
            i = 2
            length = len(data_bytes)
            while i < length:
                if data_bytes[i] != 0xFF:
                    i += 1
                    continue
                # skip padding FFs
                while i < length and data_bytes[i] == 0xFF:
                    i += 1
                if i >= length:
                    break
                marker = data_bytes[i]
                i += 1
                # markers without length
                if marker == 0xD8 or marker == 0xD9:
                    continue
                if i + 1 >= length:
                    break
                seg_len = struct.unpack('>H', data_bytes[i:i+2])[0]
                if seg_len < 2:
                    break
                # SOF0, SOF1, SOF2 markers contain size
                if marker in (0xC0, 0xC1, 0xC2, 0xC3,
                              0xC5, 0xC6, 0xC7,
                              0xC9, 0xCA, 0xCB,
                              0xCD, 0xCE, 0xCF):
                    if i + 5 < length:
                        # precision = data[i+2], height = next two, width = next two
                        height = struct.unpack('>H', data[i+3:i+5])[0]
                        width = struct.unpack('>H', data[i+5:i+7])[0]
                        return width, height
                    else:
                        break
                # skip segment
                i += seg_len
        raise ValueError('Formato de imagen no soportado o no se pudieron leer dimensiones')

    width, height = _get_size(data)
    if width == 0 or height == 0:
        raise ValueError('Dimensiones no válidas')

    g = math.gcd(width, height)
    return f"{width//g}:{height//g}"


if __name__ == '__main__':
    ejemplo = 'https://raw.githubusercontent.com/mouredevmouredev/master/mouredev_github_profile.png'
    try:
        print('URL:', ejemplo)
        print('Aspect ratio:', aspect_ratio_from_url(ejemplo))
    except Exception as e:
        print('Error:', e)