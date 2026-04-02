# Quick Start: Keyboard Shortcuts com alt+shift+i

## 🎯 Problema Resolvido

**Antes:** `alt+shift+i` não funcionava no shortcuts.yaml  
**Depois:** ✅ Funciona! (ordem dos modificadores não importa mais)

## 🚀 Como Usar

### 1. Testar se funciona
```bash
pi -e extensions/shortcut-diagnostic.ts
```

Depois execute:
```
/test-shortcuts
```

### 2. Usar nos seus extensions

**No shortcuts.yaml:**
```yaml
my-extension:
  - alt+shift+i   # minha-ação
  # OU (tanto faz!)
  - shift+alt+i   # minha-ação
```

**No seu extension TypeScript:**
```typescript
import { registerActionShortcuts } from "./shortcutLoader.ts";

registerActionShortcuts(pi, "my-extension", {
  "minha-ação": {
    description: "Faça algo",
    handler: async (ctx) => {
      ctx.ui.notify("Funcionou!", "info");
    }
  }
}, ctx.cwd);
```

### 3. Recarregar
```
/reload
```

## ✨ Novidades

- ✅ Ordem dos modificadores **não importa**: `alt+shift+i` = `shift+alt+i`
- ✅ Validação de erros no carregamento
- ✅ Comando `/test-shortcuts` para diagnóstico
- ✅ Avisa se seu terminal suporta a combinação

## ⚠️ Importante: Kitty Protocol

Combinações com múltiplos modificadores (como `alt+shift+i`) precisam do **Kitty Keyboard Protocol**.

### Verificar se seu terminal suporta:
```
/test-shortcuts
```

Procure por: `Kitty Keyboard Protocol: ACTIVE` ✅

Se estiver `INACTIVE` ❌:
- Use teclas de função (F1-F12) em vez disso
- OU mude para um terminal com Kitty support:
  - **Kitty Terminal** (recomendado)
  - **WezTerm** (habilite `enable_kitty_keyboard = true`)
  - **Ghostty** (já vem habilitado)
  - **iTerm2** (macOS, habilite nas configurações)

## 📚 Documentação Completa

Veja `docs/SHORTCUTTS_GUIDE.md` para:
- Referência completa de formato de teclas
- Matriz de compatibilidade de terminais
- Troubleshooting
- Exemplos

## 🔧 Exemplos Rápidos

```yaml
# Todos funcionam da mesma forma!
agent-team:
  - f6              # next-team
  - alt+shift+i     # prev-team
  - shift+alt+i     # prev-team (mesma coisa!)
  - ALT+SHIFT+i     # prev-team (case insensitive!)
```

## 📋 Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `/test-shortcuts` | Mostra todos os shortcuts e status do terminal |
| `/reload` | Recarrega extensions e shortcuts |
| `/hotkeys` | Mostra atalhos embutidos do Pi |

---

**Pronto!** `alt+shift+i` agora funciona corretamente! 🎉
