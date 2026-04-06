# Exemplo de Plano Declarativo: Simple Lead Router Demo

## Prompt Original

"Create an n8n workflow called 'Simple Lead Router Demo' that starts with a Webhook receiving JSON with these exact fields:
fullName (string), email (string), company (string), country (string), budget (number), timeframeDays (number), and message (string).

Normalize the fields (trim strings, lowercase email, cast budget and timeframeDays to numbers) and compute lane using these rules in order:

set lane="Invalid" if email does not contain "@" OR fullName is empty;
else set lane="HighPriority" if budget > 5000 AND timeframeDays <= 30;
else set lane="Partner" if message contains (case-insensitive) any of: "sponsor", "partnership", "affiliate", "collab";
else set lane="Standard".

Then use a Switch node on lane with 4 separate branches that do not merge back.

Invalid branch: add Gmail label lead_invalid, send a short email asking them to resubmit with missing details, and append a row to Google Sheets tab invalid_leads.

HighPriority branch: compute priorityScore (0–100) as min(100, 50 + (budget > 10000 ? 25 : 0) + (timeframeDays <= 14 ? 25 : 0)), send Slack to #leads-high-priority including name, company, score, budget, timeframe, and message, send an email with a Calendly booking link placeholder, and append a row to Google Sheets tab high_priority_leads including priorityScore.

Partner branch: create a Notion page in a database "Partnership Requests" with the lead details, send Slack to #partnerships with the message text, and append a row to Google Sheets tab partner_leads.

Standard branch: run a small "industry guess" step using a simple keyword check on message
if it contains "real estate" set segment="RealEstate"
if it contains "law" or "attorney" set segment="Legal"
else segment="General"

then do a mini Switch on segment to post to different Slack channels (#leads-real-estate, #leads-legal, or #leads-general), send a standard thank-you email, and append a row to Google Sheets tab standard_leads including segment.

Each branch ends independently."

---

## Plano de Workflow: Simple Lead Router Demo

## Resumo
Workflow de roteamento de leads que classifica entradas por prioridade e tipo, roteando para diferentes processamentos paralelos que não convergem.

## Trigger
**Webhook** (n8n-nodes-base.webhook) - Recebe JSON com dados do lead via POST

## Campos de Entrada
| Campo | Tipo | Descrição |
|-------|------|----------|
| fullName | string | Nome completo do lead |
| email | string | Email (requer @ para validação) |
| company | string | Nome da empresa |
| country | string | País |
| budget | number | Orçamento disponível |
| timeframeDays | number | Prazo em dias |
| message | string | Mensagem/observações |

## Fluxo Principal

### 1. Normalização (Set node)
- `{{ $json.fullName.trim() }}` → fullName
- `{{ $json.email.toLowerCase().trim() }}` → email
- `{{ Number($json.budget) }}` → budget
- `{{ Number($json.timeframeDays) }}` → timeframeDays
- Manter company, country, message como estão

### 2. Classificação (Code node)
Compute `lane` using these rules in order:
```javascript
const email = $json.email;
const fullName = $json.fullName;
const budget = $json.budget;
const timeframeDays = $json.timeframeDays;
const message = $json.message.toLowerCase();

let lane = "Standard";

// Rule 1: Invalid
if (!email.includes('@') || !fullName || fullName.trim() === '') {
  lane = "Invalid";
}
// Rule 2: HighPriority
else if (budget > 5000 && timeframeDays <= 30) {
  lane = "HighPriority";
}
// Rule 3: Partner
else if (message.includes('sponsor') || message.includes('partnership') ||
         message.includes('affiliate') || message.includes('collab')) {
  lane = "Partner";
}
// Rule 4: Standard (default)

return { ...$json, lane };
```

### 3. Roteamento Principal (Switch node)
Use a Switch node on `lane` with **4 separate branches that do not merge back**.

---

## Branches do Switch

### Branch: Invalid
**Nodes necessários:**
1. **Gmail** (n8n-nodes-base.gmail) - Adicionar label `lead_invalid`
2. **Send Email** (n8n-nodes-base.emailSend) - Enviar email pedindo reenvio
3. **Google Sheets** (n8n-nodes-base.googleSheets) - Append row à tab `invalid_leads`

**Fluxo:** Webhook → Set → Code → Switch[Invalid] → Gmail → Email → Sheets

### Branch: HighPriority
**Nodes necessários:**
1. **Code** (n8n-nodes-base.code) - Computar priorityScore
2. **Slack** (n8n-nodes-base.slack) - Postar em #leads-high-priority
3. **Send Email** (n8n-nodes-base.emailSend) - Enviar Calendly link
4. **Google Sheets** (n8n-nodes-base.googleSheets) - Append row à tab `high_priority_leads`

**Computação de priorityScore:**
```javascript
const budget = $json.budget;
const timeframeDays = $json.timeframeDays;
const score = Math.min(100, 50 + (budget > 10000 ? 25 : 0) + (timeframeDays <= 14 ? 25 : 0));
return { ...$json, priorityScore: score };
```

**Fluxo:** Webhook → Set → Code → Switch[HighPriority] → Code(score) → Slack → Email → Sheets

### Branch: Partner
**Nodes necessários:**
1. **Notion** (n8n-nodes-base.notion) - Criar página em database "Partnership Requests"
2. **Slack** (n8n-nodes-base.slack) - Postar em #partnerships
3. **Google Sheets** (n8n-nodes-base.googleSheets) - Append row à tab `partner_leads`

**Fluxo:** Webhook → Set → Code → Switch[Partner] → Notion → Slack → Sheets

### Branch: Standard
**Nodes necessários:**
1. **Code** (n8n-nodes-base.code) - Industry guess (segment detection)
2. **Switch** (n8n-nodes-base.switch) - Mini switch por segment
3. **Slack** (n8n-nodes-base.slack) - 3 instâncias para canais diferentes
4. **Send Email** (n8n-nodes-base.emailSend) - Email padrão de agradecimento
5. **Google Sheets** (n8n-nodes-base.googleSheets) - Append row à tab `standard_leads`

**Computação de segment:**
```javascript
const message = $json.message.toLowerCase();
let segment = "General";

if (message.includes('real estate')) {
  segment = "RealEstate";
} else if (message.includes('law') || message.includes('attorney')) {
  segment = "Legal";
}

return { ...$json, segment };
```

**Mini Switch por segment:**
- Output 1: segment == "RealEstate" → Slack #leads-real-estate
- Output 2: segment == "Legal" → Slack #leads-legal
- Output 3: segment == "General" → Slack #leads-general

**Fluxo:** Webhook → Set → Code(lane) → Switch[Standard] → Code(segment) → Switch(segment) → Slack → Email → Sheets

---

## Nodes Necessários (Consolidado)

| Nome | Tipo (catálogo) | ConnectionType | Propósito |
|------|----------------|----------------|-----------|
| Webhook | n8n-nodes-base.webhook | main | Receber leads |
| Normalize | n8n-nodes-base.set | main | Normalizar campos |
| Classify | n8n-nodes-base.code | main | Computar lane |
| Main Switch | n8n-nodes-base.switch | main | Rotear por lane |
| Invalid-Gmail | n8n-nodes-base.gmail | main | Label invalid |
| Invalid-Email | n8n-nodes-base.emailSend | main | Pedir reenvio |
| Invalid-Sheets | n8n-nodes-base.googleSheets | main | Log invalid |
| Priority-Score | n8n-nodes-base.code | main | Computar score |
| Priority-Slack | n8n-nodes-base.slack | main | Notificar alta prioridade |
| Priority-Email | n8n-nodes-base.emailSend | main | Enviar Calendly |
| Priority-Sheets | n8n-nodes-base.googleSheets | main | Log high priority |
| Partner-Notion | n8n-nodes-base.notion | main | Criar página |
| Partner-Slack | n8n-nodes-base.slack | main | Notificar parceria |
| Partner-Sheets | n8n-nodes-base.googleSheets | main | Log partner |
| Standard-Segment | n8n-nodes-base.code | main | Detectar segmento |
| Segment-Switch | n8n-nodes-base.switch | main | Rotear por segment |
| Std-RE-Slack | n8n-nodes-base.slack | main | #leads-real-estate |
| Std-Legal-Slack | n8n-nodes-base.slack | main | #leads-legal |
| Std-General-Slack | n8n-nodes-base.slack | main | #leads-general |
| Std-Email | n8n-nodes-base.emailSend | main | Agradecimento |
| Std-Sheets | n8n-nodes-base.googleSheets | main | Log standard |

**Total: 24 nodes**

## Conexões Principais
| Origem | Destino | Tipo | Saída |
|--------|---------|------|-------|
| Webhook | Normalize | main | [0] → [0] |
| Normalize | Classify | main | [0] → [0] |
| Classify | Main Switch | main | [0] → [0] |
| Main Switch | Invalid-Branch | main | [0] → [0] (Invalid) |
| Main Switch | Priority-Branch | main | [1] → [0] (HighPriority) |
| Main Switch | Partner-Branch | main | [2] → [0] (Partner) |
| Main Switch | Standard-Branch | main | [3] → [0] (Standard) |

## Parâmetros Principais

### Webhook
- `path`: "lead-router"
- `httpMethod`: "POST"
- `responseMode`: "responseNode"

### Main Switch (4 outputs)
- Output 0: `lane == "Invalid"`
- Output 1: `lane == "HighPriority"`
- Output 2: `lane == "Partner"`
- Output 3: `lane == "Standard"`

### Segment Switch (3 outputs)
- Output 0: `segment == "RealEstate"`
- Output 1: `segment == "Legal"`
- Output 2: `segment == "General"`

### Google Sheets (todas as instâncias)
- `operation`: "append"
- `sheetName`: (ver branch específico)

### Slack (HighPriority)
- `channel`: "#leads-high-priority"
- `text`: `New high priority lead!\nName: {{$json.fullName}}\nCompany: {{$json.company}}\nScore: {{$json.priorityScore}}/100\nBudget: {{$json.budget}}\nTimeframe: {{$json.timeframeDays}} days\nMessage: {{$json.message}}`

## Considerações Especiais

### Credenciais Necessárias
- Gmail (para labels e envio)
- Slack (3 canais diferentes)
- Google Sheets (spreadsheet com 4 tabs)
- Notion (database "Partnership Requests")

### Tabs do Google Sheets
Antes de executar, criar:
- `invalid_leads`
- `high_priority_leads`
- `partner_leads`
- `standard_leads`

### Limitações
- Switch principal não converge (4 branches independentes)
- Branch Standard tem sub-switch também sem convergência
- Cada branch termina em Sheets (log final)

### Pontos de Atenção
- Validar que todos os nodes existem em catalogo_nodes.py (⚠️ `gmail` e `emailSend` podem não estar no catálogo)
- Verificar se `Notion` node está disponível
- Verificar se `Slack` node está disponível

## Nota de Implementação

⚠️ **ALGUNS NODES PODEM NÃO ESTAR NO CATÁLOGO**

Verificar em `catalogo_nodes.py`:
- `n8n-nodes-base.gmail` - Pode precisar ser adicionado
- `n8n-nodes-base.emailSend` - Pode precisar ser adicionado
- `n8n-nodes-base.notion` - ✅ Disponível (linha 422)
- `n8n-nodes-base.slack` - ✅ Disponível (linha 415)
- `n8n-nodes-base.googleSheets` - ✅ Disponível (linha 405)

Se nodes de email não estiverem disponíveis, pode usar:
- `n8n-nodes-base.httpRequest` para SendGrid/Mailgun API
- Adicionar nodes ao catálogo primeiro
