# Como Instalar Kokoro TTS com Conda (Python 3.12)

## 📋 Visão Geral

Esta solução usa **Conda** para criar um ambiente isolado com Python 3.12, garantindo compatibilidade total com o Kokoro TTS.

**Solução testada e funcionando!** ✓
Baseado em: https://heyletslearnsomething.com/blog/kokoro-tts-free-text-to-speech

---

## 🚀 INSTALAÇÃO RÁPIDA

### Pré-requisitos

Você precisa ter o **Miniconda** ou **Anaconda** instalado.

**Verificar se Conda já está instalado:**
```bash
conda --version
```

Se aparecer uma versão (ex: `conda 24.x.x`), você já tem o Conda instalado! ✓

---

### PASSO 1: Instalar Miniconda (se necessário)

Se você **NÃO** tem o Conda instalado:

**Windows:**
1. Baixe o instalador em: https://docs.conda.io/en/latest/miniconda.html
2. Escolha a versão **Windows 64-bit**
3. Execute o instalador com as opções padrão
4. **IMPORTANTE:** Marque a opção "Add Miniconda to my PATH environment variable" durante a instalação

**Linux/Mac:**
```bash
# Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Mac
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh
```

**Após instalar, feche e abra o terminal novamente.**

---

### PASSO 2: Criar Ambiente Conda com Python 3.12

O Conda vai criar um ambiente **isolado** que não afeta seu Python principal:

```bash
# Criar ambiente chamado 'kokoro' com Python 3.12
conda create --name kokoro python=3.12 -y

# Ativar o ambiente
conda activate kokoro
```

**Verifique que está no ambiente correto:**
```bash
python --version
# Deve mostrar: Python 3.12.x
```

---

### PASSO 3: Instalar Dependências do Kokoro

Com o ambiente ativado:

```bash
# Opção 1: Instalar usando o arquivo de requirements
pip install -r requirements_kokoro_conda.txt

# Opção 2: Instalar manualmente
pip install kokoro>=0.9.4 soundfile torch
```

Aguarde a instalação completar (pode levar alguns minutos).

---

### PASSO 4: Testar o Kokoro TTS

```bash
# Garanta que o ambiente está ativado
conda activate kokoro

# Execute o script de teste
python kokoro_tts.py
```

**Resultado esperado:**
```
============================================================
KOKORO TTS - Text-to-Speech com PyTorch
============================================================

📋 CONFIGURAÇÕES:
   Texto: Hello! This is a test...
   Voz: af_heart
   Velocidade: 1.0x
   Arquivo de saída: audio_kokoro.wav

📦 Importando bibliotecas...
🔄 Carregando modelo Kokoro (pode demorar na primeira execução)...
✅ Modelo carregado com sucesso!

🎙️  Gerando áudio...

✅ SUCESSO!
   Arquivo: audio_kokoro.wav
   Duração: 3.45 segundos
   Tamanho: 132.5 KB
   Taxa de amostragem: 24000 Hz

============================================================
✅ PROCESSO CONCLUÍDO!
============================================================
```

---

## 🎤 USANDO O KOKORO TTS

### Personalizar o Áudio

Edite as variáveis no topo do arquivo `kokoro_tts.py`:

```python
# ===== CONFIGURAÇÕES =====
TEXTO = "Seu texto aqui"
VOZ = "af_heart"        # Veja lista abaixo
VELOCIDADE = 1.0         # 0.5 a 2.0
ARQUIVO_SAIDA = "meu_audio.wav"
# ==========================
```

### Listar Vozenhas Disponíveis

```bash
python kokoro_tts.py --vozes
```

### Vozenhas Disponíveis

| Voz | Descrição |
|-----|-----------|
| **af_heart** ❤️ | **MELHOR OPÇÃO** - Feminina, americana, natural e calorosa |
| **af_bella** 🔥 | Feminina, americana, profissional |
| **af_sarah** 👩 | Feminina, americana, madura |
| **am_adam** 👨 | Masculino, americano |
| **am_michael** 💼 | Masculino, americano, profissional |
| **bf_emma** 🇬🇧 | Feminina, britânica |
| **bm_george** 🇬🇧 | Masculino, britânico |

**Recomendação:** Use `af_heart` para melhor qualidade geral.

---

## 🔧 COMANDOS ÚTEIS

### Gerenciar o Ambiente Conda

```bash
# Ativar ambiente
conda activate kokoro

# Desativar ambiente
conda deactivate

# Listar ambientes
conda env list

# Remover ambiente (se precisar reinstalar)
conda env remove --name kokoro --yes
```

### Atualizar Dependências

```bash
conda activate kokoro
pip install --upgrade kokoro soundfile torch
```

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: "conda: command not found"

**Causa:** O Conda não está no PATH do sistema.

**Solução:**
1. **Windows:** Adicione ao PATH manualmente:
   - Painel de Controle > Sistema > Variáveis de Ambiente
   - Adicione: `C:\Users\SEU_USUARIO\miniconda3\Scripts`
   - Ou reinstale marcando "Add to PATH"

2. **Linux/Mac:** Reinicie o terminal ou execute:
   ```bash
   source ~/.bashrc  # ou ~/.zshrc
   ```

### Erro: "No module named 'kokoro'"

**Causa:** O ambiente não está ativado ou o Kokoro não foi instalado.

**Solução:**
```bash
# Verifique se está no ambiente correto
conda activate kokoro
python --version  # Deve ser 3.12.x

# Reinstale o Kokoro
pip install kokoro>=0.9.4 soundfile torch
```

### Erro: "CUDA out of memory"

**Causa:** Modelo muito grande para sua GPU.

**Solução:**
- O Kokoro usa CPU por padrão (não precisa de GPU)
- Se ainda assim der erro, reduza o tamanho do texto

### Modelo não baixa (erro de conexão)

**Solução:**
- Verifique sua conexão com a internet
- Na primeira execução, o Kokoro baixa ~2GB de modelos
- Tente novamente se a conexão cair

---

## 📚 MAIS INFORMAÇÕES

### Links Úteis

- **Documentação oficial:** https://github.com/remsky/Kokoro-FastAPI
- **Tutorial base:** https://heyletslearnsomething.com/blog/kokoro-tts-free-text-to-speech
- **GitHub Issues:** #103 e #113 (confirmam que esta solução funciona)

### Características do Kokoro

- ✅ **Alta qualidade:** Vozes naturais e expressivas
- ✅ **Multi-idioma:** Inglês (americano/britânico)
- ✅ **Rápido:** Geração em tempo real
- ✅ **Gratuito:** Código aberto
- ✅ **Sem API:** Funciona offline após baixar os modelos
- ✅ **Taxa de amostragem:** 24kHz (qualidade de CD)

---

## ✅ CHECKLIST DE INSTALAÇÃO

Use este checklist para verificar se tudo está funcionando:

- [ ] Conda está instalado (`conda --version`)
- [ ] Ambiente 'kokoro' foi criado (`conda env list`)
- [ ] Python 3.12 está ativo (`python --version` deve mostrar 3.12.x)
- [ ] Kokoro está instalado (`pip show kokoro`)
- [ ] Script executou sem erros (`python kokoro_tts.py`)
- [ ] Arquivo `audio_kokoro.wav` foi criado
- [ ] Arquivo de áudio reproduz corretamente

---

## 💡 DICAS

1. **Sempre ative o ambiente antes de usar:**
   ```bash
   conda activate kokoro
   python kokoro_tts.py
   ```

2. **Use UTF-8 para textos com acentos:**
   ```python
   # No topo do script
   # -*- coding: utf-8 -*-
   ```

3. **Textos longos podem ser divididos em frases:**
   ```python
   TEXTO = "Frase 1. Frase 2. Frase 3."
   ```

4. **Velocidade recomendada:**
   - 0.8 a 1.0 para narração normal
   - 1.2 para leitura rápida
   - 0.5 para efeito dramático

---

**Problemas?** Verifique a seção "Solução de Problemas" acima ou consulte:
- GitHub Issues: https://github.com/remsky/Kokoro-FastAPI/issues
- Tutorial original: https://heyletslearnsomething.com/blog/kokoro-tts-free-text-to-speech
