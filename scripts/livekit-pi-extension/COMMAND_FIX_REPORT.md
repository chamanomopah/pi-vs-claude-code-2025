# 🚨 Correção Urgente - Comando do Agente Python

## Data: 2026-04-06 20:19:00 GMT-3

---

## ❌ Erro Original

```
Error: Voice chat error: Agent error: Usage: pi_agent.py dev [OPTIONS]
Error: Voice chat error: Agent exited with code 2
```

### Causa Raiz

A extensão `livekit.ts` estava passando argumentos inválidos para o agente Python:

```typescript
const process = spawn("python", [scriptPath, "dev", "--room", room], {
```

**Problema:** O LiveKit agents framework **não aceita** o argumento `--room` na linha de comando.

---

## 🎯 Arquitetura do LiveKit Agents

### Entendendo o Modelo Worker-Job

O LiveKit agents usa uma arquitetura de **Worker-Job**:

```
┌─────────────────┐
│  Python Worker  │ ← Roda continuamente aguardando jobs
│  (pi_agent.py)  │
└────────┬────────┘
         │
         │ Se conecta ao LiveKit Server
         ▼
┌─────────────────┐
│ LiveKit Server  │ ← Gerencia salas e distribui jobs
└────────┬────────┘
         │
         │ Cliente especifica a sala
         ▼
┌─────────────────┐
│  Pi Extension   │ ← Conecta a uma sala específica
│   (Cliente)     │
└─────────────────┘
```

### Fluxo Correto

1. **Worker Python**: Inicia com `python pi_agent.py dev`
   - Fica aguardando conexões do LiveKit Server
   - NÃO especifica sala

2. **Cliente (Pi)**: Conecta ao LiveKit Server
   - Especifica o nome da sala
   - LiveKit Server cria um job e distribui ao worker

3. **LiveKit Server**: Gerencia tudo
   - Passa o contexto da sala para o worker via `JobContext`
   - O worker acessa a sala via `ctx.room.name`

---

## ✅ Solução Implementada

### Mudança 1: Remover `--room` do comando TypeScript

**Arquivo:** `extensions/livekit.ts`

**Antes:**
```typescript
const process = spawn("python", [scriptPath, "dev", "--room", room], {
    env,
    stdio: ["ignore", "pipe", "pipe"],
});
```

**Depois:**
```typescript
// Start the LiveKit agent worker in dev mode
// The room name is specified by the client when connecting to LiveKit Server
const process = spawn("python", [scriptPath, "dev"], {
    env,
    stdio: ["ignore", "pipe", "pipe"],
});
```

### Mudança 2: Remover parsing de `--room` no Python

**Arquivo:** `scripts/livekit-pi-extension/pi_agent.py`

**Antes:**
```python
# Get room name from command line args or use default
room_name = "default-room"
for i, arg in enumerate(sys.argv):
    if arg == "--room" and i + 1 < len(sys.argv):
        room_name = sys.argv[i + 1]
        break

print(f"[Agent] Connecting to room: {room_name}")
print(f"[Agent] LiveKit URL: {livekit_url}")
```

**Depois:**
```python
# Room name will be provided by LiveKit Server via JobContext
print(f"[Agent] LiveKit URL: {livekit_url}")
print("[Agent] Starting worker, waiting for jobs...")
```

### Mudança 3: Usar `ctx.room.name` para obter o nome da sala

**Arquivo:** `scripts/livekit-pi-extension/pi_agent.py`

**Antes:**
```python
print(f"[Agent] Connected to room: {room_name}")
```

**Depois:**
```python
# Room name is available via ctx.room.name
print(f"[Agent] Connected to room: {ctx.room.name}")
```

---

## 🧪 Testes de Validação

### Teste 1: Comando Python
```bash
$ cd scripts/livekit-pi-extension
$ python pi_agent.py dev

20:19:34.468 DEBUG  asyncio            Using proactor: IocpProactor
20:19:34.473 DEV    livekit.agents     Watching
                                            C:\Users\JOSE\.claude\...
```

**Resultado:** ✅ Worker inicia corretamente em modo dev

### Teste 2: Sintaxe Python
```bash
$ python -m py_compile scripts/livekit-pi-extension/pi_agent.py
✓ Syntax check passed
```

### Teste 3: Validação Completa
```bash
$ node scripts/livekit-pi-extension/validate_setup.js
✓ Passou: 4/4
```

---

## 📊 Comandos Disponíveis do LiveKit Agents

```bash
python pi_agent.py dev          # Modo desenvolvimento
python pi_agent.py start        # Modo produção
python pi_agent.py console      # Modo console interativo
python pi_agent.py connect      # Conectar a uma sala existente
python pi_agent.py download-files  # Baixar modelos (VAD, etc)
```

**Nenhum desses comandos aceita `--room` como argumento.**

---

## 🔧 Como Especificar a Sala

### Lado do Cliente (Pi)

A sala é especificada quando o **cliente se conecta ao LiveKit Server**:

```typescript
// No código do cliente (Pi)
const room = await client.joinRoom({
    roomName: "minha-sala",  // ← Aqui se especifica a sala
    participantName: "pi-assistant"
});
```

### Lado do Worker (Python)

O worker recebe automaticamente o contexto da sala:

```python
async def entrypoint(ctx: agents.JobContext):
    # A sala já está disponível no contexto
    room_name = ctx.room.name
    print(f"Connected to room: {room_name}")
```

---

## ✅ Comportamento Esperado Agora

### 1. Iniciar o Worker Python

```bash
python pi_agent.py dev
```

**Output esperado:**
```
[Agent] LiveKit URL: ws://localhost:7880
[Agent] Starting worker, waiting for jobs...
20:19:34.473 DEV    livekit.agents     Watching ...
```

### 2. Conectar via Pi

```bash
pi -e extensions/livekit.ts
/speak minha-sala
```

**Output esperado:**
```
[Agent] Connected to room: minha-sala
[Agent] Listening for voice input...
```

---

## 🎯 Benefícios da Correção

### 1. **Arquitetura Correta**
- Worker aguarda jobs, não especifica salas
- Cliente (Pi) especifica a sala ao conectar
- LiveKit Server gerencia a distribuição

### 2. **Escalabilidade**
- Um único worker pode atender múltiplas salas
- LiveKit Server distribui jobs automaticamente
- Pode ter múltiplos workers para balanceamento de carga

### 3. **Simplicidade**
- Não precisa passar argumentos complexos
- Room context disponível automaticamente
- Segue o padrão do LiveKit agents

---

## 📝 Resumo das Mudanças

| Arquivo | Linha | Mudança |
|---------|-------|---------|
| `extensions/livekit.ts` | ~385 | Removido `--room` e argumento `room` |
| `scripts/livekit-pi-extension/pi_agent.py` | ~95-105 | Removido parsing de `--room` |
| `scripts/livekit-pi-extension/pi_agent.py` | ~115 | Usar `ctx.room.name` em vez de `room_name` |

---

## ✅ Status Final

| Verificação | Status |
|-------------|--------|
| Comando corrigido | ✅ |
| Worker inicia corretamente | ✅ |
| Sintaxe Python válida | ✅ |
| Arquitetura correta | ✅ |
| Validação 4/4 | ✅ |
| **Pronto para testes** | ✅ |

---

## 🚀 Próximos Passos

A extensão agora segue a arquitetura correta do LiveKit agents:

```bash
# 1. Iniciar LiveKit Server
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  -v $PWD/livekit.yaml:/livekit.yaml \
  livekit/livekit-server \
  --config /livekit.yaml \
  --node-ip 127.0.0.1

# 2. Carregar extensão
pi -e extensions/livekit.ts

# 3. Iniciar voice chat
/speak minha-sala
```

---

**Correção completada em:** 2026-04-06 20:19:00 GMT-3
**Status:** ✅ **COMANDO CORRIGIDO - ARQUITETURA CORRETA**
