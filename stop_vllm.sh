#!/bin/bash

# Script para detener vLLM y Ray

echo 'Deteniendo vLLM y Ray...'

# Detener Ray
ray stop

# Matar procesos vLLM si quedan
pkill -f vllm

echo 'Servicios detenidos'
