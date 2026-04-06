# Referência Rápida - Catálogo de Nodes

## Como Consultar o Catálogo

```bash
# Listar todos os nodes disponíveis
python catalogo_nodes.py

# Verificar se um node específico existe
python -c "from catalogo_nodes import resolve_node_type; print(resolve_node_type('webhook'))"

# Ver o connectionType de um node
python -c "from catalogo_nodes import get_connection_type; print(get_connection_type('agent'))"
```

## Nodes Principais Disponíveis

### Triggers (entrada)
- `webhook` - n8n-nodes-base.webhook [main]
- `scheduleTrigger` - n8n-nodes-base.scheduleTrigger [main]
- `errorTrigger` - n8n-nodes-base.errorTrigger [main]
- `telegramTrigger` - n8n-nodes-base.telegramTrigger [main]
- `chatTrigger` - @n8n/n8n-nodes-langchain.chatTrigger [chatTrigger]

### Processamento de Dados
- `set` - n8n-nodes-base.set [main]
- `code` - n8n-nodes-base.code [main]
- `function` - n8n-nodes-base.function [main]
- `if` - n8n-nodes-base.if [main_if]
- `switch` - n8n-nodes-base.switch [main]
- `filter` - n8n-nodes-base.filter [main]
- `merge` - n8n-nodes-base.merge [main]

### Loops e Iteração
- `splitInBatches` - n8n-nodes-base.splitInBatches [main_loop]
- `splitOut` - n8n-nodes-base.splitOut [main]

### HTTP e Web
- `httpRequest` - n8n-nodes-base.httpRequest [main]
- `wait` - n8n-nodes-base.wait [main]

### AI/LangChain
- `agent` - @n8n/n8n-nodes-langchain.agent [main]
- `chat` - @n8n/n8n-nodes-langchain.chat [main]
- `textClassifier` - @n8n/n8n-nodes-langchain.textClassifier [main]
- `lmChatGoogleGemini` - @n8n/n8n-nodes-langchain.lmChatGoogleGemini [ai_languageModel]
- `memoryPostgresChat` - @n8n/n8n-nodes-langchain.memoryPostgresChat [ai_memory]

### AI Tools (para Agent)
- `httpRequestTool` - n8n-nodes-base.httpRequestTool [ai_tool]
- `slackTool` - n8n-nodes-base.slackTool [ai_tool]
- `notionTool` - n8n-nodes-base.notionTool [ai_tool]
- `toolWorkflow` - @n8n/n8n-nodes-langchain.toolWorkflow [ai_tool]
- `agentTool` - @n8n/n8n-nodes-langchain.agentTool [ai_tool]

### Integrações
- `slack` - n8n-nodes-base.slack [main]
- `notion` - n8n-nodes-base.notion [main]
- `googleSheets` - n8n-nodes-base.googleSheets [main]
- `googleDrive` - n8n-nodes-base.googleDrive [main]
- `airtable` - n8n-nodes-base.airtable [main]
- `supabase` - n8n-nodes-base.supabase [main]
- `telegram` - n8n-nodes-base.telegram [main]

### Resposta Web
- `respondToWebhook` - n8n-nodes-base.respondToWebhook [main]

### Execução
- `executeWorkflow` - n8n-nodes-base.executeWorkflow [main]
- `executeCommand` - n8n-nodes-base.executeCommand [main]

## ConnectionTypes

### Tipos de Conexão
- `main` - Conexão padrão (main: [[]])
- `main_if` - IF node com 2 saídas (main: [[], []])
- `main_loop` - Loop com 2 saídas (main: [[], []])
- `ai_tool` - Ferramenta de AI (ai_tool: [[]])
- `ai_languageModel` - Modelo de linguagem (ai_languageModel: [[]])
- `ai_memory` - Memória de AI (ai_memory: [[]])
- `chatTrigger` - Trigger de chat (chatTrigger: [[]])

### Importância do ConnectionType
Ao conectar nodes, verifique se o connectionType é compatível:
- Nodes `main` podem se conectar com outros `main`
- AI Tools devem se conectar à porta `ai_tool` de um Agent
- AI Language Models devem se conectar à porta `ai_languageModel` de um Agent

## Nodes NÃO Disponíveis (Cuidado!)

⚠️ Estes nodes NÃO estão no catálogo (última verificação):
- `gmail` / `emailSend` - Envio de email
- `mattermost` - Chat Mattermost
- `discord` - Chat Discord
- `microsoftTeams` - Teams
- `openAi` - OpenAI direct (use Agent)

## Alternativas para Nodes Faltando

### Para Email
- Use `httpRequest` com SendGrid/Mailgun/Resend APIs
- Use `slackTool` via AI Agent para notificações
- Adicione o node ao catálogo (se houver SDK n8n disponível)

### Para OpenAI
- Use `agent` com modelo configurado
- Use `httpRequest` para API direta

## Como Adicionar Nodes ao Catálogo

Se precisar de um node que não está no catálogo:

1. **Verifique se o node existe no n8n**:
   ```bash
   # Pesquisar na documentação do n8n
   # https://docs.n8n.io/integrations/creating-integrations/
   ```

2. **Adicione a catalogo_nodes.py**:
   ```python
   "n8n-nodes-base.novoNode": {
       "type": "n8n-nodes-base.novoNode",
       "typeVersion": 1.0,
       "name": "Nome do Node",
       "parameters": {
           # parâmetros padrão
       },
       "connectionType": "main"
   }
   ```

3. **Teste**:
   ```bash
   python catalogo_nodes.py
   ```

## Padrões Comuns

### Webhook → Processamento → Resposta
```
webhook [main] → set [main] → code [main] → respondToWebhook [main]
```

### Agent AI com Tools
```
chatTrigger [chatTrigger] → agent [main]
                                ↓ [ai_tool]
                            slackTool [ai_tool]
                            httpRequestTool [ai_tool]
                            notionTool [ai_tool]
                                ↓ [ai_languageModel]
                            lmChatGoogleGemini [ai_languageModel]
                                ↓ [ai_memory]
                            memoryPostgresChat [ai_memory]
```

### Switch Multi-Branch
```
code [main] → switch [main]
                  ↓ [0]      ↓ [1]      ↓ [2]
              branch1      branch2    branch3
```

### Loop
```
splitInBatches [main_loop] → processamento [main]
                                     ↓ [loop]
                              splitInBatches [main_loop]
```
