# Plano de Arquitetura - [Nome do Projeto]

**Versão:** 1.0  
**Data:** {DATE}  
**Arquiteto:** {AUTOR}  
**Status:** Proposto | Em Revisão | Aprovado

---

## 1. Visão Geral

### 1.1 Resumo Executivo
[2-3 parágrafos descrevendo o sistema, seu propósito e principais características]

### 1.2 Objetivos de Negócio
- [Objetivo 1]
- [Objetivo 2]
- [Objetivo 3]

### 1.3 Escopo
**Inclui:**
- [Feature 1]
- [Feature 2]

**Exclui (futuro):**
- [Feature 3]
- [Feature 4]

---

## 2. Requisitos Funcionais

### 2.1 Usuários e Papéis
| Papel | Descrição | Permissões Principais |
|-------|-----------|----------------------|
| Admin | Administrador do sistema | CRUD completo |
| User  | Usuário final | Leitura e criação |

### 2.2 Funcionalidades Principais
| ID | Funcionalidade | Descrição | Prioridade |
|----|---------------|-----------|------------|
| RF01 | [Feature 1] | [Descrição] | Alta |
| RF02 | [Feature 2] | [Descrição] | Alta |
| RF03 | [Feature 3] | [Descrição] | Média |

### 2.3 Regras de Negócio
- **RN-001:** [Regra 1]
- **RN-002:** [Regra 2]

---

## 3. Requisitos Não-Funcionais

### 3.1 Performance
| Métrica | Target | Observação |
|---------|--------|------------|
| Latência (p95) | < 200ms | APIs principais |
| Throughput | 10k req/s | Pico esperado |
| Tempo de resposta | < 2s | Operações CRUD |

### 3.2 Escalabilidade
| Recurso | Curto Prazo (6m) | Médio Prazo (1a) | Longo Prazo (3a) |
|---------|------------------|------------------|------------------|
| Usuários | 10k | 100k | 1M |
| Dados | 100GB | 1TB | 10TB |
| Requests/s | 100 | 1k | 10k |

### 3.3 Disponibilidade
- **SLA Alvo:** 99.9% (8.76h downtime/ano)
- **RPO:** 1 hora (máximo dados perdidos)
- **RTO:** 4 horas (tempo máximo recuperação)

### 3.4 Segurança
- Autenticação: [OAuth 2.0 / JWT / SAML]
- Autorização: [RBAC / ABAC]
- Criptografia: TLS 1.3 em trânsito, AES-256 em repouso
- Compliance: [LGPD / SOC2 / PCI-DSS]

### 3.5 Observabilidade
- Logs: Estruturados (JSON), centralizados
- Métricas: Prometheus + Grafana
- Traces: OpenTelemetry + Jaeger
- Alertas: PagerDuty para críticos

---

## 4. Stack Tecnológico

### 4.1 Frontend
| Camada | Tecnologia | Versão | Justificativa |
|--------|-----------|--------|---------------|
| Framework | [Ex: Next.js] | [14.x] | [Razão] |
| UI Library | [Ex: shadcn/ui] | [latest] | [Razão] |
| State | [Ex: Zustand] | [latest] | [Razão] |

### 4.2 Backend
| Camada | Tecnologia | Versão | Justificativa |
|--------|-----------|--------|---------------|
| Runtime | [Ex: Node.js] | [20.x LTS] | [Razão] |
| Framework | [Ex: NestJS] | [10.x] | [Razão] |
| ORM | [Ex: Prisma] | [5.x] | [Razão] |

### 4.3 Dados
| Tipo | Tecnologia | Versão | Caso de Uso |
|------|-----------|--------|-------------|
| Primary DB | [PostgreSQL] | [16.x] | Dados transacionais |
| Cache | [Redis] | [7.x] | Session, cache |
| Search | [Elasticsearch] | [8.x] | Busca textual |

### 4.4 Infraestrutura
| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| Hosting | [Vercel/AWS] | [Razão] |
| Container | [Docker] | [Razão] |
| Orchestration | [Kubernetes] | [Razão] |
| CI/CD | [GitHub Actions] | [Razão] |

### 4.5 Serviços Externos
| Serviço | Provider | Uso |
|---------|----------|-----|
| Auth | [Auth0/Clerk] | Autenticação |
| Storage | [S3/R2] | Arquivos estáticos |
| Email | [Resend/SendGrid] | Notificações |

---

## 5. Arquitetura de Componentes

### 5.1 Diagrama de Alto Nível
```
[Cliente Web/Mobile]
        ↓
[API Gateway / Load Balancer]
        ↓
┌────────────────────────────────┐
│   Application Layer (Backend)  │
│  ┌────────┐  ┌────────┐       │
│  │  Auth  │  │  API   │       │
│  │ Service│  │ Routes │       │
│  └────────┘  └────────┘       │
└────────────────────────────────┘
        ↓
┌────────────────────────────────┐
│    Domain Layer (Business)     │
│  ┌────────┐  ┌────────┐       │
│  │ Models │  │ Logic  │       │
│  └────────┘  └────────┘       │
└────────────────────────────────┘
        ↓
┌────────────────────────────────┐
│  Infrastructure Layer (Data)   │
│  ┌─────┐  ┌─────┐  ┌─────┐   │
│  │ DB  │  │Cache│  │ MQ  │   │
│  └─────┘  └─────┘  └─────┘   │
└────────────────────────────────┘
```

### 5.2 Componentes Principais

#### API Gateway
**Responsabilidade:** Roteamento, rate limiting, auth
**Tecnologia:** [Nginx/Kong/AWS API Gateway]
**Ports:** 443 (HTTPS)

#### Auth Service
**Responsabilidade:** Autenticação e autorização
**Tecnologia:** [NextAuth/Clerk/Auth0]
**Endpoints:**
- POST /auth/login
- POST /auth/logout
- POST /auth/refresh

#### API Services
**Responsabilidade:** Lógica de negócio, CRUD
**Tecnologia:** [NestJS/Express/FastAPI]
**Modules:**
- Users Module
- Products Module
- Orders Module

---

## 6. Arquitetura de Dados

### 6.1 Modelo de Dados

#### Entidades Principais
```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- [Outras tabelas principais]
```

### 6.2 Relacionamentos
```
Users (1) ─< (N) Orders
Products (1) ─< (N) OrderItems
Categories (1) ─< (N) Products
```

### 6.3 Estratégias de Dados

#### Partitioning
- [Tabela] partitioned by [data/time]
- Razão: [Motivo]

#### Indexing
- Índice em [coluna] para [query]
- Índice composto em [colunas] para [query]

#### Caching
- Cache de [dados] com TTL de [tempo]
- Cache strategy: [cache-aside/write-through]

### 6.4 Migração de Dados
- Ferramenta: [Prisma Migrate / Flyway / Alembic]
- Estratégia: [Zero-downtime migrations]

---

## 7. Integrações

### 7.1 APIs Externas
| API | Propósito | Autenticação | Rate Limit |
|-----|-----------|--------------|------------|
| [Ex: Stripe] | Pagamentos | API Key | 100 req/s |
| [Ex: SendGrid] | Email | API Key | 100 req/s |

### 7.2 Webhooks
| Evento | Payload | Handler |
|--------|---------|---------|
| payment.success | JSON | /webhooks/stripe |
| user.created | JSON | /webhooks/auth |

### 7.3 Message Broker (se aplicável)
- **Tecnologia:** [RabbitMQ/Kafka/Redis]
- **Topics/Queues:**
  - `user.created` → [consumers]
  - `order.paid` → [consumers]

---

## 8. Segurança

### 8.1 Autenticação
- **Método:** [JWT/OAuth 2.0/SAML]
- **Provider:** [Auth0/Clerk/NextAuth]
- **Token Lifetime:** 15 min (access), 7 days (refresh)

### 8.2 Autorização
- **Model:** [RBAC/ABAC]
- **Roles:** Admin, User, Guest
- **Permissions:** [resource:action]

### 8.3 Proteção de Dados
- **Em trânsito:** TLS 1.3
- **Em repouso:** AES-256
- **Sensitive fields:** Criptografados no DB
- **PII:** Masking em logs

### 8.4 Rate Limiting
| Endpoint | Limit | Window |
|----------|-------|--------|
| /api/* | 100 req | 1 min |
| /api/auth/* | 10 req | 1 min |

### 8.5 DDoS Protection
- [Cloudflare/AWS Shield]
- Rate limiting por IP
- CAPTCHA em endpoints sensíveis

---

## 9. Deploy e Infraestrutura

### 9.1 Ambientes
- **Development:** Local (Docker Compose)
- **Staging:** [Cloud/Kubernetes]
- **Production:** [Cloud/Kubernetes]

### 9.2 CI/CD Pipeline
```
1. Push to main
   ↓
2. Run tests (pytest, jest)
   ↓
3. Build Docker images
   ↓
4. Push to registry
   ↓
5. Deploy to Staging
   ↓
6. Run integration tests
   ↓
7. Manual approval (production)
   ↓
8. Deploy to Production
   ↓
9. Smoke tests
   ↓
10. Monitor alerts
```

### 9.3 Estratégia de Deploy
- **Strategy:** [Blue-Green/Canary/Rolling]
- **Rollback:** Automático em falha
- **Zero-downtime:** Sim

### 9.4 Backup e Disaster Recovery
- **Backup Frequency:** Diário (incremental), Semanal (full)
- **Retention:** 30 dias
- **Location:** [S3/GCS] + cross-region
- **RPO:** 1 hora
- **RTO:** 4 horas

---

## 10. Monitoramento e Observabilidade

### 10.1 Métricas Principais
| Categoria | Métrica | Alert |
|-----------|---------|-------|
| Performance | p95 latency | > 500ms |
| Errors | Error rate | > 1% |
| Infra | CPU usage | > 80% |
| Infra | Memory usage | > 85% |
| Business | Orders/min | < 10 |

### 10.2 Logs
- **Format:** JSON estruturado
- **Centralização:** [Loki/ELK/CloudWatch]
- **Retention:** 30 dias

### 10.3 Dashboards
- [Dashboa
