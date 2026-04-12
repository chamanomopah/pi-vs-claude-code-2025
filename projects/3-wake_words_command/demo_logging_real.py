# -*- coding: utf-8 -*-
"""
Demonstração de Logging REAL Avançado
Sistema completo com dashboard em tempo real e logging estruturado.

Execute: python demo_logging_real.py
"""

import sys
import time
import signal
from pathlib import Path
from datetime import datetime

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import sounddevice as sd
import numpy as np
import psutil
import threading
import queue

from logger import WakeWordsLogger
from structured_logger import StructuredLogger
from realtime_dashboard import RealtimeDashboard


class AdvancedLoggingDemo:
    """Demonstração completa de logging avançado."""
    
    def __init__(self):
        """Inicializa demo."""
        # Configuração de logging
        log_config = {
            'level': 'INFO',
            'log_to_file': True,
            'log_dir': 'logs',
            'log_file': 'demo_advanced.log'
        }
        
        # Inicializar sistemas
        self.logger_manager = WakeWordsLogger(log_config)
        self.logger = self.logger_manager.get_logger()
        self.struct_logger = StructuredLogger()
        self.dashboard = RealtimeDashboard()
        
        # Estado
        self.running = False
        self.audio_queue = queue.Queue()
        
        # Configurar signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("="*80)
        self.logger.info(" DEMONSTRAÇÃO DE LOGGING REAL AVANÇADO")
        self.logger.info("="*80)
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de encerramento."""
        self.logger.info(f"Recebido sinal {signum}, encerrando...")
        self.running = False
    
    def audio_callback(self, indata, frames, time_info, status):
        """
        Callback para captura de áudio.
        
        Args:
            indata: Array numpy com dados do áudio
            frames: Número de frames
            time_info: Informações de tempo
            status: Status do stream
        """
        if status:
            self.logger.warning(f"Status do stream: {status}")
        
        # Colocar na fila para processamento
        self.audio_queue.put(indata.copy())
    
    def process_audio_frame(self, frame_data, frame_num):
        """
        Processa um frame de áudio.
        
        Args:
            frame_data: Array numpy com dados
            frame_num: Número do frame
        """
        # Converter para float se necessário
        if frame_data.dtype == np.int16:
            frame_float = frame_data.astype(float) / 32768.0
        else:
            frame_float = frame_data
        
        # Calcular métricas reais
        rms = np.sqrt(np.mean(frame_float ** 2))
        peak = np.abs(frame_float).max()
        
        # Detectar voz (limiar ajustável)
        is_voice = rms > 0.01
        
        # Logging estruturado
        self.struct_logger.log_audio_frame(
            frame_num, peak, rms, is_voice, len(frame_data)
        )
        
        # Atualizar dashboard
        self.dashboard.update(audio_data=frame_float, is_voice=is_voice)
        
        return is_voice, rms
    
    def monitor_system(self):
        """Thread que monitora o sistema em background."""
        while self.running:
            try:
                # Capturar métricas REAIS do sistema
                cpu = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory()
                ram_mb = mem.used / (1024 * 1024)
                ram_percent = mem.percent
                
                # Log estruturado
                self.struct_logger.log_system_metrics(
                    cpu, ram_mb, ram_percent
                )
                
                time.sleep(1.0)  # Atualizar a cada segundo
                
            except Exception as e:
                self.logger.error(f"Erro no monitoramento: {e}")
                break
    
    def run_demo(self, duration: int = 30):
        """
        Executa demonstração.
        
        Args:
            duration: Duração em segundos
        """
        print("\n" + "="*80)
        print(" DEMONSTRAÇÃO DE LOGGING REAL AVANÇADO")
        print("="*80)
        print("\nEste sistema captura dados REAIS do seu PC:")
        print(" ✅ Áudio do microfone REAL")
        print(" ✅ CPU/RAM REAIS do sistema")
        print(" ✅ Métricas de processamento REAIS")
        print(" ✅ Logging estruturado em JSONL")
        print("\nFuncionalidades:")
        print(" 📊 Dashboard em tempo real")
        print(" 📝 Logging estruturado (JSONL)")
        print(" 📈 Gráfico de áudio")
        print(" ⏱️  Timeline de eventos")
        print("\nPressione Ctrl+C para parar")
        print("="*80)
        print("\nIniciando em 3 segundos...")
        time.sleep(3)
        
        self.running = True
        
        # Iniciar thread de monitoramento
        monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        monitor_thread.start()
        
        # Configurar áudio
        sample_rate = 16000
        channels = 1
        chunk_size = 512
        
        print("\n🎤 Iniciando captura de áudio...\n")
        
        try:
            # Iniciar stream de áudio
            with sd.InputStream(
                samplerate=sample_rate,
                channels=channels,
                dtype=np.int16,
                blocksize=chunk_size,
                callback=self.audio_callback
            ):
                start_time = time.time()
                frame_num = 0
                last_dashboard_update = start_time
                
                while self.running and (time.time() - start_time) < duration:
                    # Processar frame de áudio
                    try:
                        frame_data = self.audio_queue.get(timeout=0.5)
                        frame_num += 1
                        
                        is_voice, rms = self.process_audio_frame(frame_data, frame_num)
                        
                        # Atualizar dashboard a cada 10 frames
                        now = time.time()
                        if now - last_dashboard_update >= 0.5:
                            cpu = psutil.cpu_percent(interval=0.01)
                            ram = psutil.virtual_memory().used / (1024 * 1024)
                            
                            self.dashboard.display(
                                cpu=cpu,
                                ram=ram,
                                audio_level=rms
                            )
                            
                            last_dashboard_update = now
                        
                    except queue.Empty:
                        # Sem dados de áudio
                        pass
                    
                    # Pequena pausa para não sobrecarregar CPU
                    time.sleep(0.01)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupção pelo usuário")
        
        except Exception as e:
            self.logger.error(f"Erro na execução: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.stop_demo()
    
    def stop_demo(self):
        """Para a demonstração e mostra estatísticas."""
        self.running = False
        time.sleep(0.5)  # Dar tempo para threads encerrarem
        
        print("\n" + "="*80)
        print(" ESTATÍSTICAS FINAIS")
        print("="*80)
        
        # Estatísticas do dashboard
        dash_stats = self.dashboard.get_stats()
        print(f"\n📊 Dashboard:")
        print(f"   Tempo de execução: {dash_stats['elapsed_seconds']:.1f}s")
        print(f"   Frames processados: {dash_stats['frame_count']}")
        print(f"   Frames com voz: {dash_stats['voice_frames']} ({dash_stats['voice_percentage']:.1f}%)")
        print(f"   FPS médio: {dash_stats['fps']:.1f}")
        
        if dash_stats['avg_cpu'] > 0:
            print(f"   CPU média: {dash_stats['avg_cpu']:.1f}%")
        if dash_stats['avg_ram'] > 0:
            print(f"   RAM média: {dash_stats['avg_ram']:.0f} MB")
        
        # Estatísticas do structured logger
        stats = self.struct_logger.get_statistics()
        
        print(f"\n📝 Structured Logger:")
        print(f"   Eventos totais: {stats['total_events']}")
        print(f"   Frames de áudio: {stats['audio']['total_frames']}")
        print(f"   Amplitude média: {stats['audio']['avg_amplitude']:.4f}")
        print(f"   Voz detectada: {stats['audio']['voice_percentage']:.1f}%")
        
        # Encerrar sessão do structured logger
        self.struct_logger.log_session_end()
        
        # Exportar análise
        print(f"\n📂 Arquivos gerados:")
        print(f"   📄 Log estruturado: {self.struct_logger.log_file}")
        print(f"   📄 Log do sistema: logs/demo_advanced.log")
        
        # Exportar análise
        analysis_file = self.struct_logger.export_analysis()
        print(f"   📄 Análise exportada: {analysis_file}")
        
        print("\n" + "="*80)
        print(" ✅ DEMONSTRAÇÃO CONCLUÍDA!")
        print("="*80)
        print("\nTodos os logs são de dados REAIS do seu sistema!")
        print("   - Áudio capturado do seu microfone")
        print("   - CPU/RAM do seu sistema")
        print("   - Métricas de processamento reais")
        print("\nConsulte os arquivos de log para análise detalhada.")
        print("="*80 + "\n")


def main():
    """Função principal."""
    demo = AdvancedLoggingDemo()
    
    try:
        # Executar por 30 segundos (ou até Ctrl+C)
        demo.run_demo(duration=30)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupção pelo usuário")
        demo.stop_demo()


if __name__ == "__main__":
    main()
