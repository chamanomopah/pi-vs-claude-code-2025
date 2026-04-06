---
name: n8n-plan-catalogo
description: Cria Declarative End-to-End n8n Workflow Specification Plans baseados no catálogo de nodes do projeto. Use quando quiser planejar workflows completos ou modificar workflows existentes, usando apenas nodes disponíveis em catalogo_nodes.py.
argument-hint: [workflow_id] [descrição/modificação]
disable-model-invocation: true
allowed-tools: Read, Bash(python:*), AskUserQuestion
---

# N8N Workflow Planner - Catalog-Based

Especialista em criar **Declarative End-to-End n8n Workflow Specification Plans**.

**IMPORTANTE**: Esta skill APENAS gera planos de implementação. Nenhuma modificação será feita no n8n ou nos arquivos do projeto.

## Dois Modos de Operação

### Modo 1: Workflow Novo (sem ID)
Cria um plano do zero para um novo workflow.

```
/n8n-plan-catalogo "quero um workflow que receba leads por webhook e classifique por prioridade"
```

### Modo 2: Modificar Workflow Existente (com ID)
Analisa um workflow existente e cria um plano de modificação.

```
/n8n-plan-catalogo "bhlDnM03ko0aq" "adicionar validação de dados no início"
```

## Catálogo de Nodes

Todos os nodes e parâmetros utilizados nos planos DEVEM estar em `catalogo_nodes.py`. Consulte este catálogo antes de sugerir qualquer solução.

**Regra de Ouro**: Use apenas nodes do catálogo. Em último caso (quando não houver alternativa), pode sugerir nodes externos, mas isso deve ser EXPLÍCITO e JUSTIFICADO.

## Filosofia de Design

### 1. Declarative Workflow Specification
O plano deve descrever:
- **Nome do workflow**
- **Nó inicial** (trigger)
- **Estrutura de decisões** (switches, IFs)
- **Fluxos paralelos** que não convergem (quando aplicável)

### 2. Determinístico e Reprodutível
- Use campos exatos: "these exact fields"
- Defina regras em ordem: "using these rules in order"
- Especifique branching claramente: "X separate branches that do not merge back"
- Remova ambiguidade para garantir execução previsível

### 3. Roteamento Lógico (Decision Engine)
O padrão recomendado segue:
1. **Normalização** → trim strings, lowercase, cast types
2. **Classificação** → compute lane/category/segment
3. **Switch** → rotas independentes baseadas na classificação
4. **Sub-rotas** → cada branch com lógica independente

## Princípios de Qualidade

### Simplicidade e Confiabilidade
- **Mínimo de nodes** para garantir o resultado
- **Mínimo de parâmetros** (mas suficiente para qualidade)
- **Métodos garantidos** de sucesso são valiosos
- **Soluções simples** > soluções complexas

### Trade-offs Opcionais
Pode oferecer variações com mais funcionalidades:
- "Versão simples: X nodes, funcionalidade básica"
- "Versão completa: Y nodes, funcionalidades Z extras"
- Deixe isso EXPLÍCITO no plano

### Anti-Padrões
- ❌ Soluções que dão mínimo trabalho mas não geram o resultado esperado
- ❌ Nodes ou parâmetros desnecessários
- ❌ Fluxos complexos quando simples resolvem
- ❌ Ignorar o catálogo de nodes

## Processo de Planejamento

### Fase 0: Análise de Workflow Existente (APENAS Modo 2)

**Se o usuário fornecer um ID de workflow** (primeiro argumento):

1. **Baixar workflow** usando:
   ```bash
   cd tools\
   python workflow_download.py <workflow_id> --connection
   ```

2. **Ler arquivo `_easy_nodes.md`** gerado para entender:
   - Nodes existentes e seus tipos
   - Conexões entre nodes
   - Fluxo de dados atual
   - Pontos de intervenção possíveis

3. **Identificar pontos de intervenção**:
   - Onde inserir novos nodes (inicio, meio, fim)
   - Quais nodes existentes podem ser reaproveitados
   - Quais conexões precisam ser modificadas
   - Impacto na lógica atual

**IMPORTANTE**: No modo de modificação, o plano deve incluir:
- Seção "Análise Atual" com estrutura do workflow existente
- Seção "Ponto de Intervenção" com onde a modificação será aplicada
- Seção "Nodes Modificados" listando o que será alterado/adicionado

### Fase 1: Entendimento
Converse com o usuário para:
1. Entender o objetivo do workflow
2. Identificar inputs (fields, tipos)
3. Identificar outputs (o que deve acontecer)
4. Clarificar regras de negócio
5. Discutir preferências de simplicidade vs funcionalidade

### Fase 2: Consulta ao Catálogo

### Como Consultar o Catálogo

**Verificar se um node existe**:
```bash
python -c "from catalogo_nodes import resolve_node_type; print(resolve_node_type('webhook'))"
```

**Verificar o connectionType de um node**:
```bash
python -c "from catalogo_nodes import get_connection_type; print(get_connection_type('agent'))"
```

**Listar todos os nodes disponíveis**:
```bash
python catalogo_nodes.py
```

Sempre consulte `catalogo_nodes.py` para:
- Verificar quais nodes estão disponíveis
- Entender os parâmetros de cada node
- Identificar o tipo de conexão (connectionType)
- Confirmar capacidades antes de propor

### Fase 3: Especificação Declarativa

**Para Modo 1 (Novo Workflow)**: Use este template

```markdown
# Plano de Workflow: <Nome do Workflow>

## Resumo
<descrição breve em 1-2 frases>

## Trigger
<tipo de node inicial + o que recebe>

## Campos de Entrada
| Campo | Tipo | Descrição |
|-------|------|----------|
| nome | string | Descrição |

## Fluxo Principal

### 1. Normalização
<passos de limpeza/validação dos dados>

### 2. Classificação
Compute <campo_de_classificacao> using these rules in order:
- set value="X" if <condição 1>;
- else set value="Y" if <condição 2>;
- else set value="Z".

### 3. Roteamento (Switch)
Use a Switch node on <campo_de_classificacao> with <N> separate branches:

#### Branch: <nome_1>
<passos específicos desta branch>

#### Branch: <nome_2>
<passos específicos desta branch>

...

## Nodes Necessários
| Nome | Tipo (do catálogo) | Propósito |
|------|-------------------|-----------|
| <nome> | <tipo> | <descrição> |

## Conexões
| Origem | Destino | Tipo de Conexão |
|--------|---------|----------------|
| <source> | <target> | <main/ai_tool/etc> |

## Parâmetros Principais
| Node | Parâmetro | Valor/Expressão |
|------|-----------|-----------------|
| <node> | <param> | <valor> |

## Considerações Especiais
- <limitações>
- <dependências de credenciais>
- <pontos de atenção>
```

**Para Modo 2 (Modificar Workflow Existente)**: Use este template

```markdown
# Plano de Modificação: <Nome do Workflow>

## Resumo
<descrição breve da modificação em 1-2 frases>

## Análise Atual
- **Workflow**: <nome> (ID: <id>)
- **Nodes existentes**: <quantidade e tipos principais>
- **Fluxo atual**: <descrição do fluxo>
- **Ponto de intervenção**: <onde a modificação será aplicada>

## Nodes Existentes Relevantes
| Nome | Tipo | Propósito Atual |
|------|------|----------------|
| <node1> | <tipo> | <descrição> |

## Modificação Proposta

### 1. O que será adicionado
<descrição da nova funcionalidade>

### 2. Nodes a Criar
| Nome | Tipo (do catálogo) | Propósito |
|------|-------------------|-----------|
| <nome> | <tipo> | <descrição> |

### 3. Conexões a Adicionar/Modificar
| Origem | Destino | Tipo | Ação |
|--------|---------|------|------|
| <source> | <target> | <main> | NOVA |
| <old_source> | <old_target> | <main> | REMOVER |

### 4. Parâmetros a Configurar
| Node | Parâmetro | Valor/Expressão |
|------|-----------|-----------------|
| <node> | <param> | <valor> |

### 5. Nodes a Modificar (se aplicável)
| Node | Modificação | Justificativa |
|------|-------------|----------------|
| <node> | <modificação> | <porquê> |

## Fluxo Modificado
<descrição do novo fluxo com a modificação>
```

### Fase 4: Validação
Antes de finalizar, verifique:
- [ ] Todos os nodes estão em `catalogo_nodes.py`
- [ ] connectionTypes estão corretos para cada node
- [ ] Plano é determinístico (sem ambiguidade)
- [ ] Solução é simples mas completa
- [ ] Trade-offs estão explícitos (se houver)
- [ ] Parâmetros mínimos mas suficientes

## Exemplo de Prompt Declarativo

O usuário pode fornecer prompts como este:

> "Create an n8n workflow called 'Simple Lead Router Demo' that starts with a Webhook receiving JSON with these exact fields:
> fullName (string), email (string), company (string), country (string), budget (number), timeframeDays (number), and message (string).
>
> Normalize the fields (trim strings, lowercase email, cast budget and timeframeDays to numbers) and compute lane using these rules in order:
>
> set lane="Invalid" if email does not contain "@" OR fullName is empty;
> else set lane="HighPriority" if budget > 5000 AND timeframeDays <= 30;
> else set lane="Partner" if message contains (case-insensitive) any of: "sponsor", "partnership", "affiliate", "collab";
> else set lane="Standard".
>
> Then use a Switch node on lane with 4 separate branches that do not merge back.
>
> Invalid branch: add Gmail label lead_invalid, send a short email asking them to resubmit with missing details, and append a row to Google Sheets tab invalid_leads.
>
> HighPriority branch: compute priorityScore (0–100) as min(100, 50 + (budget > 10000 ? 25 : 0) + (timeframeDays <= 14 ? 25 : 0)), send Slack to #leads-high-priority including name, company, score, budget, timeframe, and message, send an email with a Calendly booking link placeholder, and append a row to Google Sheets tab high_priority_leads including priorityScore.
>
> Partner branch: create a Notion page in a database "Partnership Requests" with the lead details, send Slack to #partnerships with the message text, and append a row to Google Sheets tab partner_leads.
>
> Standard branch: run a small "industry guess" step using a simple keyword check on message
> if it contains "real estate" set segment="RealEstate"
> if it contains "law" or "attorney" set segment="Legal"
> else segment="General"
>
> then do a mini Switch on segment to post to different Slack channels (#leads-real-estate, #leads-legal, or #leads-general), send a standard thank-you email, and append a row to Google Sheets tab standard_leads including segment.
>
> Each branch ends independently."

Sua tarefa é traduzir esse prompt declarativo em um plano estruturado usando nodes do catálogo.

## Documentação de Apoio

Durante o planejamento, consulte:
- `catalogo_nodes.py` - Catálogo completo de nodes disponíveis
- `README_CATALOGO.md` - Documentação do catálogo (se existir)
- `README_conectar.md` - Sintaxe de conexões
- `README_parameters.md` - Sintaxe de parâmetros

## Comportamento Esperado

1. **SEMPRE consulte o catálogo** antes de sugerir nodes
2. **NUNCA proponha nodes** que não estejam no catálogo (exceto com justificativa explícita)
3. **SEMPRE prefira simplicidade** com garantia de resultado
4. **NUNCA implemente** - apenas gere o plano.md
5. **SEMPRE seja determinístico** - regras claras, sem ambiguidade
6. **Use AskUserQuestion** para decidir entre simples vs completo quando houver trade-off
7. **No modo de modificação**: SEMPRE baixe e analise o workflow existente antes de propor mudanças
8. **No modo de modificação**: SEMPRE identifique claramente o ponto de intervenção
9. **No modo de modificação**: SEMPRE verifique se nodes existentes podem ser reaproveitados

## Salvando o Plano

Ao final, salve o plano em um arquivo `.md`:

**Modo 1 (Novo Workflow)**:
- Nome: `<nome-do-workflow>-plano.md`
- Local: Diretório de trabalho atual

**Modo 2 (Modificação)**:
- Nome: `<nome-do-workflow>-modificação-<descrição>-plano.md`
- Local: Diretório de trabalho atual

O plano deve estar pronto para ser usado pelo comando `/add_existingWorkflow` para implementação.

## Próximos Passos (Implementação)

Após gerar o plano, use o comando **`/add_existingWorkflow`** para implementação:

- **Arquivo**: `.claude/commands/add_existingWorkflow.md`
- **Função**: Cria os arquivos `.nodes`, `.formula`, `.params` e executa os scripts
- **Uso**: `/add_existingWorkflow <workflow_id> <modificação>` (se modificações)
- **Uso**: Manual com os arquivos gerados pelo plano

**Importante**: Esta skill (n8n-plan-catalogo) NÃO implementa. Apenas planeja.

## Diretório de Trabalho

`C:\Users\JOSE\Downloads\cc_n8n_generator\claude_code_n8n_manager\`
