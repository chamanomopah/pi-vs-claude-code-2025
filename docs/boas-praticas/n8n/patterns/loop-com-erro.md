# Padrão: Loop com Tratamento de Erro

Processa itens individualmente com tratamento de erros para cada item.

## Quando Usar

- APIs que podem falhar para alguns itens
- Processamento onde erros não devem interromper tudo
- Need to log errors but continue processing
- Requer relatório final de sucessos e falhas

## Estrutura

```
[Split] → main[1] → [Try] → [IF: Success?] ──true→ [Log Success] → [Merge] → [Wait] → volta
                                 └─false→ [Log Error] ─────────────────┘
          └─ main[0] → [Generate Report]
```

## Implementação

### Node 1: Split In Batches
Configurações:
- **Batch Size:** 1
- **Reset:** false

**Conexões:**
- `main[0]` → Node 6 (Generate Report)
- `main[1]` → Node 2 (Try)

### Node 2: Try (Operation)
Executa a operação que pode falhar.

**Exemplos:**
- HTTP Request para API externa
- Chamada de banco de dados
- Processamento complexo

**Conecta a:** Node 3 (IF: Success?)

### Node 3: IF: Success?
Verifica se a operação foi bem-sucedida.

**Condição:** Depende do node anterior
- HTTP Request: `{{ $json.statusCode === 200 }}`
- Database: `{{ $json.success === true }}`

**Conexões:**
- `true` → Node 4 (Log Success)
- `false` → Node 5 (Log Error)

### Node 4: Log Success
Registra o sucesso (opcional).

**Ações:**
- Add to success list
- Log to database
- Send success notification

**Conecta a:** Node 6 (Merge)

### Node 5: Log Error
Registra o erro.

**Ações:**
- Add to error list
- Log error details
- Send error notification

**Conecta a:** Node 6 (Merge)

### Node 6: Merge (Wait)
Aguarda ambos os branches (success ou error).

**Mode:** Wait

**Conecta a:** Node 7 (Wait)

### Node 7: Wait
Sincroniza antes de voltar ao loop.

**Time:** 100ms

**Conecta a:** Node 1 (volta ao Split In Batches)

### Node 8: Generate Report
Gera relatório final após o loop completar.

**Entrada:** `{ finished: true, numberOfBatches: N }`

**Ações:**
- Count successes vs errors
- Generate summary
- Send final notification

## Exemplo Prático

### Processar Pedidos com API Instável

```
[Webhook] → [IF: Empty?] ──true→ [Report: Empty]
              └─false→ [Split] → main[1] → [API Request] → [IF: 200?] ──true→ [Log OK] → [Merge]
                                                         └─false→ [Log Error] ────┤
                                   main[0] → [Generate Final Report]          │
                                                                        ↓     ↓
                                                                   [Wait] → [Merge] → volta
```

**Node 4: API Request**
- Method: POST
- URL: `https://api.example.com/process`
- Retry on Fail: 3

**Node 5: IF: 200?**
- Condição: `{{ $json.statusCode === 200 }}`

**Node 6: Log OK**
- Google Sheets (append)
- Sheet: "success_log"

**Node 7: Log Error**
- Google Sheets (append)
- Sheet: "error_log"
- Campos: error, statusCode, itemId

**Node 10: Generate Final Report**
- Function node
- Count successes e errors
- Generate summary message

## Variação: Com Retry

```
[Split] → main[1] → [Try] → [IF: Success?] ──true→ [Log Success] → [Merge]
                                 └─false→ [IF: Retry < 3?] ──true→ [Wait] → [Retry Count] → volta
                                                              └─false→ [Log Error] → [Merge]
```

**Node 6: IF: Retry < 3?**
- Condição: `{{ $json.retryCount < 3 }}`

**Node 7: Wait**
- Time: 1000ms (backoff)

**Node 8: Retry Count**
- Function: `{{ { ...$json, retryCount: $json.retryCount + 1 } }}`
- Conecta de volta ao Node 2 (Try)

## Dados Acumulados

### Option 1: Memory (Function Node)

```javascript
// No final do loop (main[0])
let totalSuccess = 0;
let totalError = 0;

// Process all items
for (const item of items) {
  if (item.success) totalSuccess++;
  else totalError++;
}

return [{ json: { totalSuccess, totalError, total: items.length } }];
```

### Option 2: External Storage

```
[Log Success] → [Google Sheets: success_log]
[Log Error] → [Google Sheets: error_log]
[Generate Report] → [Read Sheets] → [Count]
```

## Validações

- ✅ Ambos os branches (success/error) convergem para Merge
- ✅ Merge está no modo Wait
- ✅ Erros são logados mas não interrompem o loop
- ✅ Relatório final usa main[0]
- ✅ Wait antes de voltar ao loop

## Erros Comuns

### ❌ Não Tratar Erro
```
[Split] → main[1] → [API Request] → [Wait] → volta
```
**Problema:** Um erro interrompe o loop inteiro

### ❌ Branch Sem Convergência
```
[IF Success] ──true→ [Log Success] → [Merge]
           └─false→ [Log Error] (não conecta ao Merge!)
```
**Problema:** Merge nunca recebe dados do branch de erro

### ❌ Não Gerar Relatório Final
```
[Split] → main[1] → [Loop with Error Handling]
(main[0] não conectado)
```
**Problema:** Não há visibilidade do resultado final
