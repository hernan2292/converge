# vLLM Distributed Cluster con vibe.py

Sistema distribuido para ejecutar modelos LLM usando vLLM en modo master/worker con integración a vibe.py.

## 📋 Requisitos

- **Windows 11** con WSL2 Ubuntu
- **GPU NVIDIA** con soporte CUDA
- **Python 3.9-3.12** en WSL
- **CUDA Toolkit** instalado en WSL

## 🚀 Instalación Rápida

### 1. Instalar vLLM en WSL Ubuntu

```bash
# Desde Windows, abre WSL Ubuntu
wsl -d Ubuntu

# Navega al directorio del proyecto
cd /mnt/c/Users/herna/OneDrive/proyects/converge

# Da permisos y ejecuta el instalador
chmod +x install_vllm.sh
./install_vllm.sh
```

El script instalará:
- Python 3 y dependencias
- CUDA Toolkit (nvcc)
- vLLM y Ray
- Entorno virtual en `~/vllm_workspace`

### 2. Verificar Instalación

```bash
# Dentro de WSL
cd ~/vllm_workspace
source vllm_env/bin/activate
python -c "import vllm, ray; print('vLLM:', vllm.__version__)"
```

## 🎯 Uso

### Modo 1: Nodo Master (Servidor Principal)

El nodo master ejecuta el modelo y coordina workers.

```bash
# Desde Windows
wsl -d Ubuntu

# Navega al proyecto
cd /mnt/c/Users/herna/OneDrive/proyects/converge

# Inicia el master
./start_vllm_master.sh [MODELO] [PUERTO] [NUM_GPUS]
```

**Ejemplos:**

```bash
# Modelo pequeño para pruebas (125M parámetros)
./start_vllm_master.sh facebook/opt-125m 8000 1

# Llama 2 7B (requiere ~14GB VRAM)
./start_vllm_master.sh meta-llama/Llama-2-7b-hf 8000 1

# Mistral 7B
./start_vllm_master.sh mistralai/Mistral-7B-v0.1 8000 1
```

**El master mostrará:**
- IP del master (ej: `172.22.23.97`)
- Puerto Ray: `6379`
- Puerto API: `8000`
- Dashboard Ray: `http://localhost:8265`

### Modo 2: Nodo Worker (Esclavo)

Los workers se conectan al master para distribuir la carga.

```bash
# En otra máquina o terminal WSL
./start_vllm_worker.sh <IP_MASTER> [PUERTO_RAY]
```

**Ejemplo:**

```bash
./start_vllm_worker.sh 172.22.23.97 6379
```

### Verificar el Cluster

**Ray Dashboard:**
- Abre en navegador: `http://localhost:8265` (si estás en el master)
- Verás todos los nodos conectados

**Verificar API:**

```bash
# Probar que el servidor responde
curl http://localhost:8000/v1/models

# Hacer una inferencia
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "facebook/opt-125m",
    "prompt": "Hello, my name is",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

## 🔗 Integración con vibe.py

Una vez el master está corriendo, usa `vibe.py` para procesar requests:

```python
# vibe.py se conecta al servidor vLLM
python vibe.py
```

Configura vibe.py para apuntar al endpoint vLLM:
```python
# En vibe.py, configurar:
base_url = "http://localhost:8000/v1"
model_name = "facebook/opt-125m"  # o el modelo que uses
```

## 🛠️ Comandos Útiles

### Detener el Cluster

```bash
# Detiene Ray y vLLM
./stop_vllm.sh
```

### Ver Estado del Cluster

```bash
# Activar entorno
cd ~/vllm_workspace
source vllm_env/bin/activate

# Ver estado de Ray
ray status

# Ver procesos vLLM
ps aux | grep vllm
```

### Verificar GPU

```bash
# Ver uso de GPU
nvidia-smi

# Monitoreo continuo
watch -n 1 nvidia-smi
```

### Logs y Debugging

```bash
# Ver logs de Ray
cat /tmp/ray/session_latest/logs/*

# Variables de entorno para debug
export VLLM_LOGGING_LEVEL=DEBUG
export RAY_VERBOSE=1
```

## 📊 Modelos Recomendados

### Para Pruebas (sin GPU potente):
- `facebook/opt-125m` (125M parámetros, ~500MB)
- `facebook/opt-350m` (350M parámetros, ~1.3GB)
- `gpt2` (124M parámetros, ~500MB)

### Para Producción (requiere GPU):
- `meta-llama/Llama-2-7b-hf` (7B parámetros, ~14GB VRAM)
- `meta-llama/Llama-2-13b-hf` (13B parámetros, ~26GB VRAM)
- `mistralai/Mistral-7B-v0.1` (7B parámetros, ~14GB VRAM)
- `mistralai/Mixtral-8x7B-v0.1` (47B parámetros, ~90GB VRAM)

## 🔧 Solución de Problemas

### Error: "Permission denied: 'nvcc'"

```bash
# Instalar CUDA Toolkit
wsl -d Ubuntu
sudo apt-get update
sudo apt-get install -y nvidia-cuda-toolkit
nvcc --version
```

### Error: "CUDA out of memory"

- Usa un modelo más pequeño
- Reduce `--max-model-len`:
  ```bash
  ./start_vllm_master.sh facebook/opt-125m 8000 1 --max-model-len 1024
  ```

### Error: "Cannot connect to Ray"

- Verifica que el master esté corriendo: `ray status`
- Revisa la IP del master: `hostname -I`
- Asegura que el firewall permita puerto 6379

### Workers no aparecen

- Verifica que ambas máquinas estén en la misma red
- Revisa firewall (puertos 6379, 8265)
- Usa la IP correcta del master (no `localhost`)

### Modelo no se descarga

- Requiere conexión a internet
- Los modelos se guardan en `~/.cache/huggingface/`
- Para modelos privados (Llama 2):
  ```bash
  huggingface-cli login
  ```

## 📁 Estructura de Archivos

```
converge/
├── install_vllm.sh           # Instalador de vLLM en WSL
├── start_vllm_master.sh      # Iniciar nodo master
├── start_vllm_worker.sh      # Iniciar nodo worker
├── stop_vllm.sh              # Detener cluster
├── vibe.py                   # Cliente para procesar requests
└── README_VLLM.md           # Esta guía
```

## 🌐 API Compatible con OpenAI

vLLM expone una API compatible con OpenAI:

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

## 📝 Notas

- El primer inicio descarga el modelo (puede tardar varios minutos)
- Los modelos se cachean en `~/.cache/huggingface/`
- WSL2 comparte la GPU de Windows automáticamente
- Para múltiples GPUs, aumenta `--tensor-parallel-size`

## 🔗 Enlaces Útiles

- [vLLM Docs](https://docs.vllm.ai/)
- [Ray Docs](https://docs.ray.io/)
- [Hugging Face Models](https://huggingface.co/models)
