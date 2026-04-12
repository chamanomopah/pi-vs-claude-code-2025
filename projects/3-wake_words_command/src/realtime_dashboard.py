# -*- coding: utf-8 -*-
"""
Real-time Dashboard - Dashboard visual em tempo real
Exibe métricas do sistema com atualização contínua.
"""

import time
import threading
from datetime import datetime
from typing import Optional, List
import sys


class RealtimeDashboard:
    """
    Dashboard em tempo real com atualização visual.
    Mostra CPU, RAM, áudio e estatísticas.
    """
    
    def __init__(self, update_interval: float = 0.1):
        """
        Inicializa dashboard.
        
        Args:
            update_interval: Intervalo entre atualizações (segundos)
        """
        self.update_interval = update_interval
        self.start_time = time.time()
        self.last_update = self.start_time
        
        # Contadores
        self.frame_count = 0
        self.voice_frames = 0
        self.wake_words_detected = 0
        self.commands_processed = 0
        
        # Histórico para gráficos
        self.cpu_history: List[float] = []
        self.ram_history: List[float] = []
        self.audio_history: List[float] = []
        self.max_history = 50
        
        # Estado
        self.is_running = False
        self.last_audio_level = 0.0
        
        # Lock para thread-safety
        self.lock = threading.Lock()
    
    def update(self, audio_data=None, is_voice=False, wake_word=False, 
               command=False, cpu=None, ram=None):
        """
        Atualiza dashboard com novos dados.
        
        Args:
            audio_data: Dados de áudio (numpy array ou None)
            is_voice: Se detectou voz
            wake_word: Se detectou wake word
            command: Se processou comando
            cpu: Uso de CPU (%)
            ram: RAM usada (MB)
        """
        with self.lock:
            self.frame_count += 1
            
            if is_voice and audio_data is not None:
                self.voice_frames += 1
                
                # Calcular nível do áudio
                import numpy as np
                if isinstance(audio_data, np.ndarray):
                    self.last_audio_level = float(np.abs(audio_data).mean() / 32768)
            
            if wake_word:
                self.wake_words_detected += 1
            
            if command:
                self.commands_processed += 1
            
            if cpu is not None:
                self.cpu_history.append(cpu)
                if len(self.cpu_history) > self.max_history:
                    self.cpu_history.pop(0)
            
            if ram is not None:
                self.ram_history.append(ram)
                if len(self.ram_history) > self.max_history:
                    self.ram_history.pop(0)
            
            self.audio_history.append(self.last_audio_level)
            if len(self.audio_history) > self.max_history:
                self.audio_history.pop(0)
    
    def display(self, cpu: float = None, ram: float = None, audio_level: float = None):
        """
        Exibe dashboard atualizado.
        
        Args:
            cpu: Uso de CPU (%)
            ram: RAM usada (MB)
            audio_level: Nível do áudio (0-1)
        """
        with self.lock:
            now = time.time()
            elapsed = now - self.start_time
            fps = self.frame_count / elapsed if elapsed > 0 else 0
            
            # Limpar tela (cross-platform)
            self._clear_screen()
            
            # Header
            self._print_header(elapsed)
            
            # Métricas do sistema
            if cpu is not None or ram is not None:
                self._print_system_metrics(cpu, ram)
            
            # Estatísticas de áudio
            self._print_audio_stats(audio_level)
            
            # Gráfico de áudio
            if self.audio_history:
                self._print_audio_graph()
            
            # Timeline de eventos
            self._print_event_timeline()
            
            self.last_update = now
    
    def _clear_screen(self):
        """Limpa a tela (cross-platform)."""
        print("\033[H\033[J", end="")
        sys.stdout.flush()
    
    def _print_header(self, elapsed: float):
        """Imprime header do dashboard."""
        print("=" * 80)
        print(" 🎤 SISTEMA WAKE WORDS - TEMPO REAL")
        print("=" * 80)
        print(f" ⏰ {datetime.now().strftime('%H:%M:%S')} | ⏱️  Tempo: {elapsed:.1f}s")
        print("-" * 80)
    
    def _print_system_metrics(self, cpu: float = None, ram: float = None):
        """Imprime métricas do sistema."""
        if cpu is not None:
            cpu_bar = self._make_bar(cpu / 100, 20)
            print(f" 💻 CPU: {cpu:5.1f}% {cpu_bar}")
        
        if ram is not None:
            ram_bar = self._make_bar(ram / 100 / 10, 20)  # Assumindo max 10GB
            print(f" 🧠 RAM: {ram:5.0f} MB {ram_bar}")
    
    def _print_audio_stats(self, audio_level: float = None):
        """Imprime estatísticas de áudio."""
        fps = self.frame_count / (time.time() - self.start_time)
        voice_pct = (self.voice_frames / max(self.frame_count, 1)) * 100
        
        print("-" * 80)
        print(f" 📊 FPS: {fps:5.1f} | 🎙️  Frames: {self.frame_count} | "
              f"🔊 Voz: {self.voice_frames} ({voice_pct:5.1f}%)")
        print(f" 🎯 Wake Words: {self.wake_words_detected} | "
              f"⚡ Comandos: {self.commands_processed}")
        
        if audio_level is not None:
            audio_bar = self._make_bar(audio_level * 10, 50)  # Amplificar para visualização
            print(f" 🔈 Áudio: [{audio_bar}] {audio_level:.4f}")
    
    def _print_audio_graph(self):
        """Imprime gráfico de nível de áudio."""
        print("-" * 80)
        print(" Gráfico de Áudio (últimos 50 frames):")
        
        graph = ""
        for level in self.audio_history:
            if level > 0.01:
                graph += "█"  # Voz
            elif level > 0.005:
                graph += "▓"  # Médio
            elif level > 0.001:
                graph += "░"  # Baixo
            else:
                graph += "·"  # Silêncio
        
        print(f" {graph}")
        print(" └" + "─" * 50 + "┘ tempo →")
    
    def _print_event_timeline(self):
        """Imprime timeline de eventos recentes."""
        print("-" * 80)
        print(" Eventos Recentes:")
        
        events = []
        if self.wake_words_detected > 0:
            events.append(f"✨ Wake word detectada (total: {self.wake_words_detected})")
        if self.commands_processed > 0:
            events.append(f"⚡ Comando processado (total: {self.commands_processed})")
        
        if events:
            for event in events:
                print(f"  {event}")
        else:
            print("  (nenhum evento ainda)")
        
        print("=" * 80)
    
    def _make_bar(self, value: float, width: int = 20) -> str:
        """
        Cria barra visual.
        
        Args:
            value: Valor (0-1)
            width: Largura da barra
            
        Returns:
            String com barra
        """
        filled = max(0, min(int(value * width), width))
        return '[' + '█' * filled + '░' * (width - filled) + ']'
    
    def get_stats(self) -> dict:
        """Retorna estatísticas atuais."""
        with self.lock:
            elapsed = time.time() - self.start_time
            
            return {
                "elapsed_seconds": elapsed,
                "frame_count": self.frame_count,
                "voice_frames": self.voice_frames,
                "voice_percentage": (self.voice_frames / max(self.frame_count, 1)) * 100,
                "wake_words_detected": self.wake_words_detected,
                "commands_processed": self.commands_processed,
                "fps": self.frame_count / elapsed if elapsed > 0 else 0,
                "avg_cpu": sum(self.cpu_history) / len(self.cpu_history) if self.cpu_history else 0,
                "avg_ram": sum(self.ram_history) / len(self.ram_history) if self.ram_history else 0,
                "avg_audio_level": sum(self.audio_history) / len(self.audio_history) if self.audio_history else 0
            }
    
    def reset(self):
        """Reseta contadores e histórico."""
        with self.lock:
            self.frame_count = 0
            self.voice_frames = 0
            self.wake_words_detected = 0
            self.commands_processed = 0
            self.cpu_history.clear()
            self.ram_history.clear()
            self.audio_history.clear()
            self.start_time = time.time()


class CompactDashboard(RealtimeDashboard):
    """
    Versão compacta do dashboard para terminais pequenos.
    """
    
    def display(self, cpu: float = None, ram: float = None, audio_level: float = None):
        """Exibe dashboard compacto."""
        with self.lock:
            now = time.time()
            elapsed = now - self.start_time
            fps = self.frame_count / elapsed if elapsed > 0 else 0
            
            # Uma linha só
            line = f"\r[{datetime.now().strftime('%H:%M:%S')}] "
            
            if cpu is not None:
                line += f"CPU:{cpu:4.1f}% "
            
            if ram is not None:
                line += f"RAM:{ram:5.0f}MB "
            
            line += f"FPS:{fps:4.1f} "
            line += f"Voz:{self.voice_frames}/{self.frame_count} "
            
            if audio_level is not None:
                line += f"Áudio:{audio_level:.3f} "
            
            line += "      "  # Espaço para limpar
            
            print(line, end="", flush=True)
            self.last_update = now


class SilentDashboard(RealtimeDashboard):
    """
    Dashboard silencioso - só atualiza internamente.
    Útil para testes automatizados.
    """
    
    def display(self, cpu: float = None, ram: float = None, audio_level: float = None):
        """Não exibe nada, só atualiza estado."""
        with self.lock:
            self.last_update = time.time()
