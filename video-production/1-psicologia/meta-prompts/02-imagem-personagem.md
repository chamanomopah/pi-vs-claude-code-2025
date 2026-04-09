# META-PROMPT: GERAÇÃO DE IMAGEM DO PERSONAGEM

## CONTEXTO
Você é um diretor de arte especializado em criar personagens consistentes para canais dark do YouTube. O personagem será o elemento visual principal que aparecerá em TODOS os vídeos, na thumbnail e nas cenas internas.

## OBJETIVO
Criar uma descrição detalhada de imagem para gerar um personagem consistente que será usado em todos os vídeos do canal de psicologia, seguindo o estilo "Explicado" (personagem colorido, fundo preto e branco).

## ESTILO VISUAL

### Características do Personagem
- **Estilo**: Ilustração digital / Arte 2D estilizada
- **Consistência**: Mesmo personagem em todos os vídeos e thumbnails
- **Expressão**: Versátil (pode variar entre sério, pensativo, surpreso, empático)
- **Cor**: Personagem em cores vibrantes, fundo completamente em P&B
- **Vibe**: Profissional mas acessível, inteligente, analítico

### Aparência Física (Base)
- **Gênero**: Masculino (mas pode ser adaptado)
- **Idade aparente**: 30-40 anos
- **Etnia**: [DEFINIR - pode variar]
- **Estilo**: Moderno, casual-profissional
- **Características marcantes**: Algo que o torne reconhecível (óculos, penteado, acessório)

### Paleta de Cores
- **Personagem**: Cores vibrantes e saturadas (azul, laranja, verde - dependendo do tema)
- **Fundo**: Preto e branco (escala de cinza, desaturado)
- **Contraste**: Alto contraste para destacar o personagem

## ELEMENTOS DO PROMPT DE IMAGEM

### Estrutura do Prompt
```
[ESTILO ARTÍSTICO] + [DESCRIÇÃO DO PERSONAGEM] + [POSE/EXPRESSÃO] + [AMBIENTE] + [ESTILO DE CORES] + [TÉCNICA DE ILUSTRAÇÃO] + [DETALHES ADICIONAIS]
```

### Componentes Obrigatórios

#### 1. Estilo Artístico
- "Digital illustration"
- "2D character art"
- "Flat design" ou "Stylized realism"
- "YouTube channel art style"

#### 2. Descrição do Personagem
```markdown
Base character appearance:
- Professional psychologist in his 30s
- [DEFINIR ETNIA: ex: Black man with short dreadlocks]
- Wearing [DEFINIR ROUPA: ex: casual blazer, turtleneck]
- [DEFINIR CARACTERÍSTICA: ex: distinctive round glasses]
- Expressive face that conveys intelligence and empathy
```

#### 3. Pose/Expressão (Variável por Cena)
- Thinking/contemplative
- Explaining/gesturing
- Looking directly at camera
- In profile/deep thought
- Surprised/realizing something

#### 4. Ambiente
- "Plain black and white background"
- "Minimalist grayscale environment"
- "Dark silhouette background"
- "No background elements"

#### 5. Estilo de Cores (CRUCIAL)
```markdown
COLOR SCHEME:
- Character: Full vibrant, saturated colors
- Background: Completely black and white, grayscale, desaturated
- High contrast between character and background
- NO colors in background elements
```

#### 6. Técnica de Ilustração
- "Clean lines"
- "Professional digital art"
- "High quality illustration"
- "Vector art style" ou "Painterly style" (definir)

#### 7. Detalhes Adicionais
- "YouTube thumbnail quality"
- "Eye-catching composition"
- "Centered character"
- "Professional lighting"

## PROMPTS PARA DIFERENTES VERSÕES

### Versão Base (Para Definição Inicial)
```
Professional digital illustration of a psychologist character, Black man in his 30s with short styled hair and distinctive round glasses, wearing a navy blue casual blazer over a white t-shirt, thoughtful and intelligent expression, clean modern art style, full vibrant colors on the character, completely black and white grayscale background, high contrast, YouTube thumbnail quality, centered composition, 8k resolution
```

### Versão Thumbnail (Expressiva)
```
Same psychologist character, Black man with round glasses in navy blazer, making a hand gesture while explaining something, surprised and enlightening expression, mouth slightly open as if having a realization, vibrant colors on character only, plain black background, high contrast, eye-catching thumbnail style, professional digital art, 8k
```

### Versão Cena Interior (Contemplativa)
```
Same psychologist character, Black man with round glasses in navy blazer, in profile view looking thoughtfully into the distance, hand on chin, contemplative and wise expression, muted but still colored character, grayscale minimalist background, professional illustration style, cinematic lighting, 8k quality
```

### Versão Cena Dados/Análise (Analítica)
```
Same psychologist character, Black man with round glasses in navy blazer, pointing at something off-screen, analytical and serious expression, glasses reflecting light slightly, vibrant character colors, completely black background, high contrast, explanatory pose, digital illustration, 8k
```

## INSTRUÇÕES DE GERAÇÃO

### Parâmetros Técnicos
- **Resolução**: 1920x1080 (16:9) para cenas, 1280x720 para thumbnail
- **Formato**: PNG ou JPG de alta qualidade
- **Estilo**: Ilustração digital 2D consistente

### APIs Recomendadas
1. **Pollinations.ai**: `https://image.pollinations.ai/prompt/[PROMPT]?width=1920&height=1080`
2. **Gemini 2.5 Flash**: Usar função de geração de imagem
3. **Outras**: DALL-E (se disponível), Stable Diffusion

### Comando de Exemplo (Bash)
```bash
curl "https://image.pollinations.ai/prompt/Professional%20digital%20illustration%20of%20psychologist%20character%20Black%20man%20in%2030s%20round%20glasses%20navy%20blazer%20thoughtful%20expression%20vibrant%20colors%20black%20white%20background?width=1920&height=1080&nologo=true" -o personagem_base.jpg
```

## CRITÉRIOS DE QUALIDADE

### A imagem gerada DEVE:
- ✅ Ter o MESMO personagem em todas as variações
- ✅ Manter o personagem colorido e fundo P&B
- ✅ Ser reconhecível como o mesmo "narrador" do canal
- ✅ Ter qualidade profissional (não amador)
- ✅ Funcionar bem em diferentes expressões/poses

### A imagem NÃO DEVE:
- ❌ Ter cores no fundo
- ❌ Mudar características físicas do personagem
- ❌ Parecer um personagem genérico sem identidade
- ❌ Ter baixa qualidade ou arte ruim
- ❌ Ser 3D ou hiper-realista (manter estilo ilustração)

## VARIÁVEIS PARA CUSTOMIZAÇÃO

### Etinia Aparência
- [ ] Black man/woman
- [ ] White man/woman
- [ ] Asian man/woman
- [ ] Latino man/woman
- [ ] Mixed race man/woman

### Estilo de Roupa
- [ ] Casual blazer (profissional moderno)
- [ ] Turtleneck (intelectual)
- [ ] Hoodie (acessível/jovem)
- [ ] Shirt and tie (tradicional)
- [ ] [Outro]

### Característica Marcante
- [ ] Óculos redondos
- [ ] Barra/styling específico no cabelo
- [ ] Acessório (colar, relógio)
- [ ] Cicatriz ou marca distintiva
- [ ] [Outro]

## CHECKLIST DE VALIDAÇÃO

Antes de aprovar o personagem base:
- [ ] Personagem é visualmente distinto e memorável
- [ ] Expressões variadas são reconhecíveis como o mesmo personagem
- [ ] Contraste colorido/P&B funciona bem
- [ ] Funciona como thumbnail (chama atenção)
- [ ] Transmite autoridade e empatia
- [ ] Consistente em 3+ variações de pose geradas

## PRÓXIMOS PASSOS

1. **Gerar 5-10 variações** do prompt base para testar consistência
2. **Selecionar a versão mais forte** como personagem oficial
3. **Documentar o prompt final** para reuso em todos os vídeos
4. **Criar biblioteca de poses**: thinking, explaining, surprised, serious, empathetic
5. **Testar em thumbnail** para validar que se destaca
