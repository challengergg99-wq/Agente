import argparse
import ast
import difflib
import re
import sys
from collections import Counter
from pathlib import Path

import ollama

MODELO_POR_DEFECTO = "qwen2.5-coder:1.5b"

CARPETAS_IGNORADAS = {"venv", ".venv", "__pycache__", ".git", "tests", "test", "migrations", "build", "dist"}

PLANTILLAS_ESTILO = {
    "google": (
        "Genera el docstring en estilo Google: usa 'Args:', 'Returns:' y "
        "'Raises:' cuando aplique, con sangría de 4 espacios bajo cada sección."
    ),
    "numpy": (
        "Genera el docstring en estilo NumPy: usa encabezados 'Parameters', "
        "'Returns' subrayados con guiones ('----------') y cada parámetro en "
        "su propia línea con el formato 'nombre : tipo'."
    ),
    "rest": (
        "Genera el docstring en estilo reStructuredText: usa ':param nombre:', "
        "':type nombre:' y ':returns:' para cada elemento."
    ),
}


def detectar_estilo_docstrings(archivos: list[Path]) -> str:
    conteo = Counter()
    for archivo in archivos:
        try:
            codigo_fuente = archivo.read_text(encoding="utf-8")
            arbol = ast.parse(codigo_fuente)
        except (SyntaxError, UnicodeDecodeError):
            continue

        for nodo in ast.walk(arbol):
            if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            doc = ast.get_docstring(nodo)
            if not doc:
                continue
            if "-------" in doc or "Parameters" in doc:
                conteo["numpy"] += 1
            elif ":param" in doc or ":returns:" in doc:
                conteo["rest"] += 1
            elif "Args:" in doc or "Returns:" in doc:
                conteo["google"] += 1

    if not conteo:
        return "google"
    return conteo.most_common(1)[0][0]


def encontrar_funciones_sin_documentar(ruta_archivo: Path) -> list[dict]:
    codigo_fuente = ruta_archivo.read_text(encoding="utf-8")
    arbol = ast.parse(codigo_fuente, filename=str(ruta_archivo))

    encontrados = []
    for nodo in ast.walk(arbol):
        es_funcion = isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef))
        es_clase = isinstance(nodo, ast.ClassDef)
        if not (es_funcion or es_clase):
            continue
        if ast.get_docstring(nodo) is not None:
            continue
        if not nodo.body:
            continue

        primer_stmt = nodo.body[0]
        es_trivial = (
            len(nodo.body) == 1 and isinstance(primer_stmt, ast.Pass)
        ) or (
            len(nodo.body) == 1
            and isinstance(primer_stmt, ast.Expr)
            and isinstance(primer_stmt.value, ast.Constant)
            and primer_stmt.value.value is Ellipsis
        )

        encontrados.append({
            "nombre": nodo.name,
            "tipo": "función" if es_funcion else "clase",
            "linea_insercion": primer_stmt.lineno,
            "indentacion": " " * primer_stmt.col_offset,
            "codigo": ast.get_source_segment(codigo_fuente, nodo),
            "trivial": es_trivial,
        })

    encontrados.sort(key=lambda x: x["linea_insercion"], reverse=True)
    return encontrados


def generar_docstring(codigo: str, estilo: str, modelo: str) -> str:
    """Le pide al modelo local que genere un docstring en el estilo indicado.

    Args:
        codigo: El código fuente de la función o clase.
        estilo: Una de "google", "numpy", "rest" — determina el formato pedido.
        modelo: Nombre del modelo de Ollama a usar (ej. "qwen2.5-coder:7b").

    Returns:
        El docstring generado, limpio y sin comillas triples ni markdown.
    """
    instrucciones_estilo = PLANTILLAS_ESTILO.get(estilo, PLANTILLAS_ESTILO["google"])
    system_prompt = (
        "Eres un asistente experto en documentar código Python. "
        "Tu única tarea es generar el CONTENIDO de un docstring claro y conciso "
        "para el código dado. "
        f"{instrucciones_estilo}\n\n"
        "Reglas estrictas, sin excepción:\n"
        "1. Responde SOLO con el texto del docstring. Nada de comillas triples "
        "(las agrega el programa), nada de bloques markdown (nunca uses ```).\n"
        "2. NO repitas ni reescribas el código de la función. Solo el docstring.\n"
        "3. Incluye una sección 'Raises' ÚNICAMENTE si el código tiene un "
        "'raise' explícito. Si el código no lanza excepciones, NO inventes una "
        "sección Raises.\n"
        "4. No agregues explicaciones antes o después del docstring.\n\n"
        "Ejemplo de una respuesta correcta para una función que suma dos números:\n"
        "Suma dos números y devuelve el resultado.\n\n"
        "Args:\n"
        "    a: Primer número.\n"
        "    b: Segundo número.\n\n"
        "Returns:\n"
        "    La suma de a y b."
    )

    respuesta = ollama.chat(
        model=modelo,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": codigo},
        ],
        options={"temperature": 0.1},
    )
    return limpiar_docstring_generado(respuesta["message"]["content"])


def limpiar_docstring_generado(texto_crudo: str) -> str:
    """Limpia la respuesta cruda del modelo hasta dejar solo el docstring.

    Args:
        texto_crudo: La respuesta tal cual la devolvió el modelo.

    Returns:
        El texto del docstring, limpio y sin indentación sobrante.
    """
    texto = texto_crudo.strip()
    texto = re.sub(r"^```[a-zA-Z]*\n?", "", texto)
    texto = re.sub(r"\n?```$", "", texto).strip()

    match = re.search(r'"""(.*?)"""', texto, re.DOTALL) or re.search(r"'''(.*?)'''", texto, re.DOTALL)
    contenido = match.group(1) if match else texto

    lineas = contenido.strip("\n").splitlines()
    lineas_no_vacias = [l for l in lineas if l.strip()]
    if lineas_no_vacias:
        indent_min = min(len(l) - len(l.lstrip()) for l in lineas_no_vacias)
        lineas = [l[indent_min:] if len(l) >= indent_min else l.strip() for l in lineas]

    return "\n".join(lineas).strip()


def construir_bloque_docstring(docstring: str, indentacion: str) -> list[str]:
    lineas_doc = docstring.splitlines() or [docstring]
    bloque = [f'{indentacion}"""{lineas_doc[0]}']
    for linea in lineas_doc[1:]:
        bloque.append(f"{indentacion}{linea}" if linea.strip() else "")
    bloque.append(f'{indentacion}"""')
    return bloque


def mostrar_diff(lineas_originales: list[str], lineas_nuevas: list[str], archivo: str) -> None:
    diff = difflib.unified_diff(
        lineas_originales, lineas_nuevas,
        fromfile=f"{archivo} (original)",
        tofile=f"{archivo} (propuesto)",
        lineterm="",
    )
    for linea in diff:
        print(linea)


def procesar_archivo(
    archivo: Path, aprobar_todo: bool, estilo: str, modelo: str, dry_run: bool, reporte: Counter
) -> bool:
    try:
        sin_documentar = encontrar_funciones_sin_documentar(archivo)
    except SyntaxError as error:
        print(f"[AVISO] No se pudo parsear {archivo}: {error}")
        reporte["saltadas_error_sintaxis"] += 1
        return aprobar_todo

    if not sin_documentar:
        return aprobar_todo

    lineas_actuales = archivo.read_text(encoding="utf-8").splitlines(keepends=True)
    aplicados_en_archivo = 0

    print(f"\n── {archivo} ──")

    for item in sin_documentar:
        if item["trivial"]:
            print(f"  (saltando '{item['nombre']}' — cuerpo trivial)")
            reporte["saltadas_trivial"] += 1
            continue

        print(f"\n  {item['tipo']} '{item['nombre']}' — generando propuesta ({estilo}, {modelo})...")
        docstring = generar_docstring(item["codigo"], estilo, modelo)
        bloque = construir_bloque_docstring(docstring, item["indentacion"])

        idx = item["linea_insercion"] - 1
        lineas_propuestas = (
            lineas_actuales[:idx] + [linea + "\n" for linea in bloque] + lineas_actuales[idx:]
        )

        mostrar_diff(lineas_actuales, lineas_propuestas, str(archivo))

        if dry_run:
            reporte["propuestas_dry_run"] += 1
            continue

        if not aprobar_todo:
            respuesta = input("\n  ¿Aplicar este cambio? [s]í / [n]o / [t]odo el resto / [c]ancelar: ").strip().lower()
            if respuesta == "c":
                print("Cancelado por el usuario.")
                if aplicados_en_archivo > 0:
                    archivo.write_text("".join(lineas_actuales), encoding="utf-8")
                sys.exit(0)
            if respuesta == "t":
                aprobar_todo = True
            elif respuesta != "s":
                reporte["saltadas_usuario"] += 1
                continue

        lineas_actuales = lineas_propuestas
        aplicados_en_archivo += 1
        reporte["documentadas"] += 1

    if aplicados_en_archivo > 0 and not dry_run:
        archivo.write_text("".join(lineas_actuales), encoding="utf-8")
        print(f"  - {aplicados_en_archivo} docstring(s) escrito(s) en {archivo}")

    return aprobar_todo


def analizar_proyecto(ruta_proyecto: str, args: argparse.Namespace) -> None:
    """Recorre un proyecto, detecta el estilo, documenta y muestra un reporte final.

    Args:
        ruta_proyecto: Ruta a la carpeta raíz del proyecto a documentar.
        args: Argumentos ya parseados de la línea de comandos.
    """
    base = Path(ruta_proyecto)
    archivos_python = [
        f for f in base.rglob("*.py") if not any(parte in CARPETAS_IGNORADAS for parte in f.parts)
    ]

    if not archivos_python:
        print(f"No se encontraron archivos .py relevantes en {ruta_proyecto}")
        return

    estilo = args.estilo if args.estilo != "auto" else detectar_estilo_docstrings(archivos_python)
    print(f"Estilo de docstring: {estilo}{' (auto-detectado)' if args.estilo == 'auto' else ' (forzado)'}")
    print(f"Modelo: {args.modelo}")
    if args.dry_run:
        print("Modo DRY-RUN: no se escribirá ningún archivo, solo se mostrarán propuestas.")
    print(f"Analizando {len(archivos_python)} archivo(s) (ignorando {', '.join(CARPETAS_IGNORADAS)})...")

    aprobar_todo = args.yes
    reporte = Counter()

    for archivo in archivos_python:
        aprobar_todo = procesar_archivo(archivo, aprobar_todo, estilo, args.modelo, args.dry_run, reporte)

    total_encontradas = sum(reporte.values())
    print("\n" + "=" * 40)
    print("REPORTE FINAL")
    print("=" * 40)
    print(f"Estilo usado:              {estilo}")
    print(f"Total funciones/clases revisadas: {total_encontradas}")
    if args.dry_run:
        print(f"  - Propuestas (dry-run, sin escribir): {reporte['propuestas_dry_run']}")
    else:
        print(f"  - Documentadas:          {reporte['documentadas']}")
        print(f"  - Saltadas (por ti):     {reporte['saltadas_usuario']}")
    print(f"  - Saltadas (triviales):  {reporte['saltadas_trivial']}")
    print(f"  - Saltadas (error sintaxis en archivo): {reporte['saltadas_error_sintaxis']}")


def construir_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos de línea de comandos.

    Returns:
        El ArgumentParser configurado con todas las opciones del agente.
    """
    parser = argparse.ArgumentParser(
        prog="doc_agent",
        description="Agente local (Ollama) que documenta código Python automáticamente.",
    )
    parser.add_argument("ruta", help="Ruta a la carpeta del proyecto a documentar")
    parser.add_argument(
        "--modelo", default=MODELO_POR_DEFECTO,
        help=f"Modelo de Ollama a usar (default: {MODELO_POR_DEFECTO})",
    )
    parser.add_argument(
        "--estilo", choices=["auto", "google", "numpy", "rest"], default="auto",
        help="Estilo de docstring a usar (default: auto-detecta del proyecto)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Muestra las propuestas sin escribir ningún archivo",
    )
    parser.add_argument(
        "--yes", action="store_true",
        help="Aprueba todos los cambios automáticamente, sin preguntar (útil en CI)",
    )
    return parser


if __name__ == "__main__":
    parser = construir_parser()
    args = parser.parse_args()
    analizar_proyecto(args.ruta, args)