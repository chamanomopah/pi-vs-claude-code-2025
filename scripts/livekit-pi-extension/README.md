# LiveKit + Pi - True Hands-Free Voice Interface

## 🎉 Status: PRONTO PARA USO

Uma interface de voz verdadeiramente hands-free para Pi.

---

## 🚀 Começo Rápido

### 1. Testar Microfone
```bash
python scripts/livekit-pi-extension/test_mic.py
```

Fale no microfone e veja o nível de volume.

### 2. Carregar Extensão
```bash
pi -e extensions/livekit.ts
```

### 3. Ativar Modo Voz
```
/speak
```

### 4. Falar Naturalmente
- Fale algo como "Hello, can you hear me?"
- O sistema transcreverá, enviará para Pi, e falará a resposta
- A última frase da resposta aparecerá no terminal

### 5. Parar
```
/un speak
```

---

## ✨ Funcionalidades

- ✅ **Ativação imediata** - `/speak` ativa modo voz sem confirmação
- ✅ **Captura automática** - Microfone captura continuamente
- ✅ **Transcrição precisa** - Deepgram STT
- ✅ **Síntese natural** - Cartesia TTS (voz Sonic-3)
- ✅ **Exibição limpa** - Apenas última frase da resposta
- ✅ **Status em tempo real** - Widget mostra estado atual
- ✅ **Verdadeiramente hands-free** - Sem cliques ou digitação

---

## 📋 Comandos

| Comando | Descrição |
|---------|-----------|
| `/speak` | Ativa modo voz imediatamente |
| `/un speak` | Para modo voz |
| `/speak-status` | Mostra status do modo voz |

---

## 🔧 Configuração

### Variáveis de Ambiente (`.env`)

```bash
# Speech-to-Text
DEEPGRAM_API_KEY=your_key_here

# Text-to-Speech
CARTESIA_API_KEY=your_key_here
```

### Dependências Python

```bash
pip install pyaudio requests numpy
```

---

## 📊 Como Funciona

```
/speak
  ↓
Extensão Pi inicia modo voz
  ↓
Cliente Python captura microfone
  ↓
VAD detecta fala
  ↓
Deepgram transcreve
  ↓
Transcrição enviada ao Pi
  ↓
Pi processa e responde
  ↓
Cartesia sintetiza fala
  ↓
Áudio reproduzido
  ↓
Última frase exibida
```

---

## 🎯 Estados do Sistema

| Emoji | Estado | Descrição |
|-------|--------|-----------|
| ⚫ | Inactive | Modo voz desativado |
| 🟡 | Starting | Iniciando modo voz |
| 🎤 | Listening | Aguardando fala |
| ⚙️ | Processing | Transcrevendo e processando |
| 🔊 | Speaking | Reproduzindo resposta |
| ❌ | Error | Erro no sistema |

---

## 📁 Arquivos

- `extensions/livekit.ts` - Extensão Pi (TypeScript)
- `scripts/livekit-pi-extension/simple_handsfree.py` - Cliente voz (Python)
- `scripts/livekit-pi-extension/test_mic.py` - Teste de microfone
- `scripts/livekit-pi-extension/.env` - Configuração (API keys)

---

## 🐛 Troubleshooting

### Microfone não funciona
```bash
# Testar microfone
python scripts/livekit-pi-extension/test_mic.py
```

Se não mostrar volume:
1. Verifique se o microfone está conectado
2. Cheque permissões do microfone
3. Teste em outro USB port
4. Verifique configurações de áudio do sistema

### Transcrição não funciona
1. Verifique DEEPGRAM_API_KEY no `.env`
2. Teste a key: `curl -H "Authorization: Token YOUR_KEY" https://api.deepgram.com`
3. Verifique conexão com internet

### Fala não funciona
1. Verifique CARTESIA_API_KEY no `.env`
2. Teste a key na documentação da Cartesia
3. Verifique se o alto-falante está funcionando

---

## 📖 Documentação Adicional

- `REIMPLEMENTATION_REPORT.md` - Relatório completo da reimplementação
- `COMMAND_FIX_REPORT.md` - Correção de comandos
- `IMPORT_FIX_REPORT.md` - Correção de imports
- `VALIDATION_REPORT.md` - Relatório de validação

---

## 🎉 Divirta-se!

Fale naturalmente e deixe o Pi fazer o resto!

---

**Versão:** 2.0 - True Hands-Free
**Data:** 2026-04-06
**Status:** ✅ Funcional
