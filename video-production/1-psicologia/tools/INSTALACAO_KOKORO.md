# Kokoro TTS - Guia Rápido

## O que é:
Kokoro TTS - Text-to-Speech local com qualidade profissional

## Vozes Disponíveis:

### Masculinas (Inglês Americano):
- `am_michael` - Melhor opção (profunda, autoritária) ⭐ RECOMENDADO
- `am_fenrir` - Forte, poderoso
- `am_puck` - Lúdico, versátil
- `am_onyx` - Elegante
- `am_echo` - Ressonante
- `am_eric` - Profissional
- `am_liam` - Amigável
- `am_adam` - Não recomendado

### Femininas (Inglês Americano):
- `af_heart` - Melhor opção (natural, calorosa) ⭐
- `af_bella` - Excelente (profissional)
- `af_sarah` - Boa (madura)
- `af_nicole` - Boa

### Britânicas:
- `bf_emma` - Feminina britânica
- `bm_george` - Masculino britânico

## Instalação (3 passos):

### 1. Instalar Miniconda
Baixar de: https://docs.conda.io/en/latest/miniconda.html

### 2. Criar ambiente
```bash
conda create --name kokoro python=3.12 -y
conda activate kokoro
```

### 3. Instalar dependências
```bash
pip install -r requirements_kokoro_conda.txt
```

## Como Usar:

### Edite o kokoro_tts.py:
```python
TEXTO = "Seu texto aqui"
VOZ = "am_michael"  # ou af_heart
VELOCIDADE = 1.0
ARQUIVO_SAIDA = "audio.wav"
```

### Execute:
```bash
conda activate kokoro
python kokoro_tts.py
```

## Voz Recomendada para Vídeos:
- Narrativa masculina: `am_michael`
- Narrativa feminina: `af_heart`

## Listar vozes disponíveis:
```bash
python kokoro_tts.py --vozes
```
