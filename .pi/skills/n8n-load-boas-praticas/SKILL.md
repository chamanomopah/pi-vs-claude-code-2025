---
name: n8n-load-boas-praticas
description: Carrega boas práticas de arquitetura n8n de arquivos organizados em pastas. Escaneia recursivamente docs/boas-praticas/n8n/
argument-hint: "[categoria|arquivo|vazio para tudo]"
allowed-tools: Read, Grep, Find, Bash
---

# N8N Boas Práticas Loader (Multi-File)

Carrega e referencia boas práticas de arquitetura n8n a partir de uma estrutura organizada de arquivos em pastas.

## Estrutura de Arquivos

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
│   └── webhook.md
└── custom/            # Convenções personalizadas
    ├── minhas-convencoes.md
    └── integracoes-especificas.md
```

## Como Usar

### Modo 1: Carregar Tudo (Padrão)

Quando não especificar argumento, carrega TODOS os arquivos `.md` recursivamente:

```
/n8n-load-boas-praticas
```

**Ação:**
1. Escaneia `docs/boas-praticas/n8n/` recursivamente
2. Lê todos os arquivos `.md` encontrados
3. Organiza por categoria (core, patterns, nodes, custom)
4. Memora índice de tópicos disponíveis

### Modo 2: Carregar Categoria Específica

Carrega todos os arquivos de uma categoria:

```
/n8n-load-boas-praticas core
/n8n-load-boas-praticas patterns
/n8n-load-boas-praticas nodes
/n8n-load-boas-praticas custom
```

**Ação:**
1. Escaneia `docs/boas-praticas/n8n/<categoria>/`
2. Lê todos os arquivos `.md` na pasta
3. Memora conteúdo da categoria

### Modo 3: Carregar Arquivo Específico

Carrega um arquivo específico (sem .md):

```
/n8n-load-boas-praticas split-in-batches
/n8n-load-boas-praticas loop-simples
/n8n-load-boas-praticas http-request
/n8n-load-boas-praticas webhook
```

**Ação:**
1. Busca arquivo `docs/boas-praticas/n8n/**/<arquivo>.md`
2. Lê o arquivo encontrado
3. Memora conteúdo específico

## Comandos de Escaneamento

### Listar Todos os Arquivos

```bash
find docs/boas-praticas/n8n/ -name "*.md" | sort
```

### Listar por Categoria

```bash
# Core
ls docs/boas-praticas/n8n/core/

# Patterns
ls docs/boas-praticas/n8n/patterns/

# Nodes
ls docs/boas-praticas/n8n/nodes/

# Custom
ls docs/boas-praticas/n8n/custom/
```

### Buscar Tópico Específico

```bash
# Buscar em todos os arquivos
grep -r "Split In Batches" docs/boas-praticas/n8n/

# Buscar em categoria específica
grep -r "main\[0\]" docs/boas-praticas/n8n/core/
```

### Contar Arquivos por Categoria

```bash
echo "Core: $(ls docs/boas-praticas/n8n/core/*.md 2>/dev/null | wc -l)"
echo "Patterns: $(ls docs/boas-praticas/n8n/patterns/*.md 2>/dev/null | wc -l)"
echo "Nodes: $(ls docs/boas-praticas/n8n/nodes/*.md 2>/dev/null | wc -l)"
echo "Custom: $(ls docs/boas-praticas/n8n/custom/*.md 2>/dev/null | wc -l)"
```

## Conteúdo Disponível

### Core (Conceitos Fundamentais)

1. **split-in-batches.md** - Tudo sobre Split In Batches
   - Saídas main[0] e main[1]
   - Padrão correto de loop
   - Verificação de lista vazia

2. **merge-nodes.md** - Tudo sobre Merge nodes
   - Modos: Wait, Append, Merge by Key
   - Regra de ouro (entradas conectadas)
   - Sincronização de branches

3. **loops.md** - Loops e branches paralelos
   - Evitar loops infinitos
   - Sincronização com Wait
   - Loops aninhados

4. **fluxo-dados.md** - Fluxo de dados e expressões
   - Documentação de entrada/saída
   - Expressões comuns
   - Transformações

### Patterns (Padrões de Arquitetura)

1. **loop-simples.md** - Padrão de loop simples
2. **loop-com-erro.md** - Padrão de loop com tratamento de erro
3. **branches-paralelos.md** - Padrão de branches paralelos

### Nodes (Documentação de Nodes)

1. **http-request.md** - HTTP Request node
2. **if-switch.md** - IF e Switch nodes
3. **webhook.md** - Webhook node

### Custom (Convenções Personalizadas)

1. **minhas-convencoes.md** - Convenções do projeto
2. **integracoes-especificas.md** - Integrações específicas

## Integração com o Arquiteto

Quando o **n8n-arquitecture** usa esta skill:

1. **Antes de projetar**: Carrega boas práticas relevantes
   ```
   /n8n-load-boas-praticas
   ```

2. **Durante o design**: Consulta arquivos específicos
   ```
   /n8n-load-boas-praticas loop-simples
   ```

3. **Na especificação**: Reference os arquivos aplicados
   ```
   Padrão aplicado: Loop Simples (docs/boas-praticas/n8n/patterns/loop-simples.md)
   ```

4. **Na validação**: Verifica se todos os padrões foram seguidos

## Exemplo de Uso

```
Usuário: "Preciso de um workflow que processe pedidos"

Arquiteto: /n8n-load-boas-praticas

[Skill escaneia e carrega todos os arquivos]

✓ Core: 4 arquivos carregados
✓ Patterns: 3 arquivos carregados
✓ Nodes: 3 arquivos carregados
✓ Custom: 2 arquivos carregados

Arquiteto: "Vou usar o padrão 'Loop Simples' (patterns/loop-simples.md):
- Split In Batches com main[0] → resumo final
- main[1] → processamento individual
- Node Wait para reconectar
- IF node antes para tratar lista vazia
Conforme docs/boas-praticas/n8n/patterns/loop-simples.md"
```

## Adicionar Novos Arquivos

### Criar Novo Arquivo

```bash
# Novo padrão
vim docs/boas-praticas/n8n/patterns/novo-padrao.md

# Nova documentação de node
vim docs/boas-praticas/n8n/nodes/novo-node.md

# Nova convenção
vim docs/boas-praticas/n8n/custom/nova-convencao.md
```

### Criar Nova Subcategoria

```bash
# Criar pasta
mkdir -p docs/boas-praticas/n8n/avancado

# Criar arquivos
vim docs/boas-praticas/n8n/avancado/loops-aninhados.md
vim docs/boas-praticas/n8n/avancado/workflows-assincronos.md
```

### Template de Arquivo

```markdown
# Título

## Quando Usar
- Situação A
- Situação B

## Estrutura
```
[Diagrama]
```

## Implementação
Detalhes...

## Exemplo Prático
### Workflow: Nome
```
[Diagrama]
```

## Validações
- ✅ Validação 1
- ✅ Validação 2

## Erros Comuns
### ❌ Erro
```
[Diagrama]
```
**Problema:** Descrição

## Checklist
- [ ] Item 1
- [ ] Item 2
```

## Localização dos Arquivos

Base do projeto: `C:\Users\JOSE\Downloads\cc_n8n_generator\claude_code_n8n_manager\`

Boas práticas: `docs/boas-praticas/n8n/`

## Comportamento Esperado

1. **SEMPRE escaneie** a pasta antes de responder
2. **LISTE todos os arquivos** encontrados
3. **LEIA os arquivos** solicitados (categoria ou específico)
4. **ORGANIZE por categoria** (core, patterns, nodes, custom)
5. **REFERENCE os arquivos** ao aplicar padrões
6. **NUNCA invente** padrões que não estão nos arquivos
7. **Use grep/find** para buscar padrões específicos

## Comandos Úteis

### Ver Estrutura Completa
```bash
find docs/boas-praticas/n8n/ -type f -name "*.md" | sort
```

### Ver Árvore de Diretórios
```bash
tree docs/boas-praticas/n8n/ 2>/dev/null || find docs/boas-praticas/n8n/ -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
```

### Buscar Tópico
```bash
grep -r "main\[0\]" docs/boas-praticas/n8n/
```

### Ler Arquivo Específico
```bash
cat docs/boas-praticas/n8n/patterns/loop-simples.md
```

## Índice de Tópicos

### Por Categoria

**Core:**
- Split In Batches (loops)
- Merge Nodes (sincronização)
- Loops e Branches Paralelos
- Fluxo de Dados

**Patterns:**
- Loop Simples
- Loop com Erro
- Branches Paralelos

**Nodes:**
- HTTP Request
- IF e Switch
- Webhook

**Custom:**
- Minhas Convenções
- Integrações Específicas

### Por Caso de Uso

- **Processar lista:** patterns/loop-simples.md
- **Processar com erro:** patterns/loop-com-erro.md
- **API externa:** nodes/http-request.md
- **Receber webhook:** nodes/webhook.md
- **Branching:** nodes/if-switch.md
- **Sincronizar:** core/merge-nodes.md
- **Expressões:** core/fluxo-dados.md

## Notas Importantes

- Esta skill é **READ-ONLY** - apenas consulta e lê arquivos
- Não modifica nenhum arquivo
- Escaneia recursivamente a pasta `docs/boas-praticas/n8n/`
- Arquivos são detectados automaticamente
- Pode ser usada múltiplas vezes durante o design
- Cada chamada recarrega os arquivos (garante atualização)

## Changelog

### v2.0.0 (2025-04-08)
- ✅ Escaneamento recursivo de pastas
- ✅ Suporte
