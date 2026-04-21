#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO 1 - Z-IMAGE-TURBO: Texto para Imagem Simples (WORKFLOW FLAT)

Descrição: Gera uma imagem a partir de um prompt de texto simples usando
          workflow flat (sem subgraphs) compatível com API do ComfyUI.

Requisitos:
    - ComfyUI rodando em http://127.0.0.1:8188
    - Z-Image-Turbo instalado com modelos
    - Python 3.8+ com bibliotecas: requests, websockets

Uso:
    python exemplo1_python_simple_FLAT.py

Saída: Imagem salva em ComfyUI/output/
"""

import asyncio
import sys
import io
from pathlib import Path

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
    import random

    # Workflow flat usa nós diretos:
    # - 27: CLIPTextEncode (prompt)
    # - 13: EmptySD3LatentImage (dimensões)
    # - 3: KSampler (steps, seed)

    # Modificar prompt no nó 27
    if "27" in workflow and "inputs" in workflow["27"]:
        workflow["27"]["inputs"]["text"] = prompt

    # Modificar dimensões no nó 13
    if "13" in workflow and "inputs" in workflow["13"]:
        workflow["13"]["inputs"]["width"] = width
        workflow["13"]["inputs"]["height"] = height

    # Modificar steps e seed no nó 3 (KSampler)
    if "3" in workflow and "inputs" in workflow["3"]:
        workflow["3"]["inputs"]["steps"] = steps
        if seed is None:
            seed = random.randint(1, 999999999999)
        workflow["3"]["inputs"]["seed"] = seed

    return workflow, seed


async def main():
    """Função principal do exemplo."""

    print("=" * 70)
    print("Z-IMAGE-TURBO - Exemplo 1: Texto para Imagem Simples (FLAT)")
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
        print("  Certifique-se que WORKFLOW - Z-IMAGE-TURBO-FLAT.json existe em:")
        print("  C:\\Users\\JOSE\\Downloads\\confyui\\ComfyUI_windows_portable\\ComfyUI\\user\\default\\workflows\\")
        return

    print()

    # 3. Configurar parâmetros
    print("3. Configurando parâmetros...")

    # Prompt de texto
    prompt = "Um gato astronauta flutuando no espaço sideral, com a Terra ao fundo, estilo arte digital, cores vibrantes, alta qualidade"

    # Dimensões da imagem
    width = 1024
    height = 1024

    # Número de steps (Z-IMAGE-TURBO é rápido, geralmente 4-8 steps)
    steps = 8

    # Seed (None = aleatório)
    seed = None  # Será gerado automaticamente

    print(f"  Prompt: {prompt}")
    print(f"  Dimensões: {width}x{height}")
    print(f"  Steps: {steps}")
    print(f"  Seed: {'(aleatório)' if seed is None else seed}")
    print()

    # 4. Modificar workflow
    print("4. Modificando workflow...")
    workflow, actual_seed = modify_workflow_flat(workflow, prompt, width, height, steps, seed)
    print("✓ Workflow modificado!")
    print(f"  Seed usado: {actual_seed}")
    print()

    # 5. Executar workflow
    print("5. Executando workflow...")
    print("-" * 70)
    print("⏳ Gerando imagem... (pode levar 10-30 segundos)")

    try:
        saved_files = await run_workflow(
            workflow=workflow,
            workflow_name="zimage_turbo/exemplo1_flat",
            client_id="python_zimage_exemplo1_flat",
            save_outputs=True
        )

        print("-" * 70)
        print()

        # 6. Resultados
        if saved_files:
            print("6. RESULTADO FINAL:")
            print()
            print("✓ Sucesso! Imagem gerada:")
            for file_path in saved_files:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  📄 {file_path.name}")
                print(f"     Caminho: {file_path}")
                print(f"     Tamanho: {size_mb:.2f} MB")
        else:
            print("⚠ Nenhum arquivo foi salvo.")
            print("  Verifique o ComfyUI para mais detalhes.")

    except Exception as e:
        print()
        print(f"✗ Erro durante execução: {e}")
        print()
        print("Possíveis causas:")
        print("  1. Modelos não encontrados ou incorretos")
        print("  2. Memória GPU insuficiente")
        print("  3. Erro nos nós do workflow")
        import traceback
        traceback.print_exc()
        return

    print()
    print("=" * 70)
    print("Fim do Exemplo 1 (FLAT)")
    print("=" * 70)


if __name__ == "__main__":
    # Executar função assíncrona
    asyncio.run(main())
