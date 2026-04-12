# Skills do Arquiteto

Este diretório contém as skills especializadas para o agente **Arquiteto de Software**.

## Skills Disponíveis

### 1. arquiteto
**Arquivo:** `SKILL.md`

Gera planos de arquitetura completos com tecnologias recomendadas, estrutura de componentes e decisões técnicas justificadas.

**Quando usar:**
- Criar arquitetura do zero para um projeto
- Refatorar ou evoluir arquitetura existente
- Documentar arquitetura de um sistema
- Avaliar diferentes opções tecnológicas

**Comandos:**
```bash
/skill:arquiteto --novo "<descrição do projeto>"
/skill:arquiteto --refinar <arquivo-arquitetura.md>
/skill:arquiteto --comparar "<stack A>" "<stack B>"
```

---

### 2. arquiteto-anti-halucinacao
**Arquivo:** `../arquiteto-anti-halucinacao/SKILL.md`

Verifica rigorosamente que 100% da arquitetura é viável sem flaws. Valida existência de tecnologias, compatibilidade, aplicabilidade de patterns e documenta fontes e evidências.

**CRÍTICO:** Sempre use esta skill após gerar ou modificar planos de arquitetura.

**Comandos:**
```bash
/skill:arquiteto-anti-halucinacao validate <arquivo-arquitetura.md>
/skill:arquiteto-anti-halucinacao check <nome-tecnologia>[:versão]
/skill:arquiteto-anti-halucinacao compat "<tech A>" "<tech B>"
/skill:arquiteto-anti-halucinacao evidence "<afirmação técnica>"
```

---

### 3. arquiteto-pesquisa-tecnica
**Arquivo:** `../arquiteto-pesquisa-tecnica/SKILL.md`

Pesquisa informações técnicas na internet para validar decisões arquiteturais, encontrar melhores práticas, comparar tecnologias e descobrir exemplos reais de uso em produção.

**Quando usar:**
- Comparar tecnologias ou frameworks
- Encontrar melhores práticas para padrões arquiteturais
- Validar decisão arquitetural com fontes externas
- Descobrir como empresas resolvem problemas similares

**Comandos:**
```bash
/skill:arquiteto-pesquisa-tecnica compare "<tecnologia A>" "<tecnologia B>"
/skill:arquiteto-pesquisa-tecnica best-practices "<padrão/arquitetura>"
/skill:arquiteto-pesquisa-tecnica validate "<decisão arquitetural>"
/skill:arquiteto-pesquisa-tecnica production "<tecnologia/padrão>"
/skill:arquiteto-pesquisa-tecnica benchmark "<tecnologia>"
/skill:arquiteto-pesquisa-tecnica search "<problema ou dúvida>"
```

---

## Workflow Típico de Uso

### Passo 1: Gerar Arquitetura Inicial
```bash
/skill:arquiteto --novo "Sistema de marketplace para produtos digitais com 100k usuários esperados"
```

### Passo 2: Pesquisar Dúvidas Específicas
```bash
/skill:arquiteto-pesquisa-tecnica compare "PostgreSQL" "MongoDB" para e-commerce
```

### Passo 3: Validar Documento (OBRIGATÓRIO)
```bash
/skill:arquiteto-anti-halucinacao validate docs/arquitetura-marketplace.md
```

### Passo 4: Corrigir Problemas Encontrados
Ajustar o documento com base nas correções sugeridas

### Passo 5: Re-validar
```bash
/skill:arquiteto-anti-halucinacao validate docs/arquitetura-marketplace-v2.md
```

---

## Estrutura de Diretórios

```
arquiteto/
├── SKILL.md                    # Documento principal da skill
├── README.md                   # Este arquivo
├── assets/                     # Templates e recursos
│   └── architecture-template.md # Template de documento de arquitetura
├── references/                 # Documentação de referência
│   ├── architecture-patterns.md # Padrões arquiteturais
│   └── tech-stack-guide.md      # Guia de seleção de stack
└── scripts/                    # Scripts auxiliares
    └── generate-architecture-doc.sh # Gerador de documentos

arquiteto-anti-halucinacao/
├── SKILL.md                    # Documento principal
├── assets/                     # Templates de relatório
├── references/                 # Metodologia de validação
└── scripts/                    # Scripts de validação
    └── validate-tech.sh        # Validação de tecnologias

arquiteto-pesquisa-tecnica/
├── SKILL.md                    # Documento principal
├── assets/                     # Templates de relatório de pesquisa
├── references/                 # Guias de pesquisa
└── scripts/                    # Scripts de busca e análise
```

---

## Scripts Auxiliares

### generate-architecture-doc.sh
Gera um documento de arquitetura inicial usando o template.

```bash
./arquiteto/scripts/generate-architecture-doc.sh <nome-projeto> [output-dir]
```

**Exemplo:**
```bash
./arquiteto/scripts/generate-architecture-doc.sh marketplace docs
# Gera: docs/arquitetura-marketplace.md
```

### validate-tech.sh
Valida se uma tecnologia existe e retorna informações básicas.

```bash
./arquiteto-anti-halucinacao/scripts/validate-tech.sh <nome-tecnologia> [versão]
```

**Exemplo:**
```bash
./arquiteto-anti-halucinacao/scripts/validate-tech.sh Prisma 5.0
```

---

## Templates Disponíveis

### architecture-template.md
Template completo de documento de arquitetura com:

1. Visão Geral
2. Requisitos Funcionais
3. Requisitos Não-Funcionais
4. Stack Tecnológico
5. Arquitetura de Componentes
6. Arquitetura de Dados
7. Integrações
8. Segurança
9. Deploy e Infraestrutura
10. Monitoramento e Observabilidade
11. Riscos e Mitigações
12. Custos Estimados
13. Roadmap de Implementação

---

## Referências Disponíveis

### architecture-patterns.md
Explica os principais padrões arquiteturais:
- Monolithic Architecture
- Microservices Architecture
- Event-Driven Architecture
- Serverless / FaaS
- Layered Architecture (N-Tier)
- Hexagonal Architecture
- CQRS
- Event Sourcing
- Space-Based Architecture
- SOA

### tech-stack-guide.md
Guia para escolha de tecnologias:
- Backend Frameworks (Node.js, Go, Python, Java, C#)
- Bancos de Dados (SQL e NoSQL)
- Message Brokers
- Frontend Frameworks
- Infraestrutura (Kubernetes, Docker Swarm, Nomad)
- Serverless Platforms

---

## Critérios de Qualidade

Um bom plano de arquitetura gerado por estas skills deve:

1. ✅ **Responder ao problema real** - Alinhado com requisitos
2. ✅ **Justificar decisões** - Trade-offs documentados
3. ✅ **Ser validado** - Sem halucinações ou tecnologias inventadas
4. ✅ **Ser acionável** - Time consegue implementar
5. ✅ **Ser observável** - Monitoramento e debugging planejados
6. ✅ **Ser economicamente viável** - Custos dentro do budget
7. ✅ **Ser evolutivo** - Caminho claro para crescimento

---

## Contribuindo

Para adicionar novos padrões, tecnologias ou melhorar os templates:

1. Editar os arquivos em `references/`
2. Atualizar `assets/architecture-template.md`
3. Adicionar novos scripts em `scripts/`
4. Documentar mudanças no `README.md`

---

## Licença

Estas skills são parte do projeto e seguem a mesma licença.
