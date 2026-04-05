# Guia Rápido: Skills por Agente

## O Que São Skills?

Skills são módulos especializados que fornecem capacidades específicas aos agentes. Elas são carregadas apenas no subprocesso do agente quando ele é dispatchado, mantendo o dispatcher leve e limpo.

## Skills Disponíveis

### 1. **5-min-scripts**
Scripts rápidos em Python para resolver problemas específicos.

**Quando usar:**
- Criar scripts utilitários simples
- Automatizar tarefas repetitivas
- Prototipar soluções rapidamente

**Exemplo de uso:**
```
"builder, crie um script em Python para renomear arquivos em massa"
```

### 2. **bowser**
Automação headless browser usando Playwright CLI.

**Quando usar:**
- Web scraping
- Screenshots de sites
- Testes de UI
- Automação de navegadores
- Sessões paralelas de browser

**Exemplo de uso:**
```
"bowser, tire um screenshot da homepage do google.com"
```

## Adicionar Skills a um Agente

Edite o arquivo `.md` do agente em `.pi/agents/`:

```yaml
---
name: meu-agente
description: Descrição do agente
tools: read,write,edit
skills:
 - 5-min-scripts
 - bowser
---
```

### Formatos Suportados

**YAML array (recomendado):**
```yaml
skills:
 - skill-um
 - skill-dois
```

**Comma-separated:**
```yaml
skills: skill-um, skill-dois
```

**Single skill:**
```yaml
skills: skill-um
```

**Singular (também funciona):**
```yaml
skill: skill-um
```

## Exemplos Práticos

### Exemplo 1: Builder com 5-min-scripts
```yaml
---
name: builder
description: Implementation and code generation
tools: read,write,edit,bash,grep,find,ls
skills:
 - 5-min-scripts
---
```

Quando o dispatcher chamar o builder com uma tarefa que envolve criar scripts, a skill `5-min-scripts` estará disponível automaticamente.

### Exemplo 2: Bowser Agent
```yaml
---
name: bowser
description: Headless browser automation agent
skills:
 - bowser
---
```

O agente bowser tem a skill `bowser` carregada para automatizar navegadores.

## Agentes Com e Sem Skills

### Com Skills (aparecem no catálogo do dispatcher)
- **builder** → `5-min-scripts`
- **bowser** → `bowser`
- **documenter** → `5-min-scripts`

### Sem Skills (não aparecem no catálogo, mas podem ser usados)
- **scout**
- **flowchart**
- E qualquer outro agente sem campo `skills`

## Como Funciona Internamente

1. **Definição**: Skills são declaradas no frontmatter do agente
2. **Parse**: A extensão `agent-team.ts` lê as skills do frontmatter
3. **Dispatch**: Quando o agente é chamado, cada skill recebe uma flag `--skill`
4. **Isolamento**: Skills são carregadas apenas no subprocesso do agente
5. **Dispatcher**: Permanece sem skills, apenas coordena

## Criar Nova Skill

Para criar uma nova skill:

1. Crie o diretório: `.pi/skills/nova-skill/`
2. Crie o arquivo: `.pi/skills/nova-skill/nova-skill.md`
3. Siga o formato:

```markdown
---
name: nova-skill
description: Descrição da skill
allowed-tools: read,write,edit,bash
---

# Nome da Skill

## Propósito
Descreva o que essa skill faz.

## Como Usar
Instruções para o agente usar esta skill.

## Resultado
O que a skill deve produzir.
```

4. Adicione a um agente:
```yaml
skills:
 - nova-skill
```

## Troubleshooting

### Skill não carrega
- Verifique se o nome da skill no frontmatter bate com o nome em `.pi/skills/`
- Verifique se o arquivo `.md` da skill existe

### Erro de skill inexistente
- O Pi retorna erro se uma skill não existe
- Isso é comportamento esperado e ajuda a validar configurações

### Agente não aparece no catálogo
- O dispatcher mostra apenas agentes com skills
- Agentes sem skills ainda podem ser usados manualmente

## Ver Mais

- Implementação técnica: `AGENT_SKILLS_IMPLEMENTATION.md`
- Resumo executivo: `SKILLS_IMPLEMENTATION_SUMMARY.md`
- Código: `extensions/agent-team.ts`
- Skills: `.pi/skills/`
- Agentes: `.pi/agents/*.md`
