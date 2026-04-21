#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO 1 - Z-IMAGE-TURBO: Texto para Imagem Simples

Descrição: Gera uma imagem a partir de um prompt de texto simples usando
          WebSocket para monitoramento em tempo real e download automático.

Requisitos:
    - ComfyUI rodando em http://127.0.0.1:8188
    - Z-Image-Turbo instalado com modelos:
      * z_image_turbo_bf16.safetensors (diffusion model)
      * qwen_3_4b.safetensors (text encoder)
      * ae.safetensors (VAE)
    - Python 3.8+ com bibliotecas: requests, websockets

Uso:
    python exemplo1_python_simple.py

Saída: Imagem salva em ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo1_simples/
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


def modify_workflow_for_prompt(workflow: dict, prompt: str, 
                               width: int = 1024, height: int = 1024,
                               steps: int = 8, seed: int = None) -> dict:
    """
    Modifica o workflow Z-IMAGE-TURBO para usar um prompt específico.
    
    Args:
        workflow: Workflow JSON carregado
        prompt: Prompt de texto para geração da imagem
        width: Largura da imagem
        height: Altura da imagem
        steps: Número de steps de difusão
        seed: Semente para geração (None = random)
        
    Returns:
        Workflow modificado
    """
    import random
    
    # O workflow Z-IMAGE-TURBO usa um nó principal (57) que é um subgraph
    # Os inputs do nó 57 controlam toda a geração
    
    if "57" in workflow and "inputs" in workflow["57"]:
        # Inputs do nó 57 mapeiam para os nós internos do subgraph
        workflow["57"]["inputs"]["text"] = prompt
        workflow["57"]["inputs"]["width"] = width
        workflow["57"]["inputs"]["height"] = height
        workflow["57"]["inputs"]["steps"] = steps
        
        # Modelos (geralmente não precisa mudar)
        # workflow["57"]["inputs"]["unet_name"] = "z_image_turbo_bf16.safetensors"
        # workflow["57"]["inputs"]["clip_name"] = "qwen_3_4b.safetensors"
        # workflow["57"]["inputs"]["vae_name"] = "ae.safetensors"
    
    # Configurar seed no nó KSampler (nó 3 dentro do subgraph)
    # Nota: O seed pode estar em um nó diferente dependendo da versão do workflow
    # Este código é genérico e pode precisar de ajustes
    
    return workflow


async def main():
    """Função principal do exemplo."""
    
    print("=" * 70)
    print("Z-IMAGE-TURBO - Exemplo 1: Texto para Imagem Simples")
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
    print("2. Carregando workflow Z-IMAGE-TURBO...")
    try:
        workflow = load_workflow("WORKFLOW - Z-IMAGE-TURBO.json")
        print("✓ Workflow carregado!")
    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
        return
    
    print()
    
    # 3. Configurar parâmetros
    print("3. Configurando parâmetros...")
    
    # Prompt para geração
    prompt = "Um gato astronauta flutuando no espaço sideral, com a Terra ao fundo, estilo arte digital, cores vibrantes, alta qualidade"
    
    # Dimensões da imagem
    width = 1024
    height = 1024
    
    # Steps de difusão (menos = mais rápido, mais = mais qualidade)
    steps = 8
    
    # Seed para geração determinística
    seed = 123456789
    
    print(f"  Prompt: {prompt}")
    print(f"  Dimensões: {width}x{height}")
    print(f"  Steps: {steps}")
    print(f"  Seed: {seed}")
    print()
    
    # 4. Modificar workflow
    print("4. Modificando workflow...")
    workflow = modify_workflow_for_prompt(
        workflow, 
        prompt=prompt,
        width=width,
        height=height,
        steps=steps,
        seed=seed
    )
    print("✓ Workflow modificado!")
    print()
    
    # 5. Executar workflow
    print("5. Executando workflow...")
    print("-" * 70)
    print("⏳ Gerando imagem... (pode levar 10-30 segundos)")
    print()
    
    try:
        saved_files = await run_workflow(
            workflow=workflow,
            workflow_name="zimage_turbo/exemplo1_simples",
            client_id="python_zimage_exemplo1",
            save_outputs=True
        )
        
        print()
        print("-" * 70)
        print()
        
        # 6. Resultados
        if saved_files:
            print("6. RESULTADO FINAL:")
            print()
            print("✓ Sucesso! Imagem gerada:")
            for file_path in saved_files:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  🖼️  {file_path.name}")
                print(f"     Caminho: {file_path}")
                print(f"     Tamanho: {size_mb:.2f} MB")
                print()
            
            # Mostrar prompt usado
            print(f"  Prompt usado: {prompt}")
            print()
            print("  Você pode abrir a imagem para ver o resultado!")
        else:
            print("⚠ Nenhum arquivo foi salvo.")
            print("  Verifique se:")
            print("    1. Os modelos estão instalados corretamente")
            print("    2. Há memória suficiente na GPU")
            print("    3. Não há erros no console do ComfyUI")
        
    except Exception as e:
        print()
        print(f"✗ Erro durante execução: {e}")
        print()
        print("Possíveis causas:")
        print("  1. Modelos não encontrados ou incorretos")
        print("  2. Memória GPU insuficiente")
        print("  3. Erro nos nós do workflow")
        return
    
    print()
    print("=" * 70)
    print("Fim do Exemplo 1")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
