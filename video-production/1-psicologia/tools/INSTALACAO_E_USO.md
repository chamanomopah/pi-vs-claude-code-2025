# TTS - Instalação e Uso Rápido

## 🚀 Início Rápido

### Opção Recomendada: Edge TTS

```bash
# 1. Instalar
pip install edge-tts

# 2. Editar as variáveis no topo do script edge_tts_simple.py
#    - TEXTO
#    - VOZ (ex: en-US-AriaNeural, pt-BR-FranciscaNeural)
#    - ARQUIVO_SAIDA

# 3. Executar
python edge_tts_simple.py
```

## 📦 Arquivos Criados

### Scripts Principais
- **edge_tts_simple.py** - Script TTS recomendado (funciona em qualquer Python) ⭐
- **kokoro_tts.py** - Script Kokoro PyTorch (requer Python 3.8-3.12)
- **kokoro_tts_onnx.py** - Script Kokoro ONNX

### Documentação
- **README_TTS.md** - Documentação completa de todos os scripts
- **README_KOKORO.md** - Documentação específica do Kokoro-82M

### Dependências
- **requirements_edge_tts.txt** - Dependências para Edge TTS
- **requirements_kokoro.txt** - Dependências para Kokoro

### Exemplos
- **test_portugues.py** - Exemplo de uso em português
- **audio_edge_tts.mp3** - Áudio de exemplo em inglês
- **audio_pt_br.mp3** - Áudio de exemplo em português

## 🎤 Vozes Disponíveis (Edge TTS)

### Inglês Americano
- `en-US-AriaNeural` - Feminina (melhor opção) ⭐
- `en-US-JennyNeural` - Feminina (profissional)
- `en-US-GuyNeural` - Masculino
- `en-US-BrandonNeural` - Masculino (profissional)

### Português Brasileiro
- `pt-BR-FranciscaNeural` - Feminina 🇧🇷
- `pt-BR-AntonioNeural` - Masculino 🇧🇷
- `pt-BR-ThalitaNeural` - Feminina (jovem) 🇧🇷

### Listar Todas as Vozes
```bash
edge-tts --list-voices
```

## ✅ Testes Realizados

### Teste 1: Inglês Americano (Feminino)
```bash
python edge_tts_simple.py
# Resultado: audio_edge_tts.mp3 (11.26 segundos)
```

### Teste 2: Português Brasileiro (Feminino)
```bash
python test_portugues.py
# Resultado: audio_pt_br.mp3
```

## 📝 Como Usar

### 1. Narrar Vídeo em Inglês

Edite `edge_tts_simple.py`:
```python
TEXTO = "Welcome to Psychology channel! In this video, we'll explore..."
VOZ = "en-US-AriaNeural"
ARQUIVO_SAIDA = "narracao_cena01.mp3"
```

Execute:
```bash
python edge_tts_simple.py
```

### 2. Narrar Vídeo em Português

Edite `edge_tts_simple.py`:
```python
TEXTO = "Bem-vindo ao canal de Psicologia! Neste vídeo..."
VOZ = "pt-BR-FranciscaNeural"
ARQUIVO_SAIDA = "narracao_cena01.mp3"
```

Execute:
```bash
python edge_tts_simple.py
```

## 🎯 Por Que Edge TTS?

1. **Compatibilidade** - Funciona em Python 3.8 a 3.13+
2. **Simplicidade** - Apenas `pip install edge-tts`
3. **Qualidade** - Vozes neurais Microsoft Edge
4. **Velocidade** - Gera áudio em segundos
5. **Gratuito** - Sem custos ou limites

## 📚 Mais Informações

Veja **README_TTS.md** para documentação completa.

---

**Status:** ✅ Testado e funcionando
**Data:** 2025-04-09
**Python:** 3.13.1
