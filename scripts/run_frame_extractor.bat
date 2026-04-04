@echo off
REM Script para executar o extrator de frames no Windows
echo Instalando dependencias...
pip install -r requirements.txt -q

echo.
echo Uso: python video_frame_extractor.py "URL_OU_CAMINHO"
echo Exemplos:
echo   python video_frame_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
echo   python video_frame_extractor.py "file:///C:/Users/JOSE/Videos/video.mp4"
echo   python video_frame_extractor.py "C:/Videos/video.mp4"
echo.
echo Para ajuda: python video_frame_extractor.py --help
echo.
