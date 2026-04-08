# Exemplo Prático: Uso do Novo Arquiteto N8N

## Cenário

Usuário solicita: *"Preciso de um workflow que processe uma lista de pedidos, valide cada um com uma API externa e envie um Telegram para o cliente."*

---

## Fluxo de Trabalho com o Novo Sistema

### Passo 1: Arquiteto Carrega Boas Práticas

```
Usuário: Preciso de um workflow que processe pedidos...

Arquiteto: /n8n-load-boas-praticas loops

[Skill carrega docs/n8n-boas-praticas.md]

✓ Boas práticas de Split In Batches carregadas
✓ Padrões de loop identificados
✓ Anti-padrões conhecidos
```

### Passo 2: Arquiteto Projeta o Workflow

```
Arquiteto: Vou projetar seguindo as boas práticas:

1. Verificação de lista vazia (padrão "Lista Vazia")
2. Split In Batches com:
   - main[0] → resumo final
   - main[1] → processamento individual
3. Loop com reconexão (padrão "Loop Simples")
4. IF node para tratar erros da API

Conforme docs/n8n-boas-praticas.md seções 1, 3 e 5.
```

### Passo 3: Especificação Detalhada

```yaml
Workflow: Processador de Pedidos

Node 1: Webhook Trigger
  Tipo: Webhook
  Conecta a: Node 2

Node 2: IF: Lista Vazia?
  Tipo: IF
  Condição: {{ $json.pedidos.length === 0 }}
  True → Node 10 (Resumo Vazio)
  False → Node 3 (Split In Batches)
  Padrão aplicado: Verificação de lista vazia (boas práticas seção 5.4)

Node 3: Split In Batches
  Tipo: Split In Batches
  Batch Size: 1
  main[0] → Node 9 (Gera Resumo)
  main[1] → Node 4 (Valida API)
  Padrão aplicado: Loop Simples (boas práticas seção 5.1)
  NOTA: main[0] só executa quando loop termina

Node 4: Valida API
  Tipo: HTTP Request
  Conecta a: Node 5

Node 5: IF: Sucesso?
  Tipo: IF
  Condição: {{ $json.valid === true }}
  True → Node 6 (Envia Telegram)
  False → Node 7 (Log Erro)
  Padrão aplicado: Tratamento de erro (boas práticas seção 5.2)

Node 6: Envia Telegram
  Tipo: Telegram
  Conecta a: Node 8

Node 7: Log Erro
  Tipo: Google Sheets (append)
  Conecta a: Node 8

Node 8: Wait
  Tipo: Wait
  Time: 100ms
  Conecta a: Node 3 (volta ao Split In Batches)
  Padrão aplicado: Sincronização de loop (boas práticas seção 1)

Node 9: Gera Resumo
  Tipo: Function
  Conecta a: Node 10

Node 10: Webhook Response
  Tipo: Webhook Response
```

### Passo 4: Validação de Boas Práticas

```
✓ Todo Split In Batches tem main[0] e main[1] conectados
✓ Todo loop reconecta para o Split In Batches
✓ Lista vazia é tratada antes do Split In Batches
✓ Não há loops infinitos (main[0] só executa quando termina)
✓ Campos de entrada/saída documentados
✓ Padrões aplicados referenceados

Checklist validado conforme docs/n8n-boas-praticas.md
```

---

## Diferença Principal

### Antes (Boas Práticas Embutidas)

```
System prompt tinha ~200 linhas de boas práticas
↓
Difícil de encontrar um padrão específico
↓
Difícil de atualizar (precisa editar o agente)
↓
System prompt inchado
```

### Depois (Boas Práticas Externalizadas)

```
System prompt limpo
↓
/n8n-load-boas-praticas loops
↓
Carrega apenas o necessário
↓
Referenceia seção específica: "seção 5.1 - Loop Simples"
↓
Fácil de expandir (adicionar ao docs/n8n-boas-praticas.md)
```

---

## Exemplo de Expansão

### Adicionar Nova Boa Prática

```bash
# 1. Editar o documento
vim docs/n8n-boas-praticas.md

# 2. Adicionar nova seção
## 7. Padrão: Loop com Retry

### Descrição
Loop que tenta N vezes antes de falhar...

### Quando Usar
- APIs que podem falhar temporariamente
- Operações de rede instáveis

### Exemplo
[Exemplo visual]

### Anti-Padrão
❌ ERRADO: Tentar infinitamente
✅ CERTO: Limitar a N tentativas
```

### Usar a Nova Boa Prática

```
Arquiteto: /n8n-load-boas-praticas retry

[A nova seção está disponível imediatamente!]

Arquiteto: Vou usar o padrão "Loop com Retry" (seção 7)...
```

---

## Conclusão

**Benefícios imediatos:**
- ✅ System prompt mais limpo
- ✅ Boas práticas fáceis de encontrar
- ✅ Fácil de expandir
- ✅ Reference específico por seção
- ✅ Reutilizável por outros agentes

**Arquiteto agora:**
1. Carrega boas práticas no início
2. Aplica padrões documentados
3. Reference seções específicas
4. Valida conforme checklist

