"""
github_docs_pr.py — Documenta código Python con Ollama y abre un Pull Request
en GitHub usando el GitHub MCP Server.

Flujo (determinista; el modelo SOLO redacta docstrings):
  1. Busca funciones/clases sin docstring en la carpeta indicada (ast)
  2. Genera docstrings con Ollama y los inserta en memoria
  3. Te muestra un resumen y pide UNA confirmación
  4. Con git local: crea rama, commit y push
  5. Con el GitHub MCP Server: crea el Pull Request

Por qué git local para la rama y MCP para el PR: subir archivos vía API exige
manejar SHAs de cada archivo, y git ya resuelve eso con tus credenciales.
MCP aporta lo que git solo no puede: crear el PR en GitHub.

Requisitos:
    pip install mcp ollama python-dotenv
    docker pull ghcr.io/github/github-mcp-server
    .env.local con GITHUB_PERSONAL_ACCESS_TOKEN=...

Uso:
    python github_docs_pr.py ./01_basico --owner TU_USUARIO --repo TU_REPO
    python github_docs_pr.py --listar-tools          # ver nombres/esquemas reales
"""

import argparse
import ast
import asyncio
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import ollama
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv(".env.local")

MODELO = "qwen2.5-coder:7b"
IGNORAR = {"venv", ".venv", "__pycache__", ".git", "tests", "node_modules"}

SYSTEM_PROMPT = (
    "Eres un experto en documentar código Python. Genera SOLO el contenido de un "
    "docstring estilo Google (Args, Returns; Raises solo si hay un 'raise' explícito). "
    "Sin comillas triples, sin markdown, sin repetir el código, sin explicaciones."
)



def limpiar(texto: str) -> str:
    """Quita markdown, código repetido e indentación sobrante de la respuesta del modelo.

    Args:
        texto: Respuesta cruda del modelo.

    Returns:
        El contenido del docstring, limpio.
    """
    texto = re.sub(r"^```[a-zA-Z]*\n?", "", texto.strip())
    texto = re.sub(r"\n?```$", "", texto).strip()
    m = re.search(r'"""(.*?)"""', texto, re.DOTALL)
    cuerpo = (m.group(1) if m else texto).strip("\n").splitlines()
    con_texto = [l for l in cuerpo if l.strip()]
    if con_texto:
        sangria = min(len(l) - len(l.lstrip()) for l in con_texto)
        cuerpo = [l[sangria:] if l.strip() else "" for l in cuerpo]
    return "\n".join(cuerpo).strip()


def generar_docstring(codigo: str, modelo: str) -> str:
    """Pide al modelo local un docstring para el código dado.

    Args:
        codigo: Código fuente de la función o clase.
        modelo: Nombre del modelo de Ollama.

    Returns:
        Docstring limpio, sin comillas triples.
    """
    r = ollama.chat(
        model=modelo,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": codigo}],
        options={"temperature": 0.1},
    )
    return limpiar(r["message"]["content"])


def documentar_archivo(ruta: Path, modelo: str) -> int:
    """Inserta docstrings en las funciones/clases sin documentar de un archivo.

    Args:
        ruta: Archivo .py a modificar (se reescribe solo si hubo cambios).
        modelo: Modelo de Ollama a usar.

    Returns:
        Cantidad de docstrings agregados.
    """
    fuente = ruta.read_text(encoding="utf-8")
    try:
        arbol = ast.parse(fuente)
    except SyntaxError:
        print(f"  [aviso] sintaxis inválida, se omite: {ruta}")
        return 0

    nodos = [
        n for n in ast.walk(arbol)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and ast.get_docstring(n) is None and n.body
        and not (len(n.body) == 1 and isinstance(n.body[0], ast.Pass))
    ]
    if not nodos:
        return 0

    lineas = fuente.splitlines(keepends=True)
    for n in sorted(nodos, key=lambda x: x.body[0].lineno, reverse=True):
        doc = generar_docstring(ast.get_source_segment(fuente, n), modelo)
        if not doc:
            continue
        sangria = " " * n.body[0].col_offset
        doc_lineas = doc.splitlines()
        bloque = [f'{sangria}"""{doc_lineas[0]}\n']
        bloque += [(f"{sangria}{l}\n" if l.strip() else "\n") for l in doc_lineas[1:]]
        bloque.append(f'{sangria}"""\n')
        idx = n.body[0].lineno - 1
        lineas[idx:idx] = bloque

    ruta.write_text("".join(lineas), encoding="utf-8")
    ast.parse("".join(lineas))  # si esto falla, mejor enterarse ahora
    return len(nodos)



def git(*args: str) -> str:
    """Ejecuta un comando git y devuelve su salida; aborta si falla.

    Args:
        *args: Argumentos de git (ej. "checkout", "-b", "rama").

    Returns:
        La salida estándar del comando.
    """
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} falló:\n{r.stderr}")
    return r.stdout.strip()



def servidor_github() -> StdioServerParameters:
    """Construye los parámetros para levantar el GitHub MCP Server con Docker.

    Returns:
        Parámetros stdio con el token tomado de .env.local.
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise SystemExit("Falta GITHUB_PERSONAL_ACCESS_TOKEN en .env.local")
    return StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
              "ghcr.io/github/github-mcp-server"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token, "PATH": os.environ.get("PATH", "")},
    )

def esquema_de(tool) -> dict:
    """Devuelve el esquema de parámetros de una tool, sin importar la versión del SDK.

    Args:
        tool: Objeto Tool devuelto por session.list_tools().

    Returns:
        El JSON Schema de entrada de la herramienta.
    """
    return getattr(tool, "inputSchema",None) or getattr(tool, "input_schema", None) or {}



async def listar_tools() -> None:
    """Imprime las herramientas del servidor con sus parámetros reales."""
    async with stdio_client(servidor_github()) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            for t in (await s.list_tools()).tools:
                props = list(esquema_de(t).get("properties", {}))
                print(f"- {t.name}: {props}")


async def crear_pr(owner: str, repo: str, rama: str, base: str, titulo: str, cuerpo: str) -> str:
    """Crea el Pull Request llamando a la herramienta del GitHub MCP Server.

    Args:
        owner: Dueño del repositorio.
        repo: Nombre del repositorio.
        rama: Rama con los cambios (head).
        base: Rama destino (ej. "main").
        titulo: Título del PR.
        cuerpo: Descripción del PR.

    Returns:
        El texto que devuelve el servidor (normalmente incluye la URL del PR).
    """
    async with stdio_client(servidor_github()) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool("create_pull_request", arguments={
                "owner": owner, "repo": repo, "title": titulo,
                "head": rama, "base": base, "body": cuerpo,
            })
            texto = "\n".join(b.text for b in res.content if hasattr(b, "text"))
            if getattr(res, "is_error", None) or getattr(res, "isError", None):
                raise SystemExit(f"El servidor MCP devolvió error:\n{texto}")
            return texto


# ---------- Orquestación ----------

def main() -> None:
    """Punto de entrada: documenta, confirma, sube la rama y abre el PR."""
    p = argparse.ArgumentParser(description="Documenta código y abre un PR vía GitHub MCP")
    p.add_argument("ruta", nargs="?", help="Carpeta con código Python a documentar")
    p.add_argument("--owner", help="Dueño del repo en GitHub")
    p.add_argument("--repo", help="Nombre del repo en GitHub")
    p.add_argument("--base", default="main", help="Rama destino del PR")
    p.add_argument("--modelo", default=MODELO)
    p.add_argument("--listar-tools", action="store_true", help="Lista las tools del servidor MCP")
    a = p.parse_args()

    if a.listar_tools:
        asyncio.run(listar_tools())
        return
    if not (a.ruta and a.owner and a.repo):
        p.error("ruta, --owner y --repo son obligatorios")

    if git("status", "--porcelain"):
        raise SystemExit("Tienes cambios sin commitear. Haz commit o stash antes de correr esto.")

    rama = f"docs/docstrings-{datetime.now():%Y%m%d-%H%M}"
    git("checkout", "-b", rama)

    archivos = [f for f in Path(a.ruta).rglob("*.py") if not set(f.parts) & IGNORAR]
    print(f"Documentando {len(archivos)} archivo(s) con {a.modelo}...")
    total, tocados = 0, []
    for f in archivos:
        n = documentar_archivo(f, a.modelo)
        if n:
            print(f"  {f}: +{n} docstring(s)")
            total += n
            tocados.append(f)

    if not tocados:
        git("checkout", "-")
        git("branch", "-D", rama)
        print("Nada que documentar.")
        return

    print(f"\nTotal: {total} docstring(s) en {len(tocados)} archivo(s). Revisa con: git diff")
    if input("¿Subir rama y abrir PR? [s/N]: ").strip().lower() != "s":
        print(f"Cancelado. Los cambios quedan en la rama local '{rama}' (descártala con git checkout - && git branch -D {rama}).")
        return

    git("add", *map(str, tocados))
    git("commit", "-m", f"docs: agrega {total} docstrings generados con IA local")
    git("push", "-u", "origin", rama)

    cuerpo = (f"Agrega {total} docstrings en {len(tocados)} archivo(s), generados con "
              f"`{a.modelo}` (Ollama). Revisar antes de mergear: pueden contener imprecisiones.")
    resultado = asyncio.run(crear_pr(a.owner, a.repo, rama, a.base,
                                     "docs: agregar docstrings generados con IA", cuerpo))
    print("\nPR creado:\n" + resultado)


if __name__ == "__main__":
    main()