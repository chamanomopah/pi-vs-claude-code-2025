---
name: n8n-create-formula
description: Criar arquivo .formula com conexões entre nodes N8N. Use para definir como os nodes se conectam no workflow.
argument-hint: [formula-spec]
disable-model-invocation: true
allowed-tools: Write, Bash
---

# Criar Arquivo .formula para N8N

Cria arquivos `.formula` com as conexões entre nodes N8N seguindo a sintaxe de fórmula.

## Formato do Arquivo .formula

```formula
# ============================================================
# ARQUIVO .FORMULA - CONEXÕES ENTRE NODES
# ============================================================

# Conexão sequencial simples
A>B>C

# Conexões AI
model>agent:ai_languageModel
memory>agent:ai_memory
tool>agent:ai_tool

# Entradas múltiplas (sintaxe <)
agent<(model,memory,tool)
```

## Sintaxe Básica

| Sintaxe | Descrição |
|---------|-----------|
| `A>B` | Conecta A ao B |
| `A>B>C` | Conexão sequencial |
| `A>(B\|C)` | Saídas múltiplas (pipe) |
| `A>(B,C)` | Saídas múltiplas (vírgula) |
| `A<(B,C)` | Entradas múltiplas |
| `A>B;C>D` | Múltiplos comandos |
| `A>B:tipo` | Conexão com tipo específico |

## Tipos de Conexão

| Tipo | Uso | Detecção Automática |
|------|-----|-------------------|
| `ai_languageModel` | LLM → Agent | ✅ `lmChat*` |
| `ai_memory` | Memória | ✅ `memory*` |
| `ai_tool` | Ferramentas | ✅ `*Tool`, `*CommandTool` |
| `ai_outputParser` | Output Parser | ✅ `outputParser*` |
| `main` | Conexão padrão | ✅ Outros nodes |

## Detecção Automática

Quando não especificado, o tipo é detectado automaticamente:

```formula
# Com detecção automática (recomendado)
model>agent
memory>agent
tool>agent

# Equivalente a:
model>agent:ai_languageModel
memory>agent:ai_memory
tool>agent:ai_tool
```

## Sintaxe `<` para Entradas Múltiplas

```formula
# Agent com múltiplas entradas
agent<(model,memory,tool)

# Equivalente a:
# model>agent:ai_languageModel
# memory>agent:ai_memory
# tool>agent:ai_tool
```

## Estrutura do Arquivo

Organize com comentários por seção:

```formula
# ============================================================
# ARQUIVO .FORMULA - CONEXÕES ENTRE NODES
# ============================================================

# --- CONECTAR AGENTTOOLS AO ORQUESTRADOR ---
agente1>orchestrator:ai_tool
agente2>orchestrator:ai_tool
agente3>orchestrator:ai_tool

# --- CONECTAR ROUTERS AOS AGENTTOOLS ---
router1>agente1:ai_languageModel
router2>agente2:ai_languageModel
router3>agente3:ai_languageModel

# --- CONECTAR MEMÓRIAS AOS AGENTTOOLS ---
memory1>agente1:ai_memory
memory2>agente2:ai_memory
memory3>agente3:ai_memory

# --- CONECTAR EXECUTE COMMANDS ---
exec1>agente1:ai_tool
exec2>agente2:ai_tool
exec3>agente3:ai_tool
```

## Padrões Comuns

### AI Agent Completo
```formula
webhook>agent
agent<(model,memory,tool)
agent>response
```

### Switch com Rotas
```formula
trigger>switch>(route1|route2|route3)
route1>handler1>merge:0
route2>handler2>merge:1
route3>handler3>merge:2
```

### Merge com Entradas
```formula
merge<(data1,data2,data3)
merge>result
```

### Loop
```formula
items>loop>(done|continue)
process>result>loop
```

## Como Usar o Arquivo Gerado

```bash
# Aplicar conexões ao workflow
python connections_create.py workflow.json workflow.formula

# Output customizado
python connections_create.py workflow.json workflow.formula --output connected.json

# Validação apenas
python connections_create.py workflow.json workflow.formula --validate
```

## Sua Tarefa

Crie um arquivo `.formula` seguindo o formato acima. O arquivo deve:

1. Ter cabeçalho com comentários explicativos
2. Usar a sintaxe de conexão apropriada
3. Organizar conexões por seção com comentários
4. Usar detecção automática quando possível
5. Especificar tipo explícito quando necessário
6. Ser salvo com extensão `.formula`

Salve o arquivo no diretório atual com nome apropriado.
