# IF e Switch Nodes

Nodes para controle de fluxo condicional.

## IF Node

### Propósito
Executa分支 baseado em condição booleana (true/false).

### Configuração

#### Condição Simples
```javascript
{{ $json.age >= 18 }}
```

#### Condição Composta
```javascript
{{ $json.age >= 18 && $json.country === 'BR' }}
```

#### Comparação de Strings
```javascript
{{ $json.status === 'active' }}
```

#### Verificação de Nulo
```javascript
{{ $json.value != null }}
```

#### Verificação de Array
```javascript
{{ Array.isArray($json.items) && $json.items.length > 0 }}
```

### Operadores Lógicos

#### AND
```javascript
{{ $json.a && $json.b }}
// Ou
{{ $json.age >= 18 && $json.country === 'BR' }}
```

#### OR
```javascript
{{ $json.a || $json.b }}
// Ou
{{ $json.type === 'premium' || $json.type === 'vip' }}
```

#### NOT
```javascript
{{ !$json.disabled }}
```

### Operadores de Comparação

#### Igualdade
```javascript
{{ $json.status === 'active' }}
```

#### Diferença
```javascript
{{ $json.status !== 'inactive' }}
```

#### Maior/Menor
```javascript
{{ $json.age > 18 }}
{{ $json.score >= 100 }}
{{ $json.price < 1000 }}
{{ $json.quantity <= 10 }}
```

### Type Casting

#### String para Número
```javascript
{{ Number($json.value) > 10 }}
```

#### String para Boolean
```javascript
{{ $json.value === 'true' }}
```

## Switch Node

### Propósito
Executa分支 baseado em múltiplas condições.

### Configuração

#### Rules (Regras)

Cada regra tem:
- **Output**: Nome da saída
- **Conditions**: Uma ou mais condições
- **Combine Operation**: ALL (AND) ou ANY (OR)

#### Exemplo: Classificação por Tipo

```javascript
Regra 1: "Premium"
  Conditions: 
    - Field: type
    - Operation: Equals
    - Value: premium

Regra 2: "Standard"
  Conditions:
    - Field: type
    - Operation: Equals
    - Value: standard

Regra 3: "Free"
  Conditions:
    - Field: type
    - Operation: Equals
    - Value: free
```

#### Expressions em Switch

```javascript
// Campo dinâmico
{{ $json.userType }}

// Com operações
{{ $json.score >= 100 }}

// Com funções
{{ $json.email.toLowerCase() }}
```

## Padrões de Uso

### Padrão 1: Validação Simples

```
[Input] → [IF: isValid?] ──true→ [Process]
                      └─false→ [Error]
```

**Node IF:**
- Condição: `{{ $json.email.includes('@') }}`

### Padrão 2: Validação Múltipla

```
[Input] → [IF: hasEmail?] ──true→ [IF: hasName?] ──true→ [Process]
                      └─false→ [Error: No Email]     └─false→ [Error: No Name]
```

### Padrão 3: Switch para Tipos

```
[Input] → [Switch: userType] → Premium → [Process Premium]
                          → Standard → [Process Standard]
                          → Free → [Process Free]
```

### Padrão 4: Default Route

```
[Input] → [IF: Known?] ──true→ [Process Known]
                      └─false→ [Process Default]
```

## Condições Comuns

### Verificar se Campo Existe
```javascript
{{ $json.field != null }}
```

### Verificar se Array não Vazio
```javascript
{{ Array.isArray($json.items) && $json.items.length > 0 }}
```

### Verificar se String não Vazia
```javascript
{{ $json.text && $json.text.trim().length > 0 }}
```

### Verificar Range
```javascript
{{ $json.age >= 18 && $json.age <= 65 }}
```

### Verificar Lista de Valores
```javascript
{{ ['premium', 'vip', 'gold'].includes($json.type) }}
```

### Verificar Regex
```javascript
{{ /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test($json.email) }}
```

## Aninhamento

### IF Aninhado

```
[Input] → [IF: A?] ──true→ [IF: B?] ──true→ [Result AB]
                └─false→ [IF: C?] ──true→ [Result AC]
                          └─false→ [Result A]
```

### Switch após IF

```
[Input] → [IF: isValid?] ──true→ [Switch: Type] → Premium → [Process P]
                                             → Standard → [Process S]
                      └─false→ [Error]
```

## Dicas

### ✅ Use IF para binário
```
[IF: isActive?] ──true→ [Enable]
              └─false→ [Disable]
```

### ✅ Use Switch para múltiplos
```
[Switch: status] → Active → [Process Active]
              → Pending → [Process Pending]
              → Inactive → [Process Inactive]
```

### ✅ Valide antes de processar
```
[Input] → [IF: Valid?] ──true→ [Process]
                      └─false→ [Error Response]
```

### ✅ Use nomes descritivos nas saídas
```
[Switch: userType] → Premium → [Process Premium]
              → Standard → [Process Standard]
```

## Anti-Padrões

### ❌ Condições Muito Complexas
```javascript
{{ $json.a && $json.b ? ($json.c ? true : false) : ($json.d ? true : false) }}
```

**Correto:** Dividir em múltiplos IFs

### ❌ Esquecer Branch False
```
[IF: condition?] ──true→ [Process]
(false branch não conectada)
```

**Problema:** Dados que não atendem condição são perdidos

### ❌ Switch sem Default
```
[Switch: type] → A → [Process A]
           → B → [Process B]
(se C chegar, não há rota!)
```

**Correto:** Adicione regra "Default" ou trate no IF anterior

### ❌ Type Mismatch
```javascript
{{ $json.age === '18' }} // age é número, '18' é string
```

**Correto:**
```javascript
{{ $json.age === 18 }}
// ou
{{ Number($json.age) === 18 }}
```

## Validações

### Para IF Node
- [ ] Condição retorna boolean
- [ ] Ambos os branches (true/false) conectados
- [ ] Type casting correto
- [ ] Não há condições aninhadas muito complexas

### Para Switch Node
- [ ] Todas as saídas conectadas
- [ ] Regra "Default" existe (se necessário)
- [ ] Operação lógica correta (ALL/ANY)
- [ ] Nomes de saídas são descritivos

## Teste de Condições

### Testar Localmente
```javascript
// No Function node antes do IF
console.log($json.age); // Verificar valor
console.log(typeof $json.age); // Verificar tipo
return [{ json: $json }];
```

### Testar com IF
```
[Input] → [Function: Log] → [IF: condition?] → ...
```

**Function Node:**
```javascript
console.log('Input:', JSON.stringify($json, null, 2));
return [{ json: $json }];
```
