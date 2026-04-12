---
name: arquiteto-anti-halucinacao
description: Verifica rigorosamente que 100% da arquitetura é viável sem flaws. Valida existência de tecnologias, compatibilidade, aplicabilidade de patterns, e documenta fontes e evidências. SEMPRE use após gerar ou modificar planos de arquitetura.
allowed-tools:
  - read
  - grep
  - find
  - bash
---

# Skill: Anti-Halucinação para Arquitetura

## 🎯 Propósito

Validar **rigorosamente** documentos de arquitetura para garantir que **100% das decisões sejam viáveis**, verificando existência de tecnologias, compatibilidade, aplicabilidade de patterns e documentando evidências.

## 📋 Quando Usar Esta Skill

**SEMPRE** use esta skill após:
- Gerar um novo plano de arquitetura
- Modificar uma arquitetura existente
- Sugerir novas tecnologias ou padrões
- Fazer afirmações técnicas sobre capacidades de sistemas

## ⚠️ Por Que Esta Skill é Crítica

LLMs podem halucinar:
- Tecnologias que não existem
- Features que ferramentas não possuem
- Compatibilidades impossíveis
- Patterns aplicados incorretamente
- Versões de software que nunca foram lançadas
- Documentos de referência inventados

Esta skill previne todos esses problemas.

---

## 🔍 Checklist de Validação Completa

Para cada afirmação técnica no documento de arquitetura, valide:

### 1. Existência da Tecnologia
- A tecnologia/ferramenta realmente existe?
- Está ativa e mantida?
- Site oficial/documentação acessível?
- Repositório Git ativo?

### 2. Versões e Releases
- A versão mencionada existe?
- Foi lançada antes da data do documento?
- Está em estado estável (não alpha/beta)?

### 3. Features e Capacidades
- A feature mencionada realmente existe?
- Documentação confirma a capacidade?
- Requer configuração especial?
- Limitações conhecidas?

### 4. Compatibilidade
- As tecnologias funcionam juntas?
- Versões são compatíveis?
- Requer adaptadores/bridges?
- Há conflitos conhecidos?

### 5. Padrões e Patterns
- O pattern é aplicável ao caso de uso?
- Exemplos reais de uso similar?
- Requer pré-condições específicas?
- Trade-offs documentados?

### 6. Evidências e Fontes
- Cada decisão tem referência?
- Links para documentação oficial?
- Exemplos de produção?
- Artigos/blogs de fontes confiáveis?

---

## 🛠️ Comandos Disponíveis

### Validar Documento Completo
```bash
/skill:arquiteto-anti-halucinacao validate <arquivo-arquitetura.md>
```

### Validar Tecnologia Específica
```bash
/skill:arquiteto-anti-halucinacao check <nome-tecnologia>[:versão]
```

### Validar Compatibilidade
```bash
/skill:arquiteto-anti-halucinacao compat "<tech A>" "<tech B>"
```

### Pesquisar Evidências
```bash
/skill:arquiteto-anti-halucinacao evidence "<afirmação técnica>"
```

---

## 📊 Método de Validação

### Fase 1: Extração de Afirmações
1. Parsear documento de arquitetura
2. Extrair todas as afirmações técnicas
3. Categorizar por tipo
4. Priorizar afirmações críticas

### Fase 2: Verificação por Categoria

#### Para Tecnologias
Verificar site oficial, repositório GitHub, versões lançadas

#### Para Features
Buscar em documentação oficial e código fonte

#### Para Compatibilidade
Verificar issues no GitHub e discussões técnicas

#### Para Patterns
Buscar implementações reais e artigos de referência

### Fase 3: Documentação de Evidências
Para cada afirmação validada, registrar fontes, detalhes, limitações

### Fase 4: Relatório de Validação
Gerar relatório com estatísticas de validação

---

## 🎯 Matriz de Validação

| Categoria | Verificação | Fontes Mínimas | Status |
|-----------|-------------|----------------|--------|
| Tecnologia Existe | Site oficial + GH active | 2 | ✅/❌ |
| Versão Correta | Release notes/changelog | 1 | ✅/❌ |
| Feature Existe | Docs oficial + code | 2 | ✅/❌ |
| Compatibilidade | Integration docs + issues | 2 | ✅/⚠️/❌ |
| Pattern Aplicável | Fowler/Blog + examples | 2 | ✅/⚠️/❌ |
| Exemplo Produção | Case study + blog post | 1 | ✅/❌ |
| Limitações | Docs + issues/benchmarks | 2 | ✅/⚠️/❌ |

---

## 🚨 Categorias de Problemas

### Erro Crítico ❌
- Tecnologia não existe
- Versão nunca lançada
- Feature inventada
- Incompatibilidade impossível
- Pattern mal aplicado

**Ação:** Rejeitar documento, sugerir correção

### Aviso ⚠️
- Tecnologia depreciada
- Versão antiga sem suporte
- Feature experimental
- Compatibilidade com workaround
- Pattern com trade-offs significativos

**Ação:** Documentar ressalvas, sugerir alternativas

### Informação ℹ️
- Limitações de performance
- Configurações necessárias
- Dependências opcionais
- Casos de borda

**Ação:** Documentar como nota

---

## 📚 Fontes Confiáveis

### Documentação Oficial (Prioridade 1)
- Site da tecnologia
- Repositório oficial GitHub/GitLab
- Docs oficiais

### Referências Técnicas (Prioridade 2)
- Martin Fowler
- Microsoft/AWS/Azure/GCP Architecture Centers
- High Scalability

### Implementações Reais (Prioridade 3)
- GitHub (projetos com stars)
- Case studies em blogs oficiais
- Engineering blogs

### Discussões Técnicas (Prioridade 4)
- StackOverflow (respostas aceitas)
- Reddit r/programming, r/devops
- Issues/discussions em repositórios

### Fontes NÃO Confiáveis ❌
- Posts sem autor/data
- Blogs pessoais sem credibilidade
- Documentos sem referências
- Afirmações sem evidências

---

## ✅ Critérios de Aprovação

Um documento de arquitetura é **APROVADO** quando:

1. 100% das tecnologias existem e estão ativas
2. 100% das versões foram lançadas antes da data do documento
3. Todas as features mencionadas existem (ou ressalvas documentadas)
4. Compatibilidades confirmadas por fontes oficiais ou ressalvas documentadas
5. Patterns aplicáveis ao caso com exemplos reais
6. Cada decisão tem pelo menos 1 fonte de evidência
7. Relatório gerado com todas as validações

**Se qualquer item ❌:** Rejeitar e solicitar correções
