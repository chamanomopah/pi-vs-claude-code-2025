# Checklist de Testes: Skills por Agente

## Status da Implementação: ✅ COMPLETA (Código)
## Status dos Testes: ⏳ PENDENTE (Execução Real)

---

## Preparação

- [ ] Backup do estado atual do projeto
- [ ] Fechar todas as instâncias do Pi
- [ ] Limpar sessões de agentes: `rm -rf .pi/agent-sessions/*.json`

---

## Teste 1: Carregar a Extensão

**Objetivo**: Verificar se a extensão carrega sem erros

```bash
pi -e extensions/agent-team.ts
```

- [ ] Extensão carrega sem erros de sintaxe
- [ ] Widget do agent-team aparece
- [ ] Time correto é carregado (ver teams.yaml)
- [ ] Status mostra: "Team: <nome> (N agentes)"

**Se falhar:**
- Verificar erros de TypeScript no console
- Verificar se `extensions/agent-team.ts` existe
- Verificar dependências instaladas

---

## Teste 2: Verificar System Prompt do Dispatcher

**Objetivo**: Confirmar que o catálogo de skills aparece no system prompt

Quando o Pi iniciar, o system prompt deve conter:

- [ ] Seção "## Agents (with skills)"
- [ ] Lista de agentes com skills
- [ ] Formato: `**Skills:** skill1, skill2`

**Exemplo esperado:**
```
## Agents (with skills)

### Builder
**Dispatch as:** `builder`
Implementation and code generation
**Skills:** 5-min-scripts
```

**Se falhar:**
- Verificar se agentes têm `skills:` no frontmatter
- Verificar se o parser está lendo corretamente
- Verificar console para erros de parsing

---

## Teste 3: Dispatcher Não Tem Skills

**Objetivo**: Confirmar que o dispatcher NÃO tem as skills carregadas

- [ ] Dispatcher tem apenas a tool `dispatch_agent`
- [ ] Dispatcher NÃO tem acesso a comandos do `5-min-scripts`
- [ ] Dispatcher NÃO tem acesso ao `bowser`

**Como testar:**
```
/dispatch
"Qual skills você tem disponíveis?"
```

Resposta esperada: Dispatcher deve dizer que só pode dispatchar para outros agentes.

---

## Teste 4: Dispatch para Agente com Skill

**Objetivo**: Verificar que skills são passadas corretamente

### 4a. Testar Builder com 5-min-scripts

```
/dispatch builder "Crie um script em Python para listar todos os arquivos .ts"
```

- [ ] Dispatch inicia sem erros
- [ ] Agente builder recebe a task
- [ ] Agente tem acesso à skill `5-min-scripts`
- [ ] Script é criado e testado
- [ ] Resultado é retornado ao dispatcher

### 4b. Testar Bowser com Bowser Skill

```
/dispatch bowser "Tire um screenshot de example.com"
```

- [ ] Dispatch inicia sem erros
- [ ] Agente bowser recebe a task
- [ ] Agente tem acesso à skill `bowser`
- [ ] Playwright é executado
- [ ] Screenshot é criado

---

## Teste 5: Verificar Flags no Subprocesso

**Objetivo**: Confirmar que flags `--skill` são passadas

- [ ] Monitorar processo do Pi (ps aux | grep pi)
- [ ] Verificar que argumentos incluem `--skill 5-min-scripts`
- [ ] Verificar que cada skill tem sua própria flag

**Como testar:**
```bash
# Em outro terminal, monitorar processos
watch -n 1 'ps aux | grep "pi.*--skill"'
```

---

## Teste 6: Agentes Sem Skills

**Objetivo**: Verificar que agentes sem skills funcionam normalmente

```
/dispatch scout "Explore a estrutura do projeto"
```

- [ ] Dispatch funciona
- [ ] Scout NÃO tem flags `--skill`
- [ ] Scout executa sua tarefa normalmente
- [ ] Nenhum erro relacionado a skills

---

## Teste 7: Múltiplas Skills

**Objetivo**: Se existir agente com múltiplas skills

Adicionar ao frontmatter de um agente de teste:
```yaml
skills:
 - 5-min-scripts
 - bowser
```

- [ ] Parser lê ambas as skills
- [ ] Dispatch passa ambas as flags: `--skill 5-min-scripts --skill bowser`
- [ ] Agente tem acesso a ambas as skills

---

## Teste 8: Skill Inexistente (Erro Esperado)

**Objetivo**: Verificar comportamento com skill inválida

Adicionar ao frontmatter:
```yaml
skills:
 - skill-inexistente-xyz
```

- [ ] Pi retorna erro ao tentar carregar a skill
- [ ] Mensagem de erro é clara sobre skill não encontrada
- [ ] Dispatcher não quebra, apenas o agente falha

---

## Teste 9: Formatos de Frontmatter

**Objetivo:** Validar diferentes formatos de skills

### 9a. YAML Array
```yaml
skills:
 - 5-min-scripts
 - bowser
```
- [ ] Funciona corretamente

### 9b. Comma-separated
```yaml
skills: 5-min-scripts, bowser
```
- [ ] Funciona corretamente

### 9c. Single Skill
```yaml
skills: 5-min-scripts
```
- [ ] Funciona corretamente

### 9d. Singular
```yaml
skill: 5-min-scripts
```
- [ ] Funciona corretamente

---

## Teste 10: Recarregar Agentes

**Objetivo**: Verificar que mudanças em skills são recarregadas

1. Adicionar skill a um agente
2. Executar `/agent-team-reload`
3. Verificar system prompt atualizado

- [ ] `/agent-team-reload` funciona
- [ ] Skills atualizadas aparecem no catálogo
- [ ] Dispatch usa novas skills

---

## Teste 11: Performance

**Objetivo**: Verificar que skills não impactam performance do dispatcher

- [ ] Dispatcher inicia rapidamente
- [ ] System prompt não está excessivamente grande
- [ ] Dispatch de agentes é rápido
- [ ] Subprocesso do agente tem skills disponíveis

**Métricas esperadas:**
- Startup do dispatcher: < 2 segundos
- System prompt: < 5000 tokens
- Dispatch até agente pronto: < 3 segundos

---

## Teste 12: Casos de Edge

### 12a. Skills com Whitespace
```yaml
skills:
  -  5-min-scripts
  - bowser
```
- [ ] Whitespace é removido corretamente

### 12b. Skills Vazias
```yaml
skills:
 -
```
- [ ] Skills vazias são filtradas
- [ ] Nenhum erro é lançado

### 12c. Skills em Branco
```yaml
skills:
```
- [ ] Retorna array vazio
- [ ] Nenhum erro é lançado

---

## Resultados Esperados

### Sucesso
- ✅ Extensão carrega sem erros
- ✅ System prompt mostra catálogo de skills
- ✅ Dispatcher NÃO tem skills carregadas
- ✅ Agentes com skills recebem flags `--skill`
- ✅ Skills funcionam no subprocesso do agente
- ✅ Agentes sem skills funcionam normalmente

### Falha (Ações Corretivas)
- ❌ Erro de sintaxe → Revisar código TypeScript
- ❌ Skills não aparecem → Verificar parser de frontmatter
- ❌ Dispatcher tem skills → Revisar before_agent_start
- ❌ Flags não passam → Revisar dispatchAgent()
- ❌ Skill não funciona → Verificar nome da skill em .pi/skills/

---

## Logs Úteis para Debug

### Ativar verbose logging
```bash
PI_VERBOSE=1 pi -e extensions/agent-team.ts
```

### Ver system prompt
```
/system
```

### Listar agentes
```
/agents-list
```

### Ver time ativo
```
/agents-team
```

---

## Conclusão

Após completar todos os testes:

- [ ] Todos os testes críticos (1-6) passam
- [ ] Testes de formato (9) passam
- [ ] Casos de edge (12) são tratados corretamente
- [ ] Performance é aceitável (11)
- [ ] Documentação está atualizada

**Se SIM**: Implementação está pronta para produção! 🎉

**Se NÃO**: Abrir issue com detalhes do teste que falhou.
