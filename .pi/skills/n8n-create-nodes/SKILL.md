---
name: n8n-create-nodes
description: Criar arquivo .nodes com definição de nodes N8N. Use para criar novos workflows ou adicionar nodes a workflows existentes.
argument-hint: "nodes-spec [-t workflow] [-s]"
disable-model-invocation: true
allowed-tools: Write, Bash
---

# Criar Arquivo .nodes para N8N

Cria arquivos `.nodes` com a definição de nodes N8N seguindo o formato padrão do sistema.

## Formato do Arquivo .nodes

```nodes
# Comentários começam com #
# Linhas vazias são ignoradas

# Multiplicação com nomes personalizados
(n=nome1,nome2,nome3)agentTool

# Nomes curtos do catálogo
(7=router1,router2,router3,router4,router5,router6,router7)lmChatGoogleGemini
```

## Sintaxe Suportada

| Sintaxe | Descrição |
|---------|-----------|
| `tipo` | Node simples |
| `(n)tipo` | Multiplica n vezes (1, 2, 3...) |
| `(n=)tipo` | Multiplica com sufixo alfabético (1A, 2A...) |
| `(n=a,b,c)tipo` | Multiplica com nomes personalizados |

## Nomes Curtos Disponíveis

### Base N8N
`set`, `httpRequest`, `wait`, `code`, `executeCommand`, `function`, `splitInBatches`, `splitOut`, `if`, `merge`, `switch`, `filter`, `googleSheets`, `slack`, `notion`, `clickUp`, `airtable`, `youTube`, `supabase`, `telegram`, `executeWorkflow`, `webhook`, `respondToWebhook`, `readBinaryFile`, `googleDrive`, `git`, `github`

### Triggers
`scheduleTrigger`, `errorTrigger`, `telegramTrigger`, `googleCalendarTrigger`, `executeWorkflowTrigger`

### AI Tools
`httpRequestTool`, `executeCommandTool`, `slackTool`, `notionTool`, `clickUpTool`, `airtableTool`, `supabaseTool`, `telegramTool`, `googleDriveTool`, `googleTasksTool`, `googleCalendarTool`, `gitTool`, `githubTool`

### LangChain
`agent`, `textClassifier`, `chatTrigger`, `chat`, `lmChatGoogleGemini`, `memoryPostgresChat`, `outputParserStructured`, `toolWorkflow`, `mcpClientTool`, `agentTool`

## Parâmetros Especiais

| Node | Parâmetro | Descrição |
|------|-----------|-----------|
| `merge` | `(n)` | Merge com n entries (2-10) |
| `switch` | `(n)` ou `(n=nomes)` | Switch com n branches (2-10) |
| `textClassifier` | `(n)` ou `(n=cats)` | Classifier com n categorias (2-10) |
| `agent` | `(f)`, `(o)`, `(f\|o)` | Agent com fallback/output parser |

## Estrutura do Arquivo

Use cabeçalho e comentários para organizar:

```nodes
# ============================================================
# ARQUIVO .NODES - DEFINIÇÃO DE NODES A CRIAR
# ============================================================

# --- AGENTTOOLS (Agentes Especializados) ---
# Cada agente precisa de: AgentTool + Router + Memory [+ ExecuteCommand]

(7=agente1,agente2,agente3,agente4,agente5,agente6,agente7)agentTool

# --- ROUTERS (Language Models) ---
(7=router1,router2,router3,router4,router5,router6,router7)lmChatGoogleGemini

# --- MEMÓRIAS (Postgres Chat) ---
(7=memoria1,memoria2,memoria3,memoria4,memoria5,memoria6,memoria7)memoryPostgresChat

# --- EXECUTE COMMAND TOOLS (Opcional) ---
(7=exec1,exec2,exec3,exec4,exec5,exec6,exec7)executeCommandTool
```

## Como Usar o Arquivo Gerado

```bash
# Criar novo workflow
python nodes_create.py workflow.nodes

# Adicionar a workflow existente
python nodes_create.py workflow.nodes -t meu_workflow.json
# Resultado: meu_workflow_nodesAdded.json
```

## Sua Tarefa

Crie um arquivo `.nodes` seguindo o formato acima. O arquivo deve:

1. Ter cabeçalho com comentários explicando o propósito
2. Usar nomes curtos do catálogo
3. Incluir comentários para cada seção
4. Seguir a sintaxe de multiplicação quando apropriado
5. Ser salvo com extensão `.nodes`

Salve o arquivo no diretório atual com nome apropriado.
