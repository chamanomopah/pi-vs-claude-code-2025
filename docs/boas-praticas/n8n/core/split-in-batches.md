# Split In Batches (Loops)

O Split In Batches é fundamental para processar listas. Ele tem **DUAS saídas**.

## Saídas

### main[0] - Saída do Loop (Executa 1 vez)
- **Quando executa**: Quando o loop TERMINA (todos itens processados)
- **O que passa**: 1 item com campos especiais
  - `finished`: true
  - `numberOfBatches`: número total de batches
- **Para que serve**: Continuar o fluxo APÓS o loop
- **Como usar**: Conecte ao próximo node do fluxo principal

### main[1] - Dentro do Loop (Executa N vezes)
- **Quando executa**: Para CADA batch de itens
- **O que passa**: Os itens do batch atual
- **Para que serve**: Processar cada item
- **Como usar**: Conecte aos nodes que processam itens

## Padrão Correto de Loop

```
[Source] → [Split In Batches] → main[1] → [Process] → [Wait] → volta
                               └─ main[0] → [Próximo Passo]
```

**Regras:**
1. main[1] conecta ao processamento
2. Último node do loop DEVE reconectar para Split In Batches
3. Node Wait antes de voltar (evita problemas de sincronização)
4. main[0] conecta ao próximo node APÓS o loop

## Verificação de Lista Vazia

```
[Source] → [IF: Empty?] ──true→ [Skip] → [Fim]
              └─false→ [Split In Batches] → ...
```

**Condição IF:** `{{ $json.items.length === 0 }}`

## Batch Size

- **Batch Size: 1** (mais comum): Processa 1 item por vez
- **Batch Size: N**: Processa N itens por vez (útil para bulk operations)

## Reset: false vs true

- **Reset: false** (recomendado): Mantém estado se re-executar
- **Reset: true**: Recomeça do zero sempre

## Verificação de Conclusão

Para verificar se o loop completou:

```javascript
// No node conectado a main[0]
{{ $json.finished === true }}
```

## Anti-Padrões

### ❌ Loop Sem Reconexão
```
[Split] → main[1] → [Process] → [Fim]
```
**Problema:** Loop não processa todos os itens

### ❌ Esquecer main[0]
```
[Split] → main[1] → [Loop] → volta
(main[0] não conectada!)
```
**Problema:** Fluxo nunca continua após o loop

### ❌ Sem Tratar Lista Vazia
```
[Source] → [Split] → ...
```
**Problema:** Erro quando lista está vazia

## Checklist

- [ ] main[0] está conectado ao fluxo após o loop
- [ ] main[1] está conectado ao processamento
- [ ] Último node reconecta para Split In Batches
- [ ] Node Wait usado antes de reconectar
- [ ] Lista vazia é tratada antes do Split
- [ ] Batch Size configurado corretamente
