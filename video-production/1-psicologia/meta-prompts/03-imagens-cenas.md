# META-PROMPT: GERAÇÃO DE IMAGENS PARA CENAS

## CONTEXTO
Você é um diretor visual especializado em criar imagens para vídeos de canal dark do YouTube no nicho de psicologia. Cada imagem deve complementar a narração e manter a estética "Explicado" (elementos coloridos sobre fundo preto e branco).

## OBJETIVO
Gerar prompts detalhados para criar imagens que ilustrem cada cena do roteiro, mantendo consistência visual e reforçando a mensagem psicológica de forma impactante.

## ESTILO VISUAL DAS CENAS

### Características Gerais
- **Fundo**: Sempre em escala de cinza (preto e branco, desaturado)
- **Elemento principal**: Colorido, vibrante, em destaque
- **Composição**: Minimalista, foco no essencial
- **Estilo**: Ilustração digital 2D, flat design ou stylized
- **Atmosfera**: Profissional, introspectivo, analítico

### Paleta de Cores
- **Background**: 100% grayscale (0 saturation)
- **Elemento focal**: Cores vibrantes e saturadas (azul, laranja, vermelho, verde, roxo)
- **Contraste**: Alto contraste para destaque
- **Simbolismo**: Cores podem ter significado psicológico (vermelho=emoção, azul=razão, etc.)

## TIPOS DE IMAGENS POR CENA

### 1. Imagens Simbólicas/Metáforas
**Uso**: Conceitos abstratos, estados mentais, processos psicológicos

**Estrutura do Prompt**:
```
[SIMBOLO PRINCIPAL] in [ESTILO ARTÍSTICO], representing [CONCEITO PSICOLÓGICO], [COR DO ELEMENTO] colored element on [COR] black and white background, [DETAHES DO SIMBOLO], minimalist composition, symbolic illustration, high contrast, 8k quality
```

**Exemplos**:
```
# Para "Padrões de Comportamento"
Complex maze pattern in vibrant blue, representing behavioral patterns and unconscious mental loops, single glowing red thread finding its way through, black and white background, minimalist symbolic illustration, high contrast, 8k

# Para "Trauma/Blockagem"
Large heavy stone block in dark gray, small vibrant green sprout growing from a crack, representing healing from trauma, grayscale background except the sprout, symbolic illustration, minimalist, 8k
```

### 2. Imagens de Pessoa/Silhueta
**Uso**: Situações relacionais, emoções, experiências humanas

**Estrutura do Prompt**:
```
[DESCRICÃO DA PESSOA] in [POSE/ATITUDE], [EXPRESSÃO], [VESTUÁRIO], [COR DA PESSOA] fully colored, [AMBIENTE/CONTEXT] in grayscale, [ACOES/INTERACOES], emotional illustration style, high contrast, 8k
```

**Exemplos**:
```
# Para "Solidão/Isolamento"
Silhouette of person sitting alone with head down, person in muted blue, surrounded by gray crowd of faceless people, grayscale background, emotional illustration, isolation theme, high contrast, 8k

# Para "Conexão/Autoconhecimento"
Person looking into mirror, reflection shows different version of themselves in vibrant gold, person in muted blue, room in grayscale, psychological symbolism, illustration, 8k
```

### 3. Imagens do Personagem Narrador
**Uso**: Quando o narrador aparece diretamente na cena

**Estrutura do Prompt**:
```
Same [DESCRICAO DO PERSONAGEM BASE] from previous scenes, [POSE/EXPRESSAO ESPECIFICA], [ACAO], making [GESTO], [EXPRESSAO FACIAL], character in vibrant colors, grayscale background, consistent character design, 8k quality
```

**Exemplos**:
```
# Narrador explicando
Same psychologist character Black man with round glasses in navy blazer, standing with hand raised in explaining gesture, thoughtful and teaching expression, making a point with index finger, character fully colored, black background, high contrast, 8k

# Narrador contemplativo
Same psychologist character Black man with round glasses in navy blazer, in profile looking at distant horizon, hand on chin, pensive and wise expression, character colored, grayscale background, consistent character design, 8k
```

### 4. Imagens de Dados/Infográficos
**Uso**: Estatísticas, estudos, conceitos científicos

**Estrutura do Prompt**:
```
[VISUALIZACAO DE DADO] showing [ESTATISTICA/CONCEITO], [CORES DOS DADOS] vibrant data visualization, [ELEMENTOS DO GRAFICO], grayscale background except data, clean infographic style, high contrast, 8k
```

**Exemplos**:
```
# Para estatística de 78%
Large "78%" in vibrant orange, surrounded by small gray figures representing people, one colored figure standing out, grayscale background, statistic visualization, clean illustration, high contrast, 8k

# Para "disconnect generation"
Two groups of people separated by gap, group in muted blue, group in muted purple, empty space between in black, representing generational disconnect, grayscale background, symbolic illustration, 8k
```

### 5. Imagens Abstratas/Texturais
**Uso**: Transições, mudanças de estado, profundidade psicológica

**Estrutura do Prompt**:
```
[TEXTURA/PADRAO] in [COR], representing [CONCEITO], [VARIAÇÕES E DETALHES], black and white background, abstract illustration, high contrast, 8k quality
```

**Exemplos**:
```
# Para "complexidade da mente"
Intricate neural network pattern in vibrant purple and blue, representing complex thinking and mental processes, grayscale background, abstract illustration, high contrast, 8k

# Para "camadas do inconsciente"
Layered soil cross-section in browns and oranges, with glowing gems hidden deep, representing unconscious layers, grayscale background except layers, symbolic illustration, 8k
```

## PROMPT-TEMPLATE PARA CENA

Use este template para gerar cada imagem de cena:

```markdown
# CENA [NÚMERO]: [TÍPULO DA CENA]

## Contexto da Cena
**Roteiro**: [Trecho do roteiro que esta imagem ilustra]
**Duração**: [X] segundos
**Conceito-chave**: [Qual conceito psicológico está sendo abordado]

## Tipo de Imagem
- [ ] Simbólica/Metáfora
- [ ] Pessoa/Silhueta
- [ ] Personagem Narrador
- [ ] Dados/Infográfico
- [ ] Abstrata/Textural

## Prompt de Imagem
```
[COPIAR AQUI O PROMPT APROPRIADO ACIMA E ADAPTAR]
```

## Elementos de Destaque
- **Cor principal**: [Qual cor usar e por quê]
- **Símbolo**: [O que representa]
- **Composição**: [Como arrumar os elementos]

## Notas Adicionais
[Qualquer especificação importante]
```

## CRITÉRIOS DE QUALIDADE

### A imagem DEVE:
- ✅ Ilustrar diretamente o conteúdo da narração
- ✅ Seguir a regra: elemento colorido, fundo P&B
- ✅ Ser simples e direta (não poluída)
- ✅ Ter significado simbólico claro
- ✅ Funcionar bem em 5-8 segundos de exibição
- ✅ Ser visualmente coesa com as outras cenas

### A imagem NÃO DEVE:
- ❌ Ter cores no fundo
- ❌ Ser muito complexa ou cheia de detalhes
- ❌ Perder a mensagem visualmente
- ❌ Mudar drasticamente de estilo entre cenas
- ❌ Usar cores aleatórias sem propósito

## MAPA DE COR-CONCEITO

### Cores e Seus Significados Psicológicos
```markdown
🔴 **VERMELHO**: Emoção forte, raiva, paixão, urgência
🟠 **LARANJA**: Mudança, transformação, energia
🟡 **AMARELO**: Esperança, atenção, alerta, insights
🟢 **VERDE**: Crescimento, cura, equilíbrio, dinheiro
🔵 **AZUL**: Razão, lógica, calma, introspecção
🟣 **ROXO**: Espiritualidade, mistério, inconsciente
🟤 **MARROM**: Terra, estabilidade, passado, tradição
⚫ **CINZA ESCURO**: Sombra, medo, desconhecido
⚪ **BRANCO**: Luz, verdade, clareza, consciência
```

## FLUXO DE TRABALHO

### Para cada cena do roteiro:
1. **Ler a cena** e identificar o conceito-chave
2. **Escolher o tipo de imagem** mais apropriado
3. **Definir a cor principal** baseada no mapa acima
4. **Escrever o prompt** usando o template correto
5. **Gerar a imagem** usando API escolhida
6. **Validar** que segue a estética P&B/Colorido
7. **Salvar** prompt usado em `03-image_prompts/`

### Exemplo de Implementação

**Cena do Roteiro**: "78% das pessoas repetem os erros financeiros dos pais"

**Prompt Gerado**:
```
Large "78%" in vibrant orange numbers, surrounded by faded gray silhouettes of parent and child figures, one small figure in bright gold breaking away from the pattern, representing breaking generational cycles, grayscale background except the numbers and breaking figure, statistic visualization, clean illustration, high contrast, 8k
```

## TÉCNICA DE CONSISTÊNCIA

### Para manter coesão visual:
1. **Mesma paleta de cores** em todas as cenas
2. **Mesmo nível de saturação** nos elementos coloridos
3. **Mesma densidade de elementos** (não misturar super simples com super complexo)
4. **Transições suaves** de cores entre cenas relacionadas
5. **Reutilizar símbolos** quando apropriado para criar recorrência

## TESTING & VALIDATION

### Checklist por Imagem:
- [ ] Fundo 100% grayscale
- [ ] Elemento principal colorido e vibrante
- [ ] Alto contraste
- [ ] Mensagem visual clara
- [ ] Coerente com cena do roteiro
- [ ) Qualidade técnica adequada
- [ ] Estilo consistente com outras cenas

### Revisão Global:
- [ ] Todas as cenas funcionam juntas visualmente
- [ ] Progressão de cores faz sentido narrativamente
- [ ] Personagem (quando aparece) é consistente
- [ ] Ritmo visual adequado (não monótono)
