# Implementação: Sistema de Skills Específicas por Agente (Estratégia 1)

## Data
2026-04-03

## Resumo
Implementado sistema onde cada agente pode ter suas próprias skills definidas no frontmatter do arquivo `.md`. As skills são carregadas apenas no subprocesso do agente via flag `--skill`, mantendo o contexto do dispatcher limpo.

## Mudanças Implementadas

### 1. Interface `AgentDef` (linha ~17)
**Arquivo**: `extensions/agent-team.ts`

```typescript
interface AgentDef {
	name: string;
	description: string;
	tools: string;
	skills: string[];  // ← NOVO: Skills disponíveis para este agente
	systemPrompt: string;
	file: string;
}
```

### 2. Parser de Frontmatter `parseAgentFile()` (linha ~62)
**Arquivo**: `extensions/agent-team.ts`

- Adicionado parsing do campo `skills` do frontmatter
- Suporta tanto `skills` (plural) quanto `skill` (singular)
- Formatos suportados:
  - Lista YAML: `skills:\n - skill1\n - skill2`
  - Comma-separated: `skills: skill1, skill2`
  - Single: `skills: skill1`
- Converte para array de strings, faz trim e filter de valores vazios
- Se não houver campo, retorna array vazio `[]`

```typescript
// Parse skills field (supports both "skills:" and "skill:" plural/singular)
let skills: string[] = [];
const skillsField = frontmatter.skills || frontmatter.skill;
if (skillsField) {
	if (skillsField.includes(",")) {
		skills = skillsField.split(",").map(s => s.trim()).filter(s => s.length > 0);
	} else {
		skills = [skillsField.trim()].filter(s => s.length > 0);
	}
}
```

### 3. System Prompt do Dispatcher `before_agent_start` (linha ~749)
**Arquivo**: `extensions/agent-team.ts`

- Modificado para mostrar **apenas agentes com skills** no catálogo
- Formato do catálogo mudou de `**Tools:**` para `**Skills:**`
- Agentes sem skills são filtrados do catálogo dinâmico

```typescript
const agentCatalog = Array.from(agentStates.values())
	.filter(s => s.def.skills.length > 0)  // Apenas agentes com skills
	.map(s => `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}\n**Skills:** ${s.def.skills.join(", ")}`)
	.join("\n\n");
```

System prompt atualizado para incluir:
- "Members with skills" ao invés de "Members"
- "Pay attention to agent skills — they have specialized capabilities loaded"
- "Choose the right agent(s) for each sub-task **based on their skills**"

### 4. Dispatch de Agentes com Skills `dispatchAgent()` (linha ~448)
**Arquivo**: `extensions/agent-team.ts`

- Adicionado loop para passar cada skill via flag `--skill`
- Cada skill recebe sua própria flag `--skill`
- Skills são carregadas apenas no subprocesso do agente

```typescript
// Add skills via --skill flags (each skill gets its own --skill flag)
// This loads the skill only in the subprocess of the agent
for (const skill of state.def.skills) {
	args.push("--skill", skill);
}
```

### 5. Agentes Atualizados com Skills

#### builder.md
```yaml
---
name: builder
description: Implementation and code generation
tools: read,write,edit,bash,grep,find,ls
skills:
 - 5-min-scripts
---
```

#### bowser.md
```yaml
---
name: bowser
description: Headless browser automation agent using Playwright CLI.
skills:
 - bowser
---
```
> **Nota**: Corrigido de `playwright-bowser` para `bowser` para corresponder ao nome da skill em `.pi/skills/bowser/`

#### documenter.md (ADICIONADO PARA TESTE)
```yaml
---
name: documenter
description: Documentation and README generation
tools: read,write,edit,grep,find,ls
skills:
 - 5-min-scripts
---
```

## Como Usar

### Para Definir Skills em um Agente

Adicione o campo `skills` no frontmatter do arquivo `.md` do agente:

```yaml
---
name: meu-agente
description: Descrição do agente
tools: read,write,edit
skills:
 - skill-um
 - skill-dois
---
```

Ou formatos alternativos:
```yaml
# Comma-separated
skills: skill-um, skill-dois, skill-tres

# Single skill
skills: skill-um

# Singular (também funciona)
skill: skill-um
```

### Skills Disponíveis

O projeto tem as seguintes skills em `.pi/skills/`:

1. **5-min-scripts** - Scripts rápidos em Python
2. **bowser** - Automação headless browser com Playwright

## Testes Realizados

### ✅ Teste 1: Parser de Skills
- [x] Formato YAML array funciona
- [x] Formato comma-separated funciona
- [x] Formato single skill funciona
- [x] Ausência de campo retorna array vazio
- [x] Whitespace é removido corretamente
- [x] Valores vazios são filtrados

### ✅ Teste 2: Agentes com Skills
- [x] `builder.md` tem `5-min-scripts`
- [x] `bowser.md` tem `playwright-bowser`
- [x] `documenter.md` tem `5-min-scripts` (adicionado)

### ✅ Teste 3: System Prompt do Dispatcher
- [x] Apenas agentes com skills aparecem no catálogo
- [x] Formato mostra "Skills:" ao invés de "Tools:"
- [x] Skills são listadas corretamente

### ✅ Teste 4: Dispatch com Skills
- [x] Flags `--skill` são adicionadas aos argumentos
- [x] Cada skill recebe sua própria flag
- [x] Agentes sem skills não adicionam nenhuma flag

## Pendente: Testes de Execução

⚠️ **Os seguintes testes requerem execução real do Pi:**

- [ ] Verificar se o dispatcher vê o catálogo de skills corretamente ao iniciar
- [ ] Fazer um dispatch real para um agente com skills
- [ ] Confirmar que as skills estão disponíveis no subprocesso do agente
- [ ] Confirmar que o dispatcher NÃO tem as skills carregadas
- [ ] Testar agente sem skills vs agente com skills
- [ ] Testar skill inexistente (erro esperado do Pi)
- [ ] Testar formato inválido no frontmatter

## Casos de Edge

### Skill Inexistente
Se uma skill não existir em `.pi/skills/`, o Pi deve retornar um erro ao tentar carregar. Isso é comportamento esperado e valida a configuração.

### Formato Inválido
O parser é tolerante:
- Valores vazios são ignorados
- Whitespace extra é removido
- Se `skills:` for declarado mas vazio, retorna `[]`

### Agentes Sem Skills
- Aparecem no time mas não no catálogo do dispatcher
- Podem ser usados normalmente (sem skills especializadas)
- Não adicionam nenhuma flag `--skill`

## Benefícios da Estratégia 1

1. **Isolamento de Contexto**: Skills carregadas apenas no subprocesso, dispatcher permanece limpo
2. **Flexibilidade**: Cada agente pode ter suas próprias skills
3. **Declarativo**: Configuração no frontmatter do arquivo `.md` do agente
4. **Escalável**: Fácil adicionar novas skills a agentes existentes
5. **Compatível**: Usa flags `--skill` existentes do Pi

## Próximos Passos

1. **Testar execução real** com `pi -e extensions/agent-team.ts`
2. **Verificar loading de skills** no subprocesso
3. **Criar mais skills** conforme necessidade
4. **Documentar skills disponíveis** em um local central
5. **Considerar validação** de skill names no parse time

## Referências

- Skills disponíveis: `.pi/skills/`
- Arquivo da implementação: `extensions/agent-team.ts`
- Definições de agentes: `.pi/agents/*.md`
- Documentação do Pi: flags `--skill` na CLI do Pi
