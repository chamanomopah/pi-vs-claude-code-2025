# Fix Agent Teams List - Scripts

Script interativo para resolver o problema onde agentes não aparecem na lista "Members with skills" da extensão Agent Teams.

## 🎯 O Problema

A extensão `agent-team.ts` filtra agentes pelo campo `skills`, mostrando apenas "none" quando a maioria dos agentes não define esse campo no frontmatter.

## 📁 Arquivos

- **`fix-agent-teams-list.ts`** - Versão TypeScript (recomendado)
- **`fix-agent-teams-list.sh`** - Versão Bash (alternativa leve)

## 🚀 Uso Rápido

### Opção A: Adicionar skills aos agentes (Recomendado)

```bash
# TypeScript
bun run scripts/fix-agent-teams-list.ts A

# Bash
./scripts/fix-agent-teams-list.sh A
```

**O que faz:** Adiciona `skills: - generic` ao frontmatter de todos os agentes que não têm skills definidos.

### Opção B: Modificar agent-team.ts (Mostrar todos os agentes)

```bash
# TypeScript
bun run scripts/fix-agent-teams-list.ts B

# Bash
./scripts/fix-agent-teams-list.sh B
```

**O que faz:** Remove o filtro de skills em `agent-team.ts`, fazendo com que TODOS os agentes apareçam na lista.

### Opção C: Gerar Relatório

```bash
# TypeScript
bun run scripts/fix-agent-teams-list.ts C

# Bash
./scripts/fix-agent-teams-list.sh C
```

**O que faz:** Cria um relatório detalhado mostrando quais agentes têm/don't tem skills.

Relatório salvo em: `.pi/reports/agent-skills-report_[TIMESTAMP].txt`

### Rollback (Desfazer alterações)

```bash
# TypeScript
bun run scripts/fix-agent-teams-list.ts R

# Bash
./scripts/fix-agent-teams-list.sh R
```

**O que faz:** Restaura arquivos a partir dos backups em `.pi/backups/`

## 📋 Menu Interativo

Para ver as opções disponíveis:

```bash
# Sem argumentos mostra o menu
bun run scripts/fix-agent-teams-list.ts
./scripts/fix-agent-teams-list.sh
```

Saída:
```
════════════════════════════════════════════════════════════
  Agent Teams List - Fix Script
════════════════════════════════════════════════════════════

This script fixes the issue where agents don't appear in
the 'Members with skills' list.

Choose an option:
  A - Add default 'skills' field to agents without it
  B - Modify agent-team.ts to show ALL agents (remove filter)
  C - Generate report of agents with/without skills
  R - Rollback from backup
  Q - Quit
```

## 🛡️ Recursos de Segurança

### Backup Automático

Todos os scripts criam backups automáticos antes de modificar arquivos:

- **Localização:** `.pi/backups/`
- **Naming:** `[filename]_[timestamp].bak`
- **Manifest:** `backup-manifest-[timestamp].json`

Exemplo de manifesto:
```json
{
  "timestamp": "2025-01-08T10:30:45.123-03:00",
  "action": "add-skills",
  "defaultSkill": "generic",
  "backups": [
    {"original": ".pi/agents/scout.md", "backup": ".pi/backups/scout.md_20250108-103045.bak"}
  ]
}
```

### Rollback

Para desfazer alterações:

```bash
# Usa o backup mais recente
bun run scripts/fix-agent-teams-list.ts R
```

Ou manualmente:
```bash
# Listar backups
ls -la .pi/backups/

# Restaurar manualmente
cp .pi/backups/scout.md_20250108-103045.bak .pi/agents/scout.md
```

## 📊 Exemplo de Relatório

Ao executar a Opção C, você verá:

```
════════════════════════════════════════════════════════════
  Opção C: Relatório de Skills
════════════════════════════════════════════════════════════

ℹ Found 12 agent(s)

Total agents found: 12

✓ Agents WITH skills (2):

  builder
    ├─ File: .pi/agents/builder.md
    └─ Skills: ["5-min-scripts"]

  flowchart
    ├─ File: .pi/agents/flowchart.md
    └─ Skills: ["mermaid", "diagrams"]

────────────────────────────────────────────────────────────────────

✗ Agents WITHOUT skills (10):

  scout
    └─ File: .pi/agents/scout.md

  planner
    └─ File: .pi/agents/planner.md

  [...]
```

## 🔧 Comparativo das Opções

| Opção | Prós | Contras | Quando Usar |
|-------|------|---------|-------------|
| **A** - Adicionar skills | • Não modifica código<br>• Fácil de reverter<br>• Preserva filtro original | • Precisa editar cada agente<br>• Skills genéricos | Quando você QUER o filtro de skills |
| **B** - Modificar código | • Uma alteração só<br>• Mostra todos agentes<br>• Skills ficam opcionais | • Modifica código da extensão<br>• Difícil de sync com updates | Quando você quer todos agentes visíveis |
| **C** - Relatório | • Não altera nada<br>• Info completa | • Requer ação manual | Para diagnóstico antes de aplicar A ou B |

## 🎯 Recomendação

**Use a Opção B** se você quer:
- Que TODOS os agentes apareçam na lista
- Uma solução rápida e centralizada
- Skills como campo opcional

**Use a Opção A** se você:
- Quer manter o filtro de skills
- Prefere modificar definições dos agentes
- Precisa de skills específicos por agente

## 📝 Personalização

### Skill Personalizado (Opção A)

```bash
# Adiciona skill "reconnaissance" em vez de "generic"
./scripts/fix-agent-teams-list.sh A reconnaissance

# TypeScript (edita a variável defaultSkill no código)
bun run scripts/fix-agent-teams-list.ts A
```

### Múltiplos Skills por Agente

Edite o arquivo do agente manualmente:

```yaml
---
name: my-agent
description: Meu agente especialista
tools: read,write,bash
skills:
  - skill-1
  - skill-2
  - skill-3
---
```

## 🐛 Troubleshooting

### Script não encontra agentes

Verifique se os diretórios existem:
```bash
ls -la agents/ .claude/agents/ .pi/agents/
```

### Permissão negada no script Bash

```bash
chmod +x scripts/fix-agent-teams-list.sh
```

### TypeScript não encontrado

```bash
# Instalar tsx globalmente
bun add -g tsx

# Ou usar npx
npx tsx scripts/fix-agent-teams-list.ts A
```

### Rollback não funciona

Verifique se os backups existem:
```bash
ls -la .pi/backups/
cat .pi/backups/backup-manifest-*.json
```

## 📚 Arquivos Criados/Modificados

### Ao executar Opção A:

**Modificados:**
- `.pi/agents/[agent].md` - Agentes sem skills recebem `skills: - generic`

**Criados:**
- `.pi/backups/[agent].md_[timestamp].bak` - Backups de cada agente
- `.pi/backups/backup-manifest-[timestamp].json` - Manifesto de backup

### Ao executar Opção B:

**Modificados:**
- `extensions/agent-team.ts` - Filtro de skills removido

**Criados:**
- `.pi/backups/agent-team.ts_[timestamp].bak` - Backup do arquivo original

### Ao executar Opção C:

**Criados:**
- `.pi/reports/agent-skills-report-[timestamp].txt` - Relatório detalhado

## 🔄 Workflow Sugerido

1. **Diagnóstico:**
   ```bash
   bun run scripts/fix-agent-teams-list.ts C
   ```
   Revise o relatório para entender a situação atual.

2. **Aplicar Solução:**
   ```bash
   bun run scripts/fix-agent-teams-list.ts B  # (recomendado)
   ```

3. **Verificar:**
   - Reinicie o Pi
   - Execute `/agents-list` para ver os agentes
   - Execute `/agents-team` para trocar de time

4. **Reverter se necessário:**
   ```bash
   bun run scripts/fix-agent-teams-list.ts R
   ```
