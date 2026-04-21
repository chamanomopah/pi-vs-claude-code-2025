# Análise e Automação ComfyUI - RESUMO EXECUTIVO

**Data:** 20 de Abril de 2026  
**Usuário:** JOSE  
**Status:** ✅ Completado

---

## 📊 O que foi analisado

### Workflows Encontrados

Foram identificados **4 workflows** no diretório do ComfyUI:

1. **KOKORO TTS** - Texto para áudio
   - Gera áudio com diferentes vozes
   - Suporte a múltiplos idiomas
   - Ajuste de velocidade

2. **QWEN TTS** - Texto para áudio avançado
   - **3 modos:** Clonagem de voz, vozes salvas, criar novas vozes
   - Suporte a português
   - Controle detalhado de parâmetros

3. **LTX Video** - Imagem para vídeo
   - Converte imagem estática em vídeo
   - Modelos LTX-2.3
   - Áudio opcional
   - Text-to-Video também disponível

4. **Z-Image-Turbo** - Texto para imagem
   - Geração rápida de imagens
   - Alta resolução (1920x1088)
   - Modelo de última geração

---

## 🎯 O que foi criado

### Documentação

**Arquivo:** `docs/comfyui-automacao-personalizada.md`

Contém:
- Configuração completa do setup do usuário
- Descrição detalhada de cada workflow
- Exemplos de cURL para todos os workflows
- Guide de troubleshooting
- Referências de modelos necessários

### Scripts de Automação

**Diretório:** `scripts/comfyui/`

#### Arquivo: `utils.py` (Funções utilitárias)

Funções disponíveis:
- `load_workflow()` - Carrega workflow JSON
- `queue_workflow()` - Envia workflow para fila
- `monitor_progress()` - Monitora via WebSocket
- `run_workflow()` - Executa workflow completo
- `upload_image()` - Upload de imagem
- `upload_audio()` - Upload de áudio
- `download_output()` - Baixa outputs
- `check_server()` - Verifica servidor
- `get_queue_info()` - Informações da fila
- E mais...

#### Scripts por Workflow:

1. **`comfyui_kokoro_tts.py`**
   ```bash
   python comfyui_kokoro_tts.py --text "Olá, mundo!" --speaker am_onyx --lang Portuguese
   ```

2. **`comfyui_qwen_tts_clone.py`**
   ```bash
   python comfyui_qwen_tts_clone.py --ref-audio voz.wav --target-text "Texto" --language Portuguese
   ```

3. **`comfyui_qwen_tts_custom.py`**
   ```bash
   python comfyui_qwen_tts_custom.py --text "Texto" --speaker Serena --language Portuguese
   ```

4. **`comfyui_qwen_tts_design.py`**
   ```bash
   python comfyui_qwen_tts_design.py --text "Texto" --instruct "Descrição da voz..."
   ```

5. **`comfyui_z_image_turbo.py`**
   ```bash
   python comfyui_z_image_turbo.py --prompt "um gato astronauta" --width 1920 --height 1088
   ```

6. **`comfyui_ltx_video.py`**
   ```bash
   # Image-to-Video
   python comfyui_ltx_video.py --prompt "Câmera se aproxima..." --image foto.png --length 121
   
   # Text-to-Video
   python comfyui_ltx_video.py --prompt "Uma egípcia real..." --text-to-video
   ```

6. **`README.md`**
   - Documentação de todos os scripts
   - Exemplos de uso
   - Troubleshooting

---

## 📁 Estrutura de Arquivos Criada

```
docs/
└── comfyui-automacao-personalizada.md    # Documentação completa (15KB)

scripts/comfyui/
├── utils.py                              # Funções utilitárias (13KB)
├── comfyui_kokoro_tts.py                 # Kokoro TTS (4KB)
├── comfyui_qwen_tts_clone.py             # Qwen Clone (7KB)
├── comfyui_qwen_tts_custom.py            # Qwen Custom (6KB)
├── comfyui_qwen_tts_design.py            # Qwen Design (5KB)
├── comfyui_z_image_turbo.py              # Z-Image (7KB)
├── comfyui_ltx_video.py                  # LTX Video (9KB)
└── README.md                             # Guia dos scripts (6KB)

Total: ~72KB de código e documentação
```

---

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\python_embeded\python.exe -m pip install requests websockets
```

### 2. Iniciar ComfyUI

```bash
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\run_nvidia_gpu.bat
```

### 3. Executar Script

```bash
# Exemplo: Gerar áudio com Kokoro
python scripts/comfyui/comfyui_kokoro_tts.py --text "Olá, mundo!" --speaker am_onyx --lang Portuguese

# Exemplo: Gerar imagem com Z-Image
python scripts/comfyui/comfyui_z_image_turbo.py --prompt "um gato astronauta"

# Exemplo: Gerar vídeo com LTX
python scripts/comfyui/comfyui_ltx_video.py --prompt "Câmera se aproxima" --image foto.png
```

---

## 📋 Caminhos Configurados

Todos os scripts usam os caminhos do usuário:

```
ComfyUI: C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI
Servidor: http://127.0.0.1:8188
Workflows: user\default\workflows\
Outputs: user\outputs\{data}\{workflow_tipo}\
```

---

## 🎨 Características dos Scripts

### ✅ Recursos Implementados

- **WebSocket monitoring:** Progresso em tempo real
- **Upload automático:** Imagens e áudios
- **Download automático:** Outputs organizados por data
- **Tratamento de erros:** Mensagens claras
- **Argumentos CLI:** Fácil de usar
- **Docstrings:** Documentação embutida
- **Caminhos Windows:** Raw strings para compatibilidade

### 📊 Organização de Outputs

```
user/outputs/
└── 2026-04-20/
    ├── kokoro_tts/
    ├── qwen_tts_clone/
    ├── qwen_tts_custom/
    ├── qwen_tts_design/
    ├── z_image_turbo/
    └── ltx_video/
```

---

## 🔮 Próximos Passos

### Integração com n8n

Com os scripts Python prontos, você pode:

1. **Criar workflows n8n** que chamam esses scripts
2. **Usar HTTP Request node** para chamar a API do ComfyUI diretamente
3. **Automatizar batch processing** de múltiplas gerações
4. **Integrar com Telegram/HTTP** para triggers externos

### Exemplo de uso no n8n:

```
Webhook → Python Script → Download → Upload para Google Drive
```

---

## 📚 Referências

- **Documentação completa:** `docs/comfyui-automacao-personalizada.md`
- **Guia dos scripts:** `scripts/comfyui/README.md`
- **Documentação ComfyUI:** https://docs.comfy.org
- **GitHub:** https://github.com/comfyanonymous/ComfyUI

---

## ✅ Status

- [x] Análise de workflows completada
- [x] Documentação personalizada criada
- [x] Scripts Python criados para todos os workflows
- [x] README com exemplos de uso
- [x] Funções utilitárias implementadas
- [x] Organização de outputs por data
- [x] Tratamento de erros
- [x] Suporte a caminhos Windows

**Pronto para usar! 🎉**
