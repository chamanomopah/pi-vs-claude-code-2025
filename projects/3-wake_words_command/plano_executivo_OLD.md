# Plano Executivo - Sistema de Wake Words e Comandos de Voz (Jarvis)

**Versão:** 2.0  
**Data:** 12/04/2026  
**Status:** Revisado e Aprovado para Implementação  
**Tipo:** Orquestração Mínima com Wake Words/Comandos de Voz

---

## Sumário Executivo

### Resumo do Projeto
Sistema de assistente pessoal por voz (estilo Jarvis) 100% local, sem custos de APIs, focado em produtividade e automação de tarefas repetitivas no computador. O sistema reconhece wake words e comandos de voz em tempo real com baixíssima latência, permitindo controle total do computador através de comandos naturais em português e inglês.

### Objetivos Principais
1. **Automação de Tarefas Repetitivas**: Minimizar ações manuais através de comandos de voz
2. **Produtividade Máxima**: Execução de comandos em < 500ms com configuração simplificada
3. **Simplicidade de Uso**: Interface intuitiva que permite modificar comandos sem programação
4. **100% Local e Gratuito**: Zero dependências de APIs pagas ou serviços cloud


### Valor Proposto
- **Economia de Tempo**: ~30 minutos/dia em tarefas repetitivas
- **Experiência Fluida**: Resposta em tempo real como um verdadeiro assistente pessoal
- **Configuração Flexível**: Adicionar/modificar comandos em segundos
- **Observabilidade Total**: Logs em tempo real para diagnóstico e otimização

---

## 1. Visão Geral do Sistema

### 1.1 Propósito
Sistema desktop que escuta continuamente por wake words específicas e executa comandos de voz pré-configurados, proporcionando controle total do computador através de interface de voz natural.

### 1.2 Usuários Alvo
- Profissionais que buscam maximizar produtividade
- Desenvolvedores que desejam automação personalizada
- Usuários avançados de computador
- Pessoas com limitações motoras que beneficiam de controle por voz

### 1.3 Escopo do Projeto

#### Inclui (MVP - Fase 1)
- ✅ Reconhecimento de wake words 100% local (português e inglês)
- ✅ Reconhecimento de comandos de voz simples
- ✅ Execução de ações do sistema operacional (Windows)
- ✅ Interface de configuração visual para comandos
- ✅ Sistema de logs em tempo real (toggle on/off)
- ✅ Feedback visual e sonoro de reconhecimento

#### Inclui (Fases Futuras)
- ⏳ Snap Layouts e posicionamento de janelas
- ⏳ Scripts customizáveis avançados
- ⏳ Integração com aplicações específicas
- ⏳ Reconhecimento de contexto

#### Exclui (Fora do Escopo)
- ❌ Processamento de linguagem natural complexo
- ❌ Conversas contínuas estilo ChatGPT
- ❌ Reconhecimento de emoções ou entonação
- ❌ Multi-idioma além de PT/EN

---

## 2. Requisitos Funcionais

### 2.1 Funcionalidades Principais (Priorizadas)

| ID | Funcionalidade | Descrição | Prioridade | Complexidade |
|----|---------------|-----------|------------|--------------|
| RF01 | **Wake Word Detection** | Detecção contínua de palavras-ativadora (ex: "Jarvis", "Computador") | **CRÍTICA** | Alta |
| RF02 | **Reconhecimento de Comandos** | STT local para comandos simples (PT/EN) | **CRÍTICA** | Alta |
| RF03 | **Execução de Ações do SO** | Abrir programas, atalhos, minimizar/fechar janelas | **ALTA** | Média |
| RF04 | **Interface de Configuração** | GUI para adicionar/editar comandos facilmente | **ALTA** | Média |
| RF05 | **Sistema de Logs** | Popup com logs em tempo real, ocultável | **ALTA** | Baixa |
| RF06 | **Feedback Visual** | Indicador de escuta ativa e reconhecimento | **ALTA** | Baixa |
| RF07 | **Scripts Personalizados** | Execução de scripts PowerShell/Batch via comando | **MÉDIA** | Média |
| RF08 | **Abrir Sites Específicos** | Configuração simplificada de URLs e comandos | **MÉDIA** | Baixa |
| RF09 | **Snap Layouts** | Posicionamento automático de janelas | **BAIXA** | Alta |
| RF10 | **Print Screen** | Captura de tela via comando de voz | **BAIXA** | Baixa |

### 2.2 Comandos de Exemplo (MVP)

#### Comandos do Sistema
| Comando (PT/EN) | Ação | Parâmetros |
|-----------------|------|------------|
| "Abrir [nome do programa]" / "Open [program]" | Inicia aplicativo | Caminho ou nome do app |
| "Fechar janela" / "Close window" | Fecha janela ativa | - |
| "Minimizar" / "Minimize" | Minimiza janela ativa | - |
| "Maximizar" / "Maximize" | Maximiza janela ativa | - |
| "Print" / "Screenshot" | Captura tela | - |
| "Copiar" / "Copy" | Ctrl+C | - |
| "Colar" / "Paste" | Ctrl+V | - |
| "Recortar" / "Cut" | Ctrl+X | - |

#### Comandos de Produtividade
| Comando | Ação | Parâmetros |
|---------|------|------------|
| "Abrir YouTube" | Abre youtube.com | URL configurável |
| "Pausar vídeo" | Simula Espaço | - |
| "Script [nome]" | Executa script | Caminho do script |
| "Atalho [nome]" | Executa atalho personalizado | Configurável |

### 2.3 Regras de Negócio

#### RN-001: Wake Word
- Sistema deve escutar continuamente por wake words configuradas
- Múltiplas wake words podem ser configuradas
- Sensibilidade ajustável (0-100%)
- Timeout de escuta após wake word: 5 segundos

#### RN-002: Confirmação de Execução
- Ações críticas (fechar aplicações) requerem confirmação visual
- Feedback sonoro curto beep após reconhecimento do comando
- Log de todas as ações executadas com timestamp

#### RN-003: Gerenciamento de Comandos
- Comandos podem ser adicionados/editados via GUI sem código
- Sintaxe de comando: expressão regular suportada
- Variáveis dinâmicas: `{program}`, `{url}`, `{argument}`

#### RN-004: Logs e Observabilidade
- Log level configurável: DEBUG, INFO, WARNING, ERROR
- Logs exibidos em popup flutuante (toggle)
- Logs persistidos em arquivo por 30 dias (rotação)
- Métricas: comandos reconhecidos/tentados, latência média

---

## 3. Requisitos Não-Funcionais

### 3.1 Performance

| Métrica | Target | Observação |
|---------|--------|------------|
| **Latência Wake Word** | < 300ms | Tempo da fala ao reconhecimento |
| **Latência Comando** | < 500ms | Do comando à execução da ação |
| **CPU Idle** | < 2% | Quando não está processando áudio |
| **CPU Ativo** | < 15% | Durante reconhecimento de comando |
| **RAM** | < 200MB | Uso de memória total |
| **Startup Time** | < 3 segundos | Do clique à escuta ativa |

### 3.2 Usabilidade

| Aspecto | Requisito |
|---------|-----------|
| **Curva de Aprendizado** | < 10 minutos para configurar primeiros comandos |
| **Configuração** | Adicionar comando simples em < 30 segundos |
| **Feedback Visual** | Indicador claro de estado (escutando/processing/error) |
| **Acessibilidade** | Interface com atalhos de teclado |

### 3.3 Confiabilidade

| Métrica | Target | Observação |
|---------|--------|------------|
| **Uptime** | 99% (pode reiniciar sem aviso) | Aplicação desktop |
| **Crash Recovery** | Automático | Reinicia em caso de crash |
| **False Positive Rate** | < 5% | Wake words não intencionais |
| **False Negative Rate** | < 10% | Comandos não reconhecidos |

### 3.4 Segurança e Privacidade

| Aspecto | Requisito |
|---------|-----------|
| **100% Local** | Nenhum dado é enviado para APIs externas |
| **Permissões** | Apenas acesso necessário ao SO |
| **Logs** | Armazenados localmente, sem informações sensíveis |
| **Scripts** | Sandbox para scripts customizados (opcional) |
| **Microfone** | Indicador visível quando ativo |

### 3.5 Compatibilidade

| Aspecto | Requisito |
|---------|-----------|
| **Sistema Operacional** | Windows 10/11 (prioridade), macOS/Linux (futuro) |
| **Arquitetura** | x64, ARM64 (experimental) |
| **Idiomas** | Português (BR), Inglês (US) |
| **Microfone** | Qualquer dispositivo compatível com o SO |

---

## 4. Arquitetura Técnica

### 4.1 Padrão Arquitetural

**Padrão Escolhido: Monólito Modular com Plugin System**

**Justificativa:**
- Aplicação desktop com domínio bem delimitado
- Time pequeno (ou individual) = complexidade deve ser mínima
- Plugin system permite extensibilidade sem overhead de microserviços
- Deploy é single binary = simplicidade máxima para usuário

**Trade-offs Considerados:**

| Opção | Vantagens | Desvantagens | Decisão |
|-------|-----------|--------------|---------|
| **Monólito Modular** | Simples, rápido, fácil deploy | Escala limitada (não é problema) | ✅ ESCOLHIDA |
| Microservices | Escala, independência | Complexidade operacional alta | ❌ Overkill |
| Serverless | Zero infra, pay-per-use | Cold starts, vendor lock-in | ❌ Não aplicável local |
| Event-Driven | Loose coupling, async | Complexidade debugging | ❌ Desnecessário |

### 4.2 Stack Tecnológico

#### Camada de Aplicação Principal

| Camada | Tecnologia | Versão | Justificativa |
|--------|-----------|--------|---------------|
| **Linguagem** | Python | 3.11+ | Ecossistema rico em ML/Audio, rápida prototipagem |
| **Framework GUI** | PyQt6 / PySide6 | 6.6+ | GUI nativa, multi-plataforma, widgets ricos |
| **Gerenciador de Pacotes** | Poetry | 1.7+ | Dependency locking, ambientes virtuais |

#### Camada de Reconhecimento de Voz

| Componente | Tecnologia | Justificativa |
|------------|-----------|---------------|
| **Wake Word Detection** | **Picovoice Porcupine** | 100% local, wake words customizáveis, ultra-baixa latência, free tier generoso (100 wake words), suporte PT/EN |
| **Speech-to-Text** | **OpenAI Whisper (local)** | SOTA accuracy, modelo tiny/base para速度, 100% local, suporta PT/EN nativamente |
| **Fallback STT** | Vosk | Alternativa lighter se Whisper for pesado |

| Alternativas Consideradas | Por que rejeitadas? |
|--------------------------|---------------------|
| Google Speech API | Não é local, custa \$, depende de internet |
| Azure Speech | Não é local, custa \$ |
| Mozilla Coqui Ainda | Projeto descontinuado |
| PicoVoice Leopard | Custa \$, overkill para comandos simples |

#### Camada de Integração com SO

| Componente | Tecnologia | Justificativa |
|------------|-----------|---------------|
| **Automação Windows** | PyAutoGUI | Simples, cross-platform, suporta teclado/mouse |
| **Gerenciamento Janelas** | pygetwindow | API simples para manipular janelas |
| **Atalhos/Scripts** | subprocess (built-in) | Executa PowerShell/Batch nativamente |
| **Snap Layouts** | pywinauto | Controle fino de janelas no Windows |

#### Camada de Configuração e Persistência

| Componente | Tecnologia | Justificativa |
|------------|-----------|---------------|
| **Formato Config** | YAML | Legível por humanos, fácil editar manualmente |
| **Validação** | Pydantic | Validação de esquema, type-safe |
| **Banco de Dados** | SQLite | Persistência de logs/métricas (opcional) |
| **Watchdog** | watchdog | Hot-reload de configuração |

#### Camada de Logs e Observabilidade

| Componente | Tecnologia | Justificativa |
|------------|-----------|---------------|
| **Logging** | loguru (Python) | Structured logging, rotação automática |
| **GUI Logs** | QPlainTextEdit (PyQt) | Widget nativo, performance suficiente |
| **Métricas** | Prometheus Client (opcional) | Para métricas avançadas |

### 4.3 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     USUÁRIO (Voice Input)                   │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  GUI LAYER (PyQt6)                          │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐    │
│  │ Config Window│  │  Logs Popup   │  │Status Tray  │    │
│  └──────────────┘  └───────────────┘  └──────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                ORCHESTRATION LAYER                          │
│  ┌──────────────────────────────────────────────────┐     │
│  │          Command Orchestrator                    │     │
│  │  - Wake word detection coordination             │     │
│  │  - Command parsing & routing                    │     │
│  │  - Action execution coordination                │     │
│  └──────────────────────────────────────────────────┘     │
└────────────┬──────────────┬──────────────┬─────────────────┘
             ↓              ↓              ↓
┌─────────────────────────────────────────────────────────────┐
│              RECOGNITION LAYER (Plugins)                    │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │ Wake Word Engine │        │ Speech-to-Text Engine   │  │
│  │ (Porcupine)      │        │ (Whisper)               │  │
│  │ - Continuous     │        │ - On-demand             │  │
│  │   listening      │        │ - Multi-language        │  │
│  └──────────────────┘        └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│               ACTION EXECUTION LAYER                        │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ │
│  │Window Mgr │ │Launcher   │ │Script     │ │Clipboard  │ │
│  │Plugin     │ │Plugin     │ │Plugin     │ │Plugin     │ │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              OPERATING SYSTEM (Windows)                     │
│          Window Manager · Process Manager · Clipboard       │
└─────────────────────────────────────────────────────────────┘

                           ↓ (persistence)
┌─────────────────────────────────────────────────────────────┐
│               STORAGE & CONFIGURATION                       │
│  ┌───────────┐         ┌───────────────────────────────┐  │
│  │Config.yml │         │ logs/ (rotating files)        │  │
│  │Commands   │         │ metrics.db (SQLite)           │  │
│  └───────────┘         └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Estrutura de Diretórios

```
jarvis-voice-assistant/
├── src/
│   ├── __init__.py
│   ├── main.py                      # Entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py              # Pydantic models
│   │   └── default_config.yml       # Config default
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py           # GUI principal
│   │   ├── config_dialog.py         # Dialog de configuração
│   │   ├── log_viewer.py            # Popup de logs
│   │   └── tray_icon.py             # System tray
│   ├── core/
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # Orquestrador principal
│   │   ├── command_parser.py        # Parser de comandos
│   │   └── state_manager.py         # Gerenciamento de estado
│   ├── recognition/
│   │   ├── __init__.py
│   │   ├── base.py                  # Interface base
│   │   ├── wake_word.py             # Porcupine wrapper
│   │   ├── speech_to_text.py        # Whisper wrapper
│   │   └── models.py                # Modelos de dados
│   ├── actions/
│   │   ├── __init__.py
│   │   ├── base.py                  # Interface base
│   │   ├── window_manager.py        # Ações de janela
│   │   ├── launcher.py              # Abrir programas
│   │   ├── scripts.py               # Executar scripts
│   │   ├── clipboard.py             # Ações clipboard
│   │   └── registry.py              # Registro de actions
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                # Loguru wrapper
│       ├── audio.py                 # Audio utilities
│       └── hotkeys.py               # Atalhos globais
├── tests/
│   ├── test_recognition.py
│   ├── test_actions.py
│   └── test_config.py
├── models/                          # Modelos Whisper
│   └── tiny.pt                      # ~40MB
├── config.yml                       # Config usuário (gitignored)
├── pyproject.toml                   # Poetry config
├── README.md
└── requirements.txt
```

### 4.5 Modelo de Dados

#### Configuração (config.yml)

```yaml
# config.yml
general:
  language: pt-BR  # pt-BR | en-US
  log_level: INFO  # DEBUG | INFO | WARNING | ERROR
  startup_minimized: false

audio:
  device_index: null  # null = default
  sample_rate: 16000
  sensitivity: 0.5  # 0.0 - 1.0 (wake word sensitivity)

wake_words:
  - jarvis
  - computer
  - hey assistant

speech_to_text:
  model: tiny  # tiny | base | small | medium
  language: pt  # Auto-detected from general.language

actions:
  window_management:
    enabled: true
    snap_layouts:
      enabled: false  # Future feature
  
  launcher:
    enabled: true
    apps:
      notepad: "C:\\Windows\\System32\\notepad.exe"
      chrome: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
      vscode: "C:\\Users\\JOSE\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
  
  scripts:
    enabled: true
    directory: "./scripts"

logging:
  file_enabled: true
  file_path: "./logs/jarvis.log"
  rotation: "10 MB"
  retention: "30 days"
  popup_enabled: true
  popup_max_lines: 100
```

#### Comandos (commands.yml)

```yaml
# commands.yml
version: "1.0"

commands:
  - id: cmd_open_program
    name: "Abrir Programa"
    patterns:
      - pt: "abrir (?P<program>.+)"
      - en: "open (?P<program>.+)"
    action:
      type: launcher
      params:
        program: "{program}"

  - id: cmd_close_window
    name: "Fechar Janela"
    patterns:
      - pt: "fechar janela"
      - en: "close window"
    action:
      type: window_close
      confirmation: true

  - id: cmd_minimize
    name: "Minimizar"
    patterns:
      - pt: "minimizar"
      - en: "minimize"
    action:
      type: window_minimize

  - id: cmd_open_youtube
    name: "Abrir YouTube"
    patterns:
      - pt: "abrir youtube"
      - en: "open youtube"
    action:
      type: launcher
      params:
        url: "https://youtube.com"

  - id: cmd_screenshot
    name: "Print Screen"
    patterns:
      - pt: "print|tirar print|screenshot"
      - en: "screenshot|take screenshot"
    action:
      type: screenshot
      params:
        save_to: "%USERPROFILE%\\Pictures\\Screenshots"

  - id: cmd_paste
    name: "Colar"
    patterns:
      - pt: "colar"
      - en: "paste"
    action:
      type: clipboard_paste

  - id: cmd_script
    name: "Executar Script"
    patterns:
      - pt: "script (?P<script_name>.+)"
      - en: "script (?P<script_name>.+)"
    action:
      type: script
      params:
        script: "{script_name}.ps1"
```

---

## 5. Plano de Implementação (Fases)

### 5.1 Visão Geral das Fases

| Fase | Nome | Duração Est. | Entregas | Dependências |
|------|------|--------------|----------|--------------|
| **Fase 0** | Setup & Pesquisa | 1 dia | Ambiente, testes de viabilidade | - |
| **Fase 1** | Wake Word MVP | 2-3 dias | Detecção de wake word funcional | Fase 0 |
| **Fase 2** | Speech-to-Text | 2-3 dias | STT local funcionando | Fase 0 |
| **Fase 3** | Actions Core | 2-3 dias | Launcher, Window Manager | Fase 1 |
| **Fase 4** | Orquestração | 2 dias | Integração Wake+STT+Actions | Fase 1,2,3 |
| **Fase 5** | GUI Básica | 3 dias | Config, Logs, Tray Icon | Fase 4 |
| **Fase 6** | Refinamento | 2-3 dias | Polimento, bugs, testes | Fase 5 |
| **Fase 7** | Features Extras | Futuro | Snap Layouts, scripts avançados | Fase 6 |

**Total Estimado MVP:** 15-20 dias (desenvolvimento individual focado)

### 5.2 Fase 0: Setup & Pesquisa (1 dia)

**Objetivo:** Validar viabilidade técnica e configurar ambiente de desenvolvimento.

**Atividades:**
1. Configurar ambiente Python 3.11+ com Poetry
2. Testar Picovoice Porcupine (criar conta free, obter API key)
3. Testar OpenAI Whisper local (instalar modelo tiny)
4. Testar PyAutoGUI para ações no Windows
5. Criar estrutura de diretórios
6. Configurar Git repository

**Entregáveis:**
- ✅ Ambiente de desenvolvimento funcional
- ✅ Prova de conceito: Porcupine detectando wake word
- ✅ Prova de conceito: Whisper transcrevendo áudio
- ✅ Prova de conceito: PyAutoGUI executando ação
- ✅ Estrutura de projeto criada

**Critérios de Sucesso:**
- Todos os PoCs funcionam end-to-end
- Latência wake word < 300ms
- Latência STT < 1s

**Riscos:**
- ⚠️ Porcupine pode não ter wake words em PT → **Mitigação:** Testar custom wake words
- ⚠️ Whisper tiny pode ser impreciso → **Mitigação:** Testar modelo base se necessário

---

### 5.3 Fase 1: Wake Word Detection (2-3 dias)

**Objetivo:** Implementar detecção contínua de wake words com baixíssima latência.

**Atividades:**

#### Dia 1: Integração Porcupine
1. Instalar pvporcupine package
2. Criar wrapper Python para Porcupine
3. Implementar stream de áudio contínuo
4. Adicionar múltiplas wake words configuráveis

**Código Esqueleto:**
```python
# src/recognition/wake_word.py
import pvporcupine
from src.utils.audio import AudioStream

class WakeWordDetector:
    def __init__(self, keywords: List[str], sensitivity: float = 0.5):
        self.porcupine = pvporcupine.create(
            access_key="YOUR_KEY",
            keywords=keywords,  # Built-in or custom
            sensitivities=[sensitivity] * len(keywords)
        )
        self.audio_stream = AudioStream(rate=self.porcupine.sample_rate)
    
    def listen_continuously(self, callback: Callable[[int], None]):
        """Callback recebe keyword_index quando detectado"""
        while True:
            pcm = self.audio_stream.read_frames()
            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                callback(keyword_index)
```

#### Dia 2: Thread e Gerenciamento de Estado
1. Executar detecção em thread separada
2. Implementar flag de stop/start
3. Gerenciar recursos (fechar stream ao parar)
4. Adicionar tratamento de erros (microfone desconectado, etc.)

#### Dia 3: Testes e Refinamento
1. Testar sensibilidade de wake words
2. Medir latência real
3. Testar diferentes ambientes (ruído)
4. Adicionar logs estruturados

**Entregáveis:**
- ✅ WakeWordDetector class funcional
- ✅ Testes unitários
- ✅ Latência < 300ms medida
- ✅ Documentação de uso

**Critérios de Sucesso:**
- Detecta wake word em 95%+ das tentativas em ambiente silencioso
- False positive rate < 5%
- Uso CPU < 2% idle

---

### 5.4 Fase 2: Speech-to-Text (2-3 dias)

**Objetivo:** Implementar transcrição de áudio para texto com Whisper local.

**Atividades:**

#### Dia 1: Integração Whisper
1. Instalar openai-whisper
2. Baixar modelo tiny (ou base)
3. Criar wrapper para Whisper
4. Implementar gravação de buffer de áudio

**Código Esqueleto:**
```python
# src/recognition/speech_to_text.py
import whisper
import numpy as np
from src.utils.audio import AudioRecorder

class SpeechToTextEngine:
    def __init__(self, model_size: str = "tiny", language: str = "pt"):
        self.model = whisper.load_model(model_size)
        self.language = language
        self.recorder = AudioRecorder(sample_rate=16000)
    
    def listen_for_command(self, duration: float = 5.0) -> str:
        """Grava por `duration` segundos e transcreve"""
        audio = self.recorder.record(duration=duration)
        audio_tensor = torch.from_numpy(audio).float()
        
        result = self.model.transcribe(
            audio_tensor,
            language=self.language,
            fp16=False  # CPU
        )
        
        return result["text"].strip()
```

#### Dia 2: Detecção de Silêncio e Timeout
1. Implementar VAD (Voice Activity Detection) simples
2. Parar gravação ao detectar silêncio
3. Adicionar timeout máximo (5s)
4. Tratamento de erros (sem fala detectada)

#### Dia 3: Otimização e Testes
1. Testar acurácia em PT e EN
2. Medir latência
3. Otimizar uso de CPU (threading)
4. Testar com ruído ambiente

**Entregáveis:**
- ✅ SpeechToTextEngine class funcional
- ✅ VAD implementado
- ✅ Testes de acurácia (baseline)
- ✅ Latência < 1s para comandos curtos

**Critérios de Sucesso:**
- Transcreve comandos simples com 90%+ acurácia
- Latência média < 800ms
- Uso CPU < 15% durante transcrição

---

### 5.5 Fase 3: Actions Core (2-3 dias)

**Objetivo:** Implementar sistema de ações para comandos do sistema.

**Atividades:**

#### Dia 1: Interface Base e Registro
1. Definir interface abstrata para Actions
2. Implementar registro de actions
3. Criar sistema de plugins

**Código Esqueleto:**
```python
# src/actions/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class Action(ABC):
    @classmethod
    @abstractmethod
    def schema(cls) -> Dict[str, Any]:
        """Define schema de parâmetros"""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> bool:
        """Executa a ação. Retorna True se sucesso"""
        pass

# src/actions/registry.py
class ActionRegistry:
    _actions: Dict[str, type[Action]] = {}
    
    @classmethod
    def register(cls, action_type: str, action_class: type[Action]):
        cls._actions[action_type] = action_class
    
    @classmethod
    def get(cls, action_type: str) -> type[Action]:
        return cls._actions[action_type]
```

#### Dia 2: Implementar Actions Principais
1. **LauncherAction:** Abrir programas/URLs
2. **WindowCloseAction:** Fechar janela ativa
3. **WindowMinimizeAction:** Minimizar janela
4. **WindowMaximizeAction:** Maximizar janela
5. **ScreenshotAction:** Capturar tela
6. **ClipboardAction:** Copiar/colar/recortar

```python
# src/actions/launcher.py
import subprocess
from src.actions.base import Action

class LauncherAction(Action):
    @classmethod
    def schema(cls) -> Dict:
        return {
            "type": "object",
            "properties": {
                "program": {"type": "string"},
                "url": {"type": "string"}
            }
        }
    
    def execute(self, program: str = None, url: str = None) -> bool:
        try:
            if url:
                subprocess.Popen(["start", url], shell=True)
            elif program:
                subprocess.Popen([program], shell=True)
            return True
        except Exception as e:
            logger.error(f"Failed to launch: {e}")
            return False
```

#### Dia 3: Testes de Actions
1. Testar cada action isoladamente
2. Testar edge cases (programa não existe, etc.)
3. Medir latência de execução
4. Adicionar logs

**Entregáveis:**
- ✅ Sistema de actions implementado
- ✅ 6+ actions funcionais
- ✅ Testes unitários
- ✅ Documentação de cada action

**Critérios de Sucesso:**
- Todas as actions executam em < 200ms
- Tratamento de erros robusto
- Fácil adicionar novas actions

---

### 5.6 Fase 4: Orquestração (2 dias)

**Objetivo:** Integrar Wake Word + STT + Actions em fluxo unificado.

**Atividades:**

#### Dia 1: Command Orchestrator
1. Criar orquestrador que coordena fluxo completo
2. Implementar parser de comandos (regex)
3. Mapear comandos para actions
4. Adicionar sistema de confirmação

**Código Esqueleto:**
```python
# src/core/orchestrator.py
from src.recognition.wake_word import WakeWordDetector
from src.recognition.speech_to_text import SpeechToTextEngine
from src.actions.registry import ActionRegistry
from src.core.command_parser import CommandParser

class CommandOrchestrator:
    def __init__(self, config: Config):
        self.wake_detector = WakeWordDetector(config.wake_words)
        self.stt_engine = SpeechToTextEngine(config.language)
        self.command_parser = CommandParser(config.commands_file)
        self.state = "IDLE"  # IDLE | LISTENING | PROCESSING
    
    def start(self):
        self.wake_detector.listen_continuously(self.on_wake_word_detected)
    
    def on_wake_word_detected(self, keyword_index: int):
        self.state = "LISTENING"
        self.play_beep()  # Feedback sonoro
        
        # Ouvir comando
        command_text = self.stt_engine.listen_for_command()
        
        if not command_text:
            self.state = "IDLE"
            return
        
        self.state = "PROCESSING"
        
        # Parser e execução
        parsed = self.command_parser.parse(command_text)
        if parsed:
            self.execute_command(parsed)
        
        self.state = "IDLE"
    
    def execute_command(self, command: ParsedCommand):
        action_class = ActionRegistry.get(command.action_type)
        action = action_class()
        success = action.execute(**command.params)
        
        if success:
            self.play_confirmation_sound()
        else:
            self.play_error_sound()
```

#### Dia 2: Parser de Comandos
1. Implementar parser baseado em regex
2. Carregar comandos do YAML
3. Extrair parâmetros
4. Adicionar sistema de aliases

**Entregáveis:**
- ✅ Orquestrador funcional
- ✅ Parser de comandos
- ✅ Fluxo completo funcionando
- ✅ Logs de execução

**Critérios de Sucesso:**
- Fluxo completo wake → stt → action em < 2s
- 90%+ dos comandos de teste executados corretamente

---

### 5.7 Fase 5: GUI (3 dias)

**Objetivo:** Criar interface gráfica para configuração e monitoramento.

**Atividades:**

#### Dia 1: Janela Principal e Tray Icon
1. Criar