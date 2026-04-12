"""
Speech-to-Text REAL usando Vosk.
Reconhecimento offline de fala em português.
"""

import os
import json
import queue
import numpy as np
from typing import Optional, Dict, List
from pathlib import Path
import logging

try:
    import vosk
    import wave
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    logging.warning("Vosk não instalado. Execute: pip install vosk")


class STTEngine:
    """
    Motor de Speech-to-Text usando Vosk.
    Reconhecimento offline de fala.
    """
    
    def __init__(self, model_path: str, sample_rate: int = 16000):
        """
        Inicializa o motor STT.
        
        Args:
            model_path: Caminho para o modelo Vosk
            sample_rate: Taxa de amostragem do áudio (Hz)
        """
        self.model_path = model_path
        self.sample_rate = sample_rate
        
        self.model: Optional[vosk.Model] = None
        self.recognizer: Optional[vosk.KaldiRecognizer] = None
        self.is_initialized = False
        
        if VOSK_AVAILABLE:
            self._initialize()
    
    def _initialize(self):
        """Inicializa o modelo Vosk."""
        try:
            # Verificar se modelo existe
            model_path = Path(self.model_path)
            
            if not model_path.exists():
                raise FileNotFoundError(
                    f"Modelo Vosk não encontrado em: {self.model_path}\n"
                    f"Baixe um modelo em: https://alphacephei.com/vosk/models\n"
                    f"Recomendado: vosk-model-small-pt-0.3"
                )
            
            # Carregar modelo
            logging.info(f"📦 Carregando modelo Vosk de: {self.model_path}")
            self.model = vosk.Model(str(model_path))
            
            # Criar recognizer
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
            
            self.is_initialized = True
            
            logging.info(f"✅ STT Engine inicializado")
            logging.info(f"   Modelo: {model_path.name}")
            logging.info(f"   Sample rate: {self.sample_rate} Hz")
            
        except Exception as e:
            logging.error(f"❌ Erro ao inicializar Vosk: {e}")
            self.is_initialized = False
            raise
    
    def process_audio(self, audio_data: bytes, final: bool = False) -> Optional[dict]:
        """
        Processa dados de áudio e retorna resultado.
        
        Args:
            audio_data: Bytes PCM do áudio
            final: Se é o último chunk do áudio
            
        Returns:
            Dict com resultado do reconhecimento ou None
        """
        if not self.is_initialized or not self.recognizer:
            logging.error("STT não inicializado!")
            return None
        
        try:
            # Processar áudio
            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                return result
            
            # Se final, obter resultado parcial
            if final:
                result = json.loads(self.recognizer.FinalResult())
                return result
            
            return None
            
        except Exception as e:
            logging.error(f"Erro ao processar áudio: {e}")
            return None
    
    def process_audio_array(self, audio_array: np.ndarray) -> Optional[dict]:
        """
        Processa array numpy de áudio.
        
        Args:
            audio_array: Array numpy de int16
            
        Returns:
            Dict com resultado do reconhecimento
        """
        # Converter para bytes PCM
        if audio_array.dtype != np.int16:
            audio_array = (audio_array * np.iinfo(np.int16).max).astype(np.int16)
        
        audio_bytes = audio_array.tobytes()
        return self.process_audio(audio_bytes)
    
    def transcribe_file(self, audio_file: str) -> Dict:
        """
        Transcreve arquivo de áudio completo.
        
        Args:
            audio_file: Caminho do arquivo WAV
            
        Returns:
            Dict com transcrição completa
        """
        if not self.is_initialized:
            return {'error': 'STT não inicializado'}
        
        try:
            # Abrir arquivo
            wf = wave.open(audio_file, 'rb')
            
            # Verificar compatibilidade
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != self.sample_rate:
                logging.warning(f"⚠️ Formato do áudio não é ideal: "
                              f"channels={wf.getnchannels()}, "
                              f"width={wf.getsampwidth()}, "
                              f"rate={wf.getframerate()}")
            
            # Reset recognizer
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
            
            # Processar arquivo
            results = []
            partial_results = []
            
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    if result.get('text'):
                        results.append(result)
                else:
                    partial = json.loads(self.recognizer.PartialResult())
                    if partial.get('partial'):
                        partial_results.append(partial)
            
            # Resultado final
            final = json.loads(self.recognizer.FinalResult())
            
            wf.close()
            
            # Combinar textos
            full_text = ' '.join([r.get('text', '') for r in results])
            if final.get('text'):
                full_text += ' ' + final['text']
            
            return {
                'text': full_text.strip(),
                'results': results,
                'partial_results': partial_results,
                'final': final
            }
            
        except Exception as e:
            logging.error(f"Erro ao transcrever arquivo: {e}")
            return {'error': str(e)}
    
    def transcribe_stream(self, audio_generator):
        """
        Transcreve stream de áudio (generator).
        
        Args:
            audio_generator: Generator que produz bytes PCM
            
        Yields:
            Dict com resultados parciais e finais
        """
        if not self.is_initialized:
            yield {'error': 'STT não inicializado'}
            return
        
        try:
            # Reset recognizer
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
            
            for audio_chunk in audio_generator:
                if self.recognizer.AcceptWaveform(audio_chunk):
                    result = json.loads(self.recognizer.Result())
                    if result.get('text'):
                        yield {'type': 'final', 'data': result}
                else:
                    partial = json.loads(self.recognizer.PartialResult())
                    if partial.get('partial'):
                        yield {'type': 'partial', 'data': partial}
            
            # Resultado final
            final = json.loads(self.recognizer.FinalResult())
            if final.get('text'):
                yield {'type': 'final', 'data': final}
                
        except Exception as e:
            logging.error(f"Erro no stream: {e}")
            yield {'error': str(e)}
    
    def reset(self):
        """Reseta o recognizer para nova transcrição."""
        if self.is_initialized and self.model:
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
    
    @staticmethod
    def list_models(models_dir: str = "models") -> List[Path]:
        """
        Lista modelos Vosk disponíveis em um diretório.
        
        Args:
            models_dir: Diretório para buscar modelos
            
        Returns:
            Lista de Path com modelos encontrados
        """
        models_path = Path(models_dir)
        
        if not models_path.exists():
            return []
        
        # Buscar diretórios com arquivo model/conf
        models = []
        for item in models_path.iterdir():
            if item.is_dir():
                conf_file = item / "am" / "final.mdl"
                if conf_file.exists():
                    models.append(item)
        
        return models
    
    @staticmethod
    def print_available_models(models_dir: str = "models"):
        """Imprime modelos disponíveis."""
        models = STTEngine.list_models(models_dir)
        
        print("\n" + "=" * 60)
        print(f"MODELOS VOSK DISPONÍVEIS EM: {models_dir}")
        print("=" * 60)
        
        if not models:
            print("⚠️  Nenhum modelo encontrado!")
            print("\nBaixe modelos em: https://alphacephei.com/vosk/models")
            print("Recomendado: vosk-model-small-pt-0.3 (Português)")
            print("Extraia para: models/vosk-model-small-pt-0.3/")
        else:
            for i, model in enumerate(models, 1):
                size_mb = sum(f.stat().st_size for f in model.rglob('*') if f.is_file()) / (1024 * 1024)
                print(f"{i}. {model.name} (~{size_mb:.0f} MB)")
        
        print("=" * 60 + "\n")
    
    def release(self):
        """Libera recursos."""
        self.model = None
        self.recognizer = None
        self.is_initialized = False
        logging.info("🔓 Recursos do STT liberados")


class CommandRecorder:
    """
    Grava comandos de voz após detecção de wake word.
    """
    
    def __init__(self, stt_engine: STTEngine, timeout: float = 5.0):
        """
        Inicializa gravador de comandos.
        
        Args:
            stt_engine: Instância do STTEngine
            timeout: Tempo máximo de gravação (segundos)
        """
        self.stt_engine = stt_engine
        self.timeout = timeout
        self.silence_threshold = 0.1  # Nível de silêncio
    
    def record_command(self, audio_capture, silence_threshold: float = 0.1) -> Optional[str]:
        """
        Grava comando do microfone.
        
        Args:
            audio_capture: Instância de AudioCapture
            silence_threshold: Nível para considerar silêncio
            
        Returns:
            Texto do comando reconhecido ou None
        """
        import time
        
        logging.info("🎙️  Gravando comando... (fale agora!)")
        
        start_time = time.time()
        audio_buffer = []
        silence_duration = 0
        max_silence = 1.0  # 1 segundo de silêncio para parar
        
        # Reset STT
        self.stt_engine.reset()
        
        while time.time() - start_time < self.timeout:
            # Ler chunk
            chunk = audio_capture.read_chunk(timeout=0.5)
            
            if chunk is None:
                continue
            
            # Calcular nível do áudio
            audio_level = audio_capture.get_audio_level(chunk)
            
            if audio_level > silence_threshold:
                # Fala detectada
                silence_duration = 0
                audio_buffer.append(chunk)
                logging.debug(f"Áudio detectado: {audio_level:.3f}")
            else:
                # Silêncio
                silence_duration += len(chunk) / audio_capture.sample_rate
                audio_buffer.append(chunk)
                
                if silence_duration > max_silence and len(audio_buffer) > 0:
                    logging.debug("Silêncio detectado, parando gravação...")
                    break
        
        if not audio_buffer:
            logging.warning("⚠️  Nenhum áudio gravado")
            return None
        
        # Concatenar áudio
        audio_data = np.concatenate(audio_buffer, axis=0)
        
        # Transcrever
        logging.info("🔄 Processando áudio...")
        result = self.stt_engine.transcribe_file(audio_data)
        
        if result.get('error'):
            logging.error(f"Erro na transcrição: {result['error']}")
            return None
        
        text = result.get('text', '').strip()
        
        if text:
            logging.info(f"✅ Comando reconhecido: '{text}'")
        else:
            logging.warning("⚠️  Nenhuma fala reconhecida")
        
        return text if text else None
