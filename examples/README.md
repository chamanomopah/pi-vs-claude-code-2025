# Exemplos Práticos - ComfyUI Automation

Este diretório contém exemplos práticos e completos para automação de workflows do ComfyUI usando **KOKORO TTS** e **Z-IMAGE-TURBO**.

## 📋 Sumário

- [KOKORO TTS - Text to Speech](#kokoro-tts)
- [Z-IMAGE-TURBO - Text to Image](#z-image-turbo)
- [Requisitos](#requisitos)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Uso Rápido](#uso-rápido)

---

## 🎤 KOKORO TTS

Workflow para geração de áudio a partir de texto usando o modelo Kokoro TTS.

### Exemplos Disponíveis

#### 📝 Exemplo 1: Texto Simples

Gera um áudio a partir de um texto simples em português.

**Arquivos:**
- `kokoro_tts/exemplo1_curl_simple.sh` - Versão cURL/bash
- `kokoro_tts/exemplo1_python_simple.py` - Versão Python

**O que faz:**
- Envia texto "Olá, mundo! Este é um teste de automação do Kokoro TTS."
- Usa speaker `am_onyx`
- Velocidade normal (1.0)
- Baixa automaticamente o áudio gerado

**Uso:**
```bash
# Versão cURL
bash examples/kokoro_tts/exemplo1_curl_simple.sh

# Versão Python
python examples/kokoro_tts/exemplo1_python_simple.py
```

---

#### 📚 Exemplo 2: Batch de Textos

Processa múltiplos textos em sequência, gerando um áudio para cada um.

**Arquivos:**
- `kokoro_tts/exemplo2_curl_batch.sh` - Versão cURL/bash
- `kokoro_tts/exemplo2_python_batch.py` - Versão Python

**O que faz:**
- Processa 3 textos diferentes
- Gera 3 arquivos de áudio separados
- Salva com nomes organizados
- Mostra progresso de cada geração

**Uso:**
```bash
# Versão cURL
bash examples/kokoro_tts/exemplo2_curl_batch.sh

# Versão Python
python examples/kokoro_tts/exemplo2_python_batch.py
```

---

#### 🎵 Exemplo 3: Upload de Áudio de Referência

Demonstra como fazer upload de áudio para referência (voice cloning).

**Arquivos:**
- `kokoro_tts/exemplo3_curl_upload.sh` - Versão cURL/bash
- `kokoro_tts/exemplo3_python_upload.py` - Versão Python

**O que faz:**
- Faz upload de um áudio de referência
- **NOTA:** O workflow KOKORO atual usa speakers pré-definidos
- Este exemplo demonstra a estrutura necessária para voice cloning

**Uso:**
```bash
# Com áudio de referência (cURL)
bash examples/kokoro_tts/exemplo3_curl_upload.sh /caminho/do/audio.wav

# Com áudio de referência (Python)
python examples/kokoro_tts/exemplo3_python_upload.py /caminho/do/audio.wav

# Sem áudio (demonstração)
python examples/kokoro_tts/exemplo3_python_upload.py
```

**⚠️ Nota Importante:**
O workflow KOKORO atual usa speakers pré-definidos (`am_onyx`, `am_michael`, etc.). Para clonagem real de voz, você precisaria de um workflow específico com nós adicionais para extrair o embedding da voz do áudio de referência.

---

## 🖼️ Z-IMAGE-TURBO

Workflow para geração de imagens a partir de texto usando Z-Image-Turbo (modelo rápido de difusão).

### Exemplos Disponíveis

#### ✏️ Exemplo 1: Texto para Imagem Simples

Gera uma imagem a partir de um prompt de texto simples.

**Arquivos:**
- `zimage_turbo/exemplo1_curl_simple.sh` - Versão cURL/bash
- `zimage_turbo/exemplo1_python_simple.py` - Versão Python

**O que faz:**
- Gera imagem do prompt: "Um gato astronauta flutuando no espaço..."
- Dimensões: 1024x1024
- Steps: 8 (rápido)
- Baixa automaticamente a imagem gerada

**Uso:**
```bash
# Versão cURL
bash examples/zimage_turbo/exemplo1_curl_simple.sh

# Versão Python
python examples/zimage_turbo/exemplo1_python_simple.py
```

---

#### 🎨 Exemplo 2: Variações de Prompt (Batch)

Gera múltiplas imagens a partir de uma lista de prompts diferentes.

**Arquivos:**
- `zimage_turbo/exemplo2_curl_batch.sh` - Versão cURL/bash
- `zimage_turbo/exemplo2_python_batch.py` - Versão Python

**O que faz:**
- Processa 3 prompts diferentes
- Gera 3 imagens separadas
- Cada prompt usa uma seed aleatória para variação
- Salva com nomes organizados

**Uso:**
```bash
# Versão cURL
bash examples/zimage_turbo/exemplo2_curl_batch.sh

# Versão Python
python examples/zimage_turbo/exemplo2_python_batch.py
```

---

#### 🖼️ Exemplo 3: Upload de Imagem + img2img

Demonstra como fazer upload de imagem para Image-to-Image.

**Arquivos:**
- `zimage_turbo/exemplo3_curl_img2img.sh` - Versão cURL/bash
- `zimage_turbo/exemplo3_python_img2img.py` - Versão Python

**O que faz:**
- Faz upload de uma imagem de referência
- **NOTA:** O workflow Z-IMAGE-TURBO atual é Text-to-Image
- Este exemplo demonstra a estrutura necessária para img2img

**Uso:**
```bash
# Com imagem de referência (cURL)
bash examples/zimage_turbo/exemplo3_curl_img2img.sh /caminho/da/imagem.jpg

# Com imagem de referência (Python)
python examples/zimage_turbo/exemplo3_python_img2img.py /caminho/da/imagem.jpg

# Sem imagem (demonstração)
python examples/zimage_turbo/exemplo3_python_img2img.py
```

**⚠️ Nota Importante:**
O workflow Z-IMAGE-TURBO atual é Text-to-Image puro. Para Image-to-Image real, você precisaria adicionar nós:
- `LoadImage`: Carregar a imagem de entrada
- `VAEEncode` ou `ImageToLatent`: Converter para latente
- `KSampler` com `denoise < 1.0` (ex: 0.7 preserva características da imagem original)

---

## 📦 Requisitos

### Geral

- **ComfyUI** rodando em `http://127.0.0.1:8188`
- Windows (paths configurados para Windows)
- **Para scripts Python:**
  - Python 3.8+
  - Bibliotecas: `requests`, `websockets`

### Para KOKORO TTS

- ComfyUI-Kokoro instalado
- Modelos do Kokoro TTS baixados

### Para Z-IMAGE-TURBO

- Z-Image-Turbo instalado
- Modelos necessários em `ComfyUI/models/`:
  - `diffusion_models/z_image_turbo_bf16.safetensors`
  - `text_encoders/qwen_3_4b.safetensors`
  - `vae/ae.safetensors`

---

## 📂 Estrutura de Arquivos

```
examples/
├── kokoro_tts/
│   ├── exemplo1_curl_simple.sh          # cURL: Texto simples
│   ├── exemplo1_python_simple.py        # Python: Texto simples
│   ├── exemplo2_curl_batch.sh           # cURL: Batch de textos
│   ├── exemplo2_python_batch.py         # Python: Batch de textos
│   ├── exemplo3_curl_upload.sh          # cURL: Upload de áudio
│   └── exemplo3_python_upload.py        # Python: Upload de áudio
├── zimage_turbo/
│   ├── exemplo1_curl_simple.sh          # cURL: Texto para imagem
│   ├── exemplo1_python_simple.py        # Python: Texto para imagem
│   ├── exemplo2_curl_batch.sh           # cURL: Batch de prompts
│   ├── exemplo2_python_batch.py         # Python: Batch de prompts
│   ├── exemplo3_curl_img2img.sh         # cURL: Upload img2img
│   └── exemplo3_python_img2img.py       # Python: Upload img2img
├── scripts/
│   └── comfyui/
│       ├── utils.py                     # Funções utilitárias
│       ├── comfyui_kokoro_tts.py        # Script principal Kokoro
│       └── comfyui_z_image_turbo.py     # Script principal Z-Image
└── README.md                            # Este arquivo
```

---

## 🚀 Uso Rápido

### Verificar ComfyUI

Antes de executar os exemplos, verifique se o ComfyUI está rodando:

```bash
# Testar conexão
curl http://127.0.0.1:8188/system_stats

# Ou via Python
python -c "import requests; print(requests.get('http://127.0.0.1:8188/system_stats').status_code)"
```

### Executar Exemplos

#### Via cURL/bash

```bash
# KOKORO TTS - Exemplo 1
cd examples/kokoro_tts
bash exemplo1_curl_simple.sh

# Z-IMAGE-TURBO - Exemplo 1
cd examples/zimage_turbo
bash exemplo1_curl_simple.sh
```

#### Via Python

```bash
# KOKORO TTS - Exemplo 1
python examples/kokoro_tts/exemplo1_python_simple.py

# Z-IMAGE-TURBO - Exemplo 1
python examples/zimage_turbo/exemplo1_python_simple.py
```

---

## 📁 Localização dos Outputs

Os arquivos gerados são salvos em:

```
ComfyUI/user/outputs/
└── YYYY-MM-DD/           # Data de geração
    ├── kokoro_tts/
    │   ├── exemplo1_simples/
    │   ├── exemplo2_batch/
    │   └── exemplo3_upload/
    └── zimage_turbo/
        ├── exemplo1_simples/
        ├── exemplo2_batch/
        └── exemplo3_img2img/
```

---

## 🛠️ Personalização

### Modificar Textos/Prompts

Edite os arrays de textos/prompts dentro dos arquivos:

**cURL/bash:**
```bash
declare -a TEXTOS=(
  "Seu texto 1 aqui"
  "Seu texto 2 aqui"
  "Seu texto 3 aqui"
)
```

**Python:**
```python
textos = [
    "Seu texto 1 aqui",
    "Seu texto 2 aqui",
    "Seu texto 3 aqui"
]
```

### Modificar Parâmetros

**KOKORO TTS:**
- `speaker`: Nome do speaker (`am_onyx`, `am_michael`, etc)
- `speed`: Velocidade (0.5 = lento, 1.0 = normal, 2.0 = rápido)
- `lang`: Idioma (`Portuguese`, `English`, `Spanish`, etc)

**Z-IMAGE-TURBO:**
- `width`: Largura da imagem (512, 1024, 1920, etc)
- `height`: Altura da imagem
- `steps`: Steps de difusão (4 = rápido, 8 = equilíbrio, 16 = qualidade)
- `seed`: Semente para geração determinística

---

## 🐛 Troubleshooting

### ComfyUI não responde

```bash
# Verificar se está rodando
curl http://127.0.0.1:8188/system_stats

# Se não responder, inicie o ComfyUI:
# Windows: run_nvidia_gpu.bat ou run_cpu.bat
```

### Modelos não encontrados

Verifique se os modelos estão nos diretórios corretos:
```
ComfyUI/models/
├── diffusion_models/z_image_turbo_bf16.safetensors
├── text_encoders/qwen_3_4b.safetensors
└── vae/ae.safetensors
```

### Erro de permissão (Linux/Mac)

```bash
chmod +x examples/kokoro_tts/*.sh
chmod +x examples/zimage_turbo/*.sh
```

### Python: Módulos faltando

```bash
pip install requests websockets
```

---

## 📚 Referências

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI-Kokoro](https://github.com/remsky/Kokoro-FastAPI)
- [Z-Image-Turbo](https://huggingface.co/Comfy-Org/z_image_turbo)

---

## 📝 Notas

- Todos os scripts usam **WebSocket** para monitoramento em tempo real
- Downloads automáticos de outputs estão implementados
- Scripts são **copiar e colar** - prontos para uso
- Paths estão configurados para **Windows** (ajuste para Linux/Mac se necessário)

---

**Criado para automação completa de workflows ComfyUI** 🚀
