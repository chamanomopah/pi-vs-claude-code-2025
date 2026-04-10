# Kokoro TTS - Início Rápido

## 🚀 USO IMEDIATO

### Windows (Duplo clique)
```
run_kokoro.bat
```

### Linux/Mac
```bash
chmod +x run_kokoro.sh
./run_kokoro.sh
```

### Com Conda Ativado
```bash
conda activate kokoro
python kokoro_tts.py
```

---

## 📝 PERSONALIZAR

Edite o arquivo `kokoro_tts.py` e altere as variáveis no topo:

```python
# ===== CONFIGURAÇÕES =====
TEXTO = "Seu texto aqui"
VOZ = "af_heart"        # Veja lista abaixo
VELOCIDADE = 1.0         # 0.5 a 2.0
ARQUIVO_SAIDA = "meu_audio.wav"
# ==========================
```

---

## 🎤 LISTAR VOZES

```bash
python kokoro_tts.py --vozes
```

**Vozenhas disponíveis:**
- `af_heart` ❤️ - **MELHOR OPÇÃO** (feminina, natural)
- `af_bella` 🔥 (feminina, profissional)
- `af_sarah` (feminina, madura)
- `am_adam` (masculino)
- `am_michael` (masculino, profissional)
- `bf_emma` 🇬🇧 (britânica)

---

## 📚 DOCUMENTAÇÃO COMPLETA

Veja `INSTALACAO_CONDAS.md` para instruções detalhadas de instalação e solução de problemas.

---

## ✅ TESTADO E FUNCIONANDO

- **Ambiente:** Conda + Python 3.12
- **Sistema:** Windows/Linux/Mac
- **Status:** ✓ Testado e validado
- **Áudio de exemplo:** `audio_kokoro.wav` (177 KB, 3.77s)

---

## 🐛 PROBLEMAS?

### Erro: "conda: command not found"
O Conda não está instalado. Baixe Miniconda: https://docs.conda.io/en/latest/miniconda.html

### Erro: "No module named 'kokoro'"
Instale as dependências:
```bash
conda activate kokoro
pip install kokoro>=0.9.4 soundfile torch
```

### Ambiente não existe
Crie o ambiente Conda:
```bash
conda create --name kokoro python=3.12 -y
conda activate kokoro
pip install kokoro>=0.9.4 soundfile torch
```

---

**Fonte:** https://heyletslearnsomething.com/blog/kokoro-tts-free-text-to-speech
