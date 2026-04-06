# Template de Plano Declarativo - N8N Workflow

**Use este template para criar novos planos de workflows n8n.**

Copie este arquivo, renomeie para `<nome-do-workflow>-plano.md` e preencha as seções.

---

# Plano de Workflow: {{NOME_DO_WORKFLOW}}

## Resumo
{{Descrição breve em 1-2 frases do que o workflow faz}}

## Trigger
**Tipo:** {{Tipo de node trigger}}
**Descrição:** {{O que dispara o workflow}}

## Campos de Entrada
| Campo | Tipo | Descrição |
|-------|------|----------|
| {{campo1}} | {{string/number/boolean}} | {{Descrição}} |
| {{campo2}} | {{string/number/boolean}} | {{Descrição}} |

## Fluxo Principal

### 1. Normalização
{{Passos de limpeza/validação dos dados (se aplicável)}}

```
Node: {{tipo do node}}
Ação:
- {{campo1}}: {{transformação}}
- {{campo2}}: {{transformação}}
```

### 2. Classificação
Compute `{{campo_de_classificacao}}` using these rules in order:
```
set value="{{valor1}}" if {{condição 1}};
else set value="{{valor2}}" if {{condição 2}};
else set value="{{valor3}}";
```

### 3. Roteamento (Switch)
Use a Switch node on `{{campo_de_classificacao}}` with {{N}} separate branches:

#### Branch: {{nome_branch_1}}
{{Descrição do propósito desta branch}}

**Nodes necessários:**
1. **{{node1}}** ({{tipo}}) - {{propósito}}
2. **{{node2}}** ({{tipo}}) - {{propósito}}

**Fluxo:** {{descrição do fluxo}}

**Lógica específica:**
```javascript
{{ código JavaScript se necessário }}
```

#### Branch: {{nome_branch_2}}
{{Descrição do propósito desta branch}}

**Nodes necessários:**
1. **{{node1}}** ({{tipo}}) - {{propósito}}

**Fluxo:** {{descrição do fluxo}}

---

## Nodes Necessários (Consolidado)
| Nome | Tipo (do catálogo) | ConnectionType | Propósito |
|------|-------------------|----------------|-----------|
| {{nome}} | {{tipo}} | {{main/ai_tool/etc}} | {{descrição}} |

**Total: {{N}} nodes**

## Conexões Principais
| Origem | Destino | Tipo | Saída |
|--------|---------|------|-------|
| {{source}} | {{target}} | {{main}} | {{[0] → [0]}} |
| {{source}} | {{target}} | {{main}} | {{[0] → [1]}} |

## Parâmetros Principais
| Node | Parâmetro | Valor/Expressão |
|------|-----------|-----------------|
| {{node}} | {{param}} | {{valor}} |

### {{Node Específico}}
- {{param1}}: {{valor}}
- {{param2}}: {{valor}}

### {{Node Específico}}
```javascript
{{ código se necessário }}
```

## Considerações Especiais

### Credenciais Necessárias
- {{Serviço 1}} (para {{propósito}})
- {{Serviço 2}} (para {{propósito}})

### Pré-requisitos
- {{Pré-requisito 1}}
- {{Pré-requisito 2}}

### Limitações
- {{Limitação 1}}
- {{Limitação 2}}

### Pontos de Atenção
- ⚠️ {{Ponto de atenção 1}}
- ⚠️ {{Ponto de atenção 2}}

## Validação de Catálogo

### Verificação de Nodes
- [ ] Todos os nodes estão em `catalogo_nodes.py`
- [ ] connectionTypes estão corretos
- [ ] Nodes alternativos foram identificados (se necessário)

### Nodes que PODEM não estar no catálogo
- ⚠️ {{node1}} - verificar e possivelmente adicionar
- ⚠️ {{node2}} - usar alternativa: {{alternativa}}

## Trade-offs Opcionais

### Versão Simples (Mínimo Viável)
**Nodes:** {{N}} nodes
**Funcionalidades:**
- {{funcionalidade 1}}
- {{funcionalidade 2}}

**Limitações:**
- {{limitação}}

### Versão Completa (Recurso Extra)
**Nodes adicionais:** {{+N}} nodes
**Funcionalidades extras:**
- {{funcionalidade extra 1}}
- {{funcionalidade extra 2}}

---

## Notas de Implementação

{{Qualquer informação adicional útil para implementação}}

## Checklist Pré-Implementação

- [ ] Catálogo verificado para todos os nodes
- [ ] Credenciais identificadas e configuráveis
- [ ] Pré-requisitos documentados
- [ ] Limitações conhecidas documentadas
- [ ] Trade-offs discutidos com usuário (se aplicável)
