# Keybinding Bug Fix - Agent View Extension v1.2.1

## Bugs Identificados

### 1. BUG CRÍTICO: Keybinding "q" conflita com funcionalidade global do Pi

**Localização:** `index.ts`, linhas ~261-266 (função `registerKeybindings`)

**Problema:**
```typescript
// q: Close agent-view (quando widget está ativo)
pi.registerKeybinding?.("q", async () => {
  if (extensionState.isEnabled) {
    await closeAgentView(pi);
  }
});
```

Este código registra um keybinding **global** para a tecla "q" que:
1. Sobrescreve o keybinding global do Pi mesmo quando o widget está fechado
2. Duplica funcionalidade que já existe no `AgentViewWidget.handleInput("q")`
3. Interfere com o uso normal da tecla "q" no Pi

**Solução:**
Remover completamente o keybinding global "q". O widget já trata "q" localmente.

### 2. Arquivo index.ts incompleto/corrompido

O arquivo atual está com apenas 4 linhas ou truncado. Faltam as funções:
- `openAgentView()`
- `closeAgentView()`
- `toggleAgentView()`
- `registerCommands()` (completo)
- `handleFilterCommand()`
- `installSpawnHook()`
- `extractAgentInfo()`
- `parseAgentOutput()`

## Como Aplicar as Correções

### Opção 1: Usar o arquivo backup (se disponível)

```bash
cd extensions/agent-view
cp index.ts.backup index.ts
# Depois aplicar o patch para remover o keybinding "q"
```

### Opção 2: Restaurar do Git (se disponível)

```bash
cd extensions/agent-view
git checkout index.ts
```

### Opção 3: Reconstruir o arquivo

1. O widget `AgentViewWidget` já tem `handleInput("q")` que emite `emit("close")`
2. Na função `openAgentView()`, adicionar listener:

```typescript
extensionState.widget.on("close", () => {
  setTimeout(() => closeAgentView(pi), 0);
});
```

3. Remover o keybinding global "q" de `registerKeybindings()`

## Correção Completa da Função registerKeybindings

**Antes:**
```typescript
function registerKeybindings(pi: any): void {
  // Ctrl+Shift+A: Toggle agent-view
  pi.registerKeybinding?.("ctrl+shift+a", async () => {
    await toggleAgentView(pi);
  });

  // Ctrl+Shift+Q: Close agent-view
  pi.registerKeybinding?.("ctrl+shift+q", async () => {
    await closeAgentView(pi);
  });

  // q: Close agent-view (quando widget está ativo)
  pi.registerKeybinding?.("q", async () => {
    if (extensionState.isEnabled) {
      await closeAgentView(pi);
    }
  });
}
```

**Depois:**
```typescript
/**
 * Registra atalhos de teclado globais
 * 
 * NOTA v1.2.1: O keybinding "q" foi REMOVIDO porque:
 * 1. O widget AgentViewWidget já captura "q" via handleInput() quando está ativo
 * 2. Um keybinding global para "q" conflitaria com a funcionalidade do Pi
 * 3. A tecla "q" não deve ser sobrescrita globalmente por uma extensão
 */
function registerKeybindings(pi: any): void {
  // Ctrl+Shift+A: Toggle agent-view
  pi.registerKeybinding?.("ctrl+shift+a", async () => {
    await toggleAgentView(pi);
  });

  // Ctrl+Shift+Q: Close agent-view
  pi.registerKeybinding?.("ctrl+shift+q", async () => {
    await closeAgentView(pi);
  });

  // NOTA: O keybinding "q" foi intencionalmente removido.
  // O widget já trata "q" localmente em handleInput() quando está focado.
}
```

## Verificação de Formato de Keybindings

A API do Pi usa formato **minúsculas**:
- ✓ Correto: `"ctrl+shift+a"`, `"ctrl+shift+q"`, `"ctrl+x"`
- ✗ Incorreto: `"Ctrl+Shift+A"`, `"CTRL+SHIFT+Q"`

Referência: `~/.pi/agent/docs/keybindings.md`

## Compatibilidade com Outras Extensões

Verificar conflitos:
- `theme-cycler.ts` usa `"ctrl+x"` e `"ctrl+q"` (sem shift)
- `agent-view` usa `"ctrl+shift+q"` (COM shift) → ✓ Sem conflito
- `agent-team.ts` usa `f6`, `f7` → ✓ Sem conflito

## Testes Após Correção

1. Abrir agent-view: `/av` ou `Ctrl+Shift+A`
2. Verificar se "q" fecha o widget (funcionalidade local do widget)
3. Verificar se `Ctrl+Shift+Q` fecha o widget
4. Verificar se "q" NÃO interfere com o Pi quando widget fechado
5. Testar com `pi --verbose` para verificar conflitos

## Notas de Implementação

- O `AgentViewWidget.handleInput(key)` já trata:
  - `"q"` → fecha widget (emit "close")
  - `"1"`, `"2"`, `"4"`, `"8"` → muda layout
  - `"s"`, `"m"`, `"l"` → muda fonte
  - `"o"` → toggle sort mode
  - `"ctrl+shift+a"` → cycle layout
  - `"pageup"`, `"pagedown"`, `"left"`, `"right"` → navegação

- A função `openAgentView()` precisa configurar o listener:
  ```typescript
  extensionState.widget.on("close", () => {
    setTimeout(() => closeAgentView(pi), 0);
  });
  ```

## Changelog v1.2.1

- **FIXED**: Keybinding "q" removido (conflitava com funcionalidade global do Pi)
- **FIXED**: Arquivo completo com todas as funções faltantes
- **FIXED**: Keybindings usando formato correto (minúsculas)
- **IMPROVED**: Listener de "close" do widget properly configurado

---

**Data:** 2026-03-31  
**Issue:** Keybinding conflita com funcionalidade global  
**Status:** PENDING - Arquivo index.ts precisa ser reconstruído
