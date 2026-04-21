# 🧪 Testar os Exemplos

## Verificação de Crição de Arquivos

```bash
# Listar todos os arquivos criados
find examples -type f | sort

# Contar arquivos por tipo
echo "Scripts cURL/bash:"
find examples -name "*.sh" | wc -l

echo "Scripts Python:"
find examples -name "*.py" | wc -l

echo "Documentação:"
find examples -name "*.md" -o -name "*.txt" | wc -l
```

**Resultado esperado:**
- 6 scripts cURL/bash (.sh)
- 7 scripts Python (.py) [6 exemplos + 1 fix_encoding.py]
- 3 arquivos de documentação (.md + .txt)

---

## Teste de Conexão com ComfyUI

```bash
# Teste básico
curl -s http://127.0.0.1:8188/system_stats | head -20

# Ver fila
curl -s http://127.0.0.1:8188/queue

# Ver object_info (nós disponíveis)
curl -s http://127.0.0.1:8188/object_info | head -50
```

---

## Testes Individuais

### KOKORO TTS

#### Exemplo 1 - Texto Simples

```bash
cd examples/kokoro_tts

# Versão Python (recomendado)
python exemplo1_python_simple.py

# Versão cURL
bash exemplo1_curl_simple.sh
```

**Output esperado:**
- Conexão com ComfyUI ✓
- Workflow carregado ✓
- Áudio gerado em `ComfyUI/user/outputs/YYYY-MM-DD/kokoro_tts/exemplo1_simples/`

#### Exemplo 2 - Batch

```bash
python exemplo2_python_batch.py
```

**Output esperado:**
- 3 áudios gerados
- Salvos em `exemplo2_batch/`

#### Exemplo 3 - Upload

```bash
# Sem imagem (demonstração)
python exemplo3_python_upload.py

# Com imagem de referência
python exemplo3_python_upload.py /caminho/do/audio.wav
```

---

### Z-IMAGE-TURBO

#### Exemplo 1 - Texto para Imagem

```bash
cd examples/zimage_turbo

# Versão Python
python exemplo1_python_simple.py

# Versão cURL
bash exemplo1_curl_simple.sh
```

**Output esperado:**
- Imagem gerada
- Salva em `ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo1_simples/`

#### Exemplo 2 - Batch

```bash
python exemplo2_python_batch.py
```

**Output esperado:**
- 3 imagens geradas
- Salvas em `exemplo2_batch/`

#### Exemplo 3 - Upload

```bash
# Sem imagem (demonstração)
python exemplo3_python_img2img.py

# Com imagem de referência
python exemplo3_python_img2img.py /caminho/da/imagem.jpg
```

---

## Teste Batch Completo

```bash
#!/bin/bash
echo "=== Testando todos os exemplos ==="

echo ""
echo "1/6 - KOKORO Exemplo 1"
python examples/kokoro_tts/exemplo1_python_simple.py

echo ""
echo "2/6 - KOKORO Exemplo 2"
python examples/kokoro_tts/exemplo2_python_batch.py

echo ""
echo "3/6 - KOKORO Exemplo 3"
python examples/kokoro_tts/exemplo3_python_upload.py

echo ""
echo "4/6 - Z-IMAGE Exemplo 1"
python examples/zimage_turbo/exemplo1_python_simple.py

echo ""
echo "5/6 - Z-IMAGE Exemplo 2"
python examples/zimage_turbo/exemplo2_python_batch.py

echo ""
echo "6/6 - Z-IMAGE Exemplo 3"
python examples/zimage_turbo/exemplo3_python_img2img.py

echo ""
echo "=== Todos os testes concluídos ==="
```

---

## Verificar Outputs

```bash
# Ver data mais recente
LATEST_OUTPUT="ComfyUI/user/outputs/$(ls -t ComfyUI/user/outputs/ | head -1)"

echo "Outputs em: $LATEST_OUTPUT"
ls -lh "$LATEST_OUTPUT"/kokoro_tts/*/
ls -lh "$LATEST_OUTPUT"/zimage_turbo/*/
```

---

## Troubleshooting

### Erro: ComfyUI não responde

```bash
# Verificar se está rodando
netstat -an | grep 8188

# Ou
curl http://127.0.0.1:8188/system_stats
```

**Solução:** Inicie o ComfyUI
```bash
cd C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI
run_nvidia_gpu.bat
```

### Erro: Encoding no Windows

```bash
cd examples
python fix_encoding.py
```

### Erro: Modelos não encontrados

Verifique:
```bash
# KOKORO
ls ComfyUI/models/*/kokoro*

# Z-IMAGE-TURBO
ls ComfyUI/models/diffusion_models/z_image_turbo*
ls ComfyUI/models/text_encoders/qwen*
ls ComfyUI/models/vae/ae.safetensors
```

---

## Checklist de Sucesso

- [ ] ComfyUI rodando em http://127.0.0.1:8188
- [ ] KOKORO TTS instalado e funcionando
- [ ] Z-IMAGE-TURBO instalado com modelos
- [ ] Exemplo 1 de KOKORO funcionou
- [ ] Exemplo 1 de Z-IMAGE funcionou
- [ ] Outputs salvos corretamente
- [ ] Scripts Python com encoding UTF-8

---

## Próximos Passos

1. **Personalizar prompts:** Edite os textos/prompts nos scripts
2. **Criar novos exemplos:** Copie e modifique os existentes
3. **Integrar em automações:** Use as funções do `utils.py`
4. **Explorar parâmetros:** Experimente diferentes valores

---

📚 **Mais informações:** [README.md](README.md) | [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
