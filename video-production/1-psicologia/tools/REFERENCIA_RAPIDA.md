# Kokoro TTS - Referência Rápida

## 🚀 Comandos Essenciais

### Ativar Ambiente
```bash
conda activate kokoro
```

### Executar TTS
```bash
python kokoro_tts.py
```

### Listar Vozenhas
```bash
python kokoro_tts.py --vozes
```

### Wrappers
```bash
# Windows
run_kokoro.bat

# Linux/Mac
./run_kokoro.sh
```

---

## 📝 Variáveis de Configuração

No topo do arquivo `kokoro_tts.py`:

```python
TEXTO = "Seu texto aqui"
VOZ = "af_heart"        # af_heart, af_bella, am_adam, etc.
VELOCIDADE = 1.0         # 0.5 a 2.0 (1.0 = normal)
ARQUIVO_SAIDA = "audio_kokoro.wav"
```

---

## 🎤 Vozenhas Principais

| Código | Descrição |
|--------|-----------|
| `af_heart` | ❤️ **MELHOR** - Feminina, natural |
| `af_bella` | 🔥 Feminina, profissional |
| `af_sarah` | 👩 Feminina, madura |
| `am_adam` | 👨 Masculino |
| `am_michael` | 💼 Masculino, profissional |
| `bf_emma` | 🇬🇧 Britânica |

---

## 🔧 Instalação Rápida

```bash
# 1. Criar ambiente
conda create --name kokoro python=3.12 -y

# 2. Ativar
conda activate kokoro

# 3. Instalar dependências
pip install kokoro>=0.9.4 soundfile torch

# 4. Testar
python kokoro_tts.py
```

---

## 📂 Arquivos Importantes

| Arquivo | Propósito |
|---------|-----------|
| `kokoro_tts.py` | Script principal |
| `run_kokoro.bat` | Wrapper Windows |
| `run_kokoro.sh` | Wrapper Linux/Mac |
| `INSTALACAO_CONDAS.md` | Guia completo |
| `RESUMO_IMPLEMENTACAO.md` | Status da implementação |

---

## ⚡ Quick Copy-Paste

### Teste Simples
```python
from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code='a')
generator = pipeline("Hello world!", voice='af_heart', speed=1.0)

for gs, ps, audio in generator:
    sf.write("output.wav", audio, 24000)
    break
```

### Batch (Múltiplos Textos)
```python
texts = ["Hello", "World", "Test"]
for i, text in enumerate(texts):
    generator = pipeline(text, voice='af_heart')
    for gs, ps, audio in generator:
        sf.write(f"output_{i}.wav", audio, 24000)
        break
```

---

## 🐛 Problemas Comuns

| Erro | Solução |
|------|---------|
| `conda: command not found` | Instale Miniconda |
| `No module named 'kokoro'` | `pip install kokoro soundfile torch` |
| `UnicodeEncodeError` | Script já corrige (UTF-8) |
| `CUDA out of memory` | Kokoro usa CPU por padrão |

---

## 📊 Especificações Técnicas

- **Taxa de amostragem:** 24kHz
- **Formato:** WAV (PCM 16-bit)
- **Modelo:** Kokoro-82M (~2GB download)
- **Backend:** PyTorch
- **Python:** 3.12+

---

## 🎯 Casos de Uso

### Para Vídeos (YouTube)
```python
VOZ = "af_heart"  # Natural e envolvente
VELOCIDADE = 1.0   # Normal
```

### Para Audiobooks
```python
VOZ = "af_sarah"  # Madura e narrativa
VELOCIDADE = 0.95  # Ligeiramente lento
```

### Para Tutoriais
```python
VOZ = "am_michael"  # Profissional masculino
VELOCIDADE = 1.1    # Um pouco mais rápido
```

---

## 💡 Dicas

1. **Primeira execução:** Baixa ~2GB de modelos (seja paciente)
2. **Português:** Funciona, mas não é nativo (considere Edge TTS)
3. **Performance:** GPU não é necessária (CPU é suficiente)
4. **Qualidade:** 24kHz é qualidade de CD
5. **Batch:** Processe múltiplos áudios em paralelo para ganhar velocidade

---

**Status:** ✅ Produção
**Versão Kokoro:** 0.9.4
**Python:** 3.12.13
**Data:** 9 de abril de 2026
