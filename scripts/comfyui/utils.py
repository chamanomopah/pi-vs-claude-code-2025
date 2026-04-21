"""
ComfyUI Utility Functions
Funções utilitárias para automação do ComfyUI
"""

import requests
import websockets
import json
import asyncio
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib.parse

# Configurações do ComfyUI
COMFYUI_SERVER = "http://127.0.0.1:8188"
COMFYUI_WS = "ws://127.0.0.1:8188/ws"

# Caminhos do sistema (Windows - usar raw strings)
COMFYUI_BASE_PATH = Path(r"C:\Users\JOSE\Downloads\confyui\ComfyUI_windows_portable\ComfyUI")
WORKFLOWS_PATH = COMFYUI_BASE_PATH / "user" / "default" / "workflows"
OUTPUTS_PATH = COMFYUI_BASE_PATH / "user" / "outputs"
AUDIO_PATH = COMFYUI_BASE_PATH / "user" / "audio"


def load_workflow(workflow_name: str) -> Dict:
    """
    Carrega um workflow do diretório de workflows.
    
    Args:
        workflow_name: Nome do arquivo JSON do workflow
        
    Returns:
        Dicionário com o workflow carregado
    """
    workflow_file = WORKFLOWS_PATH / workflow_name
    if not workflow_file.exists():
        raise FileNotFoundError(f"Workflow não encontrado: {workflow_file}")
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_output_dir(workflow_type: str, create: bool = True) -> Path:
    """
    Retorna o diretório de output organizado por data e tipo.
    
    Args:
        workflow_type: Nome do tipo de workflow (ex: 'kokoro_tts', 'ltx_video')
        create: Se True, cria o diretório se não existir
        
    Returns:
        Path do diretório de output
    """
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = OUTPUTS_PATH / today / workflow_type
    
    if create:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


async def queue_workflow(workflow: Dict, client_id: str = "python_client") -> str:
    """
    Envia um workflow para a fila do ComfyUI.
    
    Args:
        workflow: Dicionário do workflow
        client_id: ID do cliente para identificar a conexão
        
    Returns:
        prompt_id: ID do prompt enfileirado
    """
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
    elif "node_errors" in data and data["node_errors"]:
        raise Exception(f"Erros nos nós: {data['node_errors']}")
    else:
        raise Exception("Resposta inválida do servidor")


async def monitor_progress(prompt_id: str, client_id: str = "python_client") -> Dict:
    """
    Monitora o progresso do workflow via WebSocket.
    
    Args:
        prompt_id: ID do prompt a monitorar
        client_id: ID do cliente para conexão WebSocket
        
    Returns:
        Histórico da execução
    """
    uri = f"{COMFYUI_WS}?clientId={client_id}"
    
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                msg = json.loads(message)
                
                if msg.get("type") == "executing":
                    node_id = msg.get("data", {}).get("node")
                    if node_id is None:
                        # Execução completada (node = null)
                        break
                
                elif msg.get("type") == "progress":
                    data = msg.get("data", {})
                    value = data.get("value", 0)
                    max_val = data.get("max", 100)
                    print(f"Progresso: {value}/{max_val}")
                
                elif msg.get("type") == "executed":
                    node_id = msg.get("data", {}).get("node")
                    output = msg.get("data", {}).get("output")
                    print(f"Nó {node_id} executado")
                
                elif msg.get("type") == "execution_cached":
                    node_id = msg.get("data", {}).get("node")
                    print(f"Nó {node_id} em cache")
                
                elif msg.get("type") == "execution_error":
                    error_data = msg.get("data", {})
                    error_msg = error_data.get("exception_message", "Erro desconhecido")
                    raise Exception(f"Erro na execução: {error_msg}")
                
            except websockets.exceptions.ConnectionClosed:
                print("Conexão WebSocket fechada")
                break
    
    # Aguardar um momento para o servidor processar
    await asyncio.sleep(1)
    
    # Obter resultados
    return get_history(prompt_id)


def get_history(prompt_id: str) -> Dict:
    """
    Obtém o histórico de execução de um prompt.
    
    Args:
        prompt_id: ID do prompt
        
    Returns:
        Dicionário com o histórico
    """
    response = requests.get(f"{COMFYUI_SERVER}/history/{prompt_id}")
    response.raise_for_status()
    return response.json()


def extract_outputs(history: Dict) -> List[Dict]:
    """
    Extrai informações de outputs do histórico.
    
    Args:
        history: Histórico retornado por get_history()
        
    Returns:
        Lista de dicionários com informações dos outputs
    """
    outputs = []
    
    for prompt_id, prompt_data in history.items():
        if "outputs" in prompt_data:
            for node_id, node_output in prompt_data["outputs"].items():
                # Imagens
                if "images" in node_output:
                    for img in node_output["images"]:
                        outputs.append({
                            "type": "image",
                            "filename": img["filename"],
                            "subfolder": img.get("subfolder", ""),
                            "type_field": img.get("type", "output")
                        })
                
                # Áudio
                if "audio" in node_output:
                    for audio in node_output["audio"]:
                        outputs.append({
                            "type": "audio",
                            "filename": audio["filename"],
                            "subfolder": audio.get("subfolder", ""),
                            "type_field": audio.get("type", "output")
                        })
                
                # Vídeo (pode vir como image com formato diferente)
                if "videos" in node_output:
                    for video in node_output["videos"]:
                        outputs.append({
                            "type": "video",
                            "filename": video["filename"],
                            "subfolder": video.get("subfolder", ""),
                            "type_field": video.get("type", "output")
                        })
    
    return outputs


def download_output(filename: str, subfolder: str = "", type_field: str = "output") -> bytes:
    """
    Baixa um arquivo de output do ComfyUI.
    
    Args:
        filename: Nome do arquivo
        subfolder: Subpasta (se aplicável)
        type_field: Tipo de output (output, input, etc)
        
    Returns:
        Conteúdo do arquivo em bytes
    """
    params = {
        "filename": filename,
        "subfolder": subfolder,
        "type": type_field
    }
    
    response = requests.get(f"{COMFYUI_SERVER}/view", params=params)
    response.raise_for_status()
    return response.content


def save_output(content: bytes, filename: str, output_dir: Path) -> Path:
    """
    Salva um arquivo de output no diretório especificado.
    
    Args:
        content: Conteúdo do arquivo em bytes
        filename: Nome do arquivo
        output_dir: Diretório de destino
        
    Returns:
        Path completo do arquivo salvo
    """
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
    """
    Executa um workflow completo e baixa os outputs.
    
    Args:
        workflow: Dicionário do workflow
        workflow_name: Nome do tipo de workflow (para organização de outputs)
        client_id: ID do cliente
        save_outputs: Se True, baixa e salva os outputs
        
    Returns:
        Lista de Paths dos arquivos salvos
    """
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
    
    print(f"Encontrados {len(outputs)} output(s)")
    
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
    """
    Faz upload de uma imagem para o ComfyUI.
    
    Args:
        image_path: Caminho da imagem (local ou Path object)
        
    Returns:
        Resposta do servidor com nome do arquivo
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
    
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
    """
    Faz upload de um áudio para o ComfyUI.
    
    Args:
        audio_path: Caminho do áudio (local ou Path object)
        
    Returns:
        Resposta do servidor com nome do arquivo
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")
    
    # Determinar MIME type
    mime_type = "audio/wav" if audio_path.suffix == ".wav" else "audio/mpeg"
    
    files = {
        "audio": (audio_path.name, open(audio_path, "rb"), mime_type)
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


def check_server() -> bool:
    """
    Verifica se o servidor ComfyUI está rodando.
    
    Returns:
        True se servidor estiver acessível
    """
    try:
        response = requests.get(f"{COMFYUI_SERVER}/system_stats", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_queue_info() -> Dict:
    """
    Obtém informações sobre a fila de execução.
    
    Returns:
        Dicionário com informações da fila
    """
    response = requests.get(f"{COMFYUI_SERVER}/queue")
    response.raise_for_status()
    return response.json()


def clear_queue() -> bool:
    """
    Limpa a fila de execução.
    
    Returns:
        True se bem-sucedido
    """
    response = requests.post(f"{COMFYUI_SERVER}/queue", json={"clear": True})
    response.raise_for_status()
    return response.status_code == 200


def get_object_info(node_type: str = None) -> Dict:
    """
    Obtém informações sobre os nós disponíveis.
    
    Args:
        node_type: Se especificado, retorna info apenas desse nó
        
    Returns:
        Dicionário com informações do(s) nó(s)
    """
    if node_type:
        response = requests.get(f"{COMFYUI_SERVER}/object_info/{node_type}")
    else:
        response = requests.get(f"{COMFYUI_SERVER}/object_info")
    
    response.raise_for_status()
    return response.json()


def interrupt_execution() -> bool:
    """
    Interrompe a execução atual.
    
    Returns:
        True se bem-sucedido
    """
    response = requests.post(f"{COMFYUI_SERVER}/interrupt")
    response.raise_for_status()
    return response.status_code == 200


def free_memory() -> bool:
    """
    Libera memória do ComfyUI.
    
    Returns:
        True se bem-sucedido
    """
    response = requests.post(f"{COMFYUI_SERVER}/free")
    response.raise_for_status()
    return response.status_code == 200
