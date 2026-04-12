# Testes Automatizados de Áudio - Wake Words

Sistema completo de testes automatizados para detecção de wake words e reconhecimento de comandos de voz, **SEM necessidade de interação humana**.

## 🎯 O Que Este Sistema Faz

- ✅ Gera áudio de wake words via TTS (síntese de voz)
- ✅ Gera áudio de comandos via TTS
- ✅ Testa detecção de wake word (Porcupine)
- ✅ Testa transcrição de comandos (Vosk)
- ✅ Testa fluxo completo (wake word → comando → ação)
- ✅ Adiciona ruído realista aos testes
- ✅ **100% automatizado** - funciona em CI/CD
- ✅ **Reprodutível** - mesmo input = mesmo output
- ✅ **Sem microfone humano** necessário

## 🚀 Uso Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements-test-automated.txt
```

### 2. Configurar Chave Porcupine

```bash
# Windows CMD
set PORCUPINE_ACCESS_KEY=sua_chave_aqui

# Windows PowerShell
$env:PORCUPINE_ACCESS_KEY="sua_chave_aqui"

# Linux/Mac
export PORCUPINE_ACCESS_KEY=sua_chave_aqui
```

**Obter chave gratuita:** https://console.picovoice.ai/

### 3. Baixar Modelo Vosk (Português)

```bash
# Criar diretório
mkdir -p models

# Baixar modelo small (~50MB)
# Via navegador: https://alphacephei.com/vosk/models
# Escolha: vosk-model-small-pt-0.3.zip

# Extrair para models/vosk-model-small-pt-0.3/
```

### 4. Rodar Testes

```bash
# Gerar biblioteca de áudio primeiro
python tests/test_automated.py --generate-audio

# Rodar todos os testes
python tests/test_automated.py

# Teste rápido
python tests/test_automated.py --quick

# Testar apenas wake word
python tests/test_automated.py --wake-word

# Testar apenas STT
python tests/test_automated.py --stt

# Testar integração completa
python tests/test_automated.py --integration
```

## 📁 Estrutura de Arquivos

```
tests/
├── test_automated.py              # Entry point principal
├── conftest.py                     # Configuração pytest
├── automated/                      # Testes automatizados
│   ├── test_wake_word_auto.py     # Testes de wake word
│   ├── test_stt_auto.py           # Testes de STT
│   └── test_integration_auto.py   # Testes de integração
├── src/                            # Código de suporte
│   ├── audio_generation/           # Geração de áudio
│   │   ├── tts_engine.py          # TTS (pyttsx3, edge-tts)
│   │   ├── audio_generator.py     # Gerador de áudio
│   │   └── noise_injector.py      # Injeção de ruído
│   └── test_framework/             # Framework de teste
│       ├── audio_test_runner.py   # Executor de testes
│       ├── assertions.py          # Asserções customizadas
│       └── metrics.py             # Métricas (WER, CER)
└── audio_library/                  # Biblioteca de áudio
    ├── wake_words/                # Wake words pré-gravadas
    ├── commands/                  # Comandos pré-gravados
    └── generated/                 # Áudios gerados via TTS
```

## 🧪 Como Funciona

### 1. Geração de Áudio via TTS

```python
from tests.src.audio_generation import AudioGenerator, Pyttsx3TTS

# Criar gerador
tts = Pyttsx3TTS(rate=150)
generator = AudioGenerator(tts_engine=tts)

# Gerar wake word
ww_path = generator.generate_wake_word("porcupine")

# Gerar comando
cmd_path = generator.generate_command("ligar a luz")

# Gerar cenário completo
scenario_path = generator.generate_test_scenario(
    wake_word="porcupine",
    command="abrir a porta",
    output_path="scenario.wav"
)
```

### 2. Teste de Wake Word

```python
from src.wake_word import WakeWordDetector
from tests.src.test_framework import AudioTestRunner

# Criar detector
detector = WakeWordDetector(access_key=YOUR_KEY, keyword="porcupine")

# Criar test runner
runner = AudioTestRunner(wake_word_detector=detector)

# Testar
result = runner.run_wake_word_test("porcupine.wav", expected_detect=True)

print(f"Detectado: {result.detected}")
print(f"Detecções: {result.num_detections}")
print(f"Tempo: {result.detection_time_ms}ms")
```

### 3. Teste de STT

```python
from src.stt_engine import STTEngine

# Criar STT
stt = STTEngine(model_path="models/vosk-model-small-pt-0.3")

# Criar test runner
runner = AudioTestRunner(stt_engine=stt)

# Testar
result = runner.run_stt_test(
    "command.wav",
    expected_text="ligar a luz",
    max_wer=0.5
)

print(f"Texto: {result.text}")
print(f"WER: {result.wer * 100:.1f}%")
print(f"Tempo: {result.processing_time_ms}ms")
```

### 4. Injeção de Ruído

```python
from tests.src.audio_generation import NoiseInjector

injector = NoiseInjector()

# Adicionar ruído branco
noisy = injector.add_white_noise(audio, snr_db=20)

# Adicionar reverb
reverb = injector.add_room_impulse(audio, room_size="medium")

# Simular ligação telefônica
phone = injector.simulate_phone_call(audio)
```

## 📊 Métricas

### Word Error Rate (WER)

```
WER = (Substituições + Deleções + Inserções) / Total de Palavras

0.0  = Perfeito
0.5  = 50% de erro (aceitável para TTS)
1.0  = 100% de erro (falha total)
```

### Níveis de Áudio

```
-6 dB   = 50% de volume (bom)
-20 dB  = 10% de volume (baixo)
-60 dB  = 1% de volume (muito baixo)
-inf dB = Silêncio
```

## 🔧 Configuração Avançada

### Sensibilidade do Porcupine

```python
detector = WakeWordDetector(
    access_key=YOUR_KEY,
    keyword="porcupine",
    sensitivity=0.5  # 0.0 a 1.0 (padrão: 0.5)
)
```

- **0.3-0.4**: Mais sensível (mais falsos positivos)
- **0.5**: Equilibrado (recomendado)
- **0.6-0.7**: Menos sensível (pode perder detecções)

### Escolha de Voz TTS

```python
# Usar voz específica do sistema
tts = Pyttsx3TTS(voice_id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0")

# Listar vozes disponíveis
Pyttsx3TTS.print_available_voices()
```

### Níveis de Ruído

```python
# SNR (Signal-to-Noise Ratio) em dB
snr_db = 20  # Valores típicos

snr_db >= 20  # Áudio limpo
10 <= snr_db < 20  # Ruído moderado
snr_db < 10   # Muito ruído
```

## 📈 Exemplos de Saída

```
================================================================================
                    AUTOMATED AUDIO TESTING
================================================================================

✅ All dependencies installed
✅ PORCUPINE_ACCESS_KEY is set
✅ Vosk model found: models/vosk-model-small-pt-0.3

🧪 Running tests: tests/automated/ -v --tb=short

tests/test_wake_word_auto.py::TestWakeWordTTS::test_detect_porcupine_tts PASSED [15%]
tests/test_wake_word_auto.py::TestWakeWordTTS::test_detect_with_noise[30] PASSED [30%]
tests/test_stt_auto.py::TestSTTTTS::test_transcribe_commands PASSED [45%]
tests/test_integration_auto.py::TestIntegrationWorkflow::test_full_workflow PASSED [60%]

✅ All tests passed!

================================================================================
                              ✅ SUCCESS
================================================================================
```

## 🐛 Troubleshooting

### Pyttsx3 não produz áudio

```python
# Verificar vozes instaladas
python -c "import pyttsx3; e = pyttsx3.init(); print([v.name for v in e.getProperty('voices')])"

# Se não houver vozes em português, instalar:
# Windows Settings → Time & Language → Speech → Manage voices
```

### Porcupine não detecta TTS

- Aumentar sensibilidade: `sensitivity=0.4`
- Tentar taxas de fala diferentes: `rate=120, 150, 180`
- Verificar sample rate: deve ser 16kHz
- Normalizar volume do áudio

### Vosk transcrição ruim

- Usar modelo maior: `vosk-model-pt-0.3` (melhor qualidade)
- Aumentar duração do áudio (comandos muito curtos são difíceis)
- Reduzir ruído de fundo

## 📚 Referências

- [Porcupine Docs](https://picovoice.ai/docs/porcupine/)
- [Vosk Docs](https://alphacephei.com/vosk/)
- [pyttsx3 Docs](https://pyttsx3.readthedocs.io/)
- [pytest Docs](https://docs.pytest.org/)

## 🎓 Conceitos

### Como TTS substitui fala humana

1. **TTS gera áudio** → arquivo WAV real
2. **Áudio é processado** → mesmo pipeline que microfone
3. **Resultados são comparados** → passou/falhou
4. **100% automatizado** → roda em qualquer máquina

### Vantagens sobre testes com microfone

| Aspecto | Microfone Humano | TTS Automatizado |
|---------|------------------|------------------|
| Automação | ❌ Requer humano | ✅ 100% automático |
| Reprodutibilidade | ❌ Varia cada vez | ✅ Sempre igual |
| CI/CD | ❌ Impossível | ✅ Funciona |
| Velocidade | ❌ Lento | ✅ Rápido |
| Custo | ❌ Tempo humano | ✅ Gratuito |

## 📝 Licença

Este sistema de testes faz parte do projeto Wake Words Command.

---

**Happy Testing! 🎉**
