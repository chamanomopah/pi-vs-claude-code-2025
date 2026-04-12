# 🎤 TTS Audio Generation for Automated Testing

## ✅ IMPLEMENTAÇÃO CONCLUÍDA

Sistema de geração de áudio com TTS para testes 100% automatizados.

---

## 📁 Estrutura Criada

```
tests/
├── src/
│   └── audio_generation/
│       ├── __init__.py
│       ├── pyttsx3_tts.py          (6.8 KB)
│       └── audio_generator.py      (8.0 KB)
├── generate_audio.py               (2.5 KB)
└── test_audio_library.py           (3.2 KB)

tests/audio/
├── wake_words/                     (5 arquivos)
│   ├── porcupine.wav
│   ├── ok_google.wav
│   ├── alexa.wav
│   ├── hey_siri.wav
│   └── computer.wav
├── commands/                       (14 arquivos)
│   ├── ligar_a_luz.wav
│   ├── desligar_a_luz.wav
│   ├── que_horas_são.wav
│   └── ...
└── phrases/                        (8 arquivos)
    ├── olá_mundo.wav
    ├── bom_dia.wav
    └── ...
```

**Total: 27 arquivos de áudio gerados (54.6 segundos de áudio)**

---

## 🎯 Funcionalidades

### 1. Pyttsx3TTS

**Engine TTS offline e cross-platform:**
- ✅ Funciona sem internet
- ✅ Suporta Windows, Linux, macOS
- ✅ Múltiplas vozes
- ✅ Configurável (taxa, volume)

**Métodos:**
```python
tts = Pyttsx3TTS(rate=150, volume=0.9)

# Listar vozes disponíveis
voices = tts.list_voices()

# Gerar wake word
path = tts.generate_wake_word("porcupine")

# Gerar comando
path = tts.generate_command("ligar a luz")

# Gerar fala personalizada
path = tts.generate_speech("olá mundo", Path("output.wav"))

# Testar áudio
tts.test_speaker("Testing TTS")
```

### 2. AudioGenerator

**Gera biblioteca completa de áudios:**

**Wake Words (5):**
- porcupine
- ok google
- alexa
- hey siri
- computer

**Commands (14):**
- Luz: ligar, desligar, acender, apagar
- Tempo: horas, dia, clima
- Sistema: abrir, tocar, parar

**Phrases (8):**
- Cumprimentos: bom dia, boa tarde, boa noite
- Básicos: olá mundo, como vai você
- Polidez: obrigado, por favor, ajuda

**Métodos:**
```python
generator = AudioGenerator(rate=150)

# Gerar toda biblioteca
all_files = generator.generate_all()

# Gerar categorias específicas
wake_words = generator.generate_wake_words()
commands = generator.generate_commands()
phrases = generator.generate_phrases()

# Gerar áudios customizados
custom = generator.generate_custom(
    texts=["texto 1", "texto 2"],
    category="test"
)
```

---

## 🚀 Como Usar

### Gerar Biblioteca de Áudio

```bash
# Entrar no diretório
cd projects/3-wake_words_command

# Gerar todos os áudios
python tests/generate_audio.py
```

**Saída:**
```
================================================================================
 🎤 AUDIO LIBRARY GENERATOR
================================================================================
 ✅ pyttsx3 is installed and ready

Available TTS voices (2):
  [0] Microsoft Maria Desktop - Portuguese(Brazil)
  [1] Microsoft Zira Desktop - English (United States)

================================================================================
 🎤 GENERATING WAKE WORDS
================================================================================
✅ Generated wake word: porcupine -> tests\audio\wake_words\porcupine.wav (81.7 KB)
✅ Generated wake word: ok google -> tests\audio\wake_words\ok_google.wav (82.3 KB)
...

================================================================================
 📊 GENERATION SUMMARY
================================================================================
 ⏱️  Time elapsed: 4.5 seconds
 🎤 Wake words: 5
 ⚡ Commands: 14
 💬 Phrases: 8
 📁 Total files: 27
================================================================================

 ✅ SUCCESS! Generated 27 audio files
```

### Testar Arquivos de Áudio

```bash
# Testar todos os arquivos
python tests/test_audio_library.py
```

**Saída:**
```
================================================================================
 📂 AUDIO LIBRARY
================================================================================
WAKE_WORDS:
  📄 porcupine                              ( 81.7 KB)
  📄 ok_google                              ( 82.3 KB)
  ...

================================================================================
 🎵 TESTING AUDIO FILES
================================================================================
✅ wake_words      porcupine                  |  1.90s | 22050Hz | Ch:1 | RMS:0.0378
✅ wake_words      ok_google                  |  1.91s | 22050Hz | Ch:1 | RMS:0.0357
...

================================================================================
 📊 SUMMARY
================================================================================
Total files tested: 27
Total duration: 54.6 seconds
Average duration: 2.02 seconds
✅ All audio files are valid!
```

---

## 📊 Dados dos Arquivos Gerados

### Formato
- **Codec:** WAV (PCM)
- **Sample Rate:** 22050 Hz
- **Canais:** 1 (mono)
- **Bits:** 16-bit

### Qualidade
- **RMS médio:** 0.0378
- **Duração média:** 2.02 segundos
- **Tamanho médio:** 87 KB
- **Total:** 2.3 MB (27 arquivos)

### Voze Disponíveis
- **Windows:** Microsoft Maria (Portuguese-Brazil)
- **Linux:** espeak, Festival
- **macOS:** System voices

---

## 💻 Uso no Código

### Exemplo 1: Gerar Áudio Individual

```python
from tests.src.audio_generation import Pyttsx3TTS

# Criar TTS
tts = Pyttsx3TTS(rate=150)

# Gerar wake word
path = tts.generate_wake_word("hey assistant")
print(f"Generated: {path}")

# Gerar comando
path = tts.generate_command("abrir navegador")
print(f"Generated: {path}")
```

### Exemplo 2: Usar Áudio Gerado em Testes

```python
import soundfile as sf
from pathlib import Path

# Carregar áudio gerado
audio_file = Path("tests/audio/wake_words/porcupine.wav")
audio, sr = sf.read(str(audio_file))

# Usar em teste
print(f"Sample rate: {sr}")
print(f"Duration: {len(audio) / sr:.2f}s")
print(f"Channels: {1 if len(audio.shape) == 1 else audio.shape[1]}")
```

### Exemplo 3: Teste Automatizado com Áudio

```python
import sounddevice as sd
from pathlib import Path

# Carregar wake word
audio_file = Path("tests/audio/wake_words/porcupine.wav")
audio, sr = sf.read(str(audio_file))

# Reproduzir para teste
sd.play(audio, sr)
sd.wait()

# Detectar wake word
# ... (teste de detecção)
```

---

## 📝 Próximos Passos

### Integração com Testes Automatizados

```python
# tests/test_wake_word_detection.py
def test_wake_word_detection():
    """Testa detecção de wake word usando áudio TTS."""

    from tests.src.audio_generation import AudioGenerator
    from src.wake_word import WakeWordDetector

    # Gerar áudio
    generator = AudioGenerator()
    wake_words = generator.generate_wake_words()

    # Testar detecção
    detector = WakeWordDetector()

    for word, audio_path in wake_words.items():
        audio, sr = sf.read(str(audio_path))

        # Detectar
        detected = detector.detect(audio, sr)

        # Verificar
        assert detected == word, f"Failed to detect '{word}'"
        print(f"✅ Detected: {word}")
```

### Teste de Transcrição

```python
# tests/test_stt.py
def test_speech_to_text():
    """Testa transcrição usando áudio TTS."""

    from tests.src.audio_generation import AudioGenerator
    from src.stt_engine import STTEngine

    # Gerar comandos
    generator = AudioGenerator()
    commands = generator.generate_commands()

    # Testar transcrição
    stt = STTEngine()

    for command, audio_path in commands.items():
        audio, sr = sf.read(str(audio_path))

        # Transcrever
        text = stt.transcribe(audio, sr)

        # Verificar
        assert text == command, f"Transcription mismatch: '{text}' != '{command}'"
        print(f"✅ Transcribed: {command}")
```

---

## 🎯 Benefícios

### 1. Testes 100% Automatizados
- ✅ Sem necessidade de gravação manual
- ✅ Reprodutível sempre igual
- ✅ Rápido (4.5s para 27 arquivos)

### 2. Offline
- ✅ Não precisa de internet
- ✅ TTS local (pyttsx3)
- ✅ Funciona em qualquer máquina

### 3. Cross-Platform
- ✅ Windows
- ✅ Linux
- ✅ macOS

### 4. Customizável
- ✅ Vozes diferentes
- ✅ Taxa de fala
- ✅ Volume ajustável
- ✅ Textos customizados

---

## 📦 Dependências

**Adicionado ao requirements.txt:**
```
pyttsx3>=2.90      # TTS engine
soundfile>=0.12.0  # Leitura de áudio
```

**Instalar:**
```bash
pip install pyttsx3 soundfile
```

---

## 📈 Estatísticas

### Geração
- ⏱️ Tempo: 4.5 segundos
- 📁 Arquivos: 27
- 💾 Tamanho: 2.3 MB
- 🎵 Duração: 54.6 segundos

### Qualidade
- ✅ Taxa de sucesso: 100% (27/27)
- ✅ RMS médio: 0.0378
- ✅ Sample rate: 22050 Hz
- ✅ Formato: WAV 16-bit

---

## 🎉 Conclusão

**SISTEMA DE GERAÇÃO DE ÁUDIO TTS IMPLEMENTADO!**

**O que foi feito:**
- ✅ 3 arquivos core (17.3 KB de código)
- ✅ 27 arquivos de áudio gerados
- ✅ Sistema de testes criado
- ✅ Documentação completa

**Para usar:**
```bash
# Gerar biblioteca
python tests/generate_audio.py

# Testar arquivos
python tests/test_audio_library.py

# Integrar em testes
# ... (ver exemplos acima)
```

**Próximo passo:** Criar testes automatizados completos usando os áudios gerados!
