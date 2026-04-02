# Agent View Extension v1.1.0

Visualizador em tempo real para agentes Pi executando em paralelo.

## Features

- **Detecção Universal**: Detecta automaticamente subprocessos Pi via hook em `spawn()`
- **Layouts Responsivos**: 1x1, 1x2, 1x4, 1x8, e list com fallback automático
- **Modo JSON**: Emite eventos estruturados quando Pi roda com `--mode json`
- **Multi-Orquestrador**: Compatível com agent-team, agent-chain, pi-pi, subagent-widget
- **Keybindings Não-Conflitantes**: Usa `Ctrl+Shift+A` em vez de `Ctrl+A`
- **Auto-Refresh**: Atualização automática com cleanup de agentes antigos
- **Truncamento Responsivo**: Renderização correta com caracteres multibyte

## Instalação

```bash
# Copiar para diretório de extensões do Pi
cp -r agent-view ~/.pi/agent/extensions/

# Ou instalar via Pi
pi install ~/.pi/agent/extensions/agent-view
```

## Uso

### Comandos

```bash
# Abrir/fechar agent-view
/agent-view
/av

# Alterar layout
/agent-view layout 1x4
/agent-view-layout --layout 1x8

# Alterar fonte
/agent-view font small
/agent-view-font --size medium

# Alternar ordenação
/agent-view sort
/agent-view-sort

# Fechar
/agent-view close
/agent-view-close
```

### Keybindings

| Key | Action |
|-----|--------|
| `Ctrl+Shift+A` | Toggle agent-view |
| `Ctrl+Shift+Q` | Close agent-view |
| `q` | Close (quando ativo) |
| `1` | Layout 1x1 |
| `2` | Layout 1x2 |
| `4` | Layout 1x4 |
| `8` | Layout 1x8 |
| `s` | Font small |
| `m` | Font medium |
| `l` | Font large |
| `o` | Toggle sort |
| `←/→` | Navegar páginas |

### Flags CLI

```bash
pi --agent-view-layout=1x4 --agent-view-font=small
pi --agent-view-mode=manual  # Não abrir automaticamente
```

## Layouts

| Layout | Min Width | Max Agents | Descrição |
|--------|-----------|------------|-----------|
| 1x1 | 40 | 1 | Um agente em tela cheia |
| 1x2 | 60 | 2 | Dois agentes lado a lado |
| 1x4 | 80 | 4 | Quatro agentes em grid 2x2 |
| 1x8 | 120 | 8 | Oito agentes em grid 4x2 |
| list | 40 | ∞ | Lista com paginação |

**Fallback automático**: Se o terminal for menor que o mínimo, layout muda para "list".

## Status Indicators

- `○` **Idle**: Aguardando início
- `◐` **Starting**: Iniciando subprocesso
- `●` **Running**: Executando tarefa
- `◑` **Waiting**: Aguardando LLM/response
- `✓` **Complete**: Completado com sucesso
- `✗` **Error**: Erro fatal
- `⊘` **Aborted**: Cancelado pelo usuário

## Source Indicators

- `⚡` **agent-team**: Multi-agent parallel execution
- `⛓` **agent-chain**: Sequential agent chain
- `🔄` **pi-pi**: Nested Pi instances
- `⊙` **subagent**: Direct subagent spawn
- `?` **unknown**: Source unknown

## Modo JSON

Quando Pi roda com `--mode json`, o agent-view emite eventos estruturados:

```json
{"type":"agent_view","event":"start","timestamp":1711849280000,"data":{"workflowId":"wf-001","agents":4}}
{"type":"agent_view","event":"update","timestamp":1711849280500,"data":{"agents":[{"id":"scout-1","status":"running","progress":15}]}}
{"type":"agent_view","event":"end","timestamp":1711849285000,"data":{"summary":{"totalAgents":4,"successful":4}}}
```

## Arquitetura

```
agent-view/
├── index.ts      # Registro da extensão, comandos, flags, hooks
├── monitor.ts    # AgentMonitor, detecção universal, StateManager
├── widget.ts     # Componentes TUI, LayoutManager, RenderEngine
└── manifest.json # Metadados da extensão
```

### Módulos

**index.ts** (~400 linhas)
- Registro da extensão (default function)
- Comandos `/agent-view` e aliases
- Flags CLI (`--agent-view-layout`, `--agent-view-font`, `--agent-view-mode`)
- Keybindings globais (`Ctrl+Shift+A`, `q`)
- Hook em `session_start` para auto-abertura
- Hook universal em `spawn()` para detecção de subprocessos

**monitor.ts** (~450 linhas)
- `AgentMonitor`: EventEmitter para eventos de agentes
- `StateManager`: Gerenciamento de estado dos agentes
- Detecção via eventos `subagent:spawn`, `subagent:start`, `subagent:output`, `subagent:complete`
- Mapeamento de status (starting → running → waiting → complete/error)
- Auto-refresh com cleanup de agentes antigos
- Ordenação por modo (default position ou active status)

**widget.ts** (~500 linhas)
- `AgentViewWidget`: Componente TUI principal
- `LayoutManager`: Cálculo de dimensões responsivas
- `RenderEngine`: Renderização de panes, header, footer
- Suporte a layouts 1x1, 1x2, 1x4, 1x8, list
- Truncamento responsivo com `visibleWidth()` e `truncateToWidth()`
- Paginação para múltiplos agentes
- Input handling para keybindings

## Compatibilidade

| Orquestrador | Compatível | Detecção |
|--------------|------------|----------|
| agent-team | ✅ | Universal (spawn hook) |
| agent-chain | ✅ | Universal (spawn hook) |
| pi-pi | ✅ | Universal (spawn hook) |
| subagent-widget | ✅ | Universal (spawn hook) |
| subagent (original) | ✅ | Universal (spawn hook) |
| Custom | ⚠️ | Se seguir padrão Pi |

**Padrão de detecção**: Subprocessos com `--mode json -p --no-extensions --append-system-prompt`

## Desenvolvimento

```bash
# Testar extensão
pi -e ~/.pi/agent/extensions/agent-view/index.ts

# Com flags
pi --agent-view-layout=1x4 --agent-view-font=small

# Ver logs
PI_DEBUG=1 pi -e agent-view
```

## Referência

- SPEC: `specs/agent-view-spec-v1.1-summary.md`
- Correções: `specs/agent-view-spec-corrections.md`
- Pi SDK: `@mariozechner/pi-coding-agent`
- Pi TUI: `@mariozechner/pi-tui`

## License

MIT
