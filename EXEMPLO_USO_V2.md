# Exemplo Prático v2: Uso do Sistema de Boas Práticas em Pastas

## Cenário

Usuário solicita: *"Preciso de um workflow que processe uma lista de leads, valide cada um com múltiplas APIs em paralelo e envie Telegram para os que forem válidos."*

---

## Fluxo de Trabalho com a Nova Estrutura

### Passo 1: Arquiteto Carrega Boas Práticas

```
Usuário: Preciso de um workflow que processe leads...

Arquiteto: /n8n-load-boas-praticas

[Skill escaneia recursivamente docs/boas-praticas/n8n/]

✓ Encontrados 13 arquivos .md
✓ Core: 4 arquivos
✓ Patterns: 3 arquivos
✓ Nodes: 3 arquivos
✓ Custom: 2 arquivos

✓ Conteúdo carregado e organizado
```

### Passo 2: Arquiteto Consulta Arquivos Específicos

```
Arquiteto: /n8n-load-boas-praticas branches-paralelos

[Lê docs/boas-praticas/n8n/patterns/branches-paralelos.md]

✓ Padrão de branches paralelos carregado
✓ Sincronização com Merge Wait documentada
✓ Combinação de dados explicada

Arquiteto: /n8n-load-boas-praticas webhook

[Lê docs/boas-praticas/n8n/nodes/webhook.md]

✓ Webhook node documentado
✓ Response modes explicados
✅ Validação de entrada detalhada
```

### Passo 3: Arquiteto Projeta o Workflow

```
Arquiteto: Vou projetar usando os padrões:

1. Webhook para receber leads (nodes/webhook.md)
2. Validação de entrada (nodes/if-switch.md)
3. Verificação de lista vazia (core/split-in-batches.md)
4. Split In Batches para processar cada lead
5. Branches paralelas para múltiplas APIs (patterns/branches-paralelos.md)
6. Merge Wait para sincronizar (core/merge-nodes.md)
7. IF para validar resultados (nodes/if-switch.md)
8. Telegram para leads válidos (custom/integracoes-especificas.md)

Referenciando:
- docs/boas-praticas/n8n/patterns/branches-paralelos.md
- docs/boas-praticas/n8n/nodes/webhook.md
- docs/boas-praticas/n8n/core/merge-nodes.md
```

### Passo 4: Especificação Detalhada

```yaml
Workflow: Multi-Validation Lead Processor

Node 1: Webhook Receiver
  Tipo: Webhook
  Path: leads/validate-batch
  Method: POST
  Response Mode: Response Webhook Node
  Conecta a: Node 2
  Padrão aplicado: Webhook com validação (docs/boas-praticas/n8n/nodes/webhook.md)

Node 2: IF: Array Vazio?
  Tipo: IF
  Condição: {{ Array.isArray($json.leads) && $json.leads.length > 0 }}
  True → Node 4
  False → Node 3
  Padrão aplicado: Verificação de lista vazia (core/split-in-batches.md)

Node 3: Webhook Response: Empty
  Tipo: Webhook Response
  Response Code: 200
  Body: { "success": true, "message": "No leads to process", "processed": 0 }

Node 4: Split In Batches
  Tipo: Split In Batches
  Batch Size: 1
  Reset: false
  main[0] → Node 15 (Generate Summary)
  main[1] → Node 5
  Padrão aplicado: Loop Simples (patterns/loop-simples.md)
  NOTA: main[0] só executa quando loop termina

Node 5: Parallel Validation Start
  Conecta a:
    - Node 6 (HubSpot Validation)
    - Node 7 (Salesforce Validation)
    - Node 8 (Clearbit Validation)
  Padrão aplicado: Branches Paralelos (patterns/branches-paralelos.md)

Node 6: HubSpot: Validate Email
  Tipo: HTTP Request
  Method: GET
  URL: https://api.hubapi.com/contacts/v1/search/email?q={{ $json.email }}
  Authentication: Bearer Token
  Conecta a: Node 11 (Merge)
  Padrão aplicado: HTTP Request (nodes/http-request.md)

Node 7: Salesforce: Validate Lead
  Tipo: HTTP Request
  Method: GET
  URL: https://api.salesforce.com/lead/query/{{ $json.email }}
  Authentication: OAuth2
  Conecta a: Node 11 (Merge)

Node 8: Clearbit: Enrich Data
  Tipo: HTTP Request
  Method: GET
  URL: https://api.clearbit.com/v1/people/email/{{ $json.email }}
  Authentication: Bearer Token
  Conecta a: Node 11 (Merge)

Node 11: Merge: Wait for All
  Tipo: Merge
  Mode: Wait
  Aguarda: Nodes 6, 7, 8
  Conecta a: Node 12
  Padrão aplicado: Merge Wait (core/merge-nodes.md)
  NOTA: AMBAS as entradas devem estar conectadas

Node 12: Function: Combine Results
  Tipo: Function
  Combina dados das 3 APIs
  Determina se lead é válido
  Conecta a: Node 13

Node 13: IF: Lead Valid?
  Tipo: IF
  Condição: {{ $json.isValid === true }}
  True → Node 14
  False → Node 14 (mas com flag invalid)
  Padrão aplicado: IF node (nodes/if-switch.md)

Node 14: Accumulate Result
  Tipo: Function ou Database
  Acumula resultado para relatório final
  Conecta a: Node 15 (via Loop) ou Node 16

Node 15: Wait: Sync Before Next
  Tipo: Wait
  Time: 100ms
  Conecta a: Node 4 (volta ao Split In Batches)
  Padrão aplicado: Sincronização de loop (core/loops.md)

Node 16: Generate Summary
  Tipo: Function
  Processa dados acumulados
  Gera relatório final
  Conecta a: Node 17
  Entrada: main[0] do Split In Batches

Node 17: Webhook Response: Success
  Tipo: Webhook Response
  Response Code: 200
  Body:
  {
    "success": true,
    "processed": {{ $json.total }},
    "valid": {{ $json.validCount }},
    "invalid": {{ $json.invalidCount }}
  }
```

### Passo 5: Validação de Boas Práticas

```
✓ Todo Split In Batches tem main[0] e main[1] conectados
  Referência: core/split-in-batches.md

✓ Merge Wait tem todas as entradas conectadas
  Referência: core/merge-nodes.md

✓ Branches paralelas sincronizadas corretamente
  Referência: patterns/branches-paralelos.md

✓ Wait node usado antes de voltar ao loop
  Referência: core/loops.md

✓ Lista vazia tratada antes do Split
  Referência: core/split-in-batches.md

✓ Campos de entrada/saída documentados
  Referência: core/fluxo-dados.md

✓ HTTP requests com retry configurado
  Referência: nodes/http-request.md

✓ Webhook com validação e response customizada
  Referência: nodes/webhook.md

✓ IF nodes com ambas as branches conectadas
  Referência: nodes/if-switch.md

Checklist validado conforme:
- docs/boas-praticas/n8n/core/
- docs/boas-praticas/n8n/patterns/
- docs/boas-praticas/n8n/nodes/
```

---

## Diferença Principal

### Antes (Arquivo Único)

```
System prompt carrega docs/n8n-boas-praticas.md
↓
Arquivo gigante com tudo misturado
↓
Difícil de encontrar um padrão específico
↓
Sem organização por categoria
```

### Depois (Pastas Organizadas)

```
System prompt escaneia docs/boas-praticas/n8n/ recursivamente
↓
13 arquivos especializados organizados por categoria
↓
Fácil de encontrar:
  - /n8n-load-boas-praticas branches-paralelos
  - /n8n-load-boas-praticas webhook
  - /n8n-load-boas-praticas split-in-batches
↓
Referências específicas: "patterns/branches-paralelos.md seção 5"
```

---

## Exemplo de Adicionar Novo Arquivo

### Cenário: Preciso documentar um novo padrão

```bash
# 1. Criar o arquivo
vim docs/boas-praticas/n8n/patterns/loop-com-retry.md

# 2. Adicionar conteúdo seguindo o template
# 3. Salvar

# 4. Disponível IMEDIATAMENTE!
/n8n-load-boas-praticas loop-com-retry

[Arquivo é carregado automaticamente]
```

### Template Rápido

```markdown
# Loop com Retry

## Quando Usar
- APIs instáveis
- Conexões de rede problemáticas

## Estrutura
```
[Split] → main[1] → [Try] → [IF: Success?] ──true→ [Log] → [Merge]
                           └─false→ [IF: Retry < 3?] ──true→ [Wait] → [Retry]
                                                          └─false→ [Log Error]
```

## Implementação
Detalhes...

## Exemplo Prático
Workflow XYZ

## Validações
- ✅ Limite de tentativas configurado
- ✅ Wait entre tentativas
- ✅ Log de todas as tentativas

## Erros Comuns
### ❌ Sem Limite de Retry
Loop infinito!

## Checklist
- [ ] Max retry configurado
- [ ] Wait entre tentativas
- [ ] Log de erros
```

---

## Benefícios Imediatos

### Para o Arquiteto

1. **Carregamento Sob Demanda**
   - Carrega apenas o necessário
   - Mais rápido e eficiente

2. **Referências Precisas**
   - "Conforme patterns/branches-paralelos.md seção 7"
   - Link direto para o arquivo

3. **Fácil Expansão**
   - Novo padrão? Criar arquivo .md
   - Disponível imediatamente

4. **Organização Intuitiva**
   - Core para conceitos
   - Patterns para arquitetura
   - Nodes para documentação
   - Custom para personalizações

### Para o Time

1. **Colaboração**
   - Múltiplos devs podem editar
   - Sem conflitos em arquivo gigante

2. **Versionamento**
   - Git history por arquivo
   - Fácil de ver mudanças

3. **Onboarding**
   - Novos devs aprendem gradualmente
   - Leem um arquivo por vez

4. **Manutenção*
