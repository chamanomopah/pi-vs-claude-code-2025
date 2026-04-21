# Pesquisa Abrangente sobre Remotion para Geração de Vídeos em Massa

**Data:** 20 de abril de 2026
**Versão:** 4.0.448+

## 1. API Local

### Instalação
```bash
npx create-video@latest
```

### CLI
```bash
npx remotion render --codec=vp8 HelloWorld out/video.webm
npx remotion still MyComp out/image.png
```

## 2. Templates

### Composition
```tsx
<Composition
  id="MyTemplate"
  component={MyTemplate}
  durationInFrames={900}
  width={1920}
  height={1080}
  fps={30}
/>
```

## 3. Transições

```bash
npx remotion add @remotion/transitions
```

Transições: fade, slide, wipe, flip, clockWipe, iris, cube

## 4. Legendas

```bash
npx remotion add @remotion/captions
```

Formatos: SRT, VTT, JSON

## 5. Timestamps

```tsx
<Sequence from={0} durationInFrames={90}>
  <ImageSlide image="/image1.jpg" />
</Sequence>
```

## Links

- Docs: https://www.remotion.dev/docs
- GitHub: https://github.com/remotion-dev/remotion
- Discord: https://remotion.dev/discord

---

## DETALHES COMPLETOS POR SEÇÃO

### 1. API DO REMOTION 100% LOCAL

#### Renderização em Massa Completa
```javascript
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill } from "@remotion/renderer";
import { webpackOverride } from "remotion";

// Configuração
const config = {
  concurrency: 4, // Número de renderizações paralelas
  codec: "h264",
  pixelFormat: "yuv420p",
  quality: 80,
};

// Bundle único para múltiplas renderizações
const bundleLocation = await bundle({
  entryPoint: "./src/index.ts",
  webpackOverride: (config) => {
    // Otimizações
    config.resolve.symlinks = false;
    return config;
  },
});

// Dados dos vídeos
const videos = [
  { id: 1, title: "Vídeo 1", props: { color: "#ff0000" } },
  { id: 2, title: "Vídeo 2", props: { color: "#00ff00" } },
  { id: 3, title: "Vídeo 3", props: { color: "#0000ff" } },
];

// Renderização paralela
const chunks = [];
for (let i = 0; i < videos.length; i += config.concurrency) {
  chunks.push(videos.slice(i, i + config.concurrency));
}

for (const chunk of chunks) {
  await Promise.all(
    chunk.map((video) =>
      renderMedia({
        composition: {
          id: "MyVideo",
          width: 1920,
          height: 1080,
          fps: 30,
          durationInFrames: 900,
        },
        serveUrl: bundleLocation,
        codec: config.codec,
        outputLocation: `out/video-${video.id}.mp4`,
        inputProps: { ...video.props, title: video.title },
      })
    )
  );
}
```

#### Comandos CLI Avançados
```bash
# Renderizar com sobreescrita
npx remotion render MyComp out/video.mp4 --overwrite

# Renderizar sequência de imagens
npx remotion render MyComp out/frame.png --sequence

# Renderizar com qualidade específica
npx remotion render MyComp out/video.mp4 --jpeg-quality=90

# Renderizar com marcos de água (Pro)
npx remotion render MyComp out/video.mp4 --pro

# Renderizar em paralelo
npx remotion render MyComp out/video.mp4 --concurrency=4

# Benchmark para medir performance
npx remotion benchmark MyComp --frames=100 --concurrency=1
```

### 2. TEMPLATES REUTILIZÁVEIS

#### Template Avançado com Múltiplas Cenas
```tsx
import { Composition, Series, Sequence } from "remotion";
import { Spring, useSpring } from "remotion";

interface SceneConfig {
  duration: number;
  title: string;
  content: string;
}

interface TemplateProps {
  scenes: SceneConfig[];
  primaryColor: string;
  logo: string;
}

export const AdvancedTemplate: React.FC<TemplateProps> = ({
  scenes,
  primaryColor,
  logo,
}) => {
  return (
    <Series>
      {/* Intro */}
      <Series.Sequence durationInFrames={90}>
        <IntroScene logo={logo} color={primaryColor} />
      </Series.Sequence>
      
      {/* Cenas Dinâmicas */}
      {scenes.map((scene, index) => (
        <Series.Sequence 
          key={index}
          durationInFrames={scene.duration}
        >
          <DynamicScene 
            title={scene.title}
            content={scene.content}
            color={primaryColor}
          />
        </Series.Sequence>
      ))}
      
      {/* Outro */}
      <Series.Sequence durationInFrames={60}>
        <OutroScene logo={logo} color={primaryColor} />
      </Series.Sequence>
    </Series>
  );
};

// Animação com Spring
const AnimatedText: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const spring = useSpring({
    frame,
    fps: 30,
    config: { damping: 10, stiffness: 100 },
  });
  
  return (
    <div style={{
      transform: `scale(${spring})`,
      opacity: spring,
    }}>
      {text}
    </div>
  );
};
```

#### Passagem de Dados via Arquivo JSON
```bash
# Criar arquivo de dados
cat > videos-data.json << 'EOF'
[
  {
    "id": 1,
    "title": "Vídeo de Introdução",
    "scenes": [
      { "duration": 120, "title": "Bem-vindo", "content": "Conteúdo aqui" },
      { "duration": 180, "title": "Features", "content": "Mais conteúdo" }
    ]
  }
]
EOF

# Script de renderização
node render-videos.js
```

```javascript
// render-videos.js
import { bundle } from "@remotion/bundler";
import { renderMedia } from "@remotion/renderer";
import videosData from "./videos-data.json";

async function renderAllVideos() {
  const bundleLocation = await bundle({
    entryPoint: "./src/index.ts",
  });
  
  for (const video of videosData) {
    await renderMedia({
      composition: {
        id: "AdvancedTemplate",
        width: 1920,
        height: 1080,
        fps: 30,
        durationInFrames: video.scenes.reduce((acc, s) => acc + s.duration, 0) + 150,
      },
      serveUrl: bundleLocation,
      codec: "h264",
      outputLocation: `out/${video.id}.mp4`,
      inputProps: video,
    });
  }
}

renderAllVideos();
```

### 3. TRANSIÇÕES DETALHADAS

#### Todas as Transições com Exemplos
```tsx
import { TransitionSeries } from "@remotion/transitions";
import {
  fade, slide, wipe, flip, clockWipe, iris, cube
} from "@remotion/transitions/presets";
import { linearTiming, springTiming } from "@remotion/transitions/timings";

export const AllTransitionsDemo: React.FC = () => {
  return (
    <TransitionSeries>
      {/* Scene A */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneA />
      </TransitionSeries.Sequence>
      
      {/* Fade Transition */}
      <TransitionSeries.Transition
        durationInFrames={30}
        preset={fade()}
        timing={linearTiming({ durationInFrames: 30 })}
      />
      
      {/* Scene B */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneB />
      </TransitionSeries.Sequence>
      
      {/* Slide Transition */}
      <TransitionSeries.Transition
        durationInFrames={45}
        preset={slide({ 
          direction: "from-left", // from-left, from-right, from-top, from-bottom
        })}
        timing={springTiming({ 
          durationInFrames: 45,
          config: { stiffness: 100, damping: 10 },
        })}
      />
      
      {/* Scene C */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneC />
      </TransitionSeries.Sequence>
      
      {/* Wipe Transition */}
      <TransitionSeries.Transition
        durationInFrames={30}
        preset={wipe({ direction: "from-top" })}
      />
      
      {/* Scene D */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneD />
      </TransitionSeries.Sequence>
      
      {/* Clock Wipe Transition */}
      <TransitionSeries.Transition
        durationInFrames={60}
        preset={clockWipe()}
        timing={linearTiming({ 
          durationInFrames: 60,
          easing: (t) => t * t, // Ease in
        })}
      />
      
      {/* Scene E */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneE />
      </TransitionSeries.Sequence>
      
      {/* Iris Transition */}
      <TransitionSeries.Transition
        durationInFrames={45}
        preset={iris()}
      />
      
      {/* Scene F */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneF />
      </TransitionSeries.Sequence>
      
      {/* Flip Transition (PRO) */}
      <TransitionSeries.Transition
        durationInFrames={60}
        preset={flip({ direction: "horizontal" })}
      />
      
      {/* Scene G */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneG />
      </TransitionSeries.Sequence>
      
      {/* Cube Transition (PRO) */}
      <TransitionSeries.Transition
        durationInFrames={60}
        preset={cube()}
      />
      
      {/* Scene H */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SceneH />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

#### Timing Functions Customizadas
```tsx
import { TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/presets/fade";

// Easing functions
const easingFunctions = {
  linear: (t: number) => t,
  easeInQuad: (t: number) => t * t,
  easeOutQuad: (t: number) => t * (2 - t),
  easeInOutQuad: (t: number) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t),
  easeInCubic: (t: number) => t * t * t,
  easeOutC
