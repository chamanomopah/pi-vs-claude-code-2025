---
name: n8n-create-params
description: Criar arquivo .params com configuração de parâmetros N8N. Use para definir parâmetros de nodes como agentes, HTTP requests, e mais.
argument-hint: [params-spec]
disable-model-invocation: true
allowed-tools: Write, Bash
---

# Criar Arquivo .params para N8N

Cria arquivos `.params` com configuração de parâmetros de nodes N8N seguindo a sintaxe de fórmula.

## Formato do Arquivo .params

```ini
# ============================================================
# ARQUIVO .PARAMS - CONFIGURAÇÃO DE PARÂMETROS
# ============================================================

# AI Agent Configuration
agent:promptType=define
agent:text=You are a helpful assistant
agent:hasMemory=true
agent:options.maxIterations=10

# HTTP Request
http:method=POST
http:url=https://api.example.com
http:headers={"Authorization": "Bearer xxx"}
```

## Sintaxe Básica

| Sintaxe | Descrição | Exemplo |
|---------|-----------|---------|
| `node:campo=valor` | Campo simples | `http:method=POST` |
| `node:campo.subcampo=valor` | Campo aninhado | `http:options.timeout=30000` |
| `node:campo=[json]` | Array/objeto complexo | `http:headers={"Auth": "Bearer xxx"}` |
| `;` | Separador de comandos | `A:B=value1;C:D=value2` |

## Tipos de Valor

| Tipo | Sintaxe | Exemplo |
|------|---------|---------|
| String | Valor sem aspas | `http:url=https://api.example.com` |
| String com espaços | Sem aspas | `agent:text=You are helpful` |
| String com `;` | Entre aspas duplas | `agent:text="Value; with; semicolons"` |
| Number | Direto | `agent:temperature=0.7` |
| Boolean | `true`/`false` | `agent:hasMemory=true` |
| JSON Object | `{...}` | `http:options={"timeout": 30000}` |
| JSON Array | `[...]` | `http:queryParameters=[...]` |
| Expressão N8N | Prefixo `=` | `agent:text={{ $now }}` |

### ⚠️ Importante: Aspas em Valores

- **Aspas duplas (`"`)**: São tratadas como delimitadores de string. Use-as quando o valor contiver `;` ou caracteres especiais.
- **Aspas simples (`'`)**: São ignoradas pelo parser. Podem ser usadas livremente no texto (ex: "You're", "agent's").

**Exemplo**:
```ini
# CORRETO - sem aspas para texto simples
agent:text=You are a helpful assistant

# CORRETO - com aspas duplas quando há ;
agent:text="You are helpful; you assist users"

# INCORRETO - aspas simples NÃO protegem o ;
agent:text='You are helpful; you assist users'  # O ; vai separar comandos!
```

## Diferença Crítica: AI Agent vs AgentTool

| Campo | AI Agent (Pai) | AgentTool (Filho) |
|-------|----------------|-------------------|
| Prompt principal | `text` ✅ | ❌ não usado |
| System message | `options.systemMessage` | `options.systemMessage` ✅ |
| promptType | `define` | ❌ não usado |

### AI Agent (Orquestrador)
```ini
# CORRETO para AI Agent principal
orchestrator:promptType=define
orchestrator:text=You are a master orchestrator
orchestrator:hasMemory=true
orchestrator:options.maxIterations=15
```

### AgentTool (Sub-agente)
```ini
# CORRETO para AgentTool (filho)
myAgentTool:options.systemMessage=You are a specialist in Python programming...

# ERRADO para AgentTool - isso NÃO funciona!
myAgentTool:text=You are a specialist...
myAgentTool:promptType=define
```

## Campos por Tipo de Node

### AI Agent (Principal/Orquestrador)
```ini
agent:promptType=define
agent:text=You are a helpful assistant
agent:hasMemory=true
agent:hasOutputParser=false
agent:needsFallback=true
agent:options.systemMessage=Custom system message
agent:options.maxIterations=10
agent:options.enableStreaming=true
agent:options.returnIntermediateSteps=true
```

### AgentTool (Sub-agente)
```ini
# AgentTools usam options.systemMessage (recebem mensagens do pai)
specialistTool:options.systemMessage=You are a specialist in...
```

### HTTP Request
```ini
http:method=POST
http:url=https://api.example.com/v1/endpoint
http:authentication=genericCredentialType
http:genericAuthType=httpHeaderAuth
http:headers={"Content-Type": "application/json", "Authorization": "Bearer {{ $credentials.apiKey }}"}
http:queryParameters=[{"name": "limit", "value": "100"}, {"name": "offset", "value": "0"}]
http:bodyContentType=json
http:jsonBody={"user": "{{ $json.id }}", "action": "update"}
http:options.timeout=30000
http:options.response.responseFormat=json
```

### Code Node
```ini
code:mode=runOnceForAllItems
code:language=python
code:snapshotTime=-1
code:resetSnapshot=false
```

### Webhook
```ini
webhook:path=webhook/agent
webhook:responseMode=responseNode
webhook:options.respondWithWebhookStatus=false
```

## Estrutura do Arquivo

Organize com comentários por seção:

```ini
# ============================================================
# ARQUIVO .PARAMS - CONFIGURAÇÃO DE PARÂMETROS
# ============================================================

# ============================================================
# AI AGENT PRINCIPAL (ORQUESTRADOR)
# ============================================================
nero:promptType=define
nero:text=You are nero, a master orchestrator coordinating specialized AI agents.
nero:hasMemory=true
nero:hasOutputParser=false
nero:needsFallback=true
nero:options.maxIterations=15

# ============================================================
# AGENTTOOLS (SUB-AGENTES)
# ============================================================
# Cada AgentTool usa options.systemMessage (NÃO usa text ou promptType)

assistente:options.systemMessage=You are a helpful general assistant. You provide friendly, clear assistance with everyday tasks.

orchestrator:options.systemMessage=You are a Workflow Orchestration Specialist. You design, analyze, and optimize automated workflows.

programador:options.systemMessage=You are a Programming and Development Expert. You help with coding tasks, code review, debugging, and software development best practices.

# ============================================================
# HTTP REQUEST
# ============================================================
http:method=POST
http:url=https://api.example.com
http:headers={"Content-Type": "application/json"}
```

## Expressões N8N

Use prefixo `=` para expressões:

```ini
# Expressão simples
agent:text={{ $now }}

# String com expressão
agent:text=Current date: {{ $now }}

# Template complexo
http:jsonBody={"user": "{{ $json.id }}", "action": "update"}
```

## Modificadores

| Modificador | Ação | Exemplo |
|-------------|------|---------|
| `+` | Adiciona ao array existente | `+http:queryParameters=[...]` |
| `-` | Remove campo | `-http:options.proxy` |
| `!` | Força sobrescrever | `!agent:text=New text` |

## Como Usar o Arquivo Gerado

```bash
# Aplicar parâmetros ao workflow
python parameters.py workflow.json workflow.params

# Output customizado
python parameters.py workflow.json workflow.params --output configured.json

# Validação apenas
python parameters.py workflow.json workflow.params --validate
```

## Regras Importantes

1. **NÃO use Markdown** em arquivos `.params`
   - ✅ `# comentário`
   - ❌ `## Título`
   - ❌ `**negrito**`
   - ❌ `- item` de lista

2. **Use `:` como separador** (permite espaços no nome)
   - ✅ `AI Agent:text=Hello`
   - ❌ `AI Agent.text=Hello`

3. **AgentTools usam systemMessage**, não text
   - ✅ `tool:options.systemMessage=...`
   - ❌ `tool:text=...`

4. **Cuidado com aspas simples**
   - ✅ `agent:text=You're helpful` (aspas simples são ignoradas)
   - ✅ `agent:text="Value; with; semicolons"` (use aspas duplas para proteger `;`)
   - ❌ `agent:text='Value; semicolons'` (aspas simples NÃO protegem `;`)

## Sua Tarefa

Crie um arquivo `.params` seguindo o formato acima. O arquivo deve:

1. Ter cabeçalho com comentários explicativos
2. Usar sintaxe `node:campo=valor`
3. Diferenciar AI Agent de AgentTool corretamente
4. Organizar por seções com comentários
5. NÃO usar formatação Markdown
6. Ser salvo com extensão `.params`

Salve o arquivo no diretório atual com nome apropriado.
