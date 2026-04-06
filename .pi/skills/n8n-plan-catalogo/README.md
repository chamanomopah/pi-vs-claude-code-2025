# N8N Plan Catalog Skill

Especialista em criar **Declarative End-to-End n8n Workflow Specification Plans** baseados exclusivamente no catálogo de nodes do projeto.

## 📋 Descrição

Esta skill gera **planos de implementação** para workflows n8n, não implementações diretas. Ela segue uma abordagem declarativa e determinística, inspirada em "Workflow Specification Prompts" que descrevem:

1. **Arquitetura de Workflow** - Nome, trigger, estrutura de decisões, fluxos paralelos
2. **Comportamento Determinístico** - Regras claras, campos exatos, sem ambiguidade
3. **Roteamento Lógico** - Padrões de normalização → classificação → switch → sub-rotas

## 🎯 Quando Usar

Use esta skill quando precisar:
- **Planejar um workflow completo do zero**
- **Modificar um workflow existente** (fornecendo ID)
- Especificar a arquitetura de um workflow complexo
- Documentar a estrutura de decisões e branching
- Criar planos reproducíveis e determinísticos
- Avaliar diferentes abordagens antes de implementar

## 🚀 Como Usar

### Modo 1: Workflow Novo

```
/n8n-plan-catalogo "quero um workflow que receba leads por webhook, classifique por prioridade e envie para diferentes canais"
```

### Modo 2: Modificar Workflow Existente

```
/n8n-plan-catalogo "workflow_id" "descrição da modificação"

# Exemplo:
/n8n-plan-catalogo "bhlDnM03ko0aq" "adicionar validação de email no início"
```

**No modo 2, a skill irá:**
1. Baixar o workflow usando `workflow_download.py <id> --connection`
2. Ler o arquivo `_easy_nodes.md` gerado
3. Analisar nodes existentes, conexões e pontos de intervenção
4. Criar um plano de modificação com:
   - Análise do estado atual
   - Ponto de intervenção identificado
   - Nodes a criar/modificar
   - Conexões a adicionar/remover
   - Fluxo modificado

### Com Prompt Declarativo
Forneça um prompt completo estruturado:

```
Create an n8n workflow that:
1. Starts with Webhook receiving JSON with fields: name, email, type
2. Normalizes fields (trim, lowercase)
3. Classifies using rules in order:
   - set lane="VIP" if type contains "enterprise"
   - else set lane="Standard"
4. Uses Switch on lane with 2 branches
5. VIP branch sends to Slack #vip-leads
6. Standard branch logs to Google Sheets
```

## 📁 Arquivos da Skill

```
n8n-plan-catalogo/
├── SKILL.md                    # Instruções principais (OBRIGATÓRIO)
├── README.md                   # Este arquivo
├── catalogo-quickref.md        # Referência rápida dos nodes
├── template.md                 # Template para planos
└── examples/
    └── lead-router-demo.md     # Exemplo completo de plano
```

## 🔑 Princípios

### 1. Catálogo-First
✅ **SEMPRE** consulte `catalogo_nodes.py` antes de sugerir nodes
✅ Use apenas nodes disponíveis no catálogo
⚠️ Nodes externos apenas em último caso, com justificativa explícita

### 2. Simplicidade com Garantia
✅ **Mínimo de nodes** para garantir o resultado
✅ **Mínimo de parâmetros** (mas suficiente para qualidade)
✅ **Métodos garantidos** de sucesso são valiosos
❌ Anti-padrão: solução simples que não gera o resultado esperado

### 3. Determinístico
✅ "these exact fields"
✅ "using these rules in order"
✅ "X separate branches that do not merge back"
❌ Ambiguidade = falha

### 4. Trade-offs Explícitos
Quando houver opções, apresente:
- **Versão simples**: X nodes, funcionalidade básica
- **Versão completa**: Y nodes, funcionalidades extras

## 📊 Estrutura do Plano Gerado

Todo plano segue este template:

```markdown
# Plano de Workflow: <Nome>

## Resumo
<Descrição breve>

## Trigger
<Tipo + entrada>

## Campos de Entrada
| Campo | Tipo | Descrição |

## Fluxo Principal
### 1. Normalização
### 2. Classificação
### 3. Roteamento (Switch)

## Branches
### Branch: <nome>
<Nodes, fluxo, lógica>

## Nodes Necessários
| Nome | Tipo | ConnectionType | Propósito |

## Conexões
| Origem | Destino | Tipo |

## Parâmetros Principais
| Node | Parâmetro | Valor |

## Considerações Especiais
<Credenciais, pré-requisitos, limitações>
```

## 📚 Referências

### Catálogo de Nodes
- **Arquivo**: `catalogo_nodes.py`
- **Quick Ref**: `catalogo-quickref.md`

### Documentação de Apoio
- `README_CATALOGO.md` - Documentação completa do catálogo
- `README_conectar.md` - Sintaxe de conexões
- `README_parameters.md` - Sintaxe de parâmetros

### Exemplos
- `examples/lead-router-demo.md` - Exemplo completo de workflow novo (prompt declarativo → plano)
- `examples/add-validation-example.md` - Exemplo de modificação de workflow existente

## ✅ Checklist de Validação

Antes de finalizar um plano:
- [ ] Todos os nodes estão em `catalogo_nodes.py`
- [ ] connectionTypes estão corretos
- [ ] Plano é determinístico (sem ambiguidade)
- [ ] Solução é simples mas completa
- [ ] Trade-offs estão explícitos (se houver)
- [ ] Parâmetros mínimos mas suficientes

## 🎨 Padrões Comuns

### Webhook → Processamento → Resposta
```
webhook → set → code → respondToWebhook
```

### Switch Multi-Branch
```
code → switch
          ↓ [0]    ↓ [1]    ↓ [2]
      branch1  branch2  branch3
```

### Agent AI com Tools
```
chatTrigger → agent
                   ↓ [ai_tool]
               slackTool
               httpRequestTool
                   ↓ [ai_languageModel]
               geminiModel
                   ↓ [ai_memory]
               postgresMemory
```

## 🔄 Fluxo de Trabalho

### Modo 1 (Novo Workflow)
1. **Entendimento** - Converse com o usuário
2. **Consulta ao Catálogo** - Verifique nodes disponíveis
3. **Especificação** - Crie plano declarativo
4. **Validação** - Verifique todos os itens do checklist
5. **Salvamento** - Salve em `<nome>-plano.md`

### Modo 2 (Modificar Workflow)
1. **Download** - Baixe workflow usando `workflow_download.py <id> --connection`
2. **Análise** - Leia `_easy_nodes.md` e identifique estrutura atual
3. **Ponto de Intervenção** - Identifique onde modificar
4. **Especificação** - Crie plano de modificação
5. **Validação** - Verifique nodes contra catálogo e impacto no fluxo
6. **Salvamento** - Salve em `<nome>-modificação-<descrição>-plano.md`

## 📝 Saída

A skill **NUNCA implementa** - apenas gera o plano em arquivo `.md` pronto para ser usado por outras skills/comandos para implementação.

### Modo 1 (Novo)
- Arquivo: `<nome-do-workflow>-plano.md`
- Conteúdo: Plano completo do zero

### Modo 2 (Modificação)
- Arquivo: `<nome-do-workflow>-modificação-<descrição>-plano.md`
- Conteúdo:
  - Análise do estado atual
  - Ponto de intervenção
  - Nodes a criar/modificar
  - Conexões a adicionar/remover
  - Fluxo modificado
  - Arquivos de configuração (.nodes, .params, .formula)

---

**Criado com**: `/meta-skill`
**Data**: 2025-02-05
**Versão**: 1.0
