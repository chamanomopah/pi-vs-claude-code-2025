#!/usr/bin/env python3
"""
Kokoro-82M TTS - Exemplo com Múltiplas Vozes
Demonstra como usar diferentes vozes do Kokoro

Instalação:
    pip install -U kokoro-onnx soundfile
"""

import soundfile as sf
from kokoro_onnx import Kokoro

# Inicializar Kokoro
print("Carregando Kokoro-82M...")
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
print("✅ Pronto!\n")

# Texto de exemplo
texto = "This is a demonstration of Kokoro-82M text-to-speech with different voices."

# Lista de vozes para testar
vozes = [
    ("af_heart", "Feminino Americano - Melhor Qualidade ⭐"),
    ("af_bella", "Feminino Americano - Excelente 🔥"),
    ("af_nicole", "Feminino Americano - Bom"),
    ("am_michael", "Masculino Americano - Melhor ⭐"),
    ("am_fenrir", "Masculino Americano - Bom"),
    ("bf_emma", "Feminino Britânico"),
    ("bm_george", "Masculino Britânico"),
]

# Gerar áudio para cada voz
print("🎙️ Gerando áudios...\n")
for voz, descricao in vozes:
    print(f"🔊 Gerando: {voz} - {descricao}")
    
    samples, sample_rate = kokoro.create(
        texto,
        voice=voz,
        speed=1.0,
        lang="en-us"
    )
    
    arquivo = f"kokoro_{voz}.wav"
    sf.write(arquivo, samples, sample_rate)
    print(f"   ✅ Salvo: {arquivo}")
    print()

print("🎉 Todos os áudios foram gerados!")
print("💡 Abra os arquivos para comparar as vozes!")
