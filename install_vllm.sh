#!/bin/bash

echo '========================================'
echo 'Instalando vLLM en WSL2 Ubuntu'
echo '========================================'
echo

# Actualizar sistema
echo 'Actualizando sistema...'
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential

# Instalar CUDA Toolkit (incluye nvcc)
echo
echo 'Instalando CUDA Toolkit...'
sudo apt-get install -y nvidia-cuda-toolkit

# Verificar version de Python
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python: $PYTHON_VERSION"

# Crear directorio de trabajo
WORK_DIR="$HOME/vllm_workspace"
echo
echo "Creando directorio: $WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Crear entorno virtual
echo
echo 'Creando entorno virtual...'
python3 -m venv vllm_env

# Activar entorno
echo 'Activando entorno virtual...'
source vllm_env/bin/activate

# Actualizar pip
echo
echo 'Actualizando pip...'
pip install --upgrade pip setuptools wheel

# Instalar vLLM y Ray
echo
echo 'Instalando vLLM y Ray (esto puede tardar varios minutos)...'
pip install vllm ray

echo
echo '========================================'
echo 'Instalacion completada exitosamente!'
echo '========================================'
echo
echo 'Para usar vLLM:'
echo '  1. cd ~/vllm_workspace'
echo '  2. source vllm_env/bin/activate'
echo '  3. python -c "import vllm; print(vllm.__version__)"'
echo
