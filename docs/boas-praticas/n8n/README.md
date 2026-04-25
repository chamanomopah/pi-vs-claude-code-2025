# Boas Práticas N8N

Documentação organizada de boas práticas para arquitetura de workflows n8n.

## 📁 Estrutura

```
docs/boas-praticas/n8n/
├── core/              # Conceitos fundamentais
│   ├── split-in-batches.md
│   ├── merge-nodes.md
│   ├── loops.md
│   └── fluxo-dados.md
├── patterns/          # Padrões de arquitetura
│   ├── loop-simples.md
│   ├── loop-com-erro.md
│   └── branches-paralelos.md
├── nodes/             # Documentação de nodes específicos
│   ├── http-request.md
│   ├── if-switch.md
│   ├── webhook.md
│   ├── ssh-node-research.md    # [NOVO] Pesquisa completa SSH node
│   └── ssh-node-resumo.md      # [NOVO] Resumo executivo SSH
└── custom/            # Convenções personalizadas
    ├── minhas-convencoes.md
    └── integracoes-especificas.md
```

## 🚀 Como Usar

### Carregar Todas as Boas Práticas
```
/n8n-load-boas-praticas
```

### Carregar Categoria Específica
```
/n8n-load-boas-praticas core      # Conceitos fundamentais
/n8n-load-boas-praticas patterns  # Padrões de arquitetura
/n8n-load-boas-praticas nodes     # Documentação de nodes
/n8n-load-boas-praticas custom    # Convenções personalizadas
```

### Carregar Arquivo Específico
```
/n8n-load-boas-praticas split-in-batches
/n8n-load-boas-praticas loop-simples
/n8n-load-boas-praticas http-request
/n8n-load-boas-praticas ssh-node-research    # [NOVO]
/n8n-load-boas-praticas ssh-node-resumo      # [NOVO]
```

## 📚 Conteúdo

### Core (Conceitos Fundamentais)

- **split-in-batches.md** - Tudo sobre Split In Batches (loops)
  - Saídas main[0] e main[1]
  - Padrão correto de loop
  - Verificação de lista vazia

- **merge-nodes.md** - Tudo sobre Merge nodes
  - Modos: Wait, Append, Merge by Key
  - Regra de ouro (entradas conectadas)
  - Sincronização de branches

- **loops.md** - Loops e branches paralelos
  - Evitar loops infinitos
  - Sincronização com Wait
  - Loops aninhados

- **fluxo-dados.md** - Fluxo de dados e expressões
  - Documentação de entrada/saída
  - Expressões comuns
  - Transformações

### Patterns (Padrões de Arquitetura)

- **loop-simples.md** - Padrão de loop simples
  - Processar lista sequencialmente
  - Estrutura completa
  - Exemplos práticos

- **loop-com-erro.md** - Padrão de loop com tratamento de erro
  - Tratar erros sem interromper loop
  - Log de sucessos e falhas
  - Relatório final

- **branches-paralelos.md** - Padrão de branches paralelos
  - Processar em paralelo
  - Sincronizar com Merge Wait
  - Combinação de dados

### Nodes (Documentação de Nodes)

- **http-request.md** - HTTP Request node
  - Configurações básicas
  - Authentication
  - Retry e timeout
  - Padrões de uso

- **if-switch.md** - IF e Switch nodes
  - Condições booleanas
  - Múltiplas branches
  - Padrões de uso

- **webhook.md** - Webhook node
  - Configurações
  - Response modes
  - Autenticação
  - CORS

- **ssh-node-research.md** 🆕 - Pesquisa completa sobre SSH node
  - O que é e como funciona
  - Configuração no Windows
  - Boas práticas de segurança
  - Comandos úteis (Windows e Linux)
  - Troubleshooting completo
  - 7 exemplos de workflows práticos
  - Referências e fontes

- **ssh-node-resumo.md** 🆕 - Resumo executivo SSH node
  - Visão geral rápida
  - Checklist de configuração Windows
  - Erros comuns e soluções
  - Comandos mais utilizados
  - 5 exemplos de workflows
  - Dicas de performance

### Custom (Convenções Personalizadas)

- **minhas-convencoes.md** - Suas convenções
  - Nomenclatura de workflows
  - Nomenclatura de nodes
  - Convenções de dados e erro

- **integracoes-especificas.md** - Integrações do projeto
  - APIs específicas
  - Credenciais
  - Mapeamento de campos
  - Exemplos de workflows

## ➕ Adicionar Novas Boas Práticas

### 1. Criar Novo Arquivo

```bash
# Adicionar novo padrão
vim docs/boas-praticas/n8n/patterns/novo-padrao.md

# Adicionar documentação de node
vim docs/boas-praticas/n8n/nodes/novo-node.md

# Adicionar convenção específica
vim docs/boas-praticas/n8n/custom/nova-convencao.md
```

### 2. Template de Arquivo

```markdown
# Título da Boa Prática

## Quando Usar
- Situação A
- Situação B

## Estrutura
```
[Diagrama]
```

## Implementação
### Node 1: Nome
- Tipo: ...
- Configurações: ...
- Conecta a: ...

## Exemplo Prático
### Workflow Exemplo
```
[Diagrama completo]
```

## Validações
- ✅ Validação 1
- ✅ Validação 2

## Erros Comuns
### ❌ Erro Comum
```
[Diagrama do erro]
```
**Problema:** Descrição

## Checklist
- [ ] Item 1
- [ ] Item 2
```

### 3. Disponibilizar Imediatamente

Arquivos são detectados automaticamente pela skill `n8n-load-boas-praticas`.

Basta criar o arquivo `.md` na pasta apropriada e estará disponível.

## 🔍 Buscar

### Buscar em Todos os Arquivos
```bash
grep -r "Split In Batches" docs/boas-praticas/n8n/
```

### Buscar em Categoria Específica
```bash
grep -r "main[0]" docs/boas-praticas/n8n/core/
```

### Listar Todos os Arquivos
```bash
find docs/boas-praticas/n8n/ -name "*.md"
```

## 📖 Índice Remissivo

### Tópicos

- **Loops**: Ver `core/split-in-batches.md`, `core/loops.md`, `patterns/loop-simples.md`
- **Merge**: Ver `core/merge-nodes.md`, `patterns/branches-paralelos.md`
- **HTTP**: Ver `nodes/http-request.md`
- **Webhook**: Ver `nodes/webhook.md`
- **SSH**: Ver `nodes/ssh-node-research.md`, `nodes/ssh-node-resumo.md` 🆕
- **Condições**: Ver `nodes/if-switch.md`
- **Erros**: Ver `patterns/loop-com-erro.md`
- **Paralelismo**: Ver `core/loops.md`, `patterns/branches-paralelos.md`
- **Dados**: Ver `core/fluxo-dados.md`
- **Segurança**: Ver `nodes/ssh-node-research.md#segurança` 🆕
- **Windows**: Ver `nodes/ssh-node-resumo.md#windows` 🆕
- **Troubleshooting**: Ver `nodes/ssh-node-research.md#erros` 🆕

### Casos de Uso

- **Processar lista**: `patterns/loop-simples.md`
- **Processar com erro**: `patterns/loop-com-erro.md`
- **API externa**: `nodes/http-request.md`
- **Receber webhook**: `nodes/webhook.md`
- **Branching**: `nodes/if-switch.md`
- **Sincronizar**: `core/merge-nodes.md`
- **Automatizar servidor**: `nodes/ssh-node-resumo.md` 🆕
- **Deploy remoto**: `nodes/ssh-node-research.md#exemplos` 🆕
- **Monitoramento**: `nodes/ssh-node-resumo.md#exemplos` 🆕

## 🆕 Novidades (25/04/2026)

### SSH Node - Documentação Completa

Adicionada documentação abrangente sobre o SSH node do n8n com foco em ambiente Windows:

**Documentos Adicionados:**
- `ssh-node-research.md` - Guia completo (8KB)
- `ssh-node-resumo.md` - Resumo executivo (5KB)

**Conteúdo Coberto:**
✅ O que é o SSH node e suas operações
✅ Configuração completa no Windows (OpenSSH, PowerShell)
✅ Autenticação por senha e chave privada
✅ Boas práticas de segurança (N8N_ENCRYPTION_KEY, chaves SSH)
✅ Comandos úteis para Windows e Linux
✅ Troubleshooting de 6 erros comuns
✅ 7 exemplos de workflows práticos
✅ Referências e fontes oficiais

**Principais Destaques:**
- Configuração do PowerShell como shell padrão do OpenSSH
- Solução para erro de "Working Directory" no Windows
- Comandos PowerShell para gerenciamento de servidores
- Workflows de monitoramento, deploy e backup
- Checklist de segurança e hardening do n8n

## 🤝 Contribuir

Para adicionar novas boas práticas:

1. Identifique a categoria (core, patterns, nodes, custom)
2. Crie o arquivo `.md` na pasta apropriada
3. Siga o template
4. Adicione exemplos práticos
5. Documente erros comuns
6. Inclua checklist de validação

## 📝 Notas

- Todos os arquivos são em Markdown
- Use diagramas ASCII para visualização
- Inclua exemplos práticos
- Documente anti-padrões
- Adicione checklist de validação

---

**Última atualização:** 2026-04-25  
**Versão:** 2.1.0 (adicionada documentação SSH node)
