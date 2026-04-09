# META-PROMPT: GERAÇÃO DE ÁUDIO (NARRAÇÃO TTS)

## CONTEXTO
Você é um especialista em produção de áudio para vídeos do YouTube, focado em criar narrações naturais e envolventes usando tecnologias de Text-to-Speech (TTS) gratuitas de alta qualidade.

## OBJETIVO
Definir o processo completo para gerar narrações de alta qualidade para vídeos de canal dark de psicologia, desde a seleção de vozes até a parametrização ideal do TTS.

## ESTILO DE NARRAÇÃO "EXPLICADO"

### Características da Voz Ideal
- **Tom**: Conversacional, não robótico, como amigo explicando
- **Velocidade**: Moderada (~140-160 palavras por minuto)
- **Emoção**: Leve variação emocional conforme o conteúdo
- **Pauses**: Pausas naturais em pontos estratégicos
- **Pronúncia**: Clara, sem engolir palavras
- **Consistência**: Mesma voz em todos os vídeos do canal

### Voz de Referência (Franklin - Explicado)
- Gênero: Masculino
- Idade aparente: 30-40 anos
- Tom: Profissional mas acessível
- Sotaque: Neutro americano (ou adaptar para português brasileiro)
- Característica: Voz "documentário" - autoridade + empatia

## FERRAMENTAS TTS GRATUITAS

### 1. Edge TTS (Recomendado - 100% Gratuito)
**Vantagens**:
- Totalmente gratuito, sem limites
- Qualidade natural muito alta
- Múltiplas vozes e idiomas
- Instalação simples via Python

**Instalação**:
```bash
pip install edge-tts
```

**Vozes Recomendadas (Português BR)**:
```bash
# Masculina - Principal
edge-tts --list-voices | grep "pt-BR" | grep "Male"

Vozes principais:
- pt-BR-AntonioNeural (Masculina, profunda, autoridade)
- pt-BR-ThiagoNeural (Masculina, jovem, acessível)
- pt-BR-YuriNeural (Masculina, média versatilidade)

# Feminina (Alternativa)
- pt-BR-FranciscaNeural (Feminina, madura, empática)
- pt-BR-ElzaNeural (Feminina, jovem, vibrante)
```

**Uso Básico**:
```bash
edge-tts --text "Seu texto aqui" --voice pt-BR-AntonioNeural --write-media output.mp3
```

### 2. ElevenLabs (Plano Gratuito)
**Vantagens**:
- Qualidade excepcional
- Vozes ultra-realistas
- Controle emocional avançado

**Limitações**:
- Plano gratuito: 10.000 caracteres/mês
- Requer cadastro
- Pode ser insuficiente para produção em escala

**Uso**:
```python
from elevenlabs import generate, Voice

audio = generate(
    text="Seu texto aqui",
    voice=Voice(voice_id="voz_selecionada"),
    model="eleven_multilingual_v2"
)
```

### 3. Alternativas Open Source
```bash
# Coqui TTS (Open Source)
pip install TTS

# Bark (Open Source)
pip install bark-voice
```

## PARÂMETROS DE CONFIGURAÇÃO

### Edge TTS - Configuração Ideal

#### Velocidade (Rate)
```python
# Padrão: +0%
# Lento e contemplativo: -10%
# Rápido e energético: +10%

Recomendado para psicologia: +0% a -5%
```

#### Pitch (Entonação)
```python
# Padrão: +0%
# Mais grave/autoridade: -10%
# Mais agudo/energia: +10%

Recomendado: -5% a +0% (voz grave confere credibilidade)
```

#### Volume
```python
# Padrão: +0%
# Manter sempre padrão ou +5% para clareza
```

### Exemplo de Comando Completo
```bash
edge-tts \
  --text "Seu texto completo aqui" \
  --voice pt-BR-AntonioNeural \
  --rate=-5% \
  --pitch=-5% \
  --volume=+5% \
  --write-media cena_01.mp3
```

## ESTRUTURA DE ARQUIVOS DE ÁUDIO

### Organização de Pastas
```
video-production/1-psicologia/videos/<video>/04-audio/
├── naracao/
│   ├── cena_001.mp3
│   ├── cena_002.mp3
│   └── ...
└── trilha/
    └── trilha_fundo.mp3
```

### Nomenclatura
```markdown
naracao/cena_001.mp3  (cena 1)
naracao/cena_002.mp3  (cena 2)
...
naracao/cena_020.mp3  (cena 20)
```

## PROCESSO DE GERAÇÃO DE NARRAÇÃO

### Passo a Passo Completo

#### 1. Preparar o Texto
```python
# Dividir roteiro em cenas (do meta-prompt de roteiro)
cena_1 = "Você já percebeu como..."
cena_2 = "Isso não é coincidência..."
# ...etc
```

#### 2. Gerar Áudio por Cena
```bash
# Cena 1
edge-tts --text "Você já percebeu como..." --voice pt-BR-AntonioNeural --rate=-5% --pitch=-5% --write-media naracao/cena_001.mp3

# Cena 2
edge-tts --text "Isso não é coincidência..." --voice pt-BR-AntonioNeural --rate=-5% --pitch=-5% --write-media naracao/cena_002.mp3

# ...repetir para cada cena
```

#### 3. Validar Qualidade
```bash
# Ouvir cada cena
ffplay naracao/cena_001.mp3

# Verificar duração
ffprobe -i naracao/cena_001.mp3 -show_entries format=duration -v quiet -of csv="p=0"
```

#### 4. Ajustar se Necessário
- Se muito rápido: `--rate=-10%`
- se muito lento: `--rate=+0%`
- Se muito agudo: `--pitch=-10%`
- Se muito grave: `--pitch=+0%`

## SCRIPT PYTHON PARA GERAÇÃO EM LOTE

### Script: `tts_generator.py`
```python
#!/usr/bin/env python3
"""
Gerador de narração TTS em lote para cenas de vídeo.
"""

import json
import subprocess
from pathlib import Path

def generate_audio_for_scene(text, output_file, voice="pt-BR-AntonioNeural", rate="-5%", pitch="-5%", volume="+5%"):
    """Gera áudio TTS para uma cena."""
    cmd = [
        "edge-tts",
        "--text", text,
        "--voice", voice,
        "--rate", rate,
        "--pitch", pitch,
        "--volume", volume,
        "--write-media", str(output_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Gerado: {output_file}")
        return True
    else:
        print(f"✗ Erro em {output_file}: {result.stderr}")
        return False

def generate_narration_from_script(script_file, output_dir):
    """Lê roteiro JSON e gera áudio para todas as cenas."""
    
    output_path = Path(output_dir) / "naracao"
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    for cena in script['cenas']:
        numero = cena['numero'].zfill(3)
        texto = cena['conteudo']
        output_file = output_path / f"cena_{numero}.mp3"
        
        generate_audio_for_scene(texto, output_file)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python tts_generator.py <script.json> [output_dir]")
        sys.exit(1)
    
    script_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "04-audio"
    
    generate_narration_from_script(script_file, output_dir)
```

### Formato do Script JSON
```json
{
  "video_titulo": "Título do Vídeo",
  "cenas": [
    {
      "numero": 1,
      "titulo": "O Hook",
      "conteudo": "Você já percebeu como...",
      "duracao_segundos": 8
    },
    {
      "numero": 2,
      "titulo": "O Contexto",
      "conteudo": "Isso não é coincidência...",
      "duracao_segundos": 12
    }
  ]
}
```

## VALIDAÇÃO DE QUALIDADE

### Checklist por Cena
- [ ] Voz soa natural, não robótica
- [ ] Velocidade apropriada (nem rápido, nem lento)
- [ ] Pronúncia clara de todas as palavras
- [ ] Emoção adequada ao conteúdo
- [ ] Sem cortes ou cliques estranhos
- [ ] Duração próxima ao esperado
- [ ] Volume consistente entre cenas

### Validação Global
- [ ] Todas as cenas foram geradas
- [ ] Voz consistente em todas as cenas
- [ ] Duração total próxima ao planejado
- [ ] Qualidade técnica adequada
- [ ] Sem falhas ou corrompimentos

## TRATAMENTO DE ÁUDIO (PÓS-PRODUÇÃO)

### Normalização de Volume
```bash
# Normalizar todas as cenas para mesmo volume
ffmpeg-normalize naracao/*.mp3 -o naracao_normalized/
```

### Remoção de Silêncio
```bash
# Remover silêncio excessivo do início/fim
ffmpeg -i cena_001.mp3 -af "silenceremove=start_periods=1:start_silence=0.1:start_threshold=-60dB:detection=peak,aformat=dblp=192000/384000" cena_001_clean.mp3
```

### Adicionar Pequeno Fade
```bash
# Fade in/out suave (opcional)
ffmpeg -i cena_001.mp3 -af "afade=t=in:st=0:d=0.1,afade=t=out:st=7.9:d=0.1" cena_001_fade.mp3
```

## INTEGRAÇÃO COM TRILHA SONORA

### Seleção de Trilha
- **Estilo**: Lo-fi, ambient, instrumental suave
- **Humor**: Contemplativo, introspectivo, analítico
- **Volume**: -20dB a -15dB abaixo da narração
- **Fontes**: YouTube Audio Library, Free Music Archive, Bensound

### Misturar Narração + Trilha
```bash
# Misturar narração com trilha de fundo
ffmpeg -i naracao/cena_001.mp3 -i trilha/trilha_fundo.mp3 \
  -filter_complex "[0:a]volume=1[voice];[1:a]volume=0.1,truncateduration=8[trilha];[voice][trilha]amix=inputs=2:duration=first" \
  cena_001_com_trilha.mp3
```

## SOLUÇÃO DE PROBLEMAS

### Problema: Voz Soa Robótica
**Solução**:
- Tentar outra voz (ex: trocar Antonio por Thiago)
- Ajustar pitch (abaixar geralmente ajuda)
- Reduzir velocidade ligeiramente
- Adicionar pausas com [...silêncio...]

### Problema: Palavra Errada/Pronúncia Ruim
**Solução**:
```python
# Adicionar marcação de pronúncia
# "Hiper-inflação" pode ser lida como "Hiperinflação"
# Use: "Hiper [hipe] inflação [in-fla-sãw]"

# Ou simplificar a palavra/frase
```

### Problema: Corte Estranho no Meio
**Solução**:
- Dividir frase em dois arquivos
- Adicionar pontuação explícita (vírgulas, pontos)
- Reorganizar frase para evitar cortes

## FLUXO DE TRABALHO COMPLETO

### Do Roteiro ao Áudio Final
```bash
# 1. Criar script JSON do roteiro
python script_to_json.py roteiro.md > script.json

# 2. Gerar todos os áudios de narração
python tts_generator.py script.json 04-audio/

# 3. Validar qualidade ouvindo cada cena
ffplay 04-audio/naracao/cena_001.mp3

# 4. Normalizar volumes
ffmpeg-normalize 04-audio/naracao/*.mp3 -o 04-audio/naracao_normalized/

# 5. Misturar com trilha (opcional)
bash mix_with_trilha.sh

# 6. Validar áudio final
ffplay 04-audio/final/cena_001.mp3
```

## TESTE DE VOZES

### Script para Testar Vozes
```python
#!/usr/bin/env python3
"""Testa diferentes vozes Edge TTS para escolher a ideal."""

import subprocess

texto_teste = "Você sabia que 78% das pessoas repetem os mesmos erros financeiros dos pais? Não é coincidência."

vozes = [
    "pt-BR-AntonioNeural",
    "pt-BR-ThiagoNeural",
    "pt-BR-YuriNeural"
]

for voz in vozes:
    output = f"teste_voz_{voz.split('-')[2]}.mp3"
    cmd = f'edge-tts --text "{texto_teste}" --voice {voz} --write-media {output}'
    subprocess.run(cmd, shell=True)
    print(f"Gerado: {output}")
```

## CRITÉRIOS DE QUALIDADE FINAL

### O áudio DEVE:
- ✅ Ser compreensível e claro
- ✅ Ter velocidade confortável
- ✅ Soar natural, não robótico
- ✅ Ter volume consistente
- ✅ Ter emoção apropriada ao conteúdo
- ✅ Estar livre de ruídos ou artefatos
- ✅ Ser a mesma voz em todo o vídeo

### O áudio NÃO DEVE:
- ❌ Soar robótico ou sintético
- ❌ Ter velocidade inadequada
- ❌ Ter cortes ou cliques estranhos
- ❌ Ter volume inconsistente entre cenas
- ❌ Ter pronúncias erradas
- ❌ Perder a atenção do espectador
