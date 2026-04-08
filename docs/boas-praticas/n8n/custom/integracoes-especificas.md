# Integrações Específicas

Documentação de integrações específicas do projeto.

## Integração: API do Meu Sistema

### Endpoint: Criar Lead
- **URL**: `https://api.meusistema.com.br/v1/leads`
- **Method**: POST
- **Auth**: Bearer Token
- **Rate Limit**: 100 req/min
- **Timeout**: 10000ms

### Request Body
```json
{
  "nome": "string",
  "email": "string",
  "telefone": "string",
  "origem": "string",
  "interesses": ["string"]
}
```

### Response Success (201)
```json
{
  "id": "uuid",
  "createdAt": "ISO-8601",
  "status": "created"
}
```

### Response Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email inválido",
    "fields": ["email"]
  }
}
```

### Padrão de Retry
- Max tries: 3
- Wait between: 2000ms
- Backoff: Exponential

## Integração: HubSpot

### Credencial
- Name: `HubSpot Production`
- Type: OAuth2

### Criar Contato
- **Endpoint**: CRM → Contacts → Create
- **Campos Mapeados**:
  - `email` → `email`
  - `firstname` → `nome`
  - `phone` → `telefone`

### Buscar Contato por Email
- **Endpoint**: CRM → Contacts → Search
- **Filter**: `email equals "{{ $json.email }}"`

## Integração: Telegram

### Credencial
- Name: `Telegram Bot`
- Bot Token: `{CREDENTIAL}`

### Enviar Mensagem
- **Chat ID**: `{CREDENTIAL}` (grupo ou canal)
- **Text**: `{{ $json.message }}`
- **Parse Mode**: Markdown

### Formatação de Mensagem
```javascript
**Título**
📊 *Métrica*: {{ $json.value }}
📅 *Data*: {{ $json.date }}
```

## Integração: Google Sheets

### Credencial
- Name: `Google Sheets Service Account`

### Append Row
- **Spreadsheet ID**: `{CREDENTIAL}`
- **Sheet Name**: `leads`
- **Range**: `A:Z`
- **Values**: `{{ $json.rowData }}`

### Estrutura de Linha
```javascript
[
  $json.id,
  $json.nome,
  $json.email,
  $json.createdAt,
  $json.status
]
```

## Integração: Notion

### Credencial
- Name: `Notion Integration`

### Criar Página em Database
- **Database ID**: `{CREDENTIAL}`
- **Properties**:
  - `Name`: Title → `{{ $json.nome }}`
  - `Email`: Email → `{{ $json.email }}`
  - `Status`: Select → `{{ $json.status }}`
  - `Created`: Date → `{{ $json.createdAt }}`

## Integração: Slack

### Credencial
- Name: `Slack Bot`

### Enviar Mensagem
- **Channel**: `#leads`
- **Text**: `{{ $json.message }}`

### Formatação de Block Kit
```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Novo Lead*\n{{ $json.nome }}"
      }
    }
  ]
}
```

## Padrões de Integração

### Padrão: Criar e Sincronizar

```
[Source] → [API Externa: Create] → [My System: Create] → [Merge]
```

### Padrão: Buscar e Enriquecer

```
[Source] → [HubSpot: Search] → [My System: Get] → [Merge: Enriched]
```

### Padrão: webhook → Process → Multiple Integrations

```
[Webhook] → [Split] → main[1] ──┬─▶ [HubSpot] ──┐
                           ├─▶ [Slack] ────┤
                           └─▶ [Sheets] ────┴─▶ [Merge Wait]
```

## Tratamento de Erros Específicos

### HubSpot: Rate Limit
```javascript
// Status Code 429
// Retry-After header
{{ $json.headers['retry-after'] || 60 }}
```

### API Meu Sistema: Validação
```javascript
// Error Code: VALIDATION_ERROR
// Log fields com erro
{{ $json.error.fields.join(', ') }}
```

## Timeout por Integração

| Integração | Timeout | Max Tries |
|------------|---------|-----------|
| API Meu Sistema | 10000ms | 3 |
| HubSpot | 5000ms | 3 |
| Google Sheets | 30000ms | 5 |
| Notion | 10000ms | 3 |
| Slack | 5000ms | 2 |
| Telegram | 5000ms | 2 |

## Mapeamento de Campos

### HubSpot ↔ Meu Sistema

| HubSpot | Meu Sistema |
|---------|-------------|
| email | email |
| firstname | primeiro_nome |
| lastname | ultimo_nome |
| phone | telefone |
| company | empresa |

### Google Sheets ↔ Meu Sistema

| Sheets | Meu Sistema |
|--------|-------------|
| A | id |
| B | nome |
| C | email |
| D | telefone |
| E | created_at |

## Códigos de Erro Personalizados

### API Meu Sistema
- `LEAD_EXISTS`: Lead já existe (atualizar ao invés de criar)
- `INVALID_EMAIL`: Email inválido
- `DUPLICATE_LEAD`: Lead duplicado detected

### HubSpot
- `CONTACT_EXISTS`: Contato já existe
- `INVALID_EMAIL`: Email inválido (HubSpot validation)

## Exemplos de Workflows

### Workflow 1: Webhook para HubSpot

```
[Webhook: lead-create] → 
[Validate] → 
[IF: Valid?] ──true→ [HubSpot: Create Contact] → [My System: Create Lead] → [Response: 200]
            └─false→ [Response: 400]
```

### Workflow 2: Sync Bidirecional

```
[Schedule: Daily] → 
[My System: Get Leads] → 
[Split In Batches] → 
main[1] → [HubSpot: Search] → 
[IF: Exists?] ──true→ [HubSpot: Update]
            └─false→ [HubSpot: Create] →
[Wait] → volta
main[0] → [Log Summary]
```

## Notas Importantes

### ⚠️ Rate Limiting
- Sempre respeite rate limits de cada API
- Use Wait nodes entre requisições se necessário
- Implemente backoff exponencial em retries

### ⚠️ Campos Obrigatórios
- API Meu Sistema requer `email` e `nome`
- HubSpot requer `email` (único)
- Google Sheets requer todas as colunas preenchidas

### ⚠️ Ordem de Integração
- Criar em API Meu Sistema PRIMEIRO (fonte de verdade)
- Depois sync com HubSpot/Sheets
- Evita duplicatas e inconsistências

## Contato

Para dúvidas sobre integrações:
- API Meu Sistema: api@meusistema.com.br
- HubSpot: Suporte HubSpot
- n8n: #n8n-help no Slack interno
