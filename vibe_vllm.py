#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vibe vLLM - Cliente para procesar requests con vLLM cluster
Ejecuta: python vibe_vllm.py
"""

import os
import sys
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Configurar encoding UTF-8 en Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

console = Console()

# Configuración del servidor vLLM
VLLM_HOST = os.getenv("VLLM_HOST", "http://localhost:8000")
VLLM_MODEL = os.getenv("VLLM_MODEL", "facebook/opt-125m")

# Cliente OpenAI compatible con vLLM
client = OpenAI(
    api_key="EMPTY",  # vLLM no requiere API key
    base_url=f"{VLLM_HOST}/v1"
)


def test_connection():
    """Verifica que el servidor vLLM está disponible"""
    try:
        models = client.models.list()
        console.print("[green]✓[/] Conexión exitosa al servidor vLLM")
        console.print(f"[dim]Servidor: {VLLM_HOST}[/]")
        console.print(f"[dim]Modelos disponibles: {[m.id for m in models.data]}[/]")
        return True
    except Exception as e:
        console.print(f"[red]✗[/] Error conectando a vLLM: {e}")
        console.print(f"[yellow]Asegúrate de que el servidor está corriendo en {VLLM_HOST}[/]")
        return False


def completion(prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
    """Genera una completion usando vLLM"""
    try:
        response = client.completions.create(
            model=VLLM_MODEL,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].text
    except Exception as e:
        return f"Error: {e}"


def chat(messages: list, max_tokens: int = 500, temperature: float = 0.7) -> str:
    """Chat usando vLLM (si el modelo soporta chat)"""
    try:
        response = client.chat.completions.create(
            model=VLLM_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fallback a completion si chat no está disponible
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return completion(prompt, max_tokens, temperature)


def interactive_mode():
    """Modo interactivo de chat"""
    console.print(Panel.fit(
        "[bold cyan]Vibe vLLM - Modo Interactivo[/]\n"
        f"Servidor: {VLLM_HOST}\n"
        f"Modelo: {VLLM_MODEL}\n\n"
        "Escribe 'salir' para terminar",
        border_style="cyan"
    ))

    if not test_connection():
        return

    conversation = []

    while True:
        try:
            user_input = console.input("\n[bold green]Tú:[/] ")

            if user_input.lower() in ['salir', 'exit', 'quit']:
                console.print("[yellow]¡Hasta luego![/]")
                break

            if not user_input.strip():
                continue

            conversation.append({"role": "user", "content": user_input})

            console.print("[dim]Pensando...[/]")
            response = chat(conversation)

            conversation.append({"role": "assistant", "content": response})

            console.print(f"\n[bold cyan]Asistente:[/]\n{response}")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrumpido por el usuario[/]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")


def example_completions():
    """Ejemplos de uso de completions"""
    console.print(Panel.fit(
        "[bold cyan]Ejemplos de Completions[/]",
        border_style="cyan"
    ))

    if not test_connection():
        return

    examples = [
        "Once upon a time",
        "The meaning of life is",
        "In a galaxy far, far away",
        "def fibonacci(n):\n    # Python function to calculate fibonacci"
    ]

    for prompt in examples:
        console.print(f"\n[bold]Prompt:[/] {prompt}")
        console.print("[dim]Generando...[/]")

        result = completion(prompt, max_tokens=50, temperature=0.7)
        console.print(f"[green]Resultado:[/] {prompt}{result}")


def main():
    """Función principal"""
    console.clear()

    if len(sys.argv) > 1:
        if sys.argv[1] == "examples":
            example_completions()
        elif sys.argv[1] == "test":
            test_connection()
        else:
            console.print("[yellow]Uso:[/]")
            console.print("  python vibe_vllm.py          - Modo interactivo")
            console.print("  python vibe_vllm.py examples - Ver ejemplos")
            console.print("  python vibe_vllm.py test     - Test de conexión")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
