# Índice: Sistema de Skills por Agente

## 📚 Documentação

### Comece Aqui
1. **[README_SKILLS.md](README_SKILLS.md)** - Resumo executivo (5 min)
2. **[HOW_TO_USE_SKILLS.md](HOW_TO_USE_SKILLS.md)** - Guia de uso prático

### Técnica Detalhada
3. **[SKILLS_IMPLEMENTATION_SUMMARY.md](SKILLS_IMPLEMENTATION_SUMMARY.md)** - Resumo completo
4. **[AGENT_SKILLS_IMPLEMENTATION.md](AGENT_SKILLS_IMPLEMENTATION.md)** - Documentação técnica

### Testes
5. **[TEST_CHECKLIST.md](TEST_CHECKLIST.md)** - Checklist para testes manuais

## 🧪 Testes Automatizados

```bash
# Testar o parser de skills (8 testes)
bun run test-skills-parser-v2.ts

# Testar com agentes reais (5 agentes)
bun run test-real-agents.ts
```

**Status**: ✅ 100% dos testes passando (13/13)

## 🚀 Uso Rápido

### Adicionar Skills a um Agente

```yaml
---
name: meu-agente
skills:
 - 5-min-scripts
 - bowser
---
```

### Usar

```
/dispatch meu-agente "tarefa"
```

## 📋 Skills Disponíveis

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| `5-min-scripts` | `.pi/skills/5-min-scripts/5-min-scripts.md` | Scripts Python rápidos |
| `bowser` | `.pi/skills/bowser/bowser.md` | Automação browser Playwright |

## 👥 Agentes com Skills

| Agente | Skills | Arquivo |
|--------|--------|---------|
| builder | `5-min-scripts` | `.pi/agents/builder.md` |
| bowser | `bowser` | `.pi/agents/bowser.md` |
| documenter | `5-min-scripts` | `.pi/agents/documenter.md` |

## 📁 Estrutura de Arquivos

```
.
├── extensions/
│   └── agent-team.ts                 # Implementação principal
├── .pi/
│   ├── agents/
│   │   ├── builder.md                # Com skills configuradas
│   │   ├── bowser.md                 # Com skills configuradas
│   │   └── documenter.md             # Com skills configuradas
│   └── skills/
│       ├── 5-min-scripts/
│       │   └── 5-min-scripts.md      # Definição da skill
│       └── bowser/
│           └── bowser.md             # Definição da skill
├── INDEX_SKILLS.md                   # Este arquivo
├── README_SKILLS.md                  # Resumo executivo
├── HOW_TO_USE_SKILLS.md              # Guia prático
├── SKILLS_IMPLEMENTATION_SUMMARY.md  # Resumo completo
├── AGENT_SKILLS_IMPLEMENTATION.md    # Doc técnica
├── TEST_CHECKLIST.md                 # Checklist de testes
├── test-skills-parser-v2.ts          # Testes do parser
└── test-real-agents.ts               # Testes com agentes reais
```

## ⚡ Comandos Úteis

```bash
# Carregar extensão com agent-team
pi -e extensions/agent-team.ts

# Ver system prompt (deve mostrar catálogo de skills)
/system

# Listar agentes
/agents-list

# Trocar time
/agents-team

# Recarregar agentes (após mudar skills)
/agent-team-reload

# Dispatch para agente com skills
/dispatch builder "criar script Python"

# Ver agentes com skills
grep -r "skills:" .pi/agents/*.md
```

## ✅ Status da Implementação

| Componente | Status |
|------------|--------|
| Interface `AgentDef` | ✅ |
| Parser de frontmatter | ✅ |
| System prompt dispatcher | ✅ |
| Flags `--skill` no dispatch | ✅ |
| Testes automatizados | ✅ 13/13 |
| Testes manuais | ⏳ Pendente |
| Documentação | ✅ |

## 🎯 Próximos Passos

1. Executar `pi -e extensions/agent-team.ts`
2. Seguir `TEST_CHECKLIST.md` para testes manuais
3. Validar que skills funcionam em execução real
4. Adicionar mais skills conforme necessário

## 🔗 Referências Rápidas

- **Skills**: `.pi/skills/`
- **Agentes**: `.pi/agents/`
- **Código**: `extensions/agent-team.ts`
- **Teams**: `.pi/agents/teams.yaml`

---

**Última atualização**: 2026-04-03
**Versão**: 1.0
**Estratégia**: Skills específicas por agente (Estratégia 1)
