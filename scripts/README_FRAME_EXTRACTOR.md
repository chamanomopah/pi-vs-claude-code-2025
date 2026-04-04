# Extrator de Frames de Vídeo

Script Python simples para extrair frames de vídeos a cada segundo.

## 📋 Requisitos

- Python 3.7+
- OpenCV (opencv-python)
- yt-dlp (para baixar vídeos de URLs)

## 🚀 Instalação

```bash
# Instalar as dependências
pip install -r requirements.txt
```

Ou execute diretamente os scripts de atalho:

- **Windows**: `run_frame_extractor.bat`
- **Linux/Mac**: `./run_frame_extractor.sh`

## 🎬 Como Usar

### 1. Edite a URL do Vídeo

Abra o arquivo `video_frame_extractor.py` e altere a variável `VIDEO_URL` no início do arquivo:

```python
# Para vídeo do YouTube
VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Para arquivo local
VIDEO_URL = "C:/Videos/meu_video.mp4"
```

### 2. Execute o Script

```bash
python video_frame_extractor.py
```

## 📁 Estrutura de Saída

O script criará uma pasta `frames/` com subpastas para cada vídeo:

```
frames/
├── dQw4w9WgXcQ/
│   ├── frame_0000.00s.jpg
│   ├── frame_0001.00s.jpg
│   ├── frame_0002.00s.jpg
│   └── ...
└── sample_mp4/
    ├── frame_0000.00s.jpg
    └── ...
```

## ⚙️ Funcionalidades

- ✅ Suporta URLs do YouTube e outras plataformas (via yt-dlp)
- ✅ Suporta arquivos de vídeo locais
- ✅ Extrai 1 frame por segundo
- ✅ Cria pasta automática com base no ID do vídeo
- ✅ Nomes de arquivo com timestamp em segundos
- ✅ Limpeza automática de arquivos temporários

## 🔧 Personalização

Para mudar a taxa de extração de frames, edite a função `extrair_frames()`:

```python
# Exemplo: extrair 2 frames por segundo
intervalo_frames = int(fps / 2)

# Exemplo: extrair 1 frame a cada 5 segundos
intervalo_frames = int(fps * 5)
```

## 📝 Formato dos Nomes

Os frames são salvos no formato:
```
frame_XXXXX.XXs.jpg
```

Onde `XXXXX.XX` é o timestamp em segundos (ex: `frame_0012.50s.jpg` = frame no segundo 12.5)

## ❗ Limitações

- Funciona apenas com vídeos que têm FPS constante
- Requer yt-dlp instalado para baixar vídeos de URLs
- Vídeos muito longos podem demorar para processar

## 🆘 Troubleshooting

**Erro: "yt-dlp não encontrado"**
```bash
pip install yt-dlp
```

**Erro: "OpenCV não encontrado"**
```bash
pip install opencv-python
```

**Vídeo não abre**: Verifique se o arquivo existe e se o formato é suportado pelo OpenCV.
