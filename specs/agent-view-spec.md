# Agent View Extension - Complete Specification

**Version:** 1.1.0  
**Author:** Pi Pi Team  
**Status:** Draft  
**Created:** 2025-03-31  
**Updated:** 2025-03-31

---

## Table of Contents

1. [Visão Geral e Objetivos](#1-visão-geral-e-objetivos)
2. [Estrutura de Dados](#2-estrutura-de-dados)
3. [Comportamento de Ordenação](#3-comportamento-de-ordenação)
4. [Layouts e Dimensões](#4-layouts-e-dimensões)
5. [Tamanhos de Fonte](#5-tamanhos-de-fonte)
6. [Estilos de Header](#6-estilos-de-header)
7. [Atalhos de Teclado](#7-atalhos-de-teclado)
8. [Eventos e Monitoramento](#8-eventos-e-monitoramento)
9. [Configuração](#9-configuração)
10. [Modo JSON](#10-modo-json)
11. [Integração Universal](#11-integração-universal)
12. [Exemplo de Uso](#12-exemplo-de-uso)
13. [Componentes TUI](#13-componentes-tui)
14. [Fluxo de Renderização](#14-fluxo-de-renderização)
15. [Persistência de Estado](#15-persistência-de-estado)
16. [Tratamento de Erros](#16-tratamento-de-erros)

---

## 1. Visão Geral e Objetivos

### 1.1. Propósito

A extensão **Agent View** fornece uma visualização em tempo real de múltiplos agentes Pi em execução, permitindo monitorar subagentes orquestrados pela ferramenta `subagent` (ou extensão `agent-team`).

### 1.2. Objetivos Principais

1. **Visibilidade:** Mostrar todos os agentes ativos com seus estados em tempo real
2. **Comparação:** Permitir comparar outputs de diferentes agentes lado a lado
3. **Orquestração Visual:** Facilitar entender fluxos complexos (parallel, chain)
4. **Eficiência:** Display compacto sem sobrecarregar a UI
5. **Customizável:** Múltiplos layouts, estilos e tamanhos

### 1.3. Casos de Uso

```
┌─────────────────────────────────────────────────────────┐
│ Caso 1: Parallel Execution                              │
│ 4 agentes scout rodando em paralelo                     │
│ → Ver progresso de todos simultaneamente                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Caso 2: Chain Workflow                                  │
│ scout → planner → builder → reviewer                   │
│ → Ver output de cada etapa sequencialmente             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Caso 3: Single Agent com Debug                          │
│ Acompanhar tool calls e streaming de um agente específico│
└─────────────────────────────────────────────────────────┘
```

### 1.4. Integração com Sistema Pi

```
Pi Main Session
    │
    ├── TUI (blessed/terminal)
    │   └── Agent View Widget (POSIX) ← NOSSA EXTENSÃO
    │
    ├── Extensions
    │   ├── agent-team (orquestra subagentes)
    │   ├── subagent (ferramenta de orquestração)
    │   └── agent-view (NOSSA EXTENSÃO)
    │
    └── Event Bus
        └── agent_view:update ← Consumido por nós
```

---

## 2. Estrutura de Dados

### 2.1. Interfaces TypeScript Principais

```typescript
/**
 * Estado de um único agente
 */
interface AgentState {
  /** Identificador único do agente (ex: "scout-1") */
  id: string;
  
  /** Nome base do agente (ex: "scout") */
  name: string;
  
  /** Estado atual */
  status: AgentStatus;
  
  /** Tarefa atual do agente */
  task: string;
  
  /** Mensagens/outputs do agente */
  messages: AgentMessage[];
  
  /** Estatísticas de uso */
  stats: AgentStats;
  
  /** Metadados */
  metadata: AgentMetadata;
}

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

/**
 * Mensagem do agente
 */
interface AgentMessage {
  type: "text" | "tool_call" | "tool_result" | "error";
  content: string;
  timestamp: number;
  toolName?: string;
  toolArgs?: Record<string, unknown>;
}

/**
 * Estatísticas do agente
 */
interface AgentStats {
  /** Número de turns completados */
  turns: number;
  
  /** Tokens de input consumidos */
  inputTokens: number;
  
  /** Tokens de output gerados */
  outputTokens: number;
  
  /** Custo estimado em USD */
  cost: number;
  
  /** Tempo desde o início (ms) */
  elapsed: number;
  
  /** Porcentagem de progresso (0-100) */
  progress: number;
}

/**
 * Metadados do agente
 */
interface AgentMetadata {
  /** Modelo sendo usado (ex: "claude-sonnet-4-5") */
  model?: string;
  
  /** Scope do agente ("user" | "project") */
  scope: "user" | "project";
  
  /** Arquivo de definição (.md) */
  definitionPath?: string;
  
  /** Workflow pai (se aplicável) */
  workflowId?: string;
  
  /** Índice no workflow (para chains) */
  stepIndex?: number;
}
```

### 2.2. Estado Global do Widget

```typescript
/**
 * Configuração do widget Agent View
 */
interface AgentViewConfig {
  /** Layout atual */
  layout: AgentLayout;
  
  /** Tamanho da fonte */
  fontSize: FontSize;
  
  /** Estilo do header */
  headerStyle: HeaderStyle;
  
  /** Modo de ordenação */
  sortOrder: SortOrder;
  
  /** Mostra/esconde stats */
  showStats: boolean;
  
  /** Mostra/esconde metadados */
  showMetadata: boolean;
  
  /** Atualização automática (ms) */
  refreshInterval: number;
  
  /** Filtros ativos */
  filters: AgentFilters;
}

/**
 * Layouts disponíveis */
type AgentLayout =
  | "1x1"   // Um agente grande
  | "1x2"   // Dois agentes lado a lado
  | "1x4"   // Quatro agentes em grid 2x2
  | "1x8"   // Oito agentes em grid 4x2
  | "list"; // Lista vertical (scroll)

/**
 * Tamanhos de fonte */
type FontSize = "small" | "medium" | "large";

/**
 * Estilos de header */
type HeaderStyle = "minimal" | "detailed" | "compact";

/**
 * Modos de ordenação */
type SortOrder = "default" | "active";

/**
 * Filtros de agentes */
interface AgentFilters {
  /** Filtra por status */
  status?: AgentStatus[];
  
  /** Filtra por nome (regex) */
  name?: string;
  
  /** Filtra por workflow */
  workflow?: string;
}
```

### 2.3. Eventos do Sistema

```typescript
/**
 * Evento de atualização de agente
 */
interface AgentViewUpdateEvent {
  type: "agent_view:update";
  
  /** Lista de todos os agentes */
  agents: AgentState[];
  
  /** Timestamp da atualização */
  timestamp: number;
  
  /** ID do workflow (se aplicável) */
  workflowId?: string;
  
  /** Metadados do orquestrador */
  orchestrator: {
    type: "subagent" | "agent-team";
    mode: "single" | "parallel" | "chain";
    totalAgents: number;
  };
}

/**
 * Evento de ciclo de vida
 */
interface AgentViewLifecycleEvent {
  type: "agent_view:start" | "agent_view:end" | "agent_view:error";
  
  /** ID do workflow/orquestração */
  workflowId: string;
  
  /** Configuração usada */
  config?: AgentViewConfig;
  
  /** Erro (se aplicável) */
  error?: string;
}
```

---

## 3. Comportamento de Ordenação

### 3.1. Modo "default" (Ordenação por Inserção)

**Comportamento:** Agentes mantêm a ordem em que foram criados.

```
┌──────────────────────────────────────────────────────────┐
│ Layout: 1x4, Sort: default                               │
├──────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │ scout-1  │ │ scout-2  │ │ planner  │ │ builder  │     │
│ │ running  │ │ complete │ │ running  │ │ idle     │     │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│   1º criado   2º criado   3º criado   4º criado        │
└──────────────────────────────────────────────────────────┘
```

**Quando usar:**
- Workflows sequenciais (chain) onde a ordem importa
- Debug de fluxo específico
- Preservação de timeline

### 3.2. Modo "active" (Ordenação por Atividade)

**Comportamento:** Agentes ativos primeiro, ordenados por:
1. Status (running > waiting > idle > complete > error > aborted)
2. Progresso (maior primeiro)
3. Tempo de início (mais recente primeiro)

```
┌──────────────────────────────────────────────────────────┐
│ Layout: 1x4, Sort: active                                │
├──────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │ planner  │ │ scout-2  │ │ scout-1  │ │ builder  │     │
│ │ running  │ │ waiting  │ │ running  │ │ idle     │     │
│ │  75%     │ │  100%    │ │  30%     │ │  0%      │     │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│   ativo       completo     ativo       parado           │
│   prior.      prior.       prior.      fim              │
└──────────────────────────────────────────────────────────┘

Ordem interna (running):
1. planner (75% progress, mais recente)
2. scout-1 (30% progress)
```

**Diagrama de Decisão:**

```
                    Início
                      │
                      ▼
            ┌─────────────────┐
            │ Coleta agentes  │
            └────────┬────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │ Separa por buckets:    │
        │ - running (por progress│
        │ - waiting             │
        │ - idle                │
        │ - complete            │
        │ - error               │
        │ - aborted             │
        └────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │ Ordena cada bucket:    │
        │ 1. Progresso (desc)    │
        │ 2. Timestamp (desc)    │
        └────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │ Concatena buckets:     │
        │ running → waiting →    │
        │ idle → complete → ...  │
        └────────┬───────────────┘
                 │
                 ▼
              Display
```

**Quando usar:**
- Execuções paralelas (monitorar os que estão trabalhando)
- Quer ver progresso geral
- Muitos agentes, foco nos ativos

### 3.3. Algoritmo de Ordenação (Implementação)

```typescript
function sortAgents(
  agents: AgentState[],
  mode: "default" | "active"
): AgentState[] {
  if (mode === "default") {
    // Ordena por timestamp de criação
    return [...agents].sort((a, b) => {
      const aTime = a.metadata.workflowId ? 
        getWorkflowStartTime(a.metadata.workflowId) : 0;
      const bTime = b.metadata.workflowId ?
        getWorkflowStartTime(b.metadata.workflowId) : 0;
      return aTime - bTime;
    });
  }
  
  // Mode "active"
  const statusPriority: Record<AgentStatus, number> = {
    running: 0,
    waiting: 1,
    idle: 2,
    complete: 3,
    error: 4,
    aborted: 5,
  };
  
  return [...agents].sort((a, b) => {
    // 1. Por status
    const statusDiff = statusPriority[a.status] - statusPriority[b.status];
    if (statusDiff !== 0) return statusDiff;
    
    // 2. Por progresso (dentro do mesmo status)
    const progressDiff = b.stats.progress - a.stats.progress;
    if (progressDiff !== 0) return progressDiff;
    
    // 3. Por timestamp (mais recente primeiro)
    return b.stats.elapsed - a.stats.elapsed;
  });
}
```

---

## 4. Layouts e Dimensões

### 4.1. Layout 1x1 (Single Agent)

**Uso:** Foco em um único agente com máximo detalhe.

```
┌─────────────────────────────────────────────────────────────┐
│ ╔═════════════════════════════════════════════════════════╗ │
│ ║ Agent: scout-1                            [running] ⏳   ║ │
│ ║ Task: Explore authentication code                       ║ │
│ ║                                                         ║ │
│ ║ ┌─────────────────────────────────────────────────────┐ ║ │
│ ║ │ Output:                                              │ ║ │
│ ║ │                                                      │ ║ │
│ ║ │ → grep "auth" src/                                  │ ║ │
│ ║ │   Found 12 matches in 4 files                       │ ║ │
│ ║ │                                                      │ ║ │
│ ║ │ → read src/auth/login.ts                            │ ║ │
│ ║ │   [file content...]                                 │ ║ │
│ ║ │                                                      │ ║ │
│ ║ │ Analyzing dependencies...                           │ ║ │
│ ║ │                                                      │ ║ │
│ ║ └─────────────────────────────────────────────────────┘ ║ │
│ ║                                                         ║ │
│ ║ Stats: 3 turns | ↑1.2k ↓3.4k | $0.0234 | 45% | 12s     ║ │
│ ╚═════════════════════════════════════════════════════════╝ │
└─────────────────────────────────────────────────────────────┘

Dimensões (terminal 80x24):
  Width: 76 cols (margem de 2)
  Height: 22 rows (header + stats)
  Content area: ~74x18
```

### 4.2. Layout 1x2 (Side by Side)

**Uso:** Comparar dois agentes ou ver pair em parallel.

```
┌───────────────────────────────────────────────────────────────┐
│ ╔═════════════════════╗ ╔═══════════════════════════════════╗ │
│ ║ scout-1 [running]   ║ ║ scout-2 [running]                 ║ │
│ ╠═════════════════════╣ ╠═══════════════════════════════════╣ │
│ ║ → grep "models"     ║ ║ → grep "controllers"             ║ │
│ ║   8 files found     ║ ║   15 files found                  ║ │
│ ║                     ║ ║                                   ║ │
│ ║ → read src/models/  ║ ║ → read src/controllers/          ║ │
│ ║   user.ts           ║ ║   auth.controller.ts              ║ │
│ ║   [content...]      ║ ║   [content...]                    ║ │
│ ║                     ║ ║                                   ║ │
│ ║ Processing...       ║ ║ Analyzing structure...            ║ │
│ ║                     ║ ║                                   ║ │
│ ╠═════════════════════╣ ╠═══════════════════════════════════╣ │
│ ║ ↑800 ↓1.2k 30%     ║ ║ ↑1.1k ↓2.3k 60%                  ║ │
│ ╚═════════════════════╝ ╚═══════════════════════════════════╝ │
└───────────────────────────────────────────────────────────────┘

Dimensões (terminal 80x24):
  Pane width: 37 cols
  Pane height: 20 rows
  Gap: 2 cols
```

### 4.3. Layout 1x4 (Grid 2x2)

**Uso:** Monitorar 4 agentes simultaneamente.

```
┌─────────────────────────────────────────────────────────────────┐
│ ╔═════════════╗ ╔═════════════╗ ╔═════════════╗ ╔═════════════╗│
│ ║ scout [⏳]  ║ ║ planner [⏳]║ ║ builder[⏳] ║ ║ reviewer[⏳]║│
│ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣│
│ ║ → grep      ║ ║ Analyzing   ║ ║ Waiting... ║ ║ → read src/ ││
│ ║   12 files  ║ ║ scout data  ║ ║             ║ ║   auth.ts   ││
│ ║             ║ ║             ║ ║             ║ ║             ││
│ ║ → read      ║ ║ Creating    ║ ║             ║ ║ Checking... ││
│ ║   models/   ║ ║ plan...     ║ ║             ║ ║             ││
│ ║             ║ ║             ║ ║             ║ ║             ││
│ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣│
│ ║ 45%  ↑↓3.2k ║ ║ 30%  ↑↓1.8k ║ ║ 0%   ↑↓0    ║ ║ 15% ↑↓400  ║│
│ ╚═════════════╝ ╚═════════════╝ ╚═════════════╝ ╚═════════════╝│
└─────────────────────────────────────────────────────────────────┘

Dimensões (terminal 80x24):
  Pane width: 18 cols
  Pane height: 12 rows
  Gap: 2 cols (horizontal), 1 row (vertical)
```

### 4.4. Layout 1x8 (Grid 4x2)

**Uso:** Monitorar muitos agentes em paralelo.

```
┌──────────────────────────────────────────────────────────────────┐
│ ╔═════╗ ╔═════╗ ╔═════╗ ╔═════╗ ╔═════╗ ╔═════╗ ╔═════╗ ╔═════╗│
│ ║s1⏳ ║ ║s2✓ ║ ║s3⏳ ║ ║s4⏳ ║ ║s5✓ ║ ║s6⏳ ║ ║s7⏳ ║ ║s8⏳ ║│
│ ╠═════╣ ╠═════╣ ╠═════╣ ╠═════╣ ╠═════╣ ╠═════╣ ╠═════╣ ╠═════╣│
│ ║grep ║ ║done ║ ║read ║ ║grep ║ ║done ║ ║read ║ ║grep ║ ║read ║│
│ ║12 f ║ ║     ║ ║models║ ║8 f  ║ ║     ║ ║ctrls║ ║15 f ║ ║views║│
│ ║     ║ ║     ║ ║     ║ ║     ║ ║     ║ ║     ║ ║     ║ ║     ║│
│ ║45%  ║ ║100% ║ ║30%  ║ ║60%  ║ ║100% ║ ║15%  ║ ║75%  ║ ║20% ║│
│ ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝│
└──────────────────────────────────────────────────────────────────┘

Dimensões (terminal 80x24):
  Pane width: 9 cols
  Pane height: 5-6 rows
  Gap: 1 col, minimal vertical
```

### 4.5. Layout "list" (Scroll Vertical)

**Uso:** Muitos agentes, opção de scroll.

```
┌─────────────────────────────────────────────────────────────┐
│ ╔═════════════════════════════════════════════════════════╗ │
│ ║ Agents (12)                              [↑↓ scroll]    ║ │
│ ╠═════════════════════════════════════════════════════════╣ │
│ ║ ● scout-1    running  45%  ↑1.2k↓3.4k  $0.02  15s      ║ │
│ ║   Task: Explore auth...                               ║ │
│ ║   → grep "auth" src/                                  ║ │
│ ║                                                       ║ │
│ ║ ✓ scout-2    complete 100%  ↑800↓1.5k  $0.01  8s      ║ │
│ ║   Task: Explore models...                            ║ │
│ ║   Done: Found 8 model files                          ║ │
│ ║                                                       ║ │
│ ║ ● planner    running  30%  ↑2.1k↓500   $0.01  10s     ║ │
│ ║   Task: Create implementation plan...                ║ │
│ ║   Analyzing scout data...                            ║ │
│ ║                                                       ║ │
│ ║ ○ builder    idle      0%  ↑0↓0       $0     0s      ║ │
│ ║   Waiting for planner output...                     ║ │
│ ║                                                       ║ │
│ ║   [...] 8 more agents, use ↑↓ to navigate             ║ │
│ ╚═════════════════════════════════════════════════════════╝ │
└─────────────────────────────────────────────────────────────┘

Dimensões:
  Full terminal width
  Scrollable content
  Cada agente: 6-8 linhas
```

### 4.6. Tabela de Dimensões por Terminal

| Layout | Min Width | Min Height | Cols/Pane | Rows/Pane | Max Agents |
|--------|-----------|------------|-----------|-----------|------------|
| 1x1    | 40        | 10         | 100%      | 100%      | 1          |
| 1x2    | 60        | 12         | 50% - 1   | 100%      | 2          |
| 1x4    | 80        | 14         | 50% - 1   | 50% - 1   | 4          |
| 1x8    | 120       | 16         | 25% - 1   | 50% - 1   | 8          |
| list   | 40        | 10         | 100%      | scroll    | unlimited  |

**NOTA: Layout 1x8 requer terminal >= 120 cols.** Se terminal for menor, fallback automático para "list":

```typescript
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

## 5. Tamanhos de Fonte

### 5.1. Fonte "small"

**Características:** Compacta, máximo conteúdo.

```
┌────────────────────────────────────────────┐
│ scout [⏳]                    ↑800↓1.2k 45%│
│ → grep "auth" src/                     15s│
│   12 files found                         │
│ → read src/auth/login.ts                 │
│   [content preview...]                   │
└────────────────────────────────────────────┘

Linhas: ~8-10 por painel
Chars/line: ~15-20 por painel (1x8)
```

### 5.2. Fonte "medium" (Default)

**Características:** Balanceada, legível.

```
┌─────────────────────────────────────────────────┐
│ Agent: scout-1                   [running] ⏳   │
│ Task: Explore authentication code              │
│                                                  │
│ → grep "auth" src/                              │
│   Found 12 matches in 4 files                   │
│                                                  │
│ → read src/auth/login.ts                        │
│   [content preview...]                          │
│                                                  │
│ Stats: ↑800 ↓1.2k | 45% | 15s                  │
└─────────────────────────────────────────────────┘

Linhas: ~5-6 por painel
Chars/line: ~25-30 por painel (1x4)
```

### 5.3. Fonte "large"

**Características:** Máxima legibilidade, mínimo conteúdo.

```
┌───────────────────────────────────────────────────────┐
│                                                       │
│        Agent: scout-1                 [running] ⏳     │
│                                                       │
│        Task: Explore authentication code              │
│                                                       │
│        → grep "auth" src/                             │
│          Found 12 files                               │
│                                                       │
│        ↑800↓1.2k | 45% | 15s                          │
│                                                       │
└───────────────────────────────────────────────────────┘

Linhas: ~3-4 por painel
Chars/line: ~18-22 por painel (1x2)
```

### 5.4. Mapeamento de Tamanhos

```typescript
interface FontSizeConfig {
  small: {
    headerHeight: 1;
    lineHeight: 1;
    padding: { x: 1; y: 0 };
    maxContentLines: 10;
  };
  medium: {
    headerHeight: 2;
    lineHeight: 1;
    padding: { x: 2; y: 1 };
    maxContentLines: 6;
  };
  large: {
    headerHeight: 3;
    lineHeight: 1;
    padding: { x: 3; y: 2 };
    maxContentLines: 3;
  };
}
```

---

## 6. Estilos de Header

### 6.1. Header "minimal"

**Uso:** Foco no conteúdo, mínimo de distração.

```
┌──────────────────────────────────────┐
│ scout-1 [⏳]               ↑800↓1.2k  │
├──────────────────────────────────────┤
│ → grep "auth" src/                  │
│   12 files found                    │
│                                      │
│ → read src/auth/login.ts            │
│   [preview...]                      │
└──────────────────────────────────────┘

Campos:
- name (sem prefixo)
- status icon
- stats (tokens)
```

### 6.2. Header "detailed"

**Uso:** Máxima informação, debug detalhado.

```
┌──────────────────────────────────────────────────────────┐
│ ╔══ Agent: scout-1 ═══════════════════ [running] ⏳ ══╗ │
│ ║ Task: Explore authentication code                   ║ │
│ ║ Model: claude-haiku-4-5 | Scope: user              ║ │
│ ║ Turns: 3 | Elapsed: 15s | Progress: 45%             ║ │
│ ╠══════════════════════════════════════════════════════╣ │
│ ║ → grep "auth" src/                                 ║ │
│ ║   12 files found                                   ║ │
│ ║                                                     ║ │
│ ║ → read src/auth/login.ts                           ║ │
│ ║   [preview...]                                     ║ │
│ ╚══════════════════════════════════════════════════════╝ │
└──────────────────────────────────────────────────────────┘

Campos:
- "Agent:" prefixo
- Task completo
- Model
- Scope
- Turns
- Elapsed
- Progress
```

### 6.3. Header "compact"

**Uso:** Layouts densos (1x4, 1x8).

```
┌──────────────────────┐
│ s1[⏳]45% ↑↓1.2k 15s│
├──────────────────────┤
│ → grep "auth"       │
│   12 files          │
│                     │
│ → read auth/        │
│   [preview...]      │
└──────────────────────┘

Campos:
- name abreviado (s1, s2...)
- status icon
- progresso
- tokens (↑↓ abreviado)
- tempo
```

### 6.4. Comparação Visual

```
┌─ minimal ────────────┐ ┌─ detailed ────────────────┐ ┌─ compact ──────┐
│ scout-1 [⏳] ↑800↓1.2k│ │ Agent: scout-1 [running] │ │ s1[⏳]45%↑↓1.2k│
│                      │ │ Task: Explore auth...    │ │                 │
├──────────────────────┤ │ Model: haiku | Scope: user│ │ (content)       │
│ (content)            │ │ Turns: 3 | 15s | 45%     │ │                 │
│                      │ ├───────────────────────────┤ │                 │
└──────────────────────┘ │ (content)                 │ └─────────────────┘
                         └─────────────────────────────┘
```

---

## 7. Atalhos de Teclado

### 7.1. Atalhos Globais

| Key | Action | Description |
|-----|--------|-------------|
| `Ctrl+Shift+A` | Toggle layout | Cicla: 1x1 → 1x2 → 1x4 → 1x8 → list → 1x1 |
| `Ctrl+F` | Cycle font | Cicla: small → medium → large → small |
| `Ctrl+H` | Cycle header | Cicla: minimal → detailed → compact → minimal |
| `Ctrl+S` | Toggle sort | Alterna: default ↔ active |
| `Ctrl+R` | Refresh | Força atualização manual |
| `Ctrl+Shift+Q` | Close | Fecha widget agent-view |
| `q` | Close | Fecha widget agent-view (estilo htop) |
| `Ctrl+O` | Expand | Expande agente selecionado (1x1) |

**NOTA: Mudanças de keybinding para evitar conflitos:**
- `Ctrl+A` → `Ctrl+Shift+A` (evita conflito com `cursorLineStart` do editor)
- `Esc` → `q` (evita conflito com `interrupt` do Pi)
- `Ctrl+Q` → `Ctrl+Shift+Q` (evita conflito com `theme-cycler`)

### 7.2. Navegação (Layout list)

| Key | Action | Description |
|-----|--------|-------------|
| `↑` / `k` | Up | Move seleção para cima |
| `↓` / `j` | Down | Move seleção para baixo |
| `PgUp` | Page up | Move 5 agentes para cima |
| `PgDn` | Page down | Move 5 agentes para baixo |
| `Home` | First | Vai para o primeiro agente |
| `End` | Last | Vai para o último agente |
| `Enter` | Focus | Expande agente selecionado |

### 7.3. Ações de Agente

| Key | Action | Description |
|-----|--------|-------------|
| `a` | Abort | Cancela agente selecionado |
| `r` | Retry | Reinicia agente com falha |
| `c` | Copy | Copia output do agente |
| `v` | View | Abre output completo em pager |
| `d` | Details | Mostra/esconde detalhes |
| `m` | Mute | Silencia atualizações do agente |

### 7.4. Filtros

| Key | Action | Description |
|-----|--------|-------------|
| `/` | Filter | Entra no modo filtro |
| `Esc` | Clear filter | Limpa filtros |

**Modo filtro:**
```
/ Filter: run
              ^^^
              (digitando "run" -> filtra "running")

Enter: Apply
Esc: Cancel
```

### 7.5. Mapeamento de Teclas por Layout

```typescript
interface KeybindingMap {
  // Todos os layouts
  global: {
    "ctrl+shift+a": "toggleLayout";
    "ctrl+f": "cycleFont";
    "ctrl+h": "cycleHeader";
    "ctrl+s": "toggleSort";
    "ctrl+r": "refresh";
    "ctrl+shift+q": "close";
    "q": "close";
  };
  
  // Apenas layout list
  list: {
    "up|k": "navUp";
    "down|j": "navDown";
    "pageup": "pageUp";
    "pagedown": "pageDown";
    "home": "navFirst";
    "end": "navLast";
    "enter": "expandAgent";
  };
  
  // Ações em agente selecionado
  agent: {
    "a": "abortAgent";
    "r": "retryAgent";
    "c": "copyOutput";
    "v": "viewOutput";
    "d": "toggleDetails";
    "m": "muteAgent";
  };
  
  // Modo filtro
  filter: {
    "/": "enterFilterMode";
    "enter": "applyFilter";
    "q": "clearFilter";
  };
}
```

---


## 8. Eventos e Monitoramento

### 8.1. Ciclo de Vida dos Eventos

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fluxo de Eventos                             │
└─────────────────────────────────────────────────────────────────┘

agent-team / subagent
        │
        │ 1. Inicia workflow
        ▼
┌───────────────────┐
│ agent_view:start  │ ← Evento de início
└────────┬──────────┘
         │
         │ 2. Spawn subprocessos
         ▼
┌───────────────────────────────┐
│ Cada subagente emite updates  │
│ via pi.events.emit()          │
└────────┬──────────────────────┘
         │
         │ 3. Coleta estados
         ▼
┌───────────────────────────┐
│ agent_view:update          │ ← Evento de atualização
│ { agents: [...] }         │
└────────┬──────────────────┘
         │
         │ 4. Renderiza UI
         ▼
┌───────────────────────────┐
│ Widget atualiza display   │
│ (tui.setWidget)           │
└────────┬──────────────────┘
         │
         │ 5. Repete a cada refreshInterval
         ▼
      [loop]
         │
         │ 6. Todos completos
         ▼
┌───────────────────────────┐
│ agent_view:end            │ ← Evento de fim
└───────────────────────────┘
```

### 8.2. Eventos Emitidos

```typescript
// Evento de início
pi.events.emit("agent_view:start", {
  workflowId: "workflow-123",
  timestamp: Date.now(),
  config: { layout: "1x4", fontSize: "medium", ... }
});

// Evento de atualização (emitido a cada refreshInterval)
pi.events.emit("agent_view:update", {
  type: "agent_view:update",
  agents: [...], // AgentState[]
  timestamp: Date.now(),
  workflowId: "workflow-123",
  orchestrator: { type: "subagent", mode: "parallel", totalAgents: 4 }
});

// Evento de erro
pi.events.emit("agent_view:error", {
  workflowId: "workflow-123",
  timestamp: Date.now(),
  error: "Subagent scout-1 failed",
  agentId: "scout-1"
});

// Evento de fim
pi.events.emit("agent_view:end", {
  workflowId: "workflow-123",
  timestamp: Date.now(),
  summary: { totalAgents: 4, successful: 3, failed: 1, totalCost: 0.1234 }
});
```

---

## 9. Configuração

### 9.1. Arquivo de Configuração

**Localização:** `~/.pi/agent/settings.json` ou `.pi/settings.json`

```json
{
  "agentView": {
    "enabled": true,
    "layout": "1x4",
    "fontSize": "medium",
    "headerStyle": "minimal",
    "sortOrder": "active",
    "showStats": true,
    "showMetadata": false,
    "refreshInterval": 500,
    "autoOpen": "parallel",
    "maxAgents": 8
  }
}
```

### 9.2. Comandos de Configuração

```bash
/agent-view layout 1x4    # Muda layout
/agent-view font small    # Muda fonte
/agent-view sort active   # Muda ordenação
/agent-view stats on      # Mostra estatísticas
/agent-view close         # Fecha widget
```

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

---

## 10. Modo JSON

### 10.1. Comportamento em --mode json

Quando Pi roda em modo JSON (`--mode json`), o agent-view deve emitir eventos JSON estruturados em vez de renderizar widgets TUI.

### 10.2. Eventos JSON de Saída

```typescript
// Evento emitido durante workflow
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

---

## 11. Integração Universal

### 10.1. Visão Arquitetural

```
agent-team Extension
    ├─ Spawn subprocessos Pi
    ├─ Emite eventos:
    │   agent_team:workflow_start
    │   agent_team:agent_spawn
    │   agent_team:agent_update
    │   agent_team:agent_complete
    │   agent_team:workflow_end
    └─ Consome ações:
        agent_view:action (abort, retry, etc.)
                 ↓
agent-view Extension
    ├─ Consome eventos agent_team
    ├─ Renderiza widget via tui.setWidget
    └─ Emite ações do usuário
```

### 10.2. Protocolo de Eventos

```typescript
// Eventos consumidos de agent-team
interface AgentTeamEvents {
  "agent_team:workflow_start": {
    workflowId: string;
    mode: "single" | "parallel" | "chain";
    agents: Array<{ name: string; task: string }>;
  };
  
  "agent_team:agent_spawn": {
    workflowId: string;
    agentId: string;
    name: string;
    task: string;
    model: string;
  };
  
  "agent_team:agent_update": {
    workflowId: string;
    agentId: string;
    status: AgentStatus;
    messages: AgentMessage[];
    stats: Partial<AgentStats>;
  };
  
  "agent_team:agent_complete": {
    workflowId: string;
    agentId: string;
    result: { exitCode: number; output: string };
  };
}

// Eventos emitidos para agent-team
interface AgentViewEvents {
  "agent_view:action": {
    workflowId: string;
    type: "abort" | "retry" | "pause" | "resume";
    agentId?: string;
  };
}
```

---

## 11. Exemplo de Uso

### 11.1. Parallel Execution

```
Usuário: "Use 4 scouts em paralelo para explorar o código"

┌─────────────────────────────────────────────────────────────────┐
│ ╔═════════════╗ ╔═════════════╗ ╔═════════════╗ ╔═════════════╗│
│ ║ scout-1[⏳] ║ ║ scout-2[⏳] ║ ║ scout-3[⏳] ║ ║ scout-4[⏳] ║│
│ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣│
│ ║ → grep "mod"║ ║ → grep "ctrl"║ ║ → grep "serv"║ ║ → grep "test"║│
│ ║   searching ║ ║   searching ║ ║   searching ║ ║   searching  ║│
│ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣ ╠═════════════╣│
│ ║ 15%  ↑↓500  ║ ║ 20%  ↑↓600  ║ ║ 10%  ↑↓400  ║ ║ 25% ↑↓800   ║│
│ ╚═════════════╝ ╚═════════════╝ ╚═════════════╝ ╚═════════════╝│
└─────────────────────────────────────────────────────────────────┘
```

### 11.2. Chain Workflow

```
Usuário: "Use chain: scout → planner → builder → reviewer"

┌─────────────────────────────────────────────────────────────┐
│ ╔═════════════════════════════════════════════════════════╗ │
│ ║ Chain: scout → planner → builder → reviewer             ║ │
│ ╠═════════════════════════════════════════════════════════╣ │
│ ║ ● scout-1 [running]                      45% | ↑↓1.2k  ║ │
│ ║   → grep "auth" src/                                 ║ │
│ ║     Found 12 files                                   ║ │
│ ║                                                       ║ │
│ ║ ○ planner    [idle]                                  ║ │
│ ║ ○ builder    [idle]                                  ║ │
│ ║ ○ reviewer   [idle]                                  ║ │
│ ╚═════════════════════════════════════════════════════════╝ │
└─────────────────────────────────────────────────────────────┘
```

---

## 12. Componentes TUI

### 12.1. Hierarquia de Componentes

```
AgentViewWidget (Container)
├── WidgetHeader
│   ├── Title
│   ├── WorkflowInfo
│   └── Actions
├── LayoutContainer
│   ├── Layout1x1 | Layout1x2 | Layout1x4 | Layout1x8 | LayoutList
│   │   └── AgentPane[] (Box)
│   │       ├── HeaderComponent
│   │       ├── MessagesComponent
│   │       └── StatsComponent
└── WidgetFooter
    ├── SummaryStats
    └── Keybindings
```

### 12.2. Exemplo de Componente

```typescript
class AgentPane extends Box {
  constructor(
    private agent: AgentState,
    private config: AgentViewConfig,
    theme: Theme
  ) {
    super({
      border: { type: "line" },
      style: theme.getBoxStyle(agent.status)
    });
    
    this.renderContent(theme);
  }
  
  private renderContent(theme: Theme): void {
    // Header
    this.addChild(new HeaderComponent().render(this.agent, this.config.headerStyle, theme));
    
    // Messages (últimas N)
    this.addChild(new MessagesComponent().render(
      this.agent.messages.slice(-5),
      theme
    ));
    
    // Stats
    this.addChild(new StatsComponent().render(this.agent.stats, theme));
  }
}
```

---

## 13. Fluxo de Renderização

### 13.1. Pipeline de Renderização

```
Evento agent_view:update
        │
        ▼
┌───────────────────┐
│ 1. Coleta Estado  │
│    - Agentes      │
│    - Stats        │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 2. Aplica Filtros │
│    - Status       │
│    - Nome         │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 3. Ordena         │
│    - default      │
│    - active       │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 4. Limita Display │
│    - maxAgents    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 5. Seleciona      │
│    Layout         │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 6. Renderiza      │
│    Componentes    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 7. Atualiza       │
│    tui.setWidget  │
└───────────────────┘
```

### 13.2. Otimi

---

## 14. Persistência de Estado

### 14.1. Estado Persistido

```typescript
interface AgentViewState {
  // Configuração atual
  config: AgentViewConfig;
  
  // Workflow sendo monitorado
  currentWorkflow?: {
    id: string;
    startTime: number;
    agents: string[];
  };
  
  // Histórico de workflows
  history: Array<{
    id: string;
    startTime: number;
    endTime: number;
    summary: WorkflowSummary;
  }>;
  
  // Favoritos (layouts salvos)
  presets: Array<{
    name: string;
    config: AgentViewConfig;
  }>;
}
```

### 14.2. Salvamento e Restauração

```typescript
class StateManager {
  private stateFile = "~/.pi/agent/agent-view-state.json";
  
  async save(state: AgentViewState): Promise<void> {
    await fs.writeFile(
      expandHome(this.stateFile),
      JSON.stringify(state, null, 2)
    );
  }
  
  async load(): Promise<AgentViewState | null> {
    try {
      const content = await fs.readFile(expandHome(this.stateFile), "utf-8");
      return JSON.parse(content);
    } catch {
      return null;
    }
  }
  
  async savePreset(name: string, config: AgentViewConfig): Promise<void> {
    const state = await this.load() || { presets: [], history: [], config };
    state.presets.push({ name, config });
    await this.save(state);
  }
}
```

### 14.3. Ciclo de Vida do Estado

```
┌─────────────────────────────────────────────────────────────┐
│              Ciclo de Vida do Estado                         │
└─────────────────────────────────────────────────────────────┘

Início da Extensão
        │
        ▼
┌───────────────────┐
│ Carrega Estado    │
│ ~/.pi/agent/      │
│ agent-view-state  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Aplica Config     │
│ Salva             │
└─────────┬─────────┘
          │
          ▼
    [Workflow Ativo]
          │
          ├─→ Atualiza freqüentemente
          │   (config, currentWorkflow)
          │
          ▼
┌───────────────────┐
│ Workflow Completo │
│ Salva no Histórico│
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Persiste Estado   │
│ (ao encerrar)     │
└───────────────────┘
```

### 14.4. Comandos de Presets

```typescript
pi.registerCommand("agent-view-preset", {
  description: "Salva ou carrega presets de configuração",
  
  handler: async (args, ctx) => {
    const [action, name] = args.split(" ");
    
    if (action === "save") {
      await stateManager.savePreset(name, getCurrentConfig());
      ctx.ui.notify(`Preset "${name}" saved`, "success");
    }
    
    if (action === "load") {
      const state = await stateManager.load();
      const preset = state?.presets.find(p => p.name === name);
      
      if (preset) {
        applyConfig(preset.config);
        ctx.ui.notify(`Preset "${name}" loaded`, "info");
      } else {
        ctx.ui.notify(`Preset "${name}" not found`, "error");
      }
    }
    
    if (action === "list") {
      const state = await stateManager.load();
      const presets = state?.presets ?? [];
      
      ctx.ui.notify(
        `Presets: ${presets.map(p => p.name).join(", ") || "none"}`,
        "info"
      );
    }
  }
});
```

---

## 15. Tratamento de Erros

### 15.1. Tipos de Erro

```typescript
type AgentViewError =
  | { type: "workflow_not_found"; workflowId: string }
  | { type: "agent_timeout"; agentId: string; timeout: number }
  | { type: "invalid_config"; config: unknown; reason: string }
  | { type: "render_error"; message: string; stack?: string }
  | { type: "event_error"; event: string; error: string }
  | { type: "widget_error"; widget: string; error: string };
```

### 15.2. Estratégias de Recuperação

```typescript
class ErrorHandler {
  private logger = new Logger();
  
  handle(error: AgentViewError, ctx: ExtensionContext): void {
    this.logger.log("error", error.type, error);
    
    switch (error.type) {
      case "workflow_not_found":
        this.handleWorkflowNotFound(error, ctx);
        break;
      
      case "agent_timeout":
        this.handleAgentTimeout(error, ctx);
        break;
      
      case "invalid_config":
        this.handleInvalidConfig(error, ctx);
        break;
      
      case "render_error":
        this.handleRenderError(error, ctx);
        break;
      
      default:
        this.handleUnknownError(error, ctx);
    }
  }
  
  private handleWorkflowNotFound(
    error: Extract<AgentViewError, { type: "workflow_not_found" }>,
    ctx: ExtensionContext
  ): void {
    ctx.ui.notify(
      `Workflow ${error.workflowId} not found. It may have completed.`,
      "warning"
    );
    
    // Fecha widget
    closeAgentViewWidget();
  }
  
  private handleAgentTimeout(
    error: Extract<AgentViewError, { type: "agent_timeout" }>,
    ctx: ExtensionContext
  ): void {
    ctx.ui.notify(
      `Agent ${error.agentId} timed out after ${error.timeout}ms`,
      "error"
    );
    
    // Marca agente como erro
    updateAgentStatus(error.agentId, "error");
    
    // Continua monitorando outros agentes
    refreshWidget();
  }
  
  private handleInvalidConfig(
    error: Extract<AgentViewError, { type: "invalid_config" }>,
    ctx: ExtensionContext
  ): void {
    ctx.ui.notify(
      `Invalid config: ${error.reason}. Using defaults.`,
      "warning"
    );
    
    // Restaura configuração padrão
    resetToDefaultConfig();
  }
  
  private handleRenderError(
    error: Extract<AgentViewError, { type: "render_error" }>,
    ctx: ExtensionContext
  ): void {
    ctx.ui.notify(
      `Render error: ${error.message}`,
      "error"
    );
    
    // Fallback para renderização minimalista
    fallbackRender(error);
  }
  
  private handleUnknownError(
    error: AgentViewError,
    ctx: ExtensionContext
  ): void {
    ctx.ui.notify(
      `Unexpected error: ${JSON.stringify(error)}`,
      "error"
    );
    
    // Log completo para debug
    this.logger.log("error", "unknown", error);
  }
}
```

### 15.3. Fallback Rendering

```typescript
function fallbackRender(error: AgentViewRenderError): void {
  // Renderização minimalista que sempre funciona
  const lines = [
    "╔══════════════════════════════════════════╗",
    "║     Agent View: Display Error            ║",
    "╠══════════════════════════════════════════╣",
    "║                                          ║",
    `║ Error: ${error.message.slice(0, 40)}    ║`,
    "║                                          ║",
    "║ Type /agent-view close to exit           ║",
    "║ Type /agent-view refresh to retry        ║",
    "║                                          ║",
    "╚══════════════════════════════════════════╝"
  ];
  
  const widget = new Text(lines.join("\n"), 0, 0);
  
  // Atualiza widget com renderização segura
  pi.tui?.setWidget("agent-view-fallback", () => widget);
}
```

### 15.4. Logs de Debug

```typescript
class Logger {
  private logFile = "~/.pi/agent/logs/agent-view.log";
  private maxFileSize = 1024 * 1024; // 1MB
  
  async log(
    level: "debug" | "info" | "warn" | "error",
    category: string,
    data: unknown
  ): Promise<void> {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      category,
      data
    };
    
    const line = JSON.stringify(entry) + "\n";
    
    try {
      await fs.appendFile(expandHome(this.logFile), line);
      
      // Rotaciona log se muito grande
      await this.rotateIfNeeded();
    } catch (error) {
      // Silencia erros de log para não criar loop
      console.error("[agent-view] Failed to write log:", error);
    }
  }
  
  private async rotateIfNeeded(): Promise<void> {
    const stats = await fs.stat(expandHome(this.logFile)).catch(() => null);
    
    if (stats && stats.size > this.maxFileSize) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      const archiveFile = this.logFile.replace(".log", `-${timestamp}.log`);
      
      await fs.rename(expandHome(this.logFile), expandHome(archiveFile));
    }
  }
}
```

### 15.5. Monitoramento de Saúde

```typescript
class HealthMonitor {
  priv
ate lastUpdate = Date.now();
  private updateCount = 0;
  private errorCount = 0;
  
  heartbeat(): void {
    const now = Date.now();
    const elapsed = now - this.lastUpdate;
    
    if (elapsed > 30000) {
      pi.tui?.notify(
        `Agent View: No updates for ${Math.round(elapsed / 1000)}s`,
        "warning"
      );
    }
    
    this.lastUpdate = now;
    this.updateCount++;
  }
  
  recordError(): void {
    this.errorCount++;
    
    if (this.errorCount > 10) {
      pi.tui?.notify(
        `Agent View: ${this.errorCount} errors detected`,
        "error"
      );
    }
  }
  
  getStats(): { updates: number; errors: number; health: "healthy" | "degraded" | "unhealthy" } {
    const errorRate = this.errorCount / Math.max(1, this.updateCount);
    
    let health: "healthy" | "degraded" | "unhealthy";
    if (errorRate > 0.5) health = "unhealthy";
    else if (errorRate > 0.1) health = "degraded";
    else health = "healthy";
    
    return { updates: this.updateCount, errors: this.errorCount, health };
  }
}
```

---

## Apêndice A: Referência Rápida

### A.1. Atalhos Principais

| Key | Ação |
|-----|------|
| `Ctrl+A` | Cicla layouts |
| `Ctrl+F` | Cicla fontes |
| `Ctrl+H` | Cicla headers |
| `Ctrl+S` | Alterna ordenação |
| `Ctrl+R` | Força atualização |
| `Ctrl+Q` | Fecha widget |
| `Esc` | Fecha widget / Cancela |
| `Ctrl+O` | Expande agente |

### A.2. Ícones de Status

| Ícone | Status |
|-------|--------|
| ○ | idle |
| ◐ | starting |
| ⏳ | running |
| ⏸ | waiting |
| ✓ | complete |
| ✗ | error |
| ⊘ | aborted |

### A.3. Comandos

```
/agent-view layout [1x1|1x2|1x4|1x8|list]
/agent-view font [small|medium|large]
/agent-view header [minimal|detailed|compact]
/agent-view sort [default|active]
/agent-view close
```

---

**Fim do Especificação v1.0.0**
