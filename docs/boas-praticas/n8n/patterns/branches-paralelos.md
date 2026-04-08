# Padrão: Branches Paralelos

Processa itens em paralelo usando múltiplos branches e depois sincroniza.

## Quando Usar

- Processar o mesmo item de formas diferentes
- Fazer múltiplas chamadas de API simultâneas
- Enriquecer dados de múltiplas fontes
- Executar validações paralelas

## Estrutura

```
[Split] → main[1] ──┬─▶ [Branch A] ──┐
                   │                ├──▶ [Merge Wait] → [Wait] → volta ao Split
                   └─▶ [Branch B] ──┘
```

## Implementação

### Node 1: Split In Batches
Configurações:
- **Batch Size:** 1
- **Reset:** false

**Conexões:**
- `main[0]` → Node 6 (Próximo)
- `main[1]` → Node 2 (Branch A)

### Node 2: Branch A
Primeira branch de processamento.

**Exemplos:**
- HTTP Request para API A
- Database query
- Validation logic

**Conecta a:** Node 5 (Merge)

### Node 3: Branch B
Segunda branch de processamento.

**Exemplos:**
- HTTP Request para API B
- File operation
- Transformation logic

**Conecta a:** Node 5 (Merge)

### Node 4: Branch C (opcional)
Terceira branch (ou mais).

**Conecta a:** Node 5 (Merge)

### Node 5: Merge (Wait)
Sincroniza todas as branches.

**Mode:** Wait
**Inputs:** Todas as branches devem estar conectadas

**Conecta a:** Node 6 (Wait)

### Node 6: Wait
Sincroniza antes de voltar ao loop.

**Time:** 100ms

**Conecta a:** Node 1 (volta ao Split In Batches)

## Exemplo Prático

### Enriquecer Lead com Múltiplas APIs

```
[Webhook: lead] → [IF: Empty?] ──true→ [Skip]
              └─false→ [Split] → main[1] ──┬─▶ [HubSpot API] ──┐
                                         ├─▶ [Salesforce API]─┤
                                         └─▶ [Clearbit API]───┤
                                                            [Merge Wait] → [Wait] → volta
                                         main[0] → [Combine All Data] → [Response]
```

**Node 2: HubSpot API**
- HTTP Request
- URL: `https://api.hubapi.com/contacts/{{ $json.email }}`
- Method: GET

**Node 3: Salesforce API**
- HTTP Request
- URL: `https://api.salesforce.com/lead/{{ $json.email }}`
- Method: GET

**Node 4: Clearbit API**
- HTTP Request
- URL: `https://api.clearbit.com/v1/people/email/{{ $json.email }}`
- Method: GET

**Node 5: Merge Wait**
- Mode: Wait
- Aguarda todas as 3 APIs

**Node 7: Combine All Data**
- Function node
- Junta dados de todas as APIs

## Variação: Branches Condicionais

```
[Split] → main[1] → [IF: Type?] ──true→ [Branch A] ─┐
                           └─false→ [Branch B] ──┤
                                                   ├──▶ [Merge Wait] → [Wait] → volta
```

### Node 2: IF: Type?
- Condição: `{{ $json.type === 'premium' }}`

### Node 3: Branch A (Premium)
- Processamento premium
- Mais APIs, mais validações

### Node 4: Branch B (Standard)
- Processamento standard
- Menos APIs, validações básicas

## Variação: Com Transformação em Cada Branch

```
[Split] → main[1] ──┬─▶ [API A] → [Transform A] ──┐
                   └─▶ [API B] → [Transform B] ──┤
                                               ├──▶ [Merge Wait] → [Wait] → volta
```

**Node 3: Transform A**
- Function node
- Adapta dados da API A

**Node 5: Transform B**
- Function node
- Adapta dados da API B

## Sincronização

### Por Que Usar Wait?

Sem Wait:
```
[Branch A] ──┐
             ├──▶ [Merge] → [Wait]
[Branch B] ──┘
```
**Problema:** Branch que terminar primeiro continua, Merge pode não ter todos os dados

Com Wait:
```
[Branch A] ──┐
             ├──▶ [Merge Wait] → Aguarda AMBOS → [Wait]
[Branch B] ──┘
```
**Correto:** Merge aguarda todas as branches

### Tempo de Timeout

Configure timeout se as branches podem demorar muito:

**Node Merge:**
- Mode: Wait
- Options: Timeout (ex: 30000ms)

## Combinação de Dados

### Merge Mode: Append

```
[Branch A: [{a:1}]] ──┐
                     ├──▶ [Merge Append] → [{a:1}, {b:2}]
[Branch B: [{b:2}]] ──┘
```

### Merge Mode: Merge by Key

```
[Branch A: {id:1, name:"A"}] ──┐
                             ├──▶ [Merge by Key: id] → {id:1, name:"A", value:100}
[Branch B: {id:1, value:100}]┘
```

### Manual (Function Node)

```javascript
// No Function node após Merge
const items = $input.all();
const branchAData = items[0].json;
const branchBData = items[1].json;

return [{
  json: {
    ...branchAData,
    ...branchBData,
    combinedAt: new Date().toISOString()
  }
}];
```

## Performance

### Paralelo vs Sequencial

**Sequencial (lento):**
```
[Split] → [API A] → [API B] → [API C] → [Wait] → volta
Tempo: 100ms + 150ms + 80ms = 330ms
```

**Paralelo (rápido):**
```
[Split] ──┬─▶ [API A: 100ms] ──┐
          ├─▶ [API B: 150ms] ──┼─▶ [Merge Wait]
          └─▶ [API C: 80ms] ───┘
Tempo: max(100, 150, 80) = 150ms
```

## Validações

- ✅ Todas as branches convergem para o Merge
- ✅ Merge está no modo Wait
- ✅ Wait node após o Merge
- ✅ Timeout configurado (se necessário)
- ✅ Dados são combinados corretamente

## Erros Comuns

### ❌ Branch Não Conectada
```
[Branch A] ──┐
             ├──▶ [Merge Wait]
[Branch B]    (não conectada!)
```
**Problema:** Merge nunca executa (aguarda eternamente)

### ❌ Sem Wait Após Merge
```
[Branch A] ──┐
             ├──▶ [Merge Wait] → volta direto
[Branch B] ──┘
```
**Problema:** Race condition, dados podem não estar prontos

### ❌ Muitas Branches Paralelas
```
[Split] ──┬─▶ [A]
          ├─▶ [B]
          ├─▶ [C]
          ├─▶ [D]
          └─▶ [E]
```
**Problema:** Pode exceder rate limits ou causar timeout
