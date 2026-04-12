# Plano Executivo - Jarvis Wake Words - Resumo Executivo

**Versão:** 3.0 - Completo e Revisado  
**Data:** 12/04/2026  
**Status:** Aprovado para Implementação

---

## Sumário Executivo

Este documento é um plano executivo completo para o desenvolvimento de um sistema de assistente pessoal por voz (estilo Jarvis) **100% local**, sem custos de APIs, focado em produtividade e automação de tarefas repetitivas.

### Objetivos Principais
1. Automação de tarefas repetitivas através de comandos de voz
2. Produtividade máxima: execução em < 500ms
3. Simplicidade: modificar comandos sem programação
4. 100% local e gratuito

### Valor Proposto
- Economia de ~30 minutos/dia em tarefas repetitivas
- Experiência fluida como um verdadeiro assistente
- Configuração flexível em segundos
- Observabilidade total com logs em tempo real

---

## Stack Tecnológico (Resumido)

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| **Linguagem** | Python 3.11+ | Ecossistema rico em ML/Audio |
| **GUI** | PyQt6 | GUI nativa e multi-plataforma |
| **Wake Word** | Picovoice Porcupine | 100% local, ultra-baixa latência |
| **STT** | OpenAI Whisper | SOTA accuracy, modelo tiny de 40MB |
| **Automação** | PyAutoGUI, pygetwindow | Controle de janelas e teclado |
| **Config** | YAML + Pydantic | Legível e type-safe |
| **Logs** | loguru | Structured logging |

---

## Arquitetura (Resumida)

```
Usuário (Voz)
    ↓
GUI Layer (PyQt6)
    ↓
Orchestration Layer (Command Orchestrator)
    ↓
Recognition Layer (Porcupine + Whisper)
    ↓
Action Execution Layer (Plugins)
    ↓
Windows OS
```

**Padrão:** Monólito Modular com Plugin System
**Justificativa:** Aplicação desktop com domínio bem delimitado, time pequeno, simplicidade máxima.

---

## Fases de Implementação

| Fase | Nome | Duração | Entregas | Prioridade |
|------|------|---------|----------|------------|
| **0** | Setup & Pesquisa | 1 dia | Ambiente, PoCs | CRÍTICA |
| **1** | Wake Word MVP | 2-3 dias | Detecção wake word | CRÍTICA |
| **2** | Speech-to-Text | 2-3 dias | STT local | CRÍTICA |
| **3** | Actions Core | 2-3 dias | Launcher, Window Mgr | ALTA |
| **4** | Orquestração | 2 dias | Integração completa | ALTA |
| **5** | GUI Básica | 3 dias | Config, Logs, Tray | ALTA |
| **6** | Refinamento | 2-3 dias | Polimento, bugs | MÉDIA |

**Total MVP:** 15-20 dias

---

## Funcionalidades MVP

### Wake Words
- Múltiplas wake words configuráveis
- Sensibilidade ajustável
- Detecção contínua com baixíssimo consumo

### Comandos de Voz
- Abrir programas: "Abrir Chrome"
- Fechar janela: "Fechar janela"
- Minimizar/Maximizar
- Print screen
- Copiar/Colar/Recortar
- Abrir sites: "Abrir YouTube"
- Executar scripts

### Interface
- Janela de configuração visual
- System tray icon
- Logs em tempo real (toggle on/off)
- Indicador de status visual

---

## Requisitos Não-Funcionais

| Métrica | Target |
|---------|--------|
| Latência Wake Word | < 300ms |
| Latência Comando | < 500ms |
| CPU Idle | < 2% |
| RAM | < 200MB |
| Startup | < 3s |

---

## Estrutura de Diretórios

```
jarvis-voice-assistant/
├── src/
│   ├── main.py              # Entry point
│   ├── config/              # Configurações
│   ├── gui/                 # Interface PyQt6
│   ├── core/                # Orquestrador
│   ├── recognition/         # Wake word + STT
│   ├── actions/             # Plugins de ação
│   └── utils/               # Utilidades
├── tests/                   # Testes
├── models/                  # Whisper tiny.pt
├── scripts/                 # Scripts customizados
├── config.yml               # Config usuário
├── commands.yml             # Comandos
└── pyproject.toml           # Poetry
```

---

## Riscos Principais

| Risco | Mitigação | Contingência |
|-------|-----------|--------------|
| Porcupine sem PT | Custom wake words | Usar EN |
| Whisper lento | Modelo tiny + threading | Vosk |
| Falsa detecção | Ajustar sensibilidade | Confirmação visual |

---

## Próximos Passos

1. **Validação de Viabilidade (Fase 0)**
   - Configurar ambiente Python
   - Testar Porcupine + Whisper + PyAutoGUI
   - Documentar aprendizados

2. **Desenvolvimento MVP (Fases 1-5)**
   - Seguir sequência de fases
   - Testes contínuos
   - Documentação progressiva

3. **Refinamento (Fase 6)**
   - Polimento de UX
   - Otimização de performance
   - Documentação final

---

## Critérios de Aceite do MVP

- [ ] Detecta wake word em 95%+ das tentativas
- [ ] Executa comandos em < 2s (wake → STT → action)
- [ ] GUI funcional sem travar orquestrador
- [ ] Config pode ser editada via interface
- [ ] Logs visíveis em tempo real
- [ ] Zero crashes em uso normal de 1 hora
- [ ] README com instruções completas

---

## Recursos Necessários

### Hardware
- Computador com Windows 10/11
- Microfone funcional
- 4GB RAM mínimos
- 1GB espaço em disco

### Software
- Python 3.11+
- Poetry
- Git

### Serviços Externos
- Picovoice Console (free tier)
- Nenhum outro serviço pago

---

## Documentação Adicional

- Plano completo em `PLANO_EXECUTIVO_COMPLETO.md`
- Código fonte em `src/`
- Testes em `tests/`
- Exemplos de comandos em `commands.yml`

---

**Status:** Pronto para implementação  
**Próxima Ação:** Iniciar Fase 0 - Setup & Pesquisa
