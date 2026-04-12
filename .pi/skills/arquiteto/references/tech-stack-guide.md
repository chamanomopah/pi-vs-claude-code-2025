# Guia de Seleção de Stack Tecnológico

Guia para escolher tecnologias baseado em requisitos e restrições do projeto.

## Framework de Decisão

Use este framework para decidir tecnologias:

1. **Requisitos Funcionais** - O que precisa ser construído?
2. **Requisitos Não-Funcionais** - Performance, escala, disponibilidade
3. **Restrições** - Budget, time, skills, compliance
4. **Trade-offs** - O que você está disposto a sacrificar?

---

## Backend Frameworks

### Node.js / TypeScript

#### Opções: NestJS, Fastify, Express

**Prós:**
- TypeScript nativo
- Ecossistema NPM enorme
- Bom para I/O bound
- Time fullstack JavaScript

**Contras:**
- Single-threaded (CPU bound bottleneck)
- Event loop blocking
- Memory leaks potenciais

**Melhor para:**
- APIs REST/GraphQL
- Real-time (WebSockets, SSE)
- Microservices leves
- Times fullstack JS

**Evitar para:**
- CPU-intensive tasks
- Sistemas críticos com requisitos hard real-time

---

### Go

#### Opções: Gin, Echo, Fiber

**Prós:**
- Performance alta
- Concorrência simples (goroutines)
- Binary único para deploy
- Memory efficiency

**Contras:**
- Ecossistema menor que Node/Python
- Error handling verbose
- Menor quantidade de libs

**Melhor para:**
- APIs de alta performance
- Microservices
- CLIs e ferramentas
- Sistemas distribuídos

**Evitar para:**
- Prototipagem rápida
- Times sem experiência Go

---

### Python

#### Opções: FastAPI, Django, Flask

**Prós:**
- Rápido desenvolvimento
- Ecossistema ML/AI maduro
- Leitura fácil
- Bom para scripts/automação

**Contras:**
- Performance menor que Go/Java
- GIL limita paralelismo
- Deploy mais complexo (dependencies)

**Melhor para:**
- ML/AI/Data Science
- Prototipagem rápida
- Automação e scripts
- APIs internas

**Evitar para:**
- High-throughput APIs (>10k RPS)
- Sistemas com requisitos performance críticos

---

### Java / Kotlin

#### Opções: Spring Boot, Quarkus, Micronaut

**Prós:**
- Ecossistema enterprise maduro
- Performance consistente
- Type safety forte
- Multithreading robusto

**Contras:**
- Verbosidade (Java)
- Startup lento (Spring)
- Memory footprint alto

**Melhor para:**
- Enterprise applications
- Sistemas críticos
- Times Java existentes
- Microservices (Quarkus/Micronaut)

**Evitar para:**
- Serverless (cold starts)
- Prototipagem rápida
- Startups com time pequeno

---

### C# / .NET

#### Opções: ASP.NET Core

**Prós:**
- Performance alta
- Tooling excelente (Visual Studio)
- Ecossistema Microsoft
- Multiplataforma (.NET Core+)

**Contras:**
- Vendor lock-in potencial (Azure)
- Menor que Node/Python communities
- Windows-centric (ainda)

**Melhor para:**
- Enterprises Microsoft
- Times C# existentes
- Windows workloads
- Gaming (Unity backend)

**Evitar para:**
- Startups sem stack Microsoft
- Time focado em open-source

---

## Bancos de Dados

### SQL (Relacional)

#### PostgreSQL

**Prós:**
- Open-source, community-driven
- Features avançadas (JSON, arrays, etc)
- Extensível (PostGIS, pgvector)
- ACID compliant

**Contras:**
- Escala vertical limitada
- Sharding complexo
- Schema migrations necessárias

**Melhor para:**
- Dados estruturados
- Relações complexas
- Transações ACID necessárias
- GIS/Geospatial (PostGIS)

**Use cases:**
- E-commerce
- SaaS multi-tenant
- Financeiro
- CMS

---

#### MySQL / MariaDB

**Prós:**
- Ubiquity (muito usado)
- Performance boa
- Replicação simples
- Cloud managed (RDS, Cloud SQL)

**Contras:**
- Features menos que PostgreSQL
- JSON menos maduro
- Menos extensível

**Melhor para:**
- Web apps tradicionais
- Times MySQL existentes
- Simples CRUD apps

---

### NoSQL (Document)

#### MongoDB

**Prós:**
- Schema flexível
- Escala horizontal simples
- JSON nativo
- Developer-friendly

**Contras:**
- JOINs limitados ($lookup)
- Transações limitadas
- Size limits documentos (16MB)
- Memory usage alto

**Melhor para:**
- Dados semi-estruturados
- Prototipação rápida
- Catalogos, inventários
- Real-time analytics (simples)

**Use cases:**
- CMS headless
- Catalogs de produtos
- Event logs
- User profiles

---

### NoSQL (Key-Value)

#### Redis

**Prós:**
- Performance extrema (in-memory)
- Data structures ricas
- Pub/Sub, streams
- Simples de usar

**Contras:**
- Memory expensive
- Persistência assíncrona (RDB/AOF)
- Size limitado por RAM

**Melhor para:**
- Cache (sessões, queries)
- Rate limiting
- Leaderboards, counters
- Message broker leve
- Real-time analytics

---

### NoSQL (Wide-Column)

#### Cassandra / ScyllaDB

**Prós:**
- Escala linear horizontal
- Sem SPOF
- Writes muito rápidos
- Multi-master

**Contras:**
- Data modeling complexo
- Queries limitadas
- CQL limitado vs SQL
- Operações complexas

**Melhor para:**
- Time-series
- High write throughput
- Multi-DC
- IoT

---

### NoSQL (Search)

#### Elasticsearch / OpenSearch

**Prós:**
- Full-text search excelente
- Analytics poderosos
- Escala horizontal
- JSON APIs

**Contras:**
- Resource intensive
- Complexo de operar
- Consistency eventual
- Search learning curve

**Melhor para:**
- Search engines
- Logging analytics (ELK)
- E-commerce search
- Analytics dashboards

---

### Time-Series

#### TimescaleDB (PostgreSQL extension)
**Prós:** SQL familiar, extensão PostgreSQL, funções time-series
**Contras:** Baseado em PG (limites PG)

#### InfluxDB
**Prós:** Purpose-built, Flux language poderoso
**Contras:** Proprietary features, learning curve

---

### Vector (AI/ML)

#### pgvector (PostgreSQL)
**Prós:** SQL familiar, extensão PG
**Contras:** Performance menor que soluções nativas

#### Pinecone / Weaviate / Qdrant
**Prós:** Purpose-built, performance alta
**Contras:** SaaS vendor lock-in, adicional infrastructure

---

## Message Brokers

### RabbitMQ

**Prós:**
- Mensagens confiáveis
- Flexível (exchanges, queues)
- Management UI excelente
- Protocol AMQP

**Contras:**
- Escala horizontal complexa
- Memory usage
- Single node bottleneck (sem cluster)

**Melhor para:**
- Workflows confiáveis
- Complex routing
- Enterprise messaging

---

### Apache Kafka

**Prós:**
- Alta throughput
- Escala horizontal nativa
- Log-based (replayable)
- Streams (Kafka Streams)

**Contras:**
- Complexo de operar
- Learning curve steep
- Overhead para casos simples
- Zookeeper/KRaft necessário

**Melhor para:**
- Event streaming
- Data pipelines
- Event sourcing
- Microservices events

---

### NATS

**Prós:**
- Leve, simples
- Performance alta
- JetStream (persistence)
- Multi-messaging patterns

**Contras:**
- Ecossistema menor que Kafka
- Menos enterprise features

**Melhor para:**
- Microservices leves
- Edge computing
- IoT
- Simples pub/sub

---

### Redis Pub/Sub / Streams

**Prós:**
- Já usa Redis (infra existente)
- Simples de usar
- Performance alta

**Contras:**
- Limitado vs Kafka/RabbitMQ
- Reliability menor
- Persistence configurável

**Melhor para:**
- Simple pub/sub
- Real-time updates
- Small-scale streaming

---

## Frontend Frameworks

### React

**Prós:**
- Ecossistema maior
- Flexibilidade (library não framework)
- Next.js, Remix, Gatsby
- HUGE community

**Contras:**
- Boilerplate sem framework adicional
- State management manual
- "Decision fatigue"

**Melhor para:**
- Web apps complexas
- Times React experientes
- Need de flexibilidade

---

### Vue

**Prós:**
- Curva de aprendizado suave
- Single-file components
- Performance boa
- DX excelente

**Contras:**
- Comunidade menor que React
- Menos empresas usando

**Melhor para:**
- Times novos em SPA
- Prototipagem rápida
- Apps não-críticas

---

### Svelte

**Prós:**
- Sem runtime virtual DOM
- Bundle size pequeno
- Sintaxe declarativa
- Performance excelente

**Contras:**
- Ecossistema menor
- Menos empresas
- Tooling menos maduro

**Melhor para:**
- Performance crítico
- Bundle size importante
- Apps clientes corporativos

---

### Angular

**Prós:**
- Framework completo (batteries included)
- TypeScript first
- Enterprise-friendly
- CLI excelente

**Contras:**
- Verboso
- Bundle size maior
- Curva de aprendizado
- Menos flexível que React

**Melhor para:**
- Enterprises
- Times TypeScript
- Apps large-scale
- Governança forte necessária

---

## Next.js vs Remix vs Astro

### Next.js

**Pró
