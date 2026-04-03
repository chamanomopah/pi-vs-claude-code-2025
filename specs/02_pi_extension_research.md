# Pi Extension Research - Guia Completo

> Pesquisa realizada em 2026-04-03
> Fonte: Documentação oficial do Pi e código-fonte

---

## Índice
1. [Como o Pi funciona (Arquitetura Principal)](#1-como-o-pi-funciona-arquitetura-principal)
2. [Como criar uma extensão nova no Pi](#2-como-criar-uma-extensão-nova-no-pi)
3. [Como integrar LiveKit como forma de usar o Pi através de agente de voz](#3-como-integrar-livekit-como-forma-de-usar-o-pi-através-de-agente-de-voz)
4. [Boas práticas para extensões do Pi](#4-boas-práticas-para-extensões-do-pi)
5. [O que será necessário para essa integração](#5-o-que-será-necessário-para-essa-integração)
6. [Problemas comuns a evitar ao criar extensões](#6-problemas-comuns-a-evitar-ao-criar-extensões)
7. [Como o Pi gerencia sessões, modelos e providers](#7-como-o-pi-gerencia-sessões-modelos-e-providers)
8. [Estrutura de arquivos e pastas do Pi](#8-estrutura-de-arquivos-e-pastas-do-pi)
9. [Plano de implementação para integração LiveKit](#9-plano-de-implementação-para-integração-livekit)
10. [Conclusões e próximos passos](#10-conclusões-e-próximos-passos)

---

## 1. Como o Pi funciona (Arquitetura Principal)

### 1.1 Visão Geral da Arquitetura

Pi é um minimal terminal coding harness extensível construído sobre várias camadas:

```
┌─────────────────────────────────────────────────────────┐
│                    Interactive Mode                      │
│  (Editor, Commands, Keyboard Shortcuts, Message Queue)  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Extension Runtime                      │
│  (Event Handlers, Tools, Commands, UI Components)       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Agent Framework                       │
│  (@mariozechner/pi-agent - Core LLM interaction)        │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                       AI Toolkit                         │
│  (@mariozechner/pi-ai - Models, Providers, Prompts)     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Provider Layer                        │
│  (Anthropic, OpenAI, Google, Custom, OAuth)            │
└─────────────────────────────────────────────────────────┘
```

**Pacotes principais:**
- `@mariozechner/pi-coding-agent` - Core do Pi com extensions e SDK
- `@mariozechner/pi-agent` - Agent framework para LLM interactions
- `@mariozechner/pi-ai` - AI toolkit com modelos e providers
- `@mariozechner/pi-tui` - Terminal UI components para interfaces customizadas

### 1.2 Ciclo de Vida de Sessão

```
pi starts (CLI only)
  │
  ├─► session_directory (CLI startup only, no ctx)
  └─► session_start
      │
      ▼
user sends prompt ─────────────────────────────────────────┐
  │                                                        │
  ├─► (extension commands checked first, bypass if found)  │
  ├─► input (can intercept, transform, or handle)          │
  ├─► (skill/template expansion if not handled)            │
  ├─► before_agent_start (can inject message, modify system prompt)
  ├─► agent_start                                          │
  ├─► message_start / message_update / message_end         │
  │                                                        │
  │   ┌─── turn (repeats while LLM calls tools) ───┐       │
  │   │                                            │       │
  │   ├─► turn_start                               │       │
  │   ├─► context (can modify messages)            │       │
  │   ├─► before_provider_request (can inspect or replace payload)
  │   │                                            │       │
  │   │   LLM responds, may call tools:            │       │
  │   │     ├─► tool_execution_start               │       │
  │   │     ├─► tool_call (can block)              │       │
  │   │     ├─► tool_execution_update              │       │
  │   │     ├─► tool_result (can modify)           │       │
  │   │     └─► tool_execution_end                 │       │
  │   │                                            │       │
  │   └─► turn_end                                 │       │
  │                                                        │
  └─► agent_end                                            │
                                                           │
user sends another prompt ◄────────────────────────────────┘

/new (new session) or /resume (switch session)
  ├─► session_before_switch (can cancel)
  └─► session_switch

/fork
  ├─► session_before_fork (can cancel)
  └─► session_fork

/compact or auto-compaction
  ├─► session_before_compact (can cancel or customize)
  └─► session_compact

/tree navigation
  ├─► session_before_tree (can cancel or customize)
  └─► session_tree

/model or Ctrl+P (model selection/cycling)
  └─► model_select

exit (Ctrl+C, Ctrl+D)
  └─► session_shutdown
```

**Eventos principais:**
- **Session events:** `session_start`, `session_switch`, `session_fork`, `session_compact`, `session_tree`, `session_shutdown`
- **Agent events:** `before_agent_start`, `agent_start`, `agent_end`, `turn_start`, `turn_end`, `message_start/update/end`
- **Tool events:** `tool_execution_start/update/end`, `tool_call`, `tool_result`
- **Model events:** `model_select`
- **User events:** `input`, `user_bash`

### 1.3 Sistema de Tools

**Tools são funções que o LLM pode chamar:**

```typescript
interface ToolDefinition {
  name: string;
  label: string;
  description: string;
  promptSnippet?: string;           // Uma linha em "Available tools"
  promptGuidelines?: string[];      // Guidelines específicas
  parameters: TSchema;              // TypeBox schema
  prepareArguments?(args: any): any; // Compatibilidade
  execute: (
    toolCallId: string,
    params: any,
    signal?: AbortSignal,
    onUpdate?: (update: ToolUpdate) => void,
    ctx?: ExtensionContext
  ) => Promise<ToolResult>;
  renderCall?: (args, theme, context) => string[];
  renderResult?: (result, options, theme, context) => string[];
}
```

**Tools built-in:**
- `read` - Lê conteúdo de arquivos
- `write` - Escreve/cria arquivos
- `edit` - Edita arquivos com find/replace
- `bash` - Executa comandos shell
- `grep` - Busca padrões em arquivos
- `find` - Encontra arquivos por glob
- `ls` - Lista diretórios

**Registro de tools:**
```typescript
import { Type } from "@sinclair/typebox";

pi.registerTool({
  name: "my_tool",
  label: "My Tool",
  description: "What this tool does",
  parameters: Type.Object({
    input: Type.String({ description: "Input value" }),
  }),
  async execute(toolCallId, params, signal, onUpdate, ctx) {
    return {
      content: [{ type: "text", text: `Result: ${params.input}` }],
      details: {},
    };
  },
});
```

### 1.4 Sistema de UI/TUI

**Pi usa @mariozechner/pi-tui para componentes customizados:**

```typescript
interface Component {
  render(width: number): string[];
  handleInput?(data: string): void;
  wantsKeyRelease?: boolean;
  invalidate(): void;
}
```

**Componentes built-in:**
- `Text` - Texto multi-line com word wrapping
- `Box` - Container com padding e background
- `Container` - Agrupa componentes verticalmente
- `Spacer` - Espaço vertical vazio
- `Markdown` - Renderiza markdown com syntax highlighting
- `Image` - Renderiza imagens (Kitty, iTerm2, Ghostty, WezTerm)
- `Input` - Input de texto com IME support
- `Editor` - Editor multi-line completo
- `Selector` - Seleção de itens
- `Confirm` - Dialog de confirmação

**Usando UI em extensions:**
```typescript
pi.on("session_start", async (_event, ctx) => {
  // Notify
  ctx.ui.notify("Extension loaded!", "info");
  
  // Confirm dialog
  const ok = await ctx.ui.confirm("Title", "Are you sure?");
  
  // Select dialog
  const selected = await ctx.ui.select("Choose", ["A", "B", "C"]);
  
  // Input dialog
  const text = await ctx.ui.input("Enter value:");
  
  // Custom component
  const handle = ctx.ui.custom(myComponent);
  handle.close();
  
  // Status line
  ctx.ui.setStatus("my-ext", "Processing...");
  
  // Widget above editor
  ctx.ui.setWidget("my-ext", ["Line 1", "Line 2"]);
});
```

### 1.5 SDK para Integração

**O SDK permite integrar o Pi em outras aplicações:**

```typescript
import { 
  AuthStorage, 
  createAgentSession, 
  ModelRegistry, 
  SessionManager 
} from "@mariozechner/pi-coding-agent";

const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage: AuthStorage.create(),
  modelRegistry: ModelRegistry.create(authStorage),
});

session.subscribe((event) => {
  if (event.type === "message_update" && 
      event.assistantMessageEvent.type === "text_delta") {
    process.stdout.write(event.assistantMessageEvent.delta);
  }
});

await session.prompt("What files are in the current directory?");
```

**Modos de execução:**
- `InteractiveMode` - Full TUI com editor e comandos
- `runPrintMode` - Single-shot, output e exit
- `runRpcMode` - JSON-RPC para integração subprocess
- SDK direto - Acesso programático completo

---

## 2. Como criar uma extensão nova no Pi

### 2.1 Estrutura Básica

**Extensão é um módulo TypeScript que exporta uma função default:**

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";

export default function (pi: ExtensionAPI) {
  // Registrar tools
  pi.registerTool({
    name: "my_tool",
    label: "My Tool",
    description: "Does something useful",
    parameters: Type.Object({
      input: Type.String(),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      return {
        content: [{ type: "text", text: `Result: ${params.input}` }],
        details: {},
      };
    },
  });

  // Registrar comandos
  pi.registerCommand("mycmd", {
    description: "My command",
    handler: async (args, ctx) => {
      ctx.ui.notify(`Hello ${args || "world"}!`, "info");
    },
  });

  // Subscrever a eventos
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.notify("Extension loaded!", "info");
  });
}
```

### 2.2 Locais de Extensões

**Auto-discovery de extensions:**

| Location | Scope |
|----------|-------|
| `~/.pi/agent/extensions/*.ts` | Global (todos os projetos) |
| `~/.pi/agent/extensions/*/index.ts` | Global (subdiretório) |
| `.pi/extensions/*.ts` | Project-local |
| `.pi/extensions/*/index.ts` | Project-local (subdiretório) |

**Carregamento via CLI:**
```bash
pi -e ./my-extension.ts  # Quick test (sem reload)
```

**Carregamento via settings.json:**
```json
{
  "extensions": [
    "/path/to/local/extension.ts",
    "/path/to/local/extension/dir"
  ]
}
```

**Hot-reload:**
```bash
/reload  # Recarrega extensions, skills, prompts, themes
```

### 2.3 Imports Disponíveis

**Imports padrão disponíveis em extensions:**

```typescript
// Core types
import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";

// Event types
import { isToolCallEventType, isBashToolResult } from "@mariozechner/pi-coding-agent";

// Schemas
import { Type } from "@sinclair/typebox";

// AI utilities
import { StringEnum } from "@mariozechner/pi-ai";

// TUI components
import { 
  Text, Box, Container, Spacer, Markdown,
  Input, Selector, Confirm,
  matchesKey, Key,
  CURSOR_MARKER, type Focusable
} from "@mariozechner/pi-tui";

// Node.js built-ins
import { readFileSync, writeFileSync } from "node:fs";
import { resolve, join } from "node:path";
```

**Dependências npm:**
Adicione um `package.json` ao lado da extension:
```json
{
  "name": "my-extension",
  "dependencies": {
    "axios": "^1.0.0",
    "chalk": "^5.0.0"
  }
}
```

Rode `npm install` no diretório da extension, e os imports funcionam automaticamente.

### 2.4 Exemplos de Código

**Extension com tool blocking:**
```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { isToolCallEventType } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("tool_call", async (event, ctx) => {
    // Bloquear comandos perigosos
    if (isToolCallEventType("bash", event)) {
      if (event.input.command?.includes("rm -rf")) {
        const ok = await ctx.ui.confirm("Dangerous!", "Allow rm -rf?");
        if (!ok) return { block: true, reason: "Blocked by user" };
      }
    }
  });
}
```

**Extension com custom UI:**
```typescript
import { Text, Box, Container } from "@mariozechner/pi-tui";

class MyWidget extends Container {
  constructor() {
    super();
    this.addChild(new Text("Status: Active", 0, 0));
  }
}

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    const handle = ctx.ui.custom(new MyWidget());
    // Widget fica ativo até handle.close()
  });
}
```

**Extension com state persistence:**
```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  let items: string[] = [];

  // Restaurar estado da sessão
  pi.on("session_start", async (_event, ctx) => {
    items = [];
    for (const entry of ctx.sessionManager.getEntries()) {
      if (entry.type === "custom" && entry.customType === "my-state") {
        items = entry.data?.items ?? [];
      }
    }
  });

  pi.registerTool({
    name: "add_item",
    parameters: {},
    async execute(toolCallId, _params, _signal, _onUpdate, ctx) {
      items.push(`item-${items.length + 1}`);
      
      // Persistir estado
      pi.appendEntry("my-state", { items: [...items] });
      
      return {
        content: [{ type: "text", text: `Added. Total: ${items.length}` }],
        details: { items: [...items] },
      };
    },
  });
}
```

---

## 3. Como integrar LiveKit como forma de usar o Pi através de agente de voz

### 3.1 Arquiteturas Possíveis

**Arquitetura 1: Pi como orquestrador (Recomendada)**
```
┌─────────────────────────────────────────────────────────┐
│                       Usuario                             │
│                    (Browser/Mobile)                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    LiveKit Room                          │
│              (Audio/Video WebRTC)                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Pi Extension (voice-chat.ts)                │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐             │
│  │   STT     │  │   LLM     │  │   TTS    │             │
│  │ Deepgram  │→ │   Pi     │→ │ Cartesia │             │
│  └───────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

**Arquitetura 2: LiveKit Agents + Pi via SDK**
```
┌─────────────────────────────────────────────────────────┐
│                       Usuario                             │
│                    (Browser/Mobile)                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              LiveKit Agent (Python)                      │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐             │
│  │   STT     │  │  Custom  │  │   TTS    │             │
│  │ Deepgram  │→ │   Tool   │→ │ Cartesia │             │
│  └───────────┘  └────┬─────┘  └──────────┘             │
│                     │                                     │
│                     ▼                                     │
│         ┌───────────────────┐                           │
│         │   Pi via SDK       │                           │
│         │  (subprocess/RPC)  │                           │
│         └───────────────────┘                           │
└─────────────────────────────────────────────────────────┘
```

**Arquitetura 3: Pi Extension com LiveKit Client SDK**
```
┌─────────────────────────────────────────────────────────┐
│                       Usuario                             │
│                    (Browser/Mobile)                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  LiveKit Server                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Pi Extension (livekit-client.ts)           │
│              (LiveKit Client SDK JS)                     │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐             │
│  │   STT     │  │   LLM     │  │   TTS    │             │
│  │ Deepgram  │→ │   Pi     │→ │ Cartesia │             │
│  └───────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Pipeline Completo de Voz

```
User Speaks (Audio)
    │
    ├─► Captured by LiveKit Client (Browser)
    │
    ├─► Sent via WebRTC to LiveKit Server
    │
    ├─► Received by Pi Extension (as participant)
    │
    ├─► LiveKitClient: onTrackSubscribed (audio track)
    │
    ├─► STTManager: Transcribe audio to text
    │       │
    │       └─► Deepgram API (streaming STT)
    │
    ├─► VoiceChatTool: Send transcript to Pi LLM
    │       │
    │       └─► pi.sendUserMessage(transcript)
    │
    ├─► Pi LLM: Generate response
    │       │
    │       ├─► May call other tools (read, write, etc.)
    │       └─► Returns text response
    │
    ├─► VoiceChatTool: Receive LLM response
    │
    ├─► TTSManager: Convert text to audio
    │       │
    │       └─► Cartesia API (streaming TTS)
    │
    ├─► LiveKitClient: Publish audio track
    │
    └─► Audio plays in user's browser
```

### 3.3 Exemplos de Código

**Tool básico de voice chat:**
```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "voice_chat",
    label: "Voice Chat",
    description: "Interact with user via voice chat",
    parameters: Type.Object({
      message: Type.String({ description: "User's spoken message" }),
    }),
    async execute(toolCallId, params, _signal, _onUpdate, ctx) {
      // Enviar mensagem do usuário para o Pi
      pi.sendUserMessage(params.message);
      
      // A resposta virá via event listener
      return {
        content: [{ type: "text", text: "Processing voice input..." }],
        details: { userMessage: params.message },
      };
    },
  });
}
```

**Capturando resposta do LLM para TTS:**
```typescript
export default function (pi: ExtensionAPI) {
  pi.on("message_update", async (event, ctx) => {
    if (event.assistantMessageEvent.type === "text_delta") {
      const delta = event.assistantMessageEvent.delta;
      
      // Enviar para TTS
      await ctx.ttsManager.speak(delta);
      
      // Ou acumular para enviar ao LiveKit
      ctx.voiceBuffer += delta;
    }
  });

  pi.on("message_end", async (event, ctx) => {
    // Enviar audio completo via LiveKit
    if (ctx.voiceBuffer.length > 0) {
      const audioData = await ctx.ttsManager.synthesize(ctx.voiceBuffer);
      await ctx.liveKitClient.publishAudio(audioData);
      ctx.voiceBuffer = "";
    }
  });
}
```

---

## 4. Boas práticas para extensões do Pi

### 4.1 Registro de Tools

**Sempre registre tools no nível top-level da extension:**
```typescript
export default function (pi: ExtensionAPI) {
  // ✅ CORRETO - Registra no top-level
  pi.registerTool({ ... });
  
  pi.on("session_start", async () => {
    // ❌ ERRADO - Não registre tools aqui (será duplicado em /reload)
    // pi.registerTool({ ... });
  });
}
```

**Use TypeBox para schemas:**
```typescript
import { Type, StringEnum } from "@sinclair/typebox";

// ✅ CORRETO - Use StringEnum para compatibilidade com Google
parameters: Type.Object({
  action: StringEnum(["list", "add", "delete"] as const),
  text: Type.Optional(Type.String()),
})

// ❌ ERRADO - Type.Union não funciona com Google
parameters: Type.Object({
  action: Type.Union([
    Type.Literal("list"),
    Type.Literal("add"),
    Type.Literal("delete"),
  ]),
})
```

### 4.2 Type-safe Event Handling

**Use `isToolCallEventType` para narrowing:**
```typescript
import { isToolCallEventType } from "@mariozechner/pi-coding-agent";

pi.on("tool_call", async (event, ctx) => {
  // Built-in tools: sem type params
  if (isToolCallEventType("bash", event)) {
    // event.input é { command: string; timeout?: number }
    event.input.command = `source ~/.profile\n${event.input.command}`;
  }

  if (isToolCallEventType("read", event)) {
    // event.input é { path: string; offset?: number; limit?: number }
    console.log(`Reading: ${event.input.path}`);
  }

  // Custom tools com type params
  if (isToolCallEventType<"my_tool", MyToolInput>("my_tool", event)) {
    event.input.action;  // typed
  }
});
```

**Use `isBashToolResult` para results:**
```typescript
import { isBashToolResult } from "@mariozechner/pi-coding-agent";

pi.on("tool_result", async (event, ctx) => {
  if (isBashToolResult(event)) {
    // event.details é BashToolDetails
    console.log(`Exit code: ${event.details.exitCode}`);
  }
});
```

### 4.3 Output Truncation

**Pi automaticamente trunca output longo. Para controle customizado:**

```typescript
async execute(toolCallId, params, signal, onUpdate, ctx) {
  // Streaming updates
  onUpdate?.({
    content: [{ type: "text", text: "Processing..." }],
  });

  const result = await longRunningOperation();

  return {
    content: [{ type: "text", text: result }],  // Pi trunca se necessário
    details: { fullResult: result },  // Dados completos não truncados
  };
}
```

**Arquivos de output completo:**
```typescript
async execute(toolCallId, params, signal, onUpdate, ctx) {
  const outputPath = "/tmp/tool-output.txt";
  
  // Escrever output completo para arquivo
  await fs.writeFile(outputPath, largeOutput);
  
  return {
    content: [
      { type: "text", text: "Output written to file (truncated preview):\n" },
      { type: "text", text: largeOutput.slice(0, 1000) + "..." },
    ],
    details: { 
      outputPath,
      size: largeOutput.length,
    },
  };
}
```

### 4.4 Gerenciamento de Estado

**Use `details` para state com branching:**
```typescript
export default function (pi: ExtensionAPI) {
  let state = { items: [] as string[] };

  // Restaurar estado da sessão
  pi.on("session_start", async (_event, ctx) => {
    state.items = [];
    for (const entry of ctx.sessionManager.getBranch()) {
      if (entry.type === "message" && 
          entry.message.role === "toolResult" &&
          entry.message.toolName === "my_tool") {
        state.items = entry.message.details?.items ?? [];
      }
    }
  });

  pi.registerTool({
    name: "my_tool",
    async execute(toolCallId, params, _signal, _onUpdate, ctx) {
      state.items.push(params.item);
      
      return {
        content: [{ type: "text", text: "Added" }],
        details: { items: [...state.items] },  // Store para reconstruction
      };
    },
  });
}
```

**Use `pi.appendEntry` para state persistente:**
```typescript
// State que não vai para o LLM
pi.appendEntry("my-state", { count: 42 });

// Restaurar on reload
pi.on("session_start", async (_event, ctx) => {
  for (const entry of ctx.sessionManager.getEntries()) {
    if (entry.type === "custom" && entry.customType === "my-state") {
      // Reconstruir estado
    }
  }
});
```

### 4.5 UI e Interação

**Use `ctx.ui` para interações com usuário:**
```typescript
pi.on("tool_call", async (event, ctx) => {
  // Confirm dialog
  const ok = await ctx.ui.confirm("Title", "Are you sure?");
  if (!ok) return { block: true, reason: "User cancelled" };

  // Select dialog
  const selected = await ctx.ui.select("Choose option:", [
    { value: "a", label: "Option A" },
    { value: "b", label: "Option B" },
  ]);

  // Input dialog
  const text = await ctx.ui.input("Enter value:");

  // Notify
  ctx.ui.notify("Operation complete", "success");

  // Status line
  ctx.ui.setStatus("my-ext", "Processing...");

  // Widget above editor
  ctx.ui.setWidget("my-ext", ["Status: Active"]);
});
```

**Custom UI components:**
```typescript
import { Text, Box, Container } from "@mariozechner/pi-tui";

class MyWidget extends Container {
  constructor(private status: string) {
    super();
    this.updateContent();
  }

  setStatus(status: string) {
    this.status = status;
    this.updateContent();
  }

  private updateContent() {
    this.clearChildren();
    this.addChild(
      new Box(1, 1, (s) => `\x1b[48;5;238m${s}\x1b[0m`, [
        new Text(`Status: ${this.status}`, 0, 0),
      ])
    );
  }
}

// Usage
const widget = new MyWidget("Idle");
const handle = ctx.ui.custom(widget);

// Update later
widget.setStatus("Processing");
handle.requestRender();

// Close
handle.close();
```

### 4.6 Tratamento de Erros

**Use `signal` para abort-aware operations:**
```typescript
async execute(toolCallId, params, signal, onUpdate, ctx) {
  // Check for cancellation
  if (signal?.aborted) {
    return { content: [{ type: "text", text: "Cancelled" }] };
  }

  // Abort-aware fetch
  const response = await fetch("https://api.example.com", {
    method: "POST",
    body: JSON.stringify(params),
    signal: ctx.signal,  // Propagar signal
  });

  const data = await response.json();
  return {
    content: [{ type: "text", text: JSON.stringify(data) }],
    details: {},
  };
}
```

**Throw errors para sinalizar falha:**
```typescript
async execute(toolCallId, params) {
  if (!isValid(params.input)) {
    throw new Error(`Invalid input: ${params.input}`);
  }
  return { content: [{ type: "text", text: "OK" }], details: {} };
}
```

**Wrapping operações:**
```typescript
try {
  const result = await riskyOperation();
  return { content: [{ type: "text", text: "Success" }], details: result };
} catch (error) {
  ctx.ui.notify(`Error: ${error.message}`, "error");
  throw error;  // Pi marca como isError: true
}
```

---

## 5. O que será necessário para essa integração

### 5.1 Estrutura de Arquivos Necessária

```
pi-vs-claude-code-2025/
├── extensions/
│   └── livekit-voice-chat/
│       ├── package.json              # Dependências
│       ├── tsconfig.json              # Config TypeScript
│       ├── src/
│       │   ├── index.ts               # Entry point
│       │   ├── livekit-client.ts      # LiveKit client wrapper
│       │   ├── stt-manager.ts         # Deepgram STT
│       │   ├── tts-manager.ts         # Cartesia TTS
│       │   ├── session-manager.ts    # Voice session state
│       │   ├── ui-components.ts       # Custom UI
│       │   ├── config.ts             # Configuration
│       │   └── types.ts               # TypeScript types
│       └── node_modules/
├── .pi/
│   └── extensions/                   # Simlink ou cópia
│       └── livekit-voice-chat.ts     # -> extensions/livekit-voice-chat/src/index.ts
└── .env                              # Credenciais
```

### 5.2 Dependências

**package.json:**
```json
{
  "name": "livekit-voice-chat-extension",
  "version": "0.1.0",
  "type": "module",
  "dependencies": {
    "@mariozechner/pi-coding-agent": "latest",
    "@mariozechner/pi-tui": "latest",
    "@sinclair/typebox": "^0.33.0",
    "livekit-client-sdk": "^2.0.0",
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

**Dependências Python (para LiveKit Agents, se necessário):**
```txt
livekit-agents~=1.4
livekit-plugins-deepgram
livekit-plugins-cartesia
python-dotenv
```

### 5.3 Credenciais

**.env:**
```env
# LiveKit
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret

# Deepgram STT
DEEPGRAM_API_KEY=your_deepgram_key

# Cartesia TTS
CARTESIA_API_KEY=sk_car_your_cartesia_key

# Pi (opcional, se usar modelo específico)
ANTHROPIC_API_KEY=sk-ant-your-key
```

### 5.4 Portas e Configuração

**Portas necessárias:**
- `7880` - LiveKit WebSocket/HTTP principal
- `7881` - LiveKit WebRTC sobre TCP
- `50000-60000` - LiveKit WebRTC sobre UDP
- `3478` - STUN/TURN (se configurado)

**Configuração de firewall:**
```bash
# Abrir portas LiveKit
sudo ufw allow 7880/tcp
sudo ufw allow 7881/tcp
sudo ufw allow 50000:60000/udp
```

**Iniciar LiveKit Server:**
```bash
# Modo dev
livekit-server --dev

# Com config customizada
livekit-server --config config.yaml
```

---

## 6. Problemas Comuns a Evitar ao Criar Extensões

### 6.1 Lista de Problemas Comuns

**1. Registrar tools dentro de event handlers**
```typescript
// ❌ ERRADO - Será duplicado em /reload
pi.on("session_start", async () => {
  pi.registerTool({ ... });
});

// ✅ CORRETO - Registrar no top-level
export default function (pi: ExtensionAPI) {
  pi.registerTool({ ... });
}
```

**2. Não usar `signal` em operações async**
```typescript
// ❌ ERRADO - Não responde a cancelamento
async execute(toolCallId, params) {
  const result = await fetch("https://api.example.com");
  return { content: [{ type: "text", text: result }] };
}

// ✅ CORRETO - Abort-aware
async execute(toolCallId, params, signal) {
  const result = await fetch("https://api.example.com", { signal });
  return { content: [{ type: "text", text: result }] };
}
```

**3. Não usar TypeBox.StringEnum para enums**
```typescript
import { Type } from "@sinclair/typebox";

// ❌ ERRADO - Não funciona com Google
parameters: Type.Object({
  action: Type.Union([
    Type.Literal("list"),
    Type.Literal("add"),
  ]),
})

// ✅ CORRETO - StringEnum para compatibilidade
import { StringEnum } from "@mariozechner/pi-ai";
parameters: Type.Object({
  action: StringEnum(["list", "add"] as const),
})
```

**4. Mutar estado global sem considerar branching**
```typescript
// ❌ ERRADO - Estado global quebra branching
let globalItems: string[] = [];

pi.registerTool({
  name: "add_item",
  async execute() {
    globalItems.push("item");
    return { content: [{ type: "text", text: "Added" }] };
  },
});

// ✅ CORRETO - Reconstruir do session
pi.registerTool({
  name: "add_item",
  async execute() {
    const items = reconstructItemsFromSession(ctx);
    items.push("item");
    return { 
      content: [{ type: "text", text: "Added" }],
      details: { items }  // Store para reconstruction
    };
  },
});
```

**5. Bloquear thread principal em tool execution**
```typescript
// ❌ ERRADO - Bloqueia UI
async execute() {
  const result = await longSyncOperation();  // 10 segundos
  return { content: [{ type: "text", text: result }] };
}

// ✅ CORRETO - Usar streaming updates
async execute(toolCallId, params, signal, onUpdate) {
  onUpdate?.({ content: [{ type: "text", text: "Starting..." }] });
  
  const result = await longSyncOperation();
  
  onUpdate?.({ content: [{ type: "text", text: "Done" }] });
  return { content: [{ type: "text", text: result }] };
}
```

**6. Não usar `withFileMutationQueue` para tools que mutam arquivos**
```typescript
// ❌ ERRADO - Race conditions com edit/write
async execute(toolCallId, params, _signal, _onUpdate, ctx) {
  const content = await readFile(params.path);
  const modified = content.replace(params.old, params.new);
  await writeFile(params.path, modified);
}

// ✅ CORRETO - Usar mutation queue
import { withFileMutationQueue } from "@mariozechner/pi-coding-agent";

async execute(toolCallId, params, _signal, _onUpdate, ctx) {
  const absolutePath = resolve(ctx.cwd, params.path);
  
  return withFileMutationQueue(absolutePath, async () => {
    const content = await readFile(absolutePath, "utf8");
    const modified = content.replace(params.old, params.new);
    await writeFile(absolutePath, modified, "utf8");
    
    return { content: [{ type: "text", text: "Updated" }] };
  });
}
```

**7. Não lidar com erros de conexão LiveKit**
```typescript
// ❌ ERRADO - Sem tratamento de erro
async execute(toolCallId, params) {
  const room = await lkClient.joinRoom(params.roomName);
  return { content: [{ type: "text", text: "Joined" }] };
}

// ✅ CORRETO - Tratamento robusto
async execute(toolCallId, params, signal) {
  try {
    const room = await lkClient.joinRoom(params.roomName, { signal });
    return { content: [{ type: "text", text: "Joined" }] };
  } catch (error) {
    ctx.ui.notify(`Failed to join: ${error.message}`, "error");
    throw error;
  }
}
```

**8. Acumular buffer de texto infinitamente**
```typescript
// ❌ ERRADO - Memory leak
let voiceBuffer = "";

pi.on("message_update", (event) => {
  if (event.assistantMessageEvent.type === "text_delta") {
    voiceBuffer += event.assistantMessageEvent.delta;
  }
});

// ✅ CORRETO - Limpar periodicamente
pi.on("message_update", (event) => {
  if (event.assistantMessageEvent.type === "text_delta") {
    voiceBuffer += event.assistantMessageEvent.delta;
    
    // Processar e limpar
    if (voiceBuffer.length > 1000) {
      processBuffer(voiceBuffer);
      voiceBuffer = "";
    }
  }
});
```

**9. Não usar `details` para state persistente**
```typescript
// ❌ ERRADO - State perdido em branching
let counter = 0;

pi.registerTool({
  name: "increment",
  async execute() {
    counter++;
    return { content: [{ type: "text", text: `Count: ${counter}` }] };
  },
});

// ✅ CORRETO - State em details
pi.registerTool({
  name: "increment",
  async execute(toolCallId, _params, _signal, _onUpdate, ctx) {
    const counter = getCounterFromSession(ctx) + 1;
    return { 
      content: [{ type: "text", text: `Count: ${counter}` }],
      details: { counter }  // Persiste no session
    };
  },
});
```

**10. Não normalizar paths com @ prefix**
```typescript
// ❌ ERRADO - @ prefix quebra path resolution
pi.registerTool({
  name: "my_read",
  parameters: Type.Object({
    path: Type.String(),
  }),
  async execute(toolCallId, params) {
    // Se path for "@file.ts", não vai funcionar
    const content = await readFile(params.path);
  },
});

// ✅ CORRETO - Normalizar @ prefix
pi.registerTool({
  name: "my_read",
  parameters: Type.Object({
    path: Type.String(),
  }),
  async execute(toolCallId, params) {
    // Strip leading @ como built-in tools
    const path = params.path.startsWith('@') 
      ? params.path.slice(1) 
      : params.path;
    const content = await readFile(path);
  },
});
```

### 6.2 Específicos para LiveKit

**11. Não fechar tracks/audio corretamente**
```typescript
// ❌ ERRADO - Memory leak
async execute() {
  const track = await room.localParticipant.publishTrack(audioTrack);
  // Nunca dispose track
}

// ✅ CORRETO - Limpar recursos
async execute(toolCallId, params, signal) {
  const track = await room.localParticipant.publishTrack(audioTrack);
  
  signal.addEventListener('abort', () => {
    track.stop();
  });
  
  return { content: [{ type: "text", text: "Published" }] };
}
```

**12. Não usar VAD para detecção de fala**
```typescript
// ❌ ERRADO - Processa silence como fala
const transcript = await sttManager.transcribe(audioBuffer);

// ✅ CORRETO - Usar VAD
const vadResults = await vad.detect(audioBuffer);
if (vadResults.speechDetected) {
  const transcript = await sttManager.transcribe(audioBuffer);
}
```

**13. Não fazer streaming de TTS**
```typescript
// ❌ ERRADO - Espera audio completo antes de tocar
const audio = await ttsManager.synthesize(fullText);
await audio.play();

// ✅ CORRETO - Streaming TTS
const stream = ttsManager.synthesizeStream(fullText);
for await (const chunk of stream) {
  await liveKitClient.publishAudio(chunk);
}
```

**14. Não sincronizar estado entre turns**
```typescript
// ❌ ERRADO - State inconsistente
let isSpeaking = false;

// Sem sincronização com session_start
pi.on("message_update", () => {
  isSpeaking = true;
});

// ✅ CORRETO - Reconstruir estado
pi.on("session_start", async (_event, ctx) => {
  const state = reconstructVoiceState(ctx);
  isSpeaking = state.isSpeaking;
});
```

---

## 7. Como o Pi gerencia sessões, modelos e providers

### 7.1 Sistema de Sessões (JSONL)

**Sessions são armazenadas como JSONL files:**
```
~/.pi/agent/sessions/--<path>--/<timestamp>_<uuid>.jsonl
```

**Estrutura com tree (versão 3):**
- Cada entry tem `id` e `parentId`
- Branching in-place sem criar novos arquivos
- Navegação via `/tree` command

**Tipos de entries:**

```json
// Session header (primeira linha)
{"type":"session","version":3,"id":"uuid","timestamp":"...","cwd":"/path"}

// Message
{"type":"message","id":"a1b2c3d4","parentId":"...","timestamp":"...","message":{...}}

// Model change
{"type":"model_change","id":"...","parentId":"...","provider":"anthropic","modelId":"claude-sonnet-4-5"}

// Thinking level change
{"type":"thinking_level_change","id":"...","parentId":"...","thinkingLevel":"high"}

// Compaction
{"type":"compaction","id":"...","parentId":"...","summary":"...","tokensBefore":50000}

// Branch summary
{"type":"branch_summary","id":"...","parentId":"...","fromId":"...","summary":"..."}

// Custom (extension state, não vai para LLM)
{"type":"custom","id":"...","parentId":"...","customType":"my-ext","data":{...}}

// Custom message (vai para LLM)
{"type":"custom_message","id":"...","parentId":"...","customType":"my-ext","content":"...","display":true}

// Label
{"type":"label","id":"...","parentId":"...","targetId":"...","label":"checkpoint"}

// Session info
{"type":"session_info","id":"...","parentId":"...","name":"My Session"}
```

### 7.2 Tipos de Mensagens

**Content blocks:**
```typescript
interface TextContent {
  type: "text";
  text: string;
}

interface ImageContent {
  type: "image";
  data: string;      // base64 encoded
  mimeType: string;  // "image/jpeg", "image/png"
}

interface ThinkingContent {
  type: "thinking";
  thinking: string;
}

interface ToolCall {
  type: "toolCall";
  id: string;
  name: string;
  arguments: Record<string, any>;
}
```

**Message types:**
```typescript
interface UserMessage {
  role: "user";
  content: string | (TextContent | ImageContent)[];
  timestamp: number;
}

interface AssistantMessage {
  role: "assistant";
  content: (TextContent | ThinkingContent | ToolCall)[];
  api: string;
  provider: string;
  model: string;
  usage: Usage;
  stopReason: "stop" | "length" | "toolUse" | "error" | "aborted";
  timestamp: number;
}

interface ToolResultMessage {
  role: "toolResult";
  toolCallId: string;
  toolName: string;
  content: (TextContent | ImageContent)[];
  details?: any;
  isError: boolean;
  timestamp: number;
}
```

### 7.3 Sistema de Modelos

**ModelRegistry gerencia modelos disponíveis:**
```typescript
import { ModelRegistry, AuthStorage } from "@mariozechner/pi-coding-agent";

const authStorage = AuthStorage.create();
const modelRegistry = ModelRegistry.create(authStorage);

// Encontrar modelo built-in
const model = getModel("anthropic", "claude-opus-4-5");

// Encontrar qualquer modelo (incluindo custom)
const customModel = modelRegistry.find("my-provider", "my-model");

// Apenas modelos com API key configurada
const available = await modelRegistry.getAvailable();
```

**Model cycling (Ctrl+P):**
```typescript
const { session } = await createAgentSession({
  scopedModels: [
    { model: opus, thinkingLevel: "high" },
    { model: haiku, thinkingLevel: "off" },
  ],
});
```

### 7.4 Sistema de Providers

**Providers built-in:**
- Anthropic
- OpenAI
- Azure OpenAI
- Google Gemini
- Google Vertex
- Amazon Bedrock
- Mistral
- Groq
- Cerebras
- xAI
- OpenRouter
- Vercel AI Gateway
- ZAI
- OpenCode Zen
- OpenCode Go
- Hugging Face
- Kimi For Coding
- MiniMax

**Custom providers via extensions:**
```typescript
pi.registerProvider("my-proxy", {
  baseUrl: "https://proxy.example.com",
  apiKey: "PROXY_API_KEY",
  api: "anthropic-messages",
  models: [
    {
      id: "claude-sonnet-4-20250514",
      name: "Claude 4 Sonnet (proxy)",
      reasoning: false,
      input: ["text", "image"],
      cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
      contextWindow: 200000,
      maxTokens: 16384
    }
  ]
});

// Override baseUrl de provider existente
pi.registerProvider("anthropic", {
  baseUrl: "https://proxy.example.com"
});
```

**OAuth support:**
```typescript
pi.registerProvider("corporate-ai", {
  baseUrl: "https://ai.corp.com",
  api: "openai-responses",
  models: [...],
  oauth: {
    name: "Corporate AI (SSO)",
    async login(callbacks) {
      callbacks.onAuth({ url: "https://sso.corp.com/..." });
      const code = await callbacks.onPrompt({ message: "Enter code:" });
      return { refresh: code, access: code, expires: Date.now() + 3600000 };
    },
    async refreshToken(credentials) {
      return credentials;
    },
    getApiKey(credentials) {
      return credentials.access;
    }
  }
});
```

### 7.5 API Keys

**Resolução de API keys (prioridade):**
1. Runtime overrides (via `setRuntimeApiKey`, não persistido)
2. Credenciais armazenadas em `auth.json` (API keys ou OAuth tokens)
3. Environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.)
4. Fallback resolver (para custom provider keys de `models.json`)

```typescript
// Runtime override (não persistido)
authStorage.setRuntimeApiKey("anthropic", "sk-my-temp-key");

// Custom auth location
const customAuth = AuthStorage.create("/my/app/auth.json");
const customRegistry = ModelRegistry.create(customAuth, "/my/app/models.json");
```

---

## 8. Estrutura de Arquivos e Pastas do Pi

### 8.1 Estrutura Global

```
~/.pi/
├── agent/
│   ├── extensions/              # Extensions globais
│   │   ├── my-extension.ts
│   │   └── multi-file-ext/
│   │       └── index.ts
│   ├── skills/                  # Skills globais
│   │   └── my-skill/
│   │       └── SKILL.md
│   ├── prompts/                 # Prompt templates globais
│   │   └── review.md
│   ├── themes/                  # Temas globais
│   │   ├── dark.ts
│   │   └── light.ts
│   ├── sessions/                # Sessões salvas
│   │   └── --<path>--/
│   │       └── <timestamp>_<uuid>.jsonl
│   ├── settings.json            # Settings globais
│   ├── auth.json                # Credenciais
│   ├── models.json              # Modelos custom
│   ├── keybindings.json         # Keybindings custom
│   └── AGENTS.md                # Context file global
└── packages/                    # Pi packages instalados
    ├── npm/
    └── git/
```

### 8.2 Estrutura de Projeto

```
project/
├── .pi/
│   ├── extensions/              # Extensions do projeto
│   │   └── project-ext.ts
│   ├── skills/                  # Skills do projeto
│   │   └── project-skill/
│   │       └── SKILL.md
│   ├── prompts/                 # Prompts do projeto
│   │   └── deploy.md
│   ├── themes/                  # Temas do projeto
│   │   └── project-theme.ts
│   ├── settings.json            # Settings do projeto (override global)
│   ├── SYSTEM.md                # Override system prompt
│   └── APPEND_SYSTEM.md         # Append ao system prompt
├── AGENTS.md                    # Context file do projeto
├── CLAUDE.md                    # Alias para AGENTS.md
└── package.json                 # Pi package manifest
```

### 8.3 Locais para Extensão

**Precedência de carregamento:**
1. Extensions via CLI `-e` (mais alta prioridade)
2. Extensions via `settings.json`
3. Extensions globais `~/.pi/agent/extensions/`
4. Extensions do projeto `.pi/extensions/`

**Auto-discovery:**
```
~/.pi/agent/extensions/
├── simple-extension.ts          # ✅ Carregado
├── multi-file-ext/
│   └── index.ts                 # ✅ Carregado
└── nested/
    └── deep/
        └── index.ts             # ❌ Não carregado (apenas 1 nível)
```

**Hot-reload:**
```
.pi/extensions/
└── my-extension.ts              # ✅ /reload recarrega

pi -e ./my-extension.ts         # ❌ Não hot-reloada
```

---

## 9. Plano de Implementação para Integração LiveKit

### 9.1 Visão Geral

**Objetivo:** Criar uma extensão do Pi que permite interação via voz usando LiveKit para transporte de áudio, Deepgram para STT, Cartesia para TTS, e o próprio Pi para geração de resposta.

**Arquitetura escolhida:** Pi Extension com LiveKit Client SDK (Arquitetura 3)

**MVP funcional:**
- ✅ Conexão a uma sala LiveKit
- ✅ Receber áudio do usuário
- ✅ Transcrever áudio para texto (Deepgram)
- ✅ Enviar texto para o Pi LLM
- ✅ Receber resposta do Pi
- ✅ Converter resposta para áudio (Cartesia)
- ✅ Enviar áudio de volta ao usuário
- ✅ Loop de conversação contínua
- ✅ UI para controle (start/stop, status)

**Fora do MVP:**
- ❌ Múltiplos participantes na sala
- ❌ Vídeo (apenas áudio)
- ❌ Gravação de sessões
- ❌ Análise de sentimentos
- ❌ Multi-idioma avançado

### 9.2 Componentes

**Componentes principais:**
1. `LiveKitClient` - Wrapper para LiveKit Client SDK
2. `STTManager` - Deepgram STT integration
3. `TTSManager` - Cartesia TTS integration
4. `SessionManager` - Voice session state
5. `VoiceChatTool` - Tool que o LLM chama
6. `UIComponents` - Custom UI for voice chat
7. `ConfigLoader` - Configuration from .env

**Estimativa de linhas:**
- `LiveKitClient`: ~300 linhas
- `STTManager`: ~250 linhas
- `TTSManager`: ~200 linhas
- `SessionManager`: ~300 linhas
- `VoiceChatTool`: ~200 linhas
- `UIComponents`: ~150 linhas
- `ConfigLoader`: ~150 linhas
- `index.ts` (main): ~100 linhas
- **Total: ~1650 linhas**

### 9.3 Fases de Implementação

**Fase 0: Preparação do ambiente (0.5 dia)**
- Configurar LiveKit Server local
- Obter API keys (Deepgram, Cartesia)
- Criar estrutura de arquivos
- Instalar dependências

**Fase 1: Tipos e Configuração (1 dia)**
- Definir TypeScript types
- Implementar ConfigLoader
- Criar .env template
- Testar carregamento de config

**Fase 2: LiveKitClient (1-2 dias)**
- Implementar conexão à sala
- Subscrever tracks de áudio
- Publicar tracks de áudio
- Gerenciar eventos (disconnected, etc.)

**Fase 3: STTManager - Deepgram (1 dia)**
- Implementar streaming STT
- Integrar com LiveKit audio tracks
- Gerenciar VAD (Voice Activity Detection)
- Testar transcrição

**Fase 4: TTSManager - Cartesia (1 dia)**
- Implementar streaming TTS
- Gerar áudio a partir de texto
- Testar qualidade de voz

**Fase 5: SessionManager (1 dia)**
- Gerenciar estado da sessão de voz
- Controlar estado (idle, listening, speaking, processing)
- Sincronizar com Pi session

**Fase 6: Voice Chat Tool (1-2 dias)**
- Implementar tool que LLM chama
- Integrar com SessionManager
- Gerenciar loop de conversação

**Fase 7: Integração Pi e Loop de Conversação (2 dias)**
- Implementar event listeners (message_update, message_end)
- Orquestrar STT → LLM → TTS pipeline
- Gerenciar interrupções e cancelamentos

**Fase 8: UI Integration (1 dia)**
- Implementar status widget
- Criar dialogs (join room, etc.)
- Adicionar keyboard shortcuts

**Fase 9: Error Handling e Edge Cases (1 dia)**
- Tratamento de erros de conexão
- Gerenciar timeouts
- Lidar com desconexões

**Fase 10: Documentação (1-2 dias)**
- Documentar instalação
- Criar exemplos de uso
- Escrever troubleshooting guide

**Fase 11: Testing e Validação (1-2 dias)**
- Testes unitários
- Testes de integração
- Testes manuais com LiveKit room

**Fase 12: Polish e Otimização (1 dia)**
- Otimizar latência
- Melhorar feedback visual
- Performance tuning

**Fase 13: Release Final (0.5 dia)**
- Criar release notes
- Publicar extension
- Atualizar README

**Cronograma estimado:** 12-15 dias

### 9.4 Riscos e Mitigações

**Riscos técnicos:**
1. **Latência alta no pipeline** → Streaming TTS, buffer optimization
2. **Memory leaks** → Proper cleanup, track disposal
3. **Race conditions** → Mutation queue, state synchronization
4. **Audio quality issues** → Codec tuning, sample rate matching
5. **Connection drops** → Reconnection logic, state recovery

**Riscos de integração Pi:**
1. **Tool execution blocking UI** → Streaming updates, background processing
2. **Session state corruption** → Proper branching support, state reconstruction
3. **Event handler conflicts** → Proper ordering, signal handling
4. **Memory growth** → Buffer limits, periodic cleanup
5. **/reload breaking state** → Proper session_start reconstruction

**Riscos de dependências:**
1. **LiveKit SDK breaking changes** → Pin version, monitor updates
2. **Deepgram API limits** → Rate limiting, error handling
3. **Cartesia API issues** → Fallback TTS, retry logic
4. **Node.js compatibility** → Target LTS, test on multiple versions
5. **Network restrictions** → Configurable ports, proxy support

---

## 10. Conclusões e Próximos Passos

### 10.1 Resumo da Pesquisa

**O que aprendemos sobre o Pi:**
- ✅ Arquitetura extensível com events, tools, e UI components
- ✅ Session management com tree structure para branching
- ✅ Built-in tools (read, write, edit, bash, grep, find, ls)
- ✅ SDK para integração programática
- ✅ Type-safe event handling com TypeBox schemas
- ✅ Custom TUI components para interfaces ricas
- ✅ Hot-reload de extensions, skills, prompts, themes

**O que aprendemos sobre LiveKit:**
- ✅ Server para transporte de áudio/vídeo via WebRTC
- ✅ Agents Framework para Python (mas podemos usar client SDK)
- ✅ Plugins para Deepgram STT e Cartesia TTS
- ✅ Streaming APIs para baixa latência
- ✅ VAD integrado para detecção de fala

### 10.2 Viabilidade da Integração

**Arquitetura recomendada:** Pi Extension com LiveKit Client SDK

**Por que essa arquitetura?**
- ✅ Controle total do pipeline STT → LLM → TTS
- ✅ Usa o próprio Pi como LLM (nenhuma necessidade de subprocess)
- ✅ TypeScript (mesma linguagem do Pi)
- ✅ Fácil debug e extensão
- ✅ Pode usar tools do Pi diretamente

**Desafios principais:**
- ⚠️ Latência no pipeline (mitigável com streaming)
- ⚠️ Sincronização de estado (mitigável com SessionManager)
- ⚠️ Memory management (mitigável com cleanup adequado)

### 10.3 Próximos Passos

**Imediato:**
1. Revisar e aprovar arquitetura proposta
2. Obter API keys validadas para Deepgram e Cartesia
3. Configurar LiveKit Server local para testes
4. Criar estrutura de arquivos da extension

**Curto prazo (1-2 semanas):**
1. Implementar Fases 0-5 (config, LiveKitClient, STT, TTS, SessionManager)
2. Testar pipeline individualmente
3. Criar tool básico de voice chat

**Médio prazo (3-4 semanas):**
1. Implementar Fases 6-9 (loop de conversação, UI, error handling)
2. Integração completa com o Pi
3. Testes end-to-end

**Longo prazo (1-2 meses):**
1. Implementar Fases 10-13 (documentação, testing, polish, release)
2. Publicar extension como Pi package
3. Coletar feedback e iterar

### 10.4 Referências

**Documentação do Pi:**
- Main README: `~/.pi/agent/README.md`
- Extensions: `~/.pi/agent/docs/extensions.md`
- SDK: `~/.pi/agent/docs/sdk.md`
- Session: `~/.pi/agent/docs/session.md`
- TUI: `~/.pi/agent/docs/tui.md`
- Examples: `~/.pi/agent/examples/extensions/`

**Documentação do LiveKit:**
- GitHub: https://github.com/livekit/livekit
- Agents: https://github.com/livekit/agents
- Client SDK JS: https://github.com/livekit/client-sdk-js
- Docs: https://docs.livekit.io

**API Keys fornecidas:**
- Deepgram: `5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3` (validar)
- Cartesia: `sk_car_d69NmtdJKVbTj8XrrqM4Nt` (validar)

**Data da pesquisa:** 2026-04-03
**Versão do Pi:** Latest (from README)
**Versão do LiveKit Agents:** 1.4.x

---

*Este documento é um guia completo para criação de extensões do Pi com foco na integração com LiveKit para voz.*
