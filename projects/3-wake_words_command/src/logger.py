"""
Sistema de Logging REAL com monitoramento de CPU, RAM e áudio.
Monitora recursos do sistema usando psutil.
"""

import logging
import psutil
import os
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional
import json


class SystemMonitor:
    """Monitora recursos do sistema em tempo real."""
    
    def __init__(self):
        """Inicializa o monitor do sistema."""
        self.process = psutil.Process(os.getpid())
        self.boot_time = psutil.boot_time()
    
    def get_cpu_percent(self, interval: float = 0.1) -> float:
        """
        Retorna o percentual de uso da CPU.
        
        Args:
            interval: Intervalo de medição em segundos
            
        Returns:
            Uso da CPU em percentual (0-100)
        """
        try:
            return psutil.cpu_percent(interval=interval)
        except Exception as e:
            logging.warning(f"Erro ao medir CPU: {e}")
            return 0.0
    
    def get_memory_info(self) -> dict:
        """
        Retorna informações detalhadas de memória.
        
        Returns:
            Dict com informações de RAM (total, available, percent, used)
        """
        try:
            mem = psutil.virtual_memory()
            return {
                'total_mb': round(mem.total / (1024 * 1024), 2),
                'available_mb': round(mem.available / (1024 * 1024), 2),
                'used_mb': round(mem.used / (1024 * 1024), 2),
                'percent': mem.percent,
                'total_gb': round(mem.total / (1024 * 1024 * 1024), 2),
                'used_gb': round(mem.used / (1024 * 1024 * 1024), 2),
            }
        except Exception as e:
            logging.warning(f"Erro ao medir memória: {e}")
            return {
                'total_mb': 0, 'available_mb': 0, 'used_mb': 0,
                'percent': 0, 'total_gb': 0, 'used_gb': 0
            }
    
    def get_process_memory(self) -> dict:
        """
        Retorna o uso de memória do processo atual.
        
        Returns:
            Dict com RSS e VMS em MB
        """
        try:
            mem_info = self.process.memory_info()
            return {
                'rss_mb': round(mem_info.rss / (1024 * 1024), 2),
                'vms_mb': round(mem_info.vms / (1024 * 1024), 2)
            }
        except Exception as e:
            logging.warning(f"Erro ao medir memória do processo: {e}")
            return {'rss_mb': 0, 'vms_mb': 0}
    
    def get_cpu_count(self) -> dict:
        """
        Retorna informações sobre CPUs do sistema.
        
        Returns:
            Dict com count (físico e lógico)
        """
        try:
            return {
                'physical': psutil.cpu_count(logical=False),
                'logical': psutil.cpu_count(logical=True)
            }
        except Exception as e:
            logging.warning(f"Erro ao contar CPUs: {e}")
            return {'physical': 0, 'logical': 0}
    
    def get_system_info(self) -> dict:
        """
        Retorna informações completas do sistema.
        
        Returns:
            Dict com informações de CPU, memória, disco, etc.
        """
        try:
            cpu_freq = psutil.cpu_freq()
            return {
                'cpu': {
                    'percent': self.get_cpu_percent(interval=0.01),
                    'count': self.get_cpu_count(),
                    'freq_mhz': round(cpu_freq.current, 2) if cpu_freq else 0
                },
                'memory': self.get_memory_info(),
                'process_memory': self.get_process_memory(),
                'disk': self.get_disk_info(),
                'boot_time': datetime.fromtimestamp(self.boot_time).isoformat()
            }
        except Exception as e:
            logging.warning(f"Erro ao obter info do sistema: {e}")
            return {}
    
    def get_disk_info(self) -> dict:
        """
        Retorna informações de uso do disco.
        
        Returns:
            Dict com uso do disco em GB/percentual
        """
        try:
            disk = psutil.disk_usage('/')
            return {
                'total_gb': round(disk.total / (1024 * 1024 * 1024), 2),
                'used_gb': round(disk.used / (1024 * 1024 * 1024), 2),
                'free_gb': round(disk.free / (1024 * 1024 * 1024), 2),
                'percent': disk.percent
            }
        except Exception as e:
            logging.warning(f"Erro ao medir disco: {e}")
            return {'total_gb': 0, 'used_gb': 0, 'free_gb': 0, 'percent': 0}


class AudioLogger:
    """Logger específico para dados de áudio."""
    
    def __init__(self, logger: logging.Logger):
        """
        Inicializa o logger de áudio.
        
        Args:
            logger: Logger Python padrão
        """
        self.logger = logger
        self._last_level = 0.0
    
    def log_audio_level(self, level: float, threshold: float = 0.3):
        """
        Registra o nível do áudio com indicador visual.
        
        Args:
            level: Nível do áudio (0.0 a 1.0)
            threshold: Limiar para considerar como "fala detectada"
        """
        if level > threshold:
            self.logger.info(f"🎤 Áudio: {self._audio_bar(level)} ({level:.3f}) FALA DETECTADA")
        else:
            self.logger.debug(f"🎤 Áudio: {self._audio_bar(level)} ({level:.3f})")
        
        self._last_level = level
    
    def _audio_bar(self, level: float, width: int = 30) -> str:
        """
        Cria uma barra visual do nível do áudio.
        
        Args:
            level: Nível do áudio (0.0 a 1.0)
            width: Largura da barra em caracteres
            
        Returns:
            String com barra visual
        """
        filled = int(level * width)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}]"


class WakeWordsLogger:
    """Logger principal do sistema Wake Words."""
    
    def __init__(self, config: dict):
        """
        Inicializa o logger configurado.
        
        Args:
            config: Dicionário de configuração
        """
        self.config = config
        self.logger = self._setup_logger()
        self.monitor = SystemMonitor()
        self.audio_logger = AudioLogger(self.logger)
        self.start_time = datetime.now()
        
        # Log inicial
        self._log_system_info()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o logger Python com handlers."""
        logger = logging.getLogger('WakeWords')
        logger.setLevel(getattr(logging, self.config.get('level', 'INFO')))
        
        # Limpar handlers existentes
        logger.handlers.clear()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (se habilitado)
        if self.config.get('log_to_file', True):
            log_dir = Path(self.config.get('log_dir', 'logs'))
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / self.config.get('log_file', 'wake_words.log')
            
            # Rotating file handler
            from logging.handlers import RotatingFileHandler
            max_bytes = self.config.get('max_size_mb', 10) * 1024 * 1024
            backup_count = self.config.get('backup_count', 5)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def _log_system_info(self):
        """Registra informações do sistema na inicialização."""
        self.logger.info("=" * 60)
        self.logger.info("SISTEMA WAKE WORDS - INICIALIZANDO")
        self.logger.info("=" * 60)
        
        sys_info = self.monitor.get_system_info()
        
        self.logger.info(f"🖥️  CPU: {sys_info['cpu']['count']['logical']} núcleos "
                        f"({sys_info['cpu']['count']['physical']} físicos)")
        self.logger.info(f"🧠 RAM: {sys_info['memory']['total_gb']:.2f} GB total "
                        f"({sys_info['memory']['used_gb']:.2f} GB usados, "
                        f"{sys_info['memory']['percent']:.1f}%)")
        self.logger.info(f"💾 Disco: {sys_info['disk']['total_gb']:.2f} GB total "
                        f"({sys_info['disk']['used_gb']:.2f} GB usados)")
        
        self.logger.info("-" * 60)
    
    def log_wake_word_detected(self, keyword: str):
        """Registra detecção de wake word."""
        self.logger.info(f"✨ WAKE WORD DETECTADA: '{keyword}'")
    
    def log_command_detected(self, command: str):
        """Registra comando reconhecido."""
        self.logger.info(f"📝 COMANDO: '{command}'")
    
    def log_listening(self):
        """Registra estado de escuta."""
        self.logger.debug("👂 Escutando...")
    
    def log_system_stats(self):
        """Registra estatísticas do sistema."""
        cpu = self.monitor.get_cpu_percent(interval=0.01)
        mem = self.monitor.get_memory_info()
        proc_mem = self.monitor.get_process_memory()
        
        self.logger.debug(
            f"📊 CPU: {cpu:.1f}% | "
            f"RAM: {mem['used_mb']:.0f}/{mem['total_mb']:.0f} MB "
            f"({mem['percent']:.1f}%) | "
            f"Processo: {proc_mem['rss_mb']:.1f} MB"
        )
    
    def log_startup_time(self):
        """Registra tempo de inicialização."""
        duration = (datetime.now() - self.start_time).total_seconds()
        self.logger.info(f"⚡ Inicializado em {duration:.2f} segundos")
    
    def log_shutdown(self):
        """Registra desligamento do sistema."""
        duration = (datetime.now() - self.start_time).total_seconds()
        self.logger.info("=" * 60)
        self.logger.info(f"SISTEMA DESLIGADO (executado por {duration:.1f}s)")
        self.logger.info("=" * 60)
    
    def get_logger(self) -> logging.Logger:
        """Retorna o logger Python."""
        return self.logger
    
    def get_audio_logger(self) -> AudioLogger:
        """Retorna o logger de áudio."""
        return self.audio_logger
    
    def get_monitor(self) -> SystemMonitor:
        """Retorna o monitor do sistema."""
        return self.monitor


class RealTimeMonitor:
    """
    Monitoramento em tempo real do sistema.
    Executa em thread separada para não bloquear operações.
    """
    
    def __init__(self, logger: WakeWordsLogger, interval: float = 1.0):
        """
        Inicializa monitor em tempo real.
        
        Args:
            logger: Instância de WakeWordsLogger
            interval: Intervalo de monitoramento em segundos
        """
        self.logger = logger
        self.interval = interval
        self.running = False
        self.thread = None
        self.monitor = logger.monitor
        
        # Métricas acumuladas
        self.metrics_history = []
        self.max_history = 100
        
        # Timestamp de início
        self.start_time = datetime.now()
    
    def start(self):
        """Inicia monitoramento em background."""
        if self.running:
            self.logger.logger.warning("Monitoramento já está ativo!")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        self.logger.logger.info(f"[MONITOR] Monitoramento em tempo real iniciado (intervalo: {self.interval}s)")
    
    def _monitor_loop(self):
        """Loop de monitoramento executado em thread separada."""
        process = psutil.Process()
        iteration = 0
        
        while self.running:
            try:
                iteration += 1
                timestamp = datetime.now()
                
                # CPU do processo
                cpu_process = process.cpu_percent(interval=0.1)
                
                # CPU do sistema (todos os núcleos)
                cpu_system = psutil.cpu_percent(interval=0.1)
                
                # CPU por núcleo
                cpu_per_core = psutil.cpu_percent(interval=0, percpu=True)
                
                # RAM do processo
                ram_process = process.memory_info()
                ram_process_mb = ram_process.rss / (1024 * 1024)
                ram_process_vms = ram_process.vms / (1024 * 1024)
                
                # RAM do sistema
                ram_system = psutil.virtual_memory()
                ram_system_used = ram_system.used / (1024 * 1024)
                ram_system_available = ram_system.available / (1024 * 1024)
                ram_system_percent = ram_system.percent
                
                # Threads do processo
                num_threads = process.num_threads()
                
                # Arquivos abertos
                try:
                    num_files = len(process.open_files())
                except:
                    num_files = 0
                
                # Criar métrica
                metric = {
                    'timestamp': timestamp.isoformat(),
                    'iteration': iteration,
                    'cpu_process': cpu_process,
                    'cpu_system': cpu_system,
                    'cpu_per_core': cpu_per_core,
                    'ram_process_mb': ram_process_mb,
                    'ram_process_vms': ram_process_vms,
                    'ram_system_used_mb': ram_system_used,
                    'ram_system_available_mb': ram_system_available,
                    'ram_system_percent': ram_system_percent,
                    'num_threads': num_threads,
                    'num_files': num_files
                }
                
                # Adicionar ao histórico
                self.metrics_history.append(metric)
                if len(self.metrics_history) > self.max_history:
                    self.metrics_history.pop(0)
                
                # Log estruturado em formato fácil de parse
                self.logger.logger.info(
                    f"[METRIC] "
                    f"Iter:{iteration:4d} | "
                    f"CPU_PROC:{cpu_process:5.1f}% | "
                    f"CPU_SYS:{cpu_system:5.1f}% | "
                    f"RAM_PROC:{ram_process_mb:6.1f}MB | "
                    f"RAM_SYS:{ram_system_percent:5.1f}% | "
                    f"RAM_LIVRE:{ram_system_available:6.0f}MB | "
                    f"THRDS:{num_threads:2d}"
                )
                
            except Exception as e:
                self.logger.logger.error(f"[MONITOR] Erro no monitoramento: {e}")
                import traceback
                self.logger.logger.debug(traceback.format_exc())
            
            time.sleep(self.interval)
    
    def stop(self):
        """Para monitoramento."""
        if not self.running:
            return
        
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=3)
        
        duration = (datetime.now() - self.start_time).total_seconds()
        self.logger.logger.info(f"[MONITOR] Monitoramento parado (duração: {duration:.1f}s)")
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do monitoramento."""
        if not self.metrics_history:
            return {}
        
        # Calcular estatísticas
        cpu_process_vals = [m['cpu_process'] for m in self.metrics_history]
        cpu_system_vals = [m['cpu_system'] for m in self.metrics_history]
        ram_process_vals = [m['ram_process_mb'] for m in self.metrics_history]
        
        return {
            'duration_seconds': (datetime.now() - self.start_time).total_seconds(),
            'iterations': len(self.metrics_history),
            'cpu_process': {
                'avg': sum(cpu_process_vals) / len(cpu_process_vals),
                'min': min(cpu_process_vals),
                'max': max(cpu_process_vals)
            },
            'cpu_system': {
                'avg': sum(cpu_system_vals) / len(cpu_system_vals),
                'min': min(cpu_system_vals),
                'max': max(cpu_system_vals)
            },
            'ram_process_mb': {
                'avg': sum(ram_process_vals) / len(ram_process_vals),
                'min': min(ram_process_vals),
                'max': max(ram_process_vals)
            }
        }
    
    def get_metrics_history(self) -> list:
        """Retorna histórico de métricas."""
        return self.metrics_history.copy()
    
    def export_metrics_json(self, filepath: str):
        """Exporta métricas para arquivo JSON."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'start_time': self.start_time.isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'stats': self.get_stats(),
                    'metrics': self.metrics_history
                }, f, indent=2, ensure_ascii=False)
            
            self.logger.logger.info(f"[MONITOR] Métricas exportadas para: {filepath}")
        except Exception as e:
            self.logger.logger.error(f"[MONITOR] Erro ao exportar métricas: {e}")


class AudioFrameLogger:
    """
    Logger detalhado para frames de áudio.
    Registra estatísticas de cada frame capturado.
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Inicializa logger de frames.
        
        Args:
            logger: Logger Python padrão
        """
        self.logger = logger
        self.frame_count = 0
        self.voice_frame_count = 0
        self.silence_frame_count = 0
        self.start_time = datetime.now()
        
        # Limiar para detectar voz
        self.voice_threshold = 0.01
    
    def log_frame(self, frame_data, sample_rate: int = 16000):
        """
        Registra estatísticas de um frame de áudio.
        
        Args:
            frame_data: Array numpy com dados do frame
            sample_rate: Taxa de amostragem
        """
        import numpy as np
        
        self.frame_count += 1
        
        if frame_data is None or len(frame_data) == 0:
            self.logger.debug(f"[AUDIO_FRAME] Frame {self.frame_count}: VAZIO")
            return
        
        # Converter para float se necessário
        if frame_data.dtype == np.int16:
            frame_float = frame_data.astype(float) / 32768.0
        else:
            frame_float = frame_data
        
        # Calcular estatísticas
        amplitude = np.abs(frame_float).max()
        rms = np.sqrt(np.mean(frame_float ** 2))
        
        # Detectar se é voz
        is_voice = amplitude > self.voice_threshold
        
        if is_voice:
            self.voice_frame_count += 1
            status = "VOICE"
        else:
            self.silence_frame_count += 1
            status = "SILENCE"
        
        # Log detalhado
        self.logger.info(
            f"[AUDIO_FRAME] "
            f"#{self.frame_count:5d} | "
            f"Amp:{amplitude:.6f} | "
            f"RMS:{rms:.6f} | "
            f"Samples:{len(frame_data):5d} | "
            f"Status:{status:7s} | "
            f"Bar:{self._audio_bar(amplitude)}"
        )
    
    def _audio_bar(self, level: float, width: int = 20) -> str:
        """Cria barra visual do nível."""
        filled = min(int(level * 500), width)  # Amplificado para melhor visualização
        return '[' + '█' * filled + '░' * (width - filled) + ']'
    
    def get_stats(self) -> dict:
        """Retorna estatísticas dos frames."""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'duration_seconds': duration,
            'total_frames': self.frame_count,
            'voice_frames': self.voice_frame_count,
            'silence_frames': self.silence_frame_count,
            'voice_percentage': (self.voice_frame_count / self.frame_count * 100) 
                               if self.frame_count > 0 else 0,
            'frames_per_second': self.frame_count / duration if duration > 0 else 0
        }


class TranscriptionLogger:
    """
    Logger para transcrições de fala.
    Registra texto, confiança e tempos.
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Inicializa logger de transcrições.
        
        Args:
            logger: Logger Python padrão
        """
        self.logger = logger
        self.transcriptions = []
        self.start_time = datetime.now()
    
    def log_transcription(self, text: str, confidence: float = 1.0, 
                         duration: float = 0.0, alternatives: list = None):
        """
        Registra uma transcrição.
        
        Args:
            text: Texto transcrito
            confidence: Confiança da transcrição (0-1)
            duration: Duração do áudio transcrevido
            alternatives: Lista de alternativas consideradas
        """
        timestamp = datetime.now()
        
        transcription = {
            'timestamp': timestamp.isoformat(),
            'text': text,
            'confidence': confidence,
            'duration': duration,
            'alternatives': alternatives or []
        }
        
        self.transcriptions.append(transcription)
        
        # Log formatado
        self.logger.info(
            f"[TRANSCRIPTION] "
            f"Text:\"{text}\" | "
            f"Conf:{confidence:.2%} | "
            f"Dur:{duration:.2f}s | "
            f"Time:{timestamp.strftime('%H:%M:%S.%f')[:-3]}"
        )
        
        if alternatives:
            for i, alt in enumerate(alternatives, 1):
                self.logger.debug(f"  Alt[{i}]: \"{alt.get('text', '')}\" ({alt.get('confidence', 0):.2%})")
    
    def log_partial(self, text: str):
        """Registra resultado parcial."""
        self.logger.debug(f"[TRANSCRIPTION_PARTIAL] \"{text}\"")
    
    def log_error(self, error: str, details: str = ""):
        """Registra erro na transcrição."""
        self.logger.error(f"[TRANSCRIPTION_ERROR] {error} | {details}")
    
    def get_stats(self) -> dict:
        """Retorna estatísticas das transcrições."""
        if not self.transcriptions:
            return {'count': 0}
        
        confidences = [t['confidence'] for t in self.transcriptions]
        durations = [t['duration'] for t in self.transcriptions]
        
        return {
            'count': len(self.transcriptions),
            'avg_confidence': sum(confidences) / len(confidences),
            'total_duration': sum(durations),
            'avg_duration': sum(durations) / len(durations),
            'transcriptions': self.transcriptions
        }
