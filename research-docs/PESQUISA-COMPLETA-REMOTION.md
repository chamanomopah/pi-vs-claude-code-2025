# Pesquisa Abrangente: Remotion para Geração de Vídeos em Massa

**Data:** 20 de abril de 2026  
**Versão Research:** Remotion 4.0.448+  
**Fonte:** https://www.remotion.dev/docs

---

## 📋 Índice

1. [API 100% Local](#1-api-100-local)
2. [Templates Reutilizáveis](#2-templates-reutilizáveis)
3. [Transições](#3-transições)
4. [Legendas](#4-legendas)
5. [Timestamps](#5-timestamps)
6. [Casos de Automação](#6-casos-de-automação)
7. [ComfyUI + Remotion](#7-comfyui--remotion)
8. [Links Úteis](#links-úteis)

---

## 1. API 100% LOCAL

### Instalação e Configuração

```bash
# Criar novo projeto
npx create-video@latest

# Adicionar pacotes
npx remotion add @remotion/transitions
npx remotion add @remotion/captions
```

### CLI Principais

```bash
# Renderizar vídeo
npx remotion render --codec=vp8 HelloWorld out/video.webm

# Renderizar imagem estática
npx remotion still MyComp out/image.png

# Iniciar Studio
npx remotion studio

# Listar composições
npx remotion compositions
```

### Renderização em Massa (Programático)

```javascript
import { bundle } from "@remotion/bundler";
import { renderMedia } from "@remotion/renderer";

const videos = [
  { id: 1, title: "Video 1", duration: 900 },
  { id: 2, title: "Video 2", duration: 1200 },
  { id: 3, title: "Video 3", duration: 1500 },
];

// Bundle único para performance
const bundleLocation = await bundle({
  entryPoint: "./src/index.ts",
});

// Loop sequencial
for (const video of videos) {
  await renderMedia({
    composition: {
      id: "MyVideo",
      width: 1920,
      height: 1080,
      fps: 30,
      durationInFrames: video.duration,
    },
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: `out/video-${video.id}.mp4`,
    inputProps: { title: video.title },
  });
}

// Loop paralelo (mais rápido)
const concurrency = 4;
for (let i = 0; i < videos.length; i += concurrency) {
  const chunk = videos.slice(i, i + concurrency);
  await Promise.all(
    chunk.map((video) =>
      renderMedia({
        composition: {
          id: "MyVideo",
          width: 1920,
          height: 1080,
          fps: 30,
          durationInFrames: video.duration,
        },
        serveUrl: bundleLocation,
        codec: "h264",
        outputLocation: `out/video-${video.id}.mp4`,
        inputProps: { title: video.title },
      })
    )
  );
}
```

---

## 2. TEMPLATES REUTILIZÁVEIS

### Estrutura Básica

```tsx
import { Composition } from "remotion";
import { MyTemplate } from "./MyTemplate";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyTemplate"
      component={MyTemplate}
      durationInFrames={900}
      width={1920}
      height={1080}
      fps={30}
      defaultProps={{
        title: "Default Title",
        subtitle: "Default Subtitle",
        primaryColor: "#3b82f6",
        logo: "/logo.png",
      }}
    />
  );
};
```

### Template com Props Dinâmicas

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

interface TemplateProps {
  title: string;
  subtitle: string;
  primaryColor: string;
  items: Array<{ icon: string; text: string }>;
}

export const MyTemplate: React.FC<TemplateProps> = ({
  title,
  subtitle,
  primaryColor,
  items,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  
  return (
    <AbsoluteFill style={{ backgroundColor: "#0f172a" }}>
      <div style={{ opacity, padding: 60 }}>
        <h1 style={{ fontSize: 80, color: primaryColor }}>{title}</h1>
        <p style={{ fontSize: 40, color: "#94a3b8" }}>{subtitle}</p>
      </div>
      {items.map((item, index) => (
        <div key={index} style={{
          marginTop: 40,
          marginLeft: 60,
          opacity: interpolate(frame, [30 + index * 20, 60 + index * 20], [0, 1]),
        }}>
          <img src={item.icon} style={{ width: 50 }} />
          <span style={{ fontSize: 32, color: "#ffffff" }}>{item.text}</span>
        </div>
      ))}
    </AbsoluteFill>
  );
};
```

### Passagem de Dados

```bash
# Via CLI
npx remotion render MyTemplate out/video.mp4 --props='{"title":"Meu Título"}'
```

```javascript
// Via programático
await renderMedia({
  composition: { id: "MyTemplate", width: 1920, height: 1080, fps: 30 },
  serveUrl: bundleLocation,
  codec: "h264",
  outputLocation: "out/video.mp4",
  inputProps: {
    title: "Meu Título",
    subtitle: "Minha Subtítulo",
    primaryColor: "#3b82f6",
    items: [
      { icon: "/icon1.png", text: "Item 1" },
      { icon: "/icon2.png", text: "Item 2" },
    ],
  },
});
```

---

## 3. TRANSIÇÕES

### Instalação

```bash
npx remotion add @remotion/transitions
```

### Transições Disponíveis

- **fade** - Esmaecer (gratuito)
- **slide** - Deslizar (4 direções) (gratuito)
- **wipe** - Mascarar (gratuito)
- **flip** - Girar 3D (Pro)
- **clockWipe** - Máscara circular (gratuito)
- **iris** - Máscara radial (gratuito)
- **cube** - Cubo 3D (Pro)

### Exemplo Completo

```tsx
import { TransitionSeries } from "@remotion/transitions";
import { fade, slide, wipe } from "@remotion/transitions/presets";
import { linearTiming, springTiming } from "@remotion/transitions/timings";

export const VideoWithTransitions: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={90}>
        <SceneA />
      </TransitionSeries.Sequence>
      
      <TransitionSeries.Transition 
        durationInFrames={30}
        preset={fade()}
        timing={linearTiming({ durationInFrames: 30 })}
      />
      
      <TransitionSeries.Sequence durationInFrames={90}>
        <SceneB />
      </TransitionSeries.Sequence>
      
      <TransitionSeries.Transition 
        durationInFrames={45}
        preset={slide({ direction: "from-left" })}
        timing={springTiming({ durationInFrames: 45 })}
      />
      
      <TransitionSeries.Sequence durationInFrames={90}>
        <SceneC />
      </TransitionSeries.Sequence>
      
      <TransitionSeries.Transition 
        preset={wipe({ direction: "from-top" })}
      />
      
      <TransitionSeries.Sequence durationInFrames={90}>
        <SceneD />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

---

## 4. LEGENDAS

### Instalação

```bash
npx remotion add @remotion/captions
```

### Formatos Suportados

- **SRT** (SubRip)
- **VTT** (WebVTT)
- **JSON**

### Exemplo Básico

```tsx
import { Captions } from "@remotion/captions";

const transcription = [
  { start: 0, end: 2500, text: "Bem-vindo ao Remotion" },
  { start: 2500, end: 5000, text: "Uma ferramenta poderosa" },
];

export const VideoWithCaptions: React.FC = () => {
  return (
    <AbsoluteFill>
      <VideoBackground />
      <Captions 
        transcript={transcription}
        style={{ 
          fontSize: 60, 
          color: "white",
          textShadow: "2px 2px 4px rgba(0,0,0,0.8)",
        }}
      />
    </AbsoluteFill>
  );
};
```

### Parse de Arquivos

```tsx
import { parseSrt } from "@remotion/captions/srt";
import { parseVtt } from "@remotion/captions/vtt";

// Parse SRT
const srtContent = await fetch("/captions.srt").then(r => r.text());
const transcription = parseSrt(srtContent);

// Parse VTT
const vttContent = await fetch("/captions.vtt").then(r => r.text());
const transcription = parseVtt(vttContent);
```

---

## 5. TIMESTAMPS

### Sequência Básica

```tsx
import { Sequence } from "remotion";

export const ImageSlideshow: React.FC = () => {
  return (
    <AbsoluteFill>
      {/* Imagem 1: 0-90 frames (0-3s) */}
      <Sequence from={0} durationInFrames={90}>
        <ImageSlide image="/image1.jpg" />
      </Sequence>
      
      {/* Imagem 2: 90-270 frames (3-9s) */}
      <Sequence from={90} durationInFrames={180}>
        <ImageSlide image="/image2.jpg" />
      </Sequence>
      
      {/* Imagem 3: 270-450 frames (9-15s) */}
      <Sequence from={270} durationInFrames={180}>
        <ImageSlide image="/image3.jpg" />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### Timeline com Timestamps Específicos

```tsx
interface ImageSegment {
  image: string;
  startFrame: number;
  endFrame: 
