"""
Aplicação principal do Sistema Wake Words.
Coordena detecção, STT e processamento de comandos.
"""

import sys
import time
import signal
import yaml
from pathlib import Path
from typing import Optional

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from audio_capture import AudioCapture, AudioDeviceManager
from logger import WakeWordsLogger
from wake_word import WakeWordDetector
from stt_engine import STTEngine, CommandRecorder
from command_processor import CommandProcessor, Command


class WakeWordsApp:
    """
    Aplicação principal do sistema Wake Words.
    Detecta wake words, transcreve comandos e executa ações.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Inicializa a aplicação.
        
        Args:
            config_path: Caminho do arquivo de configuração
        """
        self.config = self._load_config(config_path)
        
        # Inicializar logger
        self.logger_manager = WakeWordsLogger(self.config['logging'])
        self.logger = self.logger_manager.get_logger()
        
        # Inicializar componentes
        self.audio_capture: Optional[AudioCapture] = None
        self.wake_word_detector: Optional[WakeWordDetector] = None
        self.stt_engine: Optional[STTEngine] = None
        self.command_recorder: Optional[CommandRecorder] = None
        self.command_processor: Optional[CommandProcessor] = None
        
        # Estado
        self.running = False
        self.listen_for_command = False
        
        # Configurar signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_config(self, config_path: str) -> dict:
        """Carrega configuração do arquivo YAML."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Resolver paths relativos
            config_dir = Path(config_path).parent
            if 'vosk' in config:
                vosk_path = config['vosk']['model_path']
                if not Path(vosk_path).is_absolute():
                    config['vosk']['model_path'] = str(
                        (config_dir.parent / vosk_path).resolve()
                    )
            
            return config
            
        except FileNotFoundError:
            print(f"⚠️  Arquivo de configuração não encontrado: {config_path}")
            print("Usando configurações padrão...")
            return self._default_config()
        except Exception as e:
            print(f"⚠️  Erro ao carregar configuração: {e}")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Retorna configuração padrão."""
        return {
            'porcupine': {
                'access_key': 'YOUR_ACCESS_KEY_HERE',
                'keyword_path': None,
                'sensitivity': 0.5,
                'model_path': None
            },
            'vosk': {
                'model_path': 'models/vosk-model-small-pt-0.3',
                'sample_rate': 16000,
                'alternative': 0
            },
            'audio': {
                'device_index': None,
                'sample_rate': 16000,
                'channels': 1,
                'chunk_size': 512,
                'input_format': 'int16'
            },
            'command': {
                'timeout': 5.0,
                'silence_threshold': 0.3
            },
            'logging': {
                'level': 'INFO',
                'log_to_file': True,
                'log_dir': 'logs',
                'log_file': 'wake_words.log',
                'max_size_mb': 10,
                'backup_count': 5
            },
            'monitoring': {
                'log_cpu': True,
                'log_ram': True,
                'log_audio_level': True,
                'update_interval': 1.0
            },
            'debug': {
                'show_audio_devices': False,
                'log_audio_chunks': False,
                'verbose_output': False
            }
        }
    
    def initialize(self) -> bool:
        """
        Inicializa todos os componentes.
        
        Returns:
            True se inicializado com sucesso
        """
        try:
            self.logger.info("🚀 Inicializando Wake Words System...")
            
            # Mostrar dispositivos se habilitado
            if self.config['debug']['show_audio_devices']:
                AudioDeviceManager.print_devices()
            
            # Inicializar detector de wake word
            self.logger.info("🎙️  Inicializando Wake Word Detector...")
            self.wake_word_detector = WakeWordDetector(
                access_key=self.config['porcupine']['access_key'],
                keyword=self.config['porcupine'].get('keyword_path', 'porcupine') or 'porcupine',
                sensitivity=self.config['porcupine']['sensitivity'],
                model_path=self.config['porcupine']['model_path'],
                keyword_paths=None
            )
            
            # Inicializar STT
            self.logger.info("📝 Inicializando Speech-to-Text...")
            self.stt_engine = STTEngine(
                model_path=self.config['vosk']['model_path'],
                sample_rate=self.config['vosk']['sample_rate']
            )
            
            # Inicializar captura de áudio
            self.logger.info("🎤 Inicializando captura de áudio...")
            self.audio_capture = AudioCapture(
                sample_rate=self.config['audio']['sample_rate'],
                channels=self.config['audio']['channels'],
                chunk_size=self.wake_word_detector.frame_length,
                device_id=self.config['audio']['device_index']
            )
            
            # Inicializar gravador de comandos
            self.command_recorder = CommandRecorder(
                stt_engine=self.stt_engine,
                timeout=self.config['command']['timeout']
            )
            
            # Inicializar processador de comandos
            self.command_processor = CommandProcessor()
            
            # Registra handler customizado se necessário
            self._register_custom_handlers()
            
            self.logger_manager.log_startup_time()
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na inicialização: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def _register_custom_handlers(self):
        """Registra handlers customizados de comandos."""
        # Adicionar handlers customizados aqui se necessário
        pass
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de encerramento."""
        self.logger.info(f"🛑 Sinal recebido: {signum}")
        self.running = False
    
    def run(self):
        """Executa o loop principal."""
        if not self.wake_word_detector or not self.audio_capture:
            self.logger.error("Componentes não inicializados!")
            return
        
        self.running = True
        
        print("\n" + "=" * 60)
        print("SISTEMA WAKE WORDS - ATIVO")
        print("=" * 60)
        print(f"🎙️  Wake Word: '{self.wake_word_detector.keyword}'")
        print(f"📝 Fale a wake word e depois seu comando")
        print("=" * 60)
        print("Pressione Ctrl+C para sair")
        print("=" * 60 + "\n")
        
        # Iniciar captura de áudio
        try:
            self.audio_capture.start()
            
            last_monitor_time = time.time()
            frame_count = 0
            
            while self.running:
                # Ler frame do microfone
                chunk = self.audio_capture.read_chunk(timeout=1.0)
                
                if chunk is None:
                    continue
                
                # Flatten se necessário (para mono)
                if chunk.ndim > 1:
                    chunk = chunk[:, 0]
                
                frame_count += 1
                
                # Se esperando comando, processar com STT
                if self.listen_for_command:
                    self._process_command_audio(chunk)
                    continue
                
                # Detectar wake word
                if self.wake_word_detector.process_frame(chunk):
                    self._on_wake_word_detected()
                
                # Monitoramento periódico
                current_time = time.time()
                if current_time - last_monitor_time >= self.config['monitoring']['update_interval']:
                    if self.config['monitoring']['log_cpu'] or self.config['monitoring']['log_ram']:
                        self.logger_manager.log_system_stats()
                    last_monitor_time = current_time
                
                # Log de áudio (a cada 100 frames)
                if frame_count % 100 == 0 and self.config['monitoring']['log_audio_level']:
                    audio_level = self.audio_capture.get_audio_level(
                        chunk.reshape(-1, 1)
                    )
                    self.logger_manager.get_audio_logger().log_audio_level(
                        audio_level,
                        self.config['command']['silence_threshold']
                    )
            
        except KeyboardInterrupt:
            self.logger.info("⚠️  Interrupção pelo usuário")
        except Exception as e:
            self.logger.error(f"❌ Erro no loop principal: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            self.shutdown()
    
    def _on_wake_word_detected(self):
        """Callback quando wake word é detectada."""
        self.logger_manager.log_wake_word_detected(self.wake_word_detector.keyword)
        
        print("\n" + "✨" * 30)
        print(f"WAKE WORD DETECTADA!")
        print("✨" * 30 + "\n")
        
        # Iniciar modo de escuta de comando
        self.listen_for_command = True
        
        # Reset buffer de áudio
        while not self.audio_capture.audio_queue.empty():
            self.audio_capture.audio_queue.get_nowait()
    
    def _process_command_audio(self, chunk):
        """
        Processa áudio para reconhecimento de comando.
        
        Args:
            chunk: Chunk de áudio
        """
        import numpy as np
        
        # Buffer para armazenar áudio do comando
        if not hasattr(self, '_command_buffer'):
            self._command_buffer = []
        
        self._command_buffer.append(chunk)
        
        # Calcular duração do buffer
        buffer_duration = sum(len(c) for c in self._command_buffer) / self.audio_capture.sample_rate
        
        # Verificar nível de áudio
        audio_level = self.audio_capture.get_audio_level(chunk.reshape(-1, 1))
        
        # Se áudio detectado, continuar gravando
        if audio_level > self.config['command']['silence_threshold']:
            self._last_sound_time = time.time()
            return
        
        # Se silêncio por 1 segundo, processar comando
        if hasattr(self, '_last_sound_time'):
            silence_duration = time.time() - self._last_sound_time
            
            if silence_duration > 1.0 and len(self._command_buffer) > 0:
                # Processar comando
                self._execute_command()
                self._command_buffer = []
                self.listen_for_command = False
        
        # Timeout
        if buffer_duration > self.config['command']['timeout']:
            if len(self._command_buffer) > 0:
                self._execute_command()
            
            self._command_buffer = []
            self.listen_for_command = False
    
    def _execute_command(self):
        """Executa o reconhecimento e processamento do comando."""
        if not hasattr(self, '_command_buffer') or not self._command_buffer:
            return
        
        import numpy as np
        
        # Concatenar buffer
        command_audio = np.concatenate(self._command_buffer, axis=0)
        if command_audio.ndim > 1:
            command_audio = command_audio[:, 0]
        
        print("\n🎙️  Processando comando...")
        
        # Transcrever
        result = self.stt_engine.process_audio_array(command_audio)
        
        if result and result.get('text'):
            text = result['text'].strip()
            self.logger_manager.log_command_detected(text)
            
            # Criar comando
            command = Command(text=text)
            
            # Executar
            print(f"\n📝 Comando: '{text}'")
            success = self.command_processor.execute(command)
            
            if success:
                print("✅ Comando executado!\n")
            else:
                print("❌ Falha ao executar comando\n")
        else:
            print("⚠️  Não entendi o comando\n")
        
        # Reset STT
        self.stt_engine.reset()
    
    def shutdown(self):
        """Desliga a aplicação gracefulmente."""
        self.logger.info("🔄 Desligando...")
        
        self.running = False
        
        # Parar captura de áudio
        if self.audio_capture:
            self.audio_capture.stop()
        
        # Liberar recursos
        if self.wake_word_detector:
            self.wake_word_detector.release()
        
        if self.stt_engine:
            self.stt_engine.release()
        
        self.logger_manager.log_shutdown()
        
        print("\n👋 Até logo!\n")


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sistema Wake Words Command')
    parser.add_argument('--config', '-c', 
                       default='config/config.yaml',
                       help='Caminho do arquivo de configuração')
    parser.add_argument('--list-devices', '-l',
                       action='store_true',
                       help='Listar dispositivos de áudio')
    parser.add_argument('--test-wake-word', '-w',
                       action='store_true',
                       help='Testar detecção de wake word')
    parser.add_argument('--test-mic', '-m',
                       action='store_true',
                       help='Testar microfone')
    
    args = parser.parse_args()
    
    # Modos especiais
    if args.list_devices:
        AudioDeviceManager.print_devices()
        return
    
    # Carregar config
    app = WakeWordsApp(args.config)
    
    # Modos de teste
    if args.test_mic:
        from tests.test_real import test_microphone
        test_microphone()
        return
    
    if args.test_wake_word:
        if not app.initialize():
            return
        
        from wake_word import WakeWordTester
        tester = WakeWordTester(app.wake_word_detector)
        tester.test_microphone(duration=10.0)
        app.shutdown()
        return
    
    # Modo normal
    if app.initialize():
        app.run()
    else:
        print("❌ Falha na inicialização")
        sys.exit(1)


if __name__ == '__main__':
    main()
