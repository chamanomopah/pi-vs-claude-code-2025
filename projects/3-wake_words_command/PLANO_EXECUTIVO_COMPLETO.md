# Plano Executivo - Sistema de Wake Words e Comandos de Voz (Jarvis)

**Versão:** 3.0 - Completo e Revisado  
**Data:** 12/04/2026  
**Status:** Aprovado para Implementação  
**Tipo:** Orquestração Mínima com Wake Words/Comandos de Voz

---

## Índice

1. [Sumário Executivo](#1-sumário-executivo)
2. [Visão Geral do Sistema](#2-visão-geral-do-sistema)
3. [Requisitos Funcionais](#3-requisitos-funcionais)
4. [Requisitos Não-Funcionais](#4-requisitos-não-funcionais)
5. [Arquitetura Técnica](#5-arquitetura-técnica)
6. [Plano de Implementação](#6-plano-de-implementação)
7. [Riscos e Mitigações](#7-riscos-e-mitigações)
8. [Cronograma e Milestones](#8-cronograma-e-milestones)
9. [Critérios de Aceite](#9-critérios-de-aceite)
10. [Recursos Necessários](#10-recursos-necessários)
11. [Referências](#11-referências)

---

## 1. Sumário Executivo

### 1.1 Resumo do Projeto

Sistema de assistente pessoal por voz (estilo Jarvis) **100% local**, sem custos de APIs, focado em produtividade e automação de tarefas repetitivas no computador. O sistema reconhece wake words e comandos de voz em tempo real com baixíssima latência, permitindo controle total do computador através de comandos naturais em português e inglês.

### 1.2 Objetivos Principais

1. **Automação de Tarefas Repetitivas**: Minimizar ações manuais através de comandos de voz
2. **Produtividade Máxima**: Execução de comandos em < 500ms com configuração simplificada
3. **Simplicidade de Uso**: Interface intuitiva que permite modificar comandos sem programação
4. **100% Local e Gratuito**: Zero dependências de APIs pagas ou serviços cloud

### 1.3 Valor Proposto

| Benefício | Descrição | Impacto |
|-----------|-----------|---------|
| **Economia de Tempo** | ~30 minutos/dia em tarefas repetitivas | Alta |
| **Experiência Fluida** | Resposta em tempo real como um verdadeiro assistente pessoal | Alta |
| **Configuração Flexível** | Adicionar/modificar comandos em segundos | Média |
| **Observabilidade Total** | Logs em tempo real para diagnóstico e otimização | Média |
| **Privacidade Total** | 100% local, nenhum dado enviado para a internet | Alta |

### 1.4 Contexto

- **Projeto de Orquestração Mínima**: Foco em simplicidade e velocidade
- **Desenvolvimento Individual**: Arquitetura deve ser simples o suficiente para uma pessoa manter
- **Prioridade**: Funcionalidade > Elegância

---

## 2. Visão Geral do Sistema

### 2.1 Propósito

Sistema desktop que escuta continuamente por wake words específicas e executa comandos de voz pré-configurados, proporcionando controle total do computador através de interface de voz natural.

### 2.2 Usuários Alvo

- ✅ Profissionais que buscam maximizar produtividade
- ✅ Desenvolvedores que desejam automação personalizada
- ✅ Usuários avançados de computador
- ✅ Pessoas com limitações motoras que beneficiam de controle por voz

### 2.3 Escopo do Projeto

#### MVP - Inclui
- ✅ Reconhecimento de wake words 100% local (português e inglês)
- ✅ Reconhecimento de comandos de voz simples
- ✅ Execução de ações do sistema operacional (Windows)
- ✅ Interface de configuração visual para comandos
- ✅ Sistema de logs em tempo real (toggle on/off)
- ✅ Feedback visual e sonoro de reconhecimento

#### Fases Futuras
- ⏳ Snap Layouts e posicionamento de janelas
- ⏳ Scripts customizáveis avançados
- ⏳ Integração com aplicações específicas
- ⏳ Reconhecimento de contexto

#### Fora do Escopo
- ❌ Processamento de linguagem natural complexo
- ❌ Conversas contínuas estilo ChatGPT
- ❌ Reconhecimento de emoções ou entonação
- ❌ Multi-idioma além de PT/EN

---

## 3. Requisitos Funcionais

### 3.1 Funcionalidades Principais (Priorizadas)

| ID | Funcionalidade | Descrição | Prioridade | Complexidade | Dependências |
|----|---------------|-----------|------------|--------------|--------------|
| RF01 | **Wake Word Detection** | Detecção contínua de palavras-ativadora (ex: "Jarvis", "Computador") | **CRÍTICA** | Alta | - |
| RF02 | **Reconhecimento de Comandos** | STT local para comandos simples (PT/EN) | **CRÍTICA** | Alta | RF01 |
| RF03 | **Execução de Ações do SO** | Abrir programas, atalhos, minimizar/fechar janelas | **ALTA** | Média | RF02 |
| RF04 | **Interface de Configuração** | GUI para adicionar/editar comandos facilmente | **ALTA** | Média | RF03 |
| RF05 | **Sistema de Logs** | Popup com logs em tempo real, ocultável | **ALTA** | Baixa | RF04 |
| RF06 | **Feedback Visual** | Indicador de escuta ativa e reconhecimento | **ALTA** | Baixa | RF01 |
| RF07 | **Scripts Personalizados** | Execução de scripts PowerShell/Batch via comando | **MÉDIA** | Média | RF03 |
| RF08 | **Abrir Sites Específicos** | Configuração simplificada de URLs e comandos | **MÉDIA** | Baixa | RF03 |
| RF09 | **Snap Layouts** | Posicionamento automático de janelas | **BAIXA** | Alta | RF03 |
| RF10 | **Print Screen** | Captura de tela via comando de voz | **BAIXA** | Baixa | RF03 |

### 3.2 Comandos de Exemplo (MVP)

#### Comandos do Sistema
| Comando (PT) | Comando (EN) | Ação | Parâmetros |
|--------------|--------------|------|------------|
| "Abrir [nome do programa]" | "Open [program]" | Inicia aplicativo | Caminho ou nome do app |
| "Fechar janela" | "Close window" | Fecha janela ativa | - |
| "Minimizar" | "Minimize" | Minimiza janela ativa | - |
| "Maximizar" | "Maximize" | Maximiza janela ativa | - |
| "Print" | "Screenshot" | Captura tela | - |
| "Copiar" | "Copy" | Ctrl+C | - |
| "Colar" | "Paste" | Ctrl+V | - |
| "Recortar" | "Cut" | Ctrl+X | - |

#### Comandos de Produtividade
| Comando (PT) | Comando (EN) | Ação | Parâmetros |
|--------------|--------------|------|------------|
| "Abrir YouTube" | "Open YouTube" | Abre youtube.com | URL configurável |
| "Pausar vídeo" | "Pause video" | Simula Espaço | - |
| "Script [nome]" | "Script [name]" | Executa script | Caminho do script |
| "Atalho [nome]" | "Shortcut [name]" | Executa atalho personalizado | Configurável |

### 3.3 Regras de Negócio

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

## 4. Requisitos Não-Funcionais

### 4.1 Performance

| Métrica | Target | Observação | Como Medir |
|---------|--------|------------|------------|
| **Latência Wake Word** | < 300ms | Tempo da fala ao reconhecimento | Logs com timestamp |
| **Latência Comando** | < 500ms | Do comando à execução da ação | Logs com timestamp |
| **CPU Idle** | < 2% | Quando não está processando áudio | Task Manager |
| **CPU Ativo** | < 15% | Durante reconhecimento de comando | Task Manager |
| **RAM** | < 200MB | Uso de memória total | Task Manager |
| **Startup Time** | < 3 segundos | Do clique à escuta ativa | Cronômetro |

### 4.2 Usabilidade

| Aspecto | Requisito | Como Validar |
|---------|-----------|--------------|
| **Curva de Aprendizado** | < 10 minutos para configurar primeiros comandos | Teste com usuário novo |
| **Configuração** | Adicionar comando simples em < 30 segundos | Teste de tempo |
| **Feedback Visual** | Indicador claro de estado (escutando/processing/error | Inspeção visual |
| **Acessibilidade** | Interface com atalhos de teclado | Teste de teclado |

### 4.3 Confiabilidade

| Métrica | Target | Observação | Como Validar |
|---------|--------|------------|--------------|
| **Uptime** | 99% | Pode reiniciar sem aviso (app desktop) | Logs de crash |
| **Crash Recovery** | Automático | Reinicia em caso de crash | Teste de crash |
| **False Positive Rate** | < 5% | Wake words não intencionais | Teste em ambiente real |
| **False Negative Rate** | < 10% | Comandos não reconhecidos | Teste em ambiente real |

### 4.4 Segurança e Privacidade

| Aspecto | Requisito | Como Validar |
|---------|-----------|--------------|
| **100% Local** | Nenhum dado é enviado para APIs externas | Análise de tráfego de rede |
| **Permissões** | Apenas acesso necessário ao SO | Revisão de permissões |
| **Logs** | Armazenados localmente, sem informações sensíveis | Inspeção de logs |
| **Scripts** | Sandbox para scripts customizados (opcional | Revisão de segurança |
| **Microfone** | Indicador visível quando ativo | Teste visual |

### 4.5 Compatibilidade

| Aspecto | Requisito | Notas |
|---------|-----------|-------|
| **Sistema Operacional** | Windows 10/11 (prioridade), macOS/Linux (futuro) | Fase 1: Windows apenas |
| **Arquitetura** | x64, ARM64 (experimental) | Testar em ambas |
| **Idiomas** | Português (BR), Inglês (US) | Configurável |
| **Microfone** | Qualquer dispositivo compatível com o SO | Testar com múltiplos dispositivos |

---

## 5. Arquitetura Técnica

### 5.1 Padrão Arquitetural

**Padrão Escolhido: Monólito Modular com Plugin System**

#### Justificativa
- ✅ Aplicação desktop com domínio bem delimitado
- ✅ Time pequeno (ou individual) = complexidade deve ser mínima
- ✅ Plugin system permite extensibilidade sem overhead de microserviços
- ✅ Deploy é single binary = simplicidade máxima para usuário
- ✅ Menores chances de bugs em comunicação entre componentes

#### Trade-offs Considerados

| Opção | Vantagens | Desvantagens | Decisão |
|-------|-----------|--------------|---------|
| **Monólito Modular** | Simples, rápido, fácil deploy, baixo overhead | Escala limitada (não é problema para app desktop) | ✅ **ESCOLHIDA** |
| Microservices | Escala independente, fault isolation | Complexidade operacional alta, overhead de rede | ❌ Overkill para desktop |
| Serverless | Zero infra, pay-per-use | Cold starts, vendor lock-in, não funciona local | ❌ Não aplicável |
| Event-Driven | Loose coupling, assíncrono | Complexidade de debugging, eventual consistency | ❌ Desnecessário |

### 5.2 Stack Tecnológico

#### Camada de Aplicação Principal

| Camada | Tecnologia | Versão | Justificativa |
|--------|-----------|--------|---------------|
| **Linguagem** | Python | 3.11+ | Ecossistema rico em ML/Audio, rápida prototipagem |
| **Framework GUI** | PyQt6 / PySide6 | 6.6+ | GUI nativa, multi-plataforma, widgets ricos |
| **Gerenciador de Pacotes** | Poetry | 1.7+ | Dependency locking, ambientes virtuais |

**Por que Python?**
- Ecossistema maduro para ML/Audio (Whisper, Porcupine)
- Rapidez de desenvolvimento (crítico para projeto individual)
- Bibliotecas excelentes para automação de Windows
- Fácil de debugar e manter

#### Camada de Reconhecimento de Voz

| Componente | Tecnologia | Versão | Justificativa |
|------------|-----------|--------|---------------|
| **Wake Word Detection** | **Picovoice Porcupine** | latest | 100% local, wake words customizáveis, ultra-baixa latência, free tier generoso, suporte PT/EN |
| **Speech-to-Text** | **OpenAI Whisper (local)** | latest | SOTA accuracy, modelo tiny/base para速度, 100% local, suporta PT/EN nativamente |
| **Fallback STT** | Vosk | latest | Alternativa lighter se Whisper for pesado |

**Por que essa combinação?**
- Porcupine: Única solução free realmente funcional para wake words customizáveis
- Whisper: Melhor STT open-source disponível, com modelo tiny de apenas ~40MB
- Vosk: Backup caso Whisper consuma recursos demais

**Alternativas Consideradas e Rejeitadas:**

| Tecnologia | Por que rejeitada? |
|------------|-------------------|
| Google Speech API | Não é local, custa \$, depende de internet |
| Azure Speech | Não é local, custa \$ |
| Mozilla Coqui (Ainda) | Projeto descontinuado em 2023 |
| PicoVoice Leopard | Custa \$, overkill para comandos simples |
| pocketsphinx | Muito antigo, baixa acurácia |

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

### 5.3 Diagrama de Arquitetura

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
│  │  - State management                            │     │
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
│  │ - Multi-keyword  │        │ - VAD                   │  │
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

### 5.4 Estrutura de Diretórios

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
│   ├── __init__.py
│   ├── test_recognition.py
│   ├── test_actions.py
│   ├── test_config.py
│   └── test_orchestrator.py
├── models/                          # Modelos Whisper
│   └── tiny.pt                      # ~40MB
├── scripts/                         # Scripts customizados
│   └── examples/
├── logs/                            # Logs (auto-criado)
├── config.yml                       # Config usuário (gitignored)
├── commands.yml                     # Comandos customizados
├── pyproject.toml                   # Poetry config
├── README.md
├── LICENSE
└── .gitignore
```

### 5.5 Modelo de Dados

#### Configuração (config.yml)

```yaml
# config.yml
general:
  language: pt-BR  # pt-BR | en-US
  log_level: INFO  # DEBUG | INFO | WARNING | ERROR
  startup_minimized: false
  auto_start: false  # Iniciar com Windows

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

  - id: cmd_maximize
    name: "Maximizar"
    patterns:
      - pt: "maximizar"
      - en: "maximize"
    action:
      type: window_maximize

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

  - id: cmd_copy
    name: "Copiar"
    patterns:
      - pt: "copiar"
      - en: "copy"
    action:
      type: clipboard_copy

  - id: cmd_paste
    name: "Colar"
    patterns:
      - pt: "colar"
      - en: "paste"
    action:
      type: clipboard_paste

  - id: cmd_cut
    name: "Recortar"
    patterns:
      - pt: "recortar"
      - en: "cut"
    action:
      type: clipboard_cut

  - id: cmd_pause_video
    name: "Pausar Vídeo"
    patterns:
      - pt: "pausar|pausa"
      - en: "pause"
    action:
      type: hotkey
      params:
        keys: "space"

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

## 6. Plano de Implementação

### 6.1 Visão Geral das Fases

| Fase | Nome | Duração Est. | Entregas | Dependências | Prioridade |
|------|------|--------------|----------|--------------|------------|
| **Fase 0** | Setup & Pesquisa | 1 dia | Ambiente, PoCs | - | **CRÍTICA** |
| **Fase 1** | Wake Word MVP | 2-3 dias | Detecção wake word | Fase 0 | **CRÍTICA** |
| **Fase 2** | Speech-to-Text | 2-3 dias | STT local | Fase 0 | **CRÍTICA** |
| **Fase 3** | Actions Core | 2-3 dias | Launcher, Window Mgr | Fase 1 | **ALTA** |
| **Fase 4** | Orquestração | 2 dias | Integração completa | Fase 1,2,3 | **ALTA** |
| **Fase 5** | GUI Básica | 3 dias | Config, Logs, Tray | Fase 4 | **ALTA** |
| **Fase 6** | Refinamento | 2-3 dias | Polimento, bugs | Fase 5 | **MÉDIA** |
| **Fase 7** | Features Extras | Futuro | Snap Layouts, etc | Fase 6 | **BAIXA** |

**Total Estimado MVP:** 15-20 dias (desenvolvimento individual focado)

### 6.2 Fase 0: Setup & Pesquisa (1 dia)

**Objetivo:** Validar viabilidade técnica e configurar ambiente de desenvolvimento.

**Atividades Detalhadas:**

| Horas | Atividade | Entrega |
|-------|-----------|---------|
| 1h | Configurar Python 3.11+ com Poetry | Ambiente funcional |
| 1h | Criar estrutura de diretórios | Estrutura completa |
| 1h | Testar Picovoice Porcupine | PoC wake word funcionando |
| 1h | Testar OpenAI Whisper local | PoC STT funcionando |
| 1h | Testar PyAutoGUI | PoC ação funcionando |
| 1h | Configurar Git repository | Repo inicializado |
| 2h | Documentar aprendizados | Notas de viabilidade |

**Entregáveis:**
- ✅ Ambiente de desenvolvimento funcional
- ✅ Prova de conceito: Porcupine detectando wake word
- ✅ Prova de conceito: Whisper transcrevendo áudio
- ✅ Prova de conceito: PyAutoGUI executando ação
- ✅ Estrutura de projeto criada
- ✅ Documentação de viabilidade

**Critérios de Sucesso:**
- Todos os PoCs funcionam end-to-end
- Latência wake word < 300ms
- Latência STT < 1s
- Nenhuma bloqueio técnico identificado

**Riscos e Mitigações:**
| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Porcupine não tem PT | Média | Alto | Testar custom wake words ou usar wake words em EN |
| Whisper muito lento | Média | Médio | Testar modelo tiny, considerar Vosk como fallback |
| Problemas de microfone | Baixa | Médio | Testar com múltiplos dispositivos |

### 6.3 Fase 1: Wake Word Detection (2-3 dias)

**Objetivo:** Implementar detecção contínua de wake words com baixíssima latência.

#### Dia 1: Integração Porcupine

**Atividades:**
1. Instalar pvporcupine package (`pip install pvporcupine`)
2. Criar conta no Picovoice Console para obter Access Key
3. Criar wrapper Python para Porcupine
4. Implementar stream de áudio contínuo
5. Adicionar múltiplas wake words configuráveis

**Código Esqueleto:**

```python
# src/recognition/wake_word.py
import pvporcupine
from typing import List, Callable, Optional
import threading
from src.utils.logger import get_logger

logger = get_logger(__name__)

class WakeWordDetector:
    def __init__(
        self,
        access_key: str,
        keywords: List[str],
        sensitivity: float = 0.5,
        callback: Optional[Callable[[int], None]] = None
    ):
        """
        Inicializa detector de wake word.
        
        Args:
            access_key: Chave de acesso do Picovoice
            keywords: Lista de wake words (built-in ou custom)
            sensitivity: Sensibilidade (0.0 - 1.0)
            callback: Função chamada quando wake word é detectada
        """
        self.keywords = keywords
        self.sensitivity = sensitivity
        self.callback = callback
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        try:
            # Criar instância do Porcupine
            keyword_paths = [kw if kw.endswith('.ppn') else kw for kw in keywords]
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=keyword_paths,
                sensitivities=[sensitivity] * len(keywords)
            )
            logger.info(f"WakeWordDetector initialized with {len(keywords)} keywords")
        except Exception as e:
            logger.error(f"Failed to initialize Porcupine: {e}")
            raise
    
    def _listen_loop(self):
        """Loop de escuta contínua em thread separada."""
        from src.utils.audio import AudioStream
        
        audio_stream = AudioStream(rate=self.porcupine.sample_rate, 
                                   frames_length=self.porcupine.frame_length)
        
        logger.info("Wake word detection started")
        
        try:
            while self._running:
                pcm = audio_stream.read_frames()
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    logger.info(f"Wake word detected: {self.keywords[keyword_index]}")
                    if self.callback:
                        self.callback(keyword_index)
        finally:
            audio_stream.close()
            logger.info("Wake word detection stopped")
    
    def start(self):
        """Inicia detecção de wake word em background."""
        if self._running:
            logger.warning("Wake word detection already running")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Para detecção de wake word."""
        if not self._running:
            return
        
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None
    
    def __del__(self):
        self.stop()
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()
```

#### Dia 2: Thread e Gerenciamento de Estado

**Atividades:**
1. Executar detecção em thread separada (já no esqueleto)
2. Implementar flags de stop/start
3. Gerenciar recursos (fechar stream ao parar)
4. Adicionar tratamento de erros (microfone desconectado, etc.)
5. Criar AudioStream utility

**Código Esqueleto - AudioStream:**

```python
# src/utils/audio.py
import pyaudio
from typing import Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AudioStream:
    def __init__(self, rate: int, frames_length: int):
        self.rate = rate
        self.frames_length = frames_length
        self._pyaudio: Optional[pyaudio.PyAudio] = None
        self._stream: Optional[pyaudio.Stream] = None
        self._open()
    
    def _open(self):
        try:
            self._pyaudio = pyaudio.PyAudio()
            self._stream = self._pyaudio.open(
                rate=self.rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.frames_length
            )
        except Exception as e:
            logger.error(f"Failed to open audio stream: {e}")
            raise
    
    def read_frames(self) -> bytes:
