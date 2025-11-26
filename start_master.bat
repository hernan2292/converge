@echo off
echo ========================================
echo Iniciando vLLM Master en WSL Ubuntu
echo ========================================
echo.
echo Modelo: facebook/opt-125m
echo Puerto: 8000
echo.
wsl -d Ubuntu bash -c "cd /mnt/c/Users/herna/OneDrive/proyects/converge && chmod +x *.sh && ./start_vllm_master.sh facebook/opt-125m 8000 1"
