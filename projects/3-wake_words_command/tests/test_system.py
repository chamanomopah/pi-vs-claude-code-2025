# -*- coding: utf-8 -*-
"""
Teste simples de monitoramento do sistema
"""
import psutil
import platform
import time

print("=" * 80)
print("INFORMACOES DO SISTEMA")
print("=" * 80)

# Sistema operacional
print(f"\nSistema Operacional:")
print(f"   Plataforma: {platform.system()}")
print(f"   Versao: {platform.release()}")
print(f"   Arquitetura: {platform.machine()}")
print(f"   Processador: {platform.processor()}")

# CPU
cpu_count = psutil.cpu_count()
cpu_freq = psutil.cpu_freq()
cpu_percent = psutil.cpu_percent(interval=0.5)

print(f"\nCPU:")
print(f"   Nucleos fisicos: {psutil.cpu_count(logical=False)}")
print(f"   Nucleos logicos: {cpu_count}")
print(f"   Frequencia: {cpu_freq.current:.0f} MHz")
print(f"   Frequencia max: {cpu_freq.max:.0f} MHz")
print(f"   Uso atual: {cpu_percent}%")

# Memoria
mem = psutil.virtual_memory()

print(f"\nMemoria RAM:")
print(f"   Total: {mem.total / (1024**3):.2f} GB")
print(f"   Disponivel: {mem.available / (1024**3):.2f} GB")
print(f"   Usada: {mem.used / (1024**3):.2f} GB")
print(f"   Percentual: {mem.percent}%")

# Disco
disk = psutil.disk_usage('C:')

print(f"\nDisco (C:):")
print(f"   Total: {disk.total / (1024**3):.2f} GB")
print(f"   Livre: {disk.free / (1024**3):.2f} GB")
print(f"   Usado: {disk.used / (1024**3):.2f} GB")
print(f"   Percentual: {disk.percent}%")

# Processo atual
process = psutil.Process()
proc_mem = process.memory_info()

print(f"\nProcesso Atual (PID {process.pid}):")
print(f"   RAM usada: {proc_mem.rss / (1024**2):.2f} MB")
print(f"   VMS: {proc_mem.vms / (1024**2):.2f} MB")
print(f"   Threads: {process.num_threads()}")

print("\n" + "=" * 80)
print("MONITORAMENTO EM TEMPO REAL (5 segundos)")
print("=" * 80)

start_time = time.time()
cpu_samples = []

while time.time() - start_time < 5:
    # Medir CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_samples.append(cpu_percent)
    
    # Memoria
    mem = psutil.virtual_memory()
    
    # Barra visual
    bar_length = int(cpu_percent / 2)
    bar = '#' * bar_length + '-' * (50 - bar_length)
    
    elapsed = time.time() - start_time
    print(f"\r  CPU: [{bar}] {cpu_percent:5.1f}% | RAM: {mem.percent:5.1f}% | Tempo: {elapsed:.1f}s", 
          end='', flush=True)
    
    time.sleep(0.5)

print()  # Nova linha

# Estatisticas finais
if cpu_samples:
    avg_cpu = sum(cpu_samples) / len(cpu_samples)
    min_cpu = min(cpu_samples)
    max_cpu = max(cpu_samples)
    
    print(f"\nEstatisticas de CPU:")
    print(f"   Media: {avg_cpu:.1f}%")
    print(f"   Minimo: {min_cpu:.1f}%")
    print(f"   Maximo: {max_cpu:.1f}%")

print("\n" + "=" * 80)
