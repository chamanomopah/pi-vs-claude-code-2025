#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Kokoro TTS com texto em português
"""

import sys
import os
import io

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from kokoro import KPipeline
import soundfile as sf

# Texto de teste em português
TEXTO = "Ola! Este e um teste do Kokoro TTS com texto em portugues."

print("Testando Kokoro TTS com português...")
print(f"Texto: {TEXTO}")

# Inicializar pipeline
print("Carregando modelo...")
pipeline = KPipeline(lang_code='a')  # 'a' = americano (funciona com outros idiomas)

# Gerar áudio
print("Gerando áudio...")
generator = pipeline(TEXTO, voice='af_heart', speed=1.0)

for i, (gs, ps, audio) in enumerate(generator):
    output_file = "teste_portugues.wav"
    sf.write(output_file, audio, 24000)
    print(f"✅ Áudio salvo em: {output_file}")
    print(f"   Duração: {len(audio) / 24000:.2f} segundos")
    break

print("\n✅ Teste concluído!")
print("\n⚠️  Nota: Kokoro TTS é otimizado para inglês americano.")
print("   Para português, considere usar Edge TTS (edge_tts_simple.py)")
