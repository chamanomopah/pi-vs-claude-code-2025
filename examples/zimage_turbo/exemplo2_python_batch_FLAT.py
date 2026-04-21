#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO 2 - Z-IMAGE-TURBO: Variações de Prompt (Batch) - WORKFLOW FLAT

Descrição: Gera múltiplas imagens a partir de uma lista de prompts.
          Usa workflow flat compatível com API do ComfyUI.

Requisitos:
    - ComfyUI rodando em http://127.0.0.1:8188
    - Z-Image-Turbo instalado com modelos necessários
    - Python 3.8+ com bibliotecas: requests, websockets

Uso:
    python exemplo2_python_batch_FLAT.py

Saída: Imagens salvas em ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo2_batch/
"""

import asyncio
import sys
import random
import io
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import copy

# Configurar stdout para UTF-8 (necessário no Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Adicionar diretório scripts/comfyui ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "comfyui"))

from utils import (
    load_workflow,
    run_workflow,
    check_server
)


def modify_workflow_flat(workflow: dict, prompt: str,
                        width: int = 1024, height: int = 1024,
                        steps: int = 8, seed: int = None) -> dict:
    """
    Modifica o workflow Z-IMAGE-TURBO flat para usar um prompt específico.

    Args:
        workflow: Workflow JSON carregado (flat)
        prompt: Prompt de texto para geração da imagem
        width: Largura da imagem
        height: Altura da imagem
        steps: Número de steps de difusão
        seed: Semente para geração (None = random)

    Returns:
        Workflow modificado
    """
    if seed is None:
        seed = random.randint(1, 999999999999)

    # Workflow flat usa nós diretos
    if "27" in workflow and "inputs" in workflow["27"]:
        workflow["27"]["inputs"]["text"] = prompt

    if "13" in workflow and "inputs" in workflow["13"]:
        workflow["13"]["inputs"]["width"] = width
        workflow["13"]["inputs"]["height"] = height

    if "3" in workflow and "inputs" in workflow["3"]:
        workflow["3"]["inputs"]["steps"] = steps
        workflow["3"]["inputs"]["seed"] = seed

    return workflow, seed


async def process_single_prompt(
    workflow_template: dict,
    prompt: str,
    index: int,
    width: int = 1024,
    height: int = 1024,
    steps: int = 8
) -> Dict:
    """
    Processa um único prompt e retorna informações do resultado.

    Args:
        workflow_template: Template do workflow
        prompt: Prompt para processar
        index: Índice do prompt (para nomeação)
        width: Largura da imagem
        height: Altura da imagem
        steps: Steps de difusão

    Returns:
        Dicionário com status e caminhos dos arquivos
    """
    # Clonar workflow
    workflow = copy.deepcopy(workflow_template)

    # Modificar workflow com o prompt
    workflow, seed = modify_workflow_flat(
        workflow,
        prompt=prompt,
        width=width,
        height=height,
        steps=steps
    )

    print(f"  📝 Prompt {index + 1}: {prompt[:80]}...")
    print(f"     Seed: {seed}")

    try:
        saved_files = await run_workflow(
            workflow=workflow,
            workflow_name=f"zimage_turbo/exemplo2_batch/{index+1}",
            client_id=f"python_zimage_batch_{index}",
            save_outputs=True
        )

        if saved_files:
            file_info = {
                "status": "success",
                "index": index,
                "prompt": prompt,
                "files": [str(f) for f in saved_files],
                "seed": seed
            }
            print(f"     ✓ Sucesso! {len(saved_files)} arquivo(s)")
            return file_info
        else:
            return {
                "status": "no_files",
                "index": index,
                "prompt": prompt,
                "seed": seed
            }

    except Exception as e:
        print(f"     ✗ Erro: {e}")
        return {
            "status": "error",
            "index": index,
            "prompt": prompt,
            "error": str(e)
        }


async def main():
    """Função principal do exemplo."""

    print("=" * 70)
    print("Z-IMAGE-TURBO - Exemplo 2: Variações de Prompt (Batch - FLAT)")
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
    print("2. Carregando workflow Z-IMAGE-TURBO (FLAT)...")
    try:
        workflow = load_workflow("WORKFLOW - Z-IMAGE-TURBO-FLAT.json")
        print("✓ Workflow carregado!")
    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
        return

    print()

    # 3. Definir prompts para gerar múltiplas imagens
    print("3. Configurando batch de prompts...")

    prompts = [
        "A serene mountain landscape at sunset, photorealistic, 4K, golden hour lighting",
        "A futuristic cyberpunk city at night, neon lights, rain, highly detailed",
        "A cute robot gardener watering plants, digital art, vibrant colors, Studio Ghibli style"
    ]

    print(f"  Total de prompts: {len(prompts)}")
    for i, p in enumerate(prompts, 1):
        print(f"    {i}. {p[:70]}...")
    print()

    # 4. Processar cada prompt
    print("4. Processando prompts...")
    print("-" * 70)

    start_time = datetime.now()
    results = []

    for i, prompt in enumerate(prompts):
        print(f"\n[{i+1}/{len(prompts)}] Processando prompt...")
        result = await process_single_prompt(
            workflow_template=workflow,
            prompt=prompt,
            index=i,
            width=1024,
            height=1024,
            steps=8
        )
        results.append(result)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("-" * 70)
    print()

    # 5. Sumário de resultados
    print("5. SUMÁRIO DE RESULTADOS:")
    print()

    success_count = sum(1 for r in results if r["status"] == "success")
    error_count = sum(1 for r in results if r["status"] == "error")
    no_files_count = sum(1 for r in results if r["status"] == "no_files")

    print(f"  ✓ Sucessos: {success_count}/{len(prompts)}")
    print(f"  ✗ Erros: {error_count}/{len(prompts)}")
    print(f"  ⚠ Sem arquivos: {no_files_count}/{len(prompts)}")
    print(f"  ⏱ Tempo total: {duration:.1f} segundos")
    print(f"  ⏱ Tempo médio por imagem: {duration/len(prompts):.1f} segundos")
    print()

    # 6. Listar arquivos gerados
    print("6. ARQUIVOS GERADOS:")
    print()

    for result in results:
        if result["status"] == "success":
            print(f"  Prompt {result['index']+1}:")
            for file_path in result["files"]:
                p = Path(file_path)
                size_mb = p.stat().st_size / (1024 * 1024)
                print(f"    📄 {p.name}")
                print(f"       {p}")
                print(f"       Tamanho: {size_mb:.2f} MB")
        elif result["status"] == "error":
            print(f"  ✗ Prompt {result['index']+1}: ERRO - {result['error']}")
        else:
            print(f"  ⚠ Prompt {result['index']+1}: Nenhum arquivo gerado")

    print()
    print("=" * 70)
    print("Fim do Exemplo 2 (FLAT - Batch)")
    print("=" * 70)


if __name__ == "__main__":
    # Executar função assíncrona
    asyncio.run(main())
