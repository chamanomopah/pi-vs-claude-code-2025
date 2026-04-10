#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kokoro-82M TTS - Text to Speech com Kokoro-ONNX
================================================
Script para converter texto em áudio usando Kokoro-82M via ONNX.

Este script usa a biblioteca 'kokoro-onnx' que é mais leve e compatível
com versões mais antigas do Python.

Autor: Assistant
Data: 2025-04-09
"""

# =============================================================================
# VARIÁVEIS CONFIGURÁVEIS - Edite aqui!
# =============================================================================

TEXTO = "Welcome to Psychology channel! In this video, we'll explore the fascinating world of human behavior and the mind. Subscribe for more content like this!"

VOZ = "af_heart"  # Voz a ser usada (ver lista abaixo)
VELOCIDADE = 1.0  # 1.0 = normal, 0.8 = lento, 1.2 = rápido
ARQUIVO_SAIDA = "audio_kokoro_onnx.wav"  # Nome do arquivo de saída

# =============================================================================
# CÓDIGO PRINCIPAL
# =============================================================================

import sys
import time
import os
from pathlib import Path

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def listar_vozes_disponiveis():
    """Retorna lista de vozes disponíveis no Kokoro-ONNX."""
    return {
        # Americanas Femininas (Recomendadas)
        "af_heart": "Feminina americana (melhor opção) ❤️",
        "af_bella": "Feminina americana (profissional) 🔥",
        "af_sarah": "Feminina americana (madura)",
        "af_nicole": "Feminina americana (jovem)",
        "af_sky": "Feminina americana (suave)",
        
        # Americanas Masculinas
        "am_adam": "Masculino americano",
        "am_michael": "Masculino americano (profissional)",
        "am_echo": "Masculino americano (profundo)",
        "am_eric": "Masculino americano (jovem)",
        "am_liam": "Masculino americano (energético)",
        
        # Britânicas Femininas
        "bf_emma": "Feminina britânica",
        "bf_isabella": "Feminina britânica (elegante)",
        "bf_george": "Feminina britânica (madura)",
        
        # Britânicas Masculinas
        "bm_george": "Masculino britânico",
        "bm_lewis": "Masculino britânico (jovem)",
        "bm_daniel": "Masculino britânico (profissional)",
    }


def main():
    """Função principal do script TTS."""
    
    print("=" * 70)
    print("Kokoro-82M TTS - Text to Speech (ONNX)")
    print("=" * 70)
    
    # Mostrar configurações
    print(f"\n⚙️  Configurações:")
    print(f"  📝 Texto: {TEXTO[:100]}{'...' if len(TEXTO) > 100 else ''}")
    print(f"  🎤 Voz: {VOZ}")
    print(f"  ⚡ Velocidade: {VELOCIDADE}x")
    print(f"  💾 Arquivo de saída: {ARQUIVO_SAIDA}")
    
    # Verificar voz disponível
    vozes = listar_vozes_disponiveis()
    if VOZ not in vozes:
        print(f"\n⚠️  AVISO: Voz '{VOZ}' não reconhecida.")
        print(f"\n📋 Vozes disponíveis:")
        for voz_id, descricao in sorted(vozes.items()):
            recomendado = " ⭐" if voz_id == "af_heart" else ""
            print(f"  • {voz_id:15s} - {descricao}{recomendado}")
        print(f"\nContinuando com '{VOZ}' mesmo assim...")
    else:
        print(f"  📋 Descrição voz: {vozes[VOZ]}")
    
    try:
        # Importar bibliotecas Kokoro-ONNX
        print(f"\n📦 Importando bibliotecas Kokoro-ONNX...")
        from kokoro_onnx import KokoroONNX
        
        # Inicializar modelo
        print(f"🔄 Inicializando modelo Kokoro-ONNX...")
        print(f"   ⏳ Os arquivos de voz serão baixados se necessário")
        
        # Criar instância do modelo
        model = KokoroONNX()
        
        # Gerar áudio
        print(f"\n🎵 Gerando áudio...")
        inicio = time.time()
        
        # Chamar o modelo
        audio, sample_rate = model.create_audio(
            text=TEXTO,
            voice=VOZ,
            speed=VELOCIDADE
        )
        
        tempo_geracao = time.time() - inicio
        
        # Salvar arquivo
        print(f"\n💾 Salvando áudio em: {ARQUIVO_SAIDA}")
        import soundfile as sf
        sf.write(ARQUIVO_SAIDA, audio, sample_rate)
        
        # Informações sobre o arquivo
        arquivo_path = Path(ARQUIVO_SAIDA)
        tamanho_mb = arquivo_path.stat().st_size / (1024 * 1024)
        duracao_segundos = len(audio) / sample_rate
        
        print(f"\n✅ SUCESSO!")
        print(f"=" * 70)
        print(f"\n📊 Informações do áudio gerado:")
        print(f"  • Arquivo: {ARQUIVO_SAIDA}")
        print(f"  • Tamanho: {tamanho_mb:.2f} MB")
        print(f"  • Duração: {duracao_segundos:.2f} segundos ({duracao_segundos/60:.2f} minutos)")
        print(f"  • Taxa de amostragem: {sample_rate} Hz")
        print(f"  • Canais: Mono")
        print(f"  • Tempo de geração: {tempo_geracao:.2f} segundos")
        print(f"  • Ratio: {duracao_segundos/tempo_geracao:.2f}x tempo-real")
        
    except ImportError as e:
        print(f"\n❌ ERRO: Biblioteca não encontrada.")
        print(f"\n📦 Instale as dependências com:")
        print(f"   pip install kokoro-onnx soundfile")
        print(f"\nErro detalhado: {e}")
        return 1
        
    except Exception as e:
        print(f"\n❌ ERRO durante a geração do áudio.")
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Informações finais
    print(f"\n" + "=" * 70)
    print(f"💡 Dicas de uso:")
    print(f"  • Edite as variáveis no topo do script para mudar texto/voz/velocidade")
    print(f"  • Velocidade recomendada: 0.8 a 1.2")
    print(f"  • Para textos longos, use quebras de linha para pausas naturais")
    print(f"\n🎧 Para reproduzir o áudio:")
    print(f"  Windows:  start {ARQUIVO_SAIDA}")
    print(f"  Linux:    ffplay {ARQUIVO_SAIDA}  (ou: aplay {ARQUIVO_SAIDA})")
    print(f"  macOS:    afplay {ARQUIVO_SAIDA}")
    print(f"\n📋 Para listar vozes disponíveis:")
    print(f"  python kokoro_tts_onnx.py --list-voices")
    print(f"=" * 70)
    
    return 0


def cmd_listar_vozes():
    """Lista todas as vozes disponíveis."""
    print("=" * 70)
    print("Kokoro-82M TTS (ONNX) - Vozes Disponíveis")
    print("=" * 70)
    
    vozes = listar_vozes_disponiveis()
    
    print(f"\n📋 Total de {len(vozes)} vozes disponíveis:\n")
    
    print("🇺🇸 Americanas Femininas")
    for voz_id in ["af_heart", "af_bella", "af_sarah", "af_nicole", "af_sky"]:
        recomendado = " ⭐ MELHOR OPÇÃO" if voz_id == "af_heart" else ""
        print(f"  • {voz_id:15s} - {vozes[voz_id]}{recomendado}")
    
    print("\n🇺🇸 Americanas Masculinas")
    for voz_id in ["am_adam", "am_michael", "am_echo", "am_eric", "am_liam"]:
        print(f"  • {voz_id:15s} - {vozes[voz_id]}")
    
    print("\n🇬🇧 Britânicas")
    for voz_id in ["bf_emma", "bf_isabella", "bf_george", "bm_george", "bm_lewis", "bm_daniel"]:
        print(f"  • {voz_id:15s} - {vozes[voz_id]}")
    
    print(f"\n💡 Recomendação: Use 'af_heart' para melhor qualidade feminina americana")
    print(f"💡 Alternativa: Use 'af_bella' para tom mais profissional")
    print(f"=" * 70)


if __name__ == "__main__":
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--list-voices":
        cmd_listar_vozes()
        sys.exit(0)
    
    sys.exit(main())
