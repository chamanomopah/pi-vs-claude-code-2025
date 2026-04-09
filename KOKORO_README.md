# 🎙️ Kokoro-82M TTS - Guia Rápido de Instalação

Instale e use o melhor TTS local em 5 minutos!

## 🚀 Instalação Rápida (3 passos)

### 1. Instalar dependências

```bash
pip install -U kokoro-onnx soundfile
```

### 2. Baixar modelos (automático ou manual)

**Automático:** Na primeira execução, o Kokoro baixa os modelos automaticamente!

**Manual:** Baixe estes 2 arquivos e coloque na pasta do script:
- https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx (82MB)
- https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin (220MB)

### 3. Rodar o script

```bash
python kokoro_tts_simples.py
```

Resultado: `kokoro_audio.wav` criado! 🎉

---

## 📝 Exemplo de Código

```python
import soundfile as sf
from kokoro_onnx import Kokoro

# Seu texto
texto = "Hello! This is Kokoro-82M text-to-speech."

# Gerar áudio
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
samples, sample_rate = kokoro.create(
    texto,
    voice="af_heart",  # Voz feminina americana
    speed=1.0,         # Velocidade normal
    lang="en-us"       # Inglês americano
)

# Salvar
sf.write("audio.wav", samples, sample_rate)
print("✅ audio.wav criado!")
```

---

## 🎤 Vozes Recomendadas (Inglês)

### Feminino Americano ⭐
- `af_heart` - MELHOR qualidade (Grade A)
- `af_bella` - Excelente (Grade A-)
- `af_nicole` - Boa (Grade B-)

### Masculino Americano ⭐
- `am_michael` - MELHOR masculino (Grade C+)
- `am_fenrir` - Bom (Grade C+)
- `am_puck` - Bom (Grade C+)

### Britânico 🇬🇧
- `bf_emma` - Melhor feminina britânica
- `bm_george` - Bom masculino britânico

---

## ⚡ Requisitos

- Python: 3.10, 3.11, 3.12, ou 3.13
- RAM: 4GB mínimo
- CPU: Qualquer CPU moderno
- GPU: ❌ NÃO precisa

**Roda em Raspberry Pi!** 🎉

---

## 📊 Comparação com Outros TTS

| TTS | Tamanho | GPU? | Qualidade | Facilidade |
|-----|---------|------|-----------|------------|
| **Kokoro** | 80MB | ❌ | ⭐⭐⭐⭐⭐ | Muito Fácil |
| **XTTS v2** | 2GB | ✅ | ⭐⭐⭐⭐⭐ | Média |
| **Piper** | 100MB | ❌ | ⭐⭐⭐ | Muito Fácil |

---

## 🔗 Links Úteis

- **GitHub:** https://github.com/thewh1teagle/kokoro-onnx
- **Web Demo:** https://kokoroweb.app (ouça as vozes antes de usar)
- **PyPI:** https://pypi.org/project/kokoro-onnx/

---

## ⚠️ Troubleshooting Rápido

**Erro: ModuleNotFoundError**
```bash
pip install -U kokoro-onnx soundfile
```

**Erro: FileNotFoundError**
- Baixe os arquivos manualmente (veja passo 2)

**Erro: OSError (soundfile)**
```bash
# Linux
sudo apt-get install libsndfile1
# macOS
brew install libsndfile
# Windows
pip install soundfile
```

---

## 📁 Arquivos neste Guia

- `GUIA_KOKORO_SIMPLES.md` - Guia completo e detalhado
- `kokoro_tts_simples.py` - Script pronto para usar
- `kokoro_exemplo_vozes.py` - Exemplo com múltiplas vozes
- `KOKORO_README.md` - Este arquivo

---

## 🎉 Pronto!

Você tem um TTS de alta qualidade rodando localmente em 5 minutos!

**Próximos passos:**
1. ✅ Teste diferentes vozes
2. ✅ Ajuste a velocidade (speed=0.8 a 2.0)
3. ✅ Integre em seus projetos

---

**Guia criado em 09/04/2026 | Kokoro-82M v1.0 | Apache 2.0**
