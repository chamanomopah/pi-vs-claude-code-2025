#!/usr/bin/env python3
"""
Video Frame Extractor
Extrai frames de um vídeo do YouTube

Uso:
    python video_frame_extractor.py <url_video>
    echo "<url_video>" | python video_frame_extractor.py

Output (JSON):
    {
        "frames_path": "/path/to/frames.zip",
        "video_id": "abc123",
        "frames_count": 30,
        "fps": 1
    }
"""

import sys
import json
import re
import zipfile
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print(json.dumps({"error": "yt_dlp não instalado. Execute: pip install yt-dlp"}))
    sys.exit(1)

try:
    import cv2
except ImportError:
    print(json.dumps({"error": "opencv-python não instalado. Execute: pip install opencv-python"}))
    sys.exit(1)


def extract_video_id(url):
    """Extrai o ID do vídeo de uma URL do YouTube"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def extract_frames(video_path, output_dir, fps=1, max_frames=30):
    """
    Extrai frames de um vídeo usando OpenCV

    Args:
        video_path: Caminho do arquivo de vídeo
        output_dir: Diretório para salvar frames
        fps: Frames por segundo (1 = 1 frame por segundo)
        max_frames: Número máximo de frames

    Returns:
        Lista de caminhos dos frames extraídos
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception(f"Não foi possível abrir o vídeo: {video_path}")

    # Obter FPS do vídeo
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calcular intervalo entre frames
    frame_interval = int(video_fps / fps) if fps > 0 else 30

    frames = []
    frame_count = 0
    extracted_count = 0

    while True:
        ret, frame = cap.read()

        if not ret or extracted_count >= max_frames:
            break

        if frame_count % frame_interval == 0:
            frame_file = output_path / f"frame_{extracted_count:04d}.jpg"
            cv2.imwrite(str(frame_file), frame)
            frames.append(str(frame_file))
            extracted_count += 1

        frame_count += 1

    cap.release()

    return frames


def download_and_extract_frames(video_url, output_dir="frames", fps=1, max_frames=30):
    """
    Baixa vídeo e extrai frames

    Args:
        video_url: URL do vídeo
        output_dir: Diretório base para frames
        fps: Frames por segundo
        max_frames: Número máximo de frames

    Returns:
        Dict com frames_path, video_id, frames_count
    """
    video_id = extract_video_id(video_url)

    if not video_id:
        return {"error": f"URL inválida: {video_url}"}

    # Criar diretório de saída
    frames_dir = Path(output_dir) / video_id
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Baixar vídeo
    video_file = frames_dir / f"{video_id}.mp4"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'worst[ext=mp4]',  # Pior qualidade para download rápido
        'outtmpl': str(video_file),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Extrair frames
        frames = extract_frames(
            str(video_file),
            frames_dir / "images",
            fps=fps,
            max_frames=max_frames
        )

        # Criar ZIP com frames
        zip_file = frames_dir / f"{video_id}_frames.zip"

        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for frame in frames:
                arcname = Path(frame).name
                zipf.write(frame, arcname)

        # Deletar vídeo para economizar espaço
        video_file.unlink()

        return {
            "frames_path": str(zip_file.absolute()),
            "video_id": video_id,
            "frames_count": len(frames),
            "fps": fps
        }

    except Exception as e:
        return {"error": str(e)}


def main():
    # Ler URL do argumento ou stdin
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = sys.stdin.read().strip()

    if not video_url:
        print(json.dumps({"error": "URL do vídeo não fornecida"}))
        sys.exit(1)

    # Baixar e extrair frames
    result = download_and_extract_frames(video_url)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
