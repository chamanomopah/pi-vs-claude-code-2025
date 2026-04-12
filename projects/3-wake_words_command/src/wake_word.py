"""
Detecção REAL de wake words usando Picovoice Porcupine.
Suporta múltiplas palavras-chave e sensibilidade configurável.
"""

import pvporcupine
import numpy as np
import struct
from typing import Optional, List, Callable
import logging
from pathlib import Path


class WakeWordDetector:
    """
    Detector de wake words usando Porcupine.
    Detecta palavras de ativação em tempo real.
    """
    
    # Palavras-chave disponíveis (built-in)
    BUILTIN_KEYWORDS = [
        'porcupine',
        'picovoice',
        'bumblebee',
        'alexa',
        'americano',
        'blueberry',
        'computer',
        'grapefruit',
        'grasshopper',
        'hey google',
        'hey siri',
        'jarvis',
        'ok google',
        'picovoice',
        'porcupine',
        'terminator'
    ]
    
    def __init__(self,
                 access_key: str,
                 keyword: str = 'porcupine',
                 sensitivity: float = 0.5,
                 model_path: Optional[str] = None,
                 keyword_paths: Optional[List[str]] = None):
        """
        Inicializa o detector de wake words.
        
        Args:
            access_key: Chave de acesso do Picovoice (obter em console.picovoice.ai)
            keyword: Palavra-chave built-in ou caminho para arquivo customizado
            sensitivity: Sensibilidade (0.0 a 1.0)
            model_path: Caminho para modelo customizado (opcional)
            keyword_paths: Lista de caminhos para palavras-chave customizadas
        """
        self.access_key = access_key
        self.keyword = keyword
        self.sensitivity = sensitivity
        self.model_path = model_path
        self.keyword_paths = keyword_paths or []
        
        self.porcupine: Optional[pvporcupine.Porcupine] = None
        self.is_initialized = False
        
        # Métricas
        self._detection_count = 0
        self._frame_count = 0
        
        self._initialize()
    
    def _initialize(self):
        """Inicializa o Porcupine."""
        try:
            # Preparar parâmetros
            keyword_paths = self.keyword_paths
            
            # Se keyword é built-in, usar como string
            if self.keyword.lower() in self.BUILTIN_KEYWORDS and not keyword_paths:
                keywords = [self.keyword]
                keyword_paths = None
            else:
                keywords = None
                if not keyword_paths:
                    keyword_paths = [self.keyword]
            
            # Criar instância do Porcupine
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=keywords,
                keyword_paths=keyword_paths,
                sensitivities=[self.sensitivity] * (len(keywords) if keywords else len(keyword_paths)),
                model_path=self.model_path
            )
            
            self.is_initialized = True
            
            logging.info(f"✅ Wake Word Detector inicializado")
            logging.info(f"   Palavra-chave: '{self.keyword}'")
            logging.info(f"   Sensibilidade: {self.sensitivity}")
            logging.info(f"   Taxa de amostragem: {self.porcupine.sample_rate} Hz")
            logging.info(f"   Frames por frame: {self.porcupine.frame_length}")
            
        except Exception as e:
            logging.error(f"❌ Erro ao inicializar Porcupine: {e}")
            raise
    
    @property
    def sample_rate(self) -> int:
        """Retorna a taxa de amostragem exigida."""
        return self.porcupine.sample_rate if self.porcupine else 16000
    
    @property
    def frame_length(self) -> int:
        """Retorna o número de frames exigido."""
        return self.porcupine.frame_length if self.porcupine else 512
    
    def process_frame(self, audio_frame: np.ndarray) -> bool:
        """
        Processa um frame de áudio e detecta wake word.
        
        Args:
            audio_frame: Array numpy de int16 com o áudio
            
        Returns:
            True se wake word detectada, False caso contrário
        """
        if not self.is_initialized:
            logging.error("Detector não inicializado!")
            return False
        
        try:
            # Garantir formato correto
            if audio_frame.dtype != np.int16:
                audio_frame = (audio_frame * np.iinfo(np.int16).max).astype(np.int16)
            
            # Processar frame
            result = self.porcupine.process(audio_frame)
            
            self._frame_count += 1
            
            if result >= 0:
                self._detection_count += 1
                logging.info(f"✨ WAKE WORD DETECTADA! (keyword_index={result})")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Erro ao processar frame: {e}")
            return False
    
    def process_pcm(self, pcm_data: bytes) -> bool:
        """
        Processa dados PCM brutos (bytes).
        
        Args:
            pcm_data: Bytes PCM (16-bit signed)
            
        Returns:
            True se wake word detectada
        """
        try:
            # Converter bytes para int16 array
            audio_frame = np.frombuffer(pcm_data, dtype=np.int16)
            return self.process_frame(audio_frame)
        except Exception as e:
            logging.error(f"Erro ao processar PCM: {e}")
            return False
    
    def detect_from_file(self, audio_file: str) -> List[dict]:
        """
        Detecta wake words em um arquivo de áudio.
        
        Args:
            audio_file: Caminho do arquivo WAV
            
        Returns:
            Lista de detecções com timestamps
        """
        import wave
        
        detections = []
        
        try:
            with wave.open(audio_file, 'rb') as wf:
                sample_rate = wf.getframerate()
                frames = wf.getnframes()
                
                # Verificar compatibilidade
                if sample_rate != self.sample_rate:
                    logging.warning(f"Taxa de amostragem diferente: {sample_rate} vs {self.sample_rate}")
                
                # Ler e processar frames
                audio_data = wf.readframes(frames)
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # Processar frame por frame
                frame_len = self.frame_length
                for i in range(0, len(audio_array) - frame_len, frame_len):
                    frame = audio_array[i:i + frame_len]
                    
                    if self.process_frame(frame):
                        timestamp = i / sample_rate
                        detections.append({
                            'timestamp': timestamp,
                            'keyword': self.keyword
                        })
            
            logging.info(f"📊 Detecções no arquivo: {len(detections)}")
            return detections
            
        except Exception as e:
            logging.error(f"Erro ao processar arquivo: {e}")
            return detections
    
    def reset_metrics(self):
        """Reseta contadores de métricas."""
        self._detection_count = 0
        self._frame_count = 0
    
    def get_metrics(self) -> dict:
        """Retorna métricas de detecção."""
        return {
            'detections': self._detection_count,
            'frames_processed': self._frame_count,
            'detection_rate': (self._detection_count / self._frame_count * 100) 
                              if self._frame_count > 0 else 0
        }
    
    def list_builtin_keywords(self) -> List[str]:
        """Retorna lista de palavras-chave built-in."""
        return self.BUILTIN_KEYWORDS.copy()
    
    @staticmethod
    def print_builtin_keywords():
        """Imprime todas as palavras-chave disponíveis."""
        print("\n" + "=" * 60)
        print("PALAVRAS-CHAVE DISPONÍVEIS (Built-in)")
        print("=" * 60)
        
        for i, kw in enumerate(WakeWordDetector.BUILTIN_KEYWORDS, 1):
            print(f"{i:2d}. {kw}")
        
        print("=" * 60)
        print("Obtenha sua Access Key em: https://console.picovoice.ai/")
        print()
    
    def release(self):
        """Libera recursos do Porcupine."""
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None
            self.is_initialized = False
            logging.info("🔓 Recursos do Porcupine liberados")
    
    def __del__(self):
        """Destrutor."""
        self.release()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()


class WakeWordTester:
    """Utilitário para testar detecção de wake words."""
    
    def __init__(self, detector: WakeWordDetector):
        """
        Inicializa testador.
        
        Args:
            detector: Instância do WakeWordDetector
        """
        self.detector = detector
    
    def test_microphone(self, duration: float = 10.0):
        """
        Testa detecção em tempo real do microfone.
        
        Args:
            duration: Duração do teste em segundos
        """
        from .audio_capture import AudioCapture, AudioDeviceManager
        
        print("\n" + "=" * 60)
        print(f"TESTE DE WAKE WORD - Duração: {duration}s")
        print("=" * 60)
        print(f"Fale '{self.detector.keyword}' para testar!")
        print("=" * 60 + "\n")
        
        # Criar captura com configurações compatíveis
        capture = AudioCapture(
            sample_rate=self.detector.sample_rate,
            channels=1,
            chunk_size=self.detector.frame_length
        )
        
        try:
            capture.start()
            
            import time
            start_time = time.time()
            detection_count = 0
            
            while time.time() - start_time < duration:
                # Ler frame do microfone
                chunk = capture.read_chunk(timeout=1.0)
                
                if chunk is not None and len(chunk) >= self.detector.frame_length:
                    # Flatten se necessário
                    if chunk.ndim > 1:
                        chunk = chunk[:, 0]
                    
                    # Processar frame
                    if self.detector.process_frame(chunk):
                        detection_count += 1
                        print(f"✨ DETECÇÃO #{detection_count}!")
            
            print(f"\n📊 Total de detecções: {detection_count}")
            print(f"📊 Taxa de detecção: {detection_count / duration * 100:.1f}/min")
            
        finally:
            capture.stop()
    
    def test_audio_file(self, audio_file: str):
        """
        Testa detecção em arquivo de áudio.
        
        Args:
            audio_file: Caminho do arquivo WAV
        """
        print("\n" + "=" * 60)
        print(f"TESTANDO ARQUIVO: {audio_file}")
        print("=" * 60)
        
        if not Path(audio_file).exists():
            print(f"❌ Arquivo não encontrado: {audio_file}")
            return
        
        detections = self.detector.detect_from_file(audio_file)
        
        print(f"\n📊 Total de detecções: {len(detections)}")
        
        for i, det in enumerate(detections, 1):
            print(f"  {i}. '{det['keyword']}' em {det['timestamp']:.2f}s")
        
        if not detections:
            print("   Nenhuma detecção.")
