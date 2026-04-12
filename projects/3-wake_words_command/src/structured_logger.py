# -*- coding: utf-8 -*-
"""
Structured Logger - Logging estruturado em JSONL
Registra eventos do sistema em formato estruturado para análise posterior.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import threading
import time


class StructuredLogger:
    """
    Logger estruturado que salva eventos em JSONL (JSON Lines).
    Cada linha é um JSON completo, permitindo análise fácil.
    """
    
    def __init__(self, log_dir: str = "logs", session_id: Optional[str] = None):
        """
        Inicializa logger estruturado.
        
        Args:
            log_dir: Diretório para salvar logs
            session_id: ID da sessão (opcional, auto-gerado se None)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Gerar ID da sessão
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = session_id
        
        # Criar arquivo de log estruturado
        self.log_file = self.log_dir / f"structured_{session_id}.jsonl"
        
        # Eventos em memória para análise
        self.events = []
        self.events_lock = threading.Lock()
        
        # Contadores
        self.counters = {
            "audio_frames": 0,
            "wake_words": 0,
            "transcriptions": 0,
            "commands": 0,
            "system_metrics": 0,
            "errors": 0
        }
        
        # Metadados da sessão
        self.session_start = datetime.now()
        
        # Criar header no arquivo
        self._write_header()
        
        logging.info(f"[STRUCTURED] Logger inicializado: {self.log_file}")
    
    def _write_header(self):
        """Escreve header do arquivo de log."""
        header = {
            "type": "session_start",
            "timestamp": self.session_start.isoformat(),
            "session_id": self.session_id,
            "version": "1.0"
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(header, ensure_ascii=False) + "\n")
    
    def log_event(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registra evento estruturado.
        
        Args:
            event_type: Tipo do evento
            data: Dados do evento
            
        Returns:
            Evento registrado
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "session_id": self.session_id,
            "data": data
        }
        
        with self.events_lock:
            self.events.append(event)
            
            # Atualizar contador
            if event_type in self.counters:
                self.counters[event_type] += 1
        
        # Salvar no arquivo (thread-safe com file locking)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"[STRUCTURED] Erro ao salvar evento: {e}")
        
        return event
    
    def log_audio_frame(self, frame_num: int, amplitude: float, 
                       rms: float, is_voice: bool, samples: int = 512):
        """
        Registra frame de áudio com métricas.
        
        Args:
            frame_num: Número do frame
            amplitude: Amplitude máxima (0-1)
            rms: Root Mean Square
            is_voice: Se detectou voz
            samples: Número de amostras
        """
        return self.log_event("audio_frame", {
            "frame": frame_num,
            "amplitude": float(amplitude),
            "rms": float(rms),
            "is_voice": bool(is_voice),
            "samples": samples,
            "voice_percentage": float(amplitude * 100)
        })
    
    def log_wake_word(self, word: str, confidence: float, 
                     processing_time_ms: float = 0):
        """
        Registra detecção de wake word.
        
        Args:
            word: Palavra detectada
            confidence: Confiança da detecção (0-1)
            processing_time_ms: Tempo de processamento em ms
        """
        self.counters["wake_words"] += 1
        return self.log_event("wake_word", {
            "word": word,
            "confidence": float(confidence),
            "processing_time_ms": float(processing_time_ms),
            "timestamp_iso": datetime.now().isoformat()
        })
    
    def log_transcription(self, text: str, confidence: float, 
                         processing_time: float, alternatives: List[str] = None):
        """
        Registra transcrição de comando.
        
        Args:
            text: Texto transcrito
            confidence: Confiança da transcrição (0-1)
            processing_time: Tempo de processamento em segundos
            alternatives: Lista de alternativas consideradas
        """
        self.counters["transcriptions"] += 1
        return self.log_event("transcription", {
            "text": str(text),
            "confidence": float(confidence),
            "processing_time_ms": float(processing_time * 1000),
            "text_length": len(text),
            "word_count": len(str(text).split()),
            "alternatives": alternatives or []
        })
    
    def log_command_executed(self, command: str, intent: str, 
                            success: bool, result: str = ""):
        """
        Registra execução de comando.
        
        Args:
            command: Comando original
            intent: Intent reconhecido
            success: Se executou com sucesso
            result: Resultado da execução
        """
        self.counters["commands"] += 1
        return self.log_event("command", {
            "command": command,
            "intent": intent,
            "success": bool(success),
            "result": str(result)
        })
    
    def log_system_metrics(self, cpu_percent: float, ram_mb: float, 
                          ram_percent: float, disk_percent: float = None):
        """
        Registra métricas do sistema.
        
        Args:
            cpu_percent: Uso de CPU (%)
            ram_mb: RAM usada (MB)
            ram_percent: RAM usada (%)
            disk_percent: Disco usado (%)
        """
        self.counters["system_metrics"] += 1
        return self.log_event("system_metrics", {
            "cpu_percent": float(cpu_percent),
            "ram_mb": float(ram_mb),
            "ram_percent": float(ram_percent),
            "disk_percent": float(disk_percent) if disk_percent else None
        })
    
    def log_error(self, error_type: str, error_message: str, 
                 stack_trace: str = ""):
        """
        Registra erro do sistema.
        
        Args:
            error_type: Tipo do erro
            error_message: Mensagem de erro
            stack_trace: Stack trace (opcional)
        """
        self.counters["errors"] += 1
        return self.log_event("error", {
            "error_type": error_type,
            "error_message": error_message,
            "stack_trace": stack_trace
        })
    
    def log_session_end(self):
        """Registra fim da sessão."""
        duration = (datetime.now() - self.session_start).total_seconds()
        
        event = {
            "type": "session_end",
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "duration_seconds": float(duration),
            "statistics": self.get_statistics()
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        
        logging.info(f"[STRUCTURED] Sessão encerrada: {duration:.2f}s")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calcula estatísticas dos eventos.
        
        Returns:
            Dict com estatísticas
        """
        with self.events_lock:
            total_events = len(self.events)
            
            # Estatísticas de áudio
            audio_events = [e for e in self.events if e["type"] == "audio_frame"]
            voice_frames = sum(1 for e in audio_events if e["data"].get("is_voice", False))
            avg_amplitude = sum(e["data"].get("amplitude", 0) for e in audio_events) / len(audio_events) if audio_events else 0
            
            # Estatísticas de transcrição
            transcription_events = [e for e in self.events if e["type"] == "transcription"]
            avg_confidence = sum(e["data"].get("confidence", 0) for e in transcription_events) / len(transcription_events) if transcription_events else 0
            
            # Estatísticas de comandos
            command_events = [e for e in self.events if e["type"] == "command"]
            successful_commands = sum(1 for e in command_events if e["data"].get("success", False))
            
            stats = {
                "session_id": self.session_id,
                "session_start": self.session_start.isoformat(),
                "total_events": total_events,
                "counters": self.counters.copy(),
                "audio": {
                    "total_frames": len(audio_events),
                    "voice_frames": voice_frames,
                    "voice_percentage": (voice_frames / len(audio_events) * 100) if audio_events else 0,
                    "avg_amplitude": avg_amplitude
                },
                "transcriptions": {
                    "total": len(transcription_events),
                    "avg_confidence": avg_confidence
                },
                "commands": {
                    "total": len(command_events),
                    "successful": successful_commands,
                    "success_rate": (successful_commands / len(command_events) * 100) if command_events else 0
                }
            }
            
            return stats
    
    def export_analysis(self, output_file: str = None):
        """
        Exporta análise detalhada dos eventos.
        
        Args:
            output_file: Arquivo para salvar análise (opcional)
        """
        stats = self.get_statistics()
        
        analysis = {
            "session_info": {
                "id": self.session_id,
                "start": self.session_start.isoformat(),
                "duration_seconds": (datetime.now() - self.session_start).total_seconds()
            },
            "statistics": stats,
            "events_summary": {
                "by_type": self.counters.copy(),
                "total": len(self.events)
            },
            "timeline": [
                {
                    "timestamp": e["timestamp"],
                    "type": e["type"],
                    "summary": self._get_event_summary(e)
                }
                for e in self.events[-100:]  # Últimos 100 eventos
            ]
        }
        
        if output_file is None:
            output_file = self.log_dir / f"analysis_{self.session_id}.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        logging.info(f"[STRUCTURED] Análise exportada: {output_file}")
        
        return analysis
    
    def _get_event_summary(self, event: Dict) -> str:
        """Gera resumo do evento."""
        event_type = event["type"]
        data = event["data"]
        
        if event_type == "audio_frame":
            status = "VOICE" if data.get("is_voice") else "silence"
            return f"Frame {data.get('frame')}: {status} (amp: {data.get('amplitude', 0):.4f})"
        
        elif event_type == "wake_word":
            return f"Wake word: {data.get('word')} (conf: {data.get('confidence', 0):.2%})"
        
        elif event_type == "transcription":
            return f"Transcribed: \"{data.get('text')}\" (conf: {data.get('confidence', 0):.2%})"
        
        elif event_type == "command":
            status = "✓" if data.get("success") else "✗"
            return f"Command {status}: {data.get('command')} -> {data.get('intent')}"
        
        elif event_type == "system_metrics":
            return f"CPU: {data.get('cpu_percent', 0):.1f}%, RAM: {data.get('ram_mb', 0):.0f}MB"
        
        elif event_type == "error":
            return f"ERROR: {data.get('error_type')}"
        
        return event_type
    
    def get_events_by_type(self, event_type: str) -> List[Dict]:
        """Retorna todos os eventos de um tipo."""
        with self.events_lock:
            return [e for e in self.events if e["type"] == event_type]
    
    def get_recent_events(self, count: int = 10) -> List[Dict]:
        """Retorna os últimos N eventos."""
        with self.events_lock:
            return self.events[-count:]
    
    def clear_events(self):
        """Limpa eventos da memória (não do arquivo)."""
        with self.events_lock:
            self.events.clear()
            logging.info("[STRUCTURED] Eventos da memória limpos")
