# ComfyUI Automation Scripts

Scripts Python para automatizar workflows do ComfyUI.

## 📋 Requisitos

- ComfyUI rodando em `http://127.0.0.1:8188`
- Python 3.8+ (ou usar o Python embutido do ComfyUI)
- Bibliotecas: `requests`, `websockets`

## 🔧 Instalação

```bash
# Usar o Python embutido do ComfyUI
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\python_embeded\python.exe -m pip install requests websockets
```

Ou se tiver Python instalado:

```bash
pip install requests websockets
```

## 📁 Scripts Disponíveis

### 1. Kokoro TTS (`comfyui_kokoro_tts.py`)

Gera áudio a partir de texto usando o modelo Kokoro TTS.

```bash
python comfyui_kokoro_tts.py --text "Olá, mundo!" --speaker am_onyx --lang Portuguese --speed 1.0
```

**Parâmetros:**
- `--text, -t`: Texto para converter (obrigatório)
- `--speaker, -s`: Nome do speaker (padrão: am_onyx)
- `--speed`: Velocidade da fala (padrão: 1.0)
- `--lang, -l`: Idioma (padrão: Portuguese)
- `--no-save`: Não salvar o arquivo

---

### 2. Qwen TTS Clone (`comfyui_qwen_tts_clone.py`)

Clona voz a partir de um áudio de referência.

```bash
python comfyui_qwen_tts_clone.py --ref-audio minha_voz.wav --target-text "Texto para falar" --language Portuguese
```

**Parâmetros:**
- `--ref-audio, -r`: Caminho do áudio de referência (obrigatório)
- `--target-text, -t`: Texto para falar (obrigatório)
- `--ref-text`: Texto correspondente ao áudio de referência
- `--model`: Tamanho do modelo - 1.7B ou 0.6B (padrão: 1.7B)
- `--language, -l`: Idioma (padrão: Portuguese)
- `--seed`: Semente (padrão: 0 = random)
- `--temperature`: Temperatura (padrão: 1.0)
- `--no-save`: Não salvar o arquivo

---

### 3. Qwen TTS Custom (`comfyui_qwen_tts_custom.py`)

Usa vozes predefinidas do Qwen TTS.

```bash
python comfyui_qwen_tts_custom.py --text "Texto para converter" --speaker Serena --language Portuguese
```

**Parâmetros:**
- `--text, -t`: Texto para converter (obrigatório)
- `--speaker, -s`: Nome do speaker predefinido (padrão: Serena)
- `--instruct`: Instruções de estilo da voz
- `--model`: Tamanho do modelo - 1.7B ou 0.6B (padrão: 0.6B)
- `--language, -l`: Idioma (padrão: Portuguese)
- `--seed`: Semente (padrão: 0 = random)
- `--temperature`: Temperatura (padrão: 1.2)
- `--no-save`: Não salvar o arquivo

---

### 4. Qwen TTS Design (`comfyui_qwen_tts_design.py`)

Cria novas vozes com descrição detalhada.

```bash
python comfyui_qwen_tts_design.py --text "Texto para converter" --instruct "Descrição da voz desejada..."
```

**Parâmetros:**
- `--text, -t`: Texto para converter (obrigatório)
- `--instruct, -i`: Descrição detalhada do perfil de voz (obrigatório)
- `--model`: Tamanho do modelo - 1.7B ou 0.6B (padrão: 1.7B)
- `--language, -l`: Idioma (padrão: Portuguese)
- `--seed`: Semente (padrão: 0 = random)
- `--temperature`: Temperatura (padrão: 1.0)
- `--no-save`: Não salvar o arquivo

**Exemplo de instrução de voz:**

```
--instruct "Voice Profile: Deep baritone (85–110 Hz), textured and slightly raspy at low volume. Speech rhythm is deliberate and groove-based. Accent blends African American urban cadence with subtle West African tonal inflection. Delivery style: Calm authority like a documentary narrator, with subtle swagger. Emotional control—intensity comes from timing, not volume."
```

---

### 5. Z-Image-Turbo (`comfyui_z_image_turbo.py`)

Gera imagens usando o modelo Z-Image-Turbo.

```bash
python comfyui_z_image_turbo.py --prompt "um gato astronauta no espaço" --width 1920 --height 1088
```

**Parâmetros:**
- `--prompt, -p`: Prompt de texto (obrigatório)
- `--width, -W`: Largura da imagem (padrão: 1920)
- `--height, -H`: Altura da imagem (padrão: 1088)
- `--steps, -s`: Número de steps (padrão: 8)
- `--seed`: Semente (padrão: 0 = random)
- `--cfg`: CFG scale (padrão: 1.0)
- `--shift`: Shift para AuraFlow (padrão: 3.0)
- `--no-save`: Não salvar a imagem

---

### 6. LTX Video (`comfyui_ltx_video.py`)

Gera vídeos a partir de imagens ou texto usando o modelo LTX-2.3.

```bash
# Image-to-Video
python comfyui_ltx_video.py --prompt "A câmera se aproxima suavemente..." --image input.png --length 121

# Text-to-Video
python comfyui_ltx_video.py --prompt "Uma egípcia real caminha pelo deserto..." --text-to-video --length 121
```

**Parâmetros:**
- `--prompt, -p`: Descrição do movimento/cena (obrigatório)
- `--image, -i`: Caminho da imagem de entrada (opcional)
- `--negative, -n`: Negative prompt (padrão: "pc game, console game...")
- `--width, -W`: Largura do vídeo (padrão: 1280)
- `--height, -H`: Altura do vídeo (padrão: 720)
- `--length`: Duração em frames (padrão: 121)
- `--fps`: Frame rate (padrão: 25)
- `--text-to-video`: Gerar vídeo apenas do texto
- `--cfg`: CFG scale (padrão: 1.0)
- `--no-save`: Não salvar o vídeo

⚠️ **ATENÇÃO:** Geração de vídeo pode levar vários minutos!

---

## 📂 Organização de Outputs

Os scripts salvam os arquivos em:

```
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\user\outputs\
└── {YYYY-MM-DD}/
    ├── kokoro_tts/
    ├── qwen_tts_clone/
    ├── qwen_tts_custom/
    ├── qwen_tts_design/
    ├── z_image_turbo/
    └── ltx_video/
```

## 🔍 Troubleshooting

### Servidor não está rodando

```
ERRO: Servidor ComfyUI não está rodando em http://127.0.0.1:8188
```

**Solução:** Inicie o ComfyUI:
```
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\run_nvidia_gpu.bat
```

### Erro de importação

```
ModuleNotFoundError: No module named 'requests'
```

**Solução:**
```bash
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\python_embeded\python.exe -m pip install requests websockets
```

### Workflow falha

**Solução:**
1. Verifique se os modelos necessários estão instalados
2. Teste o workflow manualmente no ComfyUI
3. Confira o console do ComfyUI para mensagens de erro específicas

---

## 📚 Documentação Completa

Veja `docs/comfyui-automacao-personalizada.md` para documentação detalhada.

---

**Última atualização:** 20/04/2026
