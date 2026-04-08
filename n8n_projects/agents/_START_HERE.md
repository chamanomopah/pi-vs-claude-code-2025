# 👋 Bem-vindo ao Ecossistema de Agentes n8n

Guia rápido para começar a usar os agentes n8n com Pi Coding Agent.

## 🚀 Comece Aqui

### O Que Foi Criado

Três agentes especializados + documentação completa:

1. **📐 n8n-architect** - Projeta workflows completos
2. **🔨 n8n-builder** - Implementa workflows (já existia)
3. **🧪 n8n-tester** - Testa workflows exaustivamente

### 📁 Arquivos Disponíveis

```
n8n_projects/agents/
├── _START_HERE.md           ← VOCÊ ESTÁ AQUI (guia rápido)
├── README.md                ← Visão geral do ecossistema
├── n8n-architect.md         ← Especificação do arquiteto
├── n8n-tester.md            ← Especificação do testador
├── EXEMPLO_FLUXO.md         ← Exemplo completo de uso
└── INTEGRACAO_PI.md         ← Guia de integração com Pi
```

## ⚡ Uso Rápido

### Comando Único (Time Completo)

```bash
pi -e agent-team --team n8n-team "Criar workflow que recebe webhook, salva no Google Sheets e avisa no Telegram"
```

### Passo a Passo

```bash
# 1. Projetar
pi -e agent-team --agent n8n-architect "Projetar workflow de processamento de pedidos"

# 2. Implementar
pi -e agent-team --agent n8n-builder "Implementar especificação do architect"

# 3. Testar
pi -e agent-team --agent n8n-tester "Testar workflow ID 123 completamente"
```

## 📖 Por Onde Começar

- **Novo no ecossistema?** → Leia `README.md`
- **Quer ver exemplos?** → Leia `EXEMPLO_FLUXO.md`
- **Quer integrar com Pi?** → Leia `INTEGRACAO_PI.md`
- **Quer usar o architect?** → Leia `n8n-architect.md`
- **Quer usar o tester?** → Leia `n8n-tester.md`

## 🎯 Fluxo de Trabalho

```
Seu Pedido
     ↓
n8n-architect (projeta)
     ↓
n8n-builder (implementa)
     ↓
n8n-tester (testa)
     ↓
[Se tiver bugs] → volta para builder
     ↓
✅ APROVADO → Workflow pronto!
```

## 🧩 Conhecimento n8n Necessário

Todos os agentes entendem:

### Split In Batches
- `main[0]` = fim do loop (todos os dados)
- `main[1]` = cada item do loop
- Precisa de Wait para continuar

### Merge Nodes
- Precisa de AMBAS entradas conectadas
- Modo "Wait" aguarda todos os dados

### Loops
- Último node reconecta para Split In Batches
- Wait sincroniza branches paralelos

## 📦 Próximos Passos

1. ✅ Especificações criadas
2. ⏳ Configurar variáveis de ambiente (.env)
3. ⏳ Testar integração com cada agente
4. ⏳ Criar primeiro workflow real

## 🆘 Precisa de Ajuda?

- **Documentação Pi**: `.pi/docs/`
- **Skills n8n**: `.pi/skills/n8n-*/`
- **Exemplos workflows**: `tools/n8n/workflow_exemples/`

---

**Status**: ✅ Pronto para uso  
**Versão**: 1.0.0  
**Data**: 2026-04-07

Vá para `README.md` para a documentação completa! 📚
