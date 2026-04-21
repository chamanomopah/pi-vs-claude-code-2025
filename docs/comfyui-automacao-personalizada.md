# ComfyUI - Documentação de Automação Personalizada

**Data:** 20 de Abril de 2026  
**Usuário:** JOSE  
**Setup:** Windows Portable

---

## 📋 Índice

1. [Setup do Usuário](#setup-do-usuário)
2. [Workflows Disponíveis](#workflows-disponíveis)
3. [Ambiente Python](#ambiente-python)
4. [Scripts de Automação](#scripts-de-automação)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ Setup do Usuário

### Caminhos do ComfyUI

```
ComfyUI Portable:
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI

Diretório User:
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\user

Workflows:
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\user\default\workflows

Outputs (Imagens):
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\user\outputs

Outputs (Áudio):
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\user\audio

Python:
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\python_embeded\python.exe
```

### Servidor

```
URL: http://127.0.0.1:8188
WebSocket: ws://127.0.0.1:8188/ws
```

---

## 🎨 Workflows Disponíveis

### 1. KOKORO - Text-to-Speech

**Arquivo:** `WORKFLOW - KOKORO.json`

**Tipo:** Geração de áudio (TTS)

**Descrição:** Gera áudio a partir de texto usando o modelo Kokoro TTS com diferentes vozes.

**Inputs:**
- `text` (STRING): Texto para converter em áudio
- `speaker` (COMBO): Voz do locutor (ex: "am_onyx")
- `speed` (FLOAT): Velocidade da fala (padrão: 1.0)
- `lang` (COMBO): Idioma (ex: "English", "Portuguese")

**Outputs:**
- Arquivo de áudio (.wav/.mp3)

**Nós principais:**
- `KokoroSpeaker`: Seleciona a voz
- `KokoroGenerator`: Gera o áudio
- `PreviewAudio`: Preview do áudio

**Exemplo de cURL:**

```bash
curl -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": {\"11\": {\"inputs\": {\"text\": \"Olá, isso é um teste.\", \"speed\": 1, \"lang\": \"Portuguese\"}, \"class_type\": \"KokoroGenerator\"}, \"10\": {\"inputs\": {\"speaker_name\": \"am_onyx\"}, \"class_type\": \"KokoroSpeaker\"}}, \"client_id\": \"curl_client\"}"
```

---

### 2. QWEN TTS - Text-to-Speech com Clonagem de Voz

**Arquivo:** `WORKFLOW - QWEN TTS.json`

**Tipo:** Geração de áudio com clonagem de voz

**Descrição:** Workflow avançado de TTS com 3 modos: clonagem de voz, vozes salvas e criação de novas vozes.

**Inputs:**

**Modo 1 - Clonagem de Voz:**
- `ref_audio` (AUDIO): Áudio de referência para clonagem
- `target_text` (STRING): Texto para falar com a voz clonada
- `ref_text` (STRING): Texto correspondente ao áudio de referência
- `model_choice` (COMBO): Tamanho do modelo (ex: "1.7B", "0.6B")
- `language` (COMBO): Idioma (ex: "Portuguese", "English")

**Modo 2 - Vozes Salvas:**
- `text` (STRING): Texto para converter
- `speaker` (COMBO): Voz predefinida (ex: "Serena")
- `instruct` (STRING): Instruções de estilo da voz
- `seed` (INT): Semente para reprodutibilidade

**Modo 3 - Criar Nova Voz:**
- `text` (STRING): Texto para converter
- `instruct` (STRING): Descrição detalhada do perfil de voz

**Outputs:**
- Arquivo de áudio (.mp3)

**Nós principais:**
- `FB_Qwen3TTSVoiceClone`: Clona voz a partir de áudio
- `FB_Qwen3TTSCustomVoice`: Usa vozes predefinidas
- `FB_Qwen3TTSVoiceDesign`: Cria nova voz com descrição
- `LoadAudio`: Carrega áudio de referência
- `SaveAudioMP3`: Salva áudio gerado

---

### 3. LTX Video - Image-to-Video

**Arquivo:** `WORKFLOW - video_ltx2_3_i2v.json`

**Tipo:** Geração de vídeo a partir de imagem

**Descrição:** Converte imagem estática em vídeo curto usando o modelo LTX-2.3 com áudio opcional.

**Inputs:**
- `image` (IMAGE): Imagem de entrada (opcional para text-to-video)
- `prompt` (STRING): Descrição do movimento/cena
- `negative_prompt` (STRING): Coisas a evitar
- `width` (INT): Largura do vídeo (padrão: 1280)
- `height` (INT): Altura do vídeo (padrão: 720)
- `length` (INT): Duração em frames (padrão: 121)
- `frame_rate` (INT): FPS (padrão: 25)
- `switch_to_text_to_video` (BOOLEAN): Se true, gera vídeo apenas do texto
- `cfg` (FLOAT): CFG scale (padrão: 1.0)

**Outputs:**
- Arquivo de vídeo (.mp4)

**Nós principais:**
- `CheckpointLoaderSimple`: Carrega modelo LTX-2.3
- `LTXVAudioVAELoader`: Carrega VAE de áudio
- `LoraLoaderModelOnly`: Carrega LoRA
- `CLIPTextEncode`: Codifica prompt
- `LTXVConditioning`: Conditioning para vídeo
- `SamplerCustomAdvanced`: Sampler para geração
- `VAEDecodeTiled`: Decodifica latent
- `CreateVideo`: Combina frames em vídeo

**Modelos necessários:**
- `ltx-2.3-22b-dev-fp8.safetensors` (checkpoint)
- `ltx-2.3-22b-distilled-lora-384.safetensors` (LoRA)
- `ltx-2.3-spatial-upscaler-x2-1.1.safetensors` (upscaler)
- `gemma_3_12B_it_fp4_mixed.safetensors` (text encoder)
- `gemma-3-12b-it-abliterated_lora_rank64_bf16.safetensors` (LoRA de texto)

---

### 4. Z-Image-Turbo - Text-to-Image

**Arquivo:** `WORKFLOW - Z-IMAGE-TURBO.json`

**Tipo:** Geração de imagem

**Descrição:** Gera imagens rapidamente usando o modelo Z-Image-Turbo.

**Inputs:**
- `text` (STRING): Prompt de texto
- `width` (INT): Largura (padrão: 1920)
- `height` (INT): Altura (padrão: 1088)
- `steps` (INT): Número de steps (padrão: 8)
- `unet_name` (COMBO): Modelo UNET
- `clip_name` (COMBO): Text encoder
- `vae_name` (COMBO): VAE

**Outputs:**
- Arquivo de imagem (.png)

**Nós principais:**
- `UNETLoader`: Carrega modelo UNET
- `CLIPLoader`: Carrega CLIP
- `VAELoader`: Carrega VAE
- `CLIPTextEncode`: Codifica prompt
- `ConditioningZeroOut`: Zera negative conditioning
- `EmptySD3LatentImage`: Cria latent vazio
- `KSampler`: Sampler
- `ModelSamplingAuraFlow`: Configura sampling
- `VAEDecode`: Decodifica para imagem
- `SaveImage`: Salva imagem

**Modelos necessários:**
- `z_image_turbo_bf16.safetensors` (diffusion model)
- `qwen_3_4b.safetensors` (text encoder)
- `ae.safetensors` (VAE)

**LoRA opcional:**
- `pixel_art_style_z_image_turbo.safetensors`

---

## 🐍 Ambiente Python

### Instalar Dependências

Usar o Python embutido do ComfyUI:

```bash
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\python_embeded\python.exe -m pip install requests websockets
```

Ou se já tiver pip configurado:

```bash
python -m pip install requests websockets
```

### Estrutura de Scripts

```
scripts/comfyui/
├── comfyui_kokoro_tts.py
├── comfyui_qwen_tts_clone.py
├── comfyui_qwen_tts_custom.py
├── comfyui_qwen_tts_design.py
├── comfyui_ltx_video.py
├── comfyui_z_image_turbo.py
└── utils.py
```

---

## 📜 Scripts de Automação

### Funções Utilitárias (utils.py)

```python
import requests
import websockets
import json
import asyncio
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib.parse

# Configurações
COMFYUI_SERVER = "http://127.0.0.1:8188"
COMFYUI_WS = "ws://127.0.0.1:8188/ws"
COMFYUI_BASE_PATH = Path(r"C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI")
WORKFLOWS_PATH = COMFYUI_BASE_PATH / "user" / "default" / "workflows"
OUTPUTS_PATH = COMFYUI_BASE_PATH / "user" / "outputs"
AUDIO_PATH = COMFYUI_BASE_PATH / "user" / "audio"


def load_workflow(workflow_name: str) -> Dict:
    """Carrega um workflow do diretório de workflows."""
    workflow_file = WORKFLOWS_PATH / workflow_name
    with open(workflow_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_output_dir(workflow_type: str, create: bool = True) -> Path:
    """Retorna o diretório de output organizado por data e tipo."""
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = OUTPUTS_PATH / today / workflow_type
    
    if create:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


async def queue_workflow(workflow: Dict, client_id: str = "python_client") -> str:
    """Envia um workflow para a fila do ComfyUI."""
    prompt_data = {
        "prompt": workflow,
        "client_id": client_id
    }
    
    response = requests.post(f"{COMFYUI_SERVER}/prompt", json=prompt_data)
    response.raise_for_status()
    
    data = response.json()
    if "prompt_id" in data:
        return data["prompt_id"]
    elif "error" in data:
        raise Exception(f"Erro ao enviar workflow: {data['error']}")
    else:
        raise Exception("Resposta inválida do servidor")


async def monitor_progress(prompt_id: str, client_id: str = "python_client") -> Dict:
    """Monitora o progresso do workflow via WebSocket."""
    uri = f"{COMFYUI_WS}?clientId={client_id}"
    
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                msg = json.loads(message)
                
                if msg.get("type") == "executing":
                    node_id = msg.get("data", {}).get("node")
                    if node_id is None:
                        # Execução completada
                        break
                
                elif msg.get("type") == "progress":
                    data = msg.get("data", {})
                    value = data.get("value", 0)
                    max_val = data.get("max", 100)
                    print(f"Progresso: {value}/{max_val}")
                
                elif msg.get("type") == "execution_error":
                    error_data = msg.get("data", {})
                    raise Exception(f"Erro na execução: {error_data}")
                
            except websockets.exceptions.ConnectionClosed:
                break
    
    # Aguardar um momento para o servidor processar
    await asyncio.sleep(1)
    
    # Obter resultados
    return get_history(prompt_id)


def get_history(prompt_id: str) -> Dict:
    """Obtém o histórico de execução de um prompt."""
    response = requests.get(f"{COMFYUI_SERVER}/history/{prompt_id}")
    response.raise_for_status()
    return response.json()


def extract_outputs(history: Dict) -> List[Dict]:
    """Extrai informações de outputs do histórico."""
    outputs = []
    
    for prompt_id, prompt_data in history.items():
        if "outputs" in prompt_data:
            for node_id, node_output in prompt_data["outputs"].items():
                if "images" in node_output:
                    for img in node_output["images"]:
                        outputs.append({
                            "type": "image",
                            "filename": img["filename"],
                            "subfolder": img.get("subfolder", ""),
                            "type_field": img.get("type", "output")
                        })
                
                if "audio" in node_output:
                    for audio in node_output["audio"]:
                        outputs.append({
                            "type": "audio",
                            "filename": audio["filename"],
                            "subfolder": audio.get("subfolder", ""),
                            "type_field": audio.get("type", "output")
                        })
    
    return outputs


def download_output(filename: str, subfolder: str = "", type_field: str = "output") -> bytes:
    """Baixa um arquivo de output do ComfyUI."""
    params = {
        "filename": filename,
        "subfolder": subfolder,
        "type": type_field
    }
    
    response = requests.get(f"{COMFYUI_SERVER}/view", params=params)
    response.raise_for_status()
    return response.content


def save_output(content: bytes, filename: str, output_dir: Path) -> Path:
    """Salva um arquivo de output no diretório especificado."""
    output_path = output_dir / filename
    with open(output_path, 'wb') as f:
        f.write(content)
    return output_path


async def run_workflow(
    workflow: Dict,
    workflow_name: str,
    client_id: str = "python_client",
    save_outputs: bool = True
) -> List[Path]:
    """Executa um workflow completo e baixa os outputs."""
    
    # Enviar workflow
    print(f"Enviando workflow '{workflow_name}'...")
    prompt_id = await queue_workflow(workflow, client_id)
    print(f"Prompt ID: {prompt_id}")
    
    # Monitorar progresso
    print("Monitorando execução...")
    history = await monitor_progress(prompt_id, client_id)
    
    # Extrair outputs
    outputs = extract_outputs(history)
    
    if not outputs:
        print("Nenhum output encontrado.")
        return []
    
    print(f"Found {len(outputs)} output(s)")
    
    # Baixar e salvar outputs
    saved_files = []
    if save_outputs:
        output_dir = get_output_dir(workflow_name)
        
        for output in outputs:
            print(f"Baixando {output['filename']}...")
            content = download_output(
                output["filename"],
                output["subfolder"],
                output["type_field"]
            )
            path = save_output(content, output["filename"], output_dir)
            saved_files.append(path)
            print(f"Salvo em: {path}")
    
    return saved_files


def upload_image(image_path: str) -> Dict:
    """Faz upload de uma imagem para o ComfyUI."""
    image_path = Path(image_path)
    
    files = {
        "image": (image_path.name, open(image_path, "rb"), "image/png")
    }
    data = {
        "type": "input"
    }
    
    try:
        response = requests.post(f"{COMFYUI_SERVER}/upload/image", files=files, data=data)
        response.raise_for_status()
        return response.json()
    finally:
        files["image"][1].close()


def upload_audio(audio_path: str) -> Dict:
    """Faz upload de um áudio para o ComfyUI."""
    audio_path = Path(audio_path)
    
    files = {
        "audio": (audio_path.name, open(audio_path, "rb"), "audio/wav")
    }
    data = {
        "type": "input"
    }
    
    try:
        response = requests.post(f"{COMFYUI_SERVER}/upload/audio", files=files, data=data)
        response.raise_for_status()
        return response.json()
    finally:
        files["audio"][1].close()
```

---

## 🎯 Exemplos de Uso

### Executar Script de Kokoro TTS

```bash
python scripts/comfyui/comfyui_kokoro_tts.py --text "Olá, mundo!" --speaker am_onyx --lang Portuguese --speed 1.0
```

### Executar Script de Qwen TTS (Clonagem)

```bash
python scripts/comfyui/comfyui_qwen_tts_clone.py --ref_audio minha_voz.wav --target_text "Texto para falar" --language Portuguese
```

### Executar Script de LTX Video

```bash
python scripts/comfyui/comfyui_ltx_video.py --image input.png --prompt "Descrição do movimento" --length 121
```

### Executar Script de Z-Image-Turbo

```bash
python scripts/comfyui/comfyui_z_image_turbo.py --prompt "um gato astronauta" --width 1920 --height 1088
```

---

## 🔧 Troubleshooting

### ComfyUI não está rodando

**Sintoma:** Connection refused ao tentar conectar

**Solução:**
1. Execute o ComfyUI:
   ```
   C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI\run_nvidia_gpu.bat
   ```

2. Aguarde a mensagem "Starting server"
3. Verifique se http://127.0.0.1:8188 está acessível no navegador

### Erro de importação

**Sintoma:** `ModuleNotFoundError: No module named 'requests'`

**Solução:**
```bash
C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\python_embeded\python.exe -m pip install requests websockets
```

### Workflow falha

**Sintoma:** Erro nos nós do workflow

**Solução:**
1. Verifique se todos os modelos necessários estão instalados
2. Abra o workflow no ComfyUI e teste manualmente
3. Verifique o console do ComfyUI para mensagens de erro específicas

### Outputs não aparecem

**Sintoma:** Script executa mas não baixa arquivos

**Solução:**
1. Verifique se o workflow tem nós de Save/SaveImage/SaveAudio
2. Confira o histórico: `curl http://127.0.0.1:8188/history/{prompt_id}`
3. Verifique permissões de escrita no diretório de outputs

---

## 📚 Referências

- **Documentação ComfyUI:** https://docs.comfy.org
- **API Reference:** https://docs.comfy.org/api
- **GitHub:** https://github.com/comfyanonymous/ComfyUI

---

**Última atualização:** 20/04/2026
