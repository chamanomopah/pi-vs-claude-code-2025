# 📘 Guia Simples de Instalação do Kokoro-82M TTS

**Tempo estimado: 5 minutos**  
**Dificuldade:** Fácil  
**Custo:** $0 (100% gratuito)

---

## 🎯 O que é o Kokoro-82M?

O **Kokoro-82M** é um TTS (Text-to-Speech) local de código aberto que:

- ✅ **Leve:** Apenas 80MB (versão quantizada) ou 300MB (completo)
- ✅ **Rápido:** Real-time mesmo em CPU
- ✅ **Gratuito:** 100% gratuito e código aberto (Apache 2.0)
- ✅ **Comercial:** Pode usar em projetos comerciais
- ✅ **Privado:** Roda localmente, sem internet
- ✅ **Fácil:** Instala com um comando `pip`

**Qualidade:** ⭐⭐⭐⭐⭐ (Conquistou #1 no TTS Spaces Arena, superando XTTS v2!)

---

## 📋 REQUISITOS MÍNIMOS

### Hardware:
- **CPU:** Qualquer CPU moderno (Intel i3, AMD Ryzen, ou melhor)
- **RAM:** 4GB mínimo
- **GPU:** ❌ NÃO precisa de GPU!
- **Disco:** 500MB para os modelos

### Software:
- **Python:** 3.10, 3.11, 3.12, ou 3.13
- **Sistema:** Windows, macOS, ou Linux

**Roda em Raspberry Pi!** 🎉

---

## 🚀 PASSO 1: INSTALAÇÃO

### Opção A: Instalação Simples (Recomendada)

Abra seu terminal/comando e execute:

```bash
pip install -U kokoro-onnx soundfile
```

**Pronto!** É só isso. ✅

---

### Opção B: Instalação com Ambiente Virtual (Mais Isolado)

Se você quer manter as coisas organizadas:

```bash
# 1. Instalar uv (gerenciador de projetos Python)
pip install uv

# 2. Criar nova pasta para seu projeto
mkdir kokoro-tts
cd kokoro-tts

# 3. Inicializar projeto com Python 3.12
uv init -p 3.12

# 4. Adicionar kokoro-onnx
uv add kokoro-onnx soundfile

# 5. Criar seu script
nano hello.py  # ou use seu editor favorito
```

---

## 📥 PASSO 2: DOWNLOAD DOS MODELOS

O Kokoro precisa de 2 arquivos de modelo:

### Método Automático (Recomendado)

Na **primeira vez** que você rodar o Kokoro, ele fará download automático dos modelos! 🎉

### Método Manual (Se preferir)

Baixe os 2 arquivos e coloque na mesma pasta do seu script:

**Links diretos:**
1. **Modelo:** https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx (82MB)
2. **Vozes:** https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin (220MB)

**Estrutura de pastas:**
```
seu-projeto/
├── kokoro-v1.0.onnx      ← Modelo principal
├── voices-v1.0.bin        ← Arquivo de vozes
└── script.py              ← Seu script Python
```

---

## 💻 PASSO 3: SEU PRIMEIRO SCRIPT

Crie um arquivo chamado `meu_primeiro_tts.py` com este código:

```python
#!/usr/bin/env python3
"""
Kokoro-82M TTS - Script Simples
Converta texto em áudio em 3 linhas de código!
"""

# ─────────────────────────────────────
# CONFIGURAÇÃO - Edite aqui
# ─────────────────────────────────────

# Seu texto (pode ser várias linhas)
TEXTO = """
Hello! This is Kokoro-82M text-to-speech.
This is an example of converting text to audio using a local, 
open-source TTS model that runs entirely on your CPU.
"""

# Nome do arquivo de saída
ARQUIVO_SAIDA = "meu_audio.wav"

# Voz (veja lista completa abaixo)
VOZ = "af_heart"  # Voz feminina americana (melhor qualidade)

# Velocidade (1.0 = normal, 0.5 = mais lento, 2.0 = mais rápido)
VELOCIDADE = 1.0

# Idioma ("en-us" = inglês americano)
IDIOMA = "en-us"

# ─────────────────────────────────────
# CÓDIGO - Não precisa editar
# ─────────────────────────────────────

import soundfile as sf
from kokoro_onnx import Kokoro

print("🎙️  Kokoro-82M TTS")
print("=" * 50)
print(f"📝 Texto: {TEXTO[:50]}...")
print(f"🎤 Voz: {VOZ}")
print(f"⚡ Velocidade: {VELOCIDADE}")
print(f"🌐 Idioma: {IDIOMA}")
print()

# Inicializar Kokoro
print("⏳ Carregando modelo...")
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
print("✅ Modelo carregado!")

# Gerar áudio
print("🔊 Gerando áudio...")
samples, sample_rate = kokoro.create(
    TEXTO,
    voice=VOZ,
    speed=VELOCIDADE,
    lang=IDIOMA
)

# Salvar
sf.write(ARQUIVO_SAIDA, samples, sample_rate)
print(f"✅ Áudio salvo: {ARQUIVO_SAIDA}")
print(f"📊 Estatísticas:")
print(f"   - Sample rate: {sample_rate} Hz")
print(f"   - Duração: {len(samples) / sample_rate:.2f} segundos")
print(f"   - Samples: {len(samples):,}")
print()
print("🎉 Sucesso! Abra o arquivo para ouvir!")
```

---

## ▶️ PASSO 4: RODAR O SCRIPT

### Se usou instalação simples:

```bash
python meu_primeiro_tts.py
```

### Se usou ambiente virtual (uv):

```bash
uv run meu_primeiro_tts.py
```

**Resultado:** Um arquivo `meu_audio.wav` será criado! 🎉

---

## 🎤 VOZES DISPONÍVEIS PARA INGLÊS

### 🇺🇸 **Inglês Americano (Melhor Qualidade)**

| Voz | Gênero | Qualidade | Descrição |
|-----|--------|-----------|-----------|
| **af_heart** ⭐ | Feminino | **A** (Melhor!) | Doce, natural, **RECOMENDADA** |
| **af_bella** 🔥 | Feminino | **A-** | Profissional, excelente |
| af_nicole | Feminino | B- | Jovem, moderna |
| af_sarah | Feminino | C+ | Madura, calma |
| af_sky | Feminino | C- | Suave, sussurrante |
| af_aoede | Feminino | C+ | Equilibrada |
| af_alloy | Feminino | C | Padrão |
| af_kore | Feminino | C+ | Equilibrada |
| af_nova | Feminino | C | Padrão |
| af_river | Feminino | D | Padrão |
| af_jessica | Feminino | D | Padrão |
| **am_michael** ⭐ | Masculino | C+ | **Profissional, RECOMENDADO** |
| am_fenrir | Masculino | C+ | Profundo |
| am_puck | Masculino | C+ | Equilibrado |
| am_liam | Masculino | D | Jovem |
| am_echo | Masculino | D | Padrão |
| am_eric | Masculino | D | Padrão |
| am_onyx | Masculino | D | Profundo |
| am_adam | Masculino | F+ | Mais grave |
| am_santa | Masculino | D- | Natal (especial) |

### 🇬🇧 **Inglês Britânico**

| Voz | Gênero | Qualidade | Descrição |
|-----|--------|-----------|-----------|
| bf_emma | Feminino | B- | **Melhor britânica** |
| bf_isabella | Feminino | C | Padrão |
| bf_alice | Feminino | D | Padrão |
| bf_lily | Feminino | D | Padrão |
| bm_george | Masculino | C | Padrão |
| bm_fable | Masculino | C | Padrão |
| bm_daniel | Masculino | D | Padrão |
| bm_lewis | Masculino | D+ | Padrão |

### 🌎 **Outros Idiomas**

- 🇯🇵 **Japonês:** jf_alpha, jf_gongitsune, jf_nezumi, jf_tebukuro, jm_kumo
- 🇨🇳 **Chinês:** zf_xiaobei, zf_xiaoni, zm_yunxi, zm_yunxia, etc
- 🇪🇸 **Espanhol:** ef_dora, em_alex, em_santa
- 🇫🇷 **Francês:** ff_siwis
- 🇮🇳 **Hindi:** hf_alpha, hf_beta, hm_omega, hm_psi
- 🇮🇹 **Italiano:** if_sara, im_nicola
- 🇧🇷 **Português:** pf_dora, pm_alex, pm_santa

**Recomendação:** Use `af_heart` (feminino) ou `am_michael` (masculino) para melhor qualidade em inglês americano.

---

## 🧪 PASSO 5: TESTE RÁPIDO

Use este texto para teste:

```python
TEXTO = """
The quick brown fox jumps over the lazy dog.
This is a test of Kokoro-82M text-to-speech system.
The quality should be excellent and natural-sounding.
"""
```

**Resultado esperado:** Áudio claro, natural, com boa pronúncia e entonação.

---

## ⚠️ TROUBLESHOOTING (Solução de Problemas)

### Erro 1: `ModuleNotFoundError: No module named 'kokoro_onnx'`

**Causa:** Kokoro não foi instalado

**Solução:**
```bash
pip install -U kokoro-onnx soundfile
```

---

### Erro 2: `FileNotFoundError: kokoro-v1.0.onnx`

**Causa:** Arquivos de modelo não encontrados

**Solução:**
1. Baixe os arquivos manualmente (ver PASSO 2)
2. Coloque na MESMA pasta do script
3. Ou use caminho completo:
```python
kokoro = Kokoro("/caminho/completo/kokoro-v1.0.onnx", 
                "/caminho/completo/voices-v1.0.bin")
```

---

### Erro 3: `OSError: Unable to load soundfile library`

**Causa:** Biblioteca soundfile não está instalada

**Solução:**
```bash
# Windows
pip install soundfile

# Linux
sudo apt-get install libsndfile1
pip install soundfile

# macOS (com Homebrew)
brew install libsndfile
pip install soundfile
```

---

### Erro 4: Áudio muito rápido ou muito lento

**Causa:** Velocidade incorreta

**Solução:**
```python
# Ajuste o parâmetro speed
samples, sample_rate = kokoro.create(
    TEXTO,
    voice="af_heart",
    speed=1.0,  # ← Tente 0.8 (mais lento) ou 1.2 (mais rápido)
    lang="en-us"
)
```

---

### Erro 5: Voz soa robótica ou estranha

**Causa:** Voz de baixa qualidade ou idioma errado

**Solução:**
```python
# Use vozes de alta quali
