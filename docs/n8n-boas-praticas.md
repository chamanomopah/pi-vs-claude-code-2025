# N8N Boas Práticas de Arquitetura

> Documento de referência para arquitetos de workflows n8n
> Última atualização: 2025-04-08

---

## Índice

1. [Split In Batches (Loops)](#1-split-in-batches-loops)
2. [Merge Nodes](#2-merge-nodes)
3. [Loops e Branches Paralelos](#3-loops-e-branches-paralelos)
4. [Fluxo de Dados](#4-fluxo-de-dados)
5. [Padrões de Arquitetura](#5-padrões-de-arquitetura)
6. [Anti-Padrões](#6-anti-padrões)

---

## 1. Split In Batches (Loops)

### Entendendo as Saídas

O Split In Batches é fundamental para processar listas. Ele tem **DUAS saídas**:

#### main[0] - Saída do Loop (Executa 1 vez)
- **Quando executa**: Quando o loop TERMINA (todos itens processados)
- **O que passa**: 1 item com campos especiais
  - `finished`: true
  - `numberOfBatches`: número total de batches
- **Para que serve**: Continuar o fluxo APÓS o loop
- **Como usar**: Conecte ao próximo node do fluxo principal

#### main[1] - Dentro do Loop (Executa N vezes)
- **Quando executa**: Para CADA batch de itens
- **O que passa**: Os itens do batch atual
- **Para que serve**: Processar cada item
- **Como usar**: Conecte aos nodes que processam itens

### Padrão Correto de Loop

```
[Source] → [Split In Batches] → main[1] → [Process] → [Wait] → volta
                               └─ main[0] → [Próximo Passo]
```

**Regras:**
1. main[1] conecta ao processamento
2. Último node do loop DEVE reconectar para Split In Batches
3. Node Wait antes de voltar (evita problemas de sincronização)
4. main[0] conecta ao próximo node APÓS o loop

### Verificação de Lista Vazia

```
[Source] → [IF: Empty?] ──true→ [Skip] → [Fim]
              └─false→ [Split In Batches] → ...
```

**Condição IF:** `{{ $json.items.length === 0 }}`

---

## 2. Merge Nodes

### Modos de Merge

#### Modo "Wait"
- **Comportamento**: Aguarda TODAS as entradas antes de continuar
- **Quando usar**: Sincronizar branches paralelos
- **Regra**: AMBAS as entradas DEVEM estar conectadas

#### Modo "Append"
- **Comportamento**: Combina itens de ambas em uma lista
- **Quando usar**: Juntar resultados de branches

#### Modo "Merge by Key"
- **Comportamento**: Junta dados baseado em campo chave
- **Quando usar**: Combinar dados relacionados

### Regra de Ouro

**NUNCA deixe uma entrada de Merge desconectada no modo Wait!**

```
❌ ERRADO:
  Branch 1 → Merge ──▶ próximo
              (entrada 2 não conectada)

✅ CERTO:
  Branch 1 ──┐
             ├──▶ Merge (Wait) ──▶ próximo
  Branch 2 ──┘
```

---

## 3. Loops e Branches Paralelos

### Evitar Loops Infinitos

```
❌ PERIGO:
[Split] → main[1] → [Process] → volta direto
                       (sem condição de saída!)

✅ SEGURO:
[Split] → main[1] → [Process] → [Wait] → volta
          main[0] → [Próximo]
```

### Sincronização com Wait

```
         ┌─▶ Process A ──┐
Split In ─┤               ├──▶ Wait ──▶ Merge ──▶ volta
         └─▶ Process B ──┘
```

---

## 4. Fluxo de Dados

### Documentação Necessária

Para CADA node, documente:
- Entrada (campos e tipos)
- Saída (campos e tipos)
- Transformações realizadas
- Expressões usadas

### Expressões Comuns

```
{{ $json.campo }}              # Campo do item atual
{{ $json.nested.value }}      # Campo aninhado
{{ $item(0).json.campo }}     # Primeiro item
{{ $json.items.length }}      # Tamanho de array
```

---

## 5. Padrões de Arquitetura

### Padrão 1: Loop Simples

```
[Source] → [Split In Batches] → main[1] → [Process] → [Wait] → volta
                               └─ main[0] → [Próximo]
```

### Padrão 2: Loop com Tratamento de Erro

```
[Split] → main[1] → [Try] → [IF: Success?] ──true→ [Continue]
                              └─false→ [Log Error] → [Merge]
          └─ main[0] → [Fim]
```

### Padrão 3: Branches Paralelos

```
[Split] → main[1] ──┬─▶ [Branch A] ──┐
                   │                ├──▶ [Merge] → [Wait] → volta
                   └─▶ [Branch B] ──┘
```

### Padrão 4: Lista Vazia

```
[Source] → [IF: Empty?] ──true→ [Skip] → [Fim]
              └─false→ [Split] → ...
```

---

## 6. Anti-Padrões

### ❌ Anti-Padrão 1: Loop Sem Reconexão

```
❌ ERRADO:
[Split] → main[1] → [Process] → [Fim]

✅ CERTO:
[Split] → main[1] → [Process] → [Wait] → volta
```

### ❌ Anti-Padrão 2: Merge com Entrada Solta

```
❌ ERRADO:
[Branch 1] → [Merge Wait] → Próximo
  (Branch 2 não conectada!)

✅ CERTO:
[Branch 1] ──┐
             ├──▶ [Merge Wait]
[Branch 2] ──┘
```

### ❌ Anti-Padrão 3: Esquecer main[0]

```
❌ ERRADO:
[Split] → main[1] → [Loop] → volta
  (main[0] não conectada!)

✅ CERTO:
[Split] → main[1] → [Loop] → volta
          main[0] → [Próximo]
```

### ❌ Anti-Padrão 4: Sem Tratar Lista Vazia

```
❌ ERRADO:
[Source] → [Split] → ...

✅ CERTO:
[Source] → [IF: Empty?] ──true→ [Skip]
              └─false→ [Split] → ...
```

---

## Checklist de Validação

Antes de entregar uma especificação:

- [ ] Todo Split In Batches tem main[0] e main[1] conectados
- [ ] Todo loop reconecta para o Split In Batches
- [ ] Todo Merge (Wait) tem AMBAS entradas conectadas
- [ ] Lista vazia é tratada antes do Split In Batches
- [ ] Não há loops infinitos possíveis
- [ ] Campos de entrada/saída estão documentados

---

**Estas boas práticas garantem workflows confiáveis, eficientes e manuteníveis.**
