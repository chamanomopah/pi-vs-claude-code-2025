# -*- coding: utf-8 -*-
"""
Teste simples de listagem de dispositivos de audio
"""
import sounddevice as sd

print("=" * 80)
print("DISPOSITIVOS DE AUDIO DO SISTEMA")
print("=" * 80)

devices = sd.query_devices()

print(f"\n{'ID':<4} | {'Nome':<40} | {'Entradas':>8} | {'Saidas':>8} | {'Taxa Hz':>10}")
print("-" * 80)

for idx, dev in enumerate(devices):
    name = dev['name'][:40]
    inputs = dev['max_input_channels']
    outputs = dev['max_output_channels']
    rate = int(dev['default_samplerate'])
    
    marker = ""
    if inputs > 0:
        marker += " [MIC]"
    if outputs > 0:
        marker += " [SPK]"
    
    print(f"{idx:<4} | {name:<40} | {inputs:>8} | {outputs:>8} | {rate:>10}{marker}")

print("-" * 80)

default_input = sd.query_devices(kind='input')
default_output = sd.query_devices(kind='output')

print(f"\n[ENTRADA] Padrao: {default_input['name']} (ID {default_input['index']})")
print(f"[SAIDA] Padrao: {default_output['name']} (ID {default_output['index']})")

print("\nHost APIs disponíveis:")
hostapis = sd.query_hostapis()
for api in hostapis:
    print(f"   - {api['name']}")

print("=" * 80)
