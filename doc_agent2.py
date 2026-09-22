import argparse
import ast
import difflib
import os
import sys
from collections import Counter
from pathlib import Path

try:
    import ollama
except ImportError:  # pragma: no cover - depende del entorno de ejecución
    ollama = None

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b")

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


def _normalizar_estilo(estilo: str | None) -> str:
    estilo = (estilo or "google").lower()
    return estilo if estilo in PLANTILLAS_ESTILO else "google"


def _resumen_desde_nombre(nombre: str) -> str:
    if not nombre:
        return "Realiza la operación solicitada."
    nombre = nombre.replace("_", " ").strip()
    if "" not in nombre:
        return f"Ejecuta la lógica de {nombre}."
    nombre_limpio = nombre.split()[0]
    if nombre_limpio.lower() in {"__init__", "__enter__", "__exit__"}:
        return "Inicializa el estado del objeto."
    return f"Ejecuta la lógica de {nombre}."


def detectar_estilo_docstrings(archivos: list[Path]) -> str:
    """Detecta el estilo dominante de docstrings del proyecto."""
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
    """Devuelve funciones y clases sin docstring en la posición correcta para inyectarlos."""
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

        codigo_del_nodo = ast.get_source_segment(codigo_fuente, nodo)
        encontrados.append(
            {
                "nombre": nodo.name,
                "tipo": "función" if es_funcion else "clase",
                "linea_insercion": primer_stmt.lineno,
                "indentacion": " " * primer_stmt.col_offset,
                "codigo": codigo_del_nodo or "",
                "trivial": es_trivial,
            }
        )

    encontrados.sort(key=lambda x: x["linea_insercion"], reverse=True)
    return encontrados


def _extraer_nodo_desde_codigo(codigo: str):
    try:
        arbol = ast.parse(codigo)
    except SyntaxError:
        return None
    return arbol.body[0] if arbol.body else None


def _generar_fallback_docstring(codigo: str, estilo: str) -> str:
    nodo = _extraer_nodo_desde_codigo(codigo)
    if nodo is None:
        return "Documento la lógica de esta sección con una descripción clara y precisa."

    def _descripcion_arg(arg_name: str) -> str:
        return f"Descripción del parámetro {arg_name}."

    if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
        resumen = _resumen_desde_nombre(nodo.name)
        argumentos = []
        for arg in nodo.args.posonlyargs + nodo.args.args + nodo.args.kwonlyargs:
            argumentos.append(f"    {arg.arg}: {_descripcion_arg(arg.arg)}")
        if nodo.args.vararg:
            argumentos.append(f"    {nodo.args.vararg.arg}: Argumentos variables adicionales.")
        if nodo.args.kwarg:
            argumentos.append(f"    {nodo.args.kwarg.arg}: Argumentos de palabra clave adicionales.")

        if estilo == "numpy":
            lineas = [resumen, "", "Parameters", "----------"]
            if argumentos:
                lineas.extend(f"{arg.split(':', 1)[0]} : {' '.join(arg.split(':', 1)[1:]).strip()}" for arg in argumentos)
            else:
                lineas.append("None")
            lineas.extend(["", "Returns", "-------", "resultado : Any", "    Resultado de la operación."])
            return "\n".join(lineas)

        if estilo == "rest":
            lineas = [resumen, ""]
            if argumentos:
                for arg in argumentos:
                    nombre, _, desc = arg.partition(":")
                    lineas.append(f":param {nombre.strip()}: {desc.strip()}")
            lineas.append(":returns: Resultado de la operación.")
            return "\n".join(lineas)

        lineas = [resumen, ""]
        if argumentos:
            lineas.append("Args:")
            lineas.extend(f"    {arg}" for arg in argumentos)
            lineas.append("")
        lineas.append("Returns:")
        lineas.append("    Resultado de la operación.")
        return "\n".join(lineas)

    if isinstance(nodo, ast.ClassDef):
        resumen = f"Representa una {nodo.name.lower()} del sistema."
        if estilo == "numpy":
            return f"{resumen}\n\nAttributes\n----------\nNone\n    No hay atributos documentados de forma específica."
        if estilo == "rest":
            return f"{resumen}\n\n:attribute: Representa la entidad asociada al tipo {nodo.name}."
        return f"{resumen}\n\nAttributes:\n    None: No hay atributos documentados de forma específica."

    return "Documenta la intención y el comportamiento de esta sección de forma clara."


def generar_docstring(codigo: str, estilo: str) -> str:
    """Genera el contenido de un docstring usando LLM si está disponible y cae a heurística segura."""
    estilo = _normalizar_estilo(estilo)
    instrucciones_estilo = PLANTILLAS_ESTILO.get(estilo, PLANTILLAS_ESTILO["google"])
    system_prompt = (
        "Eres un asistente experto en documentar código Python. "
        "Tu única tarea es generar el CONTENIDO de un docstring claro y conciso "
        "para el código dado. "
        f"{instrucciones_estilo}\n\n"
        "Reglas estrictas, sin excepción:\n"
        "1. Responde SOLO con el texto del docstring. Nada de comillas triples ni markdown.\n"
        "2. NO repitas ni reescribas el código de la función. Solo el docstring.\n"
        "3. Incluye 'Raises' sólo si el código tiene raise explícito.\n"
        "4. No agregues explicaciones antes o después del docstring.\n"
        "5. Mantén el docstring en español, claro y profesional.\n"
        "6. Si el código no tiene parámetros, no incluyas 'Args:'.\n"
        "7. Si el código no tiene retorno, no incluyas 'Returns:'.\n"
    )

    fallback = _generar_fallback_docstring(codigo, estilo)
    if ollama is None:
        return fallback

    try:
        respuesta = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": codigo},
            ],
        )
        texto = respuesta["message"]["content"].strip()
        texto_limpio = texto.strip('"').strip("'").strip()
        if texto_limpio and not texto_limpio.startswith("```"):
            return texto_limpio
    except Exception:
        pass

    return fallback


def construir_bloque_docstring(docstring: str, indentacion: str) -> list[str]:
    lineas_doc = docstring.splitlines() or [docstring]
    bloque = [f'{indentacion}"""{lineas_doc[0]}']
    for linea in lineas_doc[1:]:
        bloque.append(f"{indentacion}{linea}" if linea.strip() else "")
    bloque.append(f'{indentacion}"""')
    return bloque


def mostrar_diff(lineas_originales: list[str], lineas_nuevas: list[str], archivo: str) -> None:
    diff = difflib.unified_diff(
        lineas_originales,
        lineas_nuevas,
        fromfile=f"{archivo} (original)",
        tofile=f"{archivo} (propuesto)",
        lineterm="",
    )
    for linea in diff:
        print(linea)


def procesar_archivo(archivo: Path, aprobar_todo: bool, estilo: str, reporte: Counter, dry_run: bool = False) -> bool:
    """Procesa un archivo y aplica docstrings aprobados por el usuario o por aprobación global."""
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

        idx = max(item["linea_insercion"] - 1, 0)
        lineas_propuestas = lineas_actuales[:idx] + [linea + "\n" for linea in bloque] + lineas_actuales[idx:]

        mostrar_diff(lineas_actuales, lineas_propuestas, str(archivo))

        if dry_run:
            print("  [dry-run] sin aplicar cambios")
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


def analizar_proyecto(ruta_proyecto: str, aprobar_todo: bool = False, estilo: str | None = None, dry_run: bool = False) -> Counter:
    """Recorre un proyecto y genera la documentación solicitada."""
    base = Path(ruta_proyecto)
    if not base.exists():
        raise FileNotFoundError(f"La ruta '{ruta_proyecto}' no existe.")

    archivos_python = [
        f for f in base.rglob("*.py")
        if f.is_file() and not any(parte in CARPETAS_IGNORADAS for parte in f.parts)
    ]

    if not archivos_python:
        print(f"No se encontraron archivos .py relevantes en {ruta_proyecto}")
        return Counter()

    estilo_detectado = detectar_estilo_docstrings(archivos_python)
    estilo_final = _normalizar_estilo(estilo or estilo_detectado)
    print(f"Estilo de docstring detectado en el proyecto: {estilo_final}")
    print(f"Analizando {len(archivos_python)} archivo(s) Python (ignorando {', '.join(sorted(CARPETAS_IGNORADAS))})...")

    reporte = Counter()
    for archivo in archivos_python:
        aprobar_todo = procesar_archivo(archivo, aprobar_todo, estilo_final, reporte, dry_run=dry_run)

    total_encontradas = sum(reporte.values())
    print("\n" + "=" * 40)
    print("REPORTE FINAL")
    print("=" * 40)
    print(f"Estilo usado:              {estilo_final}")
    print(f"Total funciones/clases revisadas: {total_encontradas}")
    print(f"  - Documentadas:          {reporte['documentadas']}")
    print(f"  - Saltadas (triviales):  {reporte['saltadas_trivial']}")
    print(f"  - Saltadas (por ti):     {reporte['saltadas_usuario']}")
    print(f"  - Saltadas (error sintaxis en archivo): {reporte['saltadas_error_sintaxis']}")
    return reporte


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Documenta funciones y clases Python con estilo consistente.")
    parser.add_argument("ruta_proyecto", help="Ruta a la carpeta raíz del proyecto a documentar.")
    parser.add_argument("--estilo", choices=sorted(PLANTILLAS_ESTILO), help="Estilo de docstring a forzar.")
    parser.add_argument("--aprobar-todo", action="store_true", help="Aplía automáticamente todos los cambios sugeridos.")
    parser.add_argument("--dry-run", action="store_true", help="Muestra el diff sin modificar archivos.")
    parser.add_argument("--modelo", default=MODEL, help="Modelo de Ollama a usar para la generación de docstrings.")
    args = parser.parse_args(argv)

    # global MODEL
    # MODEL = args.modelo

    try:
        analizar_proyecto(args.ruta_proyecto, aprobar_todo=args.aprobar_todo, estilo=args.estilo, dry_run=args.dry_run)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())