# Scripts TTS - Text to Speech

Coleção de scripts para converter texto em áudio usando diferentes tecnologias.

## 📦 Scripts Disponíveis

### 1. **edge_tts_simple.py** ⭐ RECOMENDADO

**Melhor opção** para produção de vídeos.

**Vantagens:**
- ✅ Funciona em qualquer versão do Python (incluindo 3.13)
- ✅ Não requer download de modelos pesados
- ✅ Alta qualidade de voz (neural Microsoft Edge)
- ✅ Muitas vozes e idiomas disponíveis
- ✅ Leve e rápido
- ✅ GRATUITO

**Instalação:**
```bash
pip install edge-tts
```

**Uso:**
```bash
python edge_tts_simple.py
```

**Configuração:**
Edite as variáveis no topo do script:
```python
TEXTO = "Seu texto aqui"
VOZ = "en-US-AriaNeural"  # Ver lista abaixo
VELOCIDADE = "+0%"  # -10% a +10%
ARQUIVO_SAIDA = "audio.mp3"
```

**Vozes populares:**
- `en-US-AriaNeural` - Feminina americana (melhor) ⭐
- `en-US-JennyNeural` - Feminina americana (profissional)
- `en-US-GuyNeural` - Masculino americano
- `pt-BR-FranciscaNeural` - Feminina brasileira 🇧🇷
- `pt-BR-AntonioNeural` - Masculino brasileiro 🇧🇷

**Listar vozes:**
```bash
python edge_tts_simple.py --list-voices
# Para listar TODAS as vozes:
edge-tts --list-voices
```

---

### 2. **kokoro_tts.py** (PyTorch)

Modelo Kokoro-82M com backend PyTorch.

**Requisitos:**
- Python 3.8 a 3.12 (NÃO funciona com 3.13)
- 4GB RAM mínimo

**Instalação:**
```bash
pip install -r requirements_kokoro.txt
```

**Observações:**
- Baixa modelos automaticamente do HuggingFace (~82MB)
- 54 vozes em 8 idiomas
- Áudio em 24kHz WAV

**Vozes populares:**
- `af_heart` - Feminina americana (melhor) ⭐
- `af_bella` - Feminina americana (profissional)
- `am_michael` - Masculino americano

---

### 3. **kokoro_tts_onnx.py** (ONNX)

Modelo Kokoro-82M com backend ONNX.

**Instalação:**
```bash
pip install kokoro-onnx soundfile
```

**Observações:**
- Mais leve que a versão PyTorch
- Pode ter problemas de compatibilidade dependendo da versão do Python

---

## 🎯 Recomendação

**Para produção de vídeos do canal:**

Use o **`edge_tts_simple.py`** porque:

1. **Funciona garantidamente** - Sem problemas de dependência
2. **Alta qualidade** - Vozes neurais Microsoft Edge
3. **Rápido** - Gera áudio em segundos
4. **Simples** - Apenas edite as variáveis e rode
5. **Versátil** - Muitas vozes em vários idiomas

---

## 📝 Exemplos de Uso

### Vídeo em Inglês (Narração Americana Feminina)

```python
# No arquivo edge_tts_simple.py
TEXTO = """
Welcome to Psychology channel! In this video, we'll explore
the fascinating world of human behavior and the mind.

Subscribe for more content like this!
"""

VOZ = "en-US-AriaNeural"
ARQUIVO_SAIDA = "narracao_en.mp3"
```

### Vídeo em Português (Narração Brasileira Feminina)

```python
# No arquivo edge_tts_simple.py
TEXTO = """
Bem-vindo ao canal de Psicologia! Neste vídeo, vamos explorar
o fascinante mundo do comportamento humano e da mente.

Inscreva-se para mais conteúdo como este!
"""

VOZ = "pt-BR-FranciscaNeural"
ARQUIVO_SAIDA = "narracao_pt.mp3"
```

### Ajustar Velocidade

```python
# Lento para explicação detalhada
VELOCIDADE = "-10%"

# Normal
VELOCIDADE = "+0%"

# Rápido para resumos
VELOCIDADE = "+10%"
```

---

## 🛠️ Conversão de Formato

Se precisar converter MP3 para WAV (para edição de vídeo):

```bash
# Usando ffmpeg
ffmpeg -i audio.mp3 -acodec pcm_s16le -ar 24000 -ac 1 audio.wav

# Usando Python
from pydub import AudioSegment
audio = AudioSegment.from_mp3("audio.mp3")
audio.export("audio.wav", format="wav", parameters=["-ar", "24000"])
```

---

## 📚 Comparativo

| Script | Qualidade | Facilidade | Compatibilidade | Tamanho | Recomendado |
|--------|-----------|------------|-----------------|---------|-------------|
| edge_tts_simple.py | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Todas | 0 MB | ✅ SIM |
| kokoro_tts.py | ⭐⭐⭐⭐ | ⭐⭐⭐ | 3.8-3.12 | 82 MB | ❌ |
| kokoro_tts_onnx.py | ⭐⭐⭐⭐ | ⭐⭐⭐ | Variável | ~50 MB | ❌ |

---

## 🎧 Reproduzir Áudios

### Windows
```bash
start audio.mp3
```

### Linux
```bash
ffplay audio.mp3
# ou
mpg123 audio.mp3
```

### macOS
```bash
afplay audio.mp3
```

---

## 💡 Dicas

1. **Texto longo:** Use quebras de linha para criar pausas naturais
2. **Teste antes:** Gere um áudio de teste antes de processar o texto completo
3. **Backup:** Mantenha o áudio original em caso de precisar reeditar
4. **Metadados:** Considere adicionar informações ao nome do arquivo (ex: `cena01_en.mp3`)

---

## 🔧 Solução de Problemas

### edge_tts não funciona
```bash
# Reinstalar
pip uninstall edge-tts
pip install edge-tts
```

### Kokoro não funciona no Python 3.13
Use o **edge_tts_simple.py** em vez disso.

### Áudio muito baixo
```bash
# Normalizar com ffmpeg
ffmpeg -i input.mp3 -filter:a loudnorm output.mp3
```

---

## 📄 Licença

Os scripts são fornecidos como está para uso em projetos de produção de vídeos.

---

**Autor:** Assistant
**Data:** 2025-04-09
**Versão:** 1.0
