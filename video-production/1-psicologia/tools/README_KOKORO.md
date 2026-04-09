# TTS Simples - Text to Speech

Script simples para converter texto em áudio. **Nota: Este script usa Edge TTS como alternativa estável e gratuita ao Kokoro-82M.**

## 📦 Instalação

### Windows

```bash
# Instalar dependências
pip install -r requirements_kokoro.txt

# Ou instalar manualmente
pip install edge-tts
```

### Linux/Mac

```bash
# Instalar dependências
pip3 install -r requirements_kokoro.txt

# Ou instalar manualmente
pip3 install edge-tts
```

## 🚀 Como Usar

### 1. Editar o Script

Abra o arquivo `kokoro_tts_simples.py` e edite as variáveis no topo:

```python
TEXTO = "Seu texto aqui"
VOZ = "af_heart"  # Escolha a voz (veja lista abaixo)
VELOCIDADE = 1.0  # Não usado no Edge TTS
ARQUIVO_SAIDA = "audio_kokoro.wav"
```

### 2. Executar

```bash
# Windows
python kokoro_tts_simples.py

# Linux/Mac
python3 kokoro_tts_simples.py
```

### 3. Reproduzir o Áudio

```bash
# Windows
start audio_kokoro.wav

# Mac
afplay audio_kokoro.wav

# Linux
aplay audio_kokoro.wav
```

## 🎤 Vozes Disponíveis

O script usa Edge TTS que possui **centenas de vozes** em diferentes idiomas e estilos. O script faz um mapeamento automático:

### Vozes Femininas Americanas (af_*)
| Voz | Voz Edge TTS Correspondente |
|-----|-----------|
| `af_heart` | en-US-AriaNeural (Natural) |
| `af_bella` | en-US-JennyNeural (Profissional) |

### Vozes Masculinas Americanas (am_*)
| Voz | Voz Edge TTS Correspondente |
|-----|-----------|
| `am_michael` | en-US-GuyNeural (Natural) |
| `am_adam` | en-US-BrandonNeural (Profissional) |

### Listar Todas as Vozes

Para ver todas as vozes disponíveis no Edge TTS:

```bash
edge-tts --list-voices
```

Ou filtrar por idioma:

```bash
edge-tts --list-voices | grep -i "pt-BR"  # Português Brasil
edge-tts --list-voices | grep -i "en-US"  # Inglês Americano
edge-tts --list-voices | grep -i "es-ES"  # Espanhol
```

## 📝 Vozes em Português

Exemplos de vozes em português brasileiro:

```python
# Voz direta (sem mapeamento)
VOZ = "pt-BR-FranciscaNeural"  # Feminina
VOZ = "pt-BR-AntonioNeural"    # Masculina
```

Edite o script para usar a voz diretamente:

```python
# No código, substitua:
voice_id = voz_map.get(VOZ, "en-US-AriaNeural")

# Por:
voice_id = VOZ  # Usa a voz diretamente
```

## ⚙️ Configurações

### Texto com Pontuação

```python
TEXTO = """Hello! This is a test.
Pause here...
And continue with more text."""
```

### Caracteres Especiais

```python
TEXTO = "Olá! Isso é um teste.  # Pausas com pontos finais"
```

### Múltiplos Parágrafos

```python
TEXTO = """
Primeiro parágrafo aqui.

Segundo parágrafo aqui.

Terceiro parágrafo aqui.
"""
```

## 🔄 Sobre o Kokoro-82M

O modelo **Kokoro-82M** é um excelente modelo TTS open-source com 82 milhões de parâmetros. No entanto:

- A biblioteca `kokoro-onnx` requer arquivos de vozes em formato específico
- Esses arquivos não estão publicamente disponíveis no formato correto
- O formato `.bin` do HuggingFace não é compatível com o kokoro-onnx

### Alternativas ao Kokoro-82M:

1. **Edge TTS** (usado neste script) - Grátis, funciona offline, muitas vozes
2. **Bark TTS** - Modelo open-source da Suno
3. **Coqui TTS** - 🐸 TTS, modelos open-source de alta qualidade
4. **OpenAI TTS** - API paga com qualidade excelente

## 💡 Dicas de Uso

### Mudar a Voz

```python
# Feminina americana - Natural
VOZ = "af_heart"

# Masculina americana - Natural
VOZ = "am_michael"

# Português brasileiro (edite o script para usar direto)
VOZ = "pt-BR-FranciscaNeural"
```

### Texto Longo

Para textos muito longos, divida em partes:

```python
TEXTO_PART1 = "Primeira parte do texto..."
# Gere audio1.wav

TEXTO_PART2 = "Segunda parte do texto..."
# Gere audio2.wav
```

### Background Music

Combine o áudio gerado com música de fundo usando ffmpeg:

```bash
ffmpeg -i audio_kokoro.wav -i background.mp3 -filter_complex amerge=inputs=2 -shortest output.wav
```

## 🔧 Solução de Problemas

### Erro: "No module named 'edge_tts'"

```bash
pip install edge-tts
```

### Erro: "AsyncIO loop is closed"

Este é um problema conhecido no Windows. Tente:

```python
# No script, troque:
asyncio.run(gerar_audio_edge())

# Por:
asyncio.new_event_loop().run_until_complete(gerar_audio_edge())
```

### Áudio com baixa qualidade

- Tente diferentes vozes
- Use textos com pontuação adequada para pausas naturais
- Ajuste o rate/pitch (edite o script para adicionar parâmetros ao Edge TTS)

### Erro com caracteres especiais

- Use codificação UTF-8 no arquivo Python
- Evite caracteres muito especiais ou emojis

## 📊 Comparação de TTS

| Serviço | Qualidade | Velocidade | Offline | Custo |
|---------|-----------|------------|---------|-------|
| **Edge TTS** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | 🆓 |
| Kokoro-82M | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | 🆓 |
| Bark | ⭐⭐⭐⭐ | ⭐ | ✅ | 🆓 |
| OpenAI TTS | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | 💰 |

## 📚 Recursos Adicionais

### Edge TTS

- **GitHub**: https://github.com/rany2/edge-tts
- **Vozes disponíveis**: 100+ vozes em 20+ idiomas
- **Formatos**: MP3, WAV, OPUS

### Outros Modelos TTS

**Bark:**
```bash
pip install bark
```

**Coqui TTS:**
```bash
pip install TTS
```

**OpenAI TTS:**
```bash
pip install openai
```

## 📄 Licença

Este script é fornecido como está para uso educacional e comercial.

---

**Dúvidas ou problemas?** Verifique a saída do script para mensagens de erro detalhadas e dicas de solução.
