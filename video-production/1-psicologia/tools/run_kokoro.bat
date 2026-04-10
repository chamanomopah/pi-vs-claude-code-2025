@echo off
REM Wrapper para executar Kokoro TTS com Conda
REM Uso: run_kokoro.bat [opcoes]
REM   Exemplo: run_kokoro.bat
REM   Exemplo: run_kokoro.bat --vozes

echo ============================================
echo Kokoro TTS - Text-to-Speech com PyTorch
echo ============================================
echo.

REM Caminho para o Python do ambiente Conda
set PYTHON_EXE=C:\pinokio\bin\miniconda\envs\kokoro\python.exe
REM Diretório onde este script está localizado
set SCRIPT_DIR=%~dp0

REM Verificar se o Python existe
if not exist "%PYTHON_EXE%" (
    echo ERRO: Ambiente Conda 'kokoro' nao encontrado!
    echo.
    echo Por favor, instale o ambiente Conda primeiro:
    echo   1. conda create --name kokoro python=3.12 -y
    echo   2. conda activate kokoro
    echo   3. pip install kokoro>=0.9.4 soundfile torch
    echo.
    pause
    exit /b 1
)

REM Executar o script Python com os argumentos passados
"%PYTHON_EXE%" "%SCRIPT_DIR%kokoro_tts.py" %*

pause
