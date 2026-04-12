---
name: arquiteto-pesquisa-tecnica
description: Pesquisa informações técnicas na internet para validar decisões arquiteturais, encontrar melhores práticas, comparar tecnologias e descobrir exemplos reais de uso em produção. Use quando precisar de dados técnicos atualizados.
allowed-tools:
  - read
  - grep
  - find
  - bash
---

# Skill: Pesquisa Técnica para Arquitetura

## 🎯 Propósito

Realizar **pesquisas técnicas estratégicas** para validar decisões arquiteturais, encontrar melhores práticas, comparar tecnologias e descobrir exemplos reais de uso em produção.

## 📋 Quando Usar Esta Skill

Use esta skill quando:
- Precisar comparar tecnologias ou frameworks
- Quiser encontrar melhores práticas para um padrão arquitetural
- Precisar validar uma decisão arquitetural com fontes externas
- Quiser descobrir como empresas resolvem problemas similares
- Precisar de informações atualizadas sobre tecnologias
- Quiser encontrar benchmarks ou estudos de caso

---

## 🔍 Tipos de Pesquisa

### 1. Comparação de Tecnologias
```bash
/skill:arquiteto-pesquisa-tecnica compare "<tecnologia A>" "<tecnologia B>"
```

**Exemplo:**
```bash
/skill:arquiteto-pesquisa-tecnica compare "PostgreSQL" "MongoDB" para time-series
```

Retorna:
- Tabela comparativa de features
- Pontos fortes/fracos de cada
- Casos de uso ideais
- Exemplos de empresas que usam
- Referências de produção

---

### 2. Melhores Práticas
```bash
/skill:arquiteto-pesquisa-tecnica best-practices "<padrão/arquitetura>"
```

**Exemplo:**
```bash
/skill:arquiteto-pesquisa-tecnica best-practices "microservices communication"
```

Retorna:
- Padrões recomendados
- Anti-padrões comuns
- Implementações de referência
- Artigos de autoridades (Martin Fowler, etc)
- Exemplos reais

---

### 3. Validação de Decisão
```bash
/skill:arquiteto-pesquisa-tecnica validate "<decisão arquitetural>"
```

**Exemplo:**
```bash
/skill:arquiteto-pesquisa-tecnica validate "Usar GraphQL para API pública de e-commerce"
```

Retorna:
- Artigos pró/contra
- Experiências de quem usou
- Problemas conhecidos
- Alternativas comuns
- Veredito baseado em evidências

---

### 4. Busca de Exemplos em Produção
```bash
/skill:arquiteto-pesquisa-tecnica production "<tecnologia/padrão>"
```

**Exemplo:**
```bash
/skill:arquiteto-pesquisa-tecnica production "Event Sourcing com Kafka"
```

Retorna:
- Empresas que usam
- Engineering blogs
- Arquiteturas descritas
- Scale e desafios
- Lições aprendidas

---

### 5. Benchmarks e Performance
```bash
/skill:arquiteto-pesquisa-tecnica benchmark "<tecnologia>"
```

**Exemplo:**
```bash
/skill:arquiteto-pesquisa-tecnica benchmark "Redis vs Memcached"
```

Retorna:
- Benchmarks técnicos
- Testes de performance
- Limitações de escala
- Casos de borda
- Recomendações

---

### 6. Pesquisa de Problemas Específicos
```bash
/skill:arquiteto-pesquisa-tecnica search "<problema ou dúvida>"
```

**Exemplo:**
```bash
/skill:arquiteto-pesquisa-tecnica search "Como lidar com transações distribuídas em microservices"
```

Retorna:
- Soluções propostas
- Padrões aplicáveis (SAGA, 2PC, etc)
- Implementações reais
- Trade-offs documentados

---

## 📊 Metodologia de Pesquisa

### Fase 1: Definição da Query

**Query deve ser:**
- Específica (não genérica)
- Incluir termos técnicos relevantes
- Mencionar contexto quando necessário
- Usar inglês para melhor resultados

**Exemplos:**
- ❌ "banco de dados rápido"
- ✅ "PostgreSQL vs MongoDB time-series performance benchmark 2024"
- ❌ "microservices"
- ✅ "microservices communication patterns asynchronous event-driven"

---

### Fase 2: Busca em Fontes Confiáveis

#### Fontes Prioritárias (buscar nestas ordem)

1. **Documentação Oficial**
   - docs.tech.com
   - developer.tech.com
   - Repositórios oficiais

2. **Referências Técnicas**
   - martinfowler.com
   - highscalability.com
   - architecture centers (AWS, Azure, GCP)

3. **Engineering Blogs**
   - engineering.atscale.com
   - Uber Engineering Blog
   - Netflix Tech Blog
   - Airbnb Engineering

4. **Discussões Técnicas**
   - Stack Overflow (respostas aceitas, high votes)
   - Reddit (r/programming, r/devops, r/architecture)

5. **Blogs de Referência**
   - The New Stack
   - InfoQ
   - DZone (com filtragem)

---

### Fase 3: Triagem de Resultados

Para cada resultado encontrado, avaliar:

- **Data:** Mais recente que 2 anos (exceto conceitos atemporais)
- **Autor:** Fonte confiável, autor reconhecido
- **Conteúdo:** Técnico, específico, com evidências
- **Referências:** Cita fontes, links para docs

**Critérios de exclusão:**
- Posts sem data
- Blogs pessoais sem autoridade
- Conteúdo promocional/viés comercial
- Afirmações sem evidências

---

### Fase 4: Síntese e Documentação

Criar relatório com:

```markdown
## Pesquisa: [Título]

**Query:** [query usada]
**Data:** YYYY-MM-DD
**Fontes:** N resultados de M fontes

### Resumo Executivo
[2-3 parágrafos com descobertas principais]

### Descobertas por Categoria

#### Categoria 1
- **Ponto:** [descoberta]
- **Fonte:** [URL]
- **Data:** [YYYY-MM-DD]
- **Confiança:** Alta/Média/Baixa

#### Categoria 2
...

### Casos de Produção

#### Empresa A
- **Stack:** [tecnologias]
- **Scale:** [usuários, req/seg]
- **Arquitetura:** [resumo]
- **Fonte:** [URL]

### Recomendações

1. **Baseado em evidências:** [recomendação]
2. **Com ressalvas:** [recomendação + condições]
3. **Evitar:** [não recomendado + motivo]

### Referências

1. [Título] - [URL] - [Data]
2. ...
```

---

## 🎯 Matriz de Qualidade de Fontes

| Tipo de Fonte | Confiança | Prioridade | Nota |
|---------------|-----------|------------|------|
| Docs oficial tech.com | 🔴 Alta | 1 | Sempre verificar |
| Repositório oficial GitHub | 🔴 Alta | 1 | Issues/Discussions |
| Martin Fowler | 🔴 Alta | 1 | Padrões atemporais |
| Engineering blog (Big Tech) | 🟠 Média-Alta | 2 | Experiência real |
| Architecture Centers (AWS/GCP) | 🟠 Média-Alta | 2 | Guias práticos |
| High Scalability | 🟠 Média-Alta | 2 | Arquiteturas reais |
| Stack Overflow (aceita, >50 votes) | 🟡 Média | 3 | Consenso da comunidade |
| Reddit (r/programming, top) | 🟡 Média | 3 | Discussões |
| Blogs pessoais (autor reconhecido) | 🟡 Média | 3 | Opinião experiente |
| DZone/InfoQ (artigos com data) | 🟢 Média-Baixa | 4 | Variável |
| Blogs pessoais (sem autor) | 🔴 Baixa | 5 | Desconfiar |

---

## 🛠️ Scripts Auxiliares

### search-tech.sh
```bash
./scripts/search-tech.sh "<query>" [sources]
```

Busca em múltiplas fontes e retorna resultados consolidados.

### compare-tech.sh
```bash
./scripts/compare-tech.sh "<tech A>" "<tech B>"
```

Gera tabela comparativa com features, pros/cons, casos de uso.

### find-production.sh
```bash
./scripts/find-production.sh "<tecnologia>"
```

Busca casos de uso em produção por empresas reais.

---

## 📚 Tópicos Comuns de Pesquisa

### Bancos de Dados
- PostgreSQL vs MySQL vs MariaDB
- SQL vs NoSQL (PostgreSQL vs MongoDB)
- Time-series: TimescaleDB vs InfluxDB
- Vector databases: Pinecone vs pgvector vs Weaviate

### Message Queues
- Kafka vs RabbitMQ vs Redis Pub/Sub
- NATS vs RabbitMQ
- Pulsar vs Kafka

### Caches
- Redis vs Memcached
- CDNs: Cloudflare vs CloudFront vs Fastly

### API Styles
- REST vs GraphQL vs gRPC
- GraphQL Federation vs Apollo Gateway

### Auth/Security
- JWT vs Session-based auth
- OAuth 2.0 vs OpenID Connect
- Password hashing: bcrypt vs argon2

### Microservices Patterns
- API Gateway vs BFF
- Service Mesh: Istio vs Linkerd
- Database per Service vs Shared Database

### Deployment
- Kubernetes vs Nomad vs Docker Swarm
- Serverless: Lambda vs Cloud Functions vs Cloud Run
- PaaS: Heroku vs Render vs Railway

### Frontend
- React vs Vue vs Svelte
- Next.js vs Remix vs Astro
- State Management: Redux vs Zustand vs Jotai

---

## ⚠️ Cuidados na Pesquisa

### Evite

❌ Confirmation bias - buscar apenas fontes que confirmam opinião prévia
❌ Fontes desatualizadas - artigos > 2 anos para tecnologias fast-moving
❌ Viés comercial - artigos patrocinados por vendors
❌ Anedotas sem dados - "funcionou pra mim" sem métricas

### Pratique

✅ Buscar múltiplas perspectivas
✅ Verificar datas das fontes
✅ Cross-reference claims
✅ Priorizar ev
