Agora tenho uma compreensão profunda de todos os componentes. Deixa eu montar o plano completo.

---

# 🤖 Projeto JARVIS: Pi Coding Agent + LiveKit Voice — Plano Completo

## A Inspiração: [LiveClaw](https://www.youtube.com/watch?v=7OnCHldwkcg)

O vídeo mostra exatamente o conceito que você quer — um voice agent (LiveKit) que delega o "cérebro" para um agent externo (naquele caso o OpenClaw, no seu caso o **pi-coding-agent**). O cara fala, o agent pesquisa, e responde por voz. A diferença é que você quer algo **muito mais poderoso**: em vez de um gateway de mensagens, você quer o **pi-coding-agent completo** — com `bash`, `edit`, `write`, `read`, `grep`, `find`, `ls` — um Jarvis que **realmente programa e executa código** pela sua voz.

[Source: LiveClaw GitHub](https://github.com/p-sumann/liveclaw)

---

## 🏗️ Arquitetura Final

```
Você (Microfone/Browser)
        ↕ WebRTC (turn detection, interrupções, streaming)
LiveKit Server (LOCAL - porta 7880)
        ↕
LiveKit Agent (Python)
    ├── 🎙️ VAD: Silero (100% local, sem API)
    ├── 🗣️ STT: Deepgram Plugin (sua API key direto)
    ├── 🧠 "LLM": Custom llm_node → Pi RPC (subprocess stdin/stdout)
    └── 🔊 TTS: Cartesia Plugin (sua API key direto)
        
        O llm_node NÃO chama nenhuma LLM diretamente.
        Ele faz bridge com pi-coding-agent via --mode rpc.
        
Pi Coding Agent (Node.js subprocess)
    ├── Agent Loop (pi-agent-core)
    ├── Tools: bash, read, write, edit, grep, find, ls
    ├── LLM: Anthropic/OpenAI/Google (a escolha do pi)
    └── Session Management (JSONL)
```

### Como funciona a ponte:

1. **Você fala** → WebRTC → LiveKit Server
2. **Deepgram STT** transcreve sua fala em texto  
3. O **custom `llm_node`** pega o texto e envia para o **pi subprocess** via `{"type": "prompt", "message": "texto"}`
4. **Pi processa** — pode chamar tools (bash, edit, etc.), pensar, pesquisar
5. Pi emite **`text_delta` events** conforme gera a resposta
6. O `llm_node` **streama esses deltas** de volta para o pipeline LiveKit
7. **Cartesia TTS** converte o texto em fala em tempo real
8. **Você ouve** a resposta via WebRTC

### A peça-chave: `--mode rpc` do Pi

O pi-coding-agent tem um modo RPC completo ([documentação oficial](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md)) que permite:
- Enviar prompts via JSON stdin
- Receber eventos streaming via JSON stdout  
- Abortar operações
- Gerenciar sessões
- Tudo via protocolo JSONL

**Exemplo Python oficial do próprio repo do pi:**
```python
import subprocess, json

proc = subprocess.Popen(
    ["pi", "--mode", "rpc", "--no-session"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)

def send(cmd):
    proc.stdin.write(json.dumps(cmd) + "\n")
    proc.stdin.flush()

send({"type": "prompt", "message": "Hello!"})

for line in proc.stdout:
    event = json.loads(line)
    if event.get("type") == "message_update":
        delta = event.get("assistantMessageEvent", {})
        if delta.get("type") == "text_delta":
            print(delta["delta"], end="", flush=True)
    if event.get("type") == "agent_end":
        break
```

[Source: Pi RPC Docs](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md)

---

## 🔑 API Keys Necessárias (apenas 3)

| Serviço | Variável | Para quê |
|---------|----------|----------|
| **Deepgram** | `DEEPGRAM_API_KEY` | STT (Speech-to-Text) |
| **Cartesia** | `CARTESIA_API_KEY` | TTS (Text-to-Speech) |
| **Anthropic/OpenAI** | `ANTHROPIC_API_KEY` ou `OPENAI_API_KEY` | LLM que o pi usa internamente |

> ⚠️ O LiveKit Server local NÃO precisa de conta cloud. Roda com `livekit-server --dev` e gera keys padrão: `devkey` / `secret`.

[Source: LiveKit Local Docs](https://docs.livekit.io/transport/self-hosting/local/)

---

## 📋 O PLANO DE AÇÃO (para dar ao Pi Coding Agent)

Abaixo está o plano estruturado em **5 prompts sequenciais** que você vai dar ao pi-coding-agent. Cada prompt é **auto-contido** com todo o contexto necessário. Você não precisa explicar nada além do que está escrito.

---

### 📌 PROMPT 1 — Estrutura do Projeto e Dependências

> **Copie e cole este bloco inteiro como prompt para o pi:**

```
Preciso que você monte a estrutura de um projeto chamado "jarvis-voice". 

O projeto é um voice agent que usa LiveKit (WebRTC) para captura de voz, Deepgram para STT, Cartesia para TTS, e delega toda inteligência para o pi-coding-agent via modo RPC (subprocess).

## Estrutura de diretórios

jarvis-voice/
├── agent.py              # LiveKit agent principal
├── pi_bridge.py          # Classe Python que gerencia o subprocess pi --mode rpc
├── web/                  # Frontend Next.js (LiveKit playground)
├── .env.example          # Template de variáveis
├── requirements.txt      # Dependências Python
├── package.json          # Para scripts de conveniência
├── start.sh              # Script que inicia tudo (livekit-server + agent + frontend)
└── README.md

## Crie os arquivos:

### .env.example
```
# LiveKit Local (não mude para dev mode)
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret

# Deepgram (pegar em https://console.deepgram.com)
DEEPGRAM_API_KEY=

# Cartesia (pegar em https://play.cartesia.ai/keys)
CARTESIA_API_KEY=

# LLM para o pi-coding-agent (escolha um)
ANTHROPIC_API_KEY=
# OPENAI_API_KEY=
```

### requirements.txt
```
livekit-agents>=1.0
livekit-plugins-deepgram
livekit-plugins-cartesia
livekit-plugins-silero
python-dotenv
```

### package.json
```json
{
  "name": "jarvis-voice",
  "scripts": {
    "setup": "pip install -r requirements.txt && npm install -g @mariozechner/pi-coding-agent",
    "dev": "bash start.sh"
  }
}
```

Crie todos esses arquivos. Não escreva ainda o agent.py nem o pi_bridge.py (faremos no próximo passo). Apenas a estrutura, .env.example, requirements.txt e package.json.
```

---

### 📌 PROMPT 2 — Pi Bridge (o coração da integração)

> **Copie e cole este bloco inteiro como segundo prompt:**

```
Agora crie o arquivo pi_bridge.py dentro do projeto jarvis-voice/.

Este módulo é uma classe Python chamada PiBridge que:
1. Spawna o pi-coding-agent como subprocess via `pi --mode rpc`
2. Envia comandos JSON via stdin
3. Lê eventos JSONL streaming via stdout
4. Expõe um método async que envia um prompt e retorna um async generator de text_delta chunks

## Contexto técnico do protocolo RPC do pi:

- Iniciar: `pi --mode rpc --no-session` (subprocess com stdin PIPE, stdout PIPE)
- Enviar comando: escrever uma linha JSON em stdin + flush
  Exemplo: `{"type": "prompt", "message": "texto do usuario"}\n`
- Receber: ler linhas JSON de stdout. Cada linha é um evento.
- Eventos relevantes:
  - `{"type": "response", "command": "prompt", "success": true}` → confirmação
  - `{"type": "message_update", "assistantMessageEvent": {"type": "text_delta", "delta": "chunk de texto"}}` → streaming de resposta
  - `{"type": "agent_end", "messages": [...]}` → fim do processamento
  - `{"type": "tool_execution_start", "toolName": "bash", ...}` → pi executando tool
  - `{"type": "tool_execution_end", ...}` → tool finalizada
- Para abortar: `{"type": "abort"}\n`

## Requisitos da classe PiBridge:

```python
import asyncio
import json
import subprocess
from typing import AsyncGenerator, Optional

class PiBridge:
    """Bridge entre LiveKit agent e pi-coding-agent via RPC subprocess."""
    
    def __init__(self, provider: str = "anthropic", model: Optional[str] = None, working_dir: str = "."):
        """
        Args:
            provider: LLM provider para o pi (anthropic, openai, google)
            model: Modelo específico (opcional, pi usa default)
            working_dir: Diretório de trabalho do pi
        """
        # Spawna o processo pi --mode rpc
        
    async def start(self):
        """Inicia o subprocess do pi."""
        
    async def send_prompt(self, text: str) -> AsyncGenerator[str, None]:
        """
        Envia um prompt ao pi e retorna um async generator que yields chunks de texto.
        
        IMPORTANTE: 
        - Só yield os text_delta do assistantMessageEvent
        - NÃO yield conteúdo de tool_execution (bash output, etc)
        - Quando o pi executa tools, yield uma mensagem curta como "Trabalhando nisso..."
        - Quando receber agent_end, para de yieldar
        """
        
    async def abort(self):
        """Aborta a operação atual do pi."""
        
    async def shutdown(self):
        """Encerra o subprocess do pi."""
        
    def _send_command(self, cmd: dict):
        """Envia um comando JSON via stdin."""
        
    async def _read_events(self) -> AsyncGenerator[dict, None]:
        """Lê eventos JSONL do stdout do pi."""
```

## Detalhes críticos de implementação:

1. Use asyncio.subprocess (não subprocess.Popen) para não bloquear o event loop do LiveKit
2. O stdout reader deve ser um loop assíncrono que lê linha por linha
3. Para o send_prompt, crie um asyncio.Queue onde o reader thread coloca eventos e o generator consome
4. Filtre os text_delta: só repasse delta de `assistantMessageEvent.type == "text_delta"`
5. Quando pi executa tools (tool_execution_start), yield "Deixa eu trabalhar nisso... " uma vez
6. Quando receber agent_end, sinalize fim do generator
7. Handle abort: se LiveKit interromper (interrupt), envie {"type": "abort"} ao pi
8. O processo pi deve persistir entre prompts (não crie um novo a cada mensagem)

Implemente a classe completa e funcional.
```

---

### 📌 PROMPT 3 — LiveKit Agent com custom llm_node

> **Copie e cole este bloco inteiro como terceiro prompt:**

```
Agora crie o arquivo agent.py dentro do projeto jarvis-voice/.

Este é o LiveKit Agent que usa Deepgram STT, Cartesia TTS, e substitui o LLM pelo PiBridge.

## Contexto técnico do LiveKit Agents Framework:

O framework usa AgentSession com componentes plugáveis (VAD, STT, LLM, TTS).
Para substituir o LLM, criamos uma subclasse de Agent e fazemos override do método `llm_node`.

O `llm_node` é um método async generator que:
- Recebe o chat context (histórico de mensagens)
- Deve yield strings (chunks de texto) que vão para o TTS
- O LiveKit cuida de tudo mais: VAD, turn detection, interrupções, WebRTC

## Padrão de import e setup:

```python
from livekit.agents import Agent, AgentSession, AgentServer, JobContext, RunContext, cli
from livekit.plugins import silero, deepgram, cartesia
from dotenv import load_dotenv
import os

load_dotenv()

server = AgentServer()
```

## Estrutura do Agent:

```python
class JarvisAgent(Agent):
    def __init__(self, pi_bridge):
        super().__init__(
            instructions="Você é Jarvis, um assistente de voz que pode programar, executar comandos, editar arquivos e resolver problemas técnicos. Responda de forma concisa e direta, adequada para fala.",
        )
        self.pi_bridge = pi_bridge
    
    async def llm_node(self, chat_ctx, tools, model_settings):
        """
        Override do llm_node. Em vez de chamar uma LLM,
        envia o último texto do usuário para o pi-coding-agent via RPC
        e streama a resposta de volta.
        """
        # 1. Extraia a última mensagem do usuário de chat_ctx
        # chat_ctx.items é a lista de mensagens, pegar a última do role "user"
        # 2. Envie para self.pi_bridge.send_prompt(user_text)
        # 3. Yield cada chunk como AgentChunkEvent ou string pura
        # 4. Se receber abort/interrupt, chame self.pi_bridge.abort()
```

## Entrypoint:

```python
@server.rtc_session()
async def entrypoint(ctx: JobContext):
    pi = PiBridge(working_dir=os.getcwd())
    await pi.start()
    
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3", language="pt-BR"),
        tts=cartesia.TTS(
            model="sonic-3",
            voice="<uma_voz_masculina_profissional>",  # Use um voice_id do Cartesia
            language="pt",
        ),
        # NÃO passe llm= aqui, pois o Agent.llm_node cuida disso
    )
    
    agent = JarvisAgent(pi_bridge=pi)
    await session.start(agent=agent, room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)
```

## Para configurar o projeto local (sem LiveKit Cloud):

Use o LiveKit CLI para configurar o projeto local:
```bash
lk project add jarvis-local \
  --url http://localhost:7880 \
  --api-key devkey \
  --api-secret secret \
  --default
```

## Detalhes críticos:

1. O llm_node precisa retornar um AsyncGenerator ou AsyncIterable de chunks de texto
2. Consulte a API do LiveKit Agents para o formato correto do retorno do llm_node
   - Em versões recentes: yield strings direto ou use llm.ChatChunk
3. O Deepgram STT com `language="pt-BR"` garante reconhecimento em português
4. O Cartesia TTS com `language="pt"` sintetiza em português brasileiro
5. O VAD silero é 100% local, não precisa de API key
6. Importe o PiBridge do pi_bridge.py
7. NÃO use inference.STT/TTS (isso é LiveKit Cloud). Use os plugins diretamente:
   - `deepgram.STT(...)` (requer DEEPGRAM_API_KEY no env)
   - `cartesia.TTS(...)` (requer CARTESIA_API_KEY no env)

Implemente o agent.py completo e funcional. Se precisar ajustar a assinatura do llm_node para a versão atual do livekit-agents, faça `pip install livekit-agents` e leia o código fonte do AgentSession para entender a interface esperada.
```

---

### 📌 PROMPT 4 — Script de Inicialização e LiveKit Local

> **Copie e cole como quarto prompt:**

```
Crie o script start.sh que inicializa todo o stack Jarvis localmente.

## O que o script precisa fazer:

1. Verificar se o livekit-server está instalado, se não, baixar:
   - Mac: `brew install livekit`
   - Linux: baixar binário de https://github.com/livekit/livekit/releases/latest
   
2. Verificar se `pi` está instalado (`which pi`), se não: `npm install -g @mariozechner/pi-coding-agent`

3. Verificar se o .env existe (copiar de .env.example se não)

4. Checar se as API keys estão preenchidas no .env

5. Iniciar o livekit-server em background:
   ```bash
   livekit-server --dev --bind 0.0.0.0 &
   ```
   Isso inicia na porta 7880 com api-key=devkey, api-secret=secret

6. Aguardar o servidor ficar pronto (poll http://localhost:7880)

7. Configurar o projeto LiveKit CLI (se `lk` disponível):
   ```bash
   lk project add jarvis-local --url http://localhost:7880 --api-key devkey --api-secret secret --default 2>/dev/null || true
   ```

8. Iniciar o agent:
   ```bash
   python agent.py dev
   ```
   Isso registra o agent no LiveKit server local.

9. Imprimir instruções para o usuário:
   ```
   ========================================
   🤖 JARVIS está rodando!
   ========================================
   
   LiveKit Server: http://localhost:7880
   
   Para conectar via browser, abra:
   https://agents-playground.livekit.io/#tab=connect
   
   E configure:
     URL: ws://localhost:7880
     Token: (gere com: lk token create --api-key devkey --api-secret secret --join --room test --identity user)
   
   OU use o modo console (sem browser):
     python agent.py console
   ========================================
   ```

10. Trap SIGINT para matar o livekit-server em background quando parar

## Também crie um script auxiliar: generate-token.sh

```bash
#!/bin/bash
# Gera um token LiveKit para conectar no playground
lk token create \
  --api-key devkey \
  --api-secret secret \
  --join \
  --room jarvis-room \
  --identity user \
  --valid-for 24h
```

Torne ambos os scripts executáveis.
```

---

### 📌 PROMPT 5 — Web UI (Painel de Visualização do Pi)

> **Copie e cole como quinto prompt:**

```
Agora quero ver a atividade do pi-coding-agent enquanto falo com ele por voz.

Crie um dashboard web simples em jarvis-voice/web/ que mostra:
1. A transcrição da conversa em tempo real (o que eu falei + o que o Jarvis respondeu)
2. As ações do pi (tool calls: bash commands, file edits, etc.)
3. Status atual (idle, thinking, executing tool, speaking)

## Abordagem:

Modifique o pi_bridge.py para também emitir eventos via WebSocket (usando websockets ou FastAPI WebSocket).

Adicione um servidor FastAPI leve no agent.py (ou separado) que:
1. Serve a página HTML estática 
2. Aceita conexões WebSocket em /ws
3. Forwarda todos os eventos do pi para os clients WebSocket conectados

## A página web (web/index.html) deve ter:

- Layout escuro (tema terminal/hacker)
- Painel esquerdo: Chat (transcrição voz + respostas do Jarvis)
- Painel direito: Atividade do Pi (tool calls, bash output, file edits)
- Barra de status no topo (modelo atual, status, tokens usados)
- Auto-scroll conforme novos eventos chegam
- Highlight de sintaxe para código (use highlight.js CDN)

## Eventos que o dashboard recebe via WebSocket:

```json
{"type": "user_speech", "text": "crie um arquivo hello.py"}
{"type": "jarvis_response", "text": "Vou criar o arquivo para você...", "streaming": true}
{"type": "pi_tool_start", "tool": "write", "args": {"path": "hello.py"}}
{"type": "pi_tool_end", "tool": "write", "result": "Arquivo criado"}
{"type": "pi_tool_start", "tool": "bash", "args": {"command": "python hello.py"}}
{"type": "pi_tool_output", "text": "Hello World!"}
{"type": "pi_tool_end", "tool": "bash", "result": "exit code 0"}
{"type": "status", "state": "idle"}
```

## Modificações no pi_bridge.py:

Adicione um WebSocket broadcaster que:
1. Mantém uma lista de clients WebSocket conectados
2. Quando o pi emite qualquer evento, forwarda para todos os clients
3. Os eventos de tool_execution_start/update/end são formatados e enviados
4. Os text_delta também são enviados (além de ir pro TTS)

## Adicione ao start.sh:

Depois de iniciar o agent, abra automaticamente o browser no dashboard:
```bash
# Mac
open http://localhost:8080 2>/dev/null || true
# Linux  
xdg-open http://localhost:8080 2>/dev/null || true
```

Implemente tudo funcional. O dashboard é essencial para eu ver o que o pi está fazendo enquanto converso por voz.
```

---

## 🚀 Como Usar Este Plano

### Passo a passo:

1. **Instale o pi-coding-agent** se ainda não tem:
   ```bash
   npm install -g @mariozechner/pi-coding-agent
   ```

2. **Configure sua API key** do LLM (Anthropic recomendado):
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-sua-chave
   ```

3. **Crie o diretório e inicie o pi:**
   ```bash
   mkdir jarvis-voice && cd jarvis-voice
   pi
   ```

4. **Cole o Prompt 1** → Pi cria a estrutura
5. **Cole o Prompt 2** → Pi cria o pi_bridge.py
6. **Cole o Prompt 3** → Pi cria o agent.py
7. **Cole o Prompt 4** → Pi cria scripts de inicialização
8. **Cole o Prompt 5** → Pi cria o dashboard web

5. **Preencha o `.env`** com suas API keys

6. **Execute:**
   ```bash
   bash start.sh
   ```

---

## ⚡ Por que este plano funciona

| Preocupação | Solução |
|-------------|---------|
| "Pi não vai ter contexto suficiente" | Cada prompt é auto-contido com toda a especificação técnica, exemplos de código, e referências à API |
| "É complicado demais" | Dividido em 5 passos incrementais que constroem um sobre o outro |
| "LiveKit precisa de conta cloud" | Usa `livekit-server --dev` 100% local + plugins diretos (Deepgram/Cartesia) |
| "Quero ver a UI do pi" | Prompt 5 cria um dashboard web que mostra toda atividade do pi em tempo real |
| "Quero interrupções naturais" | LiveKit + Silero VAD = turn detection semântica, interrupções e streaming nativos |
| "Não quero LLM direta no LiveKit" | O `llm_node` override não chama nenhuma LLM — apenas faz bridge com o pi via subprocess |

---

## 📚 Referências Técnicas

- [Pi Mono Repo](https://github.com/badlogic/pi-mono) — Código fonte completo do pi
- [Pi RPC Protocol](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md) — Documentação completa do protocolo RPC
- [Pi Coding Agent Docs](https://www.mintlify.com/pt-act/pi-mono/packages/coding-agent) — Documentação oficial do pi-coding-agent
- [Mario Zechner's Blog Post](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/) — Arquitetura detalhada do pi
- [LiveKit Agents Framework](https://github.com/livekit/agents) — Framework de voice agents
- [LiveKit Local Setup](https://docs.livekit.io/transport/self-hosting/local/) — Como rodar LiveKit localmente
- [LiveKit LLM Output Replacement](https://docs.livekit.io/recipes/replacing_llm_output/) — Padrão de override do llm_node
- [Deepgram Plugin](https://docs.livekit.io/agents/models/stt/deepgram/) — STT com API key direto
- [Cartesia Plugin](https://docs.livekit.io/agents/models/tts/cartesia/) — TTS com API key direto
- [LiveClaw (exemplo similar)](https://github.com/p-sumann/liveclaw) — Voice agent que delega para agent externo

---

> 💡 **Dica final:** Se em algum prompt o pi travar ou pedir mais contexto, diga: *"Leia o arquivo PLAN.md e o conteúdo dos arquivos já criados para contexto, e continue a implementação."* — Salve este plano inteiro como `PLAN.md` no diretório do projeto antes de começar.