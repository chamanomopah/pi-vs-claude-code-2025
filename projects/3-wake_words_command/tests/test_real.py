"""
Testes REAIS do sistema Wake Words.
Testa hardware real: microfone, CPU, RAM, etc.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import sounddevice as sd
import psutil
import platform
import time
import numpy as np
import argparse
from datetime import datetime


def print_system_info():
    """Imprime informações completas do sistema."""
    print("\n" + "=" * 80)
    print("INFORMAÇÕES DO SISTEMA")
    print("=" * 80)
    
    # Sistema operacional
    print(f"\n🖥️  Sistema Operacional:")
    print(f"   Plataforma: {platform.system()}")
    print(f"   Versão: {platform.release()}")
    print(f"   Arquitetura: {platform.machine()}")
    print(f"   Processador: {platform.processor()}")
    
    # CPU
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(interval=0.5)
    
    print(f"\n⚡ CPU:")
    print(f"   Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"   Núcleos lógicos: {cpu_count}")
    print(f"   Frequência: {cpu_freq.current:.0f} MHz")
    print(f"   Frequência max: {cpu_freq.max:.0f} MHz")
    print(f"   Uso atual: {cpu_percent}%")
    
    # Memória
    mem = psutil.virtual_memory()
    
    print(f"\n🧠 Memória RAM:")
    print(f"   Total: {mem.total / (1024**3):.2f} GB")
    print(f"   Disponível: {mem.available / (1024**3):.2f} GB")
    print(f"   Usada: {mem.used / (1024**3):.2f} GB")
    print(f"   Percentual: {mem.percent}%")
    
    # Disco
    disk = psutil.disk_usage('/')
    
    print(f"\n💾 Disco (C:):")
    print(f"   Total: {disk.total / (1024**3):.2f} GB")
    print(f"   Livre: {disk.free / (1024**3):.2f} GB")
    print(f"   Usado: {disk.used / (1024**3):.2f} GB")
    print(f"   Percentual: {disk.percent}%")
    
    # Rede
    print(f"\n🌐 Rede:")
    net_io = psutil.net_io_counters()
    print(f"   Bytes enviados: {net_io.bytes_sent / (1024**2):.2f} MB")
    print(f"   Bytes recebidos: {net_io.bytes_recv / (1024**2):.2f} MB")
    
    # Processo atual
    process = psutil.Process()
    proc_mem = process.memory_info()
    
    print(f"\n📊 Processo Atual (PID {process.pid}):")
    print(f"   RAM usada: {proc_mem.rss / (1024**2):.2f} MB")
    print(f"   VMS: {proc_mem.vms / (1024**2):.2f} MB")
    print(f"   Threads: {process.num_threads()}")
    print(f"   Arquivos abertos: {len(process.open_files())}")
    
    print("\n" + "=" * 80)


def list_audio_devices():
    """Lista todos os dispositivos de áudio do sistema."""
    print("\n" + "=" * 80)
    print("DISPOSITIVOS DE ÁUDIO DO SISTEMA")
    print("=" * 80)
    
    try:
        devices = sd.query_devices()
        
        print(f"\n{'ID':<4} | {'Nome':<40} | {'Entradas':>8} | {'Saídas':>8} | {'Taxa Hz':>10}")
        print("-" * 80)
        
        for idx, dev in enumerate(devices):
            name = dev['name'][:40]
            inputs = dev['max_input_channels']
            outputs = dev['max_output_channels']
            rate = int(dev['default_samplerate'])
            
            marker = ""
            if inputs > 0:
                marker += " 🎤"
            if outputs > 0:
                marker += " 🔈"
            
            print(f"{idx:<4} | {name:<40} | {inputs:>8} | {outputs:>8} | {rate:>10}{marker}")
        
        print("-" * 80)
        
        # Dispositivo padrão
        default_input = sd.query_devices(kind='input')
        default_output = sd.query_devices(kind='output')
        
        print(f"\n🎤 Dispositivo de ENTRADA padrão: {default_input['name']} (ID {default_input['index']})")
        print(f"🔈 Dispositivo de SAÍDA padrão: {default_output['name']} (ID {default_output['index']})")
        
        # Host APIs
        print("\n📋 Host APIs disponíveis:")
        hostapis = sd.query_hostapis()
        for api in hostapis:
            print(f"   - {api['name']}")
        
    except Exception as e:
        print(f"❌ Erro ao listar dispositivos: {e}")
    
    print("=" * 80 + "\n")


def test_microphone(device_id=None, duration=5):
    """
    Testa a captura do microfone.
    
    Args:
        device_id: ID do dispositivo (None = padrão)
        duration: Duração do teste em segundos
    """
    print("\n" + "=" * 80)
    print(f"TESTE DE MICROFONE - {duration}s")
    print("=" * 80)
    
    if device_id is not None:
        device_info = sd.query_devices(device_id)
        print(f"\n🎤 Dispositivo: {device_info['name']}")
    else:
        print(f"\n🎤 Dispositivo: PADRÃO")
    
    print(f"⏱️  Duração: {duration} segundos")
    print("🔊 Fale algo agora...\n")
    
    try:
        # Configurar áudio
        sample_rate = 16000
        channels = 1
        chunk_size = 512
        
        # Buffer para armazenar áudio
        audio_buffer = []
        
        # Callback
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"⚠️  Status: {status}")
            audio_buffer.append(indata.copy())
        
        # Iniciar stream
        with sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype=np.int16,
            device=device_id,
            blocksize=chunk_size,
            callback=audio_callback
        ) as stream:
            print("🔴 Gravando...")
            print("-" * 80)
            
            # Monitorar em tempo real
            start_time = time.time()
            peak_level = 0
            
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                remaining = duration - elapsed
                
                # Calcular nível do áudio se tiver buffer
                if audio_buffer:
                    last_chunk = audio_buffer[-1]
                    level = np.sqrt(np.mean(np.square(last_chunk.astype(float)))) / 32768
                    peak_level = max(peak_level, level)
                    
                    # Barra visual
                    bar_length = int(level * 50)
                    bar = '█' * bar_length + '░' * (50 - bar_length)
                    
                    print(f"\r  [{bar}] {level:.4f} | ⏱️  {elapsed:.1f}s / {duration}s | 🔊 Peak: {peak_level:.4f}", end='', flush=True)
                
                time.sleep(0.1)
            
            print()  # Nova linha
        
        print("-" * 80)
        print("✅ Gravação completa!")
        
        # Estatísticas
        total_frames = sum(len(chunk) for chunk in audio_buffer)
        total_duration = total_frames / sample_rate
        
        print(f"\n📊 Estatísticas:")
        print(f"   Frames gravados: {total_frames}")
        print(f"   Duração total: {total_duration:.2f} segundos")
        print(f"   Chunks capturados: {len(audio_buffer)}")
        print(f"   Nível máximo: {peak_level:.4f}")
        
        # Converter para array
        if audio_buffer:
            audio_array = np.concatenate(audio_buffer, axis=0)
            
            # Calcular RMS
            rms = np.sqrt(np.mean(np.square(audio_array.astype(float)))) / 32768
            
            print(f"   RMS médio: {rms:.4f}")
            
            # Converter para dB
            if rms > 0:
                db = 20 * np.log10(rms)
                print(f"   Nível médio: {db:.2f} dB")
            
            # Salvar amostra se houver áudio suficiente
            if peak_level > 0.01:
                output_path = Path(__file__).parent.parent / "logs" / "test_recording.wav"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    import wave
                    with wave.open(str(output_path), 'wb') as wav_file:
                        wav_file.setnchannels(channels)
                        wav_file.setsampwidth(2)  # 16-bit
                        wav_file.setframerate(sample_rate)
                        wav_file.writeframes(audio_array.tobytes())
                    
                    print(f"\n💾 Áudio salvo em: {output_path}")
                except Exception as e:
                    print(f"\n⚠️  Erro ao salvar áudio: {e}")
            else:
                print("\n⚠️  Áudio muito baixo ou ausente")
        
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 80 + "\n")


def test_cpu_monitoring(duration=10):
    """
    Testa monitoramento de CPU.
    
    Args:
        duration: Duração do teste em segundos
    """
    print("\n" + "=" * 80)
    print(f"TESTE DE MONITORAMENTO DE CPU - {duration}s")
    print("=" * 80)
    print("📊 Monitorando uso da CPU em tempo real...\n")
    
    start_time = time.time()
    cpu_samples = []
    
    try:
        while time.time() - start_time < duration:
            # Medir CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_samples.append(cpu_percent)
            
            # CPU por núcleo
            cpu_per_core = psutil.cpu_percent(interval=0, percpu=True)
            
            # Barra visual
            bar_length = int(cpu_percent / 2)
            bar = '█' * bar_length + '░' * (50 - bar_length)
            
            elapsed = time.time() - start_time
            print(f"\r  CPU: [{bar}] {cpu_percent:5.1f}% | ⏱️  {elapsed:.1f}s", end='', flush=True)
            
            time.sleep(0.5)
        
        print()  # Nova linha
        
        # Estatísticas
        if cpu_samples:
            avg_cpu = sum(cpu_samples) / len(cpu_samples)
            min_cpu = min(cpu_samples)
            max_cpu = max(cpu_samples)
            
            print(f"\n📊 Estatísticas de CPU:")
            print(f"   Média: {avg_cpu:.1f}%")
            print(f"   Mínimo: {min_cpu:.1f}%")
            print(f"   Máximo: {max_cpu:.1f}%")
            print(f"   Amostras: {len(cpu_samples)}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    print("=" * 80 + "\n")


def test_memory_monitoring(duration=10):
    """
    Testa monitoramento de memória.
    
    Args:
        duration: Duração do teste em segundos
    """
    print("\n" + "=" * 80)
    print(f"TESTE DE MONITORAMENTO DE MEMÓRIA - {duration}s")
    print("=" * 80)
    print("📊 Monitorando uso de RAM em tempo real...\n")
    
    start_time = time.time()
    process = psutil.Process()
    initial_mem = process.memory_info().rss / (1024**2)
    
    try:
        while time.time() - start_time < duration:
            # Memória do sistema
            mem = psutil.virtual_memory()
            
            # Memória do processo
            proc_mem = process.memory_info().rss / (1024**2)
            mem_delta = proc_mem - initial_mem
            
            # Barra visual
            bar_length = int(mem.percent / 2)
            bar = '█' * bar_length + '░' * (50 - bar_length)
            
            elapsed = time.time() - start_time
            print(f"\r  RAM: [{bar}] {mem.percent:5.1f}% | Processo: {proc_mem:6.1f} MB ({mem_delta:+.1f}) | ⏱️  {elapsed:.1f}s", 
                  end='', flush=True)
            
            time.sleep(0.5)
        
        print()  # Nova linha
        
        # Info final
        final_mem = process.memory_info().rss / (1024**2)
        print(f"\n📊 Memória do Processo:")
        print(f"   Inicial: {initial_mem:.2f} MB")
        print(f"   Final: {final_mem:.2f} MB")
        print(f"   Delta: {final_mem - initial_mem:+.2f} MB")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    print("=" * 80 + "\n")


def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "🔬" * 40)
    print("SUITE COMPLETA DE TESTES - HARDWARE REAL")
    print("🔬" * 40)
    
    # Info do sistema
    print_system_info()
    
    # Dispositivos de áudio
    list_audio_devices()
    
    # Teste de microfone
    print("\n⏳ Iniciando teste de microfone em 3 segundos...")
    print("   Prepare-se para falar!\n")
    time.sleep(3)
    test_microphone(duration=5)
    
    # Monitoramento de CPU
    print("\n⏳ Iniciando teste de CPU...")
    time.sleep(1)
    test_cpu_monitoring(duration=5)
    
    # Monitoramento de RAM
    print("\n⏳ Iniciando teste de RAM...")
    time.sleep(1)
    test_memory_monitoring(duration=5)
    
    print("\n" + "✅" * 40)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("✅" * 40 + "\n")


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Testes REAIS do sistema Wake Words',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python tests/test_real.py --list-devices
  python tests/test_real.py --test-mic --duration 10
  python tests/test_real.py --test-cpu --duration 5
  python tests/test_real.py --all
        """
    )
    
    parser.add_argument('--list-devices', '-l',
                       action='store_true',
                       help='Listar dispositivos de áudio')
    parser.add_argument('--test-mic', '-m',
                       action='store_true',
                       help='Testar microfone')
    parser.add_argument('--device-id', '-d',
                       type=int,
                       default=None,
                       help='ID do dispositivo de áudio')
    parser.add_argument('--duration', '-t',
                       type=int,
                       default=5,
                       help='Duração dos testes (segundos)')
    parser.add_argument('--test-cpu', '-c',
                       action='store_true',
                       help='Testar monitoramento de CPU')
    parser.add_argument('--test-ram', '-r',
                       action='store_true',
                       help='Testar monitoramento de RAM')
    parser.add_argument('--all', '-a',
                       action='store_true',
                       help='Executar todos os testes')
    parser.add_argument('--system-info', '-s',
                       action='store_true',
                       help='Mostrar informações do sistema')
    
    args = parser.parse_args()
    
    # Executar testes
    if args.all:
        run_all_tests()
    elif args.list_devices:
        list_audio_devices()
    elif args.test_mic:
        test_microphone(device_id=args.device_id, duration=args.duration)
    elif args.test_cpu:
        test_cpu_monitoring(duration=args.duration)
    elif args.test_ram:
        test_memory_monitoring(duration=args.duration)
    elif args.system_info:
        print_system_info()
    else:
        # Default: mostrar info e listar dispositivos
        print_system_info()
        list_audio_devices()


if __name__ == '__main__':
    main()
