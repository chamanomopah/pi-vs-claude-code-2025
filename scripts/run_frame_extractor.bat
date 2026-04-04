@echo off
REM Script para executar o extrator de frames no Windows
echo Instalando dependencias...
pip install -r requirements.txt -q

echo.
echo Executando extrator de frames...
python video_frame_extractor.py

pause
