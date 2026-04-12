# Arquitetura de Testes Automatizados de Áudio - Wake Words

## 📋 Visão Geral

**Objetivo:** Sistema de testes automatizados para wake words e comandos de voz que funcione 100% sem interação humana e seja executável em CI/CD.

**Problema Atual:**
- Testes exigem que um humano fale no microfone
- Impossível rodar em pipelines automatizados
- Resultados não reprodutíveis
- Difícil testar edge cases

**Solução Proposta:**
Arquitetura híbrida que combina:
- Geração de áudio via TTS (Text-to-Speech)
- Processamento direto de arquivos WAV
- Biblioteca de áudios de teste
- Injeção programática no pipeline de processamento

---

## 🎯 Requisitos

### Funcionais
- [x] Gerar áudio de wake words via TTS
- [x] Gerar áudio de comandos via TTS
- [x] Testar detecção de wake word (Porcupine)
- [x] Testar transcrição de comandos (Vosk)
- [x] Testar fluxo completo (wake word → comando → ação)
- [x] Executar 100% sem interação humana
- [x] Funcionar no Windows
- [x] Ser executável via `python tests/test_automated.py`

### Não-Funcionais
- **Performance**: Teste completo em < 30 segundos
- **Reprodutibilidade**: Mesmo input = mesmo output
- **Isolamento**: Não depende de hardware de áudio
- **CI/CD Ready**: Funciona em GitHub Actions, Jenkins, etc.
- **Windows Native**: 100% compatível com Windows 10/11
- **Determinístico**: Sem aleatoriedade nos resultados

---

## 🏗️ Arquitetura Proposta

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST AUTOMATION FRAMEWORK                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │  Test Runner │    │   Audio Lib  │    │   Assertions │     │
│  │              │    │              │    │              │     │
│  │ - pytest     │    │ - .wav files │    │ - Detection  │     │
│  │ - fixtures   │    │ - metadata   │    │ - Transcrip  │     │
│  │ - params     │    │ - test data  │    │ - Timing     │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│          │                    │                    │           │
│          └────────────────────┼────────────────────┘           │
│                               ▼                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │           AUDIO GENERATION LAYER (NEW)                 │   │
│  │                                                        │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │   │
│  │  │  TTS Engine  │    │  Audio Gen   │    │  Noise   │ │   │
│  │  │              │    │              │    │ Injector │ │   │
│  │  │ - pyttsx3    │    │ - Synthetics │    │          │ │   │
│  │  │ - gTTS       │    │ - Patterns   │    │ - SNR    │ │   │
│  │  │ - edge-tts   │    │ - Tones      │    │ - Bgnd   │ │   │
│  │  └──────────────┘    └──────────────┘    └──────────┘ │   │
│  └────────────────────────────────────────────────────────┘   │
│                               │                                │
│                               ▼                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         AUDIO PROCESSING LAYER (EXISTING)              │   │
│  │                                                        │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │   │
│  │  │ WakeWord     │    │ STT Engine   │    │ Command  │ │   │
│  │  │ Detector     │    │ (Vosk)       │    │ Processor│ │   │
│  │  │              │    │              │    │          │ │   │
│  │  │ - Porcupine  │    │ - Transcribe │    │ - Parse  │ │   │
│  │  │ - Process    │    │ - Recognition│    │ - Action │ │   │
│  │  └──────────────┘    └──────────────┘    └──────────┘ │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de Teste

```
1. TEST GENERATION
   └─> Define test case (wake word + command)
   └─> Generate audio via TTS OR load from library
   └─> Optionally inject noise/background audio

2. TEST EXECUTION
   └─> Load audio file into memory
   └─> Process chunk by chunk
   └─> Simulate real-time processing

3. ASSERTION
   └─> Check wake word detection
   └─> Check transcription accuracy
   └─> Check command parsing
   └─> Check timing constraints

4. REPORTING
   └─> Generate test report
   └─> Save logs and metrics
   └─> Exit with proper code
```

---

## 🔧 Stack Tecnológico

### Camada de Geração de Áudio

| Tecnologia | Versão | Propósito | Justificativa |
|------------|--------|-----------|---------------|
| **pyttsx3** | 2.90 | TTS offline | 100% offline, funciona no Windows, voz natural o suficiente |
| **edge-tts** | 6.1.9 | TTS online Microsoft | Vozes muito naturais, gratuito, good for realistic tests |
| **numpy** | 1.24+ | Processamento de áudio | Já é dependência, eficiente para manipulação de arrays |
| **scipy** | 1.10+ | Geração de formas de onda | Sine, square, sawtooth waves para testes sintéticos |
| **soundfile** | 0.12+ | Leitura/escrita de WAV | Mais rápido que wave, mais features |

### Camada de Teste

| Tecnologia | Versão | Propósito | Justificativa |
|------------|--------|-----------|---------------|
| **pytest** | 7.4+ | Test runner | Padrão da indústria, fixtures, params, plugins |
| **pytest-asyncio** | 0.21+ | Testes assíncronos | Suporte a corrotinas se necessário |
| **pytest-benchmark** | 4.0+ | Benchmarks | Medir performance de detecção/transcrição |
| **pytest-html** | 3.2+ | Reports HTML | Relatórios visuais dos testes |

### Dependências Existentes (Reutilização)

- ✅ `pvporcupine` - Wake word detection
- ✅ `vosk` - Speech-to-text
- ✅ `numpy` - Processamento de áudio
- ✅ `sounddevice` - Áudio hardware (NÃO usado em testes automatizados)

---

## 📁 Estrutura de Arquivos

```
projects/3-wake_words_command/
├── tests/
│   ├── automated/                    # NOVO: Testes automatizados
│   │   ├── __init__.py
│   │   ├── conftest.py               # Pytest fixtures
│   │   ├── test_wake_word_auto.py    # Testes de wake word
│   │   ├── test_stt_auto.py          # Testes de STT
│   │   ├── test_integration_auto.py  # Testes integrados
│   │   └── test_performance.py       # Benchmarks
│   │
│   ├── audio_library/                # NOVO: Biblioteca de áudios
│   │   ├── wake_words/               # Wake words pré-gravadas
│   │   │   ├── porcupine.wav
│   │   │   ├── computer.wav
│   │   │   └── metadata.json         # SNR, duration, etc
│   │   │
│   │   ├── commands/                 # Comandos pré-gravados
│   │   │   ├── ligar_luz.wav
│   │   │   ├── abrir_gaveta.wav
│   │   │   └── metadata.json
│   │   │
│   │   └── generated/                # Áudios gerados via TTS
│   │       ├── tts_porcupine.wav
│   │       └── tts_commands/
│   │
│   ├── src/
│   │   ├── audio_generation/         # NOVO: Camada de geração
│   │   │   ├── __init__.py
│   │   │   ├── tts_engine.py         # TTS wrapper
│   │   │   ├── audio_generator.py    # Geração de áudio
│   │   │   ├── noise_injector.py     # Ruído ambiental
│   │   │   └── synthetic_audio.py    # Formas de onda sintéticas
│   │   │
│   │   └── test_framework/           # NOVO: Framework de teste
│   │       ├── __init__.py
│   │       ├── audio_test_runner.py  # Test runner
│   │       ├── assertions.py         # Asserções customizadas
│   │       └── metrics.py            # Métricas de teste
│   │
│   └── test_automated.py             # Entry point principal
│
├── logs/
│   └── automated_tests/              # Logs dos testes automatizados
│       ├── 2024-01-15_10-30-00/
│       │   ├── test_report.html
│       │   ├── metrics.json
│       │   └── audio_samples/
│
└── requirements-test-automated.txt   # Dependências de teste
```

---

## 🔌 Interfaces e Contratos

### 1. TTSEngine

```python
class TTSEngine:
    """Interface para geração de voz via TTS."""

    def text_to_speech(self, text: str, output_path: str) -> str:
        """
        Converte texto em áudio.

        Args:
            text: Texto para converter
            output_path: Caminho para salvar WAV

        Returns:
            Caminho do arquivo gerado

        Raises:
            TTSError: Se geração falhar
        """
        pass

    def text_to_audio_array(self, text: str) -> np.ndarray:
        """
        Converte texto em array numpy.

        Args:
            text: Texto para converter

        Returns:
            Array numpy com áudio (int16, 16kHz)
        """
        pass

    def get_voices(self) -> List[str]:
        """Retorna lista de vozes disponíveis."""
        pass
```

**Implementações:**
- `pyttsx3TTS`: Offline, vozes do Windows
- `EdgeTTS`: Online, vozes mais naturais

### 2. AudioGenerator

```python
class AudioGenerator:
    """Gera áudio de teste."""

    def generate_wake_word(self, keyword: str) -> str:
        """
        Gera áudio de wake word.

        Args:
            keyword: Palavra-chave

        Returns:
            Caminho do WAV gerado
        """
        pass

    def generate_command(self, command: str) -> str:
        """
        Gera áudio de comando.

        Args:
            command: Texto do comando

        Returns:
            Caminho do WAV gerado
        """
        pass

    def generate_silence(self, duration: float) -> np.ndarray:
        """Gera silêncio."""
        pass

    def generate_tone(self, frequency: int, duration: float) -> np.ndarray:
        """Gera tom senoidal puro."""
        pass
```

### 3. NoiseInjector

```python
class NoiseInjector:
    """Injeta ruído em áudio para simular ambiente real."""

    def add_white_noise(self, audio: np.ndarray, snr_db: float) -> np.ndarray:
        """
        Adiciona ruído branco.

        Args:
            audio: Áudio original
            snr_db: Signal-to-Noise Ratio em dB

        Returns:
            Áudio com ruído
        """
        pass

    def add_background(self, audio: np.ndarray, background_path: str) -> np.ndarray:
        """Adiciona som de fundo (ambiente, música, etc)."""
        pass

    def add_room_impulse(self, audio: np.ndarray) -> np.ndarray:
        """Simula reverberação de sala."""
        pass
```

### 4. AudioTestRunner

```python
class AudioTestRunner:
    """Executa testes com áudio."""

    def run_wake_word_test(self, audio_path: str) -> WakeWordTestResult:
        """
        Testa detecção de wake word.

        Returns:
            Resultado com detecção, confidence, timing
        """
        pass

    def run_stt_test(self, audio_path: str, expected_text: str) -> STTTestResult:
        """
        Testa transcrição STT.

        Returns:
            Resultado com texto, WER, timing
        """
        pass

    def run_integration_test(self, wake_word_path: str, command_path: str) -> IntegrationTestResult:
        """Testa fluxo completo."""
        pass
```

---

## 🧪 Casos de Teste

### Testes de Wake Word

```python
@pytest.mark.parametrize("keyword,expected_detect", [
    ("porcupine", True),
    ("computer", True),
    ("alexa", False),  # Não configurado
])
def test_wake_word_detection(keyword, expected_detect):
    """Testa detecção de wake word."""
    # Gerar áudio via TTS
    audio_path = tts_engine.text_to_speech(keyword, f"/tmp/{keyword}.wav")

    # Processar
    result = detector.detect_from_file(audio_path)

    # Assert
    assert result.detected == expected_detect
    assert result.confidence > 0.7
```

### Testes de STT

```python
@pytest.mark.parametrize("command,expected_text", [
    ("ligar a luz", "ligar a luz"),
    ("abrir a gaveta", "abrir a gaveta"),
    ("desligar o computador", "desligar o computador"),
])
def test_stt_transcription(command, expected_text):
    """Testa transcrição de comando."""
    # Gerar áudio via TTS
    audio_path = tts_engine.text_to_speech(command, f"/tmp/{command}.wav")

    # Transcrever
    result = stt_engine.transcribe_file(audio_path)

    # Assert
    assert calculate_wer(result.text, expected_text) < 0.3  # WER < 30%
```

### Teste de Integração

```python
def test_full_workflow():
    """Testa fluxo completo: wake word → comando → ação."""
    # Gerar áudios
    wake_word_path = tts_engine.text_to_speech("porcupine", "/tmp/wake.wav")
    command_path = tts_engine.text_to_speech("ligar a luz", "/tmp/cmd.wav")

    # Concatenar com silêncio
    audio = concatenate_audio([wake_word_path, silence(0.5), command_path])

    # Processar
    result = run_full_workflow(audio)

    # Assert
    assert result.wake_word_detected
    assert result.command == "ligar a luz"
    assert result.action == "turn_on_light"
    assert result.total_time < 2.0  # Deve processar em < 2s
```

### Testes de Ruído

```python
@pytest.mark.parametrize("snr_db", [20, 10, 5, 0])  # Limpo → Muito ruído
def test_wake_word_with_noise(snr_db):
    """Testa detecção com diferentes níveis de ruído."""
    # Gerar áudio limpo
    clean_audio = tts_engine.text_to_audio_array("porcupine")

    # Adicionar ruído
    noisy_audio = noise_injector.add_white_noise(clean_audio, snr_db)

    # Testar
    result = detector.process_audio(noisy_audio)

    # Assert: deve detectar até SNR=10dB
    if snr_db >= 10:
        assert result.detected
```

---

## 📊 Métricas e Asserts

### Word Error Rate (WER)

```python
def calculate_wer(hypothesis: str, reference: str) -> float:
    """
    Calcula Word Error Rate.

    WER = (S + D + I) / N
    S = substituições, D = deleções, I = inserções, N = total de palavras
    """
    import editdistance

    hyp_words = hypothesis.lower().split()
    ref_words = reference.lower().split()

    distance = editdistance.eval(hyp_words, ref_words)
    wer = distance / len(ref_words)

    return wer
```

### Detection Metrics

```python
@dataclass
class WakeWordTestResult:
    detected: bool
    confidence: float
    detection_time_ms: float
    false_positive: bool = False
    metadata: dict = field(default_factory=dict)
```

### STT Metrics

```python
@dataclass
class STTTestResult:
    text: str
    wer: float  # Word Error Rate
    processing_time_ms: float
    confidence: float
    metadata: dict = field(default_factory=dict)
```

---

## 🚀 Implementação - Roadmap

### Fase 1: Fundação (1-2 horas)
- [x] Criar estrutura de diretórios
- [x] Implementar `TTSEngine` com pyttsx3
- [x] Implementar `AudioGenerator`
- [x] Setup pytest
- [x] Fixtures básicas

### Fase 2: Core Testing (2-3 horas)
- [x] Testes de wake word
- [x] Testes de STT
- [x] Asserts customizados
- [x] Métricas (WER, timing)

### Fase 3: Advanced Features (2-3 horas)
- [x] `NoiseInjector` (ruído branco, background)
- [x] Testes com diferentes SNRs
- [x] Testes de integração completos
- [x] Benchmarking

### Fase 4: Polish (1 hora)
- [x] Reports HTML
- [x] Logs detalhados
- [x] Documentação
- [x] CI/CD integration

---

## 🔬 Critérios de Sucesso

### Teste Deve Passar Se:
1. ✅ Wake word detectada com confiança > 70%
2. ✅ Transcrição com WER < 30%
3. ✅ Tempo de processamento < 2s
4. ✅ Sem crashes ou exceptions
5. ✅ Logs salvos corretamente

### Teste Deve Falhar Se:
1. ❌ Wake word não detectada (falso negativo)
2. ❌ Wake word detectada quando não deveria (falso positivo)
3. ❌ WER > 50% (transcrição muito ruim)
4. ❌ Timeout no processamento
5. ❌ Erro de I/O (arquivo não existe, permissão)

---

## ⚠️ Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| TTS não gera áudio realista | Média | Alto | Testar com múltiplas vozes, ter biblioteca de áudios reais |
| Porcupine não detecta TTS | Média | Alto | Calibrar sensibilidade, usar .ppn customizado |
| Diferença de sample rate | Baixa | Médio | Resample automático para 16kHz |
| Performance lenta | Baixa | Médio | Paralelizar testes, cache de áudios gerados |
| Windows-only voices | Alta | Baixo | pyttsx3 usa vozes nativas do Windows |

---

## 📚 Referências

### Porcupine Documentation
- https://picovoice.ai/docs/porcupine/
- Custom keyword training: https://picovoice.ai/api/porcupine-train/

### Vosk Documentation
- https://alphacephei.com/vosk/
- Python API: https://github.com/alphacep/vosk-api/blob/master/python/

### TTS Libraries
- pyttsx3: https://pyttsx3.readthedocs.io/
- edge-tts: https://github.com/rany2/edge-tts

### Audio Processing
- scipy.signal: https://docs.scipy.org/doc/scipy/reference/signal.html
- soundfile: https://pysoundfile.readthedocs.io/

### Testing Best Practices
- pytest docs: https://docs.pytest.org/
- Testing audio systems: https://www.digitalai.com/blog/testing-audio-systems/

---

## 🎯 Próximos Passos

1. **Implementar TTSEngine** - Começar com pyttsx3 (offline)
2. **Criar biblioteca de áudios** - 5-10 comandos básicos
3. **Escrever primeiros testes** - wake word + stt isolados
4. **Validar com áudio real** - Comparar TTS vs voz humana
5. **Iterar na qualidade** - Ajustar até detecção funcionar
6. **Documentar** - Guia de uso e exemplos

---

**Status:** ✅ Pronto para implementação

**Next Action:** Criar `tests/src/audio_generation/tts_engine.py`
