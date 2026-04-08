# Scripts Python - Projeto 1

Este diretório contém os scripts Python necessários para o funcionamento dos workflows do projeto 1 (Youtube Video Production).

---

## SCRIPTS

### 1. youtube_channel_scraper.py
**Função**: Busca os top 3 vídeos de um canal do YouTube

**Uso**:
```bash
python youtube_channel_scraper.py "https://youtube.com/@canal"
```

**Output**:
```json
{
  "videos": [
    {"url": "https://youtube.com/watch?v=...", "title": "..."},
    ...
  ],
  "count": 3,
  "channel": "https://youtube.com/@canal"
}
```

---

### 2. youtube_transcript_downloader.py
**Função**: Baixa a transcrição de um vídeo

**Uso**:
```bash
python youtube_transcript_downloader.py "https://youtube.com/watch?v=..."
```

**Output**:
```json
{
  "transcript_path": "/path/to/transcript.txt",
  "video_id": "abc123",
  "language": "pt",
  "segments": 150
}
```

---

### 3. video_frame_extractor.py
**Função**: Extrai frames de um vídeo e cria ZIP

**Uso**:
```bash
python video_frame_extractor.py "https://youtube.com/watch?v=..."
```

**Output**:
```json
{
  "frames_path": "/path/to/frames.zip",
  "video_id": "abc123",
  "frames_count": 30,
  "fps": 1
}
```

---

## INSTALAÇÃO DE DEPENDÊNCIAS

### Requisitos
- Python 3.8+
- pip

### Instalar bibliotecas
```bash
# Básico
pip install yt-dlp opencv-python requests

# Opcional: para transcrições via API
pip install youtube-transcript-api

# Para Windows: pode precisar do Visual C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### Verificar instalação
```bash
python -c "import yt_dlp; print('yt-dlp OK')"
python -c "import cv2; print('opencv OK')"
python -c "import requests; print('requests OK')"
```

---

## TESTE DOS SCRIPTS

### Teste 1: Buscar vídeos
```bash
python youtube_channel_scraper.py "@canal_exemplo"
```

### Teste 2: Baixar transcrição
```bash
python youtube_transcript_downloader.py "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

### Teste 3: Extrair frames
```bash
python video_frame_extractor.py "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

---

## ESTRUTURA DE DIRETÓRIOS

Após execução, os scripts criarão:

```
scripts/
├── youtube_channel_scraper.py
├── youtube_transcript_downloader.py
├── video_frame_extractor.py
├── transcripts/              # Criado automaticamente
│   └── abc123_transcript.txt
└── frames/                   # Criado automaticamente
    └── abc123/
        ├── abc123_frames.zip
        └── images/
            ├── frame_0000.jpg
            ├── frame_0001.jpg
            └── ...
```

---

## INTEGRAÇÃO COM N8N

### No node Execute Command, usar:

**Para Scraper**:
```
command: python C:/path/to/scripts/youtube_channel_scraper.py "{{ $json.canal_url }}"
```

**Para Transcrição**:
```
command: python C:/path/to/scripts/youtube_transcript_downloader.py "{{ $json.url }}"
```

**Para Frames**:
```
command: python C:/path/to/scripts/video_frame_extractor.py "{{ $json.url }}"
```

---

## SOLUÇÃO DE PROBLEMAS

### Erro: "yt_dlp não instalado"
```bash
pip install yt-dlp --upgrade
```

### Erro: "opencv-python não instalado"
```bash
pip install opencv-python
```

### Erro: "Nenhuma transcrição disponível"
- O vídeo pode não ter legendas
- Tente usar `youtube_transcript_api` para legendas automáticas

### Erro: "Não foi possível abrir o vídeo"
- Verifique se o yt-dlp baixou o vídeo corretamente
- Pode ser problema de codec (tente usar ffmpeg)

---

## CONFIGURAÇÕES AVANÇADAS

### Mudar número de frames
No `video_frame_extractor.py`, altere:
```python
fps = 1  # Frames por segundo (padrão: 1)
max_frames = 30  # Máximo de frames (padrão: 30)
```

### Mudar idioma da transcrição
No `youtube_transcript_downloader.py`, altere:
```python
subtitleslangs=['pt', 'en']  # Ordem de preferência
```

### Mudar número de vídeos
No `youtube_channel_scraper.py`, altere:
```python
videos = get_channel_videos(channel_url, limit=5)  # Padrão: 3
```

---

## LICENÇA

MIT License - Uso livre para projetos pessoais e comerciais.
