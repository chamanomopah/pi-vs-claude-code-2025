# TMT - Workflow 01: Modelagem de Canal (Top Videos)

**Objetivo**: Analisar canal do YouTube e gerar metaprompts especializados para criação de conteúdo.

---

## 1. ENTRADA
- **Fonte**: URL do canal do YouTube (ex: `https://www.youtube.com/@channelname/videos`)
- **Método**: Manual (Webhook) ou disparado por Schedule Trigger
- **Parâmetro único**: `channel_url`

---

## 2. SCRIPT PYTHON - EXTRAÇÃO DE VÍDEOS

**Arquivo**: `scripts/youtube_channel_scraper.py` (NOVO)

**Função**: 
- Recebe URL do canal
- Lista todos os vídeos do canal
- Ordena por views (decrescente)
- Retorna top 3 vídeos com metadata

**Saída esperada** (JSON):
```json
[
  {
    "video_id": "abc123",
    "title": "Título do Vídeo",
    "url": "https://youtube.com/watch?v=abc123",
    "views": 1500000,
    "duration": "10:25",
    "thumbnail": "https://..."
  },
  ...
]
```

**Dependências**: `yt-dlp` ou API do YouTube Data

---

## 3. PROCESSAMENTO PARALELO (TOP 3)

### 3.1 Extração de Transcrição
**Script existente**: `scripts/youtube_transcript_downloader.py`

**Nó n8n**: Execute Command
```
cd C:\path\scripts & py youtube_transcript_downloader.py "{{ $json.url }}"
```

**Saída**: Arquivo `.txt` com transcrição orgânica (sentenças completas)

---

### 3.2 Extração de Frames
**Script existente**: `scripts/video_frame_extractor.py`

**Nó n8n**: Execute Command
```
cd C:\path\scripts & py video_frame_extractor.py "{{ $json.url }}"
```

**Saída**: Pasta `frames/<video_id>/` com frames a cada 1 segundo

---

## 4. AGENTES CLAUDE CODE (CLI)

### 4.1 Agente 1 - Metaprompt Especialista em Scripts

**Objetivo**: Analisar transcrições dos top 3 vídeos e extrair padrões

**Nó n8n**: Execute Command
```
claude -p "Analisa estas 3 transcrições dos vídeos mais assistidos do canal:
{{ transcrição_video_1 }}

{{ transcrição_video_2 }}

{{ transcrição_video_3 }}

Cria um METAPROMPT que capture:
1. Estilo de linguagem (tom, vocabulário, gírias)
2. Estrutura narrativa (abertura, desenvolvimento, fechamento)
3. Padrões de rhetoric (perguntas, metáforas, exemplos)
4. Call-to-actions típicos

Output: JSON com campos 'style', 'structure', 'rhetoric', 'cta'"
```

**Saída**: JSON com metaprompt de script

---

### 4.2 Agente 2 - Vision (Análise de Frames)

**Objetivo**: Analisar frames visuais e extrair padrões estéticos

**Nó n8n**: Execute Command
```
claude -p "Analisa estes frames dos vídeos mais assistidos do canal:
{{ frames_video_1 }} (path: frames/abc123/)
{{ frames_video_2 }} (path: frames/def456/)
{{ frames_video_3 }} (path: frames/ghi789/)

Para cada conjunto de frames, descreve:
1. Paleta de cores dominante
2. Composição de cena (close-up, wide, B-roll)
3. Estilo visual (minimalista, colorido, sério, divertido)
4. Text overlays e tipografia
5. Transições e efeitos visuais

Output: JSON com campos 'colors', 'composition', 'style', 'overlays', 'transitions'"
```

**Saída**: JSON com metaprompt visual

---

## 5. ESTRUTURA DE WORKFLOW N8N

```
[Schedule Trigger/Webhook]
        ↓
[Google Sheets - Pegar Canal] ← Lê URLs de canais para processar
        ↓
[Loop - Para cada canal]
        ↓
[Execute Command - Python Channel Scraper]
        ↓
[Code Node - Parse Top 3 Videos]
        ↓
[Split In Batches - Top 3]
        ↓
    ┌──────────────────┬──────────────────┐
    ↓                  ↓                  ↓
[Vídeo 1]          [Vídeo 2]          [Vídeo 3]
    ↓                  ↓                  ↓
┌──────────────────┬──────────────────┐
↓                  ↓                  ↓
[Transcrição]    [Transcrição]    [Transcrição]   (paralelo)
[Frames]         [Frames]         [Frames]
└──────────────────┴──────────────────┘
        ↓
[Wait - Aguarda todos terminarem]
        ↓
[Merge - Junta transcrições]
        ↓
[Merge - Junta paths de frames]
        ↓
[Execute Command - Claude Agente 1 (Script)]
        ↓
[Execute Command - Claude Agente 2 (Vision)]
        ↓
[Code Node - Parse outputs]
        ↓
[Google Sheets - Salvar Metaprompts]
        ↓
[End]
```

---

## 6. VARIÁVEIS E CAMINHOS

**Estrutura de pastas**:
```
project_root/
├── scripts/
│   ├── youtube_transcript_downloader.py
│   ├── video_frame_extractor.py
│   └── youtube_channel_scraper.py (NOVO)
├── transcripts/
│   ├── video_1.txt
│   ├── video_2.txt
│   └── video_3.txt
└── frames/
    ├── video_1_id/
    ├── video_2_id/
    └── video_3_id/
```

**Variáveis de ambiente n8n**:
- `PROJECT_PATH`: `C:\Users\JOSE\.claude\.IMPLEMENTATION\projects\B-software\H-minimum-orquestration\pi-vs-claude-code`
- `SCRIPTS_PATH`: `${PROJECT_PATH}\scripts`
- `OUTPUT_PATH`: `${PROJECT_PATH}\outputs`

---

## 7. ARMAZENAMENTO (GOOGLE SHEETS)

**Sheet**: `Canal_pisicologia` → Aba: `channels`

**Colunas**:
| canal | image_meta_prompt | script_meta_prompt | thumbnail_meta_prompt | title_meta_prompt |
|-------|-------------------|--------------------|-----------------------|-------------------|

**Updated rows**: Cada canal processado recebe seus 4 metaprompts

---

## 8. SCRIPTS NECESSÁRIOS

### 8.1 NOVO: `youtube_channel_scraper.py`

**Função**: 
```python
# Pseudocódigo
def get_top_videos(channel_url, limit=3):
    videos = yt_dlp channel_info
    sorted_videos = sort_by_views(videos)
    return sorted_videos[:limit]
```

**Instalação**: `pip install yt-dlp`

---

## 9. CONSIDERAÇÕES

### 9.1 Performance
- Python scripts devem ser lightweight
- Claude CLI pode ser lento (considerar timeout)
- Executar transcrições em paralelo

### 9.2 Rate Limits
- YouTube API tem quotas (se usar API oficial)
- yt-dlp pode ser limitado pelo YouTube
- Considerar cache de resultados

### 9.3 Error Handling
- Vídeo sem transcrição → pular ou usar plano B
- Download falhou → tentar próximo vídeo
- Claude CLI timeout → retry com prompt menor

---

## 10. PRÓXIMOS PASSOS (Após aprovação)

1. ✅ Criar `youtube_channel_scraper.py`
2. ✅ Testar scripts existentes individualmente
3. ✅ Criar workflow n8n estrutura básica
4. ✅ Implementar nós do n8n (usando tools/n8n/nodes_create.py)
5. ✅ Conectar nós (usando tools/n8n/connections_create.py)
6. ✅ Testar com 1 canal real
7. ✅ Validar outputs dos agentes Claude
8. ✅ Salvar metaprompts no Google Sheets

---

**Status**: 📋 PLANEJAMENTO - Aguardando aprovação para implementação
**Data**: 2026-04-07
