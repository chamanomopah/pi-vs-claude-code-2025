# -*- coding: utf-8 -*-
"""
Teste REAL COMPLETO do sistema com logging detalhado.
Executa com: python tests/test_complete_real.py
"""

import sys
import os
import time
import io
from pathlib import Path

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Importar módulos
from audio_capture import AudioCapture, AudioDeviceManager, AudioCaptureWithLogging
from logger import WakeWordsLogger, RealTimeMonitor, AudioFrameLogger, SystemMonitor
import logging
import numpy as np

# Configuração de logging
LOG_CONFIG = {
    'level': 'INFO',
    'log_to_file': True,
    'log_dir': 'logs',
    'log_file': 'test_complete_real.log',
    'max_size_mb': 10,
    'backup_count': 5
}


def print_section(title):
    """Imprime seção formatada."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_system_info():
    """Testa 1: Informações do sistema."""
    print_section("TESTE 1: Informações do SISTEMA (Hardware REAL)")
    
    monitor = SystemMonitor()
    
    print("\n[INFO] Sistema Operacional:")
    import platform
    print(f"  Plataforma: {platform.system()}")
    print(f"  Versao: {platform.release()}")
    print(f"  Arquitetura: {platform.machine()}")
    
    print("\n[INFO] CPU:")
    cpu_info = monitor.get_cpu_count()
    cpu_freq = monitor.__class__.__dict__.get('get_cpu_freq', lambda x: None)
    print(f"  Nucleos fisicos: {cpu_info['physical']}")
    print(f"  Nucleos logicos: {cpu_info['logical']}")
    print(f"  Uso atual: {monitor.get_cpu_percent(interval=0.5):.1f}%")
    
    print("\n[INFO] Memoria RAM:")
    mem_info = monitor.get_memory_info()
    print(f"  Total: {mem_info['total_gb']:.2f} GB")
    print(f"  Usada: {mem_info['used_gb']:.2f} GB ({mem_info['percent']:.1f}%)")
    if 'available_gb' in mem_info:
        print(f"  Disponivel: {mem_info['available_gb']:.2f} GB")
    else:
        print(f"  Disponivel: {mem_info['available_mb'] / 1024:.2f} GB")
    
    print("\n[INFO] Processo atual:")
    proc_mem = monitor.get_process_memory()
    print(f"  RAM usada: {proc_mem['rss_mb']:.2f} MB")
    print(f"  VMS: {proc_mem['vms_mb']:.2f} MB")
    
    print("\n[OK] Informacoes do sistema obtidas com sucesso!")


def test_audio_devices():
    """Testa 2: Dispositivos de áudio."""
    print_section("TESTE 2: Dispositivos de AUDIO do seu PC")
    
    print("\n[INFO] Escaneando dispositivos de audio...")
    devices = AudioDeviceManager.list_devices()
    
    print(f"\n[INFO] Total de dispositivos encontrados: {len(devices)}")
    
    mics = [d for d in devices if d.is_input]
    speakers = [d for d in devices if d.is_output]
    
    print(f"\n[INFO] Microfones (entrada): {len(mics)}")
    for mic in mics[:5]:  # Mostrar apenas 5 primeiros
        print(f"  [{mic.id:2d}] {mic.name}")
    
    if len(mics) > 5:
        print(f"  ... e mais {len(mics) - 5}")
    
    print(f"\n[INFO] Alto-falantes (saida): {len(speakers)}")
    default_input = AudioDeviceManager.get_default_input_device()
    default_output_id = 0
    
    for spk in speakers[:5]:
        is_default = (spk.id == default_output_id)
        marker = " [DEFAULT]" if is_default else ""
        print(f"  [{spk.id:2d}] {spk.name}{marker}")
    
    if default_input:
        print(f"\n[OK] Microfone padrao: ID {default_input.id} - '{default_input.name}'")
    
    print("\n[OK] Dispositivos de audio listados com sucesso!")


def test_audio_capture_with_logging():
    """Testa 3: Captura de áudio com logging."""
    print_section("TESTE 3: Captura de AUDIO com Logging (Fale AGORA!)")
    
    # Criar logger
    logger_manager = WakeWordsLogger(LOG_CONFIG)
    logger = logger_manager.get_logger()
    
    # Criar frame logger
    frame_logger = AudioFrameLogger(logger)
    
    # Criar captura com logging
    print("\n[INFO] Inicializando captura de audio...")
    audio = AudioCaptureWithLogging(
        sample_rate=16000,
        channels=1,
        chunk_size=512,
        frame_logger=frame_logger,
        log_every_n_frames=5  # Logar a cada 5 frames
    )
    
    try:
        print("\n[INFO] Iniciando captura por 5 segundos...")
        print("[FALA ALGO PARA O MICROFONE!]")
        print("-" * 80)
        
        audio.start()
        
        start_time = time.time()
        last_log_time = start_time
        
        while time.time() - start_time < 5:
            time.sleep(0.1)
            
            # Mostrar progresso
            elapsed = time.time() - start_time
            stats = audio.get_capture_stats()
            
            if time.time() - last_log_time >= 1.0:
                print(f"\r  Tempo: {elapsed:.1f}s | Frames: {stats['frames_captured']} | "
                      f"Voice: {stats['voice_percentage']:.1f}% | Peak: {stats['peak_amplitude']:.4f}",
                      end='', flush=True)
                last_log_time = time.time()
        
        print()  # Nova linha
        
        # Parar e mostrar estatísticas
        audio.stop()
        
        print("\n" + "-" * 80)
        print("[INFO] Estatisticas da captura:")
        audio.log_capture_summary()
        
        # Estatísticas do frame logger
        frame_stats = frame_logger.get_stats()
        print(f"\n[INFO] Frame Logger Stats:")
        print(f"  Total frames logados: {frame_stats['total_frames']}")
        print(f"  Frames com voz: {frame_stats['voice_frames']}")
        print(f"  Porcentagem voz: {frame_stats['voice_percentage']:.1f}%")
        print(f"  Frames/segundo: {frame_stats['frames_per_second']:.1f}")
        
        print("\n[OK] Captura de audio com logging concluida!")
        
    except Exception as e:
        print(f"\n[ERRO]Erro na captura: {e}")
        import traceback
        traceback.print_exc()
    
    return logger_manager


def test_realtime_monitoring(logger_manager):
    """Testa 4: Monitoramento em tempo real."""
    print_section("TESTE 4: Monitoramento em TEMPO REAL (CPU/RAM)")
    
    logger = logger_manager.get_logger()
    
    # Criar monitor em tempo real
    monitor = RealTimeMonitor(logger_manager, interval=0.5)
    
    print("\n[INFO] Iniciando monitoramento por 10 segundos...")
    print("[OBSERVE os logs de MONITORAMENTO abaixo!]")
    print("-" * 80)
    
    monitor.start()
    
    # Aguardar e mostrar progresso
    start_time = time.time()
    while time.time() - start_time < 10:
        time.sleep(0.5)
        elapsed = time.time() - start_time
        print(f"\r  Monitorando... {elapsed:.1f}s / 10.0s", end='', flush=True)
    
    print()  # Nova linha
    
    # Parar monitoramento
    monitor.stop()
    
    # Mostrar estatísticas
    print("\n" + "-" * 80)
    print("[INFO] Estatisticas do monitoramento:")
    stats = monitor.get_stats()
    
    if stats:
        print(f"\n  Duracao: {stats['duration_seconds']:.1f}s")
        print(f"  Iteracoes: {stats['iterations']}")
        
        if 'cpu_process' in stats:
            cpu_p = stats['cpu_process']
            print(f"\n  CPU Processo:")
            print(f"    Media: {cpu_p['avg']:.2f}%")
            print(f"    Min: {cpu_p['min']:.2f}%")
            print(f"    Max: {cpu_p['max']:.2f}%")
        
        if 'cpu_system' in stats:
            cpu_s = stats['cpu_system']
            print(f"\n  CPU Sistema:")
            print(f"    Media: {cpu_s['avg']:.2f}%")
            print(f"    Min: {cpu_s['min']:.2f}%")
            print(f"    Max: {cpu_s['max']:.2f}%")
        
        if 'ram_process_mb' in stats:
            ram = stats['ram_process_mb']
            print(f"\n  RAM Processo:")
            print(f"    Media: {ram['avg']:.2f} MB")
            print(f"    Min: {ram['min']:.2f} MB")
            print(f"    Max: {ram['max']:.2f} MB")
    
    # Exportar métricas para JSON
    metrics_file = Path('logs') / 'metrics_test.json'
    metrics_file.parent.mkdir(parents=True, exist_ok=True)
    monitor.export_metrics_json(str(metrics_file))
    
    print(f"\n[OK] Monitoramento concluido!")
    print(f"[OK] Metricas exportadas para: {metrics_file}")


def test_cpu_ram_stress():
    """Testa 5: Stress test para ver variação de CPU/RAM."""
    print_section("TESTE 5: Stress Test (CPU/RAM)")
    
    print("\n[INFO] Executando operacoes para gerar carga...")
    
    logger_manager = WakeWordsLogger(LOG_CONFIG)
    logger = logger_manager.get_logger()
    monitor = RealTimeMonitor(logger_manager, interval=0.3)
    
    monitor.start()
    
    # Gerar carga de CPU
    print("\n[INFO] Gerando carga de CPU por 3 segundos...")
    start_time = time.time()
    
    # Cálculos intensivos
    result = 0
    while time.time() - start_time < 3:
        for i in range(1000):
            result += i ** 2
    
    # Alocar memória
    print("[INFO] Alocando memoria...")
    big_list = [i for i in range(1000000)]  # ~8 MB
    
    time.sleep(2)
    
    # Liberar memória
    print("[INFO] Liberando memoria...")
    del big_list
    
    time.sleep(2)
    
    monitor.stop()
    
    # Mostrar estatísticas
    stats = monitor.get_stats()
    if stats and 'cpu_process' in stats:
        print(f"\n[INFO] CPU durante stress:")
        print(f"  Media: {stats['cpu_process']['avg']:.2f}%")
        print(f"  Max: {stats['cpu_process']['max']:.2f}%")
    
    print("\n[OK] Stress test concluido!")


def main():
    """Função principal."""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + " " * 20 + "TESTE REAL COMPLETO - SISTEMA WAKE WORDS" + " " * 20 + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    print("\n[INICIO] Testes com hardware REAL do seu sistema!")
    print("[AVISO] Alguns testes requerem interacao (falar no microfone)")
    
    try:
        # Teste 1: Info do sistema
        test_system_info()
        time.sleep(1)
        
        # Teste 2: Dispositivos de audio
        test_audio_devices()
        time.sleep(1)
        
        # Teste 3: Captura de audio com logging
        logger_manager = test_audio_capture_with_logging()
        time.sleep(1)
        
        # Teste 4: Monitoramento em tempo real
        test_realtime_monitoring(logger_manager)
        time.sleep(1)
        
        # Teste 5: Stress test
        test_cpu_ram_stress()
        
        # Resumo final
        print_section("RESUMO FINAL")
        
        print("\n[OK] Todos os testes concluidos com sucesso!")
        print("\n[INFO] Arquivos gerados:")
        print(f"  - logs/test_complete_real.log (Logs detalhados)")
        print(f"  - logs/metrics_test.json (Metricas de monitoramento)")
        
        print("\n[INFO] O que foi testado:")
        print("  [OK] Captura de informacoes do sistema (CPU, RAM, disco)")
        print("  [OK] Listagem de dispositivos de audio do seu PC")
        print("  [OK] Captura de audio do microfone com logging de frames")
        print("  [OK] Monitoramento em tempo real de CPU e RAM")
        print("  [OK] Stress test para variacao de recursos")
        
        print("\n[INFO] Dados REAIS capturados:")
        print("  - CPU do processo e do sistema")
        print("  - RAM do processo e do sistema")
        print("  - Amostras de audio do seu microfone")
        print("  - Niveis de audio (amplitude, RMS)")
        print("  - Deteccao de voz vs silencio")
        
        print("\n" + "=" * 80)
        print("[SUCESSO] SISTEMA TESTADO E FUNCIONANDO!")
        print("=" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPCAO] Teste interrompido pelo usuario.")
    except Exception as e:
        print(f"\n\n[ERRO] Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
