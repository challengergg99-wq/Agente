import ast
import sys
from pathlib import Path

import ollama

MODEL = "qwen2.5-coder:1.5b"  

SYSTEM_PROMPT = """Eres un asistente experto en documentar código Python.
Tu única tarea es generar un docstring claro y conciso para la función o clase
que te doy, siguiendo el estilo Google (Args, Returns, Raises si aplica).
Responde ÚNICAMENTE con el docstring, sin explicaciones adicionales,
sin markdown, sin comillas triples adicionales fuera del docstring en sí.
"""


def encontrar_funciones_sin_documentar(ruta_archivo: Path) -> list[dict]:
    """Parsea un archivo .py y devuelve funciones/clases sin docstring.

    Args:
        ruta_archivo: Path al archivo .py a analizar.

    Returns:
        Lista de dicts con: nombre, tipo, línea, y el código fuente del nodo.
    """
    codigo_fuente = ruta_archivo.read_text(encoding="utf-8")
    arbol = ast.parse(codigo_fuente, filename=str(ruta_archivo))

    encontrados = []
    for nodo in ast.walk(arbol):
        es_funcion = isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef))
        es_clase = isinstance(nodo, ast.ClassDef)

        if not (es_funcion or es_clase):
            continue

        tiene_docstring = ast.get_docstring(nodo) is not None
        if tiene_docstring:
            continue

        codigo_del_nodo = ast.get_source_segment(codigo_fuente, nodo)
        encontrados.append({
            "nombre": nodo.name,
            "tipo": "función" if es_funcion else "clase",
            "linea": nodo.lineno,
            "codigo": codigo_del_nodo,
        })

    return encontrados


def generar_docstring(codigo: str) -> str:
    """Le pide al modelo local que genere un docstring para el código dado.

    Args:
        codigo: El código fuente de la función o clase.

    Returns:
        El docstring generado por el modelo, como texto plano.
    """
    respuesta = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": codigo},
        ],
    )
    return respuesta["message"]["content"].strip()


def analizar_proyecto(ruta_proyecto: str) -> None:
    """Recorre un proyecto, encuentra código sin documentar y muestra propuestas.

    Args:
        ruta_proyecto: Ruta a la carpeta raíz del proyecto a documentar.
    """
    base = Path(ruta_proyecto)
    archivos_python = list(base.rglob("*.py"))

    if not archivos_python:
        print(f"No se encontraron archivos .py en {ruta_proyecto}")
        return

    print(f"Analizando {len(archivos_python)} archivo(s) Python...\n")

    total_sin_documentar = 0

    for archivo in archivos_python:
        try:
            sin_documentar = encontrar_funciones_sin_documentar(archivo)
        except SyntaxError as error:
            print(f"[AVISO] No se pudo parsear {archivo}: {error}")
            continue

        if not sin_documentar:
            continue

        print(f"── {archivo} ──")
        for item in sin_documentar:
            total_sin_documentar += 1
            print(f"\n  {item['tipo']} '{item['nombre']}' (línea {item['linea']}) — SIN docstring")
            print("  Generando propuesta con el modelo local...")

            docstring_propuesto = generar_docstring(item["codigo"])

            print(f"  Propuesta:\n")
            for linea in docstring_propuesto.splitlines():
                print(f"      {linea}")
        print()

    print(f"Total encontrado sin documentar: {total_sin_documentar}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python doc_agent.py /ruta/a/tu/proyecto")
        sys.exit(1)

    analizar_proyecto(sys.argv[1])