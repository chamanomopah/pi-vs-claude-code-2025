# Exemplo de Uso das Skills do Arquiteto

Este exemplo demonstra como usar as skills do arquiteto para criar um plano de arquitetura completo e validado.

## Cenário

Você precisa criar a arquitetura para um **marketplace de produtos digitais** com os seguintes requisitos:

- 100.000 usuários esperados no primeiro ano
- 10.000 produtos cadastrados
- 5.000 transações por dia no pico
- Upload/download de arquivos (até 500MB)
- Sistema de reviews e ratings
- Dashboard de vendas para vendedores

---

## Passo 1: Gerar Arquitetura Inicial

```bash
/skill:arquiteto --novo "Marketplace de produtos digitais com 100k usuários, suporte a upload/download de arquivos até 500MB, sistema de reviews e dashboard de vendas"
```

**Resultado:** O agente gera um documento de arquitetura completo usando o template, incluindo:

- Stack tecnológico recomendado (Next.js + Node.js + PostgreSQL + S3)
- Arquitetura de componentes (API Gateway, Auth Service, Product Service, etc)
- Arquitetura de dados (modelos de entidades, relacionamentos)
- Estratégia de segurança (JWT, RBAC, criptografia)
- Plano de deploy (Vercel + AWS RDS + S3)
- Estimativa de custos

---

## Passo 2: Pesquisar Tecnologias Específicas

Durante a geração, você pode ter dúvidas sobre decisões específicas. Use a skill de pesquisa:

### Comparar Bancos de Dados
```bash
/skill:arquiteto-pesquisa-tecnica compare "PostgreSQL" "MongoDB" para marketplace com produtos digitais
```

**Resultado:** Tabela comparativa mostrando que PostgreSQL é melhor para:
- Relações complexas (produtos, categorias, reviews)
- Transações ACID necessárias para pagamentos
- JSON fields para atributos flexíveis

### Melhores Práticas para Upload de Arquivos
```bash
/skill:arquiteto-pesquisa-tecnica best-practices "file upload large files S3 presigned URLs"
```

**Resultado:** 
- Usar presigned URLs para upload direto ao S3
- Implementar upload multipart para arquivos grandes
- Adicionar vírus scanning com Lambda@Edge

### Exemplos em Produção
```bash
/skill:arquiteto-pesquisa-tecnica production "marketplace digital products architecture"
```

**Resultado:** Casos de empresas como:
- Gumroad (stack: Rails + PostgreSQL + S3)
- Etsy (stack: PHP + PostgreSQL + Kafka)
- Itch.io (stack: Node.js + PostgreSQL + S3)

---

## Passo 3: Validar Documento (CRÍTICO!)

```bash
/skill:arquiteto-anti-halucinacao validate docs/arquitetura-marketplace.md
```

**Resultado Possível:**

```
=== Relatório de Validação ===

✅ VALIDADO: PostgreSQL 16.0
   - Lançado em: 2023-09-14
   - Fontes: postgresql.org, github.com/postgres/postgres

✅ VALIDADO: Next.js 14
   - Lançado em: 2023-10-25
   - App Router estável
   - Fontes: nextjs.org, github.com/vercel/next.js

⚠️ RESSALVA: Prisma "suporte nativo a PostgreSQL arrays"
   - Prisma suporta arrays, mas requer configuração específica
   - Ver: https://www.prisma.io/docs/concepts/components/prisma-schema/data-model#scalar-lists
   - Documentar no README do projeto

❌ INVÁLIDO: "Next.js 15 com server actions estáveis"
   - Next.js 15 ainda não lançado (documento de 2024)
   - CORREÇÃO: Usar Next.js 14 ou remover versão específica
```

---

## Passo 4: Corrigir Problemas

Com base no relatório, você ajusta o documento:

1. Corrige "Next.js 15" → "Next.js 14"
2. Adiciona nota sobre configuração de arrays no Prisma
3. Documenta as fontes das principais decisões

---

## Passo 5: Re-validar

```bash
/skill:arquiteto-anti-halucinacao validate docs/arquitetura-marketplace-v2.md
```

**Resultado:**

```
=== Relatório de Validação ===

✅ 100% das afirmações validadas
✅ Todas as tecnologias existem e estão ativas
✅ Todas as versões foram lançadas antes da data do documento
✅ Compatibilidades confirmadas
✅ Cada decisão tem pelo menos 1 fonte de evidência

APROVADO PARA IMPLEMENTAÇÃO
```

---

## Documento Final

O documento final de arquitetura (`arquitetura-marketplace-v2.md`) contém:

### Visão Geral
- Marketplace de produtos digitais multi-vendedor
- 100k usuários esperados no primeiro ano
- Stack: Next.js 14 + Node.js + PostgreSQL 16 + S3

### Stack Tecnológico

**Frontend:**
- Next.js 14 (App Router, Server Components)
- shadcn/ui (componentes UI)
- TailwindCSS (estilização)
- Zustand (state management)

**Backend:**
- Node.js 20 LTS
- NestJS 10 (framework)
- Prisma 5 (ORM)
- PostgreSQL 16 (banco de dados)

**Infraestrutura:**
- Vercel (frontend + serverless functions)
- AWS RDS (PostgreSQL gerenciado)
- AWS S3 (armazenamento de arquivos)
- AWS CloudFront (CDN)

**Serviços Externos:**
- Clerk (autenticação)
- Stripe (pagamentos)
- Resend (emails)
- Sentry (monitoramento)

### Arquitetura de Componentes

```
┌─────────────────────────────────────────┐
│         Vercel (Next.js)               │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Web UI    │  │ API Routes       │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      NestJS Backend Services            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Auth    │ │Product  │ │ Order   │   │
│  │ Service │ │ Service │ │ Service │   │
│  └─────────┘ └─────────┘ └─────────┘   │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Data Layer                      │
│  ┌──────────┐  ┌──────────┐           │
│  │PostgreSQL│  │   S3     │           │
│  │(RDS)     │  │(Files)   │           │
│  └──────────┘  └──────────┘           │
└─────────────────────────────────────────┘
```

### Arquitetura de Dados

**Principais Entidades:**
- Users (vendedores e compradores)
- Products (produtos digitais)
- Orders (pedidos)
- OrderItems (itens do pedido)
- Reviews (avaliações)
- Categories (categorias de produtos)

**Relacionamentos:**
```
Users (1) ─< (N) Products (author)
Users (1) ─< (N) Orders (buyer)
Products (1) ─< (N) OrderItems
Orders (1) ─< (N) OrderItems
Products (1) ─< (N) Reviews
Categories (1) ─< (N) Products
```

### Estratégia de Upload de Arquivos

**Flow:**
1. User solicita upload → API gera presigned URL
2. User faz upload direto ao S3 via presigned URL
3. S3 trigger → Lambda para vírus scan
4. Lambda atualiza status no PostgreSQL
5. Notificação via WebSocket ao usuário

**Benefícios:**
- Sem load no servidor de aplicação
- Upload multipart para arquivos grandes
- Vírus scan automático
- Escala horizontal automática

### Custos Estimados

| Item | Custo Mensal (USD) |
|------|-------------------|
| Vercel Pro | $20 |
| AWS RDS (db.t3.medium) | $60 |
| AWS S3 (1TB) | $23 |
| CloudFront | $0.08/GB |
| Clerk Auth | $25 |
| Stripe | 2.9% + $0.30/transação |
| Resend | $20 |
| Sentry | $26 |
| **TOTAL** | **~$200 + transações** |

### Roadmap de Implementação

**Fase 1 - MVP (4 semanas):**
- Autenticação com Clerk
- CRUD de produtos
- Upload/download de arquivos
- Checkout básico com Stripe

**Fase 2 - Beta (4 semanas):**
- Sistema de reviews
- Dashboard de vendas
- Notificações por email
- Search básico

**Fase 3 - Production (4 semanas):**
- Search avançado (PostgreSQL full-text)
- Analytics dashboard
- Rate limiting e segurança
- Monitoramento completo

---

## Referências (Validadas)

1. **PostgreSQL 16** - https://www.postgresql.org/docs/16/ - Acessado em 2024-01-15
2. **Next.js 14** - https://nextjs.org/docs - Acessado em 2024-01-15
3. **Prisma 5** - https://www.prisma.io/docs - Acessado em 2024-01-15
4. **AWS S3 Presigned URLs** - https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html - Acessado em 2024-01-15

---

## Conclusão

Este exemplo demonstra o workflow completo:

1. ✅ Gerar arquitetura com a skill `arquiteto`
2. ✅ Pesquisar dúvidas com `arquiteto-pesquisa-tecnica`
3. ✅ Validar documento com `arquiteto-anti-halucinacao`
4. ✅ Corrigir problemas encontrados
5. ✅ Re-validar até aprovação

O resultado é um plano de arquitetura **robusto, validado e pronto para implementação**.
