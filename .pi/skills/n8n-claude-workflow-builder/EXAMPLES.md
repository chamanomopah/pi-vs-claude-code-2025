# Exemplos Práticos - N8N + Claude Code CLI

## Exemplo 1: Code Review Automático

### **Workflow: code-review-auto**

**Objetivo:** Analisar PRs automaticamente e comentar sugestões

```
GitHub Webhook (PR opened) →
  [Claude: Analisar diff] →
  [Claude: Verificar segurança] →
  [Claude: Sugerir melhorias] →
  [Claude: Gerar comment] →
GitHub API (post comment)
```

### **Arquivo .nodes**
```nodes
# Trigger e análise
(1=github_webhook)webhook
(1=code_analyzer)executeCommand
(1=security_checker)executeCommand
(1=improver)executeCommand
(1=comment_generator)executeCommand
(1=github_api)httpRequest
```

### **Arquivo .formula**
```formula
github_webhook>code_analyzer>security_checker>improver>comment_generator>github_api
```

### **Arquivo .params**
```params
# Code Analyzer
code_analyzer:command=cd /d "C:\repo" && echo "Analise este diff: {{ $json.diff }}" | claude -p --dangerously-skip-permissions && exit

# Security Checker
security_checker:command=cd /d "C:\repo" && echo "Verifique vulnerabilidades: {{ $json.stdout }}" | claude -p -c --dangerously-skip-permissions && exit

# Improver
improver:command=cd /d "C:\repo" && echo "Sugira melhorias: {{ $json.stdout }}" | claude -p -c --dangerously-skip-permissions && exit

# Comment Generator
comment_generator:command=cd /d "C:\repo" && echo "gere comment para PR: {{ $json.stdout }}" | claude -p -c --dangerously-skip-permissions && exit

# GitHub API
github_api:url=https://api.github.com/repos/{{ $json.repo }}/issues/{{ $json.pr_number }}/comments
github_api:method=POST
github_api:authentication=genericCredentialType
github_api:body={{ $json.stdout }}
```

---

## Exemplo 2: Multi-Agent Development Pipeline

### **Workflow: dev-pipeline-multi-agent**

**Objetivo:** Pipeline completo com agentes especializados

```
User Request →
  [Agent 1: Planner] →
  [Agent 2: Coder] →
  [Agent 3: Tester] →
  [Agent 4: Reviewer] →
  [Agent 5: Doc Writer] →
Complete PR
```

### **Arquivo .nodes**
```nodes
# Input e orquestração
(1=telegram_trigger)telegramTrigger
(1=router)switch
(5=planner,coder,tester,reviewer,docwriter)executeCommand
(1=aggregator)code
(1=git_operations)executeCommand
(2=response,notification)telegram
```

### **Arquivo .formula**
```formula
telegram_trigger>router>(planner|coder|tester|reviewer|docwriter)>aggregator>git_operations>(response|notification)
```

### **Arquivo .params**
```params
# Planner Agent
planner:command=cd /d "C:\project" && echo "Planeje: {{ $json.message.text }}" | claude -p --system "You are a planning specialist. Break down tasks into steps." --dangerously-skip-permissions && exit

# Coder Agent
coder:command=cd /d "C:\project" && echo "Implemente: {{ $json.stdout }}" | claude -p -c --system "You are a coding specialist. Write clean, tested code." --dangerously-skip-permissions && exit

# Tester Agent
tester:command=cd /d "C:\project" && echo "Teste: {{ $json.stdout }}" | claude -p -c --system "You are a testing specialist. Create comprehensive tests." --dangerously-skip-permissions && exit

# Reviewer Agent
reviewer:command=cd /d "C:\project" && echo "Revise: {{ $json.stdout }}" | claude -p -c --system "You are a code review specialist. Check for bugs, security, performance." --dangerously-skip-permissions && exit

# Doc Writer Agent
docwriter:command=cd /d "C:\project" && echo "Documente: {{ $json.stdout }}" | claude -p -c --system "You are a documentation specialist. Write clear docs." --dangerously-skip-permissions && exit

# Git Operations
git_operations:command=cd /d "C:\project" && git add . && git commit -m "Auto: {{ $json.task }}" && git push
```

---

## Exemplo 3: Bug Auto-Fixer Loop

### **Workflow: bug-auto-fixer**

**Objetivo:** Detectar erros e tentar corrigir automaticamente

```
Error Log →
  [Claude: Analisar erro] →
  [Claude: Gerar fix] →
  [Test Runner] →
  [If: Success?] →
    YES → Notificar
    NO → [Loop: max 3x] →
      [Claude: Analisar falha] →
      [Claude: Corrigir fix] →
      [Test Runner] →
      ...
```

### **Arquivo .nodes**
```nodes
# Trigger e análise
(1=error_webhook)webhook
(1=error_analyzer)executeCommand
(1=fix_generator)executeCommand
(1=test_runner)executeCommand
(1=success_check)if
(1=loop_counter)code
(1=fail_analyzer)executeCommand
(1=fix_improver)executeCommand
(1=notifier)telegram
```

### **Arquivo .formula**
```formula
error_webhook>error_analyzer>fix_generator>test_runner>success_check
success_check>(notifier|fail_analyzer>fix_improver>loop_counter>test_runner)
```

### **Arquivo .params**
```params
# Error Analyzer
error_analyzer:command=cd /d "C:\project" && echo "Analise este erro: {{ $json.error }}" | claude -p --system "You are a debugging specialist. Identify root cause." --dangerously-skip-permissions && exit

# Fix Generator
fix_generator:command=cd /d "C:\project" && echo "gere fix para: {{ $json.stdout }}" | claude -p -c --system "You are a fix generator. Write minimal, safe fixes." --dangerously-skip-permissions && exit

# Test Runner
test_runner:command=cd /d "C:\project" && npm test -- --json

# Success Check
success_check:conditions.conditions.0.leftValue={{ $json.exitCode }}
success_check:conditions.conditions.0.rightValue=0
success_check:conditions.conditions.0.operator.operation=equals

# Fail Analyzer
fail_analyzer:command=cd /d "C:\project" && echo "Analise falha do fix: {{ $json.fix }}\nErro: {{ $json.testOutput }}" | claude -p -c --system "You analyze fix failures. Explain what went wrong." --dangerously-skip-permissions && exit

# Fix Improver
fix_improver:command=cd /d "C:\project" && echo "Melhore o fix: {{ $json.previousFix }}\nProblema: {{ $json.analysis }}" | claude -p -c --system "You improve failed fixes. Be conservative." --dangerously-skip-permissions && exit

# Loop Counter (Code Node JS)
loop_counter:jsCode=
// Max 3 tentativas
const tries = $json.tries || 0;
if (tries >= 3) {
  return [{ json: { stop: true, error: 'Max tries reached' } }];
}
return [{ json: { tries: tries + 1, continue: true } }];
```

---

## Exemplo 4: Documentation Generator

### **Workflow: doc-generator**

**Objetivo:** Gerar documentação automaticamente após commits

```
Git Push Detectado →
  [Claude: Analisar mudanças] →
  [Claude: Atualizar README] →
  [Claude: Atualizar API docs] →
  [Claude: Gerar changelog] →
  Git Commit (docs) →
  Notificar time
```

### **Arquivo .nodes**
```nodes
# Trigger e geração
(1=git_webhook)webhook
(1=change_analyzer)executeCommand
(1=readme_updater)executeCommand
(1=api_doc_generator)executeCommand
(1=changelog_generator)executeCommand
(1=git_commit_docs)executeCommand
(1=slack_notifier)slack
```

### **Arquivo .formula**
```formula
git_webhook>change_analyzer>readme_updater>api_doc_generator>changelog_generator>git_commit_docs>slack_notifier
```

### **Arquivo .params**
```params
# Change Analyzer
change_analyzer:command=cd /d "C:\project" && echo "Analise mudanças: {{ $json.commits }}" | claude -p --system "You analyze code changes and identify documentation needs." --dangerously-skip-permissions && exit

# README Updater
readme_updater:command=cd /d "C:\project" && echo "Atualize README com: {{ $json.stdout }}" | claude -p -c --system "You update README.md files based on code changes." --dangerously-skip-permissions && exit

# API Doc Generator
api_doc_generator:command=cd /d "C:\project" && echo "gere API docs para: {{ $json.stdout }}" | claude -p -c --system "You generate API documentation from code." --dangerously-skip-permissions && exit

# Changelog Generator
changelog_generator:command=cd /d "C:\project" && echo "gere entradas de CHANGELOG: {{ $json.stdout }}" | claude -p -c --system "You write changelog entries." --dangerously-skip-permissions && exit

# Git Commit Docs
git_commit_docs:command=cd /d "C:\project" && git add README.md docs/ CHANGELOG.md && git commit -m "docs: atualizar documentação [auto]" && git push

# Slack Notifier
slack_notifier:channel=#dev-updates
slack_notifier:text=Documentação atualizada: {{ $json.changelog }}
```

---

## Exemplo 5: Performance Optimizer

### **Workflow: perf-optimizer**

**Objetivo:** Analisar performance e sugerir otimizações

```
Lighthouse Report →
  [Claude: Analisar métricas] →
  [Claude: Identificar bottlenecks] →
  [Claude: Sugerir otimizações] →
  [Claude: Implementar fixes] →
  [Claude: Testar melhorias] →
  PR com otimizações
```

### **Arquivo .nodes**
```nodes
# Trigger e otimização
(1=lighthouse_webhook)webhook
(1=metrics_analyzer)executeCommand
(1=bottleneck_finder)executeCommand
(1=optimizer)executeCommand
(1=fix_implementer)executeCommand
(1=improvement_tester)executeCommand
(1=pr_creator)executeCommand
```

### **Arquivo .formula**
```formula
lighthouse_webhook>metrics_analyzer>bottleneck_finder>optimizer>fix_implementer>improvement_tester>pr_creator
```

### **Arquivo .params**
```params
# Metrics Analyzer
metrics_analyzer:command=cd /d "C:\project" && echo "Analise métricas Lighthouse: {{ $json.report }}" | claude -p --system "You are a performance analyst. Identify key metrics and issues." --dangerously-skip-permissions && exit

# Bottleneck Finder
bottleneck_finder:command=cd /d "C:\project" && echo "Identifique bottlenecks: {{ $json.stdout }}" | claude -p -c --system "You find performance bottlenecks in code." --dangerously-skip-permissions && exit

# Optimizer
optimizer:command=cd /d "C:\project" && echo "Sugira otimizações para: {{ $json.stdout }}" | claude -p -c --system "You suggest performance optimizations." --dangerously-skip-permissions && exit

# Fix Implementer
fix_implementer:command=cd /d "C:\project" && echo "Implemente otimizações: {{ $json.stdout }}" | claude -p -c --system "You implement performance optimizations safely." --dangerously-skip-permissions && exit

# Improvement Tester
improvement_tester:command=cd /d "C:\project" && npm run lighthouse -- {{ $json.url }}

# PR Creator
pr_creator:command=cd /d "C:\project" && git add . && git commit -m "perf: otimizações de performance" && git push && gh pr create --title "Performance Optimizations" --body "{{ $json.improvements }}"
```

---

## Quick Start: Criar Seu Primeiro Workflow

### **1. Chat Bot Simples (5 min)**

```bash
# Baixar workflow existente
python workflow_download.py i4o8wBE_ULaZlTrxJ05xe --parameters

# Ler estrutura
cat Um_novo_Começo_easy_nodes.md
```

**Modificações mínimas:**
- Trocar Telegram por Discord
- Adicionar comando `/help`
- Mudar working directory

### **2. Multi-Agent (15 min)**

**Criar do zero:**
1. Novo workflow vazio no n8n
2. Adicionar Telegram Trigger
3. Criar 3 executeCommand nodes
4. Configurar cada um com system message diferente
5. Conectar em sequência
6. Testar

### **3. Git Automation (10 min)**

**Adicionar ao workflow existente:**
1. Execute Command node após Claude
2. Git add + commit + push
3. Notificação via Telegram

---

## Tips & Tricks

### **Variáveis N8N**
```javascript
{{ $json.message.text }}     // Telegram message
{{ $json.stdout }}            // Claude CLI output
{{ $json.exitCode }}          // Command exit code
{{ $('NodeName').item.json }} // Output de outro node
```

### **System Messages**
```bash
--system "You are a specialist in..."
```

**Especialistas comuns:**
- Planning specialist
- Coding specialist
- Testing specialist
- Security specialist
- Performance specialist
- Documentation specialist

### **Loops com If Node**
```javascript
// Condição de loop
{{ $json.tries }} < 3
```

### **Aggregators**
```javascript
// Code Node para agregar múltiplos outputs
const results = $input.all();
return [{ json: { aggregated: results } }];
```

---

## Troubleshooting

### **Claude não responde**
- Verificar working directory
- Testar comando manualmente
- Verificar permissões

### **Nodes desconectados**
- Usar `connections_create.py workflow.json` para listar
- Verificar se todos estão conectados

### **Erro em .params**
- NÃO usar Markdown
- Verificar sintaxe `node:campo=valor`
- AgentTools usam `options.systemMessage`

---

## Próximos Passos

1. ✅ Começar com **Exemplo 1** (Code Review)
2. ✅ Evoluir para **Exemplo 2** (Multi-Agent)
3. ✅ Experimentar **Exemplo 3** (Bug Fixer)
4. ✅ Criar seu próprio workflow customizado
