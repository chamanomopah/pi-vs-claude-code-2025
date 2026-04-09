# 📘 Guia Simples de Instalação do Kokoro-82M TTS

Tempo estimado: 5 minutos | Dificuldade: Fácil | Custo: $0

---

## 🎯 O que é Kokoro-82M?

TTS local de código aberto:
- ✅ Leve: 80MB (quantizado)
- ✅ Rápido: Real-time em CPU
- ✅ Gratuito: Apache 2.0 (uso comercial OK)
- ✅ Qualidade: ⭐⭐⭐⭐⭐ (#1 no TTS Spaces Arena)

---

## 📋 REQUISITOS

- Python: 3.10, 3.11, 3.12, ou 3.13
- RAM: 4GB mínimo
- CPU: Qualquer CPU moderno
- GPU: ❌ NÃO precisa

**Roda em Raspberry Pi!**

---

## 🚀 PASSO 1: INSTALAÇÃO

```bash
pip install -U kokoro-onnx soundfile
```

Pronto! Só isso.

---

## 📥 PASSO 2: DOWNLOAD DOS MODELOS

### Automático (Recomendado)
Na primeira execução, Kokoro baixa automaticamente!

### Manual (se preferir)
Baixe e coloque na pasta do seu script:
- Modelo: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx (82MB)
- Vozes: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin (220MB)

---

## 💻 PASSO 3: SCRIPT PYTHON

Crie `meu_tts.py`:

```python
import soundfile as sf
from kokoro_onnx import Kokoro

# SEU TEXTO AQUI
texto = "Hello! This is Kokoro-82M text-to-speech running on my CPU."

# Gerar áudio
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
samples, sample_rate = kokoro.create(
    texto,
    voice="af_heart",  # Melhor voz feminina
    speed=1.0,         # 1.0 = normal
    lang="en-us"       # Inglês americano
)

# Salvar
sf.write("audio.wav", samples, sample_rate)
print("✅ audio.wav criado com sucesso!")
```

---

## ▶️ PASSO 4: RODAR

```bash
python meu_tts.py
```

Resultado: `audio.wav` criado! 🎉

---

## 🎤 VOZES RECOMENDADAS (INGLÊS)

### Feminino (Americano)
- `af_heart` ⭐ - MELHOR (Grade A)
- `af_bella` 🔥 - Excelente (Grade A-)
- `af_nicole` - Boa (Grade B-)

### Masculino (Americano)
- `am_michael` ⭐ - MELHOR (Grade C+)
- `am_fenrir` - Bom (Grade C+)
- `am_puck` - Bom (Grade C+)

### Britânico
- `bf_emma` - Melhor feminina britânica
- `bm_george` - Bom masculino britânico

---

## 🧪 TESTE RÁPIDO

```python
texto = """
The quick brown fox jumps over the lazy dog.
This is a test of Kokoro-82M text-to-speech.
"""
```

---

## ⚠️ TROUBLESHOOTING

### Erro: ModuleNotFoundError
```bash
pip install -U kokoro-onnx soundfile
```

### Erro: FileNotFoundError
- Baixe os arquivos manualmente (PASSO 2)
- Coloque na MESMA pasta do script

### Erro: OSError (soundfile)
```bash
# Linux
sudo apt-get install libsndfile1

# macOS
brew install libsndfile

# Windows
pip install soundfile
```

### Áudio muito rápido/lento
```python
speed=0.8  # Mais lento
speed=1.2  # Mais rápido
```

### Voz robótica
```python
voice="af_heart"  # Use vozes de alta qualidade
```

---

## 📊 COMPARAÇÃO

| TTS | Tamanho | GPU? | Qualidade | Facilidade |
|-----|---------|------|-----------|------------|
| **Kokoro** | 80MB | ❌ | ⭐⭐⭐⭐⭐ | Muito Fácil |
| **XTTS v2** | 2GB | ✅ | ⭐⭐⭐⭐⭐ | Média |
| **StyleTTS 2** | 1.5GB | ✅ | ⭐⭐⭐⭐⭐ | Difícil |
| **Piper** | 100MB | ❌ | ⭐⭐⭐ | Muito Fácil |

**Vantagens Kokoro:**
- ✅ Mais leve (apenas 80MB)
- ✅ Qualidade superior (segundo benchmarks)
- ✅ Instalação simples (1 comando)
- ✅ Não precisa de GPU
- ✅ Uso comercial permitido

---

## 🔗 LINKS ÚTEIS

- GitHub: https://github.com/thewh1teagle/kokoro-onnx
- Web Demo: https://kokoroweb.app
- PyPI: https://pypi.org/project/kokoro-onnx/
- Lista de Vozes: https://huggingface.co/hexgrad/Kokoro-82M/raw/main/VOICES.md

---

## 📈 PERFORMANCE

Tempo de geração (CPU Intel i5):
- 10 segundos áudio → ~8 segundos geração
- 1 minuto áudio → ~45 segundos geração

**Real-time performance!** ⚡

---

## 🎉 PRONTO!

Você tem um TTS de alta qualidade rodando localmente!

**Próximos passos:**
1. Teste diferentes vozes
2. Ajuste a velocidade
3. Integre em seus projetos

Guia criado em 09/04/2026 | Kokoro-82M v1.0
