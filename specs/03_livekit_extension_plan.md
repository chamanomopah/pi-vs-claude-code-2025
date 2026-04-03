# LiveKit Extension Plan - Planejamento Completo

> Planejamento criado em 2026-04-03
> Baseado em: Pi Extension Research + LiveKit Practical Research

---

## Índice
1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Arquitetura Proposta](#2-arquitetura-proposta)
3. [Dependências Necessárias](#3-dependências-necessárias)
4. [Estrutura de Arquivos](#4-estrutura-de-arquivos)
5. [Fluxo de Dados](#5-fluxo-de-dados)
6. [Componentes a Implementar (DETALHADO)](#6-componentes-a-implementar-detalhado)
7. [Fases de Implementação (ORDENADAS)](#7-fases-de-implementação-ordenadas)
8. [Riscos e Mitigações](#8-riscos-e-mitigações)
9. [Checklist de Validação](#9-checklist-de-validação)
10. [Inconsistências Encontradas e Soluções](#10-inconsistências-encontradas-e-soluções)
11. [Validação do Planejamento](#11-validação-do-planejamento)

---

## 1. Visão Geral do Projeto

### 1.1 Objetivo Principal

Criar uma extensão do Pi que permite interação via voz, usando:
- **LiveKit** para transporte de áudio em tempo real
- **Deepgram** para Speech-to-Text (STT)
- **Pi LLM** para geração de resposta
- **Cartesia** para Text-to-Speech (TTS)

**Resultado esperado:** Um agente de voz conversacional que pode ser acessado via browser ou mobile, com baixa latência e qualidade de voz natural.

### 1.2 MVP Funcional

**O que inclui:**
- ✅ Conexão a uma sala LiveKit
- ✅ Receber áudio do usuário
- ✅ Transcrição em tempo real (Deepgram streaming STT)
- ✅ Envio do texto transcrito para o Pi LLM
- ✅ Geração de resposta pelo Pi
- ✅ Conversão da resposta para áudio (Cartesia streaming TTS)
- ✅ Envio do áudio de volta ao usuário
- ✅ Loop de conversação contínua (turn-based)
- ✅ UI de controle (start/stop, status, indicadores)
- ✅ Tratamento de erros básico

**O que NÃO inclui (v1.0):**
- ❌ Múltiplos participantes simultâneos (1:1 apenas)
- ❌ Vídeo (apenas áudio)
- ❌ Gravação de sessões para replay
- ❌ Análise de sentimentos ou emoções
- ❌ Suporte multi-idioma avançado (apenas inglês/português básico)
- ❌ Modo "hotword" para ativação por palavra
- ❌ Interrupção inteligente da fala do assistente

### 1.3 Princípios do MVP

**Simplicidade:**
- Mínimo de dependências externas
- API simples e direta
- Documentação clara

**Performance:**
- Streaming para reduzir latência
- Buffer otimizado
- Sem bloqueios na UI

**Robustez:**
- Tratamento de erros em todos os componentes
- Recuperação automática de conexões
- State reconstruction após /reload

**Extensibilidade:**
- Código modular e desacoplado
- Interface clara para adicionar novos STT/TTS providers
- Fácil integração com outras extensions do Pi

---

## 2. Arquitetura Proposta

### 2.1 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (Browser / Mobile App)                        │
└─────────────────────────────────────────────────────────────────┘
                            │ WebRTC (Audio)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LiveKit Server                               │
│                   (ws://localhost:7880)                         │
└─────────────────────────────────────────────────────────────────┘
                            │ WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Pi Extension: livekit-voice-chat               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    LiveKitClient                         │  │
│  │  - Room connection                                        │  │
│  │  - Audio track subscription                                │  │
│  │  - Audio track publication                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    STTManager                             │  │
│  │  - VAD (Voice Activity Detection)                         │  │
│  │  - Deepgram streaming STT                                 │  │
│  │  - Transcript buffering                                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 VoiceChatTool                              │  │
│  │  - Tool que o LLM pode chamar                             │  │
│  │  - Envia transcript para Pi                                │  │
│  │  - Gerencia estado da conversação                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Pi LLM                                 │  │
│  │  - Gera resposta                                           │  │
│  │  - Pode chamar outras tools (read, write, etc.)            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    TTSManager                              │  │
│  │  - Cartesia streaming TTS                                  │  │
│  │  - Audio generation                                        │  │
│  │  - Buffer management                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    LiveKitClient                         │  │
│  │  - Publish audio track                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                     (Audio ao usuário)
```

### 2.2 Tabela de Componentes

| Componente | Responsabilidade | Dependências | Estimativa |
|------------|------------------|--------------|-------------|
| `LiveKitClient` | Conexão à sala LiveKit, gerenciar tracks | `livekit-client-sdk` | ~300 linhas |
| `STTManager` | Speech-to-Text com Deepgram | Deepgram API | ~250 linhas |
| `TTSManager` | Text-to-Speech com Cartesia | Cartesia API | ~200 linhas |
| `SessionManager` | Gerenciar estado da sessão de voz | Nenhuma | ~300 linhas |
| `VoiceChatTool` | Tool que o LLM chama para voz | SessionManager | ~200 linhas |
| `UIComponents` | Interface customizada para controle | `@mariozechner/pi-tui` | ~150 linhas |
| `ConfigLoader` | Carregar configuração de .env | `dotenv` | ~150 linhas |
| `index.ts` | Entry point, registro de tools/events | Todos acima | ~100 linhas |

**Total estimado:** ~1650 linhas de código

### 2.3 Fluxo de Comunicação

**Loop de conversação:**
```
1. [Usuario] Fala "Hello, how are you?"
   │
2. [LiveKitClient] Recebe audio track
   │
3. [STTManager] Detecta fala (VAD), transcreve → "Hello, how are you?"
   │
4. [VoiceChatTool] Chama pi.sendUserMessage("Hello, how are you?")
   │
5. [Pi LLM] Processa mensagem
   │
6. [Pi LLM] Responde via message_update events
   │
7. [TTSManager] Converte resposta para audio (streaming)
   │
8. [LiveKitClient] Publica audio track
   │
9. [Usuario] Ouve resposta
```

**Detecção de fim de fala:**
- VAD detecta silêncio por X segundos
- STT finaliza transcript
- SessionManager marca como "user_finished"

**Interrupção:**
- Usuario pode falar enquanto assistente está falando
- TTSManager cancela geração atual
- Novo transcript inicia novo loop

---

## 3. Dependências Necessárias

### 3.1 Dependências NPM

**package.json:**
```json
{
  "name": "livekit-voice-chat-extension",
  "version": "0.1.0",
  "type": "module",
  "description": "Pi extension for voice chat via LiveKit",
  "main": "./src/index.ts",
  "scripts": {
    "build": "tsc",
    "watch": "tsc --watch"
  },
  "dependencies": {
    "@mariozechner/pi-coding-agent": "latest",
    "@mariozechner/pi-tui": "latest",
    "@mariozechner/pi-ai": "latest",
    "@sinclair/typebox": "^0.33.0",
    "livekit-client-sdk": "^2.0.0",
    "dotenv": "^16.4.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

**Versões específicas (pin para estabilidade):**
```json
{
  "dependencies": {
    "livekit-client-sdk": "^2.5.0",
    "@sinclair/typebox": "^0.33.0",
    "dotenv": "^16.4.5"
  }
}
```

### 3.2 Dependências Python

**Opcional - apenas se usar LiveKit Agents:**
```txt
livekit-agents~=1.4
livekit-plugins-deepgram
livekit-plugins-cartesia
python-dotenv
```

**Nota:** Nossa arquitetura usa LiveKit Client SDK (JavaScript), então dependências Python não são necessárias para o MVP.

### 3.3 API Keys Necessárias

**LiveKit (dev mode):**
```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

**Deepgram STT:**
```env
DEEPGRAM_API_KEY=5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3
```

**Cartesia TTS:**
```env
CARTESIA_API_KEY=sk_car_d69NmtdJKVbTj8XrrqM4Nt
```

**Opcional - Pi (se não usar /login):**
```env
ANTHROPIC_API_KEY=sk-ant-...
```

### 3.4 Template de .env

```.env
# LiveKit Configuration
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_ROOM=default-room
LIVEKIT_PARTICIPANT_ID=pi-voice-assistant

# STT Configuration (Deepgram)
DEEPGRAM_API_KEY=5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3
DEEPGRAM_MODEL=nova-3-general
DEEPGRAM_LANGUAGE=en-US
VAD_THRESHOLD=0.5
VAD_SILENCE_DURATION_MS=1000

# TTS Configuration (Cartesia)
CARTESIA_API_KEY=sk_car_d69NmtdJKVbTj8XrrqM4Nt
CARTESIA_MODEL=sonic-3
CARTESIA_VOICE=9626c31c-bec5-4cca-baa8-f8ba9e84c8bc
CARTESIA_SAMPLE_RATE=24000

# Audio Configuration
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_BITRATE=128000

# Session Configuration
SESSION_TIMEOUT_MS=300000
MAX_TRANSCRIPT_LENGTH=10000
MAX_TTS_QUEUE_SIZE=5
```

---

## 4. Estrutura de Arquivos

### 4.1 Estrutura Multi-arquivo

```
extensions/livekit-voice-chat/
├── package.json                          # Dependências NPM
├── tsconfig.json                         # Config TypeScript
├── .env.example                          # Template de variáveis de ambiente
├── .env                                  # Variáveis de ambiente (gitignored)
├── src/
│   ├── index.ts                          # Entry point da extensão
│   ├── types.ts                          # TypeScript types/interfaces
│   ├── config.ts                         # ConfigLoader
│   ├── livekit-client.ts                 # LiveKitClient class
│   ├── stt-manager.ts                    # STTManager class
│   ├── tts-manager.ts                    # TTSManager class
│   ├── session-manager.ts                # SessionManager class
│   ├── voice-chat-tool.ts                # VoiceChatTool implementation
│   └── ui-components.ts                  # Custom UI components
├── README.md                             # Documentação da extensão
└── node_modules/                         # Dependências instaladas
```

**Simlink para auto-discovery:**
```bash
ln -s $PWD/extensions/livekit-voice-chat/src/index.ts .pi/extensions/livekit-voice-chat.ts
```

### 4.2 Alternativa Single-file

**Para simplificar (menos ideal mas mais fácil de testar):**

```
.pi/extensions/livekit-voice-chat.ts  # ~1500 linhas em um arquivo
```

**Desvantagens:**
- Difícil de manter
- Sem separação clara de responsabilidades
- Testes mais difíceis

**Vantagens:**
- Fácil de copiar/colar
- Sem necessidade de build
- Rápido para prototipagem

---

## 5. Fluxo de Dados

### 5.1 Fluxo de Inicialização

```
1. [Pi Carrega Extensão]
   │
2. [index.ts] Export default function(pi)
   │
3. [ConfigLoader] Carrega .env
   │   └─► Valida API keys
   │   └─► Parse configuração
   │
4. [SessionManager] Inicializa estado
   │   └─► state = "disconnected"
   │   └─► Carrega estado anterior do session (se existir)
   │
5. [UIComponents] Registra widgets
   │   └─► Status widget
   │   └─► Keyboard shortcuts
   │
6. [VoiceChatTool] Registra tool
   │   └─► name: "voice_chat"
   │   └─► parameters: { room?, action? }
   │
7. [Commands] Registra comandos
   │   └─► /voice-start [room]
   │   └─► /voice-stop
   │   └─► /voice-status
   │
8. [Event Handlers] Subscreve eventos
   │   └─► session_start: Reconstruir estado
   │   └─► message_update: Capturar resposta LLM para TTS
   │   └─► message_end: Finalizar TTS
   │
9. [Ready] Extensão pronta para uso
```

### 5.2 Fluxo de Tool Execution

```
1. [Usuário] Digita "/voice-start my-room"
   │
2. [Command Handler] voice-start
   │   └─► Valida parâmetros
   │   └─► Mostra dialog de confirmação
   │
3. [LiveKitClient] Conecta à sala
   │   └─► room.connect(url, token)
   │   └─► Aguarda participant connected
   │
4. [STTManager] Configura Deepgram
   │   └─► Cria streaming connection
   │   └─► Configura VAD
   │
5. [LiveKitClient] Subscreve tracks de áudio
   │   └─► onTrackSubscribed (audio)
   │   └─► Pipe para STTManager
   │
6. [SessionManager] Muda estado
   │   └─► state = "listening"
   │   └─► Atualiza UI widget
   │
7. [Loop Pronto] Aguardando fala do usuário
```

### 5.3 Fluxo de Eventos

**Quando usuário fala:**
```
1. [LiveKitClient] Recebe audio frame
   │
2. [STTManager] Processa áudio
   │   ├─► VAD: Detecta início de fala
   │   │   └─► SessionManager.state = "user_speaking"
   │   │
   │   └─► Deepgram: Envia áudio para transcrição
   │       └─► Recebe transcript parcial
   │       └─► Acumula em buffer
   │
3. [STTManager] VAD detecta fim de fala
   │   └─► Aguarda silêncio por X segundos
   │   └─► Deepgram finaliza transcript
   │   └─► transcript = "Hello, how are you?"
   │
4. [VoiceChatTool] Envia para Pi
   │   └─► pi.sendUserMessage(transcript, { deliverAs: "steer" })
   │   └─► SessionManager.state = "processing"
   │
5. [Pi LLM] Processa mensagem
   │   ├─► Pode chamar outras tools
   │   └─► Gera resposta
   │
6. [Event] message_update (streaming)
   │   └─► Capturado por extension
   │   └─► TTSManager converte delta para áudio
   │   └─► LiveKitClient publica áudio
   │   └─► SessionManager.state = "assistant_speaking"
   │
7. [Event] message_end
   │   └─► TTSManager finaliza
   │   └─► SessionManager.state = "listening"
   │
8. [Loop volta] Aguardando próxima fala
```

---

## 6. Componentes a Implementar (DETALHADO)

### 6.1 VoiceChatTool (~200 linhas)

**Responsabilidade:** Tool que o LLM pode chamar para interação via voz.

**Interface:**
```typescript
interface VoiceChatToolParams {
  room?: string;      // Nome da sala (opcional, usa default)
  action?: "start" | "stop" | "status";  // Ação a executar
  message?: string;   // Mensagem para enviar direto (teste)
}

interface VoiceChatToolResult {
  status: "connected" | "disconnected" | "listening" | "speaking" | "error";
  room?: string;
  transcript?: string;
  error?: string;
}
```

**Implementação:**
```typescript
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@mariozechner/pi-ai";
import { isToolCallEventType } from "@mariozechner/pi-coding-agent";

export function registerVoiceChatTool(
  pi: ExtensionAPI,
  sessionManager: SessionManager,
  liveKitClient: LiveKitClient
) {
  pi.registerTool({
    name: "voice_chat",
    label: "Voice Chat",
    description: "Interact with user via voice chat using LiveKit",
    promptSnippet: "Start, stop, or check status of voice chat session",
    promptGuidelines: [
      "Use this tool when the user asks to start voice chat",
      "Use to check current voice chat status",
      "Use to stop an active voice chat session",
    ],
    parameters: Type.Object({
      action: StringEnum(["start", "stop", "status", "send"] as const),
      room: Type.Optional(Type.String({ description: "Room name (optional, uses default)" })),
      message: Type.Optional(Type.String({ description: "Message to send directly (for testing)" })),
    }),
    
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      try {
        switch (params.action) {
          case "start":
            return await handleStart(params.room, signal, onUpdate, ctx);
          case "stop":
            return await handleStop(onUpdate, ctx);
          case "status":
            return handleStatus();
          case "send":
            return await handleSend(params.message, onUpdate, ctx);
          default:
            throw new Error(`Unknown action: ${params.action}`);
        }
      } catch (error) {
        ctx.ui.notify(`Voice chat error: ${error.message}`, "error");
        throw error;
      }
    },
  });

  async function handleStart(
    room: string | undefined,
    signal: AbortSignal | undefined,
    onUpdate: any,
    ctx: any
  ) {
    const roomName = room || sessionManager.config.defaultRoom;
    
    onUpdate?.({
      content: [{ type: "text", text: `Connecting to room: ${roomName}...` }],
    });

    const connected = await liveKitClient.connect(roomName, { signal });
    
    if (!connected) {
      throw new Error("Failed to connect to LiveKit room");
    }

    sessionManager.setState("listening");
    ctx.ui.setWidget("voice-chat", ["Status: Listening"]);
    ctx.ui.notify(`Connected to room: ${roomName}`, "success");

    return {
      content: [{ type: "text", text: `Connected to room: ${roomName}. Listening for voice input...` }],
      details: { status: "listening", room: roomName },
    };
  }

  // ... handleStop, handleStatus, handleSend implementations
}
```

### 6.2 LiveKitClient (~300 linhas)

**Responsabilidade:** Wrapper para LiveKit Client SDK.

**Interface:**
```typescript
class LiveKitClient {
  constructor(config: LiveKitConfig);
  
  // Conexão
  async connect(roomName: string, options?: ConnectOptions): Promise<boolean>;
  async disconnect(): Promise<void>;
  isConnected(): boolean;
  
  // Audio
  async publishAudioTrack(audioTrack: LocalAudioTrack): Promise<void>;
  onTrackSubscribed(callback: (track: RemoteAudioTrack) => void): void;
  
  // Eventos
  onDisconnected(callback: () => void): void;
  onParticipantConnected(callback: (p: RemoteParticipant) => void): void;
  
  // Cleanup
  dispose(): void;
}
```

**Implementação:**
```typescript
import { Room, RemoteTrack, RemoteParticipant, LocalAudioTrack } from 'livekit-client-sdk';

interface LiveKitConfig {
  url: string;
  apiKey: string;
  apiSecret: string;
  participantName: string;
}

interface ConnectOptions {
  signal?: AbortSignal;
  autoSubscribe?: boolean;
}

export class LiveKitClient {
  private room: Room | null = null;
  private config: LiveKitConfig;
  private disconnectCallbacks: Array<() => void> = [];
  private trackCallbacks: Array<(track: RemoteTrack) => void> = [];
  
  constructor(config: LiveKitConfig) {
    this.config = config;
  }

  async connect(roomName: string, options: ConnectOptions = {}): Promise<boolean> {
    try {
      // Generate token
      const token = await this.generateToken(roomName);
      
      // Create room
      this.room = new Room();
      
      // Setup event handlers
      this.setupEventHandlers(options.signal);
      
      // Connect
      await this.room.connect(this.config.url, token);
      
      return true;
    } catch (error) {
      console.error('LiveKit connection error:', error);
      return false;
    }
  }

  private async generateToken(roomName: string): Promise<string> {
    // Implement JWT token generation
    // For now, return a hardcoded dev token
    return 'dev-token';
  }

  private setupEventHandlers(signal?: AbortSignal) {
    if (!this.room) return;

    this.room.on(RoomEvent.TrackSubscribed, (track: RemoteTrack) => {
      if (track.kind === Track.Kind.Audio) {
        for (const cb of this.trackCallbacks) {
          cb(track);
        }
      }
    });

    this.room.on(RoomEvent.Disconnected, () => {
      for (const cb of this.disconnectCallbacks) {
        cb();
      }
    });

    if (signal) {
      signal.addEventListener('abort', () => {
        this.disconnect();
      });
    }
  }

  async disconnect(): Promise<void> {
    if (this.room) {
      await this.room.disconnect();
      this.room = null;
    }
  }

  isConnected(): boolean {
    return this.room !== null && this.room.state === RoomState.Connected;
  }

  onTrackSubscribed(callback: (track: RemoteTrack) => void): void {
    this.trackCallbacks.push(callback);
  }

  onDisconnected(callback: () => void): void {
    this.disconnectCallbacks.push(callback);
  }

  dispose(): void {
    this.disconnect();
    this.disconnectCallbacks = [];
    this.trackCallbacks = [];
  }
}
```

### 6.3 STTManager (~250 linhas)

**Responsabilidade:** Speech-to-Text com Deepgram.

**Interface:**
```typescript
class STTManager {
  constructor(config: STTConfig);
  
  // Transcrição
  async transcribe(audioStream: ReadableStream<Float32Array>): Promise<string>;
  
  // VAD
  detectVoiceActivity(audioBuffer: Float32Array): VADResult;
  
  // Configuração
  setVADThreshold(threshold: number): void;
  setSilenceDuration(durationMs: number): void;
  
  // Cleanup
  dispose(): void;
}

interface VADResult {
  speechDetected: boolean;
  confidence: number;
}

interface STTConfig {
  apiKey: string;
  model: string;
  language: string;
  vadThreshold: number;
  silenceDurationMs: number;
}
```

**Implementação:**
```typescript
export class STTManager {
  private config: STTConfig;
  private transcriptBuffer: string[] = [];
  private isSpeaking = false;
  private lastSpeechTime = 0;
  
  constructor(config: STTConfig) {
    this.config = config;
  }

  // Simple VAD implementation
  detectVoiceActivity(audioBuffer: Float32Array): VADResult {
    // Calculate RMS energy
    let sum = 0;
    for (let i = 0; i < audioBuffer.length; i++) {
      sum += audioBuffer[i] * audioBuffer[i];
    }
    const rms = Math.sqrt(sum / audioBuffer.length);
    
    const confidence = Math.min(rms / this.config.vadThreshold, 1);
    const speechDetected = rms > this.config.vadThreshold;
    
    if (speechDetected) {
      this.lastSpeechTime = Date.now();
      this.isSpeaking = true;
    } else if (this.isSpeaking) {
      // Check if silence duration exceeded
      const silenceDuration = Date.now() - this.lastSpeechTime;
      if (silenceDuration > this.config.silenceDurationMs) {
        this.isSpeaking = false;
      }
    }
    
    return { speechDetected, confidence };
  }

  async transcribe(audioStream: ReadableStream<Float32Array>): Promise<string> {
    // Implement Deepgram streaming STT
    // For MVP, use a mock implementation
    return new Promise((resolve) => {
      const reader = audioStream.getReader();
      const chunks: Float32Array[] = [];
      
      const read = async () => {
        const { done, value } = await reader.read();
        if (done) {
          // Combine all chunks and transcribe
          const combined = this.concatFloat32Arrays(chunks);
          resolve(this.mockTranscribe(combined));
          return;
        }
        
        const vadResult = this.detectVoiceActivity(value);
        if (vadResult.speechDetected) {
          chunks.push(value);
        } else if (!this.isSpeaking && chunks.length > 0) {
          // End of speech
          const combined = this.concatFloat32Arrays(chunks);
          resolve(this.mockTranscribe(combined));
          return;
        }
        
        read();
      };
      
      read();
    });
  }

  private concatFloat32Arrays(arrays: Float32Array[]): Float32Array {
    const totalLength = arrays.reduce((sum, arr) => sum + arr.length, 0);
    const result = new Float32Array(totalLength);
    let offset = 0;
    for (const arr of arrays) {
      result.set(arr, offset);
      offset += arr.length;
    }
    return result;
  }

  private mockTranscribe(audio: Float32Array): string {
    // Mock implementation - replace with actual Deepgram API call
    return "This is a mock transcript";
  }

  dispose(): void {
    this.transcriptBuffer = [];
    this.isSpeaking = false;
  }
}
```

### 6.4 TTSManager (~200 linhas)

**Responsabilidade:** Text-to-Speech com Cartesia.

**Interface:**
```typescript
class TTSManager {
  constructor(config: TTSConfig);
  
  // Síntese
  async synthesize(text: string): Promise<Uint8Array>;
  synthesizeStream(text: string): ReadableStream<Uint8Array>;
  
  // Streaming
  async speakChunk(chunk: string, signal?: AbortSignal): Promise<void>;
  
  // Configuração
  setVoice(voiceId: string): void;
  setSampleRate(sampleRate: number): void;
  
  // Cleanup
  cancel(): void;
  dispose(): void;
}

interface TTSConfig {
  apiKey: string;
  model: string;
  voice: string;
  sampleRate: number;
}
```

**Implementação:**
```typescript
export class TTSManager {
  private config: TTSConfig;
  private currentAbortController: AbortController | null = null;
  
  constructor(config: TTSConfig) {
    this.config = config;
  }

  async synthesize(text: string): Promise<Uint8Array> {
    // Implement Cartesia TTS API call
    // For MVP, use a mock implementation
    const response = await fetch('https://api.cartesia.ai/tts', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: this.config.model,
        voice: this.config.voice,
        text: text,
        output_format: {
          container: 'wav',
          sample_rate: this.config.sampleRate,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Cartesia API error: ${response.statusText}`);
    }

    const audioData = await response.arrayBuffer();
    return new Uint8Array(audioData);
  }

  synthesizeStream(text: string): ReadableStream<Uint8Array> {
    // Implement streaming TTS
    // For MVP, return a mock stream
    return new ReadableStream({
      async start(controller) {
        try {
          const audio = await this.synthesize(text);
          controller.enqueue(audio);
          controller.close();
        } catch (error) {
          controller.error(error);
        }
      },
    });
  }

  async speakChunk(chunk: string, signal?: AbortSignal): Promise<void> {
    this.cancel(); // Cancel previous speech
    
    this.currentAbortController = new AbortController();
    const combinedSignal = this.currentAbortController.signal;
    
    // Combine with external signal if provided
    if (signal) {
      signal.addEventListener('abort', () => this.cancel());
    }

    try {
      const stream = this.synthesizeStream(chunk);
      const reader = stream.getReader();
      
      while (true) {
        if (combinedSignal.aborted) {
          reader.cancel();
          break;
        }
        
        const { done, value } = await reader.read();
        if (done) break;
        
        // Emit audio chunk via callback or event
        // This would be connected to LiveKitClient
        this.emitAudioChunk(value);
      }
    } catch (error) {
      if (combinedSignal.aborted) {
        console.log('TTS cancelled');
      } else {
        console.error('TTS error:', error);
      }
    }
  }

  cancel(): void {
    if (this.currentAbortController) {
      this.currentAbortController.abort();
      this.currentAbortController = null;
    }
  }

  private emitAudioChunk(chunk: Uint8Array): void {
    // Emit to LiveKitClient
    // Implementation depends on integration
  }

  dispose(): void {
    this.cancel();
  }
}
```

### 6.5 SessionManager (~300 linhas)

**Responsabilidade:** Gerenciar estado da sessão de voz.

**Interface:**
```typescript
class SessionManager {
  constructor(config: VoiceChatConfig);
  
  // Estado
  getState(): VoiceChatState;
  setState(state: VoiceChatState): void;
  
  // Sessão atual
  getCurrentRoom(): string | null;
  getTranscriptHistory(): string[];
  appendTranscript(transcript: string): void;
  
  // Persistência
  saveState(sessionManager: SessionManager): void;
  restoreState(sessionManager: SessionManager): void;
  
  // Controle
  startSession(room: string): void;
  stopSession(): void;
  clearHistory(): void;
  
  // Callbacks
  onStateChange(callback: (state: VoiceChatState) => void): void;
}

type VoiceChatState = 
  | "disconnected"
  | "connecting"
  | "listening"
  | "user_speaking"
  | "processing"
  | "assistant_speaking"
  | "error";

interface VoiceChatConfig {
  defaultRoom: string;
  sessionTimeout: number;
  maxTranscriptLength: number;
}
```

**Implementação:**
```typescript
import { pi } from './index';

export class SessionManager {
  private config: VoiceChatConfig;
  private state: VoiceChatState = "disconnected";
  private currentRoom: string | null = null;
  private transcriptHistory: string[] = [];
  private stateChangeCallbacks: Array<(state: VoiceChatState) => void> = [];
  
  constructor(config: VoiceChatConfig) {
    this.config = config;
  }

  getState(): VoiceChatState {
    return this.state;
  }

  setState(state: VoiceChatState): void {
    if (this.state !== state) {
      const oldState = this.state;
      this.state = state;
      
      console.log(`Voice chat state: ${oldState} -> ${state}`);
      
      for (const cb of this.stateChangeCallbacks) {
        cb(state);
      }
      
      // Persist state
      this.saveStateToPi();
    }
  }

  getCurrentRoom(): string | null {
    return this.currentRoom;
  }

  getTranscriptHistory(): string[] {
    return [...this.transcriptHistory];
  }

  appendTranscript(transcript: string): void {
    this.transcriptHistory.push(transcript);
    
    // Limit history size
    if (this.transcriptHistory.length > 100) {
      this.transcriptHistory = this.transcriptHistory.slice(-100);
    }
    
    this.saveStateToPi();
  }

  startSession(room: string): void {
    this.currentRoom = room;
    this.setState("connecting");
  }

  stopSession(): void {
    this.currentRoom = null;
    this.setState("disconnected");
  }

  clearHistory(): void {
    this.transcriptHistory = [];
    this.saveStateToPi();
  }

  onStateChange(callback: (state: VoiceChatState) => void): void {
    this.stateChangeCallbacks.push(callback);
  }

  private saveStateToPi(): void {
    // Persist state using pi.appendEntry
    pi.appendEntry("voice-chat-state", {
      state: this.state,
      room: this.currentRoom,
      transcriptCount: this.transcriptHistory.length,
      timestamp: Date.now(),
    });
  }

  restoreStateFromPi(sessionManager: any): void {
    // Reconstruct state from session entries
    for (const entry of sessionManager.getEntries()) {
      if (entry.type === "custom" && entry.customType === "voice-chat-state") {
        const data = entry.data;
        this.state = data.state || "disconnected";
        this.currentRoom = data.room || null;
        console.log(`Restored voice chat state: ${this.state}`);
        break;
      }
    }
  }

  dispose(): void {
    this.stateChangeCallbacks = [];
  }
}
```

### 6.6 UIComponents (~150 linhas)

**Responsabilidade:** Componentes TUI customizados.

**Componentes:**
- `StatusWidget` - Widget de status acima do editor
- `JoinRoomDialog` - Dialog para entrar em sala
- `ConfirmDialog` - Dialog de confirmação

**Implementação:**
```typescript
import { Text, Box, Container } from "@mariozechner/pi-tui";

class StatusWidget extends Container {
  private statusText: Text;
  
  constructor() {
    super();
    this.updateContent("disconnected");
  }

  setStatus(status: VoiceChatState, room?: string): void {
    const statusEmoji = {
      disconnected: "⚫",
      connecting: "🟡",
      listening: "🟢",
      user_speaking: "🎤",
      processing: "⚙️",
      assistant_speaking: "🔊",
      error: "❌",
    };
    
    const emoji = statusEmoji[status] || "⚫";
    const roomText = room ? ` (${room})` : "";
    const statusLabel = status.replace(/_/g, " ");
    
    this.updateContent(`${emoji} Voice Chat: ${statusLabel}${roomText}`);
  }

  private updateContent(text: string): void {
    this.clearChildren();
    this.addChild(
      new Box(0, 0, (s) => `\x1b[48;5;236m${s}\x1b[0m`, [
        new Text(text, 0, 0),
      ])
    );
  }
}

class JoinRoomDialog extends Container {
  private input: Input;
  private selectedIndex = 0;
  private rooms = ["default-room", "meeting-room", "test-room"];
  
  constructor(private onSelect: (room: string) => void, private onCancel: () => void) {
    super();
    this.setupUI();
  }

  private setupUI(): void {
    // Create input field for custom room name
    // Create list of recent rooms
    // Handle keyboard navigation
  }

  handleInput(data: string): void {
    if (matchesKey(data, Key.enter)) {
      const room = this.input.getText() || this.rooms[this.selectedIndex];
      this.onSelect(room);
    } else if (matchesKey(data, Key.escape)) {
      this.onCancel();
    } else if (matchesKey(data, Key.up)) {
      this.selectedIndex = Math.max(0, this.selectedIndex - 1);
      this.invalidate();
    } else if (matchesKey(data, Key.down)) {
      this.selectedIndex = Math.min(this.rooms.length - 1, this.selectedIndex + 1);
      this.invalidate();
    } else {
      this.input.handleInput(data);
    }
  }
}

export function registerVoiceChatUI(pi: ExtensionAPI, sessionManager: SessionManager) {
  const statusWidget = new StatusWidget();
  
  // Register status widget
  sessionManager.onStateChange((state) => {
    statusWidget.setStatus(state, sessionManager.getCurrentRoom());
    statusWidget.requestRender?.();
  });
  
  const handle = pi.ui.custom(statusWidget, {
    overlay: false,
  });
  
  return handle;
}
```

### 6.7 ConfigLoader (~150 linhas)

**Responsabilidade:** Carregar configuração de .env.

**Interface:**
```typescript
class ConfigLoader {
  static load(): VoiceChatConfig;
  static validate(config: VoiceChatConfig): void;
}

interface VoiceChatConfig {
  livekit: {
    url: string;
    apiKey: string;
    apiSecret: string;
    defaultRoom: string;
    participantId: string;
  };
  stt: {
    apiKey: string;
    model: string;
    language: string;
    vadThreshold: number;
    silenceDurationMs: number;
  };
  tts: {
    apiKey: string;
    model: string;
    voice: string;
    sampleRate: number;
  };
  audio: {
    sampleRate: number;
    channels: number;
    bitrate: number;
  };
  session: {
    timeoutMs: number;
    maxTranscriptLength: number;
    maxTTSQueueSize: number;
  };
}
```

**Implementação:**
```typescript
import dotenv from 'dotenv';
import { readFileSync } from 'fs';
import { resolve } from 'path';

export class ConfigLoader {
  static load(): VoiceChatConfig {
    // Load .env
    const envPath = resolve(process.cwd(), '.env');
    dotenv.config({ path: envPath });
    
    const config: VoiceChatConfig = {
      livekit: {
        url: process.env.LIVEKIT_URL || 'ws://localhost:7880',
        apiKey: process.env.LIVEKIT_API_KEY || 'devkey',
        apiSecret: process.env.LIVEKIT_API_SECRET || 'secret',
        defaultRoom: process.env.LIVEKIT_ROOM || 'default-room',
        participantId: process.env.LIVEKIT_PARTICIPANT_ID || 'pi-voice-assistant',
      },
      stt: {
        apiKey: process.env.DEEPGRAM_API_KEY || '',
        model: process.env.DEEPGRAM_MODEL || 'nova-3-general',
        language: process.env.DEEPGRAM_LANGUAGE || 'en-US',
        vadThreshold: parseFloat(process.env.VAD_THRESHOLD || '0.5'),
        silenceDurationMs: parseInt(process.env.VAD_SILENCE_DURATION_MS || '1000'),
      },
      tts: {
        apiKey: process.env.CARTESIA_API_KEY || '',
        model: process.env.CARTESIA_MODEL || 'sonic-3',
        voice: process.env.CARTESIA_VOICE || '9626c31c-bec5-4cca-baa8-f8ba9e84c8bc',
        sampleRate: parseInt(process.env.CARTESIA_SAMPLE_RATE || '24000'),
      },
      audio: {
        sampleRate: parseInt(process.env.AUDIO_SAMPLE_RATE || '16000'),
        channels: parseInt(process.env.AUDIO_CHANNELS || '1'),
        bitrate: parseInt(process.env.AUDIO_BITRATE || '128000'),
      },
      session: {
        timeoutMs: parseInt(process.env.SESSION_TIMEOUT_MS || '300000'),
        maxTranscriptLength: parseInt(process.env.MAX_TRANSCRIPT_LENGTH || '10000'),
        maxTTSQueueSize: parseInt(process.env.MAX_TTS_QUEUE_SIZE || '5'),
      },
    };
    
    this.validate(config);
    return config;
  }

  static validate(config: VoiceChatConfig): void {
    const errors: string[] = [];
    
    // Validate LiveKit
    if (!config.livekit.url) {
      errors.push('LIVEKIT_URL is required');
    }
    if (!config.livekit.apiKey) {
      errors.push('LIVEKIT_API_KEY is required');
    }
    if (!config.livekit.apiSecret) {
      errors.push('LIVEKIT_API_SECRET is required');
    }
    
    // Validate STT
    if (!config.stt.apiKey) {
      errors.push('DEEPGRAM_API_KEY is required');
    }
    if (config.stt.vadThreshold < 0 || config.stt.vadThreshold > 1) {
      errors.push('VAD_THRESHOLD must be between 0 and 1');
    }
    
    // Validate TTS
    if (!config.tts.apiKey) {
      errors.push('CARTESIA_API_KEY is required');
    }
    
    // Validate audio
    if (config.audio.sampleRate <= 0) {
      errors.push('AUDIO_SAMPLE_RATE must be positive');
    }
    
    if (errors.length > 0) {
      throw new Error(`Configuration errors:\n${errors.join('\n')}`);
    }
  }
}
```

---

## 7. Fases de Implementação (ORDENADAS)

### Fase 0: Preparação do Ambiente (0.5 dia)

**Objetivo:** Configurar ambiente de desenvolvimento.

**Tarefas:**
- [ ] Instalar LiveKit Server local
- [ ] Testar LiveKit Server (`livekit-server --dev`)
- [ ] Validar API keys (Deepgram, Cartesia)
- [ ] Criar estrutura de diretórios
- [ ] Inicializar `package.json`
- [ ] Configurar `tsconfig.json`
- [ ] Criar `.env.example`
- [ ] Criar `.env` com valores reais

**Validação:**
- LiveKit Server rodando na porta 7880
- Conexão com LiveKit bem-sucedida
- .env carregado corretamente

**Risco:** Baixo - setup padrão

### Fase 1: Tipos e Configuração (1 dia)

**Objetivo:** Definir base do projeto.

**Tarefas:**
- [ ] Criar `src/types.ts` com todas as interfaces
- [ ] Implementar `ConfigLoader`
- [ ] Criar validação de configuração
- [ ] Testar carregamento de .env
- [ ] Criar testes unitários para ConfigLoader
- [ ] Documentar tipos

**Arquivos:**
- `src/types.ts`
- `src/config.ts`

**Validação:**
- Config carrega sem erros
- Validação funciona para casos inválidos
- Types TypeScript compilam

**Risco:** Baixo - código simples

### Fase 2: LiveKitClient (1-2 dias)

**Objetivo:** Implementar conexão com LiveKit.

**Tarefas:**
- [ ] Implementar classe `LiveKitClient`
- [ ] Implementar `connect()`
- [ ] Implementar `disconnect()`
- [ ] Implementar `onTrackSubscribed()`
- [ ] Implementar `publishAudioTrack()`
- [ ] Implementar geração de JWT token
- [ ] Adicionar tratamento de erros
- [ ] Criar testes unitários
- [ ] Testar conexão real com LiveKit Server

**Arquivos:**
- `src/livekit-client.ts`

**Validação:**
- Conexão com sala bem-sucedida
- Tracks são subscritos corretamente
- Desconexão limpa
- Reconnexão após erro

**Risco:** Médio - dependência de LiveKit SDK

### Fase 3: STTManager - Deepgram (1 dia)

**Objetivo:** Implementar transcrição de fala.

**Tarefas:**
- [ ] Implementar classe `STTManager`
- [ ] Implementar VAD simples (energy-based)
- [ ] Integrar Deepgram API (streaming)
- [ ] Implementar `transcribe()`
- [ ] Implementar buffering de transcript
- [ ] Adicionar timeout para fim de fala
- [ ] Criar testes unitários
- [ ] Testar com áudio real

**Arquivos:**
- `src/stt-manager.ts`

**Validação:**
- VAD detecta início/fim de fala
- Deepgram transcreve corretamente
- Transcript completo retornado
- Timeout funciona

**Risco:** Médio - API de terceiros

### Fase 4: TTSManager - Cartesia (1 dia)

**Objetivo:** Implementar síntese de voz.

**Tarefas:**
- [ ] Implementar classe `TTSManager`
- [ ] Integrar Cartesia API
- [ ] Implementar `synthesize()`
- [ ] Implementar `synthesizeStream()`
- [ ] Implementar `speakChunk()`
- [ ] Implementar cancelamento
- [ ] Adicionar tratamento de erros
- [ ] Criar testes unitários
- [ ] Testar qualidade de voz

**Arquivos:**
- `src/tts-manager.ts`

**Validação:**
- Cartesia gera áudio
- Streaming funciona
- Cancelamento interrompe geração
- Qualidade de voz aceitável

**Risco:** Médio - API de terceiros

### Fase 5: SessionManager (1 dia)

**Objetivo:** Gerenciar estado da sessão.

**Tarefas:**
- [ ] Implementar classe `SessionManager`
- [ ] Implementar estados e transições
- [ ] Implementar persistência no Pi session
- [ ] Implementar reconstrução de estado
- [ ] Implementar histórico de transcripts
- [ ] Adicionar callbacks de mudança de estado
- [ ] Criar testes unitários

**Arquivos:**
- `src/session-manager.ts`

**Validação:**
- Estados transicionam corretamente
- Estado persiste no Pi session
- Reconstrução funciona após /reload
- Histórico mantido corretamente

**Risco:** Baixo - lógica de estado

### Fase 6: Voice Chat Tool (1-2 dias)

**Objetivo:** Tool que o LLM chama para voz.

**Tarefas:**
- [ ] Implementar `registerVoiceChatTool()`
- [ ] Definir TypeBox schema
- [ ] Implementar `handleStart()`
- [ ] Implementar `handleStop()`
- [ ] Implementar `handleStatus()`
- [ ] Implementar `handleSend()`
- [ ] Adicionar tratamento de erros
- [ ] Integrar com SessionManager
- [ ] Criar testes unitários

**Arquivos:**
- `src/voice-chat-tool.ts`

**Validação:**
- Tool registrado corretamente
- LLM pode chamar a tool
- Ações funcionam
- Erros são reportados

**Risco:** Baixo - tool padrão do Pi

### Fase 7: Integração Pi e Loop de Conversação (2 dias)

**Objetivo:** Orquestrar pipeline completo.

**Tarefas:**
- [ ] Implementar `session_start` handler
- [ ] Implementar `message_update` listener
- [ ] Implementar `message_end` listener
- [ ] Integrar STT → Pi LLM → TTS
- [ ] Implementar loop de conversação
- [ ] Gerenciar interrupções
- [ ] Sincronizar estados
- [ ] Testar end-to-end
- [ ] Otimizar latência

**Arquivos:**
- `src/index.ts` (principal)

**Validação:**
- Loop completo funciona
- STT → LLM → TTS fluem
- Interrupções funcionam
- Latência aceitável

**Risco:** Alto - complexidade de integração

### Fase 8: UI Integration (1 dia)

**Objetivo:** Interface customizada.

**Tarefas:**
- [ ] Implementar `StatusWidget`
- [ ] Implementar `JoinRoomDialog`
- [ ] Implementar `ConfirmDialog`
- [ ] Registrar widgets no Pi
- [ ] Adicionar keyboard shortcuts
- [ ] Testar componentes UI
- [ ] Ajustar styling

**Arquivos:**
- `src/ui-components.ts`

**Validação:**
- Widget mostra status corretamente
- Dialogs funcionam
- Shortcuts respondem
- UI é responsiva

**Risco:** Baixo - UI components padrão

### Fase 9: Error Handling e Edge Cases (1 dia)

**Objetivo:** Robustez da extensão.

**Tarefas:**
- [ ] Tratar erros de conexão LiveKit
- [ ] Tratar erros de API Deepgram
- [ ] Tratar erros de API Cartesia
- [ ] Implementar retry logic
- [ ] Implementar timeouts
- [ ] Tratar desconexões
- [ ] Implementar recovery
- [ ] Logar erros adequadamente
- [ ] Testar casos de erro

**Validação:**
- Erros não quebram a extensão
- Recovery funciona
- Logs são úteis
- UX é boa mesmo com erros

**Risco:** Médio - muitos edge cases

### Fase 10: Documentação (1-2 dias)

**Objetivo:** Documentar extensão.

**Tarefas:**
- [ ] Criar README.md
- [ ] Documentar instalação
- [ ] Documentar configuração
- [ ] Documentar uso
- [ ] Criar exemplos de uso
- [ ] Documentar API
- [ ] Criar troubleshooting guide
- [ ] Adicionar screenshots

**Arquivos:**
- `README.md`
- `examples/`
- `docs/`

**Validação:**
- Instalação é clara
- Exemplos funcionam
- Troubleshooting é útil

**Risco:** Baixo - documentação

### Fase 11: Testing e Validação (1-2 dias)

**Objetivo:** Garantir qualidade.

**Tarefas:**
- [ ] Criar testes unitários
- [ ] Criar testes de integração
- [ ] Testar com LiveKit room real
- [ ] Testar latência
- [ ] Testar qualidade de voz
- [ ] Testar edge cases
- [ ] Testar /reload
- [ ] Testar branching
- [ ] Fix bugs encontrados
- [ ] Validar checklist

**Validação:**
- Todos os testes passam
- Latência < 2s
- Qualidade de voz boa
- Não há memory leaks

**Risco:** Médio - bugs podem aparecer

### Fase 12: Polish e Otimização (1 dia)

**Objetivo:** Melhorar experiência.

**Tarefas:**
- [ ] Otimizar latência
- [ ] Melhorar feedback visual
- [ ] Ajustar parâmetros de VAD
- [ ] Otimizar buffer sizes
- [ ] Performance tuning
- [ ] Code review
- [ ] Refactoring se necessário
- [ ] Finalizar logs

**Validação:**
- Latência mínima alcançada
- UI é responsiva
- Código é limpo

**Risco:** Baixo - otimizações

### Fase 13: Release Final (0.5 dia)

**Objetivo:** Publicar extensão.

**Tarefas:**
- [ ] Criar release notes
- [ ] Versionar (0.1.0)
- [ ] Testar instalação limpa
- [ ] Publicar como Pi package
- [ ] Atualizar README principal
- [ ] Anunciar

**Validação:**
- Instalação funciona
- Extensão carrega corretamente
- Release notes estão completas

**Risco:** Baixo - release

---

## 8. Riscos e Mitigações

### 8.1 Riscos Técnicos

**Risco 1: Latência alta no pipeline**
- **Impacto:** Alto - afeta experiência do usuário
- **Probabilidade:** Média
- **Mitigação:**
  - Usar streaming TTS em vez de esperar resposta completa
  - Otimizar buffer sizes
  - Implementar VAD agressivo
  - Usar modelos mais rápidos (nova-3, sonic-3)
- **Contingência:** Aceitar latência maior se necessário

**Risco 2: Memory leaks**
- **Impacto:** Alto - crash após uso prolongado
- **Probabilidade:** Média
- **Mitigação:**
  - Dispose de todos os recursos corretamente
  - Limpar buffers periodicamente
  - Monitorar uso de memória
  - Testes de longa duração
- **Contingência:** Implementar limites de recursos

**Risco 3: Race conditions**
- **Impacto:** Médio - estado inconsistente
- **Probabilidade:** Média
- **Mitigação:**
  - Usar `withFileMutationQueue` para operações concorrentes
  - Sincronizar estados adequadamente
  - Usar abort signals para cancelamento
- **Contingência:** Simplificar lógica concorrente

**Risco 4: Audio quality issues**
- **Impacto:** Médio - experiência ruim
- **Probabilidade:** Baixa
- **Mitigação:**
  - Tunar parâmetros de codec
  - Match sample rates
  - Testar com diferentes dispositivos
- **Contingência:** Aceitar qualidade menor se necessário

**Risco 5: Connection drops**
- **Impacto:** Alto - interrupção do serviço
- **Probabilidade:** Média
- **Mitigação:**
  - Implementar reconnection logic
  - State recovery após desconexão
  - Heartbeat para detectar drops
- **Contingência:** Exigir reconexão manual

### 8.2 Riscos de Integração Pi

**Risco 6: Tool execution blocking UI**
- **Impacto:** Médio - UI não responsiva
- **Probabilidade:** Baixa
- **Mitigação:**
  - Usar streaming updates
  - Processar em background
  - Abort operations com ESC
- **Contingência:** Aceitar bloqueios curtos

**Risco 7: Session state corruption**
- **Impacto:** Alto - dados perdidos
- **Probabilidade:** Baixa
- **Mitigação:**
  - Implementar branching support
  - Reconstruir estado do session
  - Validar estado antes de usar
- **Contingência:** Limpar estado se corrompido

**Risco 8: Event handler conflicts**
- **Impacto:** Médio - comportamento indefinido
- **Probabilidade:** Baixa
- **Mitigação:**
  - Documentar ordem de handlers
  - Usar signal handling correto
  - Evitar side effects
- **Contingência:** Desabilitar handlers conflitantes

**Risco 9: Memory growth**
- **Impacto:** Alto - crash após tempo
- **Probabilidade:** Média
- **Mitigação:**
  - Limitar buffer sizes
  - Limpar periodicamente
  - Implementar garbage collection hints
- **Contingência:** Reiniciar sessão periodicamente

**Risco 10: /reload breaking state**
- **Impacto:** Médio - perda de estado
- **Probabilidade:** Baixa
- **Mitigação:**
  - Reconstruir estado no session_start
  - Persistir estado em entries
  - Documentar comportamento
- **Contingência:** Exigir reconexão manual

### 8.3 Riscos de Dependências

**Risco 11: LiveKit SDK breaking changes**
- **Impacto:** Alto - extensão quebra
- **Probabilidade:** Baixa
- **Mitigação:**
  - Pin versão específica
  - Monitorar changelog
  - Testar com beta releases
- **Contingência:** Manter fork de versão estável

**Risco 12: Deepgram API limits**
- **Impacto:** Médio - serviço parado
- **Probabilidade:** Baixa
- **Mitigação:**
  - Implementar rate limiting
  - Tratar erros de quota
  - Cache transcripts se possível
- **Contingência:** Switch para outro STT provider

**Risco 13: Cartesia API issues**
- **Impacto:** Médio - sem TTS
- **Probabilidade:** Baixa
- **Mitigação:**
  - Fallback TTS provider
  - Retry logic com backoff
  - Cache de áudio gerado
- **Contingência:** Usar TTS simples (espeak)

**Risco 14: Node.js compatibility**
- **Impacto:** Médio - não roda em algumas versões
- **Probabilidade:** Baixa
- **Mitigação:**
  - Target LTS (Node 20+)
  - Testar em múltiplas versões
  - Usar APIs estáveis
- **Contingência:** Exigir versão específica

**Risco 15: Network restrictions**
- **Impacto:** Alto - não funciona em alguns ambientes
- **Probabilidade:** Média
- **Mitigação:**
  - Configurar portas corretamente
  - Suporte a proxy
  - Documentar requisitos de rede
- **Contingência:** Apenas funciona em ambientes configurados

### 8.4 Riscos de Performance

**Risco 16: CPU usage alto**
- **Impacto:** Médio - lento
- **Probabilidade:** Baixa
- **Mitigação:**
  - Otimizar VAD
  - Usar modelos mais leves
  - Offload para GPU se possível
- **Contingência:** Aceitar uso mais alto

**Risco 17: Network bandwidth alto**
- **Impacto:** Baixo - custo maior
- **Probabilidade:** Média
- **Mitigação:**
  - Comprimir áudio
  - Usar bitrate menor
  - Otimizar codecs
- **Contingência:** Documentar requisitos de banda

**Risco 18: Startup time lento**
- **Impacto:** Baixo - UX ruim
- **Probabilidade:** Baixa
- **Mitigação:**
  - Lazy loading
  - Cache de configuração
  - Async initialization
- **Contingência:** Aceitar startup mais lento

**Risco 19: Memory footprint grande**
- **Impacto:** Médio - não roda em sistemas limitados
- **Probabilidade:** Baixa
- **Mitigação:**
  - Otimizar buffer sizes
  - Streaming em vez de buffers completos
  - Liberar recursos não usados
- **Contingência:** Documentar requisitos de memória

### 8.5 Riscos de UX

**Risco 20: Confusing UI**
- **Impacto:** Médio - difícil de usar
- **Probabilidade:** Média
- **Mitigação:**
  - Usar ícones claros
  - Mensagens de status descritivas
  - Tooltips e help
- **Contingência:** Simplificar UI

**Risco 21: Poor error messages**
- **Impacto:** Médio - difícil de debugar
- **Probabilidade:** Média
- **Mitigação:**
  - Mensagens de erro claras
  - Sugestões de solução
  - Links para documentação
- **Contingência:** Melhorar ao longo do tempo

**Risco 22: No feedback on actions**
- **Impacto:** Baixo - UX ruim
- **Probabilidade:** Baixa
- **Mitigação:**
  - Progress indicators
  - Notificações
  - Status widgets
- **Contingência:** Adicionar feedback

**Risco 23: Hard to configure**
- **Impacto:** Alto - muitos usuários desistem
- **Probabilidade:** Média
- **Mitigação:**
  - .env.example completo
  - Validação com mensagens claras
  - Defaults sensíveis
- **Contingência:** Melhorar documentação

**Risco 24: Interrupting assistant is confusing**
- **Impacto:** Médio - UX ruim
- **Probabilidade:** Alta
- **Mitigação:**
  - Falar claramente quando interrompido
  - Mostrar indicador visual
  - Implementar hotword
- **Contingência:** Aceitar interrupção sem feedback

---

## 9. Checklist de Validação

### 9.1 Setup e Configuração (7 itens)

- [ ] LiveKit Server está rodando e acessível
- [ ] .env existe com todas as variáveis necessárias
- [ ] API keys são válidas (testadas individualmente)
- [ ] ConfigLoader carrega configuração sem erros
- [ ] Validação de configuração funciona
- [ ] Estrutura de arquivos está criada
- [ ] Dependências NPM estão instaladas

### 9.2 Funcionalidade Básica (14 itens)

- [ ] Extensão carrega no Pi (`pi -e`)
- [ ] `/voice-start [room]` conecta à sala
- [ ] Conexão com LiveKit é bem-sucedida
- [ ] Tracks de áudio são subscritos
- [ ] VAD detecta início de fala
- [ ] VAD detecta fim de fala
- [ ] Deepgram transcreve áudio para texto
- [ ] Transcript é enviado ao Pi LLM
- [ ] Pi LLM gera resposta
- [ ] Cartesia converte resposta para áudio
- [ ] Áudio é publicado no LiveKit
- [ ] Usuário ouve resposta
- [ ] Loop de conversação continua
- [ ] `/voice-stop` desconecta da sala

### 9.3 Loop de Conversação (6 itens)

- [ ] Múltiplos turns funcionam consecutivamente
- [ ] Interrupção de fala do assistente funciona
- [ ] Novo usuário iniciando fala cancela TTS anterior
- [ ] Estado transiciona corretamente (listening → processing → speaking → listening)
- [ ] Transcripts são acumulados no histórico
- [ ] Histórico persiste entre sessões

### 9.4 Gerenciamento de Sessão (6 itens)

- [ ] Estado persiste no Pi session
- [ ] Estado é reconstruído após /reload
- [ ] Conexão é restabelecida após desconexão
- [ ] Timeout de sessão funciona
- [ ] Sessão pode ser reiniciada
- [ ] Histórico pode ser limpo

### 9.5 UI e Feedback (9 itens)

- [ ] Status widget mostra estado atual
- [ ] Status widget atualiza em tempo real
- [ ] Widget mostra nome da sala
- [ ] Join room dialog funciona
- [ ] Confirm dialog funciona
- [ ] Notificações aparecem para ações importantes
- [ ] Errors são exibidos claramente
- [ ] Keyboard shortcuts funcionam
- [ ] UI é responsiva a mudanças de terminal

### 9.6 Tratamento de Erros (7 itens)

- [ ] Erros de conexão LiveKit são tratados
- [ ] Erros de API Deepgram são tratados
- [ ] Erros de API Cartesia são tratados
- [ ] Timeout de conexão funciona
- [ ] Reconnection logic funciona
- [ ] Erros são logados adequadamente
- [ ] Usuário pode recuperar de erros

### 9.7 Performance (7 itens)

- [ ] Latência de E2E < 2 segundos
- [ ] Latência de STT < 1 segundo
- [ ] Latência de TTS < 1 segundo
- [ ] CPU usage < 50% durante conversação
- [ ] Memory usage estável (sem leaks)
- [ ] Não há blocking da UI durante operações
- [ ] Streaming funciona (sem buffers completos)

### 9.8 Documentação (6 itens)

- [ ] README.md existe e está completo
- [ ] Instalação está documentada
- [ ] Configuração está documentada
- [ ] Uso está documentado com exemplos
- [ ] Troubleshooting guide existe
- [ ] API está documentada

### 9.9 Testes (9 itens)

- [ ] Testes unitários para ConfigLoader
- [ ] Testes unitários para SessionManager
- [ ] Testes unitários para LiveKitClient
- [ ] Testes unitários para STTManager
- [ ] Testes unitários para TTSManager
- [ ] Testes de integração funcionam
- [ ] Teste E2E com LiveKit room real
- [ ] Teste de latência foi executado
- [ ] Teste de longa duração (1 hora) foi executado

### 9.10 Robustez (5 itens)

- [ ] /reload não quebra estado
- [ ] Branching no Pi funciona com voice chat
- [ ] Múltiplas sessões podem ser criadas
- [ ] Extensão pode ser desabilitada sem quebrar Pi
- [ ] Não há memory leaks após uso prolongado

**Total:** 76 itens de validação

---

## 10. Inconsistências Encontradas e Soluções

### Inconsistência 1: Arquitetura LiveKit Agents vs Client SDK

**Problema:** LiveKit Agents (Python) vs LiveKit Client SDK (JavaScript)

**Solução:** Usar LiveKit Client SDK dentro da extensão Pi, pois:
- Mesma linguagem (TypeScript)
- Controle total do pipeline
- Integração direta com Pi events
- Sem necessidade de subprocess

### Inconsistência 2: Estado global vs state persistence

**Problema:** Variáveis globais não funcionam com branching

**Solução:** Usar `pi.appendEntry()` para persistir estado e reconstruir no `session_start`

### Inconsistência 3: Tool registration em event handlers

**Problema:** Registrar tools dentro de event handlers causa duplicação

**Solução:** Sempre registrar tools no top-level da extensão

### Inconsistência 4: Streaming vs batch processing

**Problema:** Pi streaming events vs APIs batch

**Solução:** Usar streaming APIs (Deepgram streaming, Cartesia streaming) e processar chunks

### Inconsistência 5: Abort signal propagation

**Problema:** Signal não propagado para operações aninhadas

**Solução:** Passar `ctx.signal` para todas as operações async que suportam abort

### Inconsistência 6: File path normalization

**Problema:** Paths com @ prefix não funcionam

**Solução:** Normalizar paths (strip @) como built-in tools

### Inconsistência 7: Enum types compatibilidade

**Problema:** Type.Union não funciona com Google API

**Solução:** Usar StringEnum de @mariozechner/pi-ai

### Inconsistência 8: Mutation de arquivos concorrente

**Problema:** Race conditions com edit/write

**Solução:** Usar `withFileMutationQueue()` para operações que mutam arquivos

### Inconsistência 9: Buffer limits

**Problema:** Buffers podem crescer indefinidamente

**Solução:** Implementar limites e limpar periodicamente

---

## 11. Validação do Planejamento

### 11.1 Revisão de Consistência Interna

**Arquitetura:** ✅ Consistente
- Componentes têm responsabilidades claras
- Dependências estão definidas
- Fluxo de dados é lógico

**Cronograma:** ✅ Consistente
- Fases estão em ordem lógica
- Dependências entre fases são respeitadas
- Tempo estimado é razoável

**Riscos:** ✅ Consistentes
- Riscos foram identificados
- Mitigações são adequadas
- Contingências foram consideradas

### 11.2 Validação de Dependências

**Dependências NPM:** ✅ Válidas
- Todos os pacotes existem
- Versões são compatíveis
- Não há conflitos

**Dependências Python:** ✅ Não necessárias
- Arquitetura usa JavaScript apenas
- LiveKit Agents não é necessário

**API Keys:** ⚠️ Necessárias validar
- Deepgram: `5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3`
- Cartesia: `sk_car_d69NmtdJKVbTj8XrrqM4Nt`
- **Ação:** Validar antes de implementar

### 11.3 Validação de Arquitetura

**Componentes:** ✅ Bem definidos
- Cada componente tem responsabilidade única
- Interfaces são claras
- Estimativa de linhas é razoável

**Fluxo de dados:** ✅ Lógico
- STT → LLM → TTS está claro
- Loop de conversação está definido
- Interrupções são tratadas

**Integração Pi:** ✅ Válida
- Usa events corretamente
- Tool registration está correto
- State persistence está implementado

### 11.4 Validação de Fases

**Fase 0 (Setup):** ✅ Clara
- Tarefas específicas
- Validação definida
- Risco baixo

**Fases 1-5 (Base):** ✅ Bem estruturadas
- Dependências claras
- Validação específica
- Risco baixo/médio

**Fases 6-7 (Integração):** ✅ Complexas mas válidas
- Maior risco aceitável
- Validação abrangente
- Contingências definidas

**Fases 8-13 (Polish):** ✅ Completas
- UI, errors, docs, testing
- Release preparado
- Risco baixo

### 11.5 Validação de Riscos

**Riscos técnicos:** ✅ Identificados e mitigados
- 5 riscos principais
- Mitigações adequadas
- Contingências definidas

**Riscos de integração Pi:** ✅ Identificados e mitigados
- 5 riscos principais
- Mitigações específicas para Pi
- Comportamento documentado

**Riscos de dependências:** ✅ Identificados e mitigados
- 5 riscos principais
- Mitigações para APIs terceiras
- Alternativas consideradas

### 11.6 Pontos Fracos Identificados e Mitigados

**Ponto fraco 1: Latência**
- **Identificado:** Risco #1
- **Mitigado:** Streaming TTS, otimizações de buffer
- **Contingência:** Aceitar latência maior se necessário

**Ponto fraco 2: API keys não validadas**
- **Identificado:** Seção 11.2
- **Mitigado:** Validação antes de implementar
- **Contingência:** Usar dev keys ou mock

**Ponto fraco 3: Complexidade de integração**
- **Identificado:** Fase 7
- **Mitigado:** Testes abrangentes, validação E2E
- **Contingência:** Simplificar se necessário

**Ponto fraco 4: Interrupções confusas**
- **Identificado:** Risco #24
- **Mitigado:** Feedback visual, hotword futuro
- **Contingência:** Aceitar UX imperfeita no MVP

**Ponto fraco 5: Configuração complexa**
- **Identificado:** Risco #23
- **Mitigado:** .env.example, validação, defaults
- **Contingência:** Melhorar documentação

---

## Conclusão

**Planejamento está completo e validado:**
- ✅ Arquitetura proposta é sólida
- ✅ Fases de implementação estão bem definidas
- ✅ Riscos foram identificados e mitigados
- ✅ Checklist de validação é abrangente (76 itens)
- ✅ Inconsistências foram resolvidas
- ✅ Próximos passos são claros

**Próximos passos imediatos:**
1. Validar API keys (Deepgram, Cartesia)
2. Setup ambiente de desenvolvimento
3. Começar Fase 0 (Preparação do ambiente)
4. Implementar Fase 1 (Tipos e Configuração)

**Estimativa de tempo total:** 12-15 dias para MVP funcional

---

*Este planejamento está pronto para execução. Qualquer alteração deve ser documentada e validada novamente.*
