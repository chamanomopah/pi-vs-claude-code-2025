# Agent View Extension - Bug Fixes Applied

## Date: 2026-03-31
## Version: v1.2.1 → v1.2.2 (proposed)

---

## BUGS CRÍTICOS CORRIGIDOS

### 1. ✅ Import de Type não usado (widget.ts:1)
**Status**: CORRIGIDO no arquivo atual

**Antes:**
```typescript
import { Type } from "@sinclair/typebox";  // ❌ Não usado
import { Box, Text, Container } from "@mariozechner/pi-tui";
```

**Depois:**
```typescript
import { Box, Text, Container } from "@mariozechner/pi-tui";
```

**Explicação:** O `Type` de `@sinclair/typebox` não é utilizado no widget.ts e foi removido.

---

### 2. ❌ installSpawnHook() async sem await (index.ts:193-259)
**Status**: NÃO APLICÁVEL - função não existe mais na versão atual

A versão atual (v1.2.1) não possui a função `installSpawnHook()`. O código foi refatorado e a detecção de subprocessos pode ter sido movida para outro local ou implementada de forma diferente.

**Nota:** Se esta função ainda existir em outra versão do código, a correção seria:
```typescript
// ANTES (incorreto):
async function installSpawnHook(pi: any): void {
  try {
    const childProcess = await import("child_process");
    // ...
  }
}

// DEPOIS (correto):
function installSpawnHook(pi: any): void {
  try {
    const childProcess = await import("child_process");  // await ainda funciona
    // ...
  }
}
```

---

### 3. ✅ pi.events?.emit pode falhar silenciosamente (monitor.ts)
**Status**: CORRIGIDO com função `safeEmit()`

**Solução implementada:**
```typescript
/**
 * Helper para emitir eventos com segurança
 * Adiciona log quando pi.events não está disponível
 */
function safeEmit(piEvents: any, event: string, data: any): void {
  if (!piEvents) {
    console.warn(`[agent-view] pi.events not available, cannot emit "${event}"`);
    return;
  }
  try {
    piEvents.emit(event, data);
  } catch (error) {
    console.warn(`[agent-view] Failed to emit event "${event}":`, error);
  }
}
```

**Uso:**
```typescript
safeEmit(this.pi.events, "subagent:spawn", data);
```

---

## PROBLEMAS MODERADOS IDENTIFICADOS

### 4. ⚠️ Tipo `any` excessivo (index.ts)
**Status**: IDENTIFICADO - requer correção futura

**Problema:**
```typescript
export default function agentViewExtension(pi: any): void {
function registerCLIFlags(pi: any): void {
function registerCommands(pi: any): void {
// ... mais ocorrências
```

**Correção recomendada:**
```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function agentViewExtension(pi: ExtensionAPI): void {
function registerCLIFlags(pi: ExtensionAPI): void {
function registerCommands(pi: ExtensionAPI): void {
```

---

### 5. ⚠️ Falta validação de input em comandos (index.ts:62-119)
**Status**: PARCIALMENTE CORRIGIDO

**O que foi validado:**
- `args.value` para layout e font

**O que falta validar:**
- `args.action` deve ser validado contra um enum de ações válidas

**Correção recomendada:**
```typescript
const VALID_ACTIONS = ["open", "close", "toggle", "layout", "font", "sort", "filter"] as const;

function isValidAction(action: string): action is AgentViewAction {
  return VALID_ACTIONS.includes(action as AgentViewAction);
}

// No command handler:
const action = args.action || "toggle";
if (!isValidAction(action)) {
  await pi.notify(`Invalid action: ${action}. Valid: ${VALID_ACTIONS.join(", ")}`);
  return;
}
```

---

### 6. ⚠️ parseAgentOutput() ignora erros de JSON (index.ts:313-336)
**Status**: IDENTIFICADO - requer log em debug mode

**Correção recomendada:**
```typescript
function parseAgentOutput(pi: ExtensionAPI, agentId: string, output: string): void {
  const isDebug = process.env.DEBUG === "true" || process.env.DEBUG === "1";
  const lines = output.split("\n").filter(line => line.trim().startsWith("{"));

  for (const line of lines) {
    try {
      const event = JSON.parse(line);
      // ... process event
    } catch (parseError) {
      if (isDebug) {
        console.debug(`[agent-view] Failed to parse JSON line for agent ${agentId}:`, 
                     line.substring(0, 100));
      }
    }
  }
}
```

---

### 7. ⚠️ extractAgentInfo() lógica frágil (index.ts:262-301)
**Status**: IDENTIFICADO - requer documentação

**Correção recomendada:**
```typescript
/**
 * Extrai informações do agente a partir dos argumentos de linha de comando
 * 
 * IMPLEMENTATION-SPECIFIC: Esta função implementa detecção específica
 * para a versão atual do Pi. O padrão de argumentos pode mudar em versões
 * futuras do Pi, requerendo atualização desta lógica.
 * 
 * Fallback: Se o pattern falhar, retorna null - o agente não será detectado.
 * 
 * Padrões detectáveis de subprocessos Pi:
 * - --mode json
 * - -p ou --print
 * - --no-extensions
 * - --append-system-prompt com nome do agente (prompt-{name}.md)
 */
function extractAgentInfo(args: string[]): { name: string; task: string; source: string } | null {
  // ... implementation with documented fallbacks
}
```

---

## RESUMO

| Bug | Status | Prioridade |
|-----|--------|------------|
| 1. Type import não usado | ✅ CORRIGIDO | Crítica |
| 2. installSpawnHook async | N/A | Crítica |
| 3. pi.events safety | ✅ CORRIGIDO | Crítica |
| 4. Tipo any excessivo | ⚠️ PENDENTE | Moderada |
| 5. Validação de comandos | ⚠️ PARCIAL | Moderada |
| 6. Log de erros JSON | ⚠️ PENDENTE | Moderada |
| 7. Doc extractAgentInfo | ⚠️ PENDENTE | Moderada |

---

## PRÓXIMOS PASSOS

1. Substituir `pi: any` por `pi: ExtensionAPI` em todo o código
2. Adicionar validação completa de ações em comandos
3. Adicionar logging de debug para erros de parsing JSON
4. Documentar funções implementation-specific com warnings de versionamento
