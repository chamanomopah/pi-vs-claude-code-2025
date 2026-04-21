#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO 2 - KOKORO TTS: Múltiplos Textos (Batch)

Descrição: Gera múltiplos áudios a partir de uma lista de textos.
          Processa cada texto sequencialmente com WebSocket para monitoramento.

Requisitos:
    - ComfyUI rodando em http://127.0.0.1:8188
    - ComfyUI-Kokoro instalado
    - Python 3.8+ com bibliotecas: requests, websockets

Uso:
    python exemplo2_python_batch.py

Saída: Áudios salvos em ComfyUI/user/outputs/YYYY-MM-DD/kokoro_tts/exemplo2_batch/
"""

import asyncio
import sys
import io
from pathlib import Path

# Configurar stdout para UTF-8 (necessário no Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from typing import List, Dict
from datetime import datetime

# Adicionar diretório scripts/comfyui ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "comfyui"))

from utils import (
    load_workflow,
    run_workflow,
    check_server,
    get_output_dir
)


def modify_workflow_for_text(workflow: dict, text: str, speaker: str = "am_onyx",
                            speed: float = 1.0, lang: str = "Portuguese") -> dict:
    """
    Modifica o workflow KOKORO para usar um texto específico.
    
    Args:
        workflow: Workflow JSON carregado
        text: Texto para converter em áudio
        speaker: Nome do speaker
        speed: Velocidade de fala
        lang: Idioma do texto
        
    Returns:
        Workflow modificado
    """
    # Modificar node 11 - KokoroGenerator
    if "11" in workflow and "inputs" in workflow["11"]:
        workflow["11"]["inputs"]["text"] = text
        workflow["11"]["inputs"]["speed"] = speed
        workflow["11"]["inputs"]["lang"] = lang
    
    # Modificar node 10 - KokoroSpeaker
    if "10" in workflow and "inputs" in workflow["10"]:
        workflow["10"]["inputs"]["speaker_name"] = speaker
    
    return workflow


async def process_single_text(
    workflow_template: dict,
    text: str,
    index: int,
    speaker: str = "am_onyx",
    speed: float = 1.0,
    lang: str = "Portuguese"
) -> Dict:
    """
    Processa um único texto e retorna informações do resultado.
    
    Args:
        workflow_template: Template do workflow
        text: Texto para processar
        index: Índice do texto (para nomeação)
        speaker: Nome do speaker
        speed: Velocidade de fala
        lang: Idioma
        
    Returns:
        Dicionário com status e caminhos dos arquivos
    """
    # Clonar workflow para não modificar o original
    import copy
    workflow = copy.deepcopy(workflow_template)
    
    # Modificar workflow com o texto
    workflow = modify_workflow_for_text(workflow, text, speaker, speed, lang)
    
    print(f"  Texto: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"  Enviando para processamento...")
    
    try:
        # Executar workflow
        saved_files = await run_workflow(
            workflow=workflow,
            workflow_name="kokoro_tts/exemplo2_batch",
            client_id=f"python_kokoro_batch_{index}",
            save_outputs=True
        )
        
        if saved_files:
            return {
                "status": "success",
                "text": text,
                "files": saved_files,
                "index": index
            }
        else:
            return {
                "status": "no_output",
                "text": text,
                "files": [],
                "index": index
            }
    
    except Exception as e:
        return {
            "status": "error",
            "text": text,
            "error": str(e),
            "files": [],
            "index": index
        }


async def main():
    """Função principal do exemplo."""
    
    print("=" * 70)
    print("KOKORO TTS - Exemplo 2: Batch de Textos")
    print("=" * 70)
    print()
    
    # 1. Verificar se ComfyUI está rodando
    print("1. Verificando conexão com ComfyUI...")
    if not check_server():
        print("✗ Erro: ComfyUI não está rodando em http://127.0.0.1:8188")
        print("  Inicie o ComfyUI antes de executar este script.")
        return
    
    print("✓ ComfyUI conectado com sucesso!")
    print()
    
    # 2. Carregar workflow base
    print("2. Carregando workflow KOKORO...")
    try:
        workflow_template = load_workflow("WORKFLOW - KOKORO.json")
        print("✓ Workflow carregado!")
    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
        return
    
    print()
    
    # 3. Definir lista de textos
    print("3. Definindo textos para processamento...")
    
    textos = [
        "Bom dia! Esta é a primeira mensagem do teste batch.",
        "Esta é a segunda mensagem. Estamos testando processamento em lote.",
        "Terceira e última mensagem do teste batch do Kokoro TTS."
    ]
    
    print(f"  Total de textos: {len(textos)}")
    for i, texto in enumerate(textos, 1):
        print(f"    {i}. {texto[:60]}{'...' if len(texto) > 60 else ''}")
    print()
    
    # 4. Configurar parâmetros
    print("4. Configurando parâmetros de geração...")
    
    speaker = "am_onyx"
    speed = 1.0
    lang = "Portuguese"
    
    print(f"  Speaker: {speaker}")
    print(f"  Velocidade: {speed}")
    print(f"  Idioma: {lang}")
    print()
    
    # 5. Processar textos em batch
    print("5. Processando textos...")
    print("-" * 70)
    
    resultados = []
    
    for i, texto in enumerate(textos):
        print(f"\n[{i+1}/{len(textos)}] Processando texto #{i+1}:")
        
        resultado = await process_single_text(
            workflow_template=workflow_template,
            text=texto,
            index=i,
            speaker=speaker,
            speed=speed,
            lang=lang
        )
        
        resultados.append(resultado)
        
        # Mostrar resultado
        if resultado["status"] == "success":
            print(f"  ✓ Sucesso!")
            for arquivo in resultado["files"]:
                print(f"    📄 {arquivo.name}")
        elif resultado["status"] == "no_output":
            print(f"  ⚠ Sem output gerado")
        else:
            print(f"  ✗ Erro: {resultado.get('error', 'Desconhecido')}")
        
        # Pequena pausa entre requisições
        if i < len(textos) - 1:
            await asyncio.sleep(1)
    
    print()
    print("-" * 70)
    print()
    
    # 6. Resumo dos resultados
    print("6. RESUMO DOS RESULTADOS:")
    print()
    
    sucesso = sum(1 for r in resultados if r["status"] == "success")
    erro = sum(1 for r in resultados if r["status"] == "error")
    sem_output = sum(1 for r in resultados if r["status"] == "no_output")
    
    print(f"  Total processados: {len(resultados)}")
    print(f"  ✓ Sucesso: {sucesso}")
    print(f"  ✗ Erros: {erro}")
    print(f"  ⚠ Sem output: {sem_output}")
    print()
    
    # Listar todos os arquivos gerados
    print("  Arquivos gerados:")
    output_dir = get_output_dir("kokoro_tts/exemplo2_batch")
    
    if output_dir.exists():
        arquivos = list(output_dir.glob("*.wav"))
        if arquivos:
            for arquivo in sorted(arquivos):
                tamanho = arquivo.stat().st_size / 1024  # KB
                print(f"    📄 {arquivo.name} ({tamanho:.1f} KB)")
        else:
            print("    (Nenhum arquivo encontrado)")
    else:
        print("    (Diretório não encontrado)")
    
    print()
    print("=" * 70)
    print("Fim do Exemplo 2")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
