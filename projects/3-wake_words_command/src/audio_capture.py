"""
Captura REAL de áudio do microfone usando sounddevice.
Suporta listagem de dispositivos e captura em tempo real.
"""

import sounddevice as sd
import numpy as np
import threading
import queue
from typing import Optional, Callable, Dict, List
import logging
from datetime import datetime


class AudioDevice:
    """Representa um dispositivo de áudio do sistema."""
    
    def __init__(self, device_id: int, info: dict):
        """
        Inicializa representação do dispositivo.
        
        Args:
            device_id: ID do dispositivo
            info: Informações do dispositivo (sounddevice query)
        """
        self.id = device_id
        self.name = info.get('name', 'Unknown')
        self.max_input_channels = info.get('max_input_channels', 0)
        self.max_output_channels = info.get('max_output_channels', 0)
        self.default_samplerate = info.get('default_samplerate', 0)
        self.host_api = info.get('hostapi', 0)
    
    @property
    def is_input(self) -> bool:
        """Verifica se dispositivo tem entrada de áudio."""
        return self.max_input_channels > 0
    
    @property
    def is_output(self) -> bool:
        """Verifica se dispositivo tem saída de áudio."""
        return self.max_output_channels > 0
    
    def __repr__(self) -> str:
        return (f"AudioDevice(id={self.id}, name='{self.name}', "
                f"inputs={self.max_input_channels}, outputs={self.max_output_channels})")


class AudioDeviceManager:
    """Gerencia dispositivos de áudio do sistema."""
    
    @staticmethod
    def list_devices() -> List[AudioDevice]:
        """
        Lista todos os dispositivos de áudio disponíveis.
        
        Returns:
            Lista de AudioDevice
        """
        devices = []
        try:
            devices_info = sd.query_devices()
            
            for idx, dev_info in enumerate(devices_info):
                devices.append(AudioDevice(idx, dev_info))
            
            return devices
        except Exception as e:
            logging.error(f"Erro ao listar dispositivos: {e}")
            return []
    
    @staticmethod
    def list_input_devices() -> List[AudioDevice]:
        """
        Lista apenas dispositivos com entrada de áudio (microfones).
        
        Returns:
            Lista de AudioDevice com entrada disponível
        """
        all_devices = AudioDeviceManager.list_devices()
        return [dev for dev in all_devices if dev.is_input]
    
    @staticmethod
    def get_default_input_device() -> Optional[AudioDevice]:
        """
        Retorna o dispositivo de entrada padrão.
        
        Returns:
            AudioDevice padrão ou None
        """
        try:
            device_info = sd.query_devices(kind='input')
            if device_info:
                device_id = sd.default.device[0]
                return AudioDevice(device_id, device_info)
        except Exception as e:
            logging.error(f"Erro ao obter dispositivo padrão: {e}")
        return None
    
    @staticmethod
    def print_devices():
        """Imprime todos os dispositivos no formato legível."""
        devices = AudioDeviceManager.list_devices()
        
        print("\n" + "=" * 80)
        print("DISPOSITIVOS DE ÁUDIO DO SISTEMA")
        print("=" * 80)
        
        if not devices:
            print("⚠️  Nenhum dispositivo encontrado!")
            return
        
        print(f"\n{'ID':<4} | {'Nome':<40} | {'Entradas':>8} | {'Saídas':>8} | {'Taxa (Hz)':>10}")
        print("-" * 80)
        
        for dev in devices:
            marker = " 🔊" if dev.is_input and dev.is_output else (" 🎤" if dev.is_input else (" 🔈" if dev.is_output else ""))
            print(f"{dev.id:<4} | {dev.name[:40]:<40} | "
                  f"{dev.max_input_channels:>8} | {dev.max_output_channels:>8} | "
                  f"{int(dev.default_samplerate):>10}{marker}")
        
        print("-" * 80)
        
        default_input = AudioDeviceManager.get_default_input_device()
        if default_input:
            print(f"\n🎤 Dispositivo de ENTRADA padrão: ID {default_input.id} - '{default_input.name}'")
        
        default_output = sd.query_devices(kind='output')
        if default_output:
            print(f"🔈 Dispositivo de SAÍDA padrão: ID {default_output['index']} - '{default_output['name']}'")
        
        print()


class AudioCapture:
    """
    Captura áudio do microfone em tempo real.
    Usa sounddevice para captura via callback assíncrono.
    """
    
    def __init__(self, 
                 sample_rate: int = 16000,
                 channels: int = 1,
                 chunk_size: int = 512,
                 device_id: Optional[int] = None):
        """
        Inicializa captura de áudio.
        
        Args:
            sample_rate: Taxa de amostragem em Hz
            channels: Número de canais (1=mono, 2=stereo)
            chunk_size: Frames por chunk
            device_id: ID do dispositivo (None = padrão)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device_id = device_id
        
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.stream: Optional[sd.InputStream] = None
        
        logging.info(f"🎤 AudioCapture inicializado: {sample_rate}Hz, "
                    f"{channels} canal(eis), chunk={chunk_size}")
    
    def _audio_callback(self, indata, frames, time, status):
        """
        Callback chamado pelo sounddevice quando áudio está disponível.
        
        Args:
            indata: Array numpy com dados de áudio
            frames: Número de frames
            time: Informações de tempo
            status: Status do stream
        """
        if status:
            logging.warning(f"Status do stream: {status}")
        
        # Colocar áudio na fila
        self.audio_queue.put(indata.copy())
    
    def start(self):
        """Inicia a captura de áudio."""
        if self.is_recording:
            logging.warning("Captura já está ativa!")
            return
        
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                blocksize=self.chunk_size,
                dtype=np.int16,
                device=self.device_id,
                callback=self._audio_callback
            )
            
            self.stream.start()
            self.is_recording = True
            
            device_info = f"dispositivo {self.device_id}" if self.device_id else "dispositivo padrão"
            logging.info(f"🔴 Capturando áudio de {device_info} ({self.sample_rate}Hz)")
            
        except Exception as e:
            logging.error(f"Erro ao iniciar captura: {e}")
            raise
    
    def stop(self):
        """Para a captura de áudio."""
        if not self.is_recording:
            return
        
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
            
            self.is_recording = False
            logging.info("⏹️  Captura de áudio parada")
            
        except Exception as e:
            logging.error(f"Erro ao parar captura: {e}")
    
    def read_chunk(self, timeout: float = 1.0) -> Optional[np.ndarray]:
        """
        Lê um chunk de áudio da fila.
        
        Args:
            timeout: Tempo máximo de espera em segundos
            
        Returns:
            Array numpy com áudio ou None se timeout
        """
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def read_all(self, max_chunks: int = 100) -> np.ndarray:
        """
        Lê todos os chunks disponíveis e concatena.
        
        Args:
            max_chunks: Número máximo de chunks para ler
            
        Returns:
            Array numpy com todos os áudios concatenados
        """
        chunks = []
        count = 0
        
        while not self.audio_queue.empty() and count < max_chunks:
            try:
                chunk = self.audio_queue.get_nowait()
                chunks.append(chunk)
                count += 1
            except queue.Empty:
                break
        
        if chunks:
            return np.concatenate(chunks, axis=0)
        
        return np.array([], dtype=np.int16).reshape(0, self.channels)
    
    def get_audio_level(self, chunk: np.ndarray) -> float:
        """
        Calcula o nível do áudio (RMS normalizado).
        
        Args:
            chunk: Array numpy com áudio
            
        Returns:
            Nível entre 0.0 e 1.0
        """
        if len(chunk) == 0:
            return 0.0
        
        # Calcular RMS
        rms = np.sqrt(np.mean(np.square(chunk.astype(float))))
        
        # Normalizar (assumindo 16-bit signed)
        max_val = np.iinfo(np.int16).max
        normalized = rms / max_val
        
        # Aplicar ganho para melhor visualização
        return min(normalized * 10, 1.0)
    
    def record_duration(self, duration: float) -> np.ndarray:
        """
        Grava áudio por duração específica.
        
        Args:
            duration: Duração em segundos
            
        Returns:
            Array numpy com áudio gravado
        """
        chunks = []
        num_chunks = int(duration * self.sample_rate / self.chunk_size)
        
        logging.info(f"🎙️  Gravando por {duration} segundos...")
        
        for i in range(num_chunks):
            chunk = self.read_chunk(timeout=2.0)
            if chunk is not None:
                chunks.append(chunk)
            
            if (i + 1) % 10 == 0:
                progress = (i + 1) / num_chunks * 100
                logging.debug(f"Gravando: {progress:.0f}%")
        
        if chunks:
            audio_data = np.concatenate(chunks, axis=0)
            logging.info(f"✅ Gravação completa: {len(audio_data)} frames")
            return audio_data
        
        logging.warning("⚠️  Nenhum áudio gravado")
        return np.array([], dtype=np.int16).reshape(0, self.channels)
    
    def save_audio(self, audio_data: np.ndarray, filepath: str):
        """
        Salva áudio em arquivo WAV.
        
        Args:
            audio_data: Array numpy com áudio
            filepath: Caminho do arquivo
        """
        try:
            import wave
            import struct
            
            # Normalizar para int16 se necessário
            if audio_data.dtype != np.int16:
                audio_data = (audio_data * np.iinfo(np.int16).max).astype(np.int16)
            
            with wave.open(filepath, 'wb') as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(2)  # 16-bit = 2 bytes
                wav_file.setframerate(self.sample_rate)
                
                # Converter para bytes e escrever
                if len(audio_data) > 0:
                    audio_bytes = audio_data.tobytes()
                    wav_file.writeframes(audio_bytes)
            
            logging.info(f"💾 Áudio salvo em: {filepath}")
            
        except Exception as e:
            logging.error(f"Erro ao salvar áudio: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


class AudioCaptureWithLogging(AudioCapture):
    """
    Captura de áudio com logging detalhado de frames.
    Registra estatísticas de cada frame capturado.
    """
    
    def __init__(self, *args, frame_logger=None, log_every_n_frames=10, **kwargs):
        """
        Inicializa captura com logging.
        
        Args:
            frame_logger: Instância de AudioFrameLogger
            log_every_n_frames: Logar a cada N frames
        """
        super().__init__(*args, **kwargs)
        self.frame_logger = frame_logger
        self.log_every_n_frames = log_every_n_frames
        self.frame_counter = 0
        
        # Estatísticas
        self.frames_captured = 0
        self.frames_with_voice = 0
        self.peak_amplitude = 0.0
    
    def _audio_callback(self, indata, frames, time, status):
        """
        Callback com logging de frames.
        
        Args:
            indata: Array numpy com dados de áudio
            frames: Número de frames
            time: Informações de tempo
            status: Status do stream
        """
        if status:
            logging.warning(f"Status do stream: {status}")
        
        # Colocar áudio na fila
        self.audio_queue.put(indata.copy())
        
        # Incrementar contador
        self.frames_captured += 1
        self.frame_counter += 1
        
        # Logar frame se tiver logger e chegar a hora
        if self.frame_logger and (self.frame_counter % self.log_every_n_frames == 0):
            self.frame_logger.log_frame(indata[:, 0] if indata.ndim > 1 else indata,
                                        self.sample_rate)
        
        # Calcular amplitude para estatísticas
        amplitude = np.abs(indata).max() / 32768.0
        self.peak_amplitude = max(self.peak_amplitude, amplitude)
        
        if amplitude > 0.01:
            self.frames_with_voice += 1
    
    def get_capture_stats(self) -> dict:
        """Retorna estatísticas da captura."""
        voice_percentage = (self.frames_with_voice / self.frames_captured * 100) if self.frames_captured > 0 else 0
        
        return {
            'frames_captured': self.frames_captured,
            'frames_with_voice': self.frames_with_voice,
            'voice_percentage': voice_percentage,
            'peak_amplitude': self.peak_amplitude,
            'capture_duration': self.frames_captured * self.chunk_size / self.sample_rate
        }
    
    def log_capture_summary(self):
        """Registra resumo da captura."""
        stats = self.get_capture_stats()
        
        logging.info(
            f"[CAPTURE_SUMMARY] "
            f"Frames:{stats['frames_captured']} | "
            f"Voice:{stats['voice_percentage']:.1f}% | "
            f"Peak:{stats['peak_amplitude']:.4f} | "
            f"Duration:{stats['capture_duration']:.2f}s"
        )
    
    def reset_stats(self):
        """Reseta estatísticas."""
        self.frames_captured = 0
        self.frames_with_voice = 0
        self.peak_amplitude = 0.0
