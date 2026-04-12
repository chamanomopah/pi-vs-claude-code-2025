# Plano Executivo Jarvis - Detalhes Finais

**Documento Complementar ao plano_executivo.md**

---

## 7. Riscos e Mitigações (Detalhado)

### 7.1 Matriz de Riscos Completa

| ID | Risco | Probabilidade | Impacto | Mitigação | Contingência | Responsável |
|----|-------|---------------|---------|-----------|--------------|-------------|
| **R001** | Porcupine não tem wake words em PT | Média | Alto | Testar custom wake words via Picovoice Console | Usar wake words em EN ("computer") | Dev |
| **R002** | Whisper muito lento em CPU | Média | Médio | Usar modelo tiny, otimizar com threading | Trocar para Vosk (mais leve) | Dev |
| **R003** | Falsa detecção de wake word | Alta | Médio | Ajustar sensibilidade, confirmar com comando | Adicionar confirmação visual | Dev |
| **R004** | Comandos não reconhecidos (STT) | Média | Médio | Ajustar linguagem, treinar modelos | Adicionar comandos por teclado | Dev |
| **R005** | Microfone não funciona | Baixa | Alto | Testar múltiplos dispositivos, seleção | Suportar microfone USB alternativo | QA |
| **R006** | PyQt6 conflita com libs | Baixa | Médio | Testar early, considerar PySide6 | Trocar para PySide6 | Dev |
| **R007** | Performance degrada | Média | Médio | Monitorar memory leaks, otimizar | Reiniciar app periodicamente | Dev |
| **R008** | Windows bloqueia automação | Baixa | Alto | Testar UAC, executar como admin | Documentar permissões | QA |
| **R009** | Dependências não instalam | Baixa | Médio | Poetry para locking de versões | Instalador standalone | Dev |
| **R010** | Usuário não configura | Média | Médio | GUI intuitiva, presets | Vídeo tutorial | UX |

### 7.2 Análise de Riscos por Categoria

#### Riscos Técnicos
- **Wake Word Detection (R001, R003):** Mitigado com custom wake words e sensibilidade ajustável
- **Speech-to-Text (R002, R004):** Mitigado com modelos alternativos (Vosk)
- **Integração Windows (R008):** Testar early com diferentes configurações de UAC

#### Riscos de Performance
- **CPU/Memory (R002, R007):** Mitigado com modelos leveis e monitoramento contínuo
- **Latência (R004):** Métricas definidas e testadas em cada fase

#### Riscos de Usabilidade
- **Configuração (R010):** Mitigado com GUI intuitiva e documentação extensa
- **Hardware (R005):** Suportar múltiplos dispositivos de áudio

---

## 8. Cronograma e Milestones (Detalhado)

### 8.1 Cronograma Semanal

| Semana | Fases | Dias | Entregas Principais | Milestones |
|--------|-------|------|---------------------|------------|
| **Semana 1** | Fase 0, 1 | 1-4 | Setup, Wake Word MVP | ✅ Wake word funcionando |
| **Semana 2** | Fase 2, 3 | 5-9 | STT, Actions | ✅ Comandos executam |
| **Semana 3** | Fase 4, 5 | 10-14 | Orquestração, GUI | ✅ App end-to-end |
| **Semana 4** | Fase 6 | 15-18 | Refinamento | ✅ MVP estável |

### 8.2 Milestones

| Milestone | Data Est. | Critérios de Sucesso | Dependências |
|-----------|-----------|----------------------|--------------|
| **M1: Viabilidade** | Dia 1 | Todos os PoCs funcionando | - |
| **M2: Wake Word** | Dia 4 | Detecta wake word < 300ms | M1 |
| **M3: STT Funcional** | Dia 7 | Transcreve com 90%+ acurácia | M1 |
| **M4: Actions MVP** | Dia 10 | 8+ actions funcionando | M2, M3 |
| **M5: Integração** | Dia 12 | Fluxo completo < 2s | M4 |
| **M6: GUI** | Dia 15 | Interface funcional | M5 |
| **M7: MVP Pronto** | Dia 18 | Todos critérios de aceite | M6 |

### 8.3 Caminho Crítico

```
Fase 0 (Setup)
    ↓
Fase 1 (Wake Word) ← CRÍTICO
    ↓
Fase 3 (Actions)
    ↓
Fase 4 (Orquestração) ← CRÍTICO
    ↓
Fase 5 (GUI)
    ↓
Fase 6 (Refinamento)
```

**Fases 2 (STT) podem ser paralelas** com Fase 3 em parte.

---

## 9. Critérios de Aceite (Detalhado)

### 9.1 Critérios Técnicos

#### Performance
- [ ] **Latência Wake Word:** Média < 300ms em 95%+ das tentativas
- [ ] **Latência Comando:** End-to-end < 2s em 90%+ das tentativas
- [ ] **CPU Idle:** < 2% quando ocioso
- [ ] **CPU Ativo:** < 15% durante transcrição
- [ ] **RAM:** < 200MB total
- [ ] **Startup:** < 3s do clique à escuta ativa

#### Confiabilidade
- [ ] **Uptime:** 99% (reinicia automaticamente se crash)
- [ ] **False Positive:** < 5% (wake words não intencionais)
- [ ] **False Negative:** < 10% (comandos não reconhecidos)
- [ ] **Crash Recovery:** Recupera automaticamente

### 9.2 Critérios Funcionais

#### Wake Words
- [ ] Detecta pelo menos 3 wake words configuráveis
- [ ] Sensibilidade ajustável via config
- [ ] Feedback visual quando detectada

#### Comandos
- [ ] **Abrir programas:** Funciona com programas configurados
- [ ] **Fechar janela:** Fecha janela ativa corretamente
- [ ] **Minimizar/Maximizar:** Manipula janelas
- [ ] **Screenshot:** Salva em diretório configurado
- [ ] **Clipboard:** Copiar/Colar funcionam
- [ ] **Abrir sites:** Abre URLs configuradas

#### Interface
- [ ] **Janela Principal:** Inicia/Para escuta
- [ ] **Status Indicator:** Mostra estado (idle/listening/processing)
- [ ] **Logs Popup:** Mostra logs em tempo real
- [ ] **Config Dialog:** Edita configurações
- [ ] **System Tray:** Menu de contexto funcional

### 9.3 Critérios de Usabilidade

- [ ] **Curva de Aprendizado:** < 10 min para configurar primeiros comandos
- [ ] **Adicionar Comando:** < 30 segundos via GUI
- [ ] **Feedback Visual:** Claro e intuitivo
- [ ] **Documentação:** README completo com troubleshooting

### 9.4 Critérios de Qualidade

#### Código
- [ ] **Testes Unitários:** Cobertura > 70% em camadas críticas
- [ ] **Logs:** Estruturados em toda aplicação
- [ ] **Error Handling:** Robusto em todas as camadas
- [ ] **Type Hints:** Usados em todo código Python

#### Documentação
- [ ] **README:** Instruções de instalação e uso
- [ ] **Comandos:** Lista de comandos disponíveis
- [ ] **Configuração:** Como adicionar comandos
- [ ] **Troubleshooting:** Problemas comuns

### 9.5 Checklist Final

```
Performance
☐ Latência wake word < 300ms (medido)
☐ Latência comando < 2s (medido)
☐ CPU idle < 2% (medido)
☐ RAM < 200MB (medido)

Funcionalidade
☐ Wake word detecta em 95%+ das tentativas
☐ 8+ actions funcionando
☐ GUI não trava orquestrador
☐ Logs visíveis em tempo real
☐ Config editável via interface

Qualidade
☐ Zero crashes em 1 hora de uso
☐ Testes unitários passando
☐ Documentação completa
☐ README pronto

Usabilidade
☐ Configurar em < 10 min
☐ Adicionar comando em < 30s
☐ Feedback visual claro
☐ Documentação acessível
```

---

## 10. Recursos Necessários (Detalhado)

### 10.1 Hardware

#### Mínimo
- CPU: Dual-core 2.0GHz
- RAM: 4GB
- Disco: 1GB livre
- Microfone: Integrado ou USB

#### Recomendado
- CPU: Quad-core 2.5GHz+
- RAM: 8GB
- Disco: SSD
- Microfone: USB com cancelamento de ruído

### 10.2 Software

#### Desenvolvimento
- Python 3.11+
- Poetry 1.7+
- Git
- VS Code (recomendado)

#### Runtime (Usuário)
- Windows 10/11 (64-bit)
- Python 3.11+ (ou instalador standalone)
- Microfone configurado

### 10.3 Dependências Python

```toml
[tool.poetry.dependencies]
python = "^3.11"
PyQt6 = "^6.6"
pvporcupine = "^3.0"
openai-whisper = "^20231117"
pyautogui = "^0.9.54"
pygetwindow = "^0.0.9"
PyYAML = "^6.0"
pydantic = "^2.5"
loguru = "^0.7.2"

[tool.poetry.dev-dependencies]
pytest = "^7.4"
pytest-qt = "^4.2"
black = "^23.12"
ruff = "^0.1"
mypy = "^1.7"
```

### 10.4 Serviços Externos

| Serviço | Uso | Custo | Necessidade |
|---------|-----|-------|-------------|
| Picovoice Console | Wake words | Free (100 words) | Obrigatório |
| OpenAI API | Não usado | - | - |
| Azure/Google | Não usado | - | - |
| Cloud storage | Não usado | - | - |

**Total de Custos:** $0/mês

---

## 11. Referências (Detalhado)

### 11.1 Documentação Técnica

#### Picovoice Porcupine
- Site: https://picovoice.ai/
- Docs: https://picovoice.ai/docs/porcupine/
- Python SDK: https://github.com/Picovoice/porcupine
- Free Tier: 100 wake words customizadas

#### OpenAI Whisper
- Paper: https://arxiv.org/abs/2212.04356
- GitHub: https://github.com/openai/whisper
- Instalação: `pip install openai-whisper`
- Modelos: tiny (39M), base (74M), small (244M), medium (769M)

#### PyQt6
- Docs: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- Tutorial: https://www.pythonguis.com/
- Exemplos: https://github.com/pyqt/pyqt6-examples

### 11.2 Alternativas Consideradas

#### Wake Word Detection
| Tecnologia | Status | Por que não? |
|------------|--------|--------------|
| Picovoice Porcupine | ✅ Escolhido | Melhor opção free |
| Mycroft Precise | ❌ | Projeto descontinuado |
| Snowboy | ❌ | Descontinuado em 2019 |
| Sherpa-ONNX | ⚠️ | Alternativa futura |

#### Speech-to-Text
| Tecnologia | Status | Por que não? |
|------------|--------|--------------|
| OpenAI Whisper | ✅ Escolhido | SOTA accuracy, local |
| Vosk | ⚠️ Fallback | Mais leve, menos preciso |
| Google Speech API | ❌ | Não é local, custa $ |
| Azure Speech | ❌ | Não é local, custa $ |
| Coqui STT | ❌ | Projeto descontinuado |

### 11.3 Boas Práticas

#### Python
- PEP 8: Style Guide
- Type Hints: Python 3.11+ features
- Logging: loguru para structured logging
- Testing: pytest + pytest-qt

#### PyQt6
- Signals/Slots para comunicação entre threads
- QThread para operações longas
- QTimer para updates de UI

#### Performance
- Profiling: cProfile, py-spy
- Memory: memory_profiler
- CPU: psutil

### 11.4 Comunidades

- Reddit: r/Python, r/PyQt
- Discord: Picovoice Community
- Stack Overflow: Tags [python], [pyqt6], [speech-recognition]

---

## 12. Apêndices

### 12.1 Glossário

| Termo | Definição |
|-------|-----------|
| **Wake Word** | Palavra que ativa o assistente (ex: "Jarvis") |
| **STT** | Speech-to-Text, transcrição de áudio para texto |
| **VAD** | Voice Activity Detection, detecção de fala |
| **MVP** | Minimum Viable Product, produto mínimo viável |
| **PoC** | Proof of Concept, prova de conceito |

### 12.2 Comandos de Exemplo Completos

```yaml
# commands.yml - Exemplo completo
version: "1.0"

commands:
  # Launcher
  - id: cmd_open_chrome
    name: "Abrir Chrome"
    patterns:
      - pt: "abrir chrome|abra o chrome"
      - en: "open chrome"
    action:
      type: launcher
      params:
        program: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

  # Window
  - id: cmd_close
    name: "Fechar Janela"
    patterns:
      - pt: "fechar janela|feche essa janela"
      - en: "close window|close this window"
    action:
      type: window_close
      confirmation: true

  # Clipboard
  - id: cmd_copy
    name: "Copiar"
    patterns:
      - pt: "copiar|copie"
      - en: "copy"
    action:
      type: clipboard_copy

  # Screenshot
  - id: cmd_screenshot
    name: "Screenshot"
    patterns:
      - pt: "print|screenshot|tirar print"
      - en: "screenshot|take screenshot|print screen"
    action:
      type: screenshot
      params:
        save_to: "%USERPROFILE%\\Pictures\\Screenshots"

  # Custom
  - id: cmd_open_youtube_music
    name: "YouTube Music"
    patterns:
      - pt: "abrir youtube music|música"
      - en: "open youtube music|music"
    action:
      type: launcher
      params:
        url: "https://music.youtube.com"
```

### 12.3 Troubleshooting Comum

#### Wake Word Não Detecta
```
Sintoma: Wake word não é reconhecida
Possíveis causas:
1. Sensibilidade muito baixa
2. Microfone com volume baixo
3. Ruído ambiente muito alto

Soluções:
1. Aumentar sensitivity em config.yml
2. Testar com diferentes microfones
3. Falar mais perto do microfone
4. Usar wake word alternativa
```

#### STT Não Transcreve
```
Sintoma: Comando não é reconhecido
Possíveis causas:
1. Modelo muito pequeno (tiny)
2. Língua incorreta configurada
3. Áudio muito baixo

Soluções:
1. Tentar modelo base
2. Verificar config de language
3. Ajustar volume do microfone
4. Falar de forma mais clara
```

#### GUI Trava
```
Sintoma: Interface não responde
Possíveis causas:
1. Operação bloqueando thread principal
2. STT demorando demais

Soluções:
1. Verificar se orquestrador está em thread separada
2. Usar modelo whisper menor
3. Aumentar timeout de STT
```

---

## Conclusão

Este plano executivo fornece:

1. ✅ **Estrutura completa** do sistema de wake words
2. ✅ **Stack tecnológico** validado e justificado
3. ✅ **Fases de implementação** com entregas claras
4. ✅ **Riscos identificados** com mitigações
5. ✅ **Cronograma realista** com milestones
6. ✅ **Critérios de aceite** mensuráveis
7. ✅ **Recursos necessários** documentados

**Próximo Passo:** Iniciar Fase 0 - Setup & Pesquisa

**Status:** ✅ APROVADO PARA IMPLEMENTAÇÃO
