#!/usr/bin/env python3
"""
YouTube Transcript Downloader
Baixa a transcrição de um vídeo do YouTube

Uso:
    python youtube_transcript_downloader.py <url_video>
    echo "<url_video>" | python youtube_transcript_downloader.py

Output (JSON):
    {
        "transcript_path": "/path/to/transcript.txt",
        "video_id": "abc123",
        "language": "pt"
    }
"""

import sys
import json
import re
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print(json.dumps({"error": "yt_dlp não instalado. Execute: pip install yt-dlp"}))
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


def download_transcript(video_url, output_dir="transcripts"):
    """
    Baixa a transcrição de um vídeo

    Args:
        video_url: URL do vídeo
        output_dir: Diretório para salvar transcrições

    Returns:
        Dict com transcript_path, video_id, language
    """
    video_id = extract_video_id(video_url)

    if not video_id:
        return {"error": f"URL inválida: {video_url}"}

    # Criar diretório de saída
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    transcript_file = output_path / f"{video_id}_transcript.txt"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'writesubtitles': True,
        'writeautomaticsub': True,  # Usa legenda automática se não tiver
        'subtitleslangs': ['pt', 'en'],
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # Tentar obter transcrição via API
            try:
                from youtube_transcript_api import YouTubeTranscriptApi

                transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])

                with open(transcript_file, 'w', encoding='utf-8') as f:
                    for entry in transcripts:
                        f.write(f"{entry['text']}\n")

                return {
                    "transcript_path": str(transcript_file.absolute()),
                    "video_id": video_id,
                    "language": transcripts[0].get('language', 'unknown') if transcripts else 'unknown',
                    "segments": len(transcripts)
                }

            except Exception as e:
                # Fallback: Tentar usar yt-dlp para baixar legenda
                subtitle = info.get('subtitles', {})

                # Tentar português
                if 'pt' in subtitle:
                    sub_url = subtitle['pt'][0]['url']
                elif 'live_chat' in subtitle:
                    sub_url = list(subtitle.values())[0][0]['url']
                else:
                    # Usar legenda automática
                    automatic_captions = info.get('automatic_captions', {})
                    if 'pt' in automatic_captions:
                        sub_url = automatic_captions['pt'][0]['url']
                    else:
                        return {"error": "Nenhuma transcrição disponível"}

                # Baixar arquivo de legenda
                import requests
                response = requests.get(sub_url)
                response.raise_for_status()

                # Converter para texto simples
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)

                with open(transcript_file, 'w', encoding='utf-8') as f:
                    for child in root.findall('.//text'):
                        text = child.text or ''
                        f.write(f"{text}\n")

                return {
                    "transcript_path": str(transcript_file.absolute()),
                    "video_id": video_id,
                    "language": "pt",
                    "method": "yt-dlp"
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

    # Baixar transcrição
    result = download_transcript(video_url)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
