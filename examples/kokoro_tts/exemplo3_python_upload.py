#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO 3 - KOKORO TTS: Upload de Áudio de Referência (Voice Cloning)

Descrição: Demonstração de upload de áudio para referência de voz.
          NOTA: O workflow KOKORO atual usa speakers pré-definidos.
          Este exemplo mostra como fazer upload e demonstra a estrutura
          necessária para voice cloning.

Requisitos:
    - ComfyUI rodando em http://127.0.0.1:8188
    - ComfyUI-Kokoro instalado
    - Arquivo de áudio de referência (.wav ou .mp3)

Uso:
    # Com áudio de referência
    python exemplo3_python_upload.py caminho/do/audio_referencia.wav
    
    # Sem áudio (demonstração com speaker fixo)
    python exemplo3_python_upload.py

Saída: Áudio salvo em ComfyUI/user/outputs/YYYY-MM-DD/kokoro_tts/exemplo3_upload/
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
    upload_audio
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


def modify_workflow_for_voice_cloning(workflow: dict, reference_audio_path: str) -> dict:
    """
    Modifica o workflow para usar um áudio de referência para voice cloning.
    
    NOTA: Esta é uma função demonstrativa. O workflow KOKORO atual
    não suporta nativamente voice cloning com áudio de referência.
    Para implementar isso, seria necessário:
    1. Adicionar nó para carregar áudio
    2. Adicionar nó para extrair speaker embedding
    3. Conectar o embedding ao KokoroGenerator
    
    Args:
        workflow: Workflow JSON carregado
        reference_audio_path: Caminho do áudio de referência
        
    Returns:
        Workflow modificado (demonstrativo)
    """
    print()
    print("⚠ VOICE CLONING NÃO IMPLEMENTADO")
    print("=" * 70)
    print()
    print("O workflow atual do Kokoro TTS usa speakers pré-definidos")
    print("e não suporta clonagem de voz com áudio de referência.")
    print()
    print("Para implementar voice cloning, você precisaria:")
    print("  1. Usar um workflow específico para voice cloning")
    print("  2. Adicionar nós para:")
    print("     - LoadAudio: carregar o áudio de referência")
    print("     - AudioToEmbedding: extrair características da voz")
    print("     - Conectar o embedding ao KokoroGenerator")
    print()
    print("Verifique a documentação do ComfyUI-Kokoro para workflows")
    print("específicos de voice cloning.")
    print()
    print("=" * 70)
    
    return workflow


async def main():
    """Função principal do exemplo."""
    
    parser = argparse.ArgumentParser(
        description="Exemplo 3 - Kokoro TTS com upload de áudio de referência"
    )
    parser.add_argument(
        "audio",
        nargs="?",
        help="Caminho do áudio de referência (opcional)"
    )
    parser.add_argument(
        "--text",
        type=str,
        default="Este é um teste de geração de áudio com Kokoro TTS.",
        help="Texto para converter em áudio"
    )
    parser.add_argument(
        "--speaker",
        type=str,
        default="am_onyx",
        help="Nome do speaker pré-definido"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("KOKORO TTS - Exemplo 3: Upload de Áudio de Referência")
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
        workflow = load_workflow("WORKFLOW - KOKORO.json")
        print("✓ Workflow carregado!")
    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
        return
    
    print()
    
    # 3. Processar áudio de referência (se fornecido)
    if args.audio:
        audio_path = Path(args.audio)
        
        print("3. Processando áudio de referência...")
        
        if not audio_path.exists():
            print(f"✗ Erro: Arquivo não encontrado: {audio_path}")
            return
        
        print(f"  Arquivo: {audio_path.name}")
        print(f"  Tamanho: {audio_path.stat().st_size:,} bytes")
        print(f"  Formato: {audio_path.suffix}")
        print()
        
        # Fazer upload do áudio
        print("  Fazendo upload para ComfyUI...")
        try:
            upload_result = upload_audio(str(audio_path))
            uploaded_name = upload_result.get("name", "")
            
            print(f"  ✓ Upload realizado: {uploaded_name}")
            print()
            
            # Tentar modificar workflow para voice cloning
            # (Nota: função demonstrativa)
            workflow = modify_workflow_for_voice_cloning(workflow, str(audio_path))
            
        except Exception as e:
            print(f"  ✗ Erro no upload: {e}")
            return
    else:
        print("3. Nenhum áudio de referência fornecido.")
        print("  Usando speaker pré-definido.")
        print()
    
    # 4. Configurar parâmetros
    print("4. Configurando parâmetros de geração...")
    
    texto = args.text
    speaker = args.speaker
    speed = 1.0
    lang = "Portuguese"
    
    print(f"  Texto: {texto}")
    print(f"  Speaker: {speaker}")
    print(f"  Velocidade: {speed}")
    print(f"  Idioma: {lang}")
    print()
    
    # 5. Modificar workflow
    print("5. Modificando workflow...")
    workflow = modify_workflow_for_text(workflow, texto, speaker, speed, lang)
    print("✓ Workflow modificado!")
    print()
    
    # 6. Executar workflow
    print("6. Executando workflow...")
    print("-" * 70)
    
    try:
        saved_files = await run_workflow(
            workflow=workflow,
            workflow_name="kokoro_tts/exemplo3_upload",
            client_id="python_kokoro_exemplo3",
            save_outputs=True
        )
        
        print("-" * 70)
        print()
        
        # 7. Resultados
        if saved_files:
            print("7. RESULTADO FINAL:")
            print()
            print("✓ Sucesso! Áudio gerado:")
            for file_path in saved_files:
                size_kb = file_path.stat().st_size / 1024
                print(f"  📄 {file_path.name}")
                print(f"     Caminho: {file_path}")
                print(f"     Tamanho: {size_kb:.1f} KB")
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
    print("  - Este exemplo demonstra o upload de áudio para referência")
    print("  - O workflow KOKORO atual usa speakers pré-definidos")
    print("  - Para voice cloning real, verifique workflows específicos")
    print("    do ComfyUI-Kokoro que suportem esta funcionalidade")


if __name__ == "__main__":
    asyncio.run(main())
