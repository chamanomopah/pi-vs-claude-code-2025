# Pesquisa Remotion - Resumo Executivo

## Descobertas Principais

### 1. API Local ✓
- **Instalação:** `npx create-video@latest`
- **Pré-requisitos:** Node 16+ ou Bun 1.0.3+
- **FFmpeg:** Incluído desde v4.0
- **CLI:** `npx remotion render`, `npx remotion still`, `npx remotion studio`
- **Renderização em massa:** Loop com `renderMedia()` usando bundle único

### 2. Templates Reutilizáveis ✓
- **Composition:** Define vídeo com props padrão
- **InputProps:** Passa dados dinâmicos (CLI ou programático)
- **Estrutura:** Componentes React com useCurrentFrame()
- **Melhor prática:** Criar bundle uma vez, renderizar múltiplos vídeos

### 3. Transições ✓
- **Pacote:** `@remotion/transitions`
- **Componente:** `<TransitionSeries>`
- **Tipos:** fade, slide, wipe, flip(Pro), clockWipe, iris, cube(Pro)
- **Timing:** linearTiming() ou springTiming()

### 4. Legendas ✓
- **Pacote:** `@remotion/captions`
- **Formatos:** SRT, VTT, JSON
- **Parsing:** parseSrt(), parseVtt()
- **Uso:** `<Captions transcript={transcription} />`

### 5. Timestamps ✓
- **Componente:** `<Sequence from={0} durationInFrames={90}>`
- **Precisão:** Frame-by-frame com useCurrentFrame()
- **Cálculo:** currentTime = frame / fps

### 6. Casos de Uso Reais ✓
- Thumbnails YouTube (renderStill)
- Social media (múltiplas resoluções)
- E-commerce (produtos em massa)
- Vídeos educacionais (com transcrições)
- Anúncios dinâmicos

### 7. ComfyUI + Remotion ✓
- **Workflow:** ComfyUI gera frames → Remotion compõe vídeo
- **API:** POST para localhost:8188/prompt
- **Estratégia:** Pré-gerar frames ou gerar on-demand
- **Seed:** Usar frame como seed para consistência

## Links Úteis

- **Docs:** https://www.remotion.dev/docs
- **API:** https://www.remotion.dev/docs/api
- **CLI:** https://www.remotion.dev/docs/cli
- **Transitions:** https://www.remotion.dev/docs/transitions
- **Captions:** https://www.remotion.dev/docs/captions
- **GitHub:** https://github.com/remotion-dev/remotion
- **Discord:** https://remotion.dev/discord

## Próximos Passos

1. Criar projeto Remotion
2. Desenvolver templates base
3. Implementar renderização em massa
4. Integrar ComfyUI se necessário
5. Automatizar pipeline completo
