#!/bin/bash

# Script para iniciar nodo WORKER (esclavo) de vLLM distribuido

echo '========================================'
echo 'Iniciando NODO WORKER vLLM'
echo '========================================'
echo

# Activar entorno
cd ~/vllm_workspace
source vllm_env/bin/activate

# Configuración
MASTER_IP="${1}"
MASTER_PORT="${2:-6379}"

if [ -z "$MASTER_IP" ]; then
    echo "ERROR: Debes proporcionar la IP del master"
    echo
    echo "Uso: ./start_vllm_worker.sh <IP_MASTER> [PUERTO]"
    echo "Ejemplo: ./start_vllm_worker.sh 192.168.1.100 6379"
    exit 1
fi

echo "Master IP: $MASTER_IP"
echo "Master Port: $MASTER_PORT"
echo

# Conectar al Ray Master
ray start --address="$MASTER_IP:$MASTER_PORT"

echo
echo 'Worker conectado al master'
echo 'Ray Dashboard: http://'"$MASTER_IP"':8265'
echo
echo 'Este nodo ahora está disponible para procesar requests'
echo 'Presiona Ctrl+C para detener'
echo

# Mantener el proceso vivo
tail -f /dev/null
