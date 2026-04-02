# Agent View Extension - Quick Start

## Instalação Rápida

```bash
# Criar diretório se não existir
mkdir -p ~/.pi/agent/extensions/

# Copiar extensão (se estiver em outro lugar)
cp -r agent-view ~/.pi/agent/extensions/

# Ou se já está no lugar certo, nada a fazer!
cd ~/.pi/agent/extensions/agent-view
```

## Uso Imediato

### Opção 1: Auto-open (recomendado)

```bash
# Agent view abre automaticamente
pi --agent-view-mode=auto

# Com layout específico
pi --agent-view-layout=1x4 --agent-view-font=small
```

### Opção 2: Manual

```bash
# Abrir durante a sessão
/agent-view
# ou
/av

# Fechar
q
# ou
/agent-view-close
```

## Keybindings Essenciais

| Key | Ação |
|-----|------|
| `Ctrl+Shift+A` | Abrir/fechar |
| `q` | Fechar |
| `1/2/4/8` | Layout (1x1, 1x2, 1x4, 1x8) |
| `o` | Ordenar por atividade |

## Testar com Multi-Agentes

```bash
# Usando agent-team (se disponível)
pi -e agent-team "Analyze this codebase" --agents 4

# Ou manualmente
pi -e subagent "Task 1" &
pi -e subagent "Task 2" &
pi -e subagent "Task 3" &
```

## Troubleshooting

### Agent view não abre
```bash
# Verificar modo
pi --agent-view-mode=auto

# Ver logs
PI_DEBUG=1 pi --agent-view-mode=auto
```

### Subprocessos não detectados
```bash
# Verificar se subprocesso usa padrão correto
pi --mode json -p --no-extensions \
   --append-system-prompt /tmp/prompt-test.md \
   "Test task"
```

### Layout quebrado
```bash
# Terminal muito pequeno, usar list
/agent-view layout list

# Ou aumentar terminal
# 1x8 precisa de >= 120 colunas
# 1x4 precisa de >= 80 colunas
```

## Comandos Úteis

```bash
# Ver todos os agentes
/agent-view

# Mudar layout
/agent-view layout 1x4

# Mudar fonte
/agent-view font small

# Ordenar por atividade
/agent-view sort

# Ver status
# Os agentes são mostrados com símbolos:
# ○ idle  ◐ starting  ● running  ◑ waiting  ✓ complete  ✗ error
```

## Arquivos de Referência

- `README.md` - Documentação completa
- `IMPLEMENTATION.md` - Detalhes da implementação
- `example.ts` - Testes e exemplos
- `specs/agent-view-spec-v1.1-summary.md` - Especificação

## Suporte

Se encontrar problemas:
1. Verificar `PI_DEBUG=1` para logs
2. Consultar `IMPLEMENTATION.md` para detalhes técnicos
3. Revisar `specs/agent-view-spec-corrections.md` para correções conhecidas
