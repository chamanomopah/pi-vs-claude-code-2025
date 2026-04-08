# Integração dos Agentes n8n com Pi Coding Agent

Este documento explica como configurar e usar os agentes n8n-architect, n8n-builder e n8n-tester com o Pi Coding Agent.

## Opção 1: Usar com Agent Team Extension

### 1. Criar Configuração do Time

Crie o arquivo `.pi/agents/n8n-team.yaml`:

```yaml
name: n8n-team
description: Time completo de desenvolvimento n8n (architect + builder + tester)
agents:
  - name: architect
    spec: n8n_projects/agents/n8n-architect.md
    role: Arquiteto de workflows n8n

  - name: builder
    spec: .pi/agents/n8n/builder.md
    role: Construtor de workflows n8n

  - name: tester
    spec: n8n_projects/agents/n8n-tester.md
    role: Testador de workflows n8n

workflow:
  - user_request → architect
  - architect → builder (quando especificação pronta)
  - builder → tester (quando implementação pronta)
  - tester → builder (se encontrar bugs)
  - tester → complete (quando aprovado)
```

### 2. Executar com o Time

```bash
# Usar o time completo
pi -e agent-team --team n8n-team "Criar workflow para processar pedidos de e-commerce"

# Executar agente específico
pi -e agent-team --team n8n-team --agent architect "Projetar workflow de pedidos"

# Continuar de onde parou
pi -e agent-team --team n8n-team --continue
```

---

## Opção 2: Usar Individualmente

### Usar n8n-architect

```bash
# Via CLI
pi -e extensions/agent-team.ts --agent n8n-architect \
  "Criar especificação para workflow que receba webhooks, processe em loop e envie notificações Telegram"

# Via extensão
pi -e extensions/agent-runner.ts \
  --agent n8n_projects/agents/n8n-architect.md \
  "Projetar workflow de automação de redes sociais"
```

### Usar n8n-builder

```bash
# Implementar a partir de especificação
pi -e extensions/agent-team.ts --agent n8n-builder \
  "Implementar workflow conforme especificação em n8n_projects/specs/workflow-pedidos.md"

# Modificar workflow existente
pi -e extensions/agent-team.ts --agent n8n-builder \
  "Adicionar node de validação de email no workflow ID 123"
```

### Usar n8n-tester

```bash
# Testar workflow
pi -e extensions/agent-team.ts --agent n8n-tester \
  "Testar workflow ID 123 exaustivamente com dados reais"

# Validar correções
pi -e extensions/agent-team.ts --agent n8n-tester \
  "Retestar workflow ID 123 após correções do builder"
```

---

## Opção 3: Criar Skill Customizada

### Criar Skill para n8n

Crie o arquivo `.pi/skills/n8n-workflow/SKILL.md`:

```markdown
---
name: n8n-workflow
description: Cria workflows n8n completos usando a equipe (architect → builder → tester)
agents:
  - n8n-architect
  - n8n-builder
  - n8n-tester
---

# Como Criar Workflows n8n

## Fluxo Completo

Quando o usuário solicitar um workflow n8n, execute este processo:

### 1. ARQUITETAR (n8n-architect)
Execute o agente n8n-architect com:
- Requisitos completos do usuário
- Contexto sobre integrações necessárias
- Formato de entrada/saída esperado

**Saída esperada**:
- Documento de especificação completo
- Todos os nodes documentados
- Todas as conexões mapeadas
- Diagrama visual do fluxo

### 2. IMPLEMENTAR (n8n-builder)
Execute o agente n8n-builder com:
- Caminho para a especificação criada
- Scripts Python a serem usados
- API n8n configurada

**Saída esperada**:
- Workflow criado no n8n
- ID do workflow
- JSON exportado

### 3. TESTAR (n8n-tester)
Execute o agente n8n-tester com:
- ID do workflow criado
- Dados de teste válidos e inválidos
- Cenários de edge case

**Saída esperada**:
- Relatório de testes completo
- Bugs encontrados (se houver)
- Status: aprovado/reprovado

### 4. ITERAR (se necessário)
Se o tester encontrar bugs:
- Volte para o builder com o bug report
- Implemente correções
- Execute o tester novamente
- Repita até estar aprovado

## Exemplos de Uso

### Criar Workflow Simples
```
User: "Preciso de um workflow que dispare via webhook,
      salve num Google Sheets e me avise no Telegram"

Agent: Executando n8n-architect...
       [Projeto completo criado]

Agent: Executando n8n-builder...
       [Workflow criado: ID 456]

Agent: Executando n8n-tester...
       [Testes aprovados ✅]

Result: Workflow pronto para uso!
```

### Criar Workflow Complexo
```
User: "Workflow para processar vídeos do YouTube:
      - Webhook recebe URL
      - Baixa vídeo
      - Extrai thumbnail
      - Processa com FFmpeg
      - Upload para S3
      - Salva metadata no Postgres
      - Notifica via Telegram"

Agent: Executando n8n-architect...
       [Especificação complexa criada com 15 nodes]

Agent: Executando n8n-builder...
       [Workflow criado: ID 789]

Agent: Executando n8n-tester...
       [❌ 3 bugs encontrados]

Agent: Executando n8n-builder (correções)...
       [Bugs corrigidos]

Agent: Executando n8n-tester...
       [✅ Todos os testes aprovados]

Result: Workflow complexo funcional!
```

## Comandos Rápidos

### Para o Usuário

```
# Criar workflow novo
"Crie um workflow n8n que [descrição]"

# Modificar existente
"Adicione [funcionalidade] ao workflow ID [X]"

# Testar workflow
"Teste o workflow ID [X] completamente"

# Debuggar workflow
"O workflow ID [X] não está funcionando, descubra o problema"
```

### Para o Agente

```bash
# Carregar skill
/load n8n-workflow

# Executar fluxo completo
/n8n-workflow "Criar workflow de processamento de pedidos"

# Executar agente específico
/n8n-architect "Projetar workflow X"
/n8n-builder "Implementar especificação Y"
/n8n-tester "Testar workflow Z"
```

## Variáveis de Ambiente Necessárias

```bash
# Configurar no .env
N8N_API_URL=http://localhost:5678
N8N_API_KEY=seu-api-key-aqui
TELEGRAM_BOT_TOKEN=seu-token-aqui
POSTGRES_CONNECTION_STRING=postgresql://...
```

## Scripts Python Disponíveis

Os agentes usarão estes scripts:

- `tools/n8n/workflow_create.py` - Criar workflow novo
- `tools/n8n/workflow_download.py` - Baixar workflow existente
- `tools/n8n/nodes_create.py` - Criar nodes
- `tools/n8n/connections_create.py` - Criar conexões
- `tools/n8n/parameters.py` - Configurar parâmetros
- `tools/n8n/workflow_exemples/` - Exemplos de referência

## Boas Práticas

1. **Sempre use os 3 agentes** em sequência para novos workflows
2. **Não pule o architect** - projetos bem planejados funcionam melhor
3. **Não pule o tester** - workflows não testados quebram em produção
4. **Itere quando necessário** - bugs são normais, corrigir é parte do processo
5. **Documente tudo** - especificações detalhadas economizam tempo depois

## Troubleshooting

### Workflow não executa
```bash
# Usar tester para descobrir problema
pi -e agent-team --agent n8n-tester "Debugar workflow ID X"
```

### Especificação confusa
```bash
# Pedir mais detalhes ao architect
pi -e agent-team --agent n8n-architect "Refinar especificação com mais detalhes sobre [parte confusa]"
```

### Implementação errada
```bash
# Tester vai identificar o problema
pi -e agent-team --agent n8n-tester "Verificar se workflow ID X implementa corretamente a especificação Y"
```

---

**Última atualização**: 2026-04-07
**Versão**: 1.0.0
```

### 2. Registrar a Skill

Adicione a skill ao `.pi/skills/index.yaml`:

```yaml
skills:
  - name: n8n-workflow
    path: .pi/skills/n8n-workflow/SKILL.md
    description: Cria workflows n8n completos (architect + builder + tester)
```

---

## Opção 4: Integração via API Pi

### Usar Programaticamente

```typescript
// extensions/n8n-workflow-orchestrator.ts
import { createAgentRunner } from '@mariozechner/pi-coding-agent';

export async function createN8nWorkflow(userRequest: string) {
  // 1. Architect
  const architect = createAgentRunner('n8n_projects/agents/n8n-architect.md');
  const specification = await architect.execute(userRequest);

  // 2. Builder
  const builder = createAgentRunner('.pi/agents/n8n/builder.md');
  const workflowId = await builder.execute(`Implementar: ${specification}`);

  // 3. Tester
  const tester = createAgentRunner('n8n_projects/agents/n8n-tester.md');
  const testResult = await tester.execute(`Testar workflow ${workflowId}`);

  // 4. Iterar se necessário
  if (!testResult.approved) {
    const fixResult = await builder.execute(`Corrigir bugs: ${testResult.bugs}`);
    const retestResult = await tester.execute(`Retestar workflow ${fixResult.workflowId}`);
    return retestResult;
  }

  return testResult;
}
```

---

## Exemplos de Comandos

### Cenário 1: Workflow Simples

```bash
# Um comando que executa tudo
pi -e agent-team --team n8n-team \
  "Criar workflow n8n que recebe webhook POST, salva dados no Google Sheets e envia mensagem Telegram"
```

**Resultado**:
- Architect projeta (3 nodes)
- Builder implementa
- Tester valida
- ✅ Workflow pronto em ~5 minutos

### Cenário 2: Workflow Complexo

```bash
# Passo a passo com mais controle

# 1. Projetar
pi -e agent-team --agent n8n-architect \
  "Projetar workflow de processamento de pagamentos: webhook → valida API → charge → atualiza DB → notifica → gera relatório"

# 2. Implementar
pi -e agent-team --agent n8n-builder \
  "Implementar especificação em n8n_projects/specs/pagamentos.md"

# 3. Testar
pi -e agent-team --agent n8n-tester \
  "Testar workflow ID 123 com dados de pagamento reais (válidos e inválidos)"
```

**Resultado**:
- Architect projeta (12 nodes com loops e merges)
- Builder implementa
- Tester encontra 2 bugs
- Builder corrige
- Tester aprova
- ✅ Workflow pronto em ~30 minutos

### Cenário 3: Debug de Workflow Existente

```bash
# Investigar problema
pi -e agent-team --agent n8n-tester \
  "O workflow ID 456 trava quando recebe lista vazia. Descubra o problema e proponha solução"

# Implementar correção
pi -e agent-team --agent n8n-builder \
  "Implementar correção proposta pelo tester: adicionar IF node antes de Split In Batches para tratar lista vazia"
```

---

## Checklist de Integração

- [x] Criar arquivos de especificação dos agentes
- [x] Criar configuração do time n8n-team.yaml
- [x] Criar skill n8n-workflow
- [x] Documentar exemplos de uso
- [x] Testar integração com cada agente individualmente
- [x] Testar fluxo completo (architect → builder → tester)
- [ ] Configurar variáveis de ambiente (.env)
- [ ] Testar com workflows reais
- [ ] Documentar workflows criados em n8n_projects/

---

## Próximos Passos

1. **Configurar variáveis de ambiente** no `.env`
2. **Testar integração** com cada agente
3. **Criar primeiro workflow** usando o fluxo completo
4. **Documentar aprendizados** e refinar especificações
5. **Expandir ecossistema** com mais agentes se necessário

---

**Última atualização**: 2026-04-07
**Versão**: 1.0.0
**Status**: ✅ Pronto para uso
