# 📚 Índice - Testes Automatizados de Áudio

Documentação completa do sistema de testes automatizados para wake words e comandos de voz.

## 🚀 Comece Aqui

**Novo no projeto?** Leia nesta ordem:

1. **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** - Resumo executivo da solução
2. **[tests/README_AUTOMATED.md](tests/README_AUTOMATED.md)** - Como usar o sistema
3. **[specs/automated-audio-testing-architecture.md](specs/automated-audio-testing-architecture.md)** - Arquitetura técnica

## 📖 Documentação

### Especificações Técnicas

| Arquivo | Descrição |
|---------|-----------|
| [specs/automated-audio-testing-architecture.md](specs/automated-audio-testing-architecture.md) | **ARQUITETURA COMPLETA** - Visão geral, componentes, tecnologias, diagramas |
| [specs/automated-audio-testing-validation.md](specs/automated-audio-testing-validation.md) | **VALIDAÇÃO** - Verificação de tecnologias, compatibilidades, evidências |

### Guias de Uso

| Arquivo | Descrição |
|---------|-----------|
| [tests/README_AUTOMATED.md](tests/README_AUTOMATED.md) | **GUIA DO USUÁRIO** - Como instalar, configurar e rodar testes |
| [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) | **RESUMO EXECUTIVO** - O que foi feito, como funciona, próximos passos |

### Código

#### Entry Point
- **[tests/test_automated.py](tests/test_automated.py)** - Script principal, CLI para rodar testes

#### Geração de Áudio (`tests/src/audio_generation/`)
- **[tts_engine.py](tests/src/audio_generation/tts_engine.py)** - TTS (pyttsx3, edge-tts)
- **[audio_generator.py](tests/src/audio_generation/audio_generator.py)** - Gerador de wake words, comandos, cenários
- **[noise_injector.py](tests/src/audio_generation/noise_injector.py)** - Injeção de ruído realista

#### Framework de Teste (`tests/src/test_framework/`)
- **[audio_test_runner.py](tests/src/test_framework/audio_test_runner.py)** - Executor de testes
- **[assertions.py](tests/src/test_framework/assertions.py)** - Asserções customizadas
- **[metrics.py](tests/src/test_framework/metrics.py)** - Métricas (WER, CER)

#### Testes Pytest (`tests/automated/`)
- **[test_wake_word_auto.py](tests/automated/test_wake_word_auto.py)** - Testes de wake word
- **[test_stt_auto.py](tests/automated/test_stt_auto.py)** - Testes de STT
- **[test_integration_auto.py](tests/automated/test_integration_auto.py)** - Testes de integração
- **[conftest.py](tests/automated/conftest.py)** - Configuração pytest

## 🎯 Quick Reference

### Instalação

```bash
pip install -r requirements-test-automated.txt
```

### Configuração

```bash
set PORCUPINE_ACCESS_KEY=sua_chave
set VOSK_MODEL_PATH=models/vosk-model-small-pt-0.3
```

### Uso

```bash
# Gerar áudio
python tests/test_automated.py --generate-audio

# Rodar testes
python tests/test_automated.py

# Teste rápido
python tests/test_automated.py --quick

# Testes específicos
python tests/test_automated.py --wake-word
python tests/test_automated.py --stt
python tests/test_automated.py --integration
```

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST AUTOMATION FRAMEWORK                    │
├─────────────────────────────────────────────────────────────────┤
│  Text → TTS → WAV → Porcupine/Vosk → Resultados → Asserts      │
└─────────────────────────────────────────────────────────────────┘
```

**Componentes:**
1. **TTS Engine**: Gera áudio de texto (pyttsx3/edge-tts)
2. **Audio Generator**: Cria wake words, comandos, cenários
3. **Noise Injector**: Adiciona ruído para testar robustez
4. **Test Runner**: Processa áudio e coleta métricas
5. **Assertions**: Valida resultados (WER, detecções)
6. **Pytest**: Orquestra tudo e gera reports

## 📊 Métricas

### WER (Word Error Rate)
```
WER = (Substituições + Deleções + Inserções) / Total de Palavras

0.0  = Perfeito
0.5  = 50% de erro (aceitável)
1.0  = 100% de erro (falha)
```

### SNR (Signal-to-Noise Ratio)
```
SNR em dB (quanto maior, melhor)

> 20 dB  = Áudio limpo
10-20 dB = Ruído moderado
< 10 dB  = Muito ruído
```

## 🔧 Troubleshooting

### Pyttsx3 não funciona
- Verificar vozes instaladas no Windows
- Tentar taxa diferente: `Pyttsx3TTS(rate=120)`

### Porcupine não detecta
- Aumentar sensibilidade: `sensitivity=0.4`
- Tentar voz mais lenta do TTS
- Usar edge-tts (mais natural)

### Vosk transcreve mal
- Usar modelo maior: `vosk-model-pt-0.3`
- Aumentar duração do comando
- Relaxar threshold: `max_wer=0.7`

## 📚 Referências Externas

- [Porcupine](https://picovoice.ai/docs/porcupine/) - Wake word detection
- [Vosk](https://alphacephei.com/vosk/) - Speech-to-text
- [pyttsx3](https://pyttsx3.readthedocs.io/) - TTS offline
- [pytest](https://docs.pytest.org/) - Test framework

## 🎓 Conceitos

### Como TTS substitui fala humana

1. **TTS gera arquivo WAV** → Áudio real, não mock
2. **Porcupine processa WAV** → Mesmo algoritmo de produção
3. **Vosk transcreve WAV** → Mesmo algoritmo de produção
4. **Resultados são validados** → WER, detecções, timing
5. **100% automatizado** → Sem humano, sem microfone

### Vantagens

| Microfone Humano | TTS Automatizado |
|------------------|------------------|
| ❌ Requer humano | ✅ 100% automático |
| ❌ Não reprodutível | ✅ Sempre igual |
| ❌ Impossível em CI/CD | ✅ CI/CD friendly |
| ❌ Lento | ✅ Rápido |

## 📝 Estrutura de Projetos

```
projects/3-wake_words_command/
│
├── SOLUTION_SUMMARY.md              # Comece aqui!
├── INDEX_AUTOMATED_TESTING.md       # Este arquivo
│
├── specs/                           # Especificações
│   ├── automated-audio-testing-architecture.md
│   └── automated-audio-testing-validation.md
│
├── tests/                           # Testes
│   ├── README_AUTOMATED.md          # Guia de uso
│   ├── test_automated.py            # Entry point
│   ├── conftest.py                  # Pytest config
│   │
│   ├── automated/                   # Testes pytest
│   │   ├── test_wake_word_auto.py
│   │   ├── test_stt_auto.py
│   │   └── test_integration_auto.py
│   │
│   ├── src/                         # Código de suporte
│   │   ├── audio_generation/        # Geração de áudio
│   │   │   ├── tts_engine.py
│   │   │   ├── audio_generator.py
│   │   │   └── noise_injector.py
│   │   │
│   │   └── test_framework/          # Framework
│   │       ├── audio_test_runner.py
│   │       ├── assertions.py
│   │       └── metrics.py
│   │
│   └── audio_library/               # Áudios gerados
│       ├── wake_words/
│       ├── commands/
│       └── generated/
│
└── requirements-test-automated.txt  # Dependências
```

## 🚀 Próximos Passos

1. **Ler**: `SOLUTION_SUMMARY.md`
2. **Instalar**: `pip install -r requirements-test-automated.txt`
3. **Configurar**: Set environment variables
4. **Gerar áudio**: `python tests/test_automated.py --generate-audio`
5. **Rodar**: `python tests/test_automated.py`

---

**Happy Testing! 🎉**
