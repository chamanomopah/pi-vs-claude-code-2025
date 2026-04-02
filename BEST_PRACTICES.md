# BEST_PRACTICES.md - Melhores Práticas para Extensões Pi

> Lições aprendidas debugando extensões Pi para compatibilidade Windows e composição correta.

> **⚠️ IMPORTANTE:** Extensões Pi são projetadas para **composição** - funcionam EM CONJUNTO com outras extensões, não sozinhas. Sua nova extensão deve se adaptar às extensões existentes, não o contrário.

---

## 🏗️ Arquitetura de Extensões

### Princípio Fundamental: Composição sobre Isolamento

Extensões Pi são projetadas para serem **combinadas**. O usuário carrega múltiplas extensões simultaneamente:

```bash
pi -e extensions/agent-team.ts -e extensions/minimal.ts -e extensions/prompt-timer.ts
```

**Sua extensão deve funcionar corretamente quando combinada com outras, sem:**
- Sobrescrever footer/status de outras extensões desnecessariamente
- Quebrar quando outra extensão redefine o tema
- Conflitar com widgets de outras extensões
- Depender de uma ordem específica de carregamento

---

## 📦 Classificação de Extensões

### 🔒 Extensões Core (NÃO MODIFICAR)

**Desenvolvidas pelo autor original do projeto.** NÃO modifique estas extensões:

| Extensão | Propósito | Responsável |
|----------|-----------|-------------|
| `agent-team.ts` | Dispatcher para equipe de especialistas | Autor Original |
| `agent-chain.ts` | Pipeline sequencial de agentes | Autor Original |
| `cross-agent.ts` | Carrega comandos/skills de múltiplos dirs | Autor Original |
| `damage-control.ts` | Auditoria de segurança em tempo real | Autor Original |
| `minimal.ts` | Footer compacto com contexto | Autor Original |
| `pi-pi.ts` | Meta-agente que constrói agentes Pi | Autor Original |
| `pure-focus.ts` | Remove footer/status - modo foco | Autor Original |
| `purpose-gate.ts` | Gate de intenção de sessão | Autor Original |
| `session-replay.ts` | Timeline da sessão | Autor Original |
| `subagent-widget.ts` | Spawner de subagentes | Autor Original |
| `system-select.ts` | Seletor de persona do agente | Autor Original |
| `theme-cycler.ts` | Ciclador de temas via hotkey | Autor Original |
| `tilldone.ts` | Sistema de disciplina de tarefas | Autor Original |
| `tool-counter.ts` | Footer rico com métricas | Autor Original |
| `tool-counter-widget.ts` | Widget de contagem por ferramenta | Autor Original |
| `themeMap.ts` | Mapeamento extensão → tema | Autor Original |

### ✨ Extensões Adicionais (SEGUEM ESTAS PRÁTICAS)

**Novas extensões que você cria** DEVEM seguir os princípios abaixo para funcionar harmoniosamente com as extensões core:

| Extensão | Tipo | Observação |
|----------|------|------------|
| `prompt-timer.ts` | Utilitário | **Exemplo a seguir** - usa widget, não sobrescreve footer |

---

## 🎯 Princípios para Novas Extensões

### 1. Use Widgets, não Footer/Status

**Problema:** Footer é sobrescrito pela última extensão que chama `setFooter()`. Status pode ser sobrescrito por extensões como `agent-team`.

**Solução:** Use `ctx.ui.setWidget()` para visualizações persistentes:

```typescript
// ✅ CORRETO para novas extensões
ctx.ui.setWidget("my-widget", (_tui, theme) => {
    const text = new Text("", 0, 0);
    const state = { value: "ready" };  // Objeto mutável

    pi.on("some_event", async (_event) => {
        state.value = "updated";
        if (tui) tui.requestRender();  // Força re-render
    });

    return {
        render(width: number): string[] {
            text.setText(theme.fg("muted", state.value));
            return text.render(width);
        },
        invalidate() {
            text.invalidate();
        },
    };
}, { placement: "belowEditor" });
```

### 2. Não Dependam de Ordem de Carregamento

Sua extensão deve funcionar independentemente da ordem em que é carregada:

```bash
# Ambos devem funcionar igualmente bem
pi -e extensions/minimal.ts -e extensions/minha-ext.ts
pi -e extensions/minha-ext.ts -e extensions/minimal.ts
```

### 3. Use IDs Únicos para Status

Se precisar usar status line, use ID único e não sobrescreva status de outras extensões:

```typescript
// ✅ CORRETO
ctx.ui.setStatus("minha-ext-unico", "Status específico");

// ❌ ERRADO
ctx.ui.setStatus("Status genérico");  // Sobrescreve todos!
```

### 4. Respeite o Tema da Extensão Principal

A última extensão carregada define o tema. Não tente forçar seu tema - deixe o usuário decidir:

```typescript
// ✅ CORRETO - use applyExtensionDefaults
pi.on("session_start", async (_event, ctx) => {
    applyExtensionDefaults(import.meta.url, ctx);  // Respeita ordem de carregamento
    // ...
});
```

---

## 🔌 Pi Events Reference

### Eventos Disponíveis (confirmados no código)

| Categoria | Evento | Quando Disparado | Uso Típico |
|-----------|--------|-----------------|------------|
| **Session** | `session_start` | Início da sessão | Inicializar UI, widgets |
| **Session** | `session_shutdown` | Fim da sessão | Limpar recursos |
| **Session** | `session_switch` | Troca de branch | Reconstruir estado |
| **Input** | `input` | Usuário envia input | Capturar início de timer |
| **Agent** | `before_agent_start` | Antes do agente começar | Gate, validação |
| **Agent** | `agent_start` | Agente começa | Track início |
| **Agent** | `agent_end` | Agente termina | Capturar tempo de resposta |
| **Tool** | `tool_call` | Ferramenta chamada | Interceptação, validação |
| **Tool** | `tool_execution_end` | Ferramenta termina | Atualizar contadores |

### ⚠️ Eventos que NÃO existem no Pi

- ❌ `user_message_end` - não existe, use `input`
- ❌ `assistant_message_end` - não existe, use `agent_end`
- ❌ `message_start`, `message_end`, `message_update` - não existem no Pi (existem no Claude Code)

### Padrão: Timer de Resposta

```typescript
// Capturar tempo de resposta do agente
const state = {
    startTime: null as number | null,
    pending: false,
    timerText: "⏱️ ready",
};

let tui: TUI | null = null;

pi.on("input", async (_event) => {
    state.startTime = Date.now();
    state.pending = true;
    state.timerText = "⏱️ calculating...";
    if (tui) tui.requestRender();
});

pi.on("agent_end", async (_event) => {
    if (!state.pending || state.startTime === null) return;

    const elapsedMs = Date.now() - state.startTime;
    const elapsedSec = (elapsedMs / 1000).toFixed(1);
    state.timerText = `⏱️ ${elapsedSec}s`;

    state.startTime = null;
    state.pending = false;
    if (tui) tui.requestRender();
});
```

---

## 🔧 Windows Compatibility

### ❌ Problema: `fileURLToPath()` falha no Windows

`import.meta.url` retorna URLs `file://` que podem causar problemas no Windows.

**Solução - Sempre use try/catch com fallback:**

```typescript
import { basename } from "path";
import { fileURLToPath } from "url";

function extensionName(fileUrl: string): string {
    let filePath = fileUrl;

    // Handle file:// URLs - normalize for Windows compatibility
    if (fileUrl.startsWith("file://")) {
        try {
            filePath = fileURLToPath(fileUrl);
        } catch {
            // Fallback: strip file:// prefix and normalize slashes
            filePath = fileUrl.replace(/^file:\/+/, "").replace(/\//g, "\\");
        }
    }

    // Normalize path separators for basename
    const normalizedPath = filePath.replace(/\\/g, "/");
    return basename(normalizedPath).replace(/\.[^.]+$/, "");
}
```

### ✅ Boas Práticas - Paths no Windows

| Função | Uso Correto | Observação |
|--------|-------------|------------|
| `path.join()` | ✅ Sempre | Lida com separadores automaticamente |
| `path.resolve()` | ✅ Sempre | Resolve caminhos relativos/absolutos |
| `path.sep` | ✅ Para split | Separador específico do OS |
| Strings hardcoded | ❌ Evitar | Use `path.join()` em vez de `/` ou `\` |

### Regex - Sempre trate CRLF

Quebras de linha no Windows são `\r\n` (CRLF), não apenas `\n`.

```typescript
// ❌ Errado - só funciona no Unix
const parts = text.split("\n");

// ✅ Correto - funciona em ambos
const parts = text.split(/\r?\n/);

// ✅ Correto - regex para delimitadores
const delimiter = /^---\r?\n/;  // Markdown frontmatter
```

---

## 🐛 Erros Comuns a Evitar

### 0. Eventos Inexistentes - CRITICAL

**Problema:** Usar eventos que não existem no Pi (ex: `user_message_end`, `assistant_message_end`).

```typescript
// ❌ ERRADO - esses eventos não existem!
pi.on("user_message_end", async (_event, ctx) => { ... });
pi.on("assistant_message_end", async (_event, ctx) => { ... });

// ✅ CORRETO - use os eventos certos do Pi
pi.on("input", async (_event, ctx) => { ... });          // usuário envia mensagem
pi.on("agent_end", async (_event, ctx) => { ... });       // agente termina de responder
```

### 1. Sobrescrever Footer de Outras Extensões

**Problema:** Múltiplas extensões usando `setFooter()` - a última a chamar sobrescreve todas.

**Solução:** Use widget em vez de footer para informação persistente.

### 2. Status Line Não Aparece

**Causa:** Extensões como `agent-team` sobrescrevem status imediatamente.

**Solução:** Use widget com `placement: "aboveEditor"` ou `placement: "belowEditor"`.

### 3. Widget Não Atualiza

**Causa:** Estado capturado no closure, ou `tui.requestRender()` não sendo chamado.

**Solução:** Use objeto mutável + `tui.requestRender()`.

```typescript
// ✅ CORRETO - estado mutável + requestRender
const state = { value: "initial" };

pi.on("event", async (_event) => {
    state.value = "updated";     // Mutável
    if (tui) tui.requestRender(); // Força refresh
});
```

### 4. Tema Não Aplicado

**Causa:** Extensão não está no `THEME_MAP` ou está sendo sobrescrita por extensão carregada depois.

**Solução:**
1. Adicione ao `THEME_MAP`
2. Use `applyExtensionDefaults(import.meta.url, ctx)`
3. Aceite que a última extensão define o tema (por design)

---

## 📦 Padrões de Código para Novas Extensões

### Padrão 1: Widget com Estado Mutável (RECOMENDADO)

```typescript
const state = { text: "Estado inicial" };
let tui: TUI | null = null;

pi.on("algum_event", async (_event) => {
    state.text = "Estado atualizado";
    if (tui) tui.requestRender();
});

ctx.ui.setWidget("widget-id", (__tui, theme) => {
    tui = __tui;
    const textComponent = new Text("", 0, 0);

    return {
        render(width: number): string[] {
            textComponent.setText(theme.fg("muted", state.text));
            return textComponent.render(width);
        },
        invalidate() {
            textComponent.invalidate();
        },
    };
}, { placement: "belowEditor" });
```

### Padrão 2: Status com ID Único

```typescript
pi.on("session_start", async (_event, ctx) => {
    ctx.ui.setStatus("minha-ext-v1", "Pronto");
});

pi.on("algum_evento", async (_event, ctx) => {
    ctx.ui.setStatus("minha-ext-v1", "Processando...");
});
```

### Padrão 3: Interceptar Tools (Gate Pattern)

```typescript
pi.on("tool_call", async (event, ctx) => {
    if (event.toolName === "bash") {
        // Validar ou bloquear
        return { block: false };
    }
    return { block: false };
});
```

---

## 🧪 Testando Novas Extensões

### Teste de Composição (OBRIGATÓRIO)

Sua extensão DEVE funcionar em combinação com as extensões core:

```bash
# Teste com minimal (mais comum)
pi -e extensions/minimal.ts -e extensions/minha-ext.ts

# Teste com agent-team (muito usado)
pi -e extensions/agent-team.ts -e extensions/minha-ext.ts

# Teste com ambas
pi -e extensions/agent-team.ts -e extensions/minimal.ts -e extensions/minha-ext.ts

# Teste em ordem inversa
pi -e extensions/minha-ext.ts -e extensions/agent-team.ts -e extensions/minimal.ts
```

### Verificação de Erros

```bash
# Redirecione stderr para ver erros de carregamento
pi -e extensions/minha-ext.ts 2>&1 | grep -i error
```

---

## 📋 Checklist para Nova Extensão

**Antes de considerar sua extensão "pronta":**

### Composição
- [ ] Funciona com `minimal.ts` carregado antes
- [ ] Funciona com `minimal.ts` carregado depois
- [ ] Funciona com `agent-team.ts` (antes e depois)
- [ ] Funciona com ambas `minimal.ts` + `agent-team.ts`
- [ ] Não sobrescreve footer/status desnecessariamente

### UI
- [ ] Usa widget para visualizações persistentes
- [ ] Se usa status, usa ID único: `setStatus("minha-ext-v1", "texto")`
- [ ] Se usa estado mutável, chama `tui.requestRender()` após atualizações
- [ ] Widget usa componente TUI (`Text`, `Container`) para renderização correta

### Windows
- [ ] Paths usam `path.join()` ou `path.resolve()`
- [ ] Regex de quebra de linha usam `\r?\n`
- [ ] `import.meta.url` tratado com try/catch se usar `fileURLToPath()`

### Tema
- [ ] Extensão adicionada ao `THEME_MAP` (se usar tema customizado)
- [ ] `applyExtensionDefaults(import.meta.url, ctx)` chamado no `session_start`
- [ ] Aceita que última extensão define o tema (não força)

### Eventos
- [ ] Usa apenas eventos existentes do Pi (`input`, `agent_end`, etc.)
- [ ] NÃO usa `user_message_end` ou `assistant_message_end` (não existem)

---

## 🔗 Referências Rápidas

| Arquivo | Propósito |
|---------|-----------|
| `THEME.md` | Tokens de cor e convenções visuais |
| `TOOLS.md` | Assinaturas de ferramentas built-in |
| `RESERVED_KEYS.md` | Atalhos reservados vs seguros |
| `COMPARISON.md` | Pi vs Claude Code - comparação features |
| `extensions/themeMap.ts` | Mapeamento extensão → tema |
| `extensions/prompt-timer.ts` | **Exemplo a seguir** - extensão que segue todos os princípios |

---

## 📝 Resumo

**Extensões Core (NÃO MODIFICAR):** Todas as 17 extensões existentes foram desenvolvidas pelo autor original e não devem ser alteradas.

**Novas Extensões (SEGUIR ESTE GUIA):** Devem ser projetadas para composição - funcionando harmoniosamente com as extensões core existentes, usando widgets, respeitando temas, e seguindo os padrões estabelecidos.

**Extensão Modelo:** `prompt-timer.ts` é o exemplo perfeito de uma extensão que segue todos os princípios de composição.

---

**Última atualização:** 2025-03-29
**Baseado em:** Debug de extensões Pi para Windows + arquitetura de composição
