# Exemplo Completo: Como os 3 Agentes Trabalham Juntos

Este documento demonstra um exemplo prático de como os agentes n8n-architect, n8n-builder e n8n-tester colaboram para criar um workflow funcional.

## Cenário: Processador de Pedidos de E-commerce

O usuário solicita: *"Preciso de um workflow n8n que receba pedidos de e-commerce, valide cada produto com uma API externa, atualize o estoque no banco de dados, envie confirmação por Telegram para cada cliente, e gere um relatório final ao processar todos os pedidos."*

---

## FASE 1: n8n-architect (Projeto)

### Entrada do Usuário
```
"Preciso de um workflow n8n que receba pedidos de e-commerce,
valide cada produto com uma API externa, atualize o estoque
no banco de dados, envie confirmação por Telegram para cada
cliente, e gere um relatório final ao processar todos os pedidos."
```

### Análise do Architect
- **Entrada**: Webhook com lista de pedidos
- **Processamento**: Loop em cada pedido → validação → atualização DB → notificação
- **Saída**: Relatório final + Webhook response

### Estrutura Projetada

```
[Webhook Receiver]
     │
     ▼
[Split In Batches] ──main[0]──▶ [Gera Relatório Final] ──▶ [Webhook Response]
     │
     └─main[1]──▶ [Valida API Externa]
                    │
                    ▼
                 [IF: API Sucesso?]
                    │
           ┌────────┴────────┐
           │                 │
         Sim               Não
           │                 │
           ▼                 ▼
    [Atualiza Estoque]  [Log Erro]
           │                 │
           └────────┬────────┘
                    ▼
           [Envia Telegram]
                    │
                    ▼
               [Wait] ────▶ volta para Split In Batches
```

### Especificação Detalhada Entregue

```yaml
WORKFLOW: Processador de Pedidos E-commerce

NODES:

1. Webhook Receiver
   Tipo: Webhook
   Path: /pedidos/processar
   Method: POST
   Response Mode: via 'Respond to Webhook' node
   Saída: { pedidos: [{id, produto, qty, cliente_email, cliente_telegram}] }

2. Split In Batches
   Tipo: Split In Batches
   Batch Size: 1
   Reset: false
   Entrada: Lista de pedidos
   Saída main[0]: { finished: true, total: N }
   Saída main[1]: Cada pedido individual
   Conexão main[0]: Node 9 (Gera Relatório)
   Conexão main[1]: Node 3 (Valida API)

3. Valida API Externa
   Tipo: HTTP Request
   Method: GET
   URL: https://api.produtos.com/validate/{{$json.id}}
   Auth: Bearer Token (env: PRODUTOS_API_KEY)
   Saída: { valid: true/false, stock: N }
   Conexão: Node 4 (IF Sucesso)

4. IF: API Sucesso?
   Tipo: IF
   Condição: {{$json.valid === true}}
   Saída true: Node 5 (Atualiza Estoque)
   Saída false: Node 7 (Log Erro)

5. Atualiza Estoque
   Tipo: Postgres (ou MySQL)
   Operação: UPDATE
   Tabela: produtos
   Where: id = {{$json.id}}
   Campos: stock = stock - {{$json.qty}}
   Conexão: Node 8 (Envia Telegram)

6. (conecta ambas as saídas do IF)
   Tipo: Merge
   Modo: Wait (aguarda ambos os branches)
   Conexão entrada1: Node 5 (sucesso)
   Conexão entrada2: Node 7 (erro)
   Saída: Node 8 (Envia Telegram)

7. Log Erro
   Tipo: No-Op (ou escreve em log)
   Dados: {{$json}}
   Conexão: Node 6 (Merge)

8. Envia Telegram
   Tipo: Telegram
   Chat ID: {{$json.cliente_telegram}}
   Mensagem: "Pedido #{{$json.id}} processado com sucesso!"
   Conexão: Node 9 (Wait)

9. Wait
   Tipo: Wait
   Tempo: 1s (ou wait for webhook)
   Conexão: Volta para Node 2 (Split In Batches)

10. Gera Relatório Final
    Tipo: Function
    Código: |
      return {
        json: {
          total_pedidos: $input.all().length,
          data_hora: new Date().toISOString(),
          status: 'completo'
        }
      }
    Conexão: Node 11 (Webhook Response)

11. Webhook Response
    Tipo: Respond to Webhook
    Status: 200
    Body: {{$json}}
    Conexão: FIM

FLUXO DE DADOS:
- Webhook recebe lista de pedidos
- Split In Batches separa cada pedido
- Loop: valida → atualiza → notifica → volta ao split
- Quando todos processados → gera relatório → responde webhook

NOTAS ESPECIAIS:
- CUIDADO: Node 6 (Merge) precisa AMBAS as entradas conectadas
- CUIDADO: Node 9 (Wait) deve reconectar para Node 2 (Split)
- API Externa pode falhar: tratar erros no IF node
```

---

## FASE 2: n8n-builder (Implementação)

### Entrada do Builder
Especificação completa criada pelo n8n-architect

### Ações Executadas

```bash
# 1. Cria workflow novo
python tools/n8n/workflow_create.py \
  --name "Processador de Pedidos" \
  --active false

# 2. Cria todos os nodes
python tools/n8n/nodes_create.py \
  --nodes webhook,split-in-batches,http-request,if,merge,postgres,telegram,wait,function,respond-webhook

# 3. Cria conexões
python tools/n8n/connections_create.py \
  --from webhook --to split-in-batches
python tools/n8n/connections_create.py \
  --from split-in-batches --to http-request --output main[1]
python tools/n8n/connections_create.py \
  --from split-in-batches --to function --output main[0]
# ... (todas as conexões especificadas)

# 4. Configura parâmetros
python tools/n8n/parameters.py \
  --node webhook --param path --value "/pedidos/processar"
python tools/n8n/parameters.py \
  --node http-request --param url --value "https://api.produtos.com/validate/{{$json.id}}"
# ... (todos os parâmetros)
```

### Saída do Builder
- Workflow criado no n8n
- ID do workflow: `workflow_abc123`
- Arquivo JSON exportado

---

## FASE 3: n8n-tester (Testes)

### Testes Executados

#### Teste 1: Dados Válidos
```bash
curl -X POST http://localhost:5678/webhook/pedidos/processar \
  -H "Content-Type: application/json" \
  -d '{
    "pedidos": [
      {"id": "P001", "produto": "Notebook", "qty": 1, "cliente_email": "user1@email.com", "cliente_telegram": "123456"},
      {"id": "P002", "produto": "Mouse", "qty": 2, "cliente_email": "user2@email.com", "cliente_telegram": "789012"}
    ]
  }'
```

**Resultado**: ✅ Workflow executou, enviou mensagens Telegram, retornou 200

#### Teste 2: Lista Vazia
```bash
curl -X POST http://localhost:5678/webhook/pedidos/processar \
  -H "Content-Type: application/json" \
  -d '{"pedidos": []}'
```

**Resultado**: ❌ **BUG ENCONTRADO**

#### Teste 3: API Retorna Erro
```bash
# Mock da API retornando erro
curl -X POST http://localhost:5678/webhook/pedidos/processar \
  -H "Content-Type: application/json" \
  -d '{"pedidos": [{"id": "INVALIDO", ...}]}'
```

**Resultado**: ❌ **BUG ENCONTRADO**

### Bug Report Entregue

```markdown
# Relatório de Testes - Processador de Pedidos

## Status: 🔴 REPROVADO

## Bugs Encontrados

### BUG #1: Loop não processa lista vazia
**Severidade**: 🟡 MÉDIA
**Localização**: Split In Batches (node-2)

**Problema**:
Quando a lista de pedidos está vazia, o workflow fica preso no Split In Batches e nunca continua para o Gera Relatório Final.

**Causa**:
Split In Batches não tem tratamento para lista vazia. main[0] só executa após processar pelo menos 1 item.

**Solução Proposta**:
Adicionar IF node antes do Split In Batches:
- IF: Lista está vazia? ($json.pedidos.length === 0)
- True: Vai direto para Gera Relatório Final
- False: Vai para Split In Batches normal

**Código do IF**:
```javascript
// Condição: {{$json.pedidos.length === 0}}
```

---

### BUG #2: Branch de erro não conecta ao Telegram
**Severidade**: 🔴 CRÍTICA
**Localização**: Merge node (node-6)

**Problema**:
Quando a API retorna erro (branch false do IF), o fluxo vai para Log Erro mas não envia notificação ao cliente.

**Causa**:
Merge node está conectado mas depois não continua para Envia Telegram. Cliente fica sem resposta.

**Solução Proposta**:
Adicionar segundo IF após o Merge:
- IF: Houve erro? ($json.error === true)
- True: Envia mensagem de erro pelo Telegram
- False: Envia mensagem de sucesso pelo Telegram
- Ambas as saídas vão para Wait node

**Estrutura**:
```
[Log Erro] ──┐
             ├──▶ [Merge] ──▶ [IF: Houve erro?] ──┬── True ──▶ [Telegram Erro] ──┐
[Atualiza] ──┘                                  └── False ─▶ [Telegram Sucesso]─┤
                                                                                ▼
                                                                             [Wait]
```

---

## Recomendações
Aguardando n8n-builder implementar correções dos bugs #1 e #2.

## Próximos Passos
- [ ] n8n-builder: Adicionar IF antes de Split In Batches
- [ ] n8n-builder: Adicionar IF após Merge para tratar erro/sucesso
- [ ] n8n-tester: Retestar após correções
```

---

## FASE 4: n8n-builder (Correções)

### Implementação das Correções

```bash
# Adiciona IF node para lista vazia
python tools/n8n/nodes_create.py --type if --name "Lista Vazia?"
python tools/n8n/connections_create.py --from webhook --to "Lista Vazia?"
python tools/n8n/connections_create.py --from "Lista Vazia?" --to function --condition true
python tools/n8n/connections_create.py --from "Lista Vazia?" --to "split-in-batches" --condition false

# Adiciona IF node para erro/sucesso
python tools/n8n/nodes_create.py --type if --name "Houve Erro?"
# ... (conexões conforme proposta pelo tester)
```

---

## FASE 5: n8n-tester (Validação)

### Retestes

#### Teste 1: Lista Vazia (Novamente)
```bash
curl -X POST http://localhost:5678/webhook/pedidos/processar \
  -H "Content-Type: application/json" \
  -d '{"pedidos": []}'
```

**Resultado**: ✅ **CORRIGIDO** - Workflow vai direto para relatório final

#### Teste 2: API com Erro (Novamente)
```bash
curl -X POST http://localhost:5678/webhook/pedidos/processar \
  -d '{"pedidos": [{"id": "INVALIDO", ...}]}'
```

**Resultado**: ✅ **CORRIGIDO** - Cliente recebe notificação de erro

### Relatório Final

```markdown
# Relatório de Testes - Processador de Pedidos (v2)

## Status: ✅ APROVADO

## Testes Executados
- [x] Dados válidos (2 pedidos)
- [x] Lista vazia
- [x] Lista com 1 pedido
- [x] Lista com 10 pedidos
- [x] API retorna sucesso
- [x] API retorna erro
- [x] API timeout
- [x] Campos faltando

## Bugs Encontrados
Nenhum bug crítico. Todos os testes passaram.

## Observações Menores
- Workflow demora ~2s para processar 10 pedidos (aceitável)
- Tratamento de erro da API está robusto

## Conclusão
**WORKFLOW PRONTO PARA PRODUÇÃO** ✅

## Próximos Passos
- [ ] Deploy em ambiente de produção
- [ ] Monitorar primeiras execuções
```

---

## Resumo do Fluxo

```
User Request
      │
      ▼
┌─────────────────────────┐
│    n8n-architect        │  ← Projeta, especifica, documenta
│  (233 linhas de spec)   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│    n8n-builder          │  ← Implementa (scripts Python)
│  (Cria workflow n8n)    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│    n8n-tester           │  ← Testa, encontra bugs, propõe soluções
│  (2 bugs encontrados)   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│    n8n-builder          │  ← Corrige bugs
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│    n8n-tester           │  ← Valida correções
│  (Aprovado!)            │
└─────────────────────────┘
```

## Tempo Total Estimado
- Architect: 30 min (especificação detalhada)
- Builder: 45 min (implementação + correções)
- Tester: 30 min (testes + retestes)
- **Total**: ~2 horas para workflow completo, testado e funcional

---

**Este exemplo demonstra a importância da separação de responsabilidades e do ciclo iterativo entre os três agentes.**
