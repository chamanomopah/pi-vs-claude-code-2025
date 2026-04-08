# Ecossistema de Agentes n8n

Este diretório contém as especificações dos agentes especializados em trabalhar com workflows n8n.

## Agentes Disponíveis

### 📐 n8n-architect
**Arquiteto de workflows n8n**

- **Função**: Analisa requisitos e projeta estruturas completas de workflows
- **Responsabilidade**: Criar especificações detalhadas para implementação
- **O que faz**: Documenta nodes, conexões, fluxo de dados, diagramas
- **O que NÃO faz**: Implementa workflows, testa, faz correções

**Quando usar**:
- Precisar criar um novo workflow do zero
- Precisar modificar a estrutura de um workflow existente
- Precisar planejar antes de implementar

**Saída**: Documento de especificação completo com todos os nodes, conexões e parâmetros

---

### 🔨 n8n-builder
**Construtor de workflows n8n**

- **Função**: Implementa workflows com base nas especificações do architect
- **Responsabilidade**: Criar nodes, conexões e workflows funcionais
- **Ferramentas**: Scripts Python em `tools/n8n/`
- **O que faz**: Executa scripts para criar workflows no n8n
- **O que NÃO faz**: Projeta estruturas, testa workflows

**Quando usar**:
- Após receber especificação do n8n-architect
- Quando implementar correções solicitadas pelo n8n-tester

**Saída**: Workflow criado no n8n (JSON ou via API)

---

### 🧪 n8n-tester
**Testador de workflows n8n**

- **Função**: Testa workflows exaustivamente e identifica problemas
- **Responsabilidade**: Garantir que workflows funcionam na prática
- **O que faz**: Executa testes manuais, documenta bugs, propõe soluções
- **O que NÃO faz**: Implementa correções, projeta estruturas

**Quando usar**:
- Após o n8n-builder implementar um workflow
- Sempre que houver modificações em workflows existentes
- Para validar que correções funcionaram

**Saída**: Relatório de testes com bugs encontrados e soluções propostas

---

## Fluxo de Trabalho Recomendado

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         n8n-architect                   │
│  - Analisa requisitos                   │
│  - Projeta estrutura                    │
│  - Documenta especificação              │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         n8n-builder                     │
│  - Implementa workflow                  │
│  - Cria nodes e conexões                │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         n8n-tester                      │
│  - Testa workflow                       │
│  - Documenta bugs                       │
└────────┬────────────────────────────────┘
         │
         ▼
    ┌────────┐
    │ Bugs? │
    └───┬────┘
        │
   Sim  │  Não
   ◄────┴────►
   │          │
   ▼          ▼
┌────────────┐  ┌──────────────┐
│ n8n-builder│  │  WORKFLOW    │
│ corrige   │  │   APROVADO   │
└────────────┘  └──────────────┘
```

## Boas Práticas

### Separação de Responsabilidades
- **Architect**: NUNCA implementa, apenas projeta
- **Builder**: NUNCA testa sem especificação, apenas implementa
- **Tester**: NUNCA implementa, apenas testa e propõe soluções

### Comunicação Entre Agentes
- Use linguagem clara e específica
- Documente tudo em arquivos estruturados
- Propenha soluções acionáveis (não vagas)
- Valide antes de considerar "pronto"

### Qualidade
- Architect: Especificações detalhadas e completas
- Builder: Implementação fiel à especificação
- Tester: Testes exaustivos com dados reais

## Localização dos Arquivos

```
n8n_projects/
├── agents/                 # Especificações dos agentes
│   ├── n8n-architect.md   # Arquiteto de workflows
│   ├── n8n-builder.md     # Construtor de workflows
│   ├── n8n-tester.md      # Testador de workflows
│   └── README.md          # Este arquivo
├── 1_Youtube_video_production/  # Exemplo de projeto
└── ...                    # Mais projetos

tools/n8n/                 # Scripts Python do builder
├── nodes_create.py        # Criar nodes
├── connections_create.py  # Criar conexões
├── parameters.py          # Configurar parâmetros
├── workflow_create.py     # Criar workflow novo
├── workflow_download.py   # Baixar workflow existente
└── workflow_exemples/     # Exemplos de workflows
```

## Como Usar os Agentes

### Com a CLI do Pi:

```bash
# Usar o architect
pi -e agent-team --agent n8n-architect "Criar workflow para processar pedidos"

# Usar o builder
pi -e agent-team --agent n8n-builder "Implementar especificação em n8n_projects/specs/pedidos.md"

# Usar o tester
pi -e agent-team --agent n8n-tester "Testar workflow ID 123"
```

### Com o Agent Team Extension:

```typescript
// No arquivo de configuração do time
agents:
  - name: architect
    spec: n8n_projects/agents/n8n-architect.md
  - name: builder
    spec: n8n_projects/agents/n8n-builder.md
  - name: tester
    spec: n8n_projects/agents/n8n-tester.md
```

## Referências

- **Documentação Pi**: `.pi/docs/`
- **Skills n8n**: `.pi/skills/n8n-*/`
- **Exemplos de Workflows**: `tools/n8n/workflow_exemples/`
- **Projetos n8n**: `n8n_projects/*/`

## Conhecimento n8n Necessário

Todos os agentes devem entender:

### Split In Batches
- `main[0]` = executa quando o loop ACABA (1 item com todos os dados)
- `main[1]` = executa em CADA item do loop
- Precisa de node Wait para continuar o loop

### Merge Nodes
- Precisam de AMBAS as entradas conectadas
- Modo "Wait" aguarda todas as entradas

### Loops
- Último node reconecta para Split In Batches
- Usar Wait para sincronizar branches paralelos

## Contribuindo

Para adicionar novos agentes ao ecossistema n8n:

1. Crie arquivo `<nome>-agente.md` em `n8n_projects/agents/`
2. Inclua frontmatter YAML completo (name, description, tools)
3. Documente claramente:
   - Responsabilidades (o que FAZ e NÃO FAZ)
   - Quando usar
   - O que produz como saída
   - Integração com outros agentes
4. Atualize este README

---

**Última atualização**: 2026-04-07
**Versão**: 1.0.0
