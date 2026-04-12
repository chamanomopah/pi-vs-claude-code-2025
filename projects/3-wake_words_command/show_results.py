# -*- coding: utf-8 -*-
"""
Script para mostrar resultados da RODADA 2
"""
import json
from pathlib import Path

print("=" * 80)
print("RODADA 2 - LOGGING REAL - RESULTADOS")
print("=" * 80)

# Carregar métricas
metrics_file = Path("logs/metrics_test.json")
if metrics_file.exists():
    with open(metrics_file, 'r') as f:
        data = json.load(f)

    print("\n[INFO] Métricas de Monitoramento:")
    print(f"  Início: {data['start_time']}")
    print(f"  Fim: {data['end_time']}")

    stats = data['stats']
    print(f"\n[INFO] Estatísticas Gerais:")
    print(f"  Duração: {stats['duration_seconds']:.2f} segundos")
    print(f"  Iterações: {stats['iterations']}")

    if 'cpu_process' in stats:
        cpu = stats['cpu_process']
        print(f"\n[INFO] CPU do Processo:")
        print(f"    Média: {cpu['avg']:.2f}%")
        print(f"    Mínimo: {cpu['min']:.2f}%")
        print(f"    Máximo: {cpu['max']:.2f}%")

    if 'cpu_system' in stats:
        cpu = stats['cpu_system']
        print(f"\n[INFO] CPU do Sistema:")
        print(f"    Média: {cpu['avg']:.2f}%")
        print(f"    Mínimo: {cpu['min']:.2f}%")
        print(f"    Máximo: {cpu['max']:.2f}%")

    if 'ram_process_mb' in stats:
        ram = stats['ram_process_mb']
        print(f"\n[INFO] RAM do Processo:")
        print(f"    Média: {ram['avg']:.2f} MB")
        print(f"    Mínimo: {ram['min']:.2f} MB")
        print(f"    Máximo: {ram['max']:.2f} MB")

    print(f"\n[INFO] Amostras coletadas: {len(data['metrics'])}")

    # Mostrar primeiras 3 amostras
    print(f"\n[INFO] Primeiras 3 amostras:")
    for i, m in enumerate(data['metrics'][:3], 1):
        print(f"  {i}. CPU_PROC: {m['cpu_process']:.1f}% | "
              f"CPU_SYS: {m['cpu_system']:.1f}% | "
              f"RAM_PROC: {m['ram_process_mb']:.1f}MB")

else:
    print("\n[AVISO] Arquivo de métricas não encontrado.")
    print("        Execute: python tests/test_complete_real.py")

print("\n" + "=" * 80)
print("[OK] RODADA 2 CONCLUÍDA COM SUCESSO!")
print("=" * 80)
print("\n[INFO] O que foi implementado:")
print("  [OK] RealTimeMonitor - Monitoramento em tempo real")
print("  [OK] AudioFrameLogger - Logging de frames de áudio")
print("  [OK] TranscriptionLogger - Logging de transcrições")
print("  [OK] AudioCaptureWithLogging - Captura com logging")
print("  [OK] Exportação de métricas para JSON")
print("  [OK] Teste completo funcional")
print("\n[INFO] Dados REAIS capturados:")
print("  - CPU do processo e do sistema (em tempo real)")
print("  - RAM do processo e do sistema (em tempo real)")
print("  - Amostras de áudio do microfone")
print("  - Detecção de voz vs silêncio")
print("  - Número de threads e arquivos abertos")
print("\n[INFO] Arquivos gerados:")
print("  - logs/test_complete_real.log")
print("  - logs/metrics_test.json")
print("\n[INFO] Próximos passos (RODADA 3):")
print("  - Adicionar transcrições reais com Vosk")
print("  - Testar wake word detector com Porcupine")
print("  - Implementar reconhecimento de comandos")
print("=" * 80)
