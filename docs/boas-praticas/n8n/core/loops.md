# Loops e Branches Paralelos

Trabalhar com loops e branches paralelos requer cuidado para evitar problemas comuns.

## Evitar Loops Infinitos

```
❌ PERIGO:
[Split] → main[1] → [Process] → volta direto
                       (sem condição de saída!)

✅ SEGURO:
[Split] → main[1] → [Process] → [Wait] → volta
          main[0] → [Próximo]
```

**Regra:** Sempre tenha um caminho claro de saída do loop.

## Sincronização com Wait

```
         ┌─▶ Process A ──┐
Split In ─┤               ├──▶ Wait ──▶ Merge ──▶ volta ao Split
         └─▶ Process B ──┘
```

**Regras:**
1. Use Wait para sincronizar branches paralelos
2. Wait garante que ambos terminem antes de continuar
3. Último node antes de voltar ao Split

## Condição de Saída

```
[Process] → [IF: finished?] ──true→ [Merge] → [Wait] → volta
               └─false→ [Continue]
```

**Condição:** `{{ $json.finished === true }}`

## Loops Aninhados

```
[Split Outer] → main[1] → [Process Outer] → [Split Inner] → main[1] → [Process Inner] → [Wait] → volta
                                 └─ main[0] → [Combine] → [Wait] → volta ao Outer
                └─ main[0] → [Resumo Outer]
```

**Regras:**
1. Cada Split In Batches tem seu próprio Wait de reconexão
2. Loops internos devem completar antes de continuar o externo
3. Cuidado com performance (loops aninhados são custosos)

## Limitação de Iterações

```
[Split] → main[1] → [Process] → [IF: Count < Max?] ──true→ [Increment] → [Wait] → volta
                                              └─false→ [Break] → main[0]
```

**Condição:** `{{ $json.count < $json.maxIterations }}`

## Branches Condicionais

```
[Split] → main[1] → [IF: Type?] ──true→ [Process A] ─┐
                           └─false→ [Process B] ──┤
                                                    ├──▶ Merge → [Wait] → volta
```

## Timeout em Loops

```
[Split] → main[1] → [Process] → [Wait: 5s] → [IF: Timeout?] ──true→ [Error]
                                                        └─false→ volta
```

## Anti-Padrões

### ❌ Loop Infinito
```
[Split] → main[1] → [Process] → volta (sem condição!)
```
**Problema:** Nunca termina

### ❌ Loop Sem Sincronização
```
         ┌─▶ A ──┐
[Split] ─┤       ├──▶ Merge (sem Wait!)
         └─▶ B ──┘
```
**Problema:** Race conditions

### ❌ Loops Aninhados Profundos
```
[Split A] → [Split B] → [Split C] → ...
```
**Problema:** Performance terrível

## Dicas de Performance

- ✅ Use Batch Size > 1 quando possível
- ✅ Evite loops aninhados (refatore se precisar)
- ✅ Use IF nodes para sair cedo do loop
- ✅ Limite iterações quando possível
- ✅ Considere usar Function node para processamento em lote

## Checklist

- [ ] Loop tem condição de saída clara
- [ ] main[0] está conectado
- [ ] Wait usado para sincronização
- [ ] Não há branches sem sincronização
- [ ] Performance considerada
- [ ] Timeout configurado (se necessário)
