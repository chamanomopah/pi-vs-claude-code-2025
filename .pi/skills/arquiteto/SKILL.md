---
name: arquiteto
description: Gera planos de arquitetura completos com tecnologias recomendadas, estrutura de componentes, decisões técnicas justificadas e visão geral do sistema. Use quando precisar planejar a arquitetura de um projeto, sistema ou feature.
allowed-tools:
  - read
  - write
  - grep
  - find
  - bash
---

# Skill: Arquiteto de Software

## 🎯 Propósito

Gerar **planos de arquitetura completos** e robustos para projetos de software, incluindo seleção de tecnologias, estrutura de componentes, decisões técnicas justificadas e visão sistêmica.

## 📋 Quando Usar Esta Skill

Ative esta skill quando o usuário:
- Precisar criar uma arquitetura do zero para um novo projeto
- Quiser refatorar ou evoluir uma arquitetura existente
- Precisar documentar a arquitetura de um sistema
- Quiser avaliar diferentes opções tecnológicas
- Precisar justificar decisões arquiteturais para stakeholders
- Quiser planejar a estrutura de componentes de um sistema

---

## 🏗️ Template de Documento de Arquitetura

Use o template em `@assets/architecture-template.md` como base para todos os documentos de arquitetura.

### Seções Obrigatórias

1. **Visão Geral** - Resumo executivo do sistema
2. **Requisitos Funcionais** - O que o sistema faz
3. **Requisitos Não-Funcionais** - Performance, segurança, escalabilidade
4. **Stack Tecnológico** - Tecnologias selecionadas e justificativas
5. **Arquitetura de Componentes** - Módulos e suas responsabilidades
6. **Arquitetura de Dados** - Modelos, bancos, fluxos de dados
7. **Integrações** - Serviços externos e APIs
8. **Segurança** - Autenticação, autorização, proteção de dados
9. **Deploy e Infraestrutura** - Como o sistema será implantado
10. **Riscos e Mitigações** - Potenciais problemas e soluções

---

## 🎯 Checklist de Geração de Arquitetura

Ao criar um plano de arquitetura, SEMPRE siga este checklist:

### **1. Compreensão do Problema**
- [ ] Entender o domínio do negócio
- [ ] Identificar os usuários e seus objetivos
- [ ] Mapear os fluxos principais
- [ ] Listar requisitos explícitos e implícitos

### **2. Requisitos Funcionais**
- [ ] Listar todas as features necessárias
- [ ] Definir regras de negócio
- [ ] Mapear casos de uso
- [ ] Identificar integrações necessárias

### **3. Requisitos Não-Funcionais**
- [ ] Performance (latência, throughput)
- [ ] Escalabilidade (usuários, dados)
- [ ] Disponibilidade (SLA, failover)
- [ ] Segurança (autenticação, autorização, criptografia)
- [ ] Manutenibilidade (observabilidade, logging)
- [ ] Compliance (LGPD, SOC2, etc)

### **4. Seleção Tecnológica**
- [ ] Avaliar linguagens/frameworks
- [ ] Selecionar bancos de dados
- [ ] Definir camada de cache
- [ ] Escolher message broker (se necessário)
- [ ] Definir estratégia de deploy
- [ ] Selecionar ferramentas de observabilidade

### **5. Arquitetura de Componentes**
- [ ] Definir limites dos módulos
- [ ] Estabelecer comunicação entre componentes
- [ ] Planejar escalabilidade horizontal/vertical
- [ ] Definir estratégias de isolamento de falhas

### **6. Arquitetura de Dados**
- [ ] Modelar entidades e relacionamentos
- [ ] Definir estratégias de normalização/desnormalização
- [ ] Planejar migração de dados
- [ ] Estabelecer backup e disaster recovery

### **7. Segurança**
- [ ] Autenticação (OAuth, JWT, SAML)
- [ ] Autorização (RBAC, ABAC)
- [ ] Proteção de dados em trânsito (TLS)
- [ ] Proteção de dados em repouso (encrypt)
- [ ] Rate limiting e DDoS protection
- [ ] Logging de auditoria

### **8. Deploy e Infraestrutura**
- [ ] Estratégia de CI/CD
- [ ] Gerenciamento de configuração
- [ ] Monitoramento e alertas
- [ ] Rollback strategy
- [ ] Ambiente de staging/produção

### **9. Documentação**
- [ ] Diagramas de arquitetura
- [ ] Documentação de APIs
- [ ] Runbooks operacionais
- [ ] Guia de desenvolvimento local

### **10. Validação**
- [ ] **CRÍTICO:** Usar skill `/skill:arquiteto-anti-halucinacao` para validar
- [ ] Prova de conceito para decisões arriscadas
- [ ] Review com stakeholders
- [ ] Análise de custos (TCO)

---

## 🛠️ Comandos Disponíveis

### **Gerar Novo Plano de Arquitetura**

```bash
/skill:arquiteto --novo "<descrição do projeto>"
```

**Exemplo:**
```bash
/skill:arquiteto --novo "Sistema de marketplace para produtos digitais com 100k usuários esperados"
```

### **Refinar Arquitetura Existente**

```bash
/skill:arquiteto --refinar <arquivo-arquitetura.md>
```

### **Comparar Stacks Tecnológicas**

```bash
/skill:arquiteto --comparar "<stack A>" "<stack B>"
```

---

## 🚀 Workflow de Criação de Arquitetura

### **Fase 1: Descoberta**
1. Interview stakeholders
2. Documentar requisitos
3. Mapear usuários e fluxos
4. Identificar restrições

### **Fase 2: Exploração**
1. Brainstorm options
2. Research tecnologias
3. Avaliar trade-offs
4. Criar proof-of-concepts (se necessário)

### **Fase 3: Decisão**
1. Selecionar stack tecnológico
2. Definir arquitetura de componentes
3. Planejar arquitetura de dados
4. Documentar decisões (ADR)

### **Fase 4: Validação**
1. **USAR SKILL arquiteto-anti-halucinacao**
2. Review com time técnico
3. Análise de custos
4. Prova de conceito

### **Fase 5: Documentação**
1. Criar diagramas
2. Documentar APIs
3. Escrever runbooks
4. Guias de desenvolvimento

---

## 📝 Template de ADR (Architecture Decision Record)

Use ADRs para documentar decisões arquiteturais importantes:

```markdown
# ADR-XXX: [Título da Decisão]

## Status
Proposto | Aceito | Deprecado | Superseded by ADR-YYY

## Contexto
Qual problema estamos tentando resolver?
Quais são as restrições?

## Decisão
O que decidimos?

## Consequências
- Positivas: ...
- Negativas: ...
- Riscos: ...
```

---

## ✅ Critérios de Sucesso

Um bom plano de arquitetura deve:

1. ✅ **Responder ao problema real** - Alinhado com requisitos
2. ✅ **Justificar decisões** - Trade-offs documentados
3. ✅ **Ser validado** - Sem halucinações ou tecnologias inventadas
4. ✅ **Ser acionável** - Time consegue implementar
5. ✅ **Ser observável** - Monitoramento e debugging planejados
6. ✅ **Ser economicamente viável** - Custos dentro do budget
7. ✅ **Ser evolutivo** - Caminho claro para crescimento

---

**Próximo passo:** Após usar esta skill, sempre execute `/skill:arquiteto-anti-halucinacao` para validar o documento gerado!
