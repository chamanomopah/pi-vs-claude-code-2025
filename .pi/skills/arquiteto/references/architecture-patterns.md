# Padrões Arquiteturais Comuns

Referência rápida de padrões arquiteturais para uso em planos de arquitetura.

## 1. Monolithic Architecture

### Descrição
Aplicação single-tier onde a UI, lógica de negócio e dados estão no mesmo códigobase.

### Quando Usar
- Startups validando produto
- Times pequenos (< 5 devs)
- Domínio simples
- Need de time-to-market rápido

### Vantagens
- Simples de desenvolver e testar
- Deploy fácil (single artifact)
- Transações locais simples
- Menor overhead operacional

### Desvantagens
- Escala é vertical (custoso)
- Acoplamento pode crescer
- Dificuldade de isolar falhas
- Tecnologia uniforme

### Tecnologias Comuns
- Backend: Rails, Django, NestJS, Spring Boot
- Frontend: Next.js (SSR), Remix
- DB: PostgreSQL, MySQL

---

## 2. Microservices Architecture

### Descrição
Aplicação dividida em serviços pequenos e independentes comunicando via APIs/mensagens.

### Quando Usar
- Domínios complexos com bounded contexts claros
- Times multi-disciplinares autônomos
- Requisitos de escala heterogêneos
- Need de polyglot programming

### Vantagens
- Escala independente por serviço
- Fault isolation natural
- Deploy independente
- Tecnologia diversificada

### Desvantagens
- Complexidade operacional alta
- Debugging distribuído difícil
- Transações distribuídas
- Network overhead

### Tecnologias Comuns
- API: REST, GraphQL, gRPC
- Messaging: Kafka, RabbitMQ, NATS
- Discovery: Consul, Eureka
- API Gateway: Kong, AWS API Gateway

### Padrões Relacionados
- API Gateway
- Service Discovery
- Circuit Breaker
- Saga (transações distribuídas)
- CQRS
- Event Sourcing

---

## 3. Event-Driven Architecture

### Descrição
Serviços comunicam via eventos, publicando/subscrevendo em message brokers.

### Quando Usar
- Workflows assíncronos
- Integrações entre serviços
- Event sourcing necessário
- Real-time processing

### Vantagens
- Loose coupling
- Alta escalabilidade
- Audit trail natural
- Reactive workflows

### Desvantagens
- Complexidade de debugging
- Event schema evolution
- Eventual consistency
- Saga pattern necessário

### Tecnologias Comuns
- Message Brokers: Kafka, RabbitMQ, NATS, Redis Pub/Sub
- Event Stores: Kafka, EventStoreDB
- CDC: Debezium

### Padrões Relacionados
- Publish-Subscribe
- Event Sourcing
- CQRS
- Saga
- Event Carrier

---

## 4. Serverless / FaaS

### Descrição
Funções executadas sob demanda, sem gerenciamento de servidores.

### Quando Usar
- Event-driven workloads
- Traffic esporádico/imprevisível
- Time-to-market crítico
- Custos operacionais baixos

### Vantagens
- Zero infrastructure management
- Auto-scaling automático
- Pay-per-use
- Rápido time-to-market

### Desvantagens
- Vendor lock-in
- Cold starts
- Execution time limits
- Debugging complexo

### Tecnologias Comuns
- AWS Lambda
- Google Cloud Functions
- Azure Functions
- Cloudflare Workers
- Deno Deploy

---

## 5. Layered Architecture (N-Tier)

### Descrição
Aplicação organizada em camadas horizontais (Presentation, Business, Data).

### Quando Usar
- Aplicações empresariais tradicionais
- Times familiarizados com DDD
- Need de separação clara de responsabilidades

### Vantagens
- Separação de concerns clara
- Testabilidade
- Manutenibilidade
- Padrão bem conhecido

### Desvantagens
- Pode ser overkill para apps simples
- Latência entre camadas
- Pode lead to anemia domain model

### Camadas Típicas
1. Presentation (API, UI)
2. Application (Use cases)
3. Domain (Business logic)
4. Infrastructure (DB, cache)

---

## 6. Hexagonal Architecture (Ports & Adapters)

### Descrição
Domain no centro, adapters externos para DB, APIs, etc.

### Quando Usar
- DDD é prioridade
- Testes de domínio importantes
- Need de flexibilidade de infra

### Vantagens
- Domain isolado de infra
- Testável sem dependências externas
- Flexível para mudanças
- DDD-friendly

### Desvantagens
- Complexidade adicional
- Curva de aprendizado
- Overhead para apps simples

---

## 7. CQRS (Command Query Responsibility Segregation)

### Descrição
Separação entre operações de escrita (Commands) e leitura (Queries).

### Quando Usar
- High read/write ratios
- Diferentes modelos para leitura/escrita
- Performance de leitura crítica
- Event sourcing

### Vantagens
- Otimização independente
- Escala separada
- Performance de leitura
- Fit com event sourcing

### Desvantagens
- Complexidade adicional
- Eventual consistency
- Mais código

### Tecnologias Comuns
- Read DB: PostgreSQL, MongoDB, Elasticsearch
- Write DB: PostgreSQL
- Sync: Debezium (CDC), messaging

---

## 8. Event Sourcing

### Descrição
Estado armazenado como sequência de eventos, não como snapshot atual.

### Quando Usar
- Audit trail crítico
- Need de replay
- Complex business logic
- Temporal queries

### Vantagens
- Audit trail completo
- Replay possibilities
- Temporal queries
- Debugging fácil

### Desvantagens
- Complexidade alta
- Event schema evolution
- Read side queries complexas
- Tooling imaturo

### Tecnologias Comuns
- Event Stores: EventStoreDB, Kafka
- Projections: PostgreSQL, MongoDB

---

## 9. Space-Based Architecture

### Descrição
Multiple instances communicating via shared tuple space (in-memory data grid).

### Quando Usar
- Extreme scalability needs
- Low latency requirements
- Stateful distributed systems

### Vantagens
- Linear scalability
- Low latency
- High availability

### Desvantagens
- Complexidade alta
- Tooling imaturo
- Debugging difícil

### Tecnologias Comuns
- Hazelcast
- Apache Ignite
- Coherence
- Infinispan

---

## 10. SOA (Service-Oriented Architecture)

### Descrição
Serviços reutilizáveis comunicando via enterprise service bus (ESB).

### Quando Usar
- Integrações enterprise complexas
- Reuso de serviços prioritário
- Governança forte

### Vantagens
- Reuso de serviços
- Governança centralizada
- Interoperabilidade

### Desvantagens
- ESB pode ser bottleneck
- Complexidade operacional
- Overhead de orquestração

---

## Matriz de Decisão

| Padrão | Escala | Complexidade | Time-to-Market | Flexibilidade |
|--------|--------|--------------|----------------|---------------|
| Monolith | Baixa | Baixa | Rápido | Baixa |
| Microservices | Alta | Alta | Lento | Alta |
| Event-Driven | Alta | Alta | Médio | Alta |
| Serverless | Média | Média | Rápido | Média |
| Layered | Média | Baixa | Médio | Média |
| Hexagonal | Média | Alta | Médio | Alta |
| CQRS | Alta | Alta | Lento | Alta |
| Event Sourcing | Alta | Muito Alta | Lento | Muito Alta |

---

## Referências

- Martin Fowler: https://martinfowler.com/articles/
- Microsoft Architecture: https://learn.microsoft.com/en-us/azure/architecture/
- AWS Architecture: https://aws.amazon.com/architecture/
- High Scalability: https://highscalability.com/
- Patterns of Enterprise Application Architecture (Martin Fowler)
- Software Architecture: The Hard Parts (N. Ford, et al.)
