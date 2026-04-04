#!/bin/bash
# Script para executar o extrator de frames no Linux/Mac

echo "Instalando dependências..."
pip install -r requirements.txt -q

echo ""
echo "Uso: python video_frame_extractor.py \"URL_OU_CAMINHO\""
echo "Exemplos:"
echo "  python video_frame_extractor.py \"https://www.youtube.com/watch?v=VIDEO_ID\""
echo "  python video_frame_extractor.py \"file:///home/user/videos/video.mp4\""
echo "  python video_frame_extractor.py \"/home/user/videos/video.mp4\""
echo ""
echo "Para ajuda: python video_frame_extractor.py --help"
echo ""
