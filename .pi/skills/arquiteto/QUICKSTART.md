# Guia Rápido - Skills do Arquiteto

## Comandos Rápidos

### Gerar Nova Arquitetura
```
/skill:arquiteto --novo "Sistema de X com Y usuários, recursos A, B, C"
```

### Comparar Tecnologias
```
/skill:arquiteto-pesquisa-tecnica compare "PostgreSQL" "MongoDB"
```

### Validar Documento
```
/skill:arquiteto-anti-halucinacao validate docs/arquitetura.md
```

### Verificar Tecnologia Específica
```
/skill:arquiteto-anti-halucinacao check "Next.js:14"
```

## Checklist Simplificado

### Para Gerar Arquitetura
1. Compreender o problema (domínio, usuários, requisitos)
2. Definir requisitos funcionais e não-funcionais
3. Selecionar stack tecnológico
4. Desenhar arquitetura de componentes
5. Planejar arquitetura de dados
6. Definir segurança
7. Planejar deploy e infraestrutura
8. Documentar riscos e custos

### Para Validar Arquitetura
- [ ] Tecnologias existem?
- [ ] Versões foram lançadas?
- [ ] Features existem?
- [ ] Compatibilidade confirmada?
- [ ] Padrões aplicáveis?
- [ ] Evidências documentadas?

## Stacks Comuns

### Startup MVP
- Frontend: Next.js + TailwindCSS
- Backend: Node.js + NestJS
- DB: PostgreSQL + Supabase
- Auth: Clerk/NextAuth
- Deploy: Vercel

### High-Scale API
- Frontend: React/Next.js
- Backend: Go + gRPC
- DB: PostgreSQL + Redis
- MQ: Kafka/NATS
- Deploy: Kubernetes

### Enterprise Java
- Frontend: React + TypeScript
- Backend: Java + Spring Boot
- DB: PostgreSQL + Redis
- Deploy: Kubernetes + AWS

## Referências Úteis

- `.pi/skills/arquiteto/README.md` - Documentação completa
- `.pi/skills/arquiteto/references/` - Guias e padrões
- `.pi/skills/arquiteto/examples/` - Exemplos de uso

## Workflow Completo

```
1. /skill:arquiteto --novo "projeto"
   ↓
2. /skill:arquiteto-pesquisa-tecnica compare "tech A" "tech B"
   ↓
3. /skill:arquiteto-anti-halucinacao validate docs/arquitetura.md
   ↓
4. Corrigir problemas
   ↓
5. /skill:arquiteto-anti-halucinacao validate docs/arquitetura-v2.md
   ↓
6. Aprovado! Implementar
```

## Scripts Úteis

```bash
# Gerar documento inicial
./.pi/skills/arquiteto/scripts/generate-architecture-doc.sh meu-projeto docs

# Validar seções do documento
./.pi/skills/arquiteto/scripts/validate-architecture.sh docs/arquitetura.md

# Verificar tecnologia
./.pi/skills/arquiteto-anti-halucinacao/scripts/validate-tech.sh Prisma 5.0
```

## Critérios de Qualidade

Um bom plano de arquitetura:
- ✅ Responde ao problema real
- ✅ Justifica decisões
- ✅ É validado (sem halucinações)
- ✅ É acionável
- ✅ É observável
- ✅ É economicamente viável
- ✅ É evolutivo

## Lembrete

**SEMPRE** valide o documento com `/skill:arquiteto-anti-halucinacao` antes de considerar completo!
