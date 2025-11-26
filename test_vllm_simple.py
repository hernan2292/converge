#!/usr/bin/env python3
"""
Test simple del servidor vLLM
Uso: python test_vllm_simple.py
"""

import sys
from openai import OpenAI

# Configuración
VLLM_HOST = "http://localhost:8000"
MODEL = "facebook/opt-125m"

print("=" * 50)
print("Test vLLM Server")
print("=" * 50)
print(f"Servidor: {VLLM_HOST}")
print(f"Modelo: {MODEL}")
print()

# Cliente
client = OpenAI(
    api_key="EMPTY",
    base_url=f"{VLLM_HOST}/v1"
)

# Test 1: Listar modelos
print("1. Verificando modelos disponibles...")
try:
    models = client.models.list()
    print(f"   ✓ Modelos: {[m.id for m in models.data]}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("\nAsegúrate de que el servidor está corriendo:")
    print("  ./start_vllm_master.sh facebook/opt-125m 8000 1")
    sys.exit(1)

# Test 2: Completion simple
print("\n2. Test de completion...")
try:
    response = client.completions.create(
        model=MODEL,
        prompt="Hello, my name is",
        max_tokens=20,
        temperature=0.7
    )
    result = response.choices[0].text
    print(f"   Prompt: Hello, my name is")
    print(f"   Resultado: {result}")
    print("   ✓ Completion exitosa")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 3: Múltiples requests
print("\n3. Test de múltiples requests...")
prompts = [
    "Once upon a time",
    "The meaning of life is",
    "In Python, a list is"
]

for prompt in prompts:
    try:
        response = client.completions.create(
            model=MODEL,
            prompt=prompt,
            max_tokens=15,
            temperature=0.7
        )
        result = response.choices[0].text
        print(f"   '{prompt}' → '{result.strip()}'")
    except Exception as e:
        print(f"   ✗ Error en '{prompt}': {e}")

print("\n" + "=" * 50)
print("✓ Todos los tests completados exitosamente!")
print("=" * 50)
