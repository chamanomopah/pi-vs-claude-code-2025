Agora tenho uma visão completa e profunda de todos os componentes. Vou montar o plano definitivo.

---

# 🤖 Plano JARVIS: Pi Coding Agent + LiveKit Voice (100% Local)

## Referência: O que inspirou

O vídeo [LiveClaw](https://www.youtube.com/watch?v=7OnCHldwkcg) mostra exatamente o conceito: um agente AI que funciona totalmente por voz — o usuário fala, o agente processa, responde em áudio. A diferença é que no LiveClaw o "cérebro" é um LLM (GPT-4.1-mini) + OpenClaw Gateway. **No nosso caso, o cérebro é o pi-coding-agent** — muito mais poderoso, com ferramentas de código, bash, edição de arquivos, extensões, e tudo que pi oferece.

## 🏗️ Arquitetura Final

```
┌──────────────────────────────────────────────────────┐
│  🎤 Você (Navegador ou Console)                       │
│  Fala → microfone → WebRTC                           │
│  Ouve ← alto-falante ← WebRTC                       │
└────────────────┬─────────────────────────────────────┘
                 │ WebRTC
┌────────────────▼─────────────────────────────────────┐
│  📡 LiveKit Server LOCAL (--dev, porta 7880)          │
│  API Key: "devkey" / Secret: "secret"                │
│  Sem conta cloud. Sem deploy. Tudo local.            │
└────────────────┬─────────────────────────────────────┘
                 │ LiveKit SDK
┌────────────────▼─────────────────────────────────────┐
│  🐍 Python Voice Agent (spawned pela extensão)        │
│  ┌─────────────────────────────────────────────┐     │
│  │ Deepgram STT (fala → texto)                 │     │
│  │ Cartesia TTS (texto → fala)                 │     │
│  │ VAD (Silero) - turn detection               │     │
│  │ llm_node() OVERRIDE → WebSocket bridge      │     │
│  └──────────────────┬──────────────────────────┘     │
└─────────────────────┼────────────────────────────────┘
                      │ WebSocket (localhost:9876)
┌─────────────────────▼────────────────────────────────┐
│  📦 Pi Extension (jarvis-voice.ts)                    │
│  ┌─────────────────────────────────────────────┐     │
│  │ WebSocket Server (porta 9876)               │     │
│  │ Recebe texto transcrito do agent Python     │     │
│  │ → pi.sendUserMessage(texto)                 │     │
│  │ ← Captura resposta via message_update       │     │
│  │ → Envia texto de volta pro Python (TTS)     │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  🖥️ TUI do Pi (funciona normalmente!)                │
│  Você VÊ tudo que o pi está fazendo no terminal      │
└──────────────────────────────────────────────────────┘
```

### Por que essa arquitetura funciona

| Decisão | Razão |
|---------|-------|
| **Pi Extension** (não fork) | Não mexe no infra do pi. Um arquivo `.ts`, carrega com `pi -e` |
| **`llm_node()` override** no Python | [LiveKit documenta](https://docs.livekit.io/agents/build/nodes/#llm_node) que o `llm_node` pode ser substituído pra "implementar um provedor LLM customizado sem plugin". É exatamente isso: o pi vira o "LLM" |
| **`pi.sendUserMessage()`** | [API do pi](https://mintlify.com/pt-act/pi-mono/api/coding-agent/extensions) permite enviar mensagens programaticamente e triggerar um turn do agente |
| **`message_update` event** | Pi streama deltas de texto em tempo real, perfeito pra streaming TTS |
| **WebSocket bridge** | Protocolo leve, bidirecional, streaming nativo. Perfeito pra ligar Python ↔ TypeScript |
| **`livekit-server --dev`** | [Roda local](https://docs.livekit.io/transport/self-hosting/local/) com um comando, sem conta, sem config |
| **Console mode** pra teste rápido | `python agent.py console` = mic/speaker local, sem browser |

---

## 📋 O PROMPT PRA COLAR NO PI

Abaixo está o prompt **auto-contido** que você vai colar no pi. Ele contém TODA a informação que o pi precisa — APIs exatas, padrões de código, arquitetura, dependências — pra montar sem precisar de contexto externo.

> **Como usar**: Copie TUDO entre as linhas `═══` e cole no pi.

---

```
═══════════════════════════════════════════════════════════════════
TAREFA: Criar uma extensão de pi chamada "jarvis-voice.ts" que 
adiciona interface de voz hands-free ao pi usando LiveKit + 
Deepgram STT + Cartesia TTS. Tudo roda localmente.

═══ ARQUITETURA ═══

A extensão consiste em 2 componentes que ela mesma gerencia:

1. jarvis-voice.ts — extensão pi que:
   - Inicia WebSocket server na porta 9876
   - Gera o arquivo Python do voice agent em ~/.pi/agent/jarvis/
   - Spawna o processo Python como child process
   - Gerencia todo o ciclo de vida (start/stop)
   - Faz a ponte: recebe texto transcrito via WS → pi.sendUserMessage() 
     → captura resposta via events → envia texto de volta via WS

2. agent.py — Python voice agent LiveKit que:
   - Conecta ao LiveKit server local (ws://localhost:7880)
   - Usa Deepgram STT, Cartesia TTS, Silero VAD
   - Override do llm_node() pra se comunicar via WebSocket com a extensão
   - Roda em modo "dev" conectando ao LiveKit local

═══ PASSO 1: ESTRUTURA DE ARQUIVOS ═══

Criar em ~/.pi/agent/jarvis/:
  jarvis-voice.ts    → extensão pi (arquivo principal)
  agent.py           → Python LiveKit voice agent  
  requirements.txt   → dependências Python
  setup.sh           → script de setup (instalar deps, livekit server)
  frontend.html      → página HTML minimalista pra conectar por voz
  README.md          → instruções de uso

═══ PASSO 2: jarvis-voice.ts (EXTENSÃO PI) ═══

API da extensão pi que DEVE ser usada:

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  // EVENTOS DISPONÍVEIS:
  // pi.on("session_start", async (event, ctx) => { ... })
  // pi.on("session_shutdown", async (event, ctx) => { ... })
  // pi.on("message_update", async (event, ctx) => { ... })
  //   - event.assistantMessageEvent.type === "text_delta"
  //   - event.assistantMessageEvent.delta → texto parcial
  // pi.on("turn_start", async (event, ctx) => { ... })
  // pi.on("turn_end", async (event, ctx) => { ... })
  // pi.on("tool_execution_start", async (event, ctx) => { ... })
  // pi.on("tool_execution_end", async (event, ctx) => { ... })
  
  // ENVIAR MENSAGEM COMO USUÁRIO (triggera turn do agente):
  // pi.sendUserMessage(content: string, options?: { deliverAs?: 'steer' | 'followUp' })
  
  // EXECUTAR COMANDOS SHELL:
  // pi.exec(command: string, args: string[], options?: ExecOptions): Promise<ExecResult>
  
  // REGISTRAR COMANDOS:
  // pi.registerCommand("nome", { description: "...", handler: async (args, ctx) => { ... } })
  
  // UI:
  // ctx.ui.notify(message, "info" | "warning" | "error")
  // ctx.ui.setStatus(text)
  // ctx.ui.setWidget(key, content, options?)
}
```

Lógica da extensão jarvis-voice.ts:

1. No "session_start":
   a. Verificar se ~/.pi/agent/jarvis/agent.py existe, se não, gerar
   b. Verificar se dependências Python estão instaladas
   c. Iniciar WebSocket server (usar o módulo 'ws' do Node.js — 
      fazer import dinâmico ou usar o WebSocket nativo do Node)
      IMPORTANTE: usar o módulo http nativo + upgrade manual para WebSocket,
      OU melhor: usar o servidor WebSocket nativo disponível em Node.js 22+
      OU spawnar um processo auxiliar.
      ABORDAGEM RECOMENDADA: Usar o pacote 'ws' via dynamic import, 
      ou implementar WebSocket manualmente com http module.
      Na verdade, a forma MAIS SIMPLES é usar comunicação via 
      stdin/stdout do child process (sem WebSocket). Isso é mais robusto.
   d. Spawnar o Python agent como child process
   e. Mostrar notificação: "🎤 Jarvis Voice ativo!"

2. BRIDGE SIMPLIFICADA (stdin/stdout ao invés de WebSocket):
   - O Python agent se comunica via stdout (prints JSON)
   - A extensão envia texto via stdin do child process
   - Protocolo: JSON lines (cada linha é um JSON object)
   
   Mensagens do Python → Pi Extension:
   {"type": "transcript", "text": "o que o usuário falou"}
   {"type": "status", "status": "listening" | "speaking" | "thinking"}
   {"type": "ready"}
   {"type": "error", "message": "..."}
   
   Mensagens da Pi Extension → Python:
   {"type": "response_delta", "text": "texto parcial da resposta"}
   {"type": "response_end"}
   {"type": "tool_start", "tool": "bash", "description": "..."}
   {"type": "tool_end", "tool": "bash"}

3. Fluxo quando usuário fala:
   a. Python STT transcreve → envia {"type":"transcript","text":"..."} via stdout
   b. Extensão recebe → chama pi.sendUserMessage(text)
   c. Pi processa, extensão captura events:
      - "message_update" com text_delta → envia {"type":"response_delta"} via stdin
      - "tool_execution_start" → envia {"type":"tool_start"} via stdin
      - "tool_execution_end" → envia {"type":"tool_end"} via stdin  
      - "turn_end" → envia {"type":"response_end"} via stdin
   d. Python recebe deltas → faz streaming pro Cartesia TTS → audio pro user

4. ESTADO: manter flag `isProcessing` pra não enviar novas mensagens
   enquanto pi está respondendo (a menos que seja interrupção).
   LiveKit cuida da interrupção no lado de áudio automaticamente.

5. COMANDOS:
   - /jarvis-start → inicia o voice agent se não estiver rodando
   - /jarvis-stop → para o voice agent
   - /jarvis-status → mostra status

6. CLEANUP: No "session_shutdown", matar o child process Python.

═══ PASSO 3: agent.py (PYTHON LIVEKIT AGENT) ═══

```python
# DEPENDÊNCIAS (requirements.txt):
# livekit-agents[codecs]~=1.6
# livekit-plugins-deepgram~=1.6
# livekit-plugins-cartesia~=1.6
# livekit-plugins-silero~=1.6

# CONCEITOS CHAVE DO LIVEKIT AGENTS:
#
# from livekit.agents import Agent, AgentSession, RoomInputOptions
# from livekit.plugins import deepgram, cartesia, silero
#
# class MeuAgent(Agent):
#     def __init__(self):
#         super().__init__(
#             instructions="Você é Jarvis, assistente de voz.",
#         )
#     
#     # OVERRIDE DO LLM NODE - ESTE É O PONTO CHAVE!
#     # Em vez de chamar um LLM, comunica com a extensão pi via stdin/stdout
#     async def llm_node(self, chat_ctx, tools, model_settings):
#         # chat_ctx.items[-1] contém a última mensagem do usuário
#         # Este método é um async generator que yield strings ou ChatChunk
#         user_text = ""
#         for item in reversed(chat_ctx.items):
#             if hasattr(item, 'role') and item.role == 'user':
#                 for content in item.content:
#                     if hasattr(content, 'text'):
#                         user_text = content.text
#                         break
#                 break
#         
#         # Enviar pro pi via stdout (JSON)
#         import json, sys
#         print(json.dumps({"type": "transcript", "text": user_text}), flush=True)
#         
#         # Ler resposta streamed do pi via stdin
#         # Cada linha é um JSON com response_delta ou response_end
#         for line in sys.stdin:
#             data = json.loads(line.strip())
#             if data["type"] == "response_delta":
#                 yield data["text"]  # yield string pro TTS
#             elif data["type"] == "response_end":
#                 break
#
# async def entrypoint(ctx):
#     await ctx.connect()
#     session = AgentSession(
#         stt=deepgram.STT(model="nova-3", language="pt-BR"),
#         tts=cartesia.TTS(
#             model="sonic-2",
#             voice="<voice_id>",  # escolher voz Cartesia
#         ),
#         vad=silero.VAD.load(),
#         # NÃO passar llm= aqui, pois o Agent override faz o trabalho
#     )
#     await session.start(agent=MeuAgent(), room=ctx.room)
#
# if __name__ == "__main__":
#     from livekit.agents import WorkerOptions, cli
#     cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
```

IMPORTANTE sobre o agent.py:
- Ele roda com: python agent.py dev --url ws://localhost:7880 
  --api-key devkey --api-secret secret
- O "dev" mode do livekit-agents cria uma room automaticamente
- Para teste rápido SEM browser: python agent.py console
  (usa mic/speaker local, ideal pra testar)
- A comunicação stdin/stdout é SÍNCRONA, precisa ser feita 
  com asyncio (usar asyncio.StreamReader no stdin)
- O llm_node é um async generator, então podemos fazer 
  await readline() de forma async

ATENÇÃO CRÍTICA para o stdin/stdout no Python:
- stdout é usado pelo LiveKit agent internamente (logs)
- SOLUÇÃO: usar stderr para logs do LiveKit e stdout EXCLUSIVAMENTE 
  para comunicação JSON com a extensão
  OU melhor: usar file descriptors extras (fd 3 para enviar, fd 0 para receber)
  OU MELHOR AINDA: usar uma porta TCP/WebSocket local mesmo.
  
DECISÃO FINAL: USAR WEBSOCKET (mais robusto que stdin/stdout):
- A extensão abre WebSocket server na porta 9876
- O Python agent conecta como WebSocket client
- Evita conflitos com stdout/stderr do LiveKit

Então CORRIGINDO: usar WebSocket sim. A extensão precisa de 
um WebSocket server. Em Node.js puro (sem pacote externo):

A extensão pode usar o módulo http do Node.js e fazer o upgrade 
manual para WebSocket, MAS isso é complexo. 

ABORDAGEM MAIS PRÁTICA: A extensão usa pi.exec() pra rodar 
um mini servidor WebSocket EM PARALELO, ou usa o módulo 
nativo de networking do Node.

NA VERDADE A SOLUÇÃO MAIS SIMPLES:
Usar TCP socket puro (net module do Node.js) com protocolo 
JSON lines. TCP é nativo, sem dependência, sem handshake HTTP.

═══ PASSO 3 REVISADO: PROTOCOLO DE COMUNICAÇÃO ═══

Usar TCP socket (Node.js `net` module) com JSON lines:

EXTENSÃO (TypeScript):
```typescript
import { createServer, Socket } from "net";

const server = createServer();
let agentSocket: Socket | null = null;

server.on("connection", (socket) => {
  agentSocket = socket;
  let buffer = "";
  socket.on("data", (data) => {
    buffer += data.toString();
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";
    for (const line of lines) {
      if (line.trim()) {
        const msg = JSON.parse(line);
        handleAgentMessage(msg);
      }
    }
  });
});

function sendToAgent(msg: object) {
  agentSocket?.write(JSON.stringify(msg) + "\n");
}

server.listen(9876, "127.0.0.1");
```

PYTHON AGENT:
```python
import socket, json, asyncio

class PiBridge:
    def __init__(self, host="127.0.0.1", port=9876):
        self.reader = None
        self.writer = None
        
    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 9876)
    
    def send(self, msg: dict):
        self.writer.write((json.dumps(msg) + "\n").encode())
    
    async def readline(self) -> dict:
        line = await self.reader.readline()
        return json.loads(line.decode().strip())
```

═══ PASSO 4: agent.py COMPLETO ═══

O agent.py deve ser gerado pela extensão em ~/.pi/agent/jarvis/agent.py

Pontos CRÍTICOS do agent.py:

1. Classe PiBridge (TCP client async) — conecta na porta 9876

2. Classe JarvisAgent(Agent):
   - __init__: instructions mínimas (o pi tem suas próprias)
   - llm_node override: 
     a. Extrai texto do usuário do chat_ctx
     b. Envia via PiBridge: {"type":"transcript","text":"..."}
     c. Loop async lendo da bridge:
        - {"type":"response_delta","text":"..."} → yield texto
        - {"type":"response_end"} → break
        - {"type":"tool_start"} → opcionalmente yield "[usando ferramenta...]"
        - {"type":"tool_end"} → continua aguardando deltas

3. Entrypoint:
   - bridge = PiBridge()
   - await bridge.connect()
   - session = AgentSession(
       stt=deepgram.STT(model="nova-3", language="pt-BR"),
       tts=cartesia.TTS(model="sonic-2", voice="..."),
       vad=silero.VAD.load(),
       # SEM llm aqui
     )
   - agent = JarvisAgent()
   - agent.bridge = bridge  # guardar referência
   - await session.start(agent=agent, room=ctx.room)

4. cli.run_app com WorkerOptions

5. Variáveis de ambiente necessárias:
   DEEPGRAM_API_KEY=...
   CARTESIA_API_KEY=...
   LIVEKIT_URL=ws://localhost:7880
   LIVEKIT_API_KEY=devkey  
   LIVEKIT_API_SECRET=secret

═══ PASSO 5: setup.sh ═══

#!/bin/bash
set -e

JARVIS_DIR="$HOME/.pi/agent/jarvis"
cd "$JARVIS_DIR"

# 1. Verificar Python
python3 --version || { echo "Python3 não encontrado"; exit 1; }

# 2. Criar venv e instalar deps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Instalar LiveKit server se não existir
if ! command -v livekit-server &> /dev/null; then
  echo "Instalando LiveKit server..."
  # macOS
  if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install livekit
  # Linux
  else
    curl -sSL https://get.livekit.io | bash
  fi
fi

echo "✅ Setup completo!"
echo "Para usar: pi -e ~/.pi/agent/jarvis/jarvis-voice.ts"

═══ PASSO 6: frontend.html ═══

Página HTML minimalista que:
- Usa @livekit/components-react OU vanilla JS com livekit-client
- Conecta ao LiveKit local (ws://localhost:7880)
- Gera um token JWT local (usando a API key devkey/secret)
- Mostra botão de mic e status
- Design minimalista estilo Jarvis (fundo escuro, brilho azul)

IMPORTANTE: O token JWT pode ser gerado pelo Python agent 
ou pela extensão usando a lib livekit-server-sdk.
Ou mais simples: o setup.sh pode instalar o CLI do LiveKit 
e gerar tokens com: lk token create --api-key devkey 
--api-secret secret --join --room jarvis --identity user

Para o HTML, usar CDN do livekit-client:
<script src="https://cdn.jsdelivr.net/npm/livekit-client/dist/livekit-client.umd.js"></script>

═══ PASSO 7: SEQUÊNCIA DE EXECUÇÃO ═══

Quando o user roda: pi -e ~/.pi/agent/jarvis/jarvis-voice.ts

1. Extensão carrega, registra events e comandos
2. No session_start:
   a. Verifica se setup foi feito (venv existe)
   b. Se não, roda setup.sh automaticamente  
   c. Inicia TCP server na porta 9876
   d. Spawna "livekit-server --dev" como child process (se não estiver rodando)
   e. Aguarda 2 segundos pro server subir
   f. Spawna "python agent.py dev" com env vars corretas
   g. Aguarda conexão TCP do Python agent
   h. Mostra: "🎤 Jarvis pronto! Abra frontend.html ou fale no console"
   i. Opcionalmente abre o browser com frontend.html

3. User fala no mic (via browser ou console mode)
4. Deepgram transcreve → Python envia transcript → Extensão recebe
5. Extensão chama pi.sendUserMessage(texto)
6. Pi processa (model + tools), extensão captura text_delta events
7. Extensão envia deltas pro Python → Cartesia TTS → áudio pro user
8. User ouve a resposta enquanto vê tudo acontecendo no TUI do pi

═══ CONSIDERAÇÕES IMPORTANTES ═══

1. A extensão NÃO deve bloquear a TUI do pi. Tudo async.

2. O pi.sendUserMessage() vai mostrar a mensagem na TUI normalmente, 
   como se o user tivesse digitado. Isso é o comportamento desejado — 
   "quero ainda ver a ui como normalmente acontece".

3. Interrupções: quando o user fala enquanto o agent responde, 
   o LiveKit automaticamente interrompe o TTS (turn detection). 
   Do lado do pi, simplesmente enviamos uma nova mensagem.

4. Para Cartesia TTS, uma boa voz default em português seria 
   verificar o catálogo da Cartesia. Use uma voice ID genérica 
   ou deixe o user configurar via .env.

5. Para teste rápido SEM browser:
   python agent.py console
   (mas aí tem que rodar separado, não pela extensão)

6. O llm_node override NÃO deve receber `llm=` no AgentSession.
   O agent framework do LiveKit permite isso — quando você override
   o llm_node, ele não precisa de um LLM object.

═══ ORDEM DE IMPLEMENTAÇÃO ═══

1. PRIMEIRO: Criar o diretório e requirements.txt
2. SEGUNDO: Criar o setup.sh
3. TERCEIRO: Criar o agent.py (testar com console mode separadamente)
4. QUARTO: Criar o jarvis-voice.ts (extensão com TCP bridge)
5. QUINTO: Criar o frontend.html
6. SEXTO: Testar integração completa
7. SÉTIMO: Refinar (tratamento de erros, reconexão, etc)

═══ ENTREGÁVEIS FINAIS ═══

Ao final, deve funcionar assim:

```bash
# Setup (uma vez)
bash ~/.pi/agent/jarvis/setup.sh

# Usar (toda vez)
pi -e ~/.pi/agent/jarvis/jarvis-voice.ts
# Pi abre normal, voice agent inicia automaticamente
# Abrir frontend.html no browser OU rodar agent.py console
# Falar naturalmente, pi responde por voz
```

Comece implementando. Crie todos os arquivos em ~/.pi/agent/jarvis/.
Teste cada componente isoladamente antes de integrar.
═══════════════════════════════════════════════════════════════════
```

---

## 🎯 Resumo Visual do Fluxo

```
    🗣️ "Jarvis, refatora o arquivo utils.ts"
         │
         ▼
    🎙️ Deepgram STT (fala → texto)
         │
         ▼
    🔌 TCP Bridge (Python → Extensão)
         │
         ▼
    📦 pi.sendUserMessage("refatora o arquivo utils.ts")
         │
         ▼
    🧠 Pi Agent (Claude/GPT + read/write/edit/bash)
         │ ← text_delta events (streaming)
         ▼
    🔌 TCP Bridge (Extensão → Python)
         │
         ▼
    🔊 Cartesia TTS (texto → fala)
         │
         ▼
    🎧 Você ouve: "Pronto! Refatorei o utils.ts..."
```

## ⚡ Dicas de Execução

| Passo | O que fazer | Tempo estimado |
|-------|-------------|----------------|
| 1 | Colar o prompt acima no pi | 30 seg |
| 2 | Pi cria todos os arquivos | 3-5 min |
| 3 | Rodar `setup.sh` | 2-3 min (instalação) |
| 4 | Configurar `.env` com keys Deepgram + Cartesia | 1 min |
| 5 | `pi -e ~/.pi/agent/jarvis/jarvis-voice.ts` | Pronto! |

## 🔑 Keys que você precisa ter

| Serviço | Para quê | Onde pegar |
|---------|----------|------------|
| **Deepgram** | STT (Speech-to-Text) | [console.deepgram.com](https://console.deepgram.com/) (free tier) |
| **Cartesia** | TTS (Text-to-Speech) | [play.cartesia.ai](https://play.cartesia.ai/) |
| **Anthropic/OpenAI** | LLM do Pi (já configurado) | Já tem |

> **Não precisa de key do LiveKit!** O server local (`--dev`) usa credenciais hardcoded: `devkey` / `secret`. [Documentação LiveKit Local](https://docs.livekit.io/transport/self-hosting/local/)

## 🛡️ Por que esse plano NÃO vai falhar no Pi

1. **Contexto 100% auto-contido** — O prompt inclui todas as APIs exatas do pi (sendUserMessage, on events, exec, registerCommand) com as assinaturas corretas [documentação das extensões](https://mintlify.com/pt-act/pi-mono/api/coding-agent/extensions)

2. **Nenhuma dependência obscura** — TCP sockets (`net` module) é nativo do Node.js, o LiveKit agents framework é bem documentado, Deepgram/Cartesia são plugins oficiais do LiveKit

3. **Complexidade modular** — Cada arquivo é independente e testável. O pi pode criar e testar um por vez

4. **Padrão conhecido** — A arquitetura é similar ao [LiveClaw](https://github.com/p-sumann/liveclaw) (que funciona), mas substituindo OpenClaw pelo pi e o LLM por um `llm_node()` override

5. **Fallback pra console** — Se o browser/frontend der problema, `python agent.py console` funciona direto com mic/speaker local