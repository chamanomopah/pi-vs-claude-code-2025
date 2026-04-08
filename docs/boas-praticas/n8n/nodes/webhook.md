# Webhook Node

Node para receber requisições HTTP externas e iniciar workflows.

## Configurações Básicas

### HTTP Method

#### GET
Para buscar dados via URL parameters.
- Não tem body
- Dados via query string

#### POST
Para enviar dados no body.
- Mais comum para APIs
- Dados via JSON/Form

#### PUT
Para atualizar recursos.

#### DELETE
Para remover recursos.

### Path
Caminho único para o webhook.

**Exemplo:**
```
/webhook/lead-create
```

**URL completa:**
```
https://seu-n8n.com/webhook/lead-create
```

### Response Mode

#### On Received
Responde imediatamente (202 Accepted).
- Workflow continua em background
- Cliente não espera conclusão

#### Last Node
Responde após o último node executar.
- Cliente espera conclusão
- Pode demorar (timeout risk)

#### Response Webhook Node
Node específico para enviar resposta.
- Controle total sobre quando responder
- Pode responder no meio do workflow

## Authentication

#### None
Webhook público (não recomendado).

#### Header Auth
Requer cabeçalho customizado:
```
X-API-Key: sua-chave-secreta
```

#### Query Auth
Requer query parameter:
```
https://seu-n8n.com/webhook/lead-create?token=seu-token
```

## Binário vs JSON

### Binary Data
Para uploads de arquivos.
- `Content-Type: multipart/form-data`
- Arquivo disponível em `$binary`

### JSON
Para dados estruturados.
- `Content-Type: application/json`
- Dados disponíveis em `$json`

## Response Options

### Response Code

#### 200 OK
Sucesso padrão.

#### 201 Created
Recurso criado com sucesso.

#### 400 Bad Request
Requisição inválida.

#### 401 Unauthorized
Autenticação necessária.

#### 403 Forbidden
Sem permissão.

#### 404 Not Found
Recurso não encontrado.

#### 500 Server Error
Erro interno.

### Response Headers
```
Access-Control-Allow-Origin: *
Content-Type: application/json
```

### Response Body
```json
{
  "success": true,
  "message": "Workflow iniciado com sucesso",
  "data": {
    "workflowId": "123",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## Padrões de Uso

### Padrão 1: Webhook Simples

```
[Webhook] → [Process] → [Database]
```

**Webhook Node:**
- Method: POST
- Path: lead-create
- Response Mode: Last Node

### Padrão 2: Webhook com Resposta Imediata

```
[Webhook: Response On Received] → [Process Long Running]
```

**Webhook Node:**
- Response Mode: On Received
- Responde 202 imediatamente
- Workflow continua em background

### Padrão 3: Webhook com Resposta Customizada

```
[Webhook] → [Process] → [Webhook Response] → [Database]
```

**Webhook Node:**
- Response Mode: Response Webhook Node

**Webhook Response Node:**
- Respond with: 'Response Body'
- Response Code: 200
- Response Body:
```json
{
  "status": "success",
  "leadId": "{{ $json.id }}"
}
```

### Padrão 4: Webhook com Validação

```
[Webhook] → [IF: Valid?] ──true→ [Process] → [Webhook Response: 200]
                      └─false→ [Webhook Response: 400]
```

**Node IF:**
- Condição: `{{ $json.email && $json.name }}`

**Webhook Response (200):**
```json
{
  "success": true,
  "message": "Lead criado"
}
```

**Webhook Response (400):**
```json
{
  "success": false,
  "error": "Email e nome são obrigatórios"
}
```

## CORS

### Habilitar CORS
Se o webhook será chamado de frontend:

**Webhook Node → Options → Response Headers:**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

### OPTIONS Request
Navegadores enviam OPTIONS antes de POST.

**Tratar OPTIONS:**
```
[Webhook] → [IF: Method === OPTIONS?] ──true→ [Respond: 204]
                              └─false→ [Process]
```

## Rate Limiting

### Padrão com Rate Limit

```
[Webhook] → [Check Rate Limit] → [IF: Allowed?] ──true→ [Process]
                                              └─false→ [Respond: 429]
```

**Node Check Rate Limit:**
- Database query ou Redis
- Verifica se excedeu limite

**Webhook Response (429):**
```json
{
  "error": "Too many requests",
  "retryAfter": 60
}
```

## Webhook Retry

### Cliente Deve Retry

```
[Webhook] → [Process] → [IF: Success?] ──true→ [Respond: 200]
                                      └─false→ [Respond: 500]
```

**Cliente (cURL):**
```bash
curl --retry 3 --retry-delay 1000 https://seu-n8n.com/webhook/endpoint
```

## Dados de Entrada

### Acessar Body

**JSON:**
```javascript
{{ $json.name }}
{{ $json.email }}
```

**Form Data:**
```javascript
{{ $json.body.name }}
{{ $json.body.email }}
```

### Acessar Headers

```javascript
{{ $json.headers['x-api-key'] }}
{{ $json.headers['content-type'] }}
```

### Acessar Query Parameters

```javascript
{{ $json.query.token }}
{{ $json.query.source }}
```

### Acessar IP

```javascript
// IPv4
{{ $json.ip }}

// Com proxy
{{ $json.headers['x-forwarded-for'] }}
```

## Segurança

### ✅ Use Authentication
```
Header Auth: X-API-Key
Query Auth: token
```

### ✅ Valide Entrada
```
[Webhook] → [IF: Valid?] ──true→ [Process]
                      └─false→ [Respond: 400]
```

### ✅ Rate Limiting
```
Limite requisições por IP ou API key
```

### ✅ HTTPS Sempre
```
Use HTTPS em produção
```

### ✅ Sanitize Input
```
[Webhook] → [Sanitize] → [Validate] → [Process]
```

## Anti-Padrões

### ❌ Sem Autenticação
```
Authentication: None
```
**Problema:** Qualquer um pode disparar o workflow

### ❌ Response Mode: Last Node com Processamento Longo
```
[Webhook: Last Node] → [Process: 5 minutos]
```
**Problema:** Cliente timeout antes de receber resposta

### ❌ Sem Validação
```
[Webhook] → [Process] (sem validar entrada)
```
**Problema:** Dados inválidos quebram o workflow

### ❌ Sem Tratamento de Erro
```
[Webhook] → [Process] (pode falhar)
```
**Problema:** Cliente não sabe o que aconteceu

## Debug

### Ver Incoming Request

```
[Webhook] → [Function: Log] → [Process]
```

**Function Node:**
```javascript
console.log('Headers:', JSON.stringify($json.headers, null, 2));
console.log('Body:', JSON.stringify($json.body, null, 2));
console.log('Query:', JSON.stringify($json.query, null, 2));
return [{ json: $json }];
```

### Testar Webhook

**cURL:**
```bash
curl -X POST https://seu-n8n.com/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'
```

**Browser Console:**
```javascript
fetch('https://seu-n8n.com/webhook/test', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'John', email: 'john@example.com' })
})
.then(r => r.json())
.then(console.log)
```

## Checklist

- [ ] HTTP Method correto
- [ ] Path único e descritivo
- [ ] Response Mode apropriado
- [ ] Autenticação configurada
- [ ] Validação de entrada
- [ ] Tratamento de erros
- [ ] CORS habilitado (se necessário)
- [ ] Rate limiting (recomendado)
- [ ] Response code correto
- [ ] HTTPS em produção
