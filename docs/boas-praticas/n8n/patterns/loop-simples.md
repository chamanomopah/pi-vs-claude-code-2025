# Padrão: Loop Simples

Processa uma lista de itens sequencialmente, um por vez.

## Quando Usar

- Processar cada item de uma lista individualmente
- Aplicar a mesma lógica a todos os itens
- Fazer chamadas de API para cada item
- Salvar/criar registros individualmente

## Estrutura

```
[Source] → [Split In Batches] → main[1] → [Process] → [Wait] → volta
                               └─ main[0] → [Próximo]
```

## Implementação

### Node 1: Source
Fornece a lista de itens a serem processados.

**Saída:** `{ items: [...] }`

### Node 2: Split In Batches
Configurações:
- **Batch Size:** 1
- **Reset:** false

**Conexões:**
- `main[0]` → Node 4 (Próximo)
- `main[1]` → Node 3 (Process)

### Node 3: Process
Processa cada item individualmente.

**Entrada:** Cada item da lista
**Saída:** Item processado
**Conecta a:** Node 4 (Wait)

### Node 4: Wait
Configurações:
- **Time:** 100ms (ou conforme necessário)

**Conecta a:** Node 2 (volta ao Split In Batches)

### Node 5: Próximo (opcional)
Continua o fluxo após o loop terminar.

**Entrada:** `{ finished: true, numberOfBatches: N }`

## Exemplo Prático

### Processar Pedidos

```
[Webhook: pedidos] → [Split In Batches] → main[1] → [Valida API] → [Wait] → volta
                                                 └─ main[0] → [Resposta]
```

**Node 2: Split In Batches**
- Batch Size: 1
- Reset: false

**Node 3: Valida API**
- HTTP Request
- URL: `{{ $json.apiUrl }}`
- Method: POST

**Node 4: Wait**
- Time: 500ms (respeitar rate limit)

## Variação: Com Tratamento de Lista Vazia

```
[Source] → [IF: Empty?] ──true→ [Skip] → [Fim]
              └─false→ [Split In Batches] → main[1] → [Process] → [Wait] → volta
                                           └─ main[0] → [Próximo]
```

**Node 2: IF: Empty?**
- Condição: `{{ $json.items.length === 0 }}`

## Variação: Com Acumulador

```
[Source] → [Split In Batches] → main[1] → [Process] → [Accumulate] → [Wait] → volta
          main[0] → [Read Accumulator] → [Próximo]
```

**Node 4: Accumulate**
- Function node que acumula resultados
- Ex: soma, contagem, lista de erros

## Validações

- ✅ main[0] conectado ao fluxo após o loop
- ✅ main[1] conectado ao processamento
- ✅ Wait node antes de voltar ao Split
- ✅ Lista vazia tratada (se aplicável)
- ✅ Batch Size configurado corretamente

## Erros Comuns

### ❌ Esquecer Wait
```
[Split] → main[1] → [Process] → volta direto
```
**Problema:** Race conditions

### ❌ Não Conectar main[0]
```
[Split] → main[1] → [Process] → [Wait] → volta
(main[0] não conectado)
```
**Problema:** Fluxo nunca continua após o loop

### ❌ Batch Size Muito Grande
```
Batch Size: 1000
```
**Problema:** Timeout ou memory issues
