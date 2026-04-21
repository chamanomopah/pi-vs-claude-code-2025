# Exemplos de Código - Remotion

## 1. Renderização em Massa

### Loop Básico
```javascript
import { bundle } from "@remotion/bundler";
import { renderMedia } from "@remotion/renderer";

const videos = [
  { id: 1, title: "Video 1" },
  { id: 2, title: "Video 2" },
];

const bundleLocation = await bundle({ entryPoint: "./src/index.ts" });

for (const video of videos) {
  await renderMedia({
    composition: { id: "MyVideo", width: 1920, height: 1080, fps: 30, durationInFrames: 900 },
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: `out/${video.id}.mp4`,
    inputProps: video,
  });
}
```

### Paralelo
```javascript
const concurrency = 4;
for (let i = 0; i < videos.length; i += concurrency) {
  const chunk = videos.slice(i, i + concurrency);
  await Promise.all(chunk.map(video => renderMedia({ /* config */ })));
}
```

## 2. Template com Props

```tsx
import { Composition } from "remotion";

export const RemotionRoot = () => (
  <Composition
    id="Template"
    component={Template}
    durationInFrames={900}
    width={1920}
    height={1080}
    fps={30}
    defaultProps={{ title: "Default", color: "#3b82f6" }}
  />
);
```

## 3. Transições

```tsx
import { TransitionSeries } from "@remotion/transitions";
import { fade, slide } from "@remotion/transitions/presets";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition preset={fade()} />
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

## 4. Legendas

```tsx
import { Captions } from "@remotion/captions";
import { parseSrt } from "@remotion/captions/srt";

const transcription = parseSrt(srtContent);

<Captions 
  transcript={transcription}
  style={{ fontSize: 60, color: "white" }}
/>
```

## 5. Sequências com Timestamps

```tsx
import { Sequence } from "remotion";

<Sequence from={0} durationInFrames={90}>
  <ContentA />
</Sequence>
<Sequence from={90} durationInFrames={180}>
  <ContentB />
</Sequence>
```

## 6. ComfyUI Integration

```tsx
const seed = 12345 + frame;
const response = await fetch("http://localhost:8188/prompt", {
  method: "POST",
  body: JSON.stringify({ prompt: comfyWorkflow }),
});
```
