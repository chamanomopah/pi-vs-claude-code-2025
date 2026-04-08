# Minhas Convenções

Convenções específicas do meu projeto/team.

## Nomenclatura de Workflows

### Padrão de Nome
```
[Modulo] [Ação] [Entidade]
```

**Exemplos:**
- `Sales Create Lead`
- `Marketing Update Subscriber`
- `Support Process Ticket`

## Nomenclatura de Nodes

### Padrão
```
[Ação] [Entidade]
```

**Exemplos:**
- `Validate Email`
- `Create Contact HubSpot`
- `Send Notification Telegram`

## Estrutura de Pastas

### Por Módulo
```
workflows/
├── sales/
│   ├── create-lead.json
│   └── update-opportunity.json
├── marketing/
│   └── send-campaign.json
└── support/
    └── process-ticket.json
```

## Convenções de Dados

### Campos Obrigatórios
Todo workflow deve ter:
- `id`: Identificador único
- `createdAt`: Timestamp de criação
- `source`: Origem dos dados

### Campos Padrão
```javascript
{
  "id": "uuid",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601",
  "source": "webhook|api|manual",
  "status": "pending|processing|completed|failed"
}
```

## Convenções de Erro

### Estrutura de Erro
```javascript
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Descrição legível",
    "details": { ... },
    "timestamp": "ISO-8601"
  }
}
```

### Códigos de Erro Padrão
- `VALIDATION_ERROR`: Dados inválidos
- `API_ERROR`: Erro em API externa
- `TIMEOUT`: Timeout de operação
- `NOT_FOUND`: Recurso não encontrado
- `PERMISSION_DENIED`: Sem permissão

## Convenções de Logging

### Níveis de Log
- `ERROR`: Erros que interrompem o workflow
- `WARN`: Alertas que não interrompem
- `INFO`: Informações gerais
- `DEBUG`: Detalhes de debug

### Estrutura de Log
```javascript
{
  "level": "INFO|WARN|ERROR",
  "workflow": "nome-do-workflow",
  "node": "nome-do-node",
  "message": "descrição",
  "data": { ... },
  "timestamp": "ISO-8601"
}
```

## Convenções de Integração

### Retry Padrão
- **Max Tries**: 3
- **Wait Between**: 1000ms
- **Backoff**: Exponential (1s, 2s, 4s)

### Timeout Padrão
- **APIs rápidas**: 5000ms
- **APIs normais**: 10000ms
- **APIs lentas**: 30000ms

### Rate Limit Padrão
- **APIs externas**: 1 req/s
- **APIs próprias**: 10 req/s

## Convenções de Documentação

### Todo Workflow Deve Ter
1. **Propósito**: O que o workflow faz
2. **Trigger**: Como é iniciado
3. **Entrada**: Estrutura dos dados de entrada
4. **Saída**: Estrutura dos dados de saída
5. **Dependências**: APIs e serviços externos
6. **Exemplo de uso**: Caso de uso típico

### Template de Documentação
```markdown
# Nome do Workflow

## Propósito
Breve descrição do que o workflow faz.

## Trigger
- Tipo: Webhook/Manual/Schedule
- Endpoint: /webhook/path

## Entrada
\`\`\`json
{
  "campo1": "tipo",
  "campo2": "tipo"
}
\`\`\`

## Saída
\`\`\`json
{
  "result": "tipo"
}
\`\`\`

## Dependências
- API X: https://api.example.com
- Serviço Y: credencial Z

## Exemplo de Uso
\`\`\`bash
curl -X POST https://n8n.example.com/webhook/path \
  -d '{"campo1":"valor1"}'
\`\`\`
```

## Convenções de Versionamento

### Versionamento de Workflows
- Use git para versionar workflows exportados
- Nome de arquivo: `nome-do-workflow-v1.0.0.json`
- Changelog em `CHANGELOG.md`

### Versionamento de APIs
- Sempre especifique a versão da API
- Ex: `https://api.example.com/v1/endpoint`

## Convenções de Testes

### Teste Manual
1. Teste com dados válidos
2. Teste com dados inválidos
3. Teste com lista vazia
4. Teste com erro de API
5. Teste com timeout

### Teste de Carga
- Teste com 10 itens
- Teste com 100 itens
- Teste com 1000 itens

## Convenções de Segurança

### Credenciais
- Usar Generic Credentials sempre
- Nunca hardcoded no workflow
- Rotacionar a cada 90 dias

### Dados Sensíveis
- Não logar dados sensíveis
- Usar criptografia quando necessário
- Maskar campos sensíveis em logs

## Convenções de Monitoramento

### Métricas a Monitorar
- Tempo de execução
- Taxa de sucesso/falha
- Volume de processamento
- Erros mais comuns

### Alertas
- Workflow falhando > 5 min
- Taxa de erro > 10%
- Timeout > 30s
