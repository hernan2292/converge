# 🚀 vLLM Distributed Cluster

Sistema distribuido para ejecutar modelos LLM usando **vLLM** en modo master/worker con integración a Python.

## 📦 Contenido del Proyecto

```
converge/
├── install.bat               # [Windows] Instalador con un click
├── start_master.bat          # [Windows] Inicia master con un click
├── install_vllm.sh           # [WSL] Instalador (CUDA + vLLM + Ray)
├── start_vllm_master.sh      # [WSL] Inicia nodo master
├── start_vllm_worker.sh      # [WSL] Inicia nodo worker/esclavo
├── stop_vllm.sh              # [WSL] Detiene el cluster
├── vibe_vllm.py              # Cliente Python interactivo
├── test_vllm_simple.py       # Test de conexión
├── vibe.py                   # Cliente Ollama (legacy)
├── requirements.txt          # Dependencias Python
├── README.md                 # Esta guía
└── README_VLLM.md           # Documentación detallada
```

## ⚡ Inicio Rápido

### 1. Instalación (una sola vez)

**Opción A: Desde Windows (recomendado)**

Doble click en `install.bat` o ejecuta desde CMD:

```cmd
install.bat
```

**Opción B: Desde WSL**

```bash
wsl -d Ubuntu
cd /mnt/c/Users/herna/OneDrive/proyects/converge
chmod +x install_vllm.sh
./install_vllm.sh
```

**Esto instalará:**
- Python 3 + pip
- CUDA Toolkit (nvcc)
- vLLM 0.11+
- Ray 2.9+
- Entorno virtual en `~/vllm_workspace`

### 2. Iniciar Master

**Opción A: Desde Windows (recomendado)**

Doble click en `start_master.bat` o ejecuta:

```cmd
start_master.bat
```

**Opción B: Desde WSL**

```bash
wsl -d Ubuntu
cd /mnt/c/Users/herna/OneDrive/proyects/converge
./start_vllm_master.sh facebook/opt-125m 8000 1
```

**Salida esperada:**
```
========================================
Ray Master iniciado exitosamente
========================================
IP del Master: 172.22.23.97
Puerto Ray: 6379
Dashboard Ray: http://localhost:8265

Para conectar workers:
  ./start_vllm_worker.sh 172.22.23.97 6379
========================================
```

### 3. Conectar Workers (Opcional)

En otras máquinas o terminales WSL:

```bash
./start_vllm_worker.sh 172.22.23.97 6379
```

### 4. Probar el Cluster

**Test rápido:**

```bash
# Activar entorno
wsl -d Ubuntu
cd ~/vllm_workspace
source vllm_env/bin/activate
pip install openai rich

# Test simple
python /mnt/c/Users/herna/OneDrive/proyects/converge/test_vllm_simple.py
```

### 5. Usar el Cluster

**Opción A: Cliente Python Interactivo (vibe_vllm.py)**

```bash
# Modo interactivo (chat)
python /mnt/c/Users/herna/OneDrive/proyects/converge/vibe_vllm.py

# Ver ejemplos
python /mnt/c/Users/herna/OneDrive/proyects/converge/vibe_vllm.py examples

# Test de conexión
python /mnt/c/Users/herna/OneDrive/proyects/converge/vibe_vllm.py test
```

**Opción B: API REST (curl)**

```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "facebook/opt-125m",
    "prompt": "Hello, my name is",
    "max_tokens": 50
  }'
```

**Opción C: Python directo**

```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)

response = client.completions.create(
    model="facebook/opt-125m",
    prompt="Once upon a time",
    max_tokens=50
)

print(response.choices[0].text)
```

## 🎯 Comandos Útiles

### Verificar Estado

```bash
# Estado de Ray
ray status

# Ver GPUs
nvidia-smi

# Procesos vLLM
ps aux | grep vllm
```

### Detener Cluster

```bash
./stop_vllm.sh
```

### Dashboard Ray

Abre en navegador: `http://localhost:8265`

## 📊 Modelos Disponibles

### Pruebas (sin GPU potente):
- `facebook/opt-125m` (125M, ~500MB)
- `facebook/opt-350m` (350M, ~1.3GB)
- `gpt2` (124M, ~500MB)

### Producción (GPU):
- `meta-llama/Llama-2-7b-hf` (7B, ~14GB VRAM)
- `mistralai/Mistral-7B-v0.1` (7B, ~14GB VRAM)
- `meta-llama/Llama-2-13b-hf` (13B, ~26GB VRAM)

## 🔧 Solución de Problemas

### Error: "Permission denied: 'nvcc'"

```bash
sudo apt-get install -y nvidia-cuda-toolkit
nvcc --version
```

### Error: "CUDA out of memory"

Usa un modelo más pequeño o reduce `--max-model-len`

### Workers no se conectan

- Verifica IP del master: `hostname -I`
- Revisa firewall (puerto 6379)
- Asegura que estén en la misma red

## 📖 Documentación

Para información detallada, consulta:
- [README_VLLM.md](README_VLLM.md) - Guía completa
- [vLLM Docs](https://docs.vllm.ai/)
- [Ray Docs](https://docs.ray.io/)

## 🛠️ Stack Tecnológico

- **vLLM** - Motor de inferencia LLM
- **Ray** - Framework de computación distribuida
- **WSL2** - Windows Subsystem for Linux
- **CUDA** - Aceleración GPU
- **Python 3.9-3.12**

## 📝 Notas

- Primer inicio descarga el modelo (puede tardar)
- Modelos se cachean en `~/.cache/huggingface/`
- API compatible con OpenAI
- WSL2 comparte GPU de Windows automáticamente

---

**Desarrollado para procesamiento distribuido de LLMs en Windows con WSL2**
