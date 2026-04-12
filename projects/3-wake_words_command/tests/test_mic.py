# -*- coding: utf-8 -*-
"""
Teste simples de captura do microfone
"""
import sounddevice as sd
import numpy as np
import time

print("=" * 80)
print("TESTE DE MICROFONE")
print("=" * 80)

# Configuracoes
sample_rate = 16000
channels = 1
duration = 5  # segundos

print(f"\nDispositivo: PADRAO")
print(f"Taxa de amostragem: {sample_rate} Hz")
print(f"Canais: {channels}")
print(f"Duracao: {duration} segundos")
print("\n[Fale algo agora...]")
print("Gravando..." + "-" * 60)

# Buffer para armazenar audio
audio_buffer = []

# Callback
def audio_callback(indata, frames, time_info, status):
    if status:
        print(f"Status: {status}")
    audio_buffer.append(indata.copy())
    # Mostrar nivel
    level = np.sqrt(np.mean(np.square(indata.astype(float)))) / 32768
    bar_length = int(level * 50)
    bar = '#' * bar_length + '-' * (50 - bar_length)
    print(f"\r  [{bar}] {level:.4f}", end='', flush=True)

# Iniciar stream
with sd.InputStream(
    samplerate=sample_rate,
    channels=channels,
    dtype=np.int16,
    callback=audio_callback
) as stream:
    start_time = time.time()
    peak_level = 0
    
    while time.time() - start_time < duration:
        time.sleep(0.1)
        
        if audio_buffer:
            last_chunk = audio_buffer[-1]
            level = np.sqrt(np.mean(np.square(last_chunk.astype(float)))) / 32768
            peak_level = max(peak_level, level)

print()  # Nova linha
print("-" * 60)
print("Gravacao completa!")

# Estatisticas
if audio_buffer:
    total_frames = sum(len(chunk) for chunk in audio_buffer)
    total_duration = total_frames / sample_rate
    audio_array = np.concatenate(audio_buffer, axis=0)
    rms = np.sqrt(np.mean(np.square(audio_array.astype(float)))) / 32768
    
    print(f"\nEstatisticas:")
    print(f"  Frames gravados: {total_frames}")
    print(f"  Duracao total: {total_duration:.2f} segundos")
    print(f"  Chunks capturados: {len(audio_buffer)}")
    print(f"  Nivel maximo: {peak_level:.4f}")
    print(f"  RMS medio: {rms:.4f}")
    
    if rms > 0:
        db = 20 * np.log10(rms)
        print(f"  Nivel medio: {db:.2f} dB")
    
    if peak_level > 0.01:
        print(f"\n[OK] Microfone funcionando!")
    else:
        print(f"\n[ALERTA] Nivel de audio muito baixo ou ausente")
else:
    print("\n[ERRO] Nenhum audio capturado")

print("=" * 80)
