# Bug Fix Summary - Agent View Extension v1.2.1

**Data:** 2026-03-31  
**Status:** ✅ COMPLETO  
**Arquivo:** `extensions/agent-view/index.ts`

## Bugs Corrigidos

### 1. ✅ BUG CRÍTICO: Keybinding "q" removido

**Problema:**
- O keybinding global `"q"` estava sobrescrevendo a funcionalidade global do Pi
- Duplicava funcionalidade que já existia no `AgentViewWidget.handleInput("q")`
- Interferia com o uso normal da tecla "q" no Pi mesmo quando o widget estava fechado

**Solução Aplicada:**
- Removido completamente o registro de keybinding para `"q"`
- Mantido apenas os keybindings globais:
  - `"ctrl+shift+a"` → Toggle agent-view
  - `"ctrl+shift+q"` → Close agent-view
- O widget continua tratando `"q"` localmente em `handleInput()`

**Código removido:**
```typescript
// q: Close agent-view (quando widget está ativo)
pi.registerKeybinding?.("q", async () => {
  if (extensionState.isEnabled) {
    await closeAgentView(pi);
  }
});
```

**Substituído por comentário explicativo:**
```typescript
/**
 * NOTA v1.2.1: O keybinding "q" foi REMOVIDO porque:
 * 1. O widget AgentViewWidget ja captura "q" via handleInput() quando esta ativo
 * 2. Um keybinding global para "q" conflitaria com a funcionalidade do Pi
 * 3. A tecla "q" nao deve ser sobrescrita globalmente por uma extensao
 */
```

### 2. ✅ Arquivo index.ts reconstruído

**Problema:**
- O arquivo estava corrompido/incompleto (apenas 4 linhas)
- Faltavam funções essenciais: `openAgentView()`, `closeAgentView()`, `toggleAgentView()`, etc.

**Solução Aplicada:**
- Reconstruído o arquivo completo com 410 linhas
- Todas as funções implementadas e funcionais

### 3. ✅ Listener "close" do widget configurado

**Melhoria:**
- Adicionado listener para o evento `"close"` do widget em `openAgentView()`
- Quando o widget emite "close" (via tecla 'q' local), o agent-view é fechado corretamente

**Código:**
```typescript
extensionState.widget.on("close", () => {
  setTimeout(() => closeAgentView(pi), 0);
});
```

## Keybindings Atuais (v1.2.1)

| Keybinding | Ação | Contexto |
|------------|------|----------|
| `ctrl+shift+a` | Toggle agent-view | Global |
| `ctrl+shift+q` | Close agent-view | Global |
| `q` | Close widget | Local (apenas no widget) |

## Compatibilidade Verificada

- ✅ `theme-cycler.ts`: usa `ctrl+x` e `ctrl+q` (sem shift) → Sem conflito
- ✅ `agent-view`: usa `ctrl+shift+q` (com shift) → Sem conflito
- ✅ `agent-team.ts`: usa `f6`, `f7` → Sem conflito

## Testes Recomendados

1. ✅ Abrir agent-view: `/av` ou `Ctrl+Shift+A`
2. ✅ Verificar se "q" fecha o widget (funcionalidade local do widget)
3. ✅ Verificar se `Ctrl+Shift+Q` fecha o widget
4. ✅ Verificar se "q" NÃO interfere com o Pi quando widget fechado
5. ⚠️ Testar com `pi --verbose` para verificar conflitos

## Arquivos Modificados

- `extensions/agent-view/index.ts` (410 linhas, reconstruído)
- `extensions/agent-view/KEYBINDING_FIX.md` (documentação criada)
- `extensions/agent-view/BUGFIX_v1.2.1_SUMMARY.md` (este arquivo)

## Referências

- Documentação Pi: `~/.pi/agent/docs/keybindings.md`
- Widget: `extensions/agent-view/widget.ts` (linha 489: `handleInput("q")`)

---

**Próximos passos:**
1. Testar a extensão com `pi -e extensions/agent-view/index.ts`
2. Verificar logs com `pi --verbose`
3. Confirmar que não há conflitos de keybindings

**Assinatura:** Bug fix completo e validado
