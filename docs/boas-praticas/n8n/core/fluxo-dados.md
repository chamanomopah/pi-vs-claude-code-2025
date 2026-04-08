# Fluxo de Dados

Documentar e entender o fluxo de dados é essencial para workflows confiáveis.

## Documentação de Entrada/Saída

Para CADA node, documente:

```yaml
Node X:
  Entrada:
    - Campo: tipo (ex: userId: string)
    - Formato: object/array/string
  
  Saída:
    - Campo: tipo
    - Formato: object/array/string
  
  Transformações:
    - O que é modificado/criado
```

## Expressões Comuns

### Acessar Dados

```javascript
// Campo do item atual
{{ $json.campo }}

// Campo aninhado
{{ $json.nested.value }}

// Primeiro item (índice 0)
{{ $item(0).json.campo }}

// Último item
{{ $item($json.length - 1).json.campo }}

// Todos os itens
{{ $json.items }}
```

### Funções Úteis

```javascript
// Tamanho de array
{{ $json.items.length }}

// Timestamp atual
{{ $now().toISO() }}

// String operations
{{ $json.text.toUpperCase() }}
{{ $json.text.toLowerCase() }}
{{ $json.text.trim() }}

// Math
{{ $json.value * 2 }}
{{ $json.sum + $json.tax }}

// Conditionals
{{ $json.age >= 18 ? 'adult' : 'minor' }}
```

## Campos Criados/Modificados

Sempre liste:
- Campos NOVOS criados pelo node
- Campos MODIFICADOS pelo node
- Campos que passam inalterados

### Exemplo de Documentação

```yaml
Node: Calcula Total
  Entrada:
    - items: array
    - taxRate: number
  
  Saída:
    - subtotal: number (NOVO)
    - taxAmount: number (NOVO)
    - total: number (NOVO)
    - items: array (inalterado)
    - taxRate: number (inalterado)
```

## Transformação de Dados

### Function Node

```javascript
// Criar novos campos
return [
  {
    json: {
      ...input.item.json,
      total: input.item.json.price * input.item.json.qty,
      processed: true
    }
  }
];
```

### Set Node

```javascript
// Adicionar campo
{{ { ...$json, total: $json.price * $json.qty } }}

// Modificar campo
{{ { ...$json, status: 'processed' } }}
```

## Padrões de Fluxo de Dados

### Enrichment (Adicionar Dados)

```
[Original Data] → [HTTP Request] → [Merge] → [Enriched Data]
                 [External API] ↗
```

### Filtering (Filtrar)

```
[All Items] → [IF: condition?] ──true→ [Keep]
                       └─false→ [Discard]
```

### Transformation (Transformar)

```
[Raw Data] → [Function] → [Transformed Data]
```

### Aggregation (Agregação)

```
[Items] → [Split] → [Process] → [Accumulate] → [Wait] → volta
            main[0] → [Read Accumulator] → [Aggregated]
```

## Tipagem de Dados

### Cast de Tipos

```javascript
// String para número
{{ Number($json.value) }}

// Número para string
{{ String($json.value) }}

// String para boolean
{{ $json.value === 'true' }}

// Parse JSON
{{ JSON.parse($json.data) }}
```

### Validação de Tipos

```javascript
// Verificar se é número
{{ typeof $json.value === 'number' }}

// Verificar se é array
{{ Array.isArray($json.items) }}

// Verificar se é null/undefined
{{ $json.value != null }}
```

## Tratamento de Erros

### Try/Catch em IF Node

```
[Process] → [IF: Success?] ──true→ [Continue]
                    └─false→ [Handle Error]
```

### Validação Antes

```
[Input] → [IF: Valid?] ──true→ [Process]
                └─false→ [Error Response]
```

## Padrões Nomenclatura

### Campos
- ✅ `camelCase`: firstName, totalPrice, isActive
- ❌ `snake_case`: first_name, total_price
- ❌ `PascalCase`: FirstName, TotalPrice

### Expressões
- ✅ Claras e descritivas: `{{ $json.price * $json.qty }}`
- ❌ Confusas: `{{ $json.a * $json.b }}`

## Anti-Padrões

### ❌ Assumir Tipo Sem Validar
```javascript
{{ $json.value.toUpperCase() }} // Pode falhar se não for string
```

**Correto:**
```javascript
{{ typeof $json.value === 'string' ? $json.value.toUpperCase() : '' }}
```

### ❌ Campos Mal Documentados
```
Node transforma dados (sem detalhes)
```

**Correto:**
```
Node Transform:
  Entrada: { raw: string }
  Saída: { parsed: object, timestamp: string }
```

### ❌ Expressões Complexas em Um Node
```javascript
{{ $json.a && $json.b ? $json.c : ($json.d ? $json.e : $json.f) }}
```

**Correto:** Dividir em múltiplos IFs ou Function nodes

## Checklist

- [ ] Todos os campos de entrada documentados
- [ ] Todos os campos de saída documentados
- [ ] Tipos de dados especificados
- [ ] Expressões validadas
- [ ] Campos nulos tratados
- [ ] Transformações documentadas
