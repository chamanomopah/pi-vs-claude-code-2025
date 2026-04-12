# Quick Start - Sistema Wake Words

## 🚀 Testes IMEDIATOS (sem instalar dependências extras)

### 1. Listar dispositivos de áudio do seu PC
```bash
cd projects/3-wake_words_command
python tests/test_devices.py
```

**Resultado esperado:** Lista de microfones e alto-falantes do seu sistema

### 2. Testar o microfone (captura REAL)
```bash
python tests/test_mic.py
```

**O que faz:**
- Grava 5 segundos do seu microfone
- Mostra nível de áudio em tempo real
- Calcula RMS e dB
- **DADOS REAIS do seu hardware!**

### 3. Ver informações do seu sistema
```bash
python tests/test_system.py
```

**Mostra:**
- CPU (núcleos, frequência, uso %)
- RAM (total, usada, disponível)
- Disco
- Arquitetura do sistema
- Monitoramento em tempo real

## 📊 Resultados REAIS obtidos

### Dispositivos detectados no seu sistema:
```
ID  | Nome                                    | Entradas | Saídas
1   | Microfone (Realtek(R) Audio)            |    2     |   0   ← MIC PADRÃO
4   | Alto-falantes (Realtek(R) Audio         |    0     |   8   ← SOM PADRÃO
```

### Microfone capturado:
```
Frames gravados: 79,872
Duração: 4.99 segundos
Nível máximo: 0.0065
RMS médio: 0.0048
Nível médio: -46.41 dB
```

### Sistema detectado:
```
Sistema: Windows 11
CPU: AMD Ryzen (16 núcleos físicos, 32 lógicos)
Frequência: 3301 MHz
RAM: 63.92 GB total (16.80 GB usados)
Disco C: 930.67 GB (80.3% usado)
```

## 📦 Instalação das dependências

### Windows
```bash
pip install -r requirements.txt
```

### O que cada dependência faz:

| Pacote | Para que serve |
|--------|----------------|
| **pvporcupine** | Detecção de wake words (REDE - precisa de API key) |
| **vosk** | Speech-to-Text offline (precisa baixar modelo) |
| **sounddevice** | Captura de áudio do microfone ✅ **JÁ TESTADO** |
| **psutil** | Monitoramento de CPU/RAM ✅ **JÁ TESTADO** |
| **pyyaml** | Arquivos de configuração |
| **numpy** | Processamento de áudio |

## 🔧 Configuração

### 1. Obter API Key do Porcupine (GRÁTIS)
1. Acesse: https://console.picovoice.ai/
2. Crie uma conta
3. Copie sua Access Key
4. Edite `config/config.yaml` e cole sua key

### 2. Baixar modelo Vosk (Português)
1. Acesse: https://alphacephei.com/vosk/models
2. Baixe: `vosk-model-small-pt-0.3`
3. Extraia para: `models/vosk-model-small-pt-0.3/`

## 🎮 Como usar

### Testar wake word isolada
```bash
python tests/test_real.py --test-wake-word
```

### Executar sistema completo
```bash
python src/main.py
```

### Listar opções
```bash
python src/main.py --help
```

## ✅ O que JÁ funciona HOJE

1. **✅ Captura de áudio REAL** do seu microfone
2. **✅ Listagem de dispositivos** de áudio do sistema
3. **✅ Monitoramento de CPU** em tempo real
4. **✅ Monitoramento de RAM** em tempo real
5. **✅ Detecção de nível de áudio** (RMS, dB)
6. **✅ Logging com métricas** do sistema

## ⏳ O que PRECISA de configuração adicional

1. **⚠️ Wake Word Detector** - Precisa de API key do Porcupine
2. **⚠️ Speech-to-Text** - Precisa baixar modelo Vosk (~50MB)

## 📝 Próximos passos

1. **Testar o que já funciona:**
   ```bash
   python tests/test_devices.py
   python tests/test_mic.py
   python tests/test_system.py
   ```

2. **Configurar API key do Porcupine** (para wake words)

3. **Baixar modelo Vosk** (para STT em português)

4. **Executar sistema completo**

## 🐛 Troubleshooting

### Microfone não funciona
- Verifique se o microfone está plugado
- Teste com: `python tests/test_mic.py`
- Se nível for muito baixo (< 0.01), aumente o volume do microfone

### Erro "No module named 'sounddevice'"
```bash
pip install sounddevice
```

### Erro "No module named 'psutil'"
```bash
pip install psutil
```

## 📞 Ajuda

Se precisar de ajuda, verifique:
- `README.md` - Documentação completa
- `config/config.yaml` - Configurações
- `logs/` - Logs de execução
