# Wake Words Command System

Sistema REAL de detecção de wake words e reconhecimento de comandos de voz.

## 📋 Estrutura do Projeto

```
3-wake_words_command/
├── src/                    # Código fonte
│   ├── audio_capture.py   # Captura REAL do microfone
│   ├── logger.py          # Logging REAL com métricas do sistema
│   ├── wake_word.py       # Detecção REAL de wake words
│   ├── stt_engine.py      # Speech-to-Text REAL
│   ├── command_processor.py # Processador de comandos
│   └── main.py            # Aplicação principal
├── tests/                  # Testes REAIS
│   └── test_real.py       # Testes de hardware
├── models/                 # Modelos Vosk (vazio inicialmente)
├── config/                 # Arquivos de configuração
│   └── config.yaml        # Configurações do sistema
├── logs/                   # Logs da aplicação
└── requirements.txt        # Dependências Python
```

## 🚀 Instalação

### Windows

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Baixar modelo Vosk (português)
# Visite: https://alphacephei.com/vosk/models
# Baixe: vosk-model-small-pt-0.3
# Extraia para: models/vosk-model-small-pt-0.3
```

### Obter API Key do Porcupine

1. Acesse: https://console.picovoice.ai/
2. Crie uma conta gratuita
3. Copie sua Access Key
4. Configure em `config/config.yaml`

## 🎤 Testes REAIS de Hardware

```bash
# Listar dispositivos de áudio do sistema
python tests/test_real.py --list-devices

# Testar captura do microfone
python tests/test_real.py --test-mic

# Monitorar recursos do sistema
python tests/test_real.py --monitor-system

# Executar todos os testes
python tests/test_real.py --all
```

## 🎯 Uso

```bash
# Iniciar o sistema
python src/main.py

# Fale "Porcupine" ou "OK Google" para ativar
# Depois fale seu comando
```

## 🔧 Configuração

Edite `config/config.yaml` para ajustar:

- **wake_word**: Palavra de ativação (porcupine, ok-google, etc.)
- **sensitivity**: Sensibilidade da detecção (0.0 a 1.0)
- **audio_device**: Dispositivo de áudio (default = None)
- **model_path**: Caminho do modelo Vosk

## 📊 Métricas Monitoradas

- **CPU**: Uso percentual do processador
- **RAM**: Memória utilizada (MB/GB)
- **Audio Level**: Nível do áudio capturado (dB)
- **Latency**: Latência da detecção (ms)

## 🛠️ Troubleshooting

### Microfone não detectado
```bash
python tests/test_real.py --list-devices
# Escolha um ID e configure em config.yaml
```

### Erro no Porcupine
- Verifique sua Access Key em `config/config.yaml`
- Acesse: https://console.picovoice.ai/

### Modelo Vosk não encontrado
- Baixe: https://alphacephei.com/vosk/models
- Extraia para: `models/vosk-model-small-pt-0.3`

## 📝 Dependências

- **pvporcupine**: Detecção de wake words (Picovoice)
- **vosk**: Speech-to-Text offline
- **sounddevice**: Captura de áudio em tempo real
- **psutil**: Monitoramento do sistema
- **pyyaml**: Arquivos de configuração

## 📄 Licença

MIT License
