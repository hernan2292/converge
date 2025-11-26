#!/bin/bash

# Script para iniciar nodo MASTER de vLLM distribuido

echo '========================================'
echo 'Iniciando NODO MASTER vLLM'
echo '========================================'
echo

# Activar entorno
cd ~/vllm_workspace
source vllm_env/bin/activate

# Configuración
MODEL_NAME="${1:-facebook/opt-125m}"
PORT="${2:-8000}"
TENSOR_PARALLEL_SIZE="${3:-1}"  # Número de GPUs

echo "Modelo: $MODEL_NAME"
echo "Puerto: $PORT"
echo "Tensor Parallel: $TENSOR_PARALLEL_SIZE"
echo

# Iniciar Ray Head (Master)
echo "Iniciando Ray Head..."
ray start --head --port=6379 --dashboard-host=0.0.0.0 --disable-usage-stats

# Obtener IP del master
MASTER_IP=$(hostname -I | awk '{print $1}')

echo
echo '========================================'
echo 'Ray Master iniciado exitosamente'
echo '========================================'
echo "IP del Master: $MASTER_IP"
echo "Puerto Ray: 6379"
echo "Dashboard Ray: http://localhost:8265"
echo
echo 'Para conectar workers desde otras máquinas:'
echo "  ./start_vllm_worker.sh $MASTER_IP 6379"
echo
echo '========================================'
echo 'Iniciando servidor vLLM...'
echo '========================================'
echo

# Iniciar servidor vLLM
python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL_NAME" \
    --host 0.0.0.0 \
    --port "$PORT" \
    --tensor-parallel-size "$TENSOR_PARALLEL_SIZE" \
    --dtype auto \
    --enforce-eager \
    --disable-log-requests
