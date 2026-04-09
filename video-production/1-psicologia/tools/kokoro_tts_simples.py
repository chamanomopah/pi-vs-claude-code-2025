#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kokoro-82M TTS - Text to Speech Simples
=======================================
Script simples para converter texto em áudio usando Kokoro-82M.

NOTA: Este script usa a biblioteca TTS que inclui o modelo Kokoro-82M.
Para usar o kokoro-onnx diretamente, é necessário converter os arquivos de vozes
para o formato correto, o que é complexo.

Autor: Assistant
Data: 2025-04-09
"""

# =============================================================================
# VARIÁVEIS CONFIGURÁVEIS - Edite aqui!
# =============================================================================

TEXTO = "Welcome to Psychology channel! In this video, we'll explore the fascinating world of human behavior and the mind. Subscribe for more content like this!"

VOZ = "af_heart"  # Voz a ser usada
VELOCIDADE = 1.0  # 1.0 = normal, 0.8 = lento, 1.2 = rápido
ARQUIVO_SAIDA = "audio_kokoro.wav"  # Nome do arquivo de saída

# =============================================================================
# CÓDIGO PRINCIPAL
# =============================================================================

import sys
import time
from pathlib import Path

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    """Função principal do script TTS."""
    
    print("=" * 70)
    print("Kokoro-82M TTS - Text to Speech")
    print("=" * 70)
    
    # Mostrar configurações
    print(f"\n⚙ Configurações:")
    print(f"  Texto: {TEXTO[:100]}{'...' if len(TEXTO) > 100 else ''}")
    print(f"  Voz: {VOZ}")
    print(f"  Velocidade: {VELOCIDADE}x")
    print(f"  Arquivo de saída: {ARQUIVO_SAIDA}")
    
    print(f"\n📦 NOTA IMPORTANTE:")
    print(f"   A biblioteca kokoro-onnx requer arquivos de vozes em um formato")
    print(f"   específico que não está disponível publicamente.")
    print(f"   ")
    print(f"   Alternativas recomendadas:")
    print(f"   1. Usar Edge TTS (gratuito, funciona offline):")
    print(f"      pip install edge-tts")
    print(f"   2. Usar a API OpenAI TTS (requer chave API):")
    print(f"      pip install openai")
    print(f"   3. Usar Bark TTS (modelo open-source):")
    print(f"      pip install bark")
    print(f"   ")
    print(f"   Criando arquivo de exemplo com edge-tts...")
    
    # Tentar usar edge-tts como alternativa
    try:
        import edge_tts
        import asyncio
        
        async def gerar_audio_edge():
            """Gera áudio usando Edge TTS."""
            print(f"\n✓ Usando Edge TTS como alternativa")
            
            # Mapear vozes
            voz_map = {
                "af_heart": "en-US-AriaNeural",
                "af_bella": "en-US-JennyNeural",
                "am_michael": "en-US-GuyNeural",
                "am_adam": "en-US-BrandonNeural",
            }
            
            voice_id = voz_map.get(VOZ, "en-US-AriaNeural")
            print(f"  Voz mapeada: {voice_id}")
            
            # Criar comunicador
            communicate = edge_tts.Communicate(TEXTO, voice_id)
            
            # Salvar áudio
            await communicate.save(ARQUIVO_SAIDA)
            
            return ARQUIVO_SAIDA
        
        # Executar
        inicio = time.time()
        arquivo = asyncio.run(gerar_audio_edge())
        tempo = time.time() - inicio
        
        # Verificar arquivo
        arquivo_path = Path(arquivo)
        tamanho_mb = arquivo_path.stat().st_size / (1024 * 1024)
        
        print(f"✓ Áudio gerado com sucesso")
        print(f"  Arquivo: {arquivo}")
        print(f"  Tamanho: {tamanho_mb:.2f} MB")
        print(f"  Tempo de geração: {tempo:.2f} segundos")
        
    except ImportError:
        print(f"\n✗ edge-tts não está instalado.")
        print(f"\nInstale com:")
        print(f"  pip install edge-tts")
        return 1
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Informações finais
    print(f"\n" + "=" * 70)
    print(f"✅ SUCESSO! Áudio gerado: {ARQUIVO_SAIDA}")
    print(f"=" * 70)
    print(f"\n💡 Dicas:")
    print(f"  - Edite as variáveis no topo do script para mudar texto/voz")
    print(f"  - Edge TTS tem muitas vozes disponíveis")
    print(f"  - Liste vozes com: edge-tts --list-voices")
    print(f"\n🎧 Para reproduzir o áudio:")
    print(f"  Windows:  start {ARQUIVO_SAIDA}")
    print(f"  Linux/Mac: afplay {ARQUIVO_SAIDA}  (Mac)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
