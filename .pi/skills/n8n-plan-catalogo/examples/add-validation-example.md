# Exemplo de Plano de Modificação: Adicionar Validação

## Prompt Original

```
/n8n-plan-catalogo "bhlDnM03ko0aq" "adicionar validação de email no início do workflow"
```

---

# Plano de Modificação: Lead Router com Validação de Email

## Resumo
Adicionar validação de email no início do workflow existente para rejeitar leads com emails inválidos antes do processamento principal.

## Análise Atual
- **Workflow**: Simple Lead Router Demo (ID: bhlDnM03ko0aq)
- **Nodes existentes**: 4 nodes (Webhook, Set Normalize, Code Classify, Switch Router)
- **Fluxo atual**: Webhook → Set Normalize → Code Classify → Switch Router → 4 branches
- **Ponto de intervenção**: Após Webhook, antes de Set Normalize

## Nodes Existentes Relevantes
| Nome | Tipo | Propósito Atual |
|------|------|----------------|
| Webhook | webhook | Recebe leads via POST |
| Set Normalize | set | Normaliza campos (trim, lowercase, cast) |
| Code Classify | code | Classifica lead em lane (Invalid/HighPriority/Partner/Standard) |
| Switch Router | switch | Rotear para 4 branches independentes |

## Modificação Proposta

### 1. O que será adicionado
Validação de email usando Filter node para rejeitar leads com email inválido antes do processamento normal.

### 2. Nodes a Criar
| Nome | Tipo (do catálogo) | Propósito |
|------|-------------------|-----------|
| Filter Valid Email | n8n-nodes-base.filter | Filtrar apenas emails válidos |
| Set Error Message | n8n-nodes-base.set | Adicionar mensagem de erro |
| Respond Invalid | n8n-nodes-base.respondToWebhook | Responder ao webhook com erro |

### 3. Conexões a Adicionar/Modificar
| Origem | Destino | Tipo | Ação |
|--------|---------|------|------|
| Webhook | Filter Valid Email | main | NOVA |
| Filter Valid Email | Set Normalize | main | NOVA (saída TRUE) |
| Filter Valid Email | Set Error Message | main | NOVA (saída FALSE) |
| Set Error Message | Respond Invalid | main | NOVA |
| Webhook | Set Normalize | main | REMOVER |

### 4. Parâmetros a Configurar

#### Filter Valid Email
- **conditions**:
  - leftValue: `{{ $json.email }}`
  - operator: `contains`
  - rightValue: `@`
  - combinator: `and`
  - Segunda condição:
    - leftValue: `{{ $json.email }}`
    - operator: `isNotEmpty`
- **Output**: TRUE (email válido) → continua para Set Normalize
- **Output**: FALSE (email inválido) → vai para Set Error Message

#### Set Error Message
- **mode**: "Merge into existing JSON"
- **fields to add**:
  ```json
  {
    "error": "INVALID_EMAIL",
    "message": "Email address is required and must contain @"
  }
  ```

#### Respond Invalid
- **respondWith**: "text"
- **responseBody**: `{{ $json.message }}`
- **options.status**: "400"

### 5. Fluxo Modificado

**Antes**:
```
Webhook → Set Normalize → Code Classify → Switch Router → 4 branches
```

**Depois**:
```
Webhook → Filter Valid Email → [TRUE] → Set Normalize → Code Classify → Switch Router → 4 branches
                              → [FALSE] → Set Error Message → Respond Invalid (FIM)
```

## Nodes Necessários (Consolidado)
| Nome | Tipo (do catálogo) | ConnectionType | Propósito |
|------|-------------------|----------------|-----------|
| Filter Valid Email | n8n-nodes-base.filter | main | Validar email |
| Set Error Message | n8n-nodes-base.set | main | Adicionar erro |
| Respond Invalid | n8n-nodes-base.respondToWebhook | main | Responder erro |

**Total: 3 nodes novos** (workflow terá 7 nodes no total)

## Validação de Catálogo

### Verificação de Nodes
- [x] `n8n-nodes-base.filter` - ✅ Disponível (linha 174 do catalogo_nodes.py)
- [x] `n8n-nodes-base.set` - ✅ Disponível (linha 19)
- [x] `n8n-nodes-base.respondToWebhook` - ✅ Disponível (linha 501)

### ConnectionTypes
- filter: `main` ✅
- set: `main` ✅
- respondToWebhook: `main` ✅

## Considerações Especiais

### Credenciais Necessárias
Nenhuma (nodes locais, sem integrações externas)

### Pré-requisitos
- Webhook existente deve aceitar método POST
- Response mode deve estar configurado para "responseNode" (Webhook)

### Impacto no Fluxo Atual
- **Mínimo**: Apenas adiciona filtro no início
- **Não invasivo**: Não modifica lógica existente de classificação
- **Performance**: Adiciona 1 operação de filtro (negligenciável)

### Limitações
- Apenas valida que email contém "@" e não está vazio
- Não valida formato completo de email (regex complexo)
- Para validação mais robusta, poderia usar Code node com regex

### Trade-offs Opcionais

#### Versão Simples (Atual)
**Nodes**: 3 nodes (Filter, Set, Respond)
**Validação**: Contém "@" + não vazio
**Implementação**: Rápida, nativa do n8n

#### Versão Robusta (Opcional)
**Nodes adicionais**: +1 node (Code com regex)
**Validação**: Regex completo de email
**Código Code**:
```javascript
const email = $json.email;
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const isValid = emailRegex.test(email);
return isValid ? [{ json: $json }] : [];
```

## Checklist Pré-Implementação

- [x] Catálogo verificado para todos os nodes
- [x] connectionTypes estão corretos
- [x] Ponto de intervenção identificado (após Webhook)
- [x] Conexões a remover documentadas
- [x] Conexões a adicionar documentadas
- [x] Impacto no fluxo atual analisado
- [x] Limitações documentadas
- [x] Trade-offs discutidos (validação simples vs robusta)
