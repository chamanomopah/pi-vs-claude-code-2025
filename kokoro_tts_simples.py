#!/usr/bin/env python3
"""
Kokoro-82M TTS - Script Simples e Completo
Converta texto em áudio com Kokoro-82M (TTS local)

Instalação:
    pip install -U kokoro-onnx soundfile

Uso:
    python kokoro_tts_simples.py
"""

import soundfile as sf
from kokoro_onnx import Kokoro
import os

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO - Edite aqui
# ═══════════════════════════════════════════════════════════════

# Seu texto (pode ser várias linhas)
TEXTO = """
Hello! This is Kokoro-82M, an open-source text-to-speech model.
This audio was generated locally on your CPU, without any cloud API.
The quality is excellent and the sound is very natural.
"""

# Nome do arquivo de saída
ARQUIVO_SAIDA = "kokoro_audio.wav"

# Voz (veja lista abaixo)
# Feminino americano: af_heart (melhor), af_bella, af_nicole, af_sarah
# Masculino americano: am_michael (melhor), am_fenrir, am_puck
# Britânico: bf_emma, bm_george
VOZ = "af_heart"

# Velocidade (1.0 = normal, 0.5 = lento, 2.0 = rápido)
VELOCIDADE = 1.0

# Idioma ("en-us" = inglês americano, "en-gb" = inglês britânico)
IDIOMA = "en-us"

# ═══════════════════════════════════════════════════════════════
# CÓDIGO - Não precisa editar abaixo
# ═══════════════════════════════════════════════════════════════

def main():
    """Função principal do Kokoro TTS"""
    
    print("=" * 60)
    print("🎙️  Kokoro-82M TTS - Text to Speech Local")
    print("=" * 60)
    print()
    
    # Mostrar configuração
    print("⚙️  Configuração:")
    print(f"   📝 Texto: {TEXTO[:60]}...")
    print(f"   🎤 Voz: {VOZ}")
    print(f"   ⚡ Velocidade: {VELOCIDADE}x")
    print(f"   🌐 Idioma: {IDIOMA}")
    print(f"   💾 Arquivo: {ARQUIVO_SAIDA}")
    print()
    
    # Verificar se arquivos de modelo existem
    modelo_file = "kokoro-v1.0.onnx"
    voices_file = "voices-v1.0.bin"
    
    if not os.path.exists(modelo_file):
        print(f"❌ Erro: Arquivo '{modelo_file}' não encontrado!")
        print(f"   Faça download em:")
        print(f"   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx")
        return
    
    if not os.path.exists(voices_file):
        print(f"❌ Erro: Arquivo '{voices_file}' não encontrado!")
        print(f"   Faça download em:")
        print(f"   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin")
        return
    
    # Inicializar Kokoro
    print("⏳ Carregando modelo Kokoro-82M...")
    try:
        kokoro = Kokoro(modelo_file, voices_file)
        print("✅ Modelo carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return
    
    print()
    
    # Gerar áudio
    print("🔊 Gerando áudio...")
    try:
        samples, sample_rate = kokoro.create(
            TEXTO,
            voice=VOZ,
            speed=VELOCIDADE,
            lang=IDIOMA
        )
        print("✅ Áudio gerado!")
    except Exception as e:
        print(f"❌ Erro ao gerar áudio: {e}")
        return
    
    # Calcular estatísticas
    duracao_segundos = len(samples) / sample_rate
    duracao_minutos = duracao_segundos / 60
    
    # Salvar arquivo
    print()
    print(f"💾 Salvando em '{ARQUIVO_SAIDA}'...")
    try:
        sf.write(ARQUIVO_SAIDA, samples, sample_rate)
        print("✅ Arquivo salvo!")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return
    
    # Mostrar estatísticas
    print()
    print("📊 Estatísticas:")
    print(f"   📏 Duração: {duracao_segundos:.2f} segundos ({duracao_minutos:.2f} minutos)")
    print(f"   🔊 Sample rate: {sample_rate} Hz")
    print(f"   📈 Samples: {len(samples):,}")
    print(f"   📊 Tamanho: {os.path.getsize(ARQUIVO_SAIDA):,} bytes ({os.path.getsize(ARQUIVO_SAIDA)/1024/1024:.2f} MB)")
    print()
    
    print("=" * 60)
    print("🎉 SUCESSO! Áudio gerado com Kokoro-82M!")
    print("=" * 60)
    print()
    print(f"✨ Abra '{ARQUIVO_SAIDA}' para ouvir o áudio!")
    print()
    
    # Lista de vozes disponíveis
    print("💡 Dica: Vozes disponíveis para inglês:")
    print("   Feminino (americano): af_heart ⭐, af_bella, af_nicole, af_sarah")
    print("   Masculino (americano): am_michael ⭐, am_fenrir, am_puck")
    print("   Britânico: bf_emma, bm_george")
    print()

if __name__ == "__main__":
    main()
