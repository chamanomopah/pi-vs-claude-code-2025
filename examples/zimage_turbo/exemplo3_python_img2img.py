#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO 3 - Z-IMAGE-TURBO: Upload de Imagem + Image-to-Image

Descrição: Demonstração de upload de imagem para Image-to-Image.
          NOTA: O workflow Z-IMAGE-TURBO atual é Text-to-Image.
          Este exemplo mostra como fazer upload e demonstra a estrutura
          necessária para img2img.

Requisitos:
    - ComfyUI rodando em http://127.0.0.1:8188
    - Z-Image-Turbo instalado com modelos necessários
    - Arquivo de imagem de referência (.png ou .jpg)

Uso:
    # Com imagem de referência
    python exemplo3_python_img2img.py caminho/da/imagem.jpg
    
    # Sem imagem (demonstração com prompt)
    python exemplo3_python_img2img.py

Saída: Imagem salva em ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo3_img2img/
"""

import asyncio
import sys
import io
from pathlib import Path

# Configurar stdout para UTF-8 (necessário no Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import argparse

# Adicionar diretório scripts/comfyui ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "comfyui"))

from utils import (
    load_workflow,
    run_workflow,
    check_server,
    upload_image
)


def modify_workflow_for_prompt(workflow: dict, prompt: str,
                               width: int = 1024, height: int = 1024,
                               steps: int = 8) -> dict:
    """
    Modifica o workflow Z-IMAGE-TURBO para usar um prompt específico.
    
    Args:
        workflow: Workflow JSON carregado
        prompt: Prompt de texto
        width: Largura da imagem
        height: Altura da imagem
        steps: Número de steps
        
    Returns:
        Workflow modificado
    """
    if "57" in workflow and "inputs" in workflow["57"]:
        workflow["57"]["inputs"]["text"] = prompt
        workflow["57"]["inputs"]["width"] = width
        workflow["57"]["inputs"]["height"] = height
        workflow["57"]["inputs"]["steps"] = steps
    
    return workflow


def modify_workflow_for_img2img(workflow: dict, reference_image_path: str,
                                denoise: float = 0.7) -> dict:
    """
    Modifica o workflow para Image-to-Image.
    
    NOTA: Esta é uma função demonstrativa. O workflow Z-IMAGE-TURBO
    atual é Text-to-Image puro. Para img2img real seria necessário:
    1. Adicionar nó LoadImage para carregar a imagem
    2. Adicionar nó VAEEncode/ImageToLatent
    3. Configurar KSampler com denoise < 1.0
    4. Conectar o latente da imagem ao KSampler
    
    Args:
        workflow: Workflow JSON carregado
        reference_image_path: Caminho da imagem de referência
        denoise: Fator de denoising (0.0-1.0)
        
    Returns:
        Workflow modificado (demonstrativo)
    """
    print()
    print("⚠ IMAGE-TO-IMAGE NÃO IMPLEMENTADO")
    print("=" * 70)
    print()
    print("O workflow atual do Z-Image-Turbo é Text-to-Image puro")
    print("e não suporta Image-to-Image com imagem de referência.")
    print()
    print("Para implementar img2img, você precisaria:")
    print("  1. Modificar o workflow adicionando nós para:")
    print("     - LoadImage: carregar a imagem de referência")
    print("     - VAEEncode ou ImageToLatent: converter para latente")
    print("     - Conectar ao KSampler com denoise < 1.0")
    print()
    print("  2. Parâmetros importantes:")
    print("     - denoise: 0.0-1.0 (0.7 é um bom ponto de partida)")
    print("       * 1.0 = ignora a imagem (geração do zero)")
    print("       * 0.5-0.7 = preserva bastante da imagem original")
    print("       * 0.2-0.4 = preserva quase tudo da imagem")
    print()
    print("  3. O prompt descreve as MUDANÇAS desejadas")
    print()
    print("Verifique workflows de img2img para ComfyUI para exemplos.")
    print()
    print("=" * 70)
    
    return workflow


async def main():
    """Função principal do exemplo."""
    
    parser = argparse.ArgumentParser(
        description="Exemplo 3 - Z-Image-Turbo com upload de imagem"
    )
    parser.add_argument(
        "image",
        nargs="?",
        help="Caminho da imagem de referência (opcional)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Um castelo flutuante nas nuvens ao pôr do sol, estilo Studio Ghibli",
        help="Prompt para geração"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1024,
        help="Largura da imagem"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1024,
        help="Altura da imagem"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Z-IMAGE-TURBO - Exemplo 3: Upload de Imagem + img2img")
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
    
    # 3. Processar imagem de referência (se fornecida)
    if args.image:
        image_path = Path(args.image)
        
        print("3. Processando imagem de referência...")
        
        if not image_path.exists():
            print(f"✗ Erro: Arquivo não encontrado: {image_path}")
            return
        
        print(f"  Arquivo: {image_path.name}")
        print(f"  Tamanho: {image_path.stat().st_size:,} bytes")
        print(f"  Formato: {image_path.suffix}")
        print()
        
        # Fazer upload da imagem
        print("  Fazendo upload para ComfyUI...")
        try:
            upload_result = upload_image(str(image_path))
            uploaded_name = upload_result.get("name", "")
            
            print(f"  ✓ Upload realizado: {uploaded_name}")
            print()
            
            # Tentar modificar workflow para img2img
            # (Nota: função demonstrativa)
            workflow = modify_workflow_for_img2img(workflow, str(image_path))
            
        except Exception as e:
            print(f"  ✗ Erro no upload: {e}")
            return
    else:
        print("3. Nenhuma imagem de referência fornecida.")
        print("  Usando Text-to-Image (geração do zero).")
        print()
    
    # 4. Configurar parâmetros
    print("4. Configurando parâmetros de geração...")
    
    prompt = args.prompt
    width = args.width
    height = args.height
    steps = 8
    
    print(f"  Prompt: {prompt}")
    print(f"  Dimensões: {width}x{height}")
    print(f"  Steps: {steps}")
    print()
    
    # 5. Modificar workflow
    print("5. Modificando workflow...")
    workflow = modify_workflow_for_prompt(workflow, prompt, width, height, steps)
    print("✓ Workflow modificado!")
    print()
    
    # 6. Executar workflow
    print("6. Executando workflow...")
    print("-" * 70)
    
    try:
        saved_files = await run_workflow(
            workflow=workflow,
            workflow_name="zimage_turbo/exemplo3_img2img",
            client_id="python_zimage_exemplo3",
            save_outputs=True
        )
        
        print()
        print("-" * 70)
        print()
        
        # 7. Resultados
        if saved_files:
            print("7. RESULTADO FINAL:")
            print()
            print("✓ Sucesso! Imagem gerada:")
            for file_path in saved_files:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  🖼️  {file_path.name}")
                print(f"     Caminho: {file_path}")
                print(f"     Tamanho: {size_mb:.2f} MB")
        else:
            print("⚠ Nenhum arquivo foi salvo.")
            print("  Verifique o ComfyUI para mais detalhes.")
        
    except Exception as e:
        print()
        print(f"✗ Erro durante execução: {e}")
        return
    
    print()
    print("=" * 70)
    print("Fim do Exemplo 3")
    print("=" * 70)
    print()
    print("NOTAS:")
    print("  - Este exemplo demonstra o upload de imagem para referência")
    print("  - O workflow Z-IMAGE-TURBO atual é Text-to-Image")
    print("  - Para img2img real, você precisa:")
    print("    * Usar um workflow específico para Image-to-Image")
    print("    * Ou modificar este workflow adicionando nós de carga de imagem")
    print("    * Configurar denoise < 1.0 no KSampler")


if __name__ == "__main__":
    asyncio.run(main())
