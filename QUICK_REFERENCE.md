# Quick Reference: Boas Práticas N8N v2

## Estrutura

```
docs/boas-praticas/n8n/
├── core/       (4) - Conceitos fundamentais
├── patterns/   (3) - Padrões de arquitetura
├── nodes/      (3) - Documentação de nodes
└── custom/     (2) - Convenções personalizadas
```

## Comandos

```bash
# Carregar tudo
/n8n-load-boas-praticas

# Carregar categoria
/n8n-load-boas-praticas core|patterns|nodes|custom

# Carregar arquivo
/n8n-load-boas-praticas split-in-batches|loop-simples|http-request
```

## Adicionar Arquivo

```bash
# 1. Criar
vim docs/boas-praticas/n8n/<categoria>/<arquivo>.md

# 2. Disponível imediatamente!
```

## Categorias

| Categoria | Arquivos | Conteúdo |
|-----------|----------|----------|
| core | 4 | split-in-batches, merge-nodes, loops, fluxo-dados |
| patterns | 3 | loop-simples, loop-com-erro, branches-paralelos |
| nodes | 3 | http-request, if-switch, webhook |
| custom | 2 | minhas-convencoes, integracoes-especificas |

## Referências

```
"Conforme patterns/loop-simples.md seção 5"
"Documentado em nodes/webhook.md"
"Padrão em core/merge-nodes.md"
```

## Comandos Úteis

```bash
find docs/boas-praticas/n8n/ -name "*.md" | sort
tree docs/boas-praticas/n8n/
grep -r "main[0]" docs/boas-praticas/n8n/
```

---

**Mudança:** Arquivo único → 13 arquivos em pastas organizadas  
**Benefício:** Fácil expansão, carregamento sob demanda, referências precisas
