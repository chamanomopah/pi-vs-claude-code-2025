# PLANO: Divisão Workflow 00 em 4 Partes

**Projeto**: 1_Youtube_video_production  
**Workflow original**: 00_modeling_workflow.json

---

## PARTE 1 - CAPTURA (3 vídeos)

**Objetivo**: Obter top 3 vídeos do canal

**Nodes**:
1. Schedule Trigger → dispara workflow
2. Google Sheets (pegar canal) → lê URL do canal
3. Execute Command (find videos links) → python channel scraper
4. IF (valida tem vídeos) → se vazio skip, se tem continua
5. **Google Sheets (salvar URLs capturadas)** → coluna `videos_urls`

**Saída**: Lista com 3 URLs salvas na planilha

**Trigger**: Schedule ou Webhook

---

## PARTE 2 - LOOP PROCESSAMENTO

**Objetivo**: Para cada vídeo: pegar transcrição + frames

**Nodes**:
1. Split In Batches (batch size=1)
   - main[0] → Parte 3 (fim loop)
   - main[1] → processamento
2. Set (input) → prepara url_video
3. Execute Command (url to transcrição) → python transcript
4. Set (input1) → prepara url_video
5. Execute Command (baixar frames) → python frame extractor
6. Wait → sincroniza transcrição + frames
7. Merge → junta resultados
8. **Google Sheets (salvar transcrições/frames)** → colunas `transcript_path`, `frames_path`
9. Loop → volta para Split In Batches

**Saída**: Array salvo na planilha

**Padrão**: Loop Simples (main[1] → process → wait → volta)

---

## PARTE 3 - META PROMPTS

**Objetivo**: Agentes analisam e geram 2 meta prompts

**Nodes**:
1. Set (input2) → prepara para agent image
2. Execute Command (agent image prompt especialist) → claude vision
3. Set (input3) → prepara para agent script
4. Execute Command (agent script prompt especialist) → claude script
5. Wait → sincroniza ambos agents
6. Merge → junta os 2 meta prompts
7. **Google Sheets (salvar meta prompts)** → colunas `script_meta_prompt`, `image_meta_prompt`

**Saída**: Meta prompts salvos

**Agentes**: Claude Code CLI via Execute Command

---

## PARTE 4 - GERAÇÃO FINAL

**Objetivo**: Salvar resultado final consolidado

**Nodes**:
1. Google Sheets (salvar scripts) → confirmação final
2. Google Drive (salvar imagens) → upload frames (opcional)
3. Webhook Response → sucesso

**Saída**: Confirmação completa

---

## CONEXÕES ENTRE PARTES

```
Parte 1 (último node) → Split In Batches (inicia Parte 2)
Parte 2 (main[0]) → Parte 3 (primeiro node)
Parte 3 (último node) → Parte 4 (primeiro node)
```

---

## SHEETS - COLUNAS

| canal | videos_urls | transcript_path | frames_path | script_meta_prompt | image_meta_prompt |
|-------|-------------|-----------------|-------------|--------------------|-------------------|

---

## ARQUIVOS NECESSÁRIOS

**Scripts Python**:
- `youtube_channel_scraper.py`
- `youtube_transcript_downloader.py`
- `video_frame_extractor.py`

---

## PRÓXIMO PASSO

Criar os 4 arquivos JSON dos workflows
