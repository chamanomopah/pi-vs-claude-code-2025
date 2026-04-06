---
name: n8n-claude-workflow-builder
user-invocable: true
description: Especialista em criar workflows N8N automatizados usando Claude Code CLI. Cria workflows complexos com múltiplos agentes, automação de desenvolvimento, orquestração de tarefas e integrações via Telegram/HTTP.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
---

# Skill: N8N + Claude Code Workflow Builder

## 🎯 Propósito

Criar workflows N8N automatizados que utilizam a **CLI do Claude Code** para orquestrar desenvolvimento, automação e tarefas complexas via chat (Telegram, HTTP Webhook, etc).

## 📋 Quando Usar Esta Skill

Ative esta skill quando o usuário:
- Quiser criar um workflow N8N que usa Claude Code CLI
- Precisar automatizar tarefas de desenvolvimento via chat
- Quiser criar múltiplos agentes especializados orquestrados
- Precisar integrar Claude Code com Telegram, Discord, Slack, etc
- Quiser criar pipelines de desenvolvimento automatizados
- Precisar de workflows com sessões persistentes do Claude

## 🏗️ Arquitetura Base

### **Componentes Essenciais**

```
[Input Layer] → [N8N Orchestration] → [Claude CLI] → [Output Layer]

Input Layer:
- Telegram Trigger
- HTTP Webhook
- Schedule Trigger
- Database Polling

N8N Orchestration:
- Execute Command Node
- Code/Function Nodes
- Switch/If Nodes (roteamento)
- Transformações de dados

Claude CLI:
claude -p -c --dangerously-skip-permissions
  -p: prompt mode (stdin)
  -c: continue (sessão persistente)
  --dangerously-skip-permissions: auto-confirma

Output Layer:
- Response messages
- Webhook callbacks
- File generation
- Git operations
```

---

## 🚀 Tipos de Workflow

### **1. Chat Bot Simples**

**Caso de uso:** Assistente via Telegram

```
Telegram Trigger → If (@) → [nova sessão | última sessão] → Response
```

**Nodes necessários:**
- `telegramTrigger` - Recebe mensagens
- `if` - Verifica se é comando
- `executeCommand` (2x) - Claude CLI
- `telegram` - Envia resposta

**Claude CLI flags:**
```bash
# Nova sessão
claude -p --dangerously-skip-permissions

# Sessão continuada
claude -p -c --dangerously-skip-permissions
```

---

### **2. Multi-Etapa Pipeline**

**Caso de uso:** Tarefas complexas com múltiplos passos

```
Input → Planning → Coding → Testing → Review → Output
```

**Nodes necessários:**
- Trigger (HTTP/Telegram)
- 5+ `executeCommand` nodes (um por etapa)
- `switch` para roteamento entre etapas
- `code` nodes para transformação
- Response nodes

**Fluxo:**
1. User: "criar CRUD de produtos"
2. **Planning**: Claude planeja arquitetura
3. **Coding**: Claude implementa código
4. **Testing**: Claude gera e executa testes
5. **Review**: Claude revisa tudo
6. **Output**: Retorna resultado completo

---

### **3. Multi-Agent System**

**Caso de uso:** Agentes especializados trabalhando em paralelo

```
Input → Orquestrador → [Agent1, Agent2, Agent3] → Aggregator → Output
```

**Agents comuns:**
- **Planner**: Planeja arquitetura
- **Coder**: Implementa código
- **Tester**: Cria e executa testes
- **Reviewer**: Code review
- **Doc**: Gera documentação
- **Security**: Verifica segurança
- **Optimizer**: Otimiza performance

**Cada agent precisa de:**
- `executeCommand` com Claude CLI
- Working directory específico
- System message específica
- Tools específicas

---

### **4. Auto-Improvement Loop**

**Caso de uso:** Refinamento até sucesso

```
Task → Claude → Test → If (error) → Loop → Claude → Fix → Test
```

**Nodes:**
- `executeCommand` (Claude)
- `executeCommand` (test runner)
- `if` (verifica sucesso)
- Loop com contador

**Lógica:**
```javascript
// Code Node
const maxTries = 3;
let currentTry = 0;

while (currentTry < maxTries) {
  const result = await executeClaude(task);

  if (result.success) break;

  task = `corrigir erro: ${result.error}`;
  currentTry++;
}
```

---

### **5. Git Automation**

**Caso de uso:** Commits automáticos após mudanças

```
Claude executa → Git add → Git commit → Git push → Notifica
```

**Nodes:**
- `executeCommand` (Claude CLI)
- `executeCommand` (git operations)
- `httpRequest` (webhook notification)

**Git commands:**
```bash
# Auto-commit
cd /d "path" && git add . &&
git status --porcelain | findstr . >nul &&
(git commit -m "Auto %date% %time%" && git push) ||
echo Nothing to commit

# Pull
cd /d "path" && git add . && git pull
```

---

## 📝 Scripts Python Disponíveis

### **workflow_download.py**
```bash
python workflow_download.py <workflow_id> --parameters
```

**Gera:**
- `<nome>.json` - Workflow completo
- `<nome>_easy_nodes.md` - Nodes + conexões + parâmetros

**Use:** Baixar workflow existente para análise

---

### **nodes_create.py**
```bash
python nodes_create.py arquivo.nodes -t workflow.json
```

**Entrada:** `.nodes` (fórmula de nodes)
**Saída:** `workflow_nodesAdded.json`

**Formato .nodes:**
```nodes
# Comentários com #
(7=agente1,agente2,...)agentTool
(7=router1,router2,...)lmChatGoogleGemini
(7=memoria1,memoria2,...)memoryPostgresChat
```

---

### **connections_create.py**
```bash
python connections_create.py workflow.json arquivo.formula
```

**Entrada:** `.formula` (conexões)
**Saída:** `workflow_connected.json`

**Formato .formula:**
```formula
# Comentários com #
A>B                        # Conexão simples
A>(B|C)                   # Múltiplas saídas
A<B:ai_tool                # Conexão com tipo
```

---

### **parameters.py**
```bash
python parameters.py workflow.json arquivo.params
```

**Entrada:** `.params` (parâmetros)
**Saída:** `workflow_params.json`

**Formato .params:**
```params
# Comentários com #
node:campo=valor           # Configuração simples
node:options.campo=valor   # Campo aninhado
node:text=texto longo      # String com espaços
```

**⚠️ CRÍTICO:**
- Arquivos .params NÃO suportam Markdown
- AgentTools usam `options.systemMessage`
- AI Agents usam `text` + `promptType=define`

---

### **workflow_update.py**
```bash
python workflow_update.py <workflow_id> workflow.json
```

**Envia workflow atualizado para o n8n**

---

## 🔧 Claude Code CLI - Referência Rápida

### **Flags Principais**

| Flag | Função | Exemplo |
|------|--------|---------|
| `-p` | Prompt mode (stdin) | `echo "prompt" \| claude -p` |
| `-c` | Continue session | `claude -p -c` |
| `--dangerously-skip-permissions` | Auto-confirma | `claude --dangerously-skip-permissions` |

### **Padrões de Uso**

#### **Nova Sessão**
```bash
cd /d "C:\path\to\project" &&
echo "{{ prompt }}" | claude -p --dangerously-skip-permissions &&
exit
```

#### **Sessão Continuada**
```bash
cd /d "C:\path\to\project" &&
echo "{{ prompt }}" | claude -p -c --dangerously-skip-permissions &&
exit
```

#### **System Message**
```bash
echo "{{ prompt }}" | claude -p -c --system "You are a specialist in..."
```

---

## 🎯 Template de Workflow Completo

### **Workflow: "Development Assistant"**

**Objetivo:** Assistente completo de desenvolvimento via Telegram

**Nodes:**
1. `telegramTrigger` - Recebe mensagens
2. `if` - Verifica tipo de comando
3. `switch` - Roteia para ação
4. `executeCommand` (nova sessão) - Claude CLI limpo
5. `executeCommand` (última sessão) - Claude CLI continuado
6. `executeCommand` (git operations) - Git automático
7. `code` - Transformação de dados
8. `telegram` (3x) - Envio de respostas

**Fluxo:**
```
Telegram →
  If (contains @) →
    Switch →
      [@command] → última sessão → Response
      [/pull] → git pull → Response
      [/push] → git push → Response
      [default] → nova sessão → Response
```

**Parâmetros Claude CLI:**
```params
# Nova sessão
nova_sessão:command=cd /d "C:\path" && echo {{ $json.message.text }} | claude -p --dangerously-skip-permissions && exit

# Última sessão
ultima_sessão:command=cd /d "C:\path" && echo {{ $json.message.text }} | claude -p -c --dangerously-skip-permissions && exit
```

---

## 📚 Guias de Referência

### **Documentação Interna**
- `@docs/claude_code_cli.md` - Referência completa CLI
- `@n8n_workflows/i4o8wBE_ULaZlTrxJ05xe-um_novo_começo/CLAUDE_CODE_CLI_N8N.md` - Conceitos avançados

### **Command de Modificação**
- `@.claude/commands/add_existingWorkflow.md` - Sintaxe completa de scripts

---

## 🔄 Workflow de Criação

### **Passo 1: Entender Requisitos**

Pergunte ao usuário:
- Qual o objetivo do workflow?
- Qual input source? (Telegram, HTTP, etc)
- Quais ações o Claude deve executar?
- Precisa de sessões persistentes?
- Precisa de múltiplos agentes?

### **Passo 2: Baixar Workflow Base (se modificando)**

```bash
python workflow_download.py <workflow_id> --parameters
```

### **Passo 3: Criar Arquivos de Configuração**

**3.1. `.nodes`** - Nodes necessários
**3.2. `.formula`** - Conexões entre nodes
**3.3. `.params`** - Parâmetros de configuração

### **Passo 4: Executar Scripts**

```bash
# Criar nodes
python nodes_create.py config.nodes -t workflow.json

# Conectar nodes
python connections_create.py workflow_nodesAdded.json config.formula

# Configurar parâmetros
python parameters.py workflow_connected.json config.params
```

### **Passo 5: Atualizar N8N**

```bash
python workflow_update.py <workflow_id> workflow_final.json
```

### **Passo 6: Documentar**

Criar:
- `README.md` - Visão geral
- `_easy_nodes.md` - Estrutura técnica
- Diagramas de fluxo

---

## ⚠️ Segurança

### **Riscos do `--dangerously-skip-permissions`**

⚠️ **Executa comandos sem confirmação**
⚠️ **Pode modificar arquivos críticos**
⚠️ **Pode expor dados sensíveis**

### **Mitigações**

1. ✅ Working directory isolado
2. ✅ Validação de input
3. ✅ Rate limiting
4. ✅ Auditoria de logs
5. ✅ Ambiente de sandboxing (VM/container)

---

## 🎓 Exemplos Práticos

### **Exemplo 1: Code Review Bot**

```
PR aberto → Webhook →
  [Claude: Analisar mudanças] →
  [Claude: Verificar segurança] →
  [Claude: Sugerir melhorias] →
Comment no PR
```

### **Exemplo 2: Test Generator**

```
Código modificado → N8N →
  [Claude: Gerar unit tests] →
  [Claude: Executar testes] →
Report via Slack
```

### **Exemplo 3: Documentation Updater**

```
Commit detectado → N8N →
  [Claude: Atualizar README] →
  [Claude: Atualizar API docs] →
Commit automático
```

---

## 🔍 Troubleshooting

### **Erro: API KEY expirada**
```bash
# Atualizar .env
N8N_API_KEY=nova_key_aqui
```

### **Erro: Nodes não conectados**
```bash
# Verificar conexões
python connections_create.py workflow.json
```

### **Erro: Parâmetros não aplicados**
```bash
# Verificar sintaxe .params
# NÃO usar Markdown em .params
```

### **Claude CLI não responde**
```bash
# Verificar working directory
# Verificar permissões
# Testar manualmente:
echo "test" | claude -p
```

---

## 📦 Estrutura de Diretórios

```
project/
├── n8n_workflows/
│   └── [workflow_id]-[nome]/
│       ├── [workflow].json
│       ├── [workflow]_easy_nodes.md
│       ├── CLAUDE_CODE_CLI_N8N.md
│       └── README.md
├── .claude/
│   └── skills/
│       └── n8n-claude-workflow-builder/
│           └── SKILL.md
├── docs/
│   └── claude_code_cli.md
└── workflow_download.py
```

---

## 🚀 Next Steps

Após criar o workflow:

1. ✅ Testar manualmente cada node
2. ✅ Verificar parâmetros Claude CLI
3. ✅ Validar conexões
4. ✅ Testar fluxo completo
5. ✅ Documentar uso
6. ✅ Commit e versionar

---

## 💡 Best Practices

1. **COMECE SIMPLES** - Chat bot básico primeiro
2. **EVOLUA GRADUALMENTE** - Adicione complexidade aos poucos
3. **TESTE SEMPRE** - Valide cada etapa
4. **DOCUMENTE TUDO** - README + easy_nodes + guias
5. **USE PATTERNS** - Reuse estruturas que funcionam
6. **SEGURANÇA PRIMEIRO** - Sandbox + validação
7. **VERSIONE** - Git para cada mudança significativa
