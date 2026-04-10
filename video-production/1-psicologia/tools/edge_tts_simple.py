#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge TTS - Text to Speech com Microsoft Edge
=============================================
Script para converter texto em áudio usando Edge TTS (Microsoft Edge).

Autor: Assistant
Data: 2025-04-09
"""

# =============================================================================
# VARIÁVEIS CONFIGURÁVEIS - Edite aqui!
# =============================================================================

TEXTO = "Welcome to Psychology channel! In this video, we'll explore the fascinating world of human behavior and the mind. Subscribe for more content like this!"

VOZ = "en-US-AriaNeural"  # Voz a ser usada (ex: pt-BR-FranciscaNeural para portugues)
VELOCIDADE = "+0%"  # +0% = normal, -10% = lento, +10% = rapido
PITCH = "+0Hz"  # +0Hz = normal
ARQUIVO_SAIDA = "audio_edge_tts.mp3"  # Nome do arquivo de saida

# =============================================================================
# CÓDIGO PRINCIPAL
# =============================================================================

import sys
import time
import asyncio
from pathlib import Path


def listar_vozes_disponiveis():
    """Retorna lista de vozes populares no Edge TTS."""
    return {
        # Inglês Americano Femininas
        "en-US-AriaNeural": "Feminina americana (melhor opcao)",
        "en-US-JennyNeural": "Feminina americana (profissional)",
        "en-US-MichelleNeural": "Feminina americana (conversacional)",
        
        # Inglês Americano Masculinas
        "en-US-GuyNeural": "Masculino americano",
        "en-US-BrandonNeural": "Masculino americano (profissional)",
        
        # Português Brasileiro
        "pt-BR-FranciscaNeural": "Feminina brasileira",
        "pt-BR-AntonioNeural": "Masculino brasileiro",
    }


async def gerar_audio():
    """Funcao assincrona para gerar audio."""
    
    print("=" * 70)
    print("Edge TTS - Text to Speech (Microsoft Edge)")
    print("=" * 70)
    
    print(f"\nConfiguracoes:")
    print(f"  Texto: {TEXTO[:80]}...")
    print(f"  Voz: {VOZ}")
    print(f"  Velocidade: {VELOCIDADE}")
    print(f"  Arquivo: {ARQUIVO_SAIDA}")
    
    try:
        from edge_tts import Communicate
        
        print(f"\nCriando comunicador TTS...")
        communicate = Communicate(
            text=TEXTO,
            voice=VOZ,
            rate=VELOCIDADE,
            pitch=PITCH
        )
        
        print(f"Gerando audio...")
        inicio = time.time()
        
        await communicate.save(ARQUIVO_SAIDA)
        
        tempo = time.time() - inicio
        
        arquivo_path = Path(ARQUIVO_SAIDA)
        tamanho_mb = arquivo_path.stat().st_size / (1024 * 1024)
        
        print(f"\nSUCESSO!")
        print(f"=" * 70)
        print(f"\nInformacoes do audio:")
        print(f"  Arquivo: {ARQUIVO_SAIDA}")
        print(f"  Tamanho: {tamanho_mb:.2f} MB")
        print(f"  Tempo de geracao: {tempo:.2f} segundos")
        print(f"  Formato: MP3")
        
    except ImportError as e:
        print(f"\nERRO: Biblioteca 'edge-tts' nao encontrada.")
        print(f"Detalhes: {e}")
        print(f"\nInstale com:")
        print(f"   pip install edge-tts")
        return 1
        
    except Exception as e:
        print(f"\nERRO durante a geracao: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print(f"\n" + "=" * 70)
    print(f"Dicas:")
    print(f"  - Edite as variaveis no topo do script")
    print(f"  - Velocidade: '-10%' a '+10%'")
    print(f"\nReproduzir:")
    print(f"  Windows: start {ARQUIVO_SAIDA}")
    print(f"  Linux: ffplay {ARQUIVO_SAIDA}")
    print(f"=" * 70)
    
    return 0


def main():
    """Funcao principal."""
    if len(sys.argv) > 1 and sys.argv[1] == "--list-voices":
        print("Edge TTS - Vozes Populares\n")
        for voz, desc in listar_vozes_disponiveis().items():
            print(f"  {voz:25s} - {desc}")
        print(f"\nPara listar todas: edge-tts --list-voices")
        return 0
    
    return asyncio.run(gerar_audio())


if __name__ == "__main__":
    sys.exit(main())
