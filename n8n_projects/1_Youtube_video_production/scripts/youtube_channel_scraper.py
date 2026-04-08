#!/usr/bin/env python3
"""
YouTube Channel Scraper
Busca os top 3 vídeos de um canal do YouTube

Uso:
    python youtube_channel_scraper.py <url_canal>
    echo "<url_canal>" | python youtube_channel_scraper.py

Output (JSON):
    {
        "videos": [
            {"url": "https://youtube.com/watch?v=...", "title": "..."},
            {"url": "https://youtube.com/watch?v=...", "title": "..."},
            {"url": "https://youtube.com/watch?v=...", "title": "..."}
        ]
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


def get_channel_videos(channel_url, limit=3):
    """
    Busca os top N vídeos de um canal

    Args:
        channel_url: URL do canal do YouTube
        limit: Número de vídeos para buscar (padrão: 3)

    Returns:
        Lista de dicionários com url e title
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'playlistend': limit,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)

            videos = []

            # Se for um canal/playlisy
            if 'entries' in result:
                for entry in result['entries'][:limit]:
                    if entry:
                        video_url = f"https://youtube.com/watch?v={entry['id']}"
                        videos.append({
                            "url": video_url,
                            "title": entry.get('title', 'Sem título'),
                            "id": entry['id']
                        })
            # Se for um vídeo único
            elif 'id' in result:
                video_url = f"https://youtube.com/watch?v={result['id']}"
                videos.append({
                    "url": video_url,
                    "title": result.get('title', 'Sem título'),
                    "id": result['id']
                })

            return videos

    except Exception as e:
        return [{"error": str(e)}]


def extract_channel_url(url):
    """
    Normaliza URLs variadas para formato de canal

    Aceita:
    - https://youtube.com/@usuario
    - https://youtube.com/c/usuario
    - https://youtube.com/channel/UC...
    - https://youtube.com/user/usuario
    """
    # Se já é uma URL válida, retorna como está
    patterns = [
        r'youtube\.com/@',
        r'youtube\.com/c/',
        r'youtube\.com/channel/',
        r'youtube\.com/user/',
    ]

    if any(re.search(pattern, url) for pattern in patterns):
        return url

    # Se tem @ sem URL completa
    if url.startswith('@'):
        return f"https://youtube.com/{url}"

    return url


def main():
    # Ler URL do argumento ou stdin
    if len(sys.argv) > 1:
        channel_url = sys.argv[1]
    else:
        channel_url = sys.stdin.read().strip()

    if not channel_url:
        print(json.dumps({"error": "URL do canal não fornecida"}))
        sys.exit(1)

    # Normalizar URL
    channel_url = extract_channel_url(channel_url)

    # Buscar vídeos
    videos = get_channel_videos(channel_url, limit=3)

    # Output JSON
    result = {
        "videos": videos,
        "count": len(videos),
        "channel": channel_url
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
