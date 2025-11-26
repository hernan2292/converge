@echo off
echo ========================================
echo Instalador vLLM para WSL Ubuntu
echo ========================================
echo.
echo Este script instalara:
echo - Python 3 y dependencias
echo - CUDA Toolkit (nvcc)
echo - vLLM y Ray
echo.
echo IMPORTANTE: Esto puede tardar 10-15 minutos
echo.
pause

wsl -d Ubuntu bash -c "cd /mnt/c/Users/herna/OneDrive/proyects/converge && chmod +x install_vllm.sh && ./install_vllm.sh"

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Para iniciar el master, ejecuta:
echo   start_master.bat
echo.
pause
