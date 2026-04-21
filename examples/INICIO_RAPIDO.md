# 🚀 Guia de Início Rápido

## Testar em 2 Minutos

### 1. Verificar ComfyUI

```bash
curl http://127.0.0.1:8188/system_stats
```

Se retornar JSON, o ComfyUI está rodando! ✅

### 2. Executar Primeiro Exemplo

**KOKORO TTS:**
```bash
cd examples/kokoro_tts
python exemplo1_python_simple.py
```

**Z-IMAGE-TURBO:**
```bash
cd examples/zimage_turbo
python exemplo1_python_simple.py
```

### 3. Encontrar Output

Os arquivos são salvos em:
```
ComfyUI/user/outputs/YYYY-MM-DD/
├── kokoro_tts/exemplo1_simples/
└── zimage_turbo/exemplo1_simples/
```

---

## Exemplos Disponíveis

| Workflow | Exemplo | cURL | Python | Descrição |
|----------|---------|------|--------|-----------|
| **KOKORO TTS** | 1 | ✅ | ✅ | Texto simples |
| **KOKORO TTS** | 2 | ✅ | ✅ | Batch de textos |
| **KOKORO TTS** | 3 | ✅ | ✅ | Upload áudio |
| **Z-IMAGE** | 1 | ✅ | ✅ | Texto para imagem |
| **Z-IMAGE** | 2 | ✅ | ✅ | Batch de prompts |
| **Z-IMAGE** | 3 | ✅ | ✅ | Upload imagem |

---

## Comandos Rápidos

```bash
# Todos os exemplos KOKORO
for i in 1 2 3; do
  echo "=== KOKORO Exemplo $i ==="
  python examples/kokoro_tts/exemplo${i}_python_*.py
done

# Todos os exemplos Z-IMAGE
for i in 1 2 3; do
  echo "=== Z-IMAGE Exemplo $i ==="
  python examples/zimage_turbo/exemplo${i}_python_*.py
done
```

---

## Problemas?

**ComfyUI não responde:**
```bash
# Iniciar ComfyUI
cd C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI
run_nvidia_gpu.bat
```

**Erro de encoding no Windows:**
```bash
cd examples
python fix_encoding.py
```

**Modelos faltando:**
- Verifique `ComfyUI/models/`
- KOKORO: ComfyUI-Kokoro instalado
- Z-IMAGE: `diffusion_models/z_image_turbo_bf16.safetensors`

---

📚 **Documentação completa:** [README.md](README.md)
