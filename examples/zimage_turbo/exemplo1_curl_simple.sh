#!/bin/bash
###############################################################################
# EXEMPLO 1 - Z-IMAGE-TURBO: Texto para Imagem Simples
# 
# Descrição: Gera uma imagem a partir de um prompt de texto simples
# 
# Requisitos:
#   - ComfyUI rodando em http://127.0.0.1:8188
#   - Z-Image-Turbo instalado com modelos necessários:
#     * z_image_turbo_bf16.safetensors (diffusion model)
#     * qwen_3_4b.safetensors (text encoder)
#     * ae.safetensors (VAE)
# 
# Uso:
#   bash exemplo1_curl_simple.sh
# 
# Saída: Imagem salva em ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo1_simples/
###############################################################################

# Configurações
COMFYUI_URL="http://127.0.0.1:8188"
CLIENT_ID="curl_zimage_exemplo1"
OUTPUT_DIR="C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/outputs/$(date +%Y-%m-%d)/zimage_turbo/exemplo1_simples"

# Criar diretório de output
mkdir -p "$OUTPUT_DIR"

echo "=== Z-IMAGE-TURBO - Exemplo 1: Texto para Imagem Simples ==="
echo ""

# Prompt para geração de imagem
PROMPT="Um gato astronauta flutuando no espaço sideral, com a Terra ao fundo, estilo arte digital, cores vibrantes, alta qualidade"

# Parâmetros de geração
WIDTH=1024
HEIGHT=1024
STEPS=8
SEED=123456789

echo "Parâmetros da geração:"
echo "  Prompt: $PROMPT"
echo "  Dimensões: ${WIDTH}x${HEIGHT}"
echo "  Steps: $STEPS"
echo "  Seed: $SEED"
echo ""

# Escape do prompt para JSON
PROMPT_ESCAPED=$(echo "$PROMPT" | jq -Rs .)

# JSON do workflow para Z-IMAGE-TURBO
# Estrutura baseada no workflow WORKFLOW - Z-IMAGE-TURBO.json
# - Node 57: Grupo principal (subgraph com nós internos)
#   - Node 13: EmptySD3LatentImage (imagem latente vazia)
#   - Node 27: CLIPTextEncode (codificar prompt)
#   - Node 28: UNETLoader (carregar modelo de difusão)
#   - Node 29: VAELoader (carregar VAE)
#   - Node 30: CLIPLoader (carregar text encoder)
#   - Node 3: KSampler (sampler para geração)
#   - Node 8: VAEDecode (decodificar latente)
#   - Node 11: ModelSamplingAuraFlow (configurar sampling)
#   - Node 33: ConditioningZeroOut (negative prompt)
# - Node 9: SaveImage (salvar imagem)

# Payload JSON
# NOTA: Z-Image-Turbo usa subgraphs, então a estrutura é mais complexa
# Os inputs do nó 57 são mapeados para os nós internos do subgraph

JSON_PAYLOAD="{
  \"57\": {
    \"inputs\": {
      \"text\": $PROMPT_ESCAPED,
      \"width\": $WIDTH,
      \"height\": $HEIGHT,
      \"steps\": $STEPS,
      \"unet_name\": \"z_image_turbo_bf16.safetensors\",
      \"clip_name\": \"qwen_3_4b.safetensors\",
      \"vae_name\": \"ae.safetensors\"
    },
    \"class_type\": \"f2fdebf6-dfaf-43b6-9eb2-7f70613cfdc1\"
  },
  \"9\": {
    \"inputs\": {
      \"images\": [\"57\", 0],
      \"filename_prefix\": \"z-image-turbo\"
    },
    \"class_type\": \"SaveImage\"
  }
}"

echo "Enviando requisição para ComfyUI..."

# Enviar requisição
RESPONSE=$(curl -s -X POST "$COMFYUI_URL/prompt" \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": $JSON_PAYLOAD,
    \"client_id\": \"$CLIENT_ID\"
  }")

echo "Resposta do servidor:"
echo "$RESPONSE" | jq '.'

# Extrair prompt_id
PROMPT_ID=$(echo "$RESPONSE" | jq -r '.prompt_id')

if [ "$PROMPT_ID" != "null" ] && [ -n "$PROMPT_ID" ]; then
  echo ""
  echo "✓ Workflow enfileirado com sucesso!"
  echo "  Prompt ID: $PROMPT_ID"
  echo ""
  echo "⏳ Aguardando processamento..."
  echo "  (Isso pode levar 10-30 segundos dependendo do hardware)"
  echo ""
  
  # Aguardar mais tempo pois geração de imagem demora
  sleep 15
  
  # Obter histórico
  HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
  
  # Verificar status
  STATUS=$(echo "$HISTORY_RESPONSE" | jq -r ".[\"$PROMPT_ID\"].status //.status" 2>/dev/null)
  
  # Tentar extrair filename da imagem
  IMAGE_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r ".[\"$PROMPT_ID\"].outputs // {} | to_entries[] | select(.value.images != null) | .value.images[0].filename" 2>/dev/null)
  
  # Se não encontrou, tentar novamente após mais tempo
  if [ "$IMAGE_FILENAME" == "null" ] || [ -z "$IMAGE_FILENAME" ]; then
    echo "  Ainda processando... aguardando mais 15 segundos..."
    sleep 15
    
    HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
    IMAGE_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r ".[\"$PROMPT_ID\"].outputs // {} | to_entries[] | select(.value.images != null) | .value.images[0].filename" 2>/dev/null)
  fi
  
  if [ "$IMAGE_FILENAME" != "null" ] && [ -n "$IMAGE_FILENAME" ]; then
    echo "✓ Imagem gerada: $IMAGE_FILENAME"
    
    # Download da imagem
    SUBFOLDER=""
    TYPE="output"
    
    echo "Baixando imagem..."
    curl -s "$COMFYUI_URL/view?filename=$IMAGE_FILENAME&subfolder=$SUBFOLDER&type=$TYPE" \
      -o "$OUTPUT_DIR/$IMAGE_FILENAME"
    
    if [ -f "$OUTPUT_DIR/$IMAGE_FILENAME" ]; then
      FILE_SIZE=$(wc -c < "$OUTPUT_DIR/$IMAGE_FILENAME" 2>/dev/null || echo "0")
      echo "✓ Arquivo salvo em: $OUTPUT_DIR/$IMAGE_FILENAME"
      echo "  Tamanho: $FILE_SIZE bytes"
      
      # Converter tamanho para KB
      FILE_SIZE_KB=$((FILE_SIZE / 1024))
      echo "  Tamanho: ${FILE_SIZE_KB} KB"
    else
      echo "✗ Erro no download do arquivo"
    fi
  else
    echo "⚠ Não foi possível obter a imagem."
    echo ""
    echo "Possíveis causas:"
    echo "  1. A geração ainda está em andamento (aguarde mais)"
    echo "  2. Os modelos não estão instalados corretamente"
    echo "  3. Erro na execução do workflow"
    echo ""
    echo "Verifique o ComfyUI para ver o status da execução."
  fi
else
  echo ""
  echo "✗ Erro ao enfileirar workflow"
  echo ""
  echo "Verifique se:"
  echo "  1. ComfyUI está rodando em $COMFYUI_URL"
  echo "  2. Z-Image-Turbo está instalado"
  echo "  3. Os modelos necessários estão presentes:"
  echo "     - diffusion_models/z_image_turbo_bf16.safetensors"
  echo "     - text_encoders/qwen_3_4b.safetensors"
  echo "     - vae/ae.safetensors"
fi

echo ""
echo "=== Fim do Exemplo 1 ==="
