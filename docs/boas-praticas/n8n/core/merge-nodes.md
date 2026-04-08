# Merge Nodes

Os Merge nodes são fundamentais para sincronizar e combinar dados de múltiplas fontes.

## Modos de Merge

### Modo "Wait"
- **Comportamento**: Aguarda TODAS as entradas antes de continuar
- **Quando usar**: Sincronizar branches paralelos
- **Regra**: AMBAS as entradas DEVEM estar conectadas
- **Executa**: Somente quando todas as entradas chegarem

### Modo "Append"
- **Comportamento**: Combina itens de ambas em uma lista
- **Quando usar**: Juntar resultados de branches
- **Regra**: Entradas podem ser opcionais
- **Resultado**: Array com todos os itens

### Modo "Merge by Key"
- **Comportamento**: Junta dados baseado em campo chave
- **Quando usar**: Combinar dados relacionados
- **Regra**: Especificar campo de junção
- **Resultado**: Objeto com dados mesclados

## Regra de Ouro

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

## Padrões de Uso

### Sincronização de Branches

```
         ┌─▶ Branch A ──┐
Split In ─┤              ├──▶ Merge (Wait) ──▶ próximo
         └─▶ Branch B ──┘
```

- Merge aguarda AMBAS as branches completarem
- Use Wait nodes dentro de branches se necessário
- Garante que dados estão prontos antes de continuar

### Append de Resultados

```
[Process A] ──┐
             ├──▶ Merge (Append) ──▶ [Listar Todos]
[Process B] ──┘
```

### Merge por Chave

```
[User Data] ──┐
             ├──▶ Merge (by Key: userId) ──▶ [User + Orders]
[User Orders]┘
```

## Parâmetros Importantes

### Modo Wait
- **Mode**: Wait
- **Wait Until**: All input streams have data

### Modo Append
- **Mode**: Append
- **Options**: Include unpaired data (opcional)

### Modo Merge by Key
- **Mode**: Combine
- **Combine By**: Merge By Key
- **Property to Match**: Nome do campo (ex: userId)

## Anti-Padrões

### ❌ Merge com Entrada Solta (Wait Mode)
```
[Branch A] → [Merge Wait] → Próximo
(Branch B não conectada!)
```
**Problema:** Merge nunca executa (aguarda eternamente)

### ❌ Merge por Chave sem Campo Comum
```
[Data A: {id: 1}] ──┐
                   ├──▶ Merge (by Key: userId)
[Data B: {code: 1}]┘
```
**Problema:** Nada é mesclado (campos diferentes)

### ❌ Esquecer de Conectar Todas as Entradas
```
[Branch A] ──┐
             ├──▶ Merge
[Branch B] ──┘ (não conectado!)
```
**Problema:** Comportamento indefinido

## Checklist

- [ ] Modo correto selecionado
- [ ] Todas as entradas conectadas (modo Wait)
- [ ] Campo de chave especificado (modo Merge by Key)
- [ ] Dados têm campos compatíveis (modo Merge by Key)
- [ ] Timeout configurado (se necessário)
