import ast
import difflib
import sys
from collections import Counter
from pathlib import Path

import ollama

MODEL = "qwen2.5-coder:1.5b"  # ajusta al tag que descargaste con `ollama pull`

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
    """Analiza los docstrings ya existentes en el proyecto para inferir el estilo.

    Busca marcadores típicos de cada convención (Google, NumPy, reST) en los
    docstrings que YA existen en el código, y elige el más frecuente. Si no
    encuentra suficiente evidencia, usa Google por defecto.

    Args:
        archivos: Lista de archivos .py del proyecto a inspeccionar.

    Returns:
        Una de: "google", "numpy", "rest".
    """
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
            len(nodo.body) == 1
            and isinstance(primer_stmt, (ast.Pass,))
        ) or (
            len(nodo.body) == 1
            and isinstance(primer_stmt, ast.Expr)
            and isinstance(primer_stmt.value, ast.Constant)
            and primer_stmt.value.value is Ellipsis
        )

        codigo_del_nodo = ast.get_source_segment(codigo_fuente, nodo)

        encontrados.append({
            "nombre": nodo.name,
            "tipo": "función" if es_funcion else "clase",
            "linea_insercion": primer_stmt.lineno,
            "indentacion": " " * primer_stmt.col_offset,
            "codigo": codigo_del_nodo,
            "trivial": es_trivial,
        })

    encontrados.sort(key=lambda x: x["linea_insercion"], reverse=True)
    return encontrados


def generar_docstring(codigo: str, estilo: str) -> str:
    instrucciones_estilo = PLANTILLAS_ESTILO.get(estilo, PLANTILLAS_ESTILO["google"])
    system_prompt = (
        "Eres un asistente experto en documentar código Python. "
        "Tu única tarea es generar un docstring claro y conciso para el código dado. "
        f"{instrucciones_estilo} "
        "Responde ÚNICAMENTE con el texto del docstring (sin comillas triples, "
        "esas las agrega el programa), sin explicaciones adicionales, sin markdown."
    )

    respuesta = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": codigo},
        ],
    )
    texto = respuesta["message"]["content"].strip()
    return texto.strip('"').strip("'").strip()


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


def procesar_archivo(archivo: Path, aprobar_todo: bool, estilo: str, reporte: Counter) -> bool:
    """Analiza un archivo, propone docstrings y aplica los que se aprueben.

    Args:
        archivo: Path al archivo .py a procesar.
        aprobar_todo: Si es True, no pregunta y aplica todas las propuestas.
        estilo: Estilo de docstring a usar ("google", "numpy" o "rest").
        reporte: Counter compartido donde se acumulan las estadísticas finales.

    Returns:
        El valor actualizado de aprobar_todo (puede cambiar si el usuario
        elige "todo" durante la revisión de este archivo).
    """
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
            print(f"  (saltando '{item['nombre']}' — cuerpo trivial, no aporta documentar)")
            reporte["saltadas_trivial"] += 1
            continue

        print(f"\n  {item['tipo']} '{item['nombre']}' — generando propuesta ({estilo})...")
        docstring = generar_docstring(item["codigo"], estilo)
        bloque = construir_bloque_docstring(docstring, item["indentacion"])

        idx = item["linea_insercion"] - 1
        lineas_propuestas = (
            lineas_actuales[:idx]
            + [linea + "\n" for linea in bloque]
            + lineas_actuales[idx:]
        )

        mostrar_diff(lineas_actuales, lineas_propuestas, str(archivo))

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

    if aplicados_en_archivo > 0:
        archivo.write_text("".join(lineas_actuales), encoding="utf-8")
        print(f"  - {aplicados_en_archivo} docstring(s) escrito(s) en {archivo}")

    return aprobar_todo


def analizar_proyecto(ruta_proyecto: str) -> None:
    """Recorre un proyecto, detecta el estilo, documenta y muestra un reporte final.

    Args:
        ruta_proyecto: Ruta a la carpeta raíz del proyecto a documentar.
    """
    base = Path(ruta_proyecto)
    archivos_python = [
        f for f in base.rglob("*.py")
        if not any(parte in CARPETAS_IGNORADAS for parte in f.parts)
    ]

    if not archivos_python:
        print(f"No se encontraron archivos .py relevantes en {ruta_proyecto}")
        return

    estilo = detectar_estilo_docstrings(archivos_python)
    print(f"Estilo de docstring detectado en el proyecto: {estilo}")
    print(f"Analizando {len(archivos_python)} archivo(s) Python (ignorando {', '.join(CARPETAS_IGNORADAS)})...")

    aprobar_todo = False
    reporte = Counter()

    for archivo in archivos_python:
        aprobar_todo = procesar_archivo(archivo, aprobar_todo, estilo, reporte)

    total_encontradas = sum(reporte.values())
    print("\n" + "=" * 40)
    print("REPORTE FINAL")
    print("=" * 40)
    print(f"Estilo usado:              {estilo}")
    print(f"Total funciones/clases revisadas: {total_encontradas}")
    print(f"  - Documentadas:          {reporte['documentadas']}")
    print(f"  - Saltadas (triviales):  {reporte['saltadas_trivial']}")
    print(f"  - Saltadas (por ti):     {reporte['saltadas_usuario']}")
    print(f"  - Saltadas (error sintaxis en archivo): {reporte['saltadas_error_sintaxis']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python doc_agent.py /ruta/a/tu/proyecto")
        sys.exit(1)

    analizar_proyecto(sys.argv[1])