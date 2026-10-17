import asyncio
import os

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MODELO = "llama3.1:8b" #para trabajar con ollama


def esquema_mcp_a_ollama(tool) -> dict:
    """Convierte la definición de una herramienta MCP al formato de Ollama.

    Args:
        tool: Objeto Tool devuelto por session.list_tools() (tiene name,
            description e inputSchema).

    Returns:
        Dict en el formato {"type": "function", "function": {...}} que
        Ollama espera en el parámetro `tools` de ollama.chat().
    """
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema,
        },
    }


async def ejecutar_conversacion(session: ClientSession, herramientas_ollama: list[dict], prompt_usuario: str) -> None:
    """Corre el bucle de tool calling: el modelo decide, MCP ejecuta, el modelo responde.

    Args:
        session: Sesión MCP ya inicializada, conectada al GitHub MCP Server.
        herramientas_ollama: Lista de herramientas en formato Ollama.
        prompt_usuario: La instrucción del usuario, ej. "abre un issue en X".
    """
    mensajes = [
        {
            "role": "system",
            "content": (
                "Eres un asistente que gestiona repositorios de GitHub. "
                "Usa las herramientas disponibles cuando el usuario te pida "
                "crear, leer o modificar algo en GitHub. No inventes resultados: "
                "si necesitas info de GitHub, usa una herramienta para obtenerla."
            ),
        },
        {"role": "user", "content": prompt_usuario},
    ]

    respuesta = ollama.chat(model=MODELO, messages=mensajes, tools=herramientas_ollama)
    mensaje = respuesta["message"]

    llamadas = mensaje.get("tool_calls") or []
    if not llamadas:
        print("\nRespuesta del modelo (sin usar herramientas):")
        print(mensaje["content"])
        return

    mensajes.append(mensaje)

    for llamada in llamadas:
        nombre_funcion = llamada["function"]["name"]
        argumentos = llamada["function"]["arguments"]
        print(f"\n[Ejecutando herramienta real] {nombre_funcion}({argumentos})")

        resultado = await session.call_tool(nombre_funcion, arguments=argumentos)
        texto_resultado = "\n".join(
            bloque.text for bloque in resultado.content if hasattr(bloque, "text")
        )

        mensajes.append({
            "role": "tool",
            "content": texto_resultado,
        })

    respuesta_final = ollama.chat(model=MODELO, messages=mensajes, tools=herramientas_ollama)
    print("\nRespuesta final del modelo:")
    print(respuesta_final["message"]["content"])


async def main() -> None:
    """Conecta al GitHub MCP Server, lista herramientas y corre una conversación de prueba."""
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise SystemExit("Define GITHUB_PERSONAL_ACCESS_TOKEN antes de correr esto.")

    parametros_servidor = StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token},
    )

    async with stdio_client(parametros_servidor) as (lectura, escritura):
        async with ClientSession(lectura, escritura) as session:
            await session.initialize()

            resultado_tools = await session.list_tools()
            herramientas_ollama = [esquema_mcp_a_ollama(t) for t in resultado_tools.tools]

            print(f"Herramientas disponibles del GitHub MCP Server: {len(herramientas_ollama)}")
            for tool in resultado_tools.tools[:10]:
                print(f"  - {tool.name}")

            await ejecutar_conversacion(
                session,
                herramientas_ollama,
                "Lista mis repositorios más recientes en GitHub.",
            )


if __name__ == "__main__":
    asyncio.run(main())