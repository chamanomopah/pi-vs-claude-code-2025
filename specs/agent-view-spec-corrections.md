# Agent View Spec - Correções Críticas v1.1.0

**Data:** 2025-03-31  
**Versão Original:** 1.0.0  
**Versão Atualizada:** 1.1.0

---

## Resumo das Alterações

### 1. Atualização de Versão

**ARQUIVO:** `agent-view-spec.md` (linhas 1-29)

**MUDANÇA:**
```diff
- **Version:** 1.0.0
+ **Version:** 1.1.0
+ **Updated:** 2025-03-31

## Table of Contents
- 10. [Integração com agent-team](#10-integração-com-agent-team)
+ 10. [Modo JSON](#10-modo-json)
+ 11. [Integração Universal](#11-integração-universal)
- 11. [Exemplo de Uso](#11-exemplo-de-uso)
+ 12. [Exemplo de Uso](#12-exemplo-de-uso)
- 12. [Componentes TUI](#12-componentes-tui)
+ 13. [Componentes TUI](#13-componentes-tui)
- 13. [Fluxo de Renderização](#13-fluxo-de-renderização)
+ 14. [Fluxo de Renderização](#14-fluxo-de-renderização)
- 14. [Persistência de Estado](#14-persistência-de-estado)
+ 15. [Persistência de Estado](#15-persistência-de-estado)
- 15. [Tratamento de Erros](#15-tratamento-de-erros)
+ 16. [Tratamento de Erros](#16-tratamento-de-erros)
```

---

### 2. Mapeamento de Status (Seção 2)

**ARQUIVO:** `agent-view-spec.md` (linhas ~100-120)

**MUDANÇA:**
```typescript
/**
 * Estados possíveis do agente
 * 
 * NOTA: Mapeamento para Pi subprocess status:
 * - "starting" → detectado via spawn (pré-execução)
 * - "running" → Pi agent em turn (message_start sem message_end)
 * - "waiting" → aguardando LLM/response
 * - "complete" → exitCode === 0
 * - "error" → exitCode !== 0
 * - "aborted" → signal.aborted === true
 * - "idle" → subprocess spawnado mas sem activity ainda
 */
type AgentStatus =
  | "idle"          // Aguardando início
  | "starting"      // Iniciando subprocesso
  | "running"       // Executando (em turn)
  | "waiting"       // Aguardando input/LLM
  | "complete"      // Completou com sucesso
  | "error"         // Erro fatal
  | "aborted";      // Cancelado pelo usuário

/**
 * Mapeia eventos do subprocesso Pi para AgentStatus
 */
function mapPiEventToStatus(event: {
  type: string;
  exitCode?: number;
  streaming?: boolean;
}): AgentStatus {
  if (event.type === "process_start") return "starting";
  if (event.type === "agent_start") return "running";
  if (event.streaming === true && event.type === "turn_end") return "waiting";
  if (event.type === "agent_end") {
    if (event.exitCode === 0) return "complete";
    return "error";
  }
  return "idle";
}
```

---

### 3. Layout 1x8 com Fallback Responsivo (Seção 4.6)

**ARQUIVO:** `agent-view-spec.md` (linha ~606)

**MUDANÇA:**
```diff
### 4.6. Tabela de Dimensões por Terminal

| Layout | Min Width | Min Height | Cols/Pane | Rows/Pane | Max Agents |
|--------|-----------|------------|-----------|-----------|------------|
| 1x1    | 40        | 10         | 100%      | 100%      | 1          |
| 1x2    | 60        | 12         | 50% - 1   | 100%      | 2          |
| 1x4    | 80        | 14         | 50% - 1   | 50% - 1   | 4          |
- | 1x8    | 80        | 16         | 25% - 1   | 50% - 1   | 8          |
+ | 1x8    | 120       | 16         | 25% - 1   | 50% - 1   | 8          |
| list   | 40        | 10         | 100%      | scroll    | unlimited  |

+ **NOTA: Layout 1x8 requer terminal >= 120 cols.** Se terminal for menor, fallback automático para "list":
+ 
+ ```typescript
+ function getEffectiveLayout(
+   requestedLayout: AgentLayout,
+   terminalWidth: number
+ ): AgentLayout {
+   if (requestedLayout === "1x8" && terminalWidth < 120) {
+     return "list"; // Fallback responsivo
+   }
+   return requestedLayout;
+ }
+ ```
```

---

### 4. Correção de Keybindings (Seção 7.1 e 7.5)

**ARQUIVO:** `agent-view-spec.md` (linhas ~775 e ~880)

**MUDANÇA:**
```diff
### 7.1. Atalhos Globais

| Key | Action | Description |
|-----|--------|-------------|
- | `Ctrl+A` | Toggle layout | Cicla: 1x1 → 1x2 → 1x4 → 1x8 → list → 1x1 |
+ | `Ctrl+Shift+A` | Toggle layout | Cicla: 1x1 → 1x2 → 1x4 → 1x8 → list → 1x1 |
| `Ctrl+F` | Cycle font | Cicla: small → medium → large → small |
| `Ctrl+H` | Cycle header | Cicla: minimal → detailed → compact → minimal |
| `Ctrl+S` | Toggle sort | Alterna: default ↔ active |
| `Ctrl+R` | Refresh | Força atualização manual |
- | `Ctrl+Q` / `Esc` | Close | Fecha widget agent-view |
+ | `Ctrl+Shift+Q` | Close | Fecha widget agent-view |
+ | `q` | Close | Fecha widget agent-view (estilo htop) |
| `Ctrl+O` | Expand | Expande agente selecionado (1x1) |

+ **NOTA: Mudanças de keybinding para evitar conflitos:**
+ - `Ctrl+A` → `Ctrl+Shift+A` (evita conflito com `cursorLineStart` do editor)
+ - `Esc` → `q` (evita conflito com `interrupt` do Pi)
+ - `Ctrl+Q` → `Ctrl+Shift+Q` (evita conflito com `theme-cycler`)
```

**E na seção 7.5:**
```diff
interface KeybindingMap {
  // Todos os layouts
  global: {
-   "ctrl+a": "toggleLayout";
+   "ctrl+shift+a": "toggleLayout";
    "ctrl+f": "cycleFont";
    "ctrl+h": "cycleHeader";
    "ctrl+s": "toggleSort";
    "ctrl+r": "refresh";
-   "ctrl+q": "close";
-   "escape": "close";
+   "ctrl+shift+q": "close";
+   "q": "close";
  };
  
  // Modo filtro
  filter: {
    "/": "enterFilterMode";
    "enter": "applyFilter";
-   "escape": "clearFilter";
+   "q": "clearFilter";
  };
}
```

---

### 5. Nova Seção 10: Modo JSON

**NOVA SEÇÃO** após a seção 9 (Configuração)

**CONTEÚDO:**
```typescript
## 10. Modo JSON

### 10.1. Comportamento em --mode json

Quando Pi roda em modo JSON (`--mode json`), o agent-view deve emitir eventos JSON estruturados em vez de renderizar widgets TUI.

### 10.2. Eventos JSON de Saída

interface AgentViewJSONEvent {
  type: "agent_view";
  event: "update" | "start" | "end" | "error";
  timestamp: number;
  data: AgentViewUpdateData | AgentViewStartData | AgentViewEndData | AgentViewErrorData;
}

interface AgentViewUpdateData {
  workflowId: string;
  agents: Array<{
    id: string;
    name: string;
    status: AgentStatus;
    progress: number;
    stats: AgentStats;
  }>;
  orchestrator: {
    type: "subagent" | "agent-team" | "universal";
    mode: "single" | "parallel" | "chain";
  };
}

### 10.3. Exemplo de Saída JSON

{"type":"agent_view","event":"start","timestamp":1711849280000,"data":{"workflowId":"wf-001","mode":"parallel","agents":4}}
{"type":"agent_view","event":"update","timestamp":1711849280500,"data":{"workflowId":"wf-001","agents":[{"id":"scout-1","status":"running","progress":15}]}}
{"type":"agent_view","event":"end","timestamp":1711849285000,"data":{"workflowId":"wf-001","summary":{"totalAgents":4,"successful":4}}}

### 10.4. Detecção de Modo JSON

function isJSONMode(pi: ExtensionAPI): boolean {
  return process.argv.includes("--mode") && 
         process.argv.includes("json");
}

class AgentMonitor {
  emitUpdate(data: AgentViewUpdateData): void {
    if (this.jsonMode) {
      console.log(JSON.stringify({
        type: "agent_view",
        event: "update",
        timestamp: Date.now(),
        data
      }));
    } else {
      this.pi.events.emit("agent_view:update", {...});
    }
  }
}
```

---

### 6. Nova Seção 11: Integração Universal

**SUBSTITUI** a seção 10 (Integração com agent-team)

**CONTEÚDO PRINCIPAL:**
```typescript
## 11. Integração Universal

### 11.1. Abordagem de Detecção Universal

**PROBLEMA:** Dependência de eventos customizados (`agent_team:*`) limita a extensão.

**SOLUÇÃO:** Detecção universal via hook em `spawn()` + padrão de argumentos.

### 11.2. Padrão de Detecção

Agentes Pi spawnados compartilham este padrão:

pi --mode json -p --no-extensions \
   --append-system-prompt /tmp/prompt-AGENT_NAME.md \
   "Task: ..."

**Características detectáveis:**
1. `--mode json`
2. `-p` ou `--print`
3. `--no-extensions`
4. `--append-system-prompt` com nome do agente

### 11.3. Hook em spawn()

const originalSpawn = spawn;
spawn = function(command: string, args: string[], options: any) {
  if (command === "pi" && isAgentSubprocess(args)) {
    const agentInfo = extractAgentInfo(args);
    
    pi.events.emit("subagent:spawn", {
      agentId: agentInfo.name,
      agentName: agentInfo.name,
      task: agentInfo.task,
      pid: null
    });
    
    const proc = originalSpawn.call(this, command, args, options);
    pi.events.emit("subagent:spawn", {...agentInfo, pid: proc.pid});
    
    return proc;
  }
  
  return originalSpawn.call(this, command, args, options);
};

### 11.4. Compatibilidade

| Orquestrador | Compatível | Notas |
|--------------|------------|-------|
| agent-team   | ✅ | Usa padrão esperado |
| agent-chain  | ✅ | Usa padrão esperado |
| pi-pi        | ✅ | Usa padrão esperado |
| subagent-widget | ✅ | Usa padrão esperado |
| subagent (original) | ✅ | Usa padrão esperado |
| Custom       | ✅ | Se seguir padrão |
```

---

### 7. Flags CLI Adicionais (Seção 9.3)

**NOVA SUBSEÇÃO** na seção 9

**CONTEÚDO:**
```typescript
### 9.3. Flags CLI

pi --agent-view-layout=1x4
pi --agent-view-font=small
pi --agent-view-mode=auto   # auto | manual | never

// Registro na extensão
pi.registerFlag("agent-view-layout", {
  description: "Layout inicial do agent-view",
  type: "string",
  enum: ["1x1", "1x2", "1x4", "1x8", "list"],
  default: "1x4"
});

pi.registerFlag("agent-view-font", {
  description: "Tamanho de fonte do agent-view",
  type: "string",
  enum: ["small", "medium", "large"],
  default: "medium"
});

pi.registerFlag("agent-view-mode", {
  description: "Modo de abertura do agent-view",
  type: "string",
  enum: ["auto", "manual", "never"],
  default: "auto"
});
```

---

### 8. Estrutura de Arquivos Consolidada (Seção 13)

**ARQUIVO:** `agent-view-spec.md` (seção Componentes TUI)

**MUDANÇA:**
```diff
### 13.1. Hierarquia de Componentes

- AgentViewWidget (Container)
├── WidgetHeader
├── LayoutContainer
│   └── AgentPane[] (Box)
└── WidgetFooter

- Arquivos:
  - index.ts (150 linhas)
  - monitor.ts (200 linhas)
  - widget.ts (400 linhas)
  - renderer.ts (300 linhas)
  - state.ts (150 linhas)

+ AgentViewWidget (Container)
+ ├── WidgetHeader
+ ├── LayoutContainer
+ │   └── AgentPane[] (Box)
+ └── WidgetFooter
+ 
+ Arquivos:
+ - index.ts (200 linhas) - Entry point, registro de comandos/flags
+ - monitor.ts (250 linhas) - Detecção universal, hook de spawn
+ - widget.ts (500 linhas) - TUI components, renderização
```

---

### 9. Correções de Renderização (Seção 14)

**ARQUIVO:** `agent-view-spec.md` (seção Fluxo de Renderização)

**ADIÇÕES:**
```typescript
### 14.5. Truncamento Responsivo

// Usar visibleWidth() e truncateToWidth() do TUI
import { visibleWidth, truncateToWidth } from "@mariozechner/pi-tui";

class AgentPane extends Box {
  renderContent(theme: Theme): void {
    const maxWidth = this.visibleWidth - 4; // padding
    
    for (const msg of this.agent.messages) {
      const truncated = truncateToWidth(msg.content, maxWidth);
      this.addChild(new Text(truncated, 0, 0));
    }
  }
}

### 14.6. AutoRefreshManager com Cleanup

class AutoRefreshManager {
  private intervalId?: NodeJS.Timeout;
  
  start(refreshInterval: number): void {
    this.stop(); // Limpa anterior se existir
    
    this.intervalId = setInterval(() => {
      this.refresh();
    }, refreshInterval);
  }
  
  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = undefined;
    }
  }
  
  dispose(): void {
    this.stop();
  }
}

// Uso na extensão
pi.on("session_shutdown", () => {
  refreshManager.dispose();
});
```

---

## Checklist de Implementação

- [x] Atualizar versão para 1.1.0
- [x] Adicionar mapeamento de status (Seção 2)
- [x] Atualizar layout 1x8 com fallback (Seção 4.6)
- [x] Corrigir keybindings conflitantes (Seção 7)
- [x] Adicionar seção Modo JSON (nova Seção 10)
- [x] Substituir Integração por Integração Universal (nova Seção 11)
- [x] Adicionar flags CLI (Seção 9.3)
- [x] Consolidar estrutura de arquivos (Seção 13)
- [x] Adicionar correções de renderização (Seção 14)

---

## Próximos Passos

1. Aplicar estas correções ao arquivo principal `agent-view-spec.md`
2. Revisar diagramas ASCII para refletir novos keybindings
3. Adicionar exemplos de uso da detecção universal
4. Documentar casos de teste para each orquestrador compatível
