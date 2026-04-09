# META-PROMPTS: Canal de Psicologia (1-psicologia)

## 📋 Resumo Executivo

Este diretório contém os meta-prompts completos para produção de vídeos do canal de psicologia no estilo "Explicado" (personagem colorido, fundo preto e branco). Os meta-prompts foram desenvolvidos seguindo a metodologia de 3 fases e são baseados na análise do canal competidor.

## 🎯 Estrutura dos Meta-Prompts

### 01. Roteiro (`01-roteiro.md`)
**Finalidade**: Gerar roteiros completos e envolventes para vídeos de psicologia.

**Elementos-chave**:
- Estrutura de roteiro em cenas de 5-8 segundos
- Hook inicial gerador de identificação
- Conteúdo baseado em dados e psicologia científica
- Tom analítico, empático e em primeira pessoa
- Formato padronizado para fácil conversão em imagem+áudio

**Variáveis de entrada**: Tema, público-alvo, foco principal, dados adicionais

---

### 02. Imagem do Personagem (`02-imagem-personagem.md`)
**Finalidade**: Criar e manter consistência do personagem que aparece em todos os vídeos e thumbnails.

**Elementos-chave**:
- Personagem consistente: sempre o mesmo em todas as aparições
- Estilo: Ilustração digital 2D, cores vibrantes
- Regra de ouro: Personagem colorido, fundo 100% P&B
- Múltiplas poses e expressões para diferentes contextos
- Reconhecível como o narrador do canal

**Variáveis**: Etnia, estilo de roupa, característica marcante

---

### 03. Imagens das Cenas (`03-imagens-cenas.md`)
**Finalidade**: Gerar imagens que ilustrem cada cena do roteiro mantendo a estética do canal.

**Tipos de imagens**:
1. **Simbólicas/Metáforas**: Conceitos abstratos e estados mentais
2. **Pessoa/Silhueta**: Situações relacionais e emoções
3. **Personagem Narrador**: Quando o narrador aparece diretamente
4. **Dados/Infográficos**: Estatísticas e conceitos científicos
5. **Abstratas/Texturais**: Transições e profundidade psicológica

**Regra fundamental**: Elemento principal colorido, fundo grayscale

---

### 04. Thumbnail (`04-thumbnail.md`)
**Finalidade**: Criar thumbnails que maximizam CTR mantendo identidade do canal.

**Elementos-chave**:
- Personagem central consistente
- Expressão impactante (surpresa, realização, curiosidade)
- Fundo P&B para máximo contraste
- Texto curto (2-3 palavras) e impactante
- Composição limpa e focalizada

**Fórmulas de sucesso**: Revelação, pergunta, estatística choque, antes vs depois

---

### 05. Título (`05-titulo.md`)
**Finalidade**: Gerar títulos otimizados para CTR e SEO do YouTube.

**Fórmulas testadas**:
1. "O Que Ninguém Te Diz" → Revelação de segredo
2. Números + Revelação → "78% das pessoas..."
3. Pergunta Provocativa → "Por que você sempre..."
4. O Erro Que Você Comete → Identificação de problema
5. História/Narração → "Como eu percebi..."
6. Antes vs Depois → Transformação

**Estrutura recomendada**: `[TÍTULO] - Explicado`

---

### 06. Áudio de Narração (`06-audio-narracao.md`)
**Finalidade**: Definir processo de geração de narração TTS de alta qualidade.

**Ferramenta principal**: Edge TTS (100% gratuito)

**Parâmetros ideais**:
- Voz: pt-BR-AntonioNeural (masculina, profunda)
- Velocidade: +0% a -5% (moderada)
- Pitch: -5% (voz grave confere credibilidade)
- Volume: +5% (clareza)

**Estrutura**: Um arquivo MP3 por cena

---

### 07. Montagem de Vídeo (`07-montagem-video.md`)
**Finalidade**: Processo completo de montagem com FFmpeg.

**Etapas**:
1. Montagem de clipes individuais (imagem + áudio)
2. Criação de lista de concatenação
3. Concatenação de todos os clipes
4. Adição de trilha sonora
5. Exportação final otimizada para YouTube

**Configurações finais**:
- Codec: H.264 (libx264)
- Resolução: 1920x1080 (Full HD)
- CRF: 21 (qualidade)
- Áudio: AAC 192k
- Faststart: Habilitado

---

## 🎨 Identidade Visual do Canal

### Paleta de Cores (Mapa Simbólico)
```markdown
🔴 VERMELHO    → Emoção forte, raiva, paixão, urgência
🟠 LARANJA     → Mudança, transformação, energia
🟡 AMARELO     → Esperança, atenção, insights
🟢 VERDE       → Crescimento, cura, equilíbrio, dinheiro
🔵 AZUL        → Razão, lógica, calma, introspecção
🟣 ROXO        → Espiritualidade, mistério, inconsciente
🟤 MARROM      → Terra, estabilidade, passado
⚫ CINZA ESCURO → Sombra, medo, desconhecido
⚪ BRANCO       → Luz, verdade, clareza, consciência
```

### Regra Visual Fundamental
**Personagem/Elemento focal**: Cores vibrantes e saturadas
**Fundo e contexto**: 100% grayscale (preto e branco)
**Contraste**: Sempre alto para destacar o elemento principal

---

## 📊 Análise do Canal Competidor

### Canal "Explicado" - Franklin

**Características identificadas**:
- ✅ Personagem consistente em todos os vídeos/thumbnails
- ✅ Estilo colorido (personagem) + P&B (fundo)
- ✅ Narração em primeira pessoa, analítica e profunda
- ✅ Baseada em dados estatísticos e pesquisas
- ✅ Estrutura de roteiro: Hook → Contexto → Dados → Insight → CTA
- ✅ Títulos com diferencial "Explicado"
- ✅ Vídeos de 2-3 minutos (canal dark)
- ✅ Thumbnail expressiva com personagem central

**Arquivos de análise**:
- Transcrição: `video_transcript.txt`
- Frames extraídos: `frames/QWIxFghgrS0/` (653 frames)

---

## 🚀 Metodologia de 3 Fases

### FASE 1: Geração de Meta-Prompts ✅ (CONCLUÍDA)
- [x] Análise de canal competidor (transcrição + frames)
- [x] Identificação de padrões de roteiro, visual, título
- [x] Criação de meta-prompts para todas as etapas
- [x] Documentação completa para reuso

### FASE 2: Vídeo MVP Manual (PRÓXIMA)
- [ ] Escolher tema do primeiro vídeo
- [ ] Usar meta-prompt de roteiro para gerar roteiro completo
- [ ] Gerar imagem do personagem base (definir aparência)
- [ ] Para cada cena: gerar imagem + narração TTS
- [ ] Montar clipes com FFmpeg
- [ ] Concatenar e adicionar trilha
- [ ] Gerar thumbnail e título
- [ ] Validar qualidade e ajustar meta-prompts se necessário

### FASE 3: Automação N8N (FUTURO)
- [ ] Documentar fluxo completo validado
- [ ] Criar workflow N8N
- [ ] Configurar nós: LLM (meta-prompts), APIs (imagem, TTS), FFmpeg
- [ ] Testar e validar workflow
- [ ] Escalar produção

---

## 🛠️ Stack Tecnológico (100% Gratuito)

| Etapa | Ferramenta | Custo |
|-------|-----------|-------|
| **LLM** | Gemini 2.5 Flash (Nano Banana) | Gratuita |
| **Imagens** | Pollinations.ai ou Gemini 2.5 Flash | Gratuita |
| **TTS** | Edge TTS (Python) | 100% Gratuito |
| **Edição** | FFmpeg | Open Source |
| **Orquestração** | Capacidades agênticas → N8N | Gratuito |

---

## 📁 Estrutura de Diretórios

```
video-production/1-psicologia/
├── meta-prompts/           (ESTE DIRETÓRIO)
│   ├── 00-index.md         (Este arquivo)
│   ├── 01-roteiro.md
│   ├── 02-imagem-personagem.md
│   ├── 03-imagens-cenas.md
│   ├── 04-thumbnail.md
│   ├── 05-titulo.md
│   ├── 06-audio-narracao.md
│   └── 07-montagem-video.md
├── assets/                 (Trilhas, fonts)
│   └── trilhas/
└── videos/                 (Vídeos individuais)
    └── <numero-titulo>/
        ├── 01-roteiro.md
        ├── 02-imagens/    (cena_001.jpg, ...)
        ├── 03-image_prompts/ (cena_001.txt, ...)
        ├── 04-audio/
        │   ├── naracao/   (cena_001.mp3, ...)
        │   └── trilha/    (trilha_fundo.mp3)
        ├── 05-clipes/     (cena_001.mp4, ...)
        ├── 06-final/      (video_final.mp4)
        └── 08-processo.md (Documentação)
```

---

## 🎯 Como Usar Estes Meta-Prompts

### Para Criar um Novo Vídeo:

1. **Definir o tema**: Escolha o tópico psicológico
2. **Gerar roteiro**: Use `01-roteiro.md` com o tema
3. **Criar personagem**: Use `02-imagem-personagem.md` (se primeira vez)
4. **Gerar imagens**: Use `03-imagens-cenas.md` para cada cena
5. **Gerar narração**: Use `06-audio-narracao.md` para cada cena
6. **Montar clipes**: Use `07-montagem-video.md` (scripts Python)
7. **Criar thumbnail**: Use `04-thumbnail.md`
8. **Definir título**: Use `05-titulo.md`
9. **Exportar final**: Script completo em `07-montagem-video.md`

### Para Automatizar no N8N:

1. Cada meta-prompt vira um nó LLM separado
2. Use os prompts exatamente como definidos
3. Configure nós de API (imagem, TTS) com os parâmetros especificados
4. Use FFmpeg via nó Execute Command com os comandos documentados
5. Valide fluxo completo antes de escalar

---

## 📝 Próximos Passos

### Imediatos (FASE 2)
1. Escolher tema do primeiro vídeo MVP
2. Definir aparência do personagem (etnia, roupa, acessório)
3. Gerar roteiro usando `01-roteiro.md`
4. Testar geração de imagem do personagem
5. Validar toda a cadeia de produção manualmente

### Curto Prazo
6. Criar vídeo MVP completo (~1 minuto)
7. Validar qualidade em cada etapa
8. Ajustar meta-prompts baseado em aprendizados
9. Documentar processo em `08-processo.md`

### Médio Prazo (FASE 3)
10. Criar workflow N8N baseado no processo validado
11. Testar automação completa
12. Escalar produção para múltiplos vídeos

---

## 🔗 Documentação Relacionada

- **Skill de Vídeo**: `.pi/skills/video/agentic-to-n8n/`
- **Ferramentas de Vídeo**: `tools/video/`
  - `youtube_transcript_downloader.py`
  - `video_frame_extractor.py`
  - `youtube_channel_scraper.py`
- **Metodologia**: Ver skill completo para detalhes das 3 fases

---

**Status**: Meta-prompts criados e prontos para FASE 2 (Vídeo MVP Manual)

**Próximo passo**: Escolher tema do primeiro vídeo e iniciar produção manual
