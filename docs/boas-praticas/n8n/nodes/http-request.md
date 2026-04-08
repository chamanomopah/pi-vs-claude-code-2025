# HTTP Request Node

Node para fazer chamadas HTTP a APIs externas.

## Configurações Básicas

### Method
- **GET**: Buscar dados
- **POST**: Criar recursos
- **PUT**: Atualizar recursos (completo)
- **PATCH**: Atualizar recursos (parcial)
- **DELETE**: Remover recursos

### URL
Pode ser estática ou dinâmica:

**Estática:**
```
https://api.example.com/users
```

**Dinâmica:**
```
https://api.example.com/users/{{ $json.userId }}
```

### Authentication

#### None
Para APIs públicas.

#### Header Auth
Adiciona cabeçalho customizado:
- **Name**: `Authorization`
- **Value**: `Bearer {{ $json.token }}`

#### Generic Credential Type
Para credenciais salvas no n8n:
- Select existing credential
- n8n gerencia automaticamente

## Headers

### Content-Type

**Para JSON:**
```
Content-Type: application/json
```

**Para Form Data:**
```
Content-Type: application/x-www-form-urlencoded
```

### Custom Headers
```
X-API-Key: {{ $json.apiKey }}
X-Request-ID: {{ $json.requestId }}
```

## Body

### JSON (application/json)

```json
{
  "name": "{{ $json.name }}",
  "email": "{{ $json.email }}",
  "age": {{ $json.age }}
}
```

### Form Data

```
name={{ $json.name }}&email={{ $json.email }}
```

## Query Parameters

### Via URL
```
https://api.example.com/users?limit={{ $json.limit }}&offset={{ $json.offset }}
```

### Via Query Parameters UI
- **Key**: `limit`
- **Value**: `{{ $json.limit }}`

## Tratamento de Resposta

### Response Format

- **JSON**: Parseia automaticamente para objeto
- **String**: Mantém como texto
- **File**: Para downloads

### Full Response vs Body

**Body (default):**
```javascript
// Apenas o corpo da resposta
{ "id": 1, "name": "John" }
```

**Full Response:**
```javascript
// Inclui headers, status, etc
{
  "statusCode": 200,
  "headers": { ... },
  "body": { "id": 1, "name": "John" }
}
```

## Retry on Fail

### Configuração
- **Retry on Fail**: true
- **Max Tries**: 3
- **Wait Between Tries**: 1000ms

### Quando Usar
- APIs com instabilidade temporária
- Rate limits que causam timeouts
- Conexões de rede instáveis

## Timeout

### Valor Recomendado
- **APIs rápidas**: 5000ms (5s)
- **APIs normais**: 10000ms (10s)
- **APIs lentas**: 30000ms (30s)

### Timeout vs Retry
```
Timeout: 5000ms
Retry on Fail: true (3 tentativas)
Tempo total: até 15s (5s × 3)
```

## Tratamento de Erros

### Verificar Status Code

```
[HTTP Request] → [IF: statusCode === 200?] ──true→ [Success]
                                      └─false→ [Handle Error]
```

### Capturar Error Response

**Full Response:**
```javascript
{{ $json.statusCode !== 200 ? $json.body : null }}
```

**Error Message:**
```javascript
{{ $json.error?.message || 'Unknown error' }}
```

## Padrões de Uso

### GET simples

```
[HTTP Request]
- Method: GET
- URL: https://api.example.com/users/{{ $json.userId }}
- Response Format: JSON
```

### POST com dados

```
[HTTP Request]
- Method: POST
- URL: https://api.example.com/users
- Headers: Content-Type: application/json
- Body: { "name": "{{ $json.name }}", "email": "{{ $json.email }}" }
```

### PUT para atualizar

```
[HTTP Request]
- Method: PUT
- URL: https://api.example.com/users/{{ $json.userId }}
- Body: { "name": "{{ $json.newName }}" }
```

### DELETE

```
[HTTP Request]
- Method: DELETE
- URL: https://api.example.com/users/{{ $json.userId }}
```

### Com autenticação Bearer

```
[HTTP Request]
- Method: GET
- URL: https://api.example.com/protected
- Authentication: Header Auth
  - Name: Authorization
  - Value: Bearer {{ $json.token }}
```

## Rate Limiting

### Respeitar Rate Limits

```
[HTTP Request] → [Wait: 1000ms] → [HTTP Request] → [Wait: 1000ms] → ...
```

### Detectar Rate Limit

```
[HTTP Request] → [IF: statusCode === 429?] ──true→ [Wait: 60000ms] → [Retry]
                                      └─false→ [Continue]
```

## Dicas de Segurança

### ✅ NUNCA exponha credenciais
```
❌ https://api.example.com?apiKey=hardcoded_key_123
✅ https://api.example.com?apiKey={{ $json.apiKey }}
```

### ✅ Use Generic Credentials
```
Armazene tokens no n8n, não no workflow
```

### ✅ Valide dados antes
```
[IF: isValid?] ──true→ [HTTP Request]
          └─false→ [Error]
```

## Anti-Padrões

### ❌ Timeout Muito Curto
```
Timeout: 500ms
```
**Problema:** Pode falhar com APIs normais

### ❌ Sem Retry
```
Retry on Fail: false
```
**Problema:** Qualquer falha interrompe o workflow

### ❌ Ignorar Erros
```
[HTTP Request] → [Next] (sem verificar statusCode)
```
**Problema:** Erros passam despercebidos

### ❌ Hardcoded Credentials
```
Headers: Authorization: Bearer abc123xyz
```
**Problema:** Credenciais expostas no workflow

## Checklist

- [ ] Method correto selecionado
- [ ] URL configurada (estática ou dinâmica)
- [ ] Headers necessários adicionados
- [ ] Body formatado corretamente
- [ ] Response format apropriado
- [ ] Timeout configurado
- [ ] Retry on Fail habilitado (se aplicável)
- [ ] Tratamento de erros implementado
- [ ] Rate limits respeitados
- [ ] Credenciais não estão hardcoded
