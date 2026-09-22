# doc_agent 🤖📝

Agente de IA que documenta código Python automáticamente, corriendo **100% local** con [Ollama](https://ollama.com) — sin costo, sin enviar tu código a ningún servidor externo.

## Qué hace

- Recorre tu proyecto y encuentra funciones y clases sin docstring (usando `ast`, no expresiones regulares).
- Detecta el estilo de docstring que ya usas en el proyecto (Google, NumPy o reST) y lo replica.
- Genera propuestas con un modelo local vía Ollama.
- Te muestra un **diff** de cada cambio y espera tu aprobación antes de escribir nada.
- Salta automáticamente código trivial (`pass`, `...`) para no generar ruido.
- Al final, imprime un reporte de cuántas funciones documentó, saltó, y por qué.

## Instalación

1. Instala [Ollama](https://ollama.com):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. Descarga un modelo orientado a código:
   ```bash
   ollama pull qwen2.5-coder:1.5b 

3. Clona este repo e instala la dependencia de Python:
   ```bash
   git clone <tu-repo>
   cd doc_agent
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install ollama
   ```

## Uso

```bash
# Modo básico: revisa cada cambio antes de aplicarlo
python doc_agent.py /ruta/a/tu/proyecto

# Ver qué propondría, sin escribir ningún archivo
python doc_agent.py /ruta/a/tu/proyecto --dry-run

# Usar otro modelo de Ollama
python doc_agent.py /ruta/a/tu/proyecto --modelo qwen2.5-coder:14b

# Forzar un estilo de docstring en vez de auto-detectarlo
python doc_agent.py /ruta/a/tu/proyecto --estilo numpy

# Aprobar todos los cambios sin preguntar (útil en CI)
python doc_agent.py /ruta/a/tu/proyecto --yes
```

## Flags disponibles

| Flag | Descripción |
|---|---|
| `--modelo` | Modelo de Ollama a usar (default: `qwen2.5-coder:1.5b`) |
| `--estilo` | `auto` (default), `google`, `numpy` o `rest` |
| `--dry-run` | Muestra propuestas sin escribir archivos |
| `--yes` | Aplica todos los cambios sin pedir confirmación |

## Cómo funciona (por dentro)

1. **Lectura**: parsea cada archivo `.py` con el módulo `ast` de Python para encontrar funciones/clases reales sin docstring, ignorando carpetas como `venv`, `tests`, `__pycache__`, etc.
2. **Detección de estilo**: inspecciona los docstrings ya existentes en el proyecto buscando marcadores de cada convención, y elige la más frecuente.
3. **Generación**: por cada función, envía el código a Ollama con un prompt estricto (sin markdown, sin inventar excepciones, sin repetir el código).
4. **Limpieza**: la respuesta del modelo pasa por un parser que quita bloques de markdown accidentales y extrae solo el contenido real del docstring.
5. **Escritura controlada**: muestra un diff de cada inserción y espera tu aprobación (`sí` / `no` / `todo` / `cancelar`) antes de tocar el archivo.

## Limitaciones conocidas

- Modelos locales pequeños (5b) a veces generan docstrings genéricos o se equivocan en type hints complejos — revisa siempre los diffs antes de aprobar.
- No maneja aún la actualización de docstrings existentes que estén desactualizados, solo agrega los que faltan.
- La detección de estilo es heurística (busca palabras clave), no un parser formal de cada convención.

## Próximos pasos posibles

- Modo `--interactivo` con resúmenes por archivo antes de empezar.
- Soporte para actualizar (no solo agregar) docstrings existentes.
- Integración como pre-commit hook.

## Licencia

MIT — úsalo, modifícalo, compártelo.
