"""
Sistema de Logging REAL com monitoramento de CPU, RAM e áudio.
Monitora recursos do sistema usando psutil.
"""

import logging
import psutil
import os
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
