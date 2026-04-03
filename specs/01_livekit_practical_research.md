# LiveKit Practical Research - Guia Completo

> Pesquisa realizada em 2026-04-03
> APIs fornecidas: Deepgram STT, Cartesia TTS

---

## Índice
1. [Como fazer projetos práticos com LiveKit](#1-como-fazer-projetos-práticos-com-livekit)
2. [Boas práticas para desenvolvimento com LiveKit](#2-boas-práticas-para-desenvolvimento-com-livekit)
3. [Erros comuns ao rodar LiveKit localmente](#3-erros-comuns-ao-rodar-livekit-localmente)
4. [Como integrar Deepgram (STT) com LiveKit](#4-como-integrar-deepgram-stt-com-livekit)
5. [Como integrar Cartesia (TTS) com LiveKit](#5-como-integrar-cartesia-tts-com-livekit)
6. [Exemplos de código práticos](#6-exemplos-de-código-práticos)

---

## 1. Como fazer projetos práticos com LiveKit

### 1.1 Instalação do LiveKit Server

#### Instalação via CLI (Recomendado)

**macOS:**
```bash
brew install livekit
```

**Linux:**
```bash
curl -sSL https://get.livekit.io | bash
```

**Windows:**
- Baixe a última versão: https://github.com/livekit/livekit/releases/latest

#### Iniciando em modo de desenvolvimento
```bash
livekit-server --dev
```

**Credenciais de desenvolvimento padrão:**
- API Key: `devkey`
- API Secret: `secret`
- Porta: `7880` (WebSocket/HTTP)
- Porta TCP: `7881` (WebRTC sobre TCP)
- Porta UDP: `50000-60000` (WebRTC sobre UDP)

**Fonte:** https://github.com/livekit/livekit

### 1.2 LiveKit CLI - Ferramenta essencial

#### Instalação do CLI
```bash
# macOS
brew install livekit

# Linux
curl -sSL https://get.livekit.io | bash
```

**Repositório:** https://github.com/livekit/livekit-cli

#### Comandos úteis

**Criar token de acesso:**
```bash
lk token create \
    --api-key devkey \
    --api-secret secret \
    --join \
    --room my-first-room \
    --identity user1 \
    --valid-for 24h
```

**Entrar em uma sala (simular participante):**
```bash
lk room join \
    --url ws://localhost:7880 \
    --api-key devkey --api-secret secret \
    --identity bot-user1 \
    --publish-demo \
    my-first-room
```

**Fonte:** https://github.com/livekit/livekit

### 1.3 LiveKit Agents Framework

#### Instalação do Agents Framework

**Instalação completa com plugins:**
```bash
pip install "livekit-agents[openai,silero,deepgram,cartesia,turn-detector]~=1.4"
```

**Plugins individuais:**
```bash
pip install livekit-plugins-deepgram
pip install livekit-plugins-cartesia
```

**Repositório:** https://github.com/livekit/agents

### 1.4 Estrutura de um projeto LiveKit Agents

#### Estrutura recomendada
```
my-agent-project/
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências Python
├── agent.py                  # Código principal do agente
├── frontend/                 # Aplicação frontend (opcional)
│   ├── package.json
│   └── src/
└── config.yaml              # Configuração (se necessário)
```

#### Arquivo requirements.txt
```txt
livekit-agents~=1.4
livekit-plugins-deepgram
livekit-plugins-cartesia
livekit-plugins-openai
python-dotenv
```

#### Arquivo .env
```env
# LiveKit
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Provedores
DEEPGRAM_API_KEY=5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3
CARTESIA_API_KEY=sk_car_d69NmtdJKVbTj8XrrqM4Nt
OPENAI_API_KEY=sk-your-openai-key
```

**Fonte:** https://github.com/livekit-examples/python-agents-examples

### 1.5 Executando Agentes

#### Modos de execução

**Modo Console (teste local sem servidor):**
```bash
python agent.py console
```

**Modo Desenvolvimento (hot reload):**
```bash
python agent.py dev
```

**Modo Produção:**
```bash
python agent.py start
```

**Conectar a sala existente:**
```bash
python agent.py connect --room <room> --identity <id>
```

**Fonte:** https://github.com/livekit/agents/blob/main/AGENTS.md

### 1.6 Exemplo de Aplicação Completa

#### Backend (Python)
```python
from livekit.agents import Agent, AgentServer, AgentSession, JobContext
from livekit.plugins import silero

server = AgentServer()

class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant."
        )

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt="deepgram/nova-3-general",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
    )
    agent = MyAgent()
    await session.start(agent=agent, room=ctx.room)
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(server)
```

#### Frontend (React - Exemplo simplificado)
```typescript
import { Room, RemoteTrackPublication } from 'livekit-client';

const room = new Room();

async function joinRoom() {
  await room.connect('wss://your-server.livekit.cloud', token);
  room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
    if (track.kind === Track.Kind.Video) {
      const element = document.createElement('video');
      element.srcObject = new MediaStream([track.mediaStreamTrack]);
      document.body.appendChild(element);
    }
  });
}
```

**Fonte:** https://github.com/livekit/agents e https://github.com/livekit/client-sdk-js

---

## 2. Boas práticas para desenvolvimento com LiveKit

### 2.1 Gerenciamento de Credenciais

#### Use variáveis de ambiente
```python
import os
from dotenv import load_dotenv

load_dotenv()

LIVEKIT_URL = os.getenv('LIVEKIT_URL')
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')
```

**NUNCA hardcode credenciais no código.**

### 2.2 Tratamento de Erros

#### Tratamento robusto de exceções
```python
from livekit.agents import JobContext, JobProcess
import logging

logger = logging.getLogger(__name__)

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    try:
        session = AgentSession(
            stt="deepgram/nova-3-general",
            llm="openai/gpt-4.1-mini",
            tts="cartesia/sonic-3",
        )
        await session.start(agent=agent, room=ctx.room)
        await ctx.connect()
    except Exception as e:
        logger.error(f"Error in session: {e}")
        raise
```

### 2.3 Prewarming de recursos

#### Carregar VAD antes da sessão
```python
from livekit.plugins import silero

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

server = AgentServer()
server.setup_fnc = prewarm
```

**Fonte:** https://github.com/livekit/agents/blob/main/AGENTS.md

### 2.4 Logging Estruturado

#### Contexto de log
```python
@server.rtc_session()
async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {
        "room": ctx.room.name,
        "identity": ctx.info.identity
    }
```

### 2.5 Testes de Agentes

#### Testes assíncronos com pytest
```python
import pytest
from livekit.agents import AgentSession

@pytest.mark.asyncio
async def test_agent_response():
    async AgentSession(llm=llm) as sess:
        await sess.start(MyAgent())
        result = await sess.run(user_input="Hello")
        result.expect.next_event().is_message(role="assistant")
```

**Fonte:** https://github.com/livekit/agents/blob/main/README.md

### 2.6 Versionamento de Dependências

#### Use especificações de versão
```bash
# Use ~= para updates de compatibilidade
pip install "livekit-agents~=1.4"

# Ou pinne versões específicas para produção
pip install "livekit-agents==1.4.0"
```

### 2.7 Configuração de Rede

#### Portas necessárias
- `7880` - WebSocket/HTTP principal
- `7881` - WebRTC sobre TCP
- `50000-60000` - WebRTC sobre UDP
- `3478` - STUN/TURN (se configurado)

#### Firewall
```bash
# Abrir portas necessárias
sudo ufw allow 7880/tcp
sudo ufw allow 7881/tcp
sudo ufw allow 50000:60000/udp
```

**Fonte:** https://github.com/livekit/livekit/blob/master/config-sample.yaml

---

## 3. Erros comuns ao rodar LiveKit localmente

### 3.1 Erros de Rede

#### Erro: Connection refused na porta 7880
**Solução:**
```bash
# Verificar se o servidor está rodando
ps aux | grep livekit-server

# Iniciar o servidor
livekit-server --dev
```

#### Erro: UDP ports blocked
**Sintoma:** Vídeo/audio não carrega
**Solução:**
```bash
# Verificar firewall
sudo ufw status

# Abrir portas UDP
sudo ufw allow 50000:60000/udp

# Ou usar TCP fallback
# Adicionar ao config.yaml:
# rtc:
#   tcp_port: 7881
```

**Fonte:** https://github.com/livekit/livekit

### 3.2 Erros de Autenticação

#### Erro: Invalid token
**Solução:**
```bash
# Verificar credenciais no .env
cat .env | grep LIVEKIT

# Gerar novo token
lk token create \
    --api-key devkey \
    --api-secret secret \
    --join \
    --room my-room \
    --identity user1
```

#### Erro: Token expired
**Solução:**
```bash
# Gerar token com validade maior
lk token create \
    --api-key devkey \
    --api-secret secret \
    --join \
    --room my-room \
    --identity user1 \
    --valid-for 72h
```

### 3.3 Erros de Memória/Performance

#### Erro: Out of memory
**Solução:**
```python
# Limite de sessões concorrentes
# Configurar no server setup

# Otimizar VAD
from livekit.plugins import silero
vad = silero.VAD.load(threshold=0.5)  # Aumentar threshold
```

#### Erro: CPU alto
**Solução:**
```python
# Usar preemptive_generation com cuidado
session = AgentSession(
    stt="deepgram/nova-3-general",
    llm="openai/gpt-4.1-mini",
    tts="cartesia/sonic-3",
    preemptive_generation=False,  # Desativar para reduzir CPU
)
```

### 3.4 Erros de Dependências

#### Erro: Module not found: livekit.agents
**Solução:**
```bash
# Verificar ambiente virtual
which python

# Reinstalar
pip uninstall livekit-agents
pip install "livekit-agents[openai,silero,deepgram,cartesia]~=1.4"
```

#### Erro: Missing VAD model
**Solução:**
```python
# Prewarming correto
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

server = AgentServer()
server.setup_fnc = prewarm
```

### 3.5 Erros de API Keys

#### Erro: Deepgram API key invalid
**Solução:**
```env
# Verificar arquivo .env
DEEPGRAM_API_KEY=5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3
```

#### Erro: Cartesia API key invalid
**Solução:**
```env
# Verificar arquivo .env
CARTESIA_API_KEY=sk_car_d69NmtdJKVbTj8XrrqM4Nt
```

**Nota:** As chaves fornecidas precisam ser válidas. Verifique no console de cada provedor.

### 3.6 Erros de CORS

#### Erro: CORS policy blocked
**Solução:**
```yaml
# config.yaml
# Adicionar domínios permitidos
cors:
  allowed_origins:
    - http://localhost:3000
    - https://your-domain.com
```

### 3.7 Erros de SSL/TLS

#### Erro: SSL certificate error
**Solução:**
```bash
# Para desenvolvimento, pode usar http
LIVEKIT_URL=ws://localhost:7880

# Para produção, usar certificados válidos
LIVEKIT_URL=wss://your-domain.com
```

---

## 4. Como integrar Deepgram (STT) com LiveKit

### 4.1 Instalação do Plugin Deepgram

```bash
pip install livekit-plugins-deepgram
```

**Repositório:** https://github.com/livekit/agents/tree/main/livekit-plugins/livekit-plugins-deepgram

### 4.2 Configuração da API Key

```env
# .env
DEEPGRAM_API_KEY=5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3
```

### 4.3 Usando Deepgram via LiveKit Inference (Recomendado)

#### Exemplo básico
```python
from livekit.agents import Agent, AgentSession, JobContext
from livekit.agents import inference

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3-general", language="multi"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(model="cartesia/sonic-3"),
    )
    # ...
```

**Documentação:** https://docs.livekit.io/agents/integrations/stt/deepgram/

### 4.4 Usando Deepgram diretamente

#### Exemplo com plugin direto
```python
from livekit.agents import Agent, AgentSession
from livekit.plugins import deepgram

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="en-US"),
        llm=llm,
        tts=tts,
    )
    # ...
```

### 4.5 Modelos Deepgram disponíveis

| Modelo | Descrição | Uso |
|--------|-----------|-----|
| `nova-3` | Modelo padrão, alta precisão | Geral |
| `nova-3-general` | Otimizado para uso geral | Conversas |
| `nova-3-phonecall` | Otimizado para telefonia | Chamadas |
| `nova-3-meeting` | Otimizado para reuniões | Meetings |

**Fonte:** Documentação Deepgram via LiveKit Agents

### 4.6 Configurações avançadas do Deepgram

#### Multilíngue
```python
stt=inference.STT(
    model="deepgram/nova-3-general",
    language="multi",  # Suporte a múltiplos idiomas
)
```

#### Streaming com pontuação
```python
stt=inference.STT(
    model="deepgram/nova-3-general",
    punctuate=True,  # Adicionar pontuação
    profanity_filter=True,  # Filtrar palavrões
)
```

### 4.7 Exemplo completo com Deepgram

```python
"""
Agent Deepgram Completo
"""
from dotenv import load_dotenv
from livekit.agents import (
    Agent, AgentServer, AgentSession,
    JobContext, inference, cli
)
from livekit.plugins import silero

load_dotenv()

class DeepgramAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant."
        )

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        # Deepgram STT
        stt=inference.STT(
            model="deepgram/nova-3-general",
            language="multi",
        ),
        # LLM (qualquer provedor)
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        # TTS
        tts=inference.TTS(model="cartesia/sonic-3"),
        # VAD
        vad=silero.VAD.load(),
    )
    
    agent = DeepgramAgent()
    await session.start(agent=agent, room=ctx.room)
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(server)
```

**Fonte:** https://github.com/livekit/agents e https://github.com/livekit-examples/python-agents-examples

---

## 5. Como integrar Cartesia (TTS) com LiveKit

### 5.1 Instalação do Plugin Cartesia

```bash
pip install livekit-plugins-cartesia
```

**Repositório:** https://github.com/livekit/agents/tree/main/livekit-plugins/livekit-plugins-cartesia

### 5.2 Configuração da API Key

```env
# .env
CARTESIA_API_KEY=sk_car_d69NmtdJKVbTj8XrrqM4Nt
```

### 5.3 Usando Cartesia via LiveKit Inference (Recomendado)

#### Exemplo básico
```python
from livekit.agents import Agent, AgentSession, JobContext
from livekit.agents import inference

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3-general"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
    )
```

**Documentação:** https://docs.livekit.io/agents/integrations/tts/cartesia/

### 5.4 Usando Cartesia diretamente

#### Exemplo com plugin direto
```python
from livekit.plugins import cartesia

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=cartesia.TTS(
            model="sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        ),
    )
```

### 5.5 Modelos e vozes Cartesia

#### Modelos disponíveis
- `sonic-3` - Modelo principal, alta qualidade
- `sonic-2` - Modelo anterior, menor latência

#### Voces populares
Voice IDs para o modelo sonic-3:
- `9626c31c-bec5-4cca-baa8-f8ba9e84c8bc` - Voice padrão
- Outras vozes disponíveis no dashboard Cartesia

### 5.6 Configurações avançadas do Cartesia

#### Controle de velocidade
```python
tts=inference.TTS(
    model="cartesia/sonic-3",
    voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
    speed=1.2,  # Velocidade (default: 1.0)
)
```

#### Sample rate
```python
tts=inference.TTS(
    model="cartesia/sonic-3",
    voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
    sample_rate=24000,  # Sample rate em Hz
)
```

### 5.7 Exemplo completo com Cartesia

```python
"""
Agent Cartesia Completo
"""
from dotenv import load_dotenv
from livekit.agents import (
    Agent, AgentServer, AgentSession,
    JobContext, inference, cli
)
from livekit.plugins import silero

load_dotenv()

class CartesiaAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant with a natural voice."
        )

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        # STT
        stt=inference.STT(model="deepgram/nova-3-general"),
        # LLM
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        # Cartesia TTS
        tts=inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
            sample_rate=24000,
        ),
        # VAD
        vad=silero.VAD.load(),
    )
    
    agent = CartesiaAgent()
    await session.start(agent=agent, room=ctx.room)
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(server)
```

### 5.8 Combinando Deepgram + Cartesia

```python
"""
Pipeline completa: Deepgram STT + OpenAI LLM + Cartesia TTS
"""
from dotenv import load_dotenv
from livekit.agents import (
    Agent, AgentServer, AgentSession,
    JobContext, inference, cli
)
from livekit.plugins import silero

load_dotenv()

class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant."
        )

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        # STT: Deepgram
        stt=inference.STT(
            model="deepgram/nova-3-general",
            language="multi",
        ),
        # LLM: OpenAI
        llm=inference.LLM(
            model="openai/gpt-4.1-mini",
        ),
        # TTS: Cartesia
        tts=inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        ),
        # VAD: Silero
        vad=silero.VAD.load(),
    )
    
    agent = VoiceAgent()
    await session.start(agent=agent, room=ctx.room)
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(server)
```

**Fonte:** https://github.com/livekit/agents e https://github.com/livekit-examples/python-agents-examples

---

## 6. Exemplos de Código Práticos

### 6.1 Agente Simples (Listen and Respond)

**Fonte:** https://github.com/livekit-examples/python-agents-examples

```python
"""
Listen and Respond Agent
Agente mais básico que ouve e responde
"""
import logging
from dotenv import load_dotenv
from livekit.agents import (
    JobContext, JobProcess, Agent, AgentSession,
    inference, AgentServer, cli
)
from livekit.plugins import silero

load_dotenv()

logger = logging.getLogger("listen-and-respond")
logger.setLevel(logging.INFO)

class ListenAndRespondAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
                You are a helpful agent. When the user speaks, 
                you listen and respond.
            """
        )

    async def on_enter(self):
        self.session.generate_reply()

server = AgentServer()

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

server.setup_fnc = prewarm

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3-general"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )
    
    agent = ListenAndRespondAgent()

    await session.start(agent=agent, room=ctx.room)
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(server)
```

### 6.2 Agente com Tool Calling

**Fonte:** https://github.com/livekit-examples/python-agents-examples

```python
"""
Tool Calling Agent
Demonstra como usar function tools
"""
import logging
from dotenv import load_dotenv
from livekit.agents import (
    JobContext, JobProcess, AgentServer, cli,
    Agent, AgentSession, inference,
    RunContext, function_tool
)
from livekit.plugins import silero

logger = logging.getLogger("tool-calling")
logger.setLevel(logging.INFO)

load_dotenv()

class ToolCallingAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
                You are a helpful assistant communicating through voice. 
                Don't use any unpronouncable characters.
                Note: If asked to print to the console, use the 
                `print_to_console` function.
            """
        )

    @function_tool
    async def print_to_console(self, context: RunContext):
        """Print a message to the console."""
        print("Console Print Success!")
        return None, "I've printed to the console."

    async def on_enter(self):
        self.session.generate_reply()

server = AgentServer()

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

server.setup_fnc = prewarm

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3-general"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    await session.start(agent=ToolCallingAgent(), room=ctx.room)
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(server)
```

### 6.3 Multi-Agent Handoff

**Fonte:** https://github.com/livekit/agents/blob/main/README.md

```python
"""
Multi-Agent Handoff
Demonstra transferência entre múltiplos agentes
"""
from livekit.agents import (
    Agent, AgentServer, AgentSession,
    JobContext, function_tool, inference,
    RunContext
)
from livekit.plugins import silero, openai

server = AgentServer()

class IntroAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=f"""
                You are a story teller. Your goal is to gather a few 
                pieces of information from the user to make the story 
                personalized and engaging.
                Ask the user for their name and where they are from
            """
        )

    async def on_enter(self):
        self.session.generate_reply(
            instructions="greet the user and gather information"
        )

    @function_tool
    async def information_gathered(
        self,
        context: RunContext,
        name: str,
        location: str,
    ):
        """Called when user provides all needed information."""
        context.userdata.name = name
        context.userdata.location = location
        
        story_agent = StoryAgent(name, location)
        return story_agent, "Let's start the story!"

class StoryAgent(Agent):
    def __init__(self, name: str, location: str) -> None:
        super().__init__(
            instructions=f"""
                You are a storyteller. Use the user's information to make 
                the story personalized. The user's name is {name}, 
                from {location}
            """,
            llm=openai.realtime.RealtimeModel(voice="echo"),
        )

    async def on_enter(self):
        self.session.generate_reply()

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    userdata = type('obj', (object,), {})()
    session = AgentSession(
        vad=silero.VAD.load(),
        stt="deepgram/nova-3-general",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        userdata=userdata,
    )

    await session.start(agent=IntroAgent(), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)
```

### 6.4 Agente de Tradução

```python
"""
Translation Agent
Demonstra tradução em tempo real
"""
from livekit.agents import Agent, AgentSession, JobContext, inference
from livekit.plugins import silero

class TranslationAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
                You are a professional translator. 
                Translate everything the user says from English to French.
                Provide only the translation, nothing else.
            """
        )

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3-general"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
        vad=silero.VAD.load(),
    )
    
    agent = TranslationAgent()
    await session.start(agent=agent, room=ctx.room)
    await ctx.connect()
```

### 6.5 Testes de Agentes

**Fonte:** https://github.com/livekit/agents/blob/main/README.md

```python
"""
Tests de Agentes
Demonstra como escrever testes para agentes
"""
import pytest
from livekit.agents import Agent, AgentSession
from livekit.plugins import google

class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful assistant."
        )

@pytest.mark.asyncio
async def test_no_availability():
    llm = google.LLM()
    async AgentSession(llm=llm) as sess:
        await sess.start(MyAgent())
        result = await sess.run(
            user_input="Hello, I need to place an order."
        )
        result.expect.skip_next_event_if(type="message", role="assistant")
        result.expect.next_event().is_function_call(name="start_order")
        result.expect.next_event().is_function_call_output()
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="assistant should be asking the user what they would like"
            )
        )
```

---

## Recursos Adicionais

### Repositórios Oficiais
- **LiveKit Server:** https://github.com/livekit/livekit
- **LiveKit Agents:** https://github.com/livekit/agents
- **Agents Examples:** https://github.com/livekit-examples/python-agents-examples
- **LiveKit CLI:** https://github.com/livekit/livekit-cli
- **Client SDK JS:** https://github.com/livekit/client-sdk-js
- **LiveKit React:** https://github.com/livekit/livekit-react

### Documentação
- **Documentação Principal:** https://docs.livekit.io
- **Agents Docs:** https://docs.livekit.io/agents/
- **Deepgram Plugin:** https://docs.livekit.io/agents/integrations/stt/deepgram/
- **Cartesia Plugin:** https://docs.livekit.io/agents/integrations/tts/cartesia/

### Comunidade
- **Slack:** https://livekit.io/join-slack
- **Twitter:** https://twitter.com/livekit
- **GitHub Issues:** https://github.com/livekit/agents/issues

### Exemplos de Aplicações
- **LiveKit Meet:** https://meet.livekit.io
- **Spatial Audio Demo:** https://spatial-audio-demo.livekit.io/
- **AI Voice Assistant (Kitt):** https://livekit.io/kitt

---

## Checklist de Desenvolvimento

### Primeiros Passos
- [ ] Instalar LiveKit CLI
- [ ] Iniciar servidor em modo dev (`livekit-server --dev`)
- [ ] Criar arquivo `.env` com credenciais
- [ ] Instalar `livekit-agents` com plugins necessários
- [ ] Testar com `lk room join`

### Desenvolvimento do Agente
- [ ] Criar classe `Agent` com instruções
- [ ] Configurar `AgentSession` com STT, LLM, TTS
- [ ] Implementar função `entrypoint`
- [ ] Adicionar function tools se necessário
- [ ] Testar em modo `console`

### Integração Deepgram
- [ ] Instalar `livekit-plugins-deepgram`
- [ ] Configurar `DEEPGRAM_API_KEY`
- [ ] Usar `inference.STT(model="deepgram/nova-3-general")`
- [ ] Testar reconhecimento de fala

### Integração Cartesia
- [ ] Instalar `livekit-plugins-cartesia`
- [ ] Configurar `CARTESIA_API_KEY`
- [ ] Usar `inference.TTS(model="cartesia/sonic-3", voice="...")`
- [ ] Testar síntese de voz

### Produção
- [ ] Configurar Redis para distribuição
- [ ] Usar tokens JWT válidos
- [ ] Implementar tratamento de erros
- [ ] Adicionar logs estruturados
- [ ] Configurar monitoramento
- [ ] Testar com carga

---

## Notas Importantes

1. **API Keys:** As chaves fornecidas (Deepgram e Cartesia) precisam ser validadas nos respectivos painéis de controle dos provedores.

2. **Documentação em constante atualização:** A documentação do LiveKit é atualizada frequentemente. Sempre verifique a versão mais recente.

3. **LiveKit Cloud vs Self-hosted:** Para desenvolvimento rápido, considere usar LiveKit Cloud com créditos gratuitos.

4. **Dependências:** Mantenha todas as dependências atualizadas, mas teste antes de atualizar em produção.

5. **Comunidade:** Junte-se ao Slack do LiveKit para obter ajuda direta da comunidade e da equipe.

---

## Referências

Todas as informações neste documento foram obtidas de:
- Repositórios oficiais do LiveKit no GitHub
- Documentação oficial do LiveKit
- Repositório de exemplos `python-agents-examples`
- Documentação de plugins (Deepgram, Cartesia)
- Arquivos de configuração de exemplo

**Data da pesquisa:** 2026-04-03
**Versão do Agents:** 1.4.x
**Versão do LiveKit Server:** Latest

---

*Este documento é um guia prático para desenvolvimento com LiveKit, focando em integrações reais e exemplos funcionais.*
