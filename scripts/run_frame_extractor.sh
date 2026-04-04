#!/bin/bash
# Script para executar o extrator de frames no Linux/Mac

echo "Instalando dependências..."
pip install -r requirements.txt -q

echo ""
echo "Executando extrator de frames..."
python video_frame_extractor.py
