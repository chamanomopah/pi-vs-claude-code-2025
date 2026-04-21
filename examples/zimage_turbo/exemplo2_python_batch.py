#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO 2 - Z-IMAGE-TURBO: Variações de Prompt (Batch)

Descrição: Gera múltiplas imagens a partir de uma lista de prompts.
          Processa cada prompt sequencialmente com WebSocket para monitoramento.

Requisitos:
    - ComfyUI rodando em http://127.0.0.1:8188
    - Z-Image-Turbo instalado com modelos necessários
    - Python 3.8+ com bibliotecas: requests, websockets

Uso:
    python exemplo2_python_batch.py

Saída: Imagens salvas em ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo2_batch/
"""

import asyncio
import sys
import random
from pathlib import Path
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
    if seed is None:
        seed = random.randint(1, 999999999)
    
    # Modificar nó principal (57) - subgraph do Z-Image-Turbo
    if "57" in workflow and "inputs" in workflow["57"]:
        workflow["57"]["inputs"]["text"] = prompt
        workflow["57"]["inputs"]["width"] = width
        workflow["57"]["inputs"]["height"] = height
        workflow["57"]["inputs"]["steps"] = steps
    
    return workflow


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
    import copy
    workflow = copy.deepcopy(workflow_template)
    
    # Modificar workflow com o prompt
    workflow = modify_workflow_for_prompt(
        workflow, 
        prompt=prompt,
        width=width,
        height=height,
        steps=steps
    )
    
    print(f"  Prompt: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")
    print(f"  Enviando para geração...")
    
    try:
        # Executar workflow
        saved_files = await run_workflow(
            workflow=workflow,
            workflow_name="zimage_turbo/exemplo2_batch",
            client_id=f"python_zimage_batch_{index}",
            save_outputs=True
        )
        
        if saved_files:
            return {
                "status": "success",
                "prompt": prompt,
                "files": saved_files,
                "index": index
            }
        else:
            return {
                "status": "no_output",
                "prompt": prompt,
                "files": [],
                "index": index
            }
    
    except Exception as e:
        return {
            "status": "error",
            "prompt": prompt,
            "error": str(e),
            "files": [],
            "index": index
        }


async def main():
    """Função principal do exemplo."""
    
    print("=" * 70)
    print("Z-IMAGE-TURBO - Exemplo 2: Batch de Prompts")
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
        workflow_template = load_workflow("WORKFLOW - Z-IMAGE-TURBO.json")
        print("✓ Workflow carregado!")
    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
        return
    
    print()
    
    # 3. Definir lista de prompts
    print("3. Definindo prompts para processamento...")
    
    prompts = [
        "Um dragão feito de cristal voando sobre montanhas nevadas ao pôr do sol, estilo fantasia épica",
        "Um robô amigável servindo café em uma cafeteria futurista, iluminação neon, anos 80",
        "Uma floresta mágica com cogumelos luminosos e fadas dançando, noturno, cênico"
    ]
    
    print(f"  Total de prompts: {len(prompts)}")
    for i, prompt in enumerate(prompts, 1):
        print(f"    {i}. {prompt[:70]}{'...' if len(prompt) > 70 else ''}")
    print()
    
    # 4. Configurar parâmetros
    print("4. Configurando parâmetros de geração...")
    
    width = 1024
    height = 1024
    steps = 8
    
    print(f"  Dimensões: {width}x{height}")
    print(f"  Steps: {steps}")
    print()
    
    # 5. Estimar tempo
    tempo_estimado = len(prompts) * 20
    print(f"5. Estimativa de tempo: ~{tempo_estimado} segundos")
    print()
    
    # 6. Processar prompts em batch
    print("6. Processando prompts...")
    print("-" * 70)
    
    resultados = []
    
    for i, prompt in enumerate(prompts):
        print(f"\n[{i+1}/{len(prompts)}] Gerando imagem #{i+1}:")
        
        resultado = await process_single_prompt(
            workflow_template=workflow_template,
            prompt=prompt,
            index=i,
            width=width,
            height=height,
            steps=steps
        )
        
        resultados.append(resultado)
        
        # Mostrar resultado
        if resultado["status"] == "success":
            print(f"  ✓ Sucesso!")
            for arquivo in resultado["files"]:
                tamanho = arquivo.stat().st_size / (1024 * 1024)
                print(f"    🖼️  {arquivo.name} ({tamanho:.2f} MB)")
        elif resultado["status"] == "no_output":
            print(f"  ⚠ Sem output gerado")
        else:
            print(f"  ✗ Erro: {resultado.get('error', 'Desconhecido')}")
        
        # Pequena pausa entre requisições
        if i < len(prompts) - 1:
            print()
            print("  Aguardando 3 segundos antes da próxima geração...")
            await asyncio.sleep(3)
    
    print()
    print("-" * 70)
    print()
    
    # 7. Resumo dos resultados
    print("7. RESUMO DOS RESULTADOS:")
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
    print("  Imagens geradas:")
    output_dir = get_output_dir("zimage_turbo/exemplo2_batch")
    
    if output_dir.exists():
        arquivos = list(output_dir.glob("*.png")) + list(output_dir.glob("*.jpg"))
        if arquivos:
            for arquivo in sorted(arquivos):
                tamanho = arquivo.stat().st_size / (1024 * 1024)
                print(f"    🖼️  {arquivo.name} ({tamanho:.2f} MB)")
        else:
            print("    (Nenhum arquivo encontrado)")
    else:
        print("    (Diretório não encontrado)")
    
    print()
    print("=" * 70)
    print("Fim do Exemplo 2")
    print("=" * 70)
    print()
    print("DICA: Experimente variar:")
    print("  - Prompts: diferentes temas, estilos, assuntos")
    print("  - Dimensões: 512x512, 1920x1088, etc")
    print("  - Steps: 4 (rápido), 8 (equilíbrio), 16 (qualidade)")


if __name__ == "__main__":
    asyncio.run(main())
