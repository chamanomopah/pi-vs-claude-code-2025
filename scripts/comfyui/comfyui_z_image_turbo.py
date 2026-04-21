"""
ComfyUI - Z-Image-Turbo Automation
Script para gerar imagens usando o modelo Z-Image-Turbo
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Adicionar diretório parent ao path para importar utils
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    load_workflow, run_workflow, check_server
)


def prepare_z_image_turbo_workflow(
    prompt: str,
    width: int = 1920,
    height: int = 1088,
    steps: int = 8,
    seed: int = 0,
    cfg: float = 1.0,
    sampler_name: str = "res_multistep",
    scheduler: str = "simple",
    shift: float = 3.0,
    unet_name: str = "z_image_turbo_bf16.safetensors",
    clip_name: str = "qwen_3_4b.safetensors",
    vae_name: str = "ae.safetensors"
) -> dict:
    """
    Prepara o workflow Z-Image-Turbo com os parâmetros fornecidos.
    
    Args:
        prompt: Prompt de texto para gerar imagem
        width: Largura da imagem
        height: Altura da imagem
        steps: Número de steps de amostragem
        seed: Semente (0 para random)
        cfg: CFG scale
        sampler_name: Nome do sampler
        scheduler: Nome do scheduler
        shift: Shift para ModelSamplingAuraFlow
        unet_name: Nome do modelo UNET
        clip_name: Nome do text encoder (CLIP)
        vae_name: Nome do VAE
        
    Returns:
        Dicionário do workflow pronto para enviar
    """
    # Carregar workflow base
    workflow = load_workflow("WORKFLOW - Z-IMAGE-TURBO.json")
    
    # O workflow usa um subgraph (f2fdebf6-dfaf-43b6-9eb2-7f70613cfdc1)
    # que é um nó customizado que encapsula toda a lógica
    # Precisamos encontrar e atualizar os parâmetros corretos
    
    # Vamos buscar o nó que contém o subgraph
    for node_id, node_data in workflow.items():
        if isinstance(node_data, dict) and "class_type" in node_data:
            # O nó principal é o subgraph Text to Image
            if node_data.get("type") == "f2fdebf6-dfaf-43b6-9eb2-7f70613cfdc1":
                if "inputs" in node_data:
                    node_data["inputs"]["text"] = prompt
                    node_data["inputs"]["width"] = width
                    node_data["inputs"]["height"] = height
                    node_data["inputs"]["steps"] = steps
    
    # Se o workflow tiver nós individuais (versão mais antiga)
    # Atualizar CLIPTextEncode (prompt)
    for node_id, node_data in workflow.items():
        if isinstance(node_data, dict):
            class_type = node_data.get("class_type", "")
            inputs = node_data.get("inputs", {})
            
            if class_type == "CLIPTextEncode" and "text" in inputs:
                # Assumir que é o positive prompt
                node_data["inputs"]["text"] = prompt
            
            elif class_type == "KSampler":
                node_data["inputs"]["seed"] = seed
                node_data["inputs"]["cfg"] = cfg
                node_data["inputs"]["sampler_name"] = sampler_name
                node_data["inputs"]["scheduler"] = scheduler
                node_data["inputs"]["steps"] = steps
            
            elif class_type == "EmptySD3LatentImage":
                node_data["inputs"]["width"] = width
                node_data["inputs"]["height"] = height
            
            elif class_type == "ModelSamplingAuraFlow":
                node_data["inputs"]["shift"] = shift
            
            elif class_type == "UNETLoader":
                node_data["inputs"]["unet_name"] = unet_name
            
            elif class_type == "CLIPLoader":
                node_data["inputs"]["clip_name"] = clip_name
            
            elif class_type == "VAELoader":
                node_data["inputs"]["vae_name"] = vae_name
    
    return workflow


async def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Gera imagens usando Z-Image-Turbo no ComfyUI"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        required=True,
        help="Prompt de texto para gerar imagem"
    )
    parser.add_argument(
        "--width", "-W",
        type=int,
        default=1920,
        help="Largura da imagem (padrão: 1920)"
    )
    parser.add_argument(
        "--height", "-H",
        type=int,
        default=1088,
        help="Altura da imagem (padrão: 1088)"
    )
    parser.add_argument(
        "--steps", "-s",
        type=int,
        default=8,
        help="Número de steps (padrão: 8)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Semente (0 para random, padrão: 0)"
    )
    parser.add_argument(
        "--cfg",
        type=float,
        default=1.0,
        help="CFG scale (padrão: 1.0)"
    )
    parser.add_argument(
        "--shift",
        type=float,
        default=3.0,
        help="Shift para AuraFlow (padrão: 3.0)"
    )
    parser.add_argument(
        "--client-id",
        type=str,
        default="z_image_turbo_client",
        help="ID do cliente para ComfyUI"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Não salvar a imagem"
    )
    
    args = parser.parse_args()
    
    # Verificar servidor
    print("Verificando servidor ComfyUI...")
    if not check_server():
        print("ERRO: Servidor ComfyUI não está rodando em http://127.0.0.1:8188")
        print("Inicie o ComfyUI e tente novamente.")
        sys.exit(1)
    print("Servidor OK!")
    
    # Preparar workflow
    print(f"\nPreparando workflow Z-Image-Turbo:")
    print(f"  Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"  Dimensões: {args.width}x{args.height}")
    print(f"  Steps: {args.steps}")
    print(f"  CFG: {args.cfg}")
    print(f"  Shift: {args.shift}")
    
    workflow = prepare_z_image_turbo_workflow(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        steps=args.steps,
        seed=args.seed,
        cfg=args.cfg,
        shift=args.shift
    )
    
    # Executar workflow
    try:
        output_files = await run_workflow(
            workflow=workflow,
            workflow_name="z_image_turbo",
            client_id=args.client_id,
            save_outputs=not args.no_save
        )
        
        if output_files:
            print(f"\n✓ Sucesso! {len(output_files)} arquivo(s) gerado(s):")
            for f in output_files:
                print(f"  - {f}")
        else:
            print("\n✓ Workflow executado (sem outputs salvos)")
    
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
