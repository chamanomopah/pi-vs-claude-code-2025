# 🎹 Guia Completo do Sistema de Shortcuts

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Arquivo shortcuts.yaml](#estrutura-do-arquivo-shortcutsyaml)
3. [Como Editar o Arquivo](#como-editar-o-arquivo)
4. [Formato dos Key IDs](#formato-dos-key-ids)
5. [Adicionando Novos Atalhos](#adicionando-novos-atalhos)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Recarregando Alterações](#recarregando-alterações)
8. [Troubleshooting](#troubleshooting)
9. [Referência Rápida](#referência-rápida)

---

## Visão Geral

O arquivo **`.pi/agents/shortcuts.yaml`** é o local centralizado onde você define todos os atalhos de teclado para as extensões do Pi. Isso permite personalizar atalhos sem precisar editar o código-fonte das extensões.

### Vantagens

- ✅ **Centralização**: Todos os atalhos em um único lugar
- ✅ **Personalização Fácil**: Altere atalhos sem tocar no código
- ✅ **Documentação Integrada**: Comentários inline descrevem cada atalho
- ✅ **Recarregamento Dinâmico**: Use `/reload` para aplicar mudanças


---

## Estrutura do Arquivo shortcuts.yaml

### Formato Básico

```yaml
# Comentário descrevendo o grupo de extensão
extension-name:
  - keyId    # Descrição do atalho (opcional)
  - keyId    # Outro atalho para a mesma ação

another-extension:
  - f1       # Ação primária
  - ctrl+x   # Atalho alternativo
```

### Componentes

| Componente | Descrição | Exemplo |
|------------|-----------|---------|
| **Extension Name** | Identificador da extensão (deve corresponder ao usado em `registerShortcuts()`) | `agent-team` |
| **Key ID** | Identificador do atalho de teclado (formato: `modifier+key`) | `ctrl+x` |
| **Description** | Comentário inline descrevendo a função (opcional) | `# Ciclar para próximo tema` |

---

## Como Editar o Arquivo

### Passo 1: Localizar o Arquivo

O arquivo está localizado em:

```
.pi/agents/shortcuts.yaml
```

### Passo 2: Abrir para Edição

Use seu editor preferido:

```bash
# VS Code
code .pi/agents/shortcuts.yaml

# Vim
vim .pi/agents/shortcuts.yaml

# Nano
nano .pi/agents/shortcuts.yaml
```

### Passo 3: Fazer as Alterações

**⚠️ REGRAS DE OURO:**

1. **Mantenha a indentação consistente** (use espaços, não tabs)
2. **Use letras minúsculas** para modificadores e teclas
3. **Não use teclas reservadas** (veja lista abaixo)
4. **Adicione comentários descritivos** para cada atalho

### Passo 4: Salvar e Recarregar

```bash
/reload
```

---

## Formato dos Key IDs

### Sintaxe

```
modifier+key
```

### Modificadores Disponíveis

| Modificador | Descrição |
|-------------|-----------|
| `ctrl` | Control key |
| `shift` | Shift key |
| `alt` | Alt/Option key |

**Combinando modificadores:**

```yaml
- ctrl+x          # Apenas um modificador
- ctrl+shift+p    # Dois modificadores
- ctrl+alt+delete # Três modificadores
```

### Teclas Disponíveis

#### Letras e Números
- `a-z`: Letras minúsculas
- `0-9`: Dígitos

#### Teclas de Função
- `f1` a `f12`: Teclas de função (recomendado para extensões)

#### Teclas Especiais
- `escape`, `enter`, `tab`, `space`
- `backspace`, `delete`
- `home`, `end`
- `pageUp`, `pageDown`
- `up`, `down`, `left`, `right`

#### Símbolos
- `` ` ``, `-`, `=`, `[`, `]`, `\`, `;`, `'`, `,`, `.`, `/`
- `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `_`, `+`
- `|`, `~`, `{`, `}`, `:`, `<`, `>`, `?`

---

## ⚠️ Teclas Reservadas (NÃO USE)

Estas teclas são reservadas pelo Pi e **não podem ser sobrescritas**:

| Key ID | Ação no Pi |
|--------|------------|
| `escape` | Cancelar/abortar |
| `ctrl+c` | Limpar/copiar |
| `ctrl+d` | Sair |
| `ctrl+z` | Suspender |
| `shift+tab` | Ciclar nível de thinking |
| `ctrl+p` | Ciclar modelo para frente |
| `ctrl+shift+p` | Ciclar modelo para trás |
| `ctrl+l` | Selecionar modelo |
| `ctrl+o` | Expandir ferramentas |
| `ctrl+t` | Toggle thinking |
| `ctrl+g` | Editor externo |
| `alt+enter` | Mensagem de follow-up |
| `enter` | Enviar mensagem |
| `ctrl+k` | Deletar até o fim da linha |

**💡 Dica:** Se você tentar usar uma tecla reservada, ela será silenciosamente ignorada.

---

## ✅ Teclas Seguras (Recomendadas)

### Teclas de Função (F1-F12)

**Altamente recomendadas** — Todas estão livres por padrão:

```yaml
my-extension:
  - f1    # Ação principal
  - f2    # Ação secundária
  - f3    # Ação terciária
  # ... até f12
```

### Combinações Ctrl+Letra

A maioria está disponível (exceto as reservadas):

```yaml
my-extension:
  - ctrl+x    # ✓ Disponível
  - ctrl+q    # ✓ Disponível
  - ctrl+h    # ⚠️ Pode ser interceptado por alguns terminais
```

**⚠️ EVITE:** `ctrl+letter` em terminais macOS com atalhos do sistema


---

## Adicionando Novos Atalhos

### Cenário 1: Alterar Atalho Existente

**Antes:**
```yaml
theme-cycler:
  - ctrl+x   # Cycle theme forward
  - ctrl+q   # Cycle theme backward
```

**Depois (mudando para F-keys):**
```yaml
theme-cycler:
  - f9       # Cycle theme forward
  - f10      # Cycle theme backward
```

### Cenário 2: Adicionar Atalho para Nova Extensão

**1. Crie a extensão** (`extensions/my-tool.ts`):

```typescript
import { registerShortcuts } from "./shortcutLoader.ts";

pi.on("session_start", async (_event, ctx) => {
  registerShortcuts(pi, "my-tool", {
    "f1": {
      handler: async (shortcutCtx) => {
        if (!shortcutCtx.hasUI) return;
        pi.tui().notify("Minha ferramenta ativada!");
      }
    },
    "ctrl+shift+m": {
      description: "Mostrar menu",
      handler: async (shortcutCtx) => {
        if (!shortcutCtx.hasUI) return;
        // Mostrar menu
      }
    },
  }, ctx.cwd);
});
```

**2. Adicione os atalhos ao YAML:**

```yaml
# ────────────────────────────────────────────────────────────────────────────────
# My Tool Extension (extensions/my-tool.ts)
# ────────────────────────────────────────────────────────────────────────────────
my-tool:
  - f1               # Ativar ferramenta
  - ctrl+shift+m     # Mostrar menu
```

**3. Recarregue:**

```bash
/reload
```

### Cenário 3: Múltiplos Atalhos para Mesma Ação

```yaml
# ────────────────────────────────────────────────────────────────────────────────
# Navigator Extension (extensions/navigator.ts)
# ────────────────────────────────────────────────────────────────────────────────
navigator:
  - f1           # Voltar (atalho primário)
  - ctrl+left    # Voltar (alternativa)
  - alt+left     # Voltar (terceira opção)
  
  - f2           # Avançar
  - ctrl+right   # Avançar (alternativa)
```

---

## Exemplos Práticos

### Exemplo 1: Extensão de Gerenciamento de Janelas

```yaml
# ────────────────────────────────────────────────────────────────────────────────
# Window Manager Extension (extensions/window-mgr.ts)
# ────────────────────────────────────────────────────────────────────────────────
window-mgr:
  - ctrl+shift+n   # Nova janela
  - ctrl+shift+w   # Fechar janela
  - ctrl+tab       # Ciclar janelas
  - ctrl+shift+tab # Ciclar janelas (reverso)
  - f5             # Maximizar janela
  - f6             # Minimizar janela
```

### Exemplo 2: Extensão de Edição

```yaml
# ────────────────────────────────────────────────────────────────────────────────
# Quick Editor Extension (extensions/quick-editor.ts)
# ────────────────────────────────────────────────────────────────────────────────
quick-editor:
  - f1          # Salvar
  - f2          # Desfazer
  - f3          # Refazer
  - f4          # Buscar
  - f5          # Substituir
  - ctrl+s      # Salvar (alternativa)
  - ctrl+z      # Desfazer (alternativa)
```

### Exemplo 3: Extensão com Atalhos Contextuais

```yaml
# ────────────────────────────────────────────────────────────────────────────────
# Context Tools Extension (extensions/context-tools.ts)
# ────────────────────────────────────────────────────────────────────────────────
context-tools:
  - f1              # Analisar seleção atual
  - f2              # Explicar código selecionado
  - f3              # Documentar função atual
  - ctrl+shift+a    # Analisar todo o arquivo
  - ctrl+shift+e    # Explicar todo o arquivo
```

### Exemplo 4: Extensão de Productivity

```yaml
# ────────────────────────────────────────────────────────────────────────────────
# Productivity Booster Extension (extensions/productivity-booster.ts)
# ────────────────────────────────────────────────────────────────────────────────
productivity-booster:
  - f1              # Iniciar Pomodoro
  - f2              # Pausar Pomodoro
  - f3              # Ver estatísticas
  - f4              # Criar nota rápida
  - f5              # Buscar notas
  - ctrl+p          # Toggle Pomodoro (alternativa)
```

---

## Recarregando Alterações

### Método 1: Comando /reload (Recomendado)

Após editar `shortcuts.yaml`, simplesmente digite no chat:

```bash
/reload
```

**O que acontece:**
1. Pi recarrega todas as extensões
2. Cada extensão relê o arquivo `shortcuts.yaml`
3. Novos atalhos são registrados
4. Atalhos removidos são desregistrados

### Método 2: Reiniciar Pi

Se `/reload` não funcionar:

```bash
# Saia do Pi (ctrl+d ou /exit)
# Reinicie com:
pi -e extensions/sua-extensão.ts
```

### Método 3: Recarregamento Seletivo

Se você tem múltiplas extensões e quer recarregar apenas uma:

```bash
# Descarregue a extensão
/unload extensions/sua-extensão.ts

# Carregue novamente
/load extensions/sua-extensão.ts
```


---

## Troubleshooting

### ❌ Problema: Atalhos Não Funcionam

#### Possível Causa 1: Tecla Reservada

**Sintoma:** O atalho não faz nada, sem erro.

**Solução:**
```bash
# Verifique se a tecla está reservada
# Consulte a seção "Teclas Reservadas" acima
```

**Exemplo de correção:**
```yaml
# ❌ ERRADO (ctrl+l é reservado)
my-extension:
  - ctrl+l   # Não vai funcionar

# ✅ CORRETO
my-extension:
  - f1       # Use F-key em vez disso
```

#### Possível Causa 2: Erro de Sintaxe no YAML

**Sintoma:** `/reload` mostra erro de parse.

**Solução:**
```bash
# Verifique:
# 1. Indentação consistente (use espaços, não tabs)
# 2. Dois pontos após o nome da extensão
# 3. Hífen antes de cada keyId
# 4. Formato correto: modifier+key (minúsculas)
```

**Exemplo de correção:**
```yaml
# ❌ ERRADO
my-extension
  - f1
  - Ctrl+X    # Maiúsculas errado

# ✅ CORRETO
my-extension:
  - f1
  - ctrl+x    # Minúsculas correto
```

#### Possível Causa 3: Extensão Não Registrou os Atalhos

**Sintoma:** Atalhos não aparecem mesmo após `/reload`.

**Solução:**
```typescript
// Verifique se registerShortcuts está sendo chamado em session_start
pi.on("session_start", async (_event, ctx) => {
  // ❌ ERRADO (fora de session_start)
  // registerShortcuts(...);
});

pi.on("session_start", async (_event, ctx) => {
  // ✅ CORRETO (dentro de session_start)
  registerShortcuts(pi, "my-extension", {
    "f1": { handler: async (shortcutCtx) => { /* ... */ } },
  }, ctx.cwd);
});
```

#### Possível Causa 4: Nome da Extensão Incorreto

**Sintoma:** Atalhos não são carregados.

**Solução:**
```yaml
# No YAML:
my-extension:
  - f1
```

```typescript
// No código TypeScript - deve ser IGUAL ao YAML
registerShortcuts(pi, "my-extension", { // ← Deve bater com YAML
  "f1": { handler: async (ctx) => { /* ... */ } },
}, ctx.cwd);
```

---

### ⚠️ Problema: Conflitos em macOS

**Sintoma:** `alt+letter` digita caracteres especiais em vez de ativar atalho.

**Causa:** Terminais macOS interceptam `alt+letter` para caracteres acentuados.

**Solução:**
```yaml
# ❌ EVITE em macOS
my-extension:
  - alt+a    # Pode digitar 'å' em vez de ativar

# ✅ USE estas alternativas
my-extension:
  - f1           # Function keys - sempre funcionam
  - ctrl+a       # Ctrl+letter - funciona em todos os terminais
```

**Terminais com suporte completo a `alt`:**
- Kitty
- WezTerm
- Ghostty
- ITerm2 (com configuração específica)

---

### 🔍 Problema: Verificar Quais Atalhos Estão Carregados

**Solução 1: Use a extensão test-shortcuts**

```bash
# Carregue a extensão
pi -e extensions/test-shortcuts.ts

# Pressione F10 para listar todos os atalhos carregados
```

**Solução 2: Adicione log na sua extensão**

```typescript
pi.on("session_start", async (_event, ctx) => {
  const shortcuts = loadShortcuts("my-extension", ctx.cwd);
  console.log(`Atalhos carregados para my-extension:`, Array.from(shortcuts.entries()));
  // ...
});
```

**Solução 3: Use o modo verbose do Pi**

```bash
pi -e extensions/sua-extensão.ts --verbose
```

---

### 🐛 Problema: Alterações no YAML Não São Aplicadas

**Sintoma:** Você editou `shortcuts.yaml` mas `/reload` não aplica mudanças.

**Solução:**
```bash
# 1. Verifique se editou o arquivo correto
# Caminho: .pi/agents/shortcuts.yaml (não .pi/agent/)

# 2. Verifique permissões do arquivo
ls -la .pi/agents/shortcuts.yaml

# 3. Tente recarregar completamente
/reload

# 4. Se ainda não funcionar, reinicie Pi
# Saia (ctrl+d) e execute:
pi -e extensions/sua-extensão.ts
```

---

## Referência Rápida

### Template Básico

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Minha Extensão
# ═══════════════════════════════════════════════════════════════════════════════
#
# Descrição geral da extensão e seus atalhos.
#
# Atalhos:
#   - f1: Ação principal
#   - f2: Ação secundária
#
# ═══════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────────
# My Extension (extensions/my-extension.ts)
# ────────────────────────────────────────────────────────────────────────────────
my-extension:
  - f1          # Descrição da ação
  - f2          # Outra ação
```

### Checklist de Edição

- [ ] Use minúsculas para modificadores e teclas
- [ ] Não use teclas reservadas
- [ ] Mantenha indentação consistente
- [ ] Adicione comentários descritivos
- [ ] Teste após editar com `/reload`
- [ ] Verifique logs com `--verbose` se necessário

### Key IDs Válidos

```
Formato: [modifier+]key

Modifiers: ctrl, shift, alt (combinável)
Keys:
  - a-z, 0-9
  - f1-f12
  - escape, enter, tab, space, backspace, delete
  - home, end, pageUp, pageDown
  - up, down, left, right
  - Símbolos: ` - = [ ] \ ; ' , . / ! @ # $ % ^ & * ( ) _ + | ~ { } : < > ?
```

### Teclas Reservadas (Quick Reference)

```
escape, ctrl+c, ctrl+d, ctrl+z, shift+tab
ctrl+p, ctrl+shift+p, ctrl+l, ctrl+o, ctrl+t
ctrl+g, alt+enter, enter, ctrl+k
```

---

## 📚 Recursos Adicionais

### Arquivos Relacionados

- **`.pi/agents/shortcuts.yaml`** - Configuração de atalhos
- **`extensions/shortcutLoader.ts`** - Módulo para carregar atalhos
- **`extensions/agent-team.ts`** - Exemplo de uso
- **`extensions/theme-cycler.ts`** - Outro exemplo de uso
- **`extensions/test-shortcuts.ts`** - Teste e debug de atalhos

### Documentação do Pi

- **`.pi/agents/SHORTCUTS.md`** - Documentação técnica do formato
- **Pi docs: `keybindings.md`** - Referência completa de keybindings

### Comandos Úteis

```bash
# Editar shortcuts.yaml
code .pi/agents/shortcuts.yaml

# Recarregar após alterações
/reload

# Ver atalhos carregados (com test-shortcuts)
# Pressione F10

# Modo verbose para debug
pi -e extensions/sua-extensão.ts --verbose
```

---

## 💡 Dicas de Boas Práticas

1. **Use F-Keys para Extensões**: `f1-f12` são universalmente disponíveis e não conflitam com atalhos do sistema.

2. **Documente Sempre**: Adicione comentários descritivos para cada atalho.

3. **Seja Consistente**: Use padrões similares em extensões relacionadas (ex: `f1-f5` para navegação, `f6-f10` para edição).

4. **Teste em Múltiplos Terminais**: Especialmente se usar `alt` ou `shift` modifiers.

5. **Evite Sobrecarregar**: Não use todos os F-keys de uma vez. Deixe espaço para futuras extensões.

6. **Use Alternativas**: Forneça múltiplos atalhos para ações importantes (ex: `f1` e `ctrl+s` para salvar).

7. **Pense em Acessibilidade**: Alguns usuários podem ter dificuldade com combinações complexas. Forneça opções simples.

---

**Última atualização:** 2026-04-02  
**Versão do shortcuts.yaml:** 1.0  
**Maintainer:** Pi Extension Playground Team
