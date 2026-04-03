---
description: Workflow completo de integração de tecnologia externa ao Pi (research → docs → plan → flowchart)
---
# Integração $1 ao Pi

## Workflow
1. **Researcher** (agent: researcher) → specs/01_${1}_practical_research.md
   - Projetos práticos, exemplos, boas práticas
   - Erros comuns e como evitá-los
   - Integrações documentadas

2. **Pi Docs Expert** (agent: pi-docs-expert) → specs/02_${1}_extension_research.md
   - Como Pi funciona (arquitetura, eventos, tools)
   - Como criar extensão para $1
   - Boas práticas e problemas a evitar

3. **Planner** (agent: planner) → specs/03_${1}_extension_plan.md
   - Arquitetura proposta
   - Componentes e dependências
   - Fases de implementação (ordenadas)
   - Riscos e mitigações
   - Checklist de validação

4. **Flowchart** (agent: flowchart) → specs/04_${1}_extension_flowchart.md
   - Fluxograma em Mermaid
   - Legenda dos componentes
   - Explicação dos fluxos

## Objetivo
Criar extensão Pi funcional para $1 (MVP, não AI slop)

## Evitar
- Alucinações (validar tudo)
- API keys inválidas (validar no startup)
- Arquitetura incompatível (verificar docs oficiais)
- Fases sem ordem lógica (implementação sequencial)
- Falta de validação (checklist completo)
- Não criar arquivos fisicamente (usar tool write)
