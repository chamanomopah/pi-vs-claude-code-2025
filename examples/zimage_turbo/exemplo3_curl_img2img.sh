#!/bin/bash
###############################################################################
# EXEMPLO 3 - Z-IMAGE-TURBO: Upload de Imagem + img2img
# 
# Descrição: Faz upload de uma imagem de referência e gera uma nova imagem
#           baseada nela (Image-to-Image)
# 
# Requisitos:
#   - ComfyUI rodando em http://127.0.0.1:8188
#   - Z-Image-Turbo instalado com modelos necessários
#   - Arquivo de imagem de referência (.png ou .jpg)
# 
# Uso:
#   bash exemplo3_curl_img2img.sh /caminho/da/imagem_referencia.jpg
# 
#   Se não fornecer caminho, usará prompt de texto (sem upload)
# 
# Saída: Imagem salva em ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo3_img2img/
###############################################################################

# Configurações
COMFYUI_URL="http://127.0.0.1:8188"
CLIENT_ID="curl_zimage_exemplo3"
OUTPUT_DIR="C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/outputs/$(date +%Y-%m-%d)/zimage_turbo/exemplo3_img2img"

# Criar diretório de output
mkdir -p "$OUTPUT_DIR"

# Obter caminho da imagem de referência (argumento ou padrão)
REFERENCE_IMAGE="${1:-}"

echo "=== Z-IMAGE-TURBO - Exemplo 3: Upload de Imagem + img2img ==="
echo ""

# Se não foi fornecida imagem, demonstrar com prompt de texto
if [ -z "$REFERENCE_IMAGE" ]; then
  echo "⚠ Nenhuma imagem de referência fornecida."
  echo ""
  echo "Uso: bash exemplo3_curl_img2img.sh /caminho/da/imagem.jpg"
  echo ""
  echo "Este exemplo pode funcionar de duas formas:"
  echo "  1. Com upload de imagem: Image-to-Image"
  echo "  2. Sem imagem: Text-to-Image (demonstração abaixo)"
  echo ""
  echo "NOTA: O workflow Z-IMAGE-TURBO atual é focado em Text-to-Image."
  echo "      Para Image-to-Image completo, seria necessário adicionar:"
  echo "      - Nó LoadImage para carregar a imagem"
  echo "      - Nó ImageToLatent para converter para latente"
  echo "      - Conectar ao KSampler com parâmetro denoise < 1.0"
  echo ""
  
  # Demonstrar com prompt de texto
  echo "Demonstrando com Text-to-Image (sem upload de imagem)..."
  echo ""
  
  PROMPT="Um castelo flutuante nas nuvens ao pôr do sol, estilo Studio Ghibli"
  WIDTH=1024
  HEIGHT=1024
  STEPS=8
  HAS_IMAGE=false
  
else
  # Verificar se arquivo existe
  if [ ! -f "$REFERENCE_IMAGE" ]; then
    echo "✗ Erro: Arquivo não encontrado: $REFERENCE_IMAGE"
    exit 1
  fi
  
  # Verificar extensão
  EXT="${REFERENCE_IMAGE##*.}"
  if [[ ! "$EXT" =~ ^(png|jpg|jpeg|webp)$ ]]; then
    echo "⚠ Aviso: Extensão .$EXT pode não ser suportada"
    echo "  Formatos recomendados: .png, .jpg, .jpeg, .webp"
  fi
  
  echo "Arquivo de referência: $REFERENCE_IMAGE"
  FILE_SIZE=$(stat -c%s "$REFERENCE_IMAGE" 2>/dev/null || stat -f%z "$REFERENCE_IMAGE" 2>/dev/null)
  echo "Tamanho: $FILE_SIZE bytes"
  echo ""
  
  # Fazer upload da imagem
  echo "Fazendo upload da imagem..."
  
  # Determinar MIME type
  MIME_TYPE="image/png"
  if [ "$EXT" == "jpg" ] || [ "$EXT" == "jpeg" ]; then
    MIME_TYPE="image/jpeg"
  elif [ "$EXT" == "webp" ]; then
    MIME_TYPE="image/webp"
  fi
  
  # Upload via curl
  UPLOAD_RESPONSE=$(curl -s -X POST "$COMFYUI_URL/upload/image" \
    -F "image=@$REFERENCE_IMAGE;type=$MIME_TYPE" \
    -F "type=input")
  
  echo "Resposta do upload:"
  echo "$UPLOAD_RESPONSE" | jq '.'
  echo ""
  
  # Extrair nome do arquivo carregado
  UPLOADED_NAME=$(echo "$UPLOAD_RESPONSE" | jq -r '.name')
  UPLOADED_SUBFOLDER=$(echo "$UPLOAD_RESPONSE" | jq -r '.subfolder // ""')
  
  if [ "$UPLOADED_NAME" == "null" ] || [ -z "$UPLOADED_NAME" ]; then
    echo "✗ Erro no upload da imagem"
    exit 1
  fi
  
  echo "✓ Upload realizado: $UPLOADED_NAME"
  echo ""
  
  # NOTA: O workflow Z-IMAGE-TURBO atual é Text-to-Image
  # Para img2img real, precisaríamos modificar o workflow
  echo "NOTA: O workflow atual do Z-Image-Turbo é Text-to-Image."
  echo "      Para usar a imagem carregada em img2img, seria necessário:"
  echo "      1. Adicionar nó LoadImage"
  echo "      2. Adicionar nó ImageToLatent (com parâmetro denoise < 1.0)"
  echo "      3. Conectar ao KSampler"
  echo ""
  echo "Gerando imagem com prompt de texto (demonstração)..."
  echo ""
  
  PROMPT="Transformar a cena em uma versão artística abstrata"
  WIDTH=1024
  HEIGHT=1024
  STEPS=8
  HAS_IMAGE=true
fi

# Construir JSON do workflow
PROMPT_ESCAPED=$(echo "$PROMPT" | jq -Rs .)

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

echo "Parâmetros da geração:"
echo "  Prompt: $PROMPT"
echo "  Dimensões: ${WIDTH}x${HEIGHT}"
echo "  Steps: $STEPS"
if [ "$HAS_IMAGE" = true ]; then
  echo "  Imagem carregada: $UPLOADED_NAME (não usada no workflow atual)"
fi
echo ""

# Enviar requisição
echo "Enviando requisição para ComfyUI..."

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
  
  # Aguardar processamento
  sleep 20
  
  # Obter histórico
  HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
  
  # Extrair filename
  IMAGE_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r ".[\"$PROMPT_ID\"].outputs // {} | to_entries[] | select(.value.images != null) | .value.images[0].filename" 2>/dev/null)
  
  if [ "$IMAGE_FILENAME" != "null" ] && [ -n "$IMAGE_FILENAME" ]; then
    echo "✓ Imagem gerada: $IMAGE_FILENAME"
    
    # Download
    curl -s "$COMFYUI_URL/view?filename=$IMAGE_FILENAME&subfolder=&type=output" \
      -o "$OUTPUT_DIR/$IMAGE_FILENAME"
    
    if [ -f "$OUTPUT_DIR/$IMAGE_FILENAME" ]; then
      FILE_SIZE=$(wc -c < "$OUTPUT_DIR/$IMAGE_FILENAME" 2>/dev/null || echo "0")
      FILE_SIZE_KB=$((FILE_SIZE / 1024))
      echo "✓ Arquivo salvo em: $OUTPUT_DIR/$IMAGE_FILENAME"
      echo "  Tamanho: ${FILE_SIZE_KB} KB"
    else
      echo "✗ Erro no download do arquivo"
    fi
  else
    echo "⚠ Não foi possível obter a imagem. Verifique o ComfyUI."
  fi
else
  echo ""
  echo "✗ Erro ao enfileirar workflow"
fi

echo ""
echo "=== Fim do Exemplo 3 ==="
echo ""
echo "NOTA SOBRE IMG2IMG:"
echo "Para implementar Image-to-Image completo com Z-Image-Turbo:"
echo "  1. O workflow precisa incluir nós para:"
echo "     - LoadImage: carregar a imagem de entrada"
echo "     - VAEEncode (ou ImageToLatent): converter para latente"
echo "     - KSampler com denoise < 1.0 (ex: 0.7 para preservar características)"
echo "  2. Ou usar um workflow específico para img2img"
echo "  3. O workflow atual é Text-to-Image puro"
echo ""
echo "Este exemplo demonstra o processo de upload e a estrutura necessária."
