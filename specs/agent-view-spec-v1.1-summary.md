# Agent View Spec v1.1 - Resumo de Correções

**Status:** CORREÇÕES DOCUMENTADAS  
**Data:** 2025-03-31  
**Arquivo Principal:** `specs/agent-view-spec.md`

---

## Resumo Executivo

O SPEC v1.1.0 contém correções críticas identificadas pelos especialistas em:
- Detecção universal de subprocessos (sem dependência de eventos customizados)
- Layout responsivo (fallback para terminals pequenos)
- Keybindings não-conflitantes
- Modo JSON para integração CLI
- Estrutura de arquivos otimizada

**Arquivo de documentação completa:** `specs/agent-view-spec-corrections.md`

---

## Lista de Correções por Seção

### ✅ 1. Cabeçalho e TOC (Linhas 1-29)

**Mudanças:**
- Versão: 1.0.0 → 1.1.0
- Adicionado campo "Updated: 2025-03-31"
- Table of Contents renumerada:
  - Nova seção 10: Modo JSON
  - Nova seção 11: Integração Universal (substitui "Integração com agent-team")
  - Seções 12-16 renumeradas

---

### ✅ 2. Mapeamento de Status (Seção 2.1, após linha 110)

**Adicionar:**
```typescript
/**
 * NOTA: Mapeamento para Pi subprocess status:
 * - "starting" → detectado via spawn (pré-execução)
 * - "running" → Pi agent em turn (message_start sem message_end)
 * - "waiting" → aguardando LLM/response
 * - "complete" → exitCode === 0
 * - "error" → exitCode !== 0
 * - "aborted" → signal.aborted === true
 * - "idle" → subprocess spawnado mas sem activity ainda
 */

// Função de mapeamento
function mapPiEventToStatus(event: {...}): AgentStatus {
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

### ✅ 3. Layout 1x8 Responsivo (Seção 4.6, linha ~606)

**Mudar:**
```diff
| 1x8    | 80        | 16         | 25% - 1   | 50% - 1   | 8          |
+ | 1x8    | 120       | 16         | 25% - 1   | 50% - 1   | 8          |
```

**Adicionar após a tabela:**
```typescript
**NOTA: Layout 1x8 requer terminal >= 120 cols.** Se terminal for menor, 
fallback automático para "list":

function getEffectiveLayout(
  requestedLayout: AgentLayout,
  terminalWidth: number
): AgentLayout {
  if (requestedLayout === "1x8" && terminalWidth < 120) {
    return "list"; // Fallback responsivo
  }
  return requestedLayout;
}
```

---

### ✅ 4. Keybindings Corrigidos (Seção 7.1, linha ~771)

**Mudar tabela:**
```diff
- | `Ctrl+A` | Toggle layout |
+ | `Ctrl+Shift+A` | Toggle layout |
- | `Ctrl+Q` / `Esc` | Close |
+ | `Ctrl+Shift+Q` | Close |
+ | `q` | Close | Fecha widget (estilo htop) |
```

**Adicionar nota:**
```typescript
**NOTA: Mudanças para evitar conflitos:**
- `Ctrl+A` → `Ctrl+Shift+A` (evita `cursorLineStart` do editor)
- `Esc` → `q` (evita `interrupt` do Pi)  
- `Ctrl+Q` → `Ctrl+Shift+Q` (evita `theme-cycler`)
```

**Seção 7.5 (linha ~895), mudar interface:**
```diff
interface KeybindingMap {
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
  
  filter: {
    "/": "enterFilterMode";
    "enter": "applyFilter";
-   "escape": "clearFilter";
+   "q": "clearFilter";
  };
}
```

---

### ✅ 5. Flags CLI (Nova Seção 9.3, após linha 1030)

**Adicionar após "### 9.2. Comandos de Configuração":**
```typescript
### 9.3. Flags CLI

```bash
# Flags adicionadas pelo Pi quando agent-view está ativo
pi --agent-view-layout=1x4
pi --agent-view-font=small
pi --agent-view-mode=auto   # auto | manual | never
```

**Integração com CLI:**

```typescript
// Extensão registra flags
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

// Uso na extensão
const layout = pi.getFlag("--agent-view-layout") as AgentLayout;
const font = pi.getFlag("--agent-view-font") as FontSize;
const mode = pi.getFlag("--agent-view-mode") as "auto" | "manual" | "never";
```
```

---

### ✅ 6. Nova Seção 10: Modo JSON (Inserir após linha ~1035)

**CONTEÚDO COMPLETO DA NOVA SEÇÃO:**
```markdown
## 10. Modo JSON

### 10.1. Comportamento em --mode json

Quando Pi roda em modo JSON (`--mode json`), o agent-view deve emitir eventos JSON estruturados em vez de renderizar widgets TUI.

### 10.2. Eventos JSON de Saída

```typescript
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
```

### 10.3. Exemplo de Saída JSON

```json
{"type":"agent_view","event":"start","timestamp":1711849280000,"data":{"workflowId":"wf-001","mode":"parallel","agents":4}}
{"type":"agent_view","event":"update","timestamp":1711849280500,"data":{"workflowId":"wf-001","agents":[{"id":"scout-1","name":"scout","status":"running","progress":15,"stats":{"turns":1,"inputTokens":800,"outputTokens":200}}]}}
{"type":"agent_view","event":"update","timestamp":1711849281000,"data":{"workflowId":"wf-001","agents":[{"id":"scout-1","name":"scout","status":"complete","progress":100,"stats":{"turns":3,"inputTokens":1200,"outputTokens":800}}]}}
{"type":"agent_view","event":"end","timestamp":1711849285000,"data":{"workflowId":"wf-001","summary":{"totalAgents":4,"successful":4,"totalCost":0.0234}}}
```

### 10.4. Detecção de Modo JSON

```typescript
function isJSONMode(pi: ExtensionAPI): boolean {
  // Detecta se Pi está em modo JSON
  return process.argv.includes("--mode") && 
         process.argv.includes("json");
}

class AgentMonitor {
  constructor(private pi: ExtensionAPI) {
    this.jsonMode = isJSONMode(pi);
  }
  
  emitUpdate(data: AgentViewUpdateData): void {
    if (this.jsonMode) {
      // Emite JSON para stdout
      console.log(JSON.stringify({
        type: "agent_view",
        event: "update",
        timestamp: Date.now(),
        data
      }));
    } else {
      // Emite evento interno para TUI
      this.pi.events.emit("agent_view:update", {
        type: "agent_view:update",
        agents: data.agents,
        timestamp: Date.now()
      });
    }
  }
}
```
```

---

### ✅ 7. Nova Seção 11: Integração Universal (Substituir seção 10 atual)

**LOCALIZAÇÃO:** Substituir conteúdo de "## 10. Integração com agent-team" em diante

**CONTEÚDO RESUMIDO:**
```markdown
## 11. Integração Universal

### 11.1. Abordagem de Detecção Universal

**PROBLEMA:** Dependência de eventos `agent_team:*` limita extensão.

**SOLUÇÃO:** Hook em `spawn()` + padrão de argumentos Pi.

### 11.2. Padrão de Detecção

Subprocessos Pi usam este padrão:
```bash
pi --mode json -p --no-extensions \
   --append-system-prompt /tmp/prompt-AGENT_NAME.md \
   "Task: ..."
```

**Características:**
- `--mode json` → subprocesso não-interativo
- `--no-extensions` → isolamento
- `--append-system-prompt` → contém nome do agente

### 11.3. Hook em spawn()

```typescript
const originalSpawn = spawn;
spawn = function(command: string, args: string[], options: any) {
  if (command === "pi" && isAgentSubprocess(args)) {
    const agentInfo = extractAgentInfo(args);
    pi.events.emit("subagent:spawn", {...agentInfo});
    
    const proc = originalSpawn.call(this, command, args, options);
    pi.events.emit("subagent:spawn", {...agentInfo, pid: proc.pid});
    
    return proc;
  }
  return originalSpawn.call(this, command, args, options);
};

function isAgentSubprocess(args: string[]): boolean {
  return args.includes("--mode") && args.includes("json") &&
         args.includes("--no-extensions");
}
```

### 11.4. Compatibilidade

| Orquestrador | Compatível | Notas |
|--------------|------------|-------|
| agent-team   | ✅ | Usa padrão esperado |
| agent-chain  | ✅ | Usa padrão esperado |
| pi-pi        | ✅ | Usa padrão esperado |
| subagent-widget | ✅ | Usa padrão esperado |
| subagent     | ✅ | Usa padrão esperado |
| Custom       | ✅ | Se seguir padrão |

### 11.5. Eventos Universais

```typescript
interface UniversalSubagentEvents {
  "subagent:spawn": {
    agentId: string;
    agentName: string;
    task: string;
    pid: number | null;
  };
  
  "subagent:output": {
    agentId: string;
    output: string;
    timestamp: number;
  };
  
  "subagent:complete": {
    agentId: string;
    exitCode: number;
    duration: number;
  };
}
```
```

---

### ✅ 8. Estrutura de Arquivos (Seção 13.1, linha ~1150)

**Mudar para:**
```diff
### 13.1. Estrutura de Arquivos

- Arquivos (5):
-   - index.ts (150 linhas)
-   - monitor.ts (200 linhas)
-   - widget.ts (400 linhas)
-   - renderer.ts (300 linhas)
-   - state.ts (150 linhas)
+ Arquivos (3):
+   - index.ts (200 linhas) - Entry point, registro de comandos/flags
+   - monitor.ts (250 linhas) - Detecção universal, hook de spawn
+   - widget.ts (500 linhas) - TUI components, renderização, layout
```

---

### ✅ 9. Correções de Renderização (Seção 14, após linha ~1250)

**Adicionar novas subseções:**

**14.5. Truncamento Responsivo**
```typescript
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
```

**14.6. AutoRefreshManager com Cleanup**
```typescript
class AutoRefreshManager {
  private intervalId?: NodeJS.Timeout;
  
  start(refreshInterval: number): void {
    this.stop(); // Limpa anterior
    this.intervalId = setInterval(() => this.refresh(), refreshInterval);
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

## Arquivos Criados

1. **agent-view-spec.md** - Especificação principal (deve ser atualizado manualmente)
2. **agent-view-spec-corrections.md** - Documentação completa das correções
3. **agent-view-spec.v1.0** - Backup da versão original
4. **apply-spec-corrections.sh** - Script de aplicação automática (parcial)

---

## Próximos Passos

1. ✅ Documentação de correções criada
2. ⏳ Aplicar correções ao SPEC principal manualmente ou via editor
3. ⏳ Atualizar diagramas ASCII com novos keybindings
4. ⏳ Adicionar exemplos de detecção universal
5. ⏳ Revisar e validar consistência completa

---

**Fim do Resumo v1.1**
