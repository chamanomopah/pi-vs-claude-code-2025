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

## 🎬 Como Usar

### Uso Básico

```bash
python video_frame_extractor.py "URL_OU_CAMINHO"
```

### Exemplos

```bash
# URL do YouTube (baixa automaticamente)
python video_frame_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Arquivo local com formato file:///
python video_frame_extractor.py "file:///C:/Users/JOSE/Videos/meu_video.mp4"

# Arquivo local com caminho direto (Windows)
python video_frame_extractor.py "C:/Videos/meu_video.mp4"

# Arquivo local com caminho direto (Linux/Mac)
python video_frame_extractor.py "/home/user/videos/meu_video.mp4"
```

### Opções da Linha de Comando

```bash
python video_frame_extractor.py --help
```

| Opção | Descrição |
|-------|-----------|
| `url` | URL ou caminho do vídeo (obrigatório) |
| `-o, --output` | Nome da pasta de saída (opcional) |
| `-f, --fps` | Frames por segundo para extrair (padrão: 1) |

### Formatos Suportados

| Formato | Exemplo | Descrição |
|---------|---------|-----------|
| URL Remota | `https://www.youtube.com/watch?v=XXXXX` | Baixa o vídeo automaticamente |
| file:/// (Windows) | `file:///C:/Videos/meu_video.mp4` | Arquivo local no Windows |
| file:/// (Linux/Mac) | `file:///home/user/videos/meu_video.mp4` | Arquivo local no Linux/Mac |
| Caminho direto | `C:/Videos/meu_video.mp4` | Caminho direto do arquivo |

**Nota:** O formato `file:///` é útil para manter consistência com URLs e é compatível com muitas ferramentas que geram caminhos neste formato.

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
- ✅ Suporta arquivos de vídeo locais (caminho direto ou file:///)
- ✅ Extrai 1 frame por segundo (configurável via `-f`)
- ✅ Cria pasta automática com base no ID do vídeo
- ✅ Nomes de arquivo com timestamp em segundos
- ✅ Limpeza automática de arquivos temporários
- ✅ Detecção automática do tipo de entrada (URL/file://:/local)
- ✅ Interface de linha de comando compatível com padrão Unix

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
