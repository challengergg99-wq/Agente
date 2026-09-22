from collections import Counter

import doc_agent2


def test_encontrar_funciones_sin_documentar_detecta_elementos_sin_documentar(tmp_path):
    archivo = tmp_path / "modulo.py"
    archivo.write_text(
        """
def suma(a, b):
    return a + b


def vacio():
    pass


class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
""",
        encoding="utf-8",
    )

    funciones = doc_agent2.encontrar_funciones_sin_documentar(archivo)
    nombres = {item["nombre"] for item in funciones}

    assert {"suma", "vacio", "Persona", "__init__"}.issubset(nombres)


def test_procesar_archivo_soporta_dry_run(tmp_path, monkeypatch):
    archivo = tmp_path / "modulo.py"
    archivo.write_text("def suma(a, b):\n    return a + b\n", encoding="utf-8")

    monkeypatch.setattr(
        doc_agent2,
        "generar_docstring",
        lambda codigo, estilo: "Suma dos números y devuelve el resultado.",
    )

    resultado = doc_agent2.procesar_archivo(
        archivo,
        aprobar_todo=True,
        estilo="google",
        reporte=Counter(),
        dry_run=True,
    )

    assert resultado is True
    assert archivo.read_text(encoding="utf-8") == "def suma(a, b):\n    return a + b\n"


def test_generar_docstring_tiene_fallback_si_ollama_falla(monkeypatch):
    def lanzar_error(*args, **kwargs):
        raise RuntimeError("Ollama no disponible")

    monkeypatch.setattr(doc_agent2.ollama, "chat", lanzar_error)

    texto = doc_agent2.generar_docstring("def suma(a, b):\n    return a + b\n", "google")

    assert "Suma" in texto or "suma" in texto.lower()
