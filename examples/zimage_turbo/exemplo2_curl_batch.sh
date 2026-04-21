#!/bin/bash
###############################################################################
# EXEMPLO 2 - Z-IMAGE-TURBO: Variações de Prompt (Batch)
# 
# Descrição: Gera múltiplas imagens a partir de uma lista de prompts
#           Processa cada prompt sequencialmente
# 
# Requisitos:
#   - ComfyUI rodando em http://127.0.0.1:8188
#   - Z-Image-Turbo instalado com modelos necessários
#   - Utilitário jq para parsing JSON
# 
# Uso:
#   bash exemplo2_curl_batch.sh
# 
# Saída: Imagens salvas em ComfyUI/user/outputs/YYYY-MM-DD/zimage_turbo/exemplo2_batch/
###############################################################################

# Configurações
COMFYUI_URL="http://127.0.0.1:8188"
OUTPUT_BASE_DIR="C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/outputs/$(date +%Y-%m-%d)/zimage_turbo/exemplo2_batch"

# Criar diretório de output
mkdir -p "$OUTPUT_BASE_DIR"

echo "=== Z-IMAGE-TURBO - Exemplo 2: Batch de Prompts ==="
echo ""

# Array de prompts para processar
# Cada prompt gerará uma imagem diferente
declare -a PROMPTS=(
  "Um dragão feito de cristal voando sobre montanhas nevadas ao pôr do sol, estilo fantasia épica"
  "Um robô amigável servindo café em uma cafeteria futurista, iluminação neon, anos 80"
  "Uma floresta mágica com cogumelos luminosos e fadas dançando, noturno, cênico"
)

# Configurações de geração
WIDTH=1024
HEIGHT=1024
STEPS=8

echo "Configurações:"
echo "  Dimensões: ${WIDTH}x${HEIGHT}"
echo "  Steps: $STEPS"
echo "  Quantidade de prompts: ${#PROMPTS[@]}"
echo ""

# Função para enviar requisição de geração de imagem
# Args: $1 = índice do prompt, $2 = prompt
gerar_imagem() {
  local INDEX=$1
  local PROMPT=$2
  local CLIENT_ID="curl_zimage_batch_$INDEX"
  
  echo "----------------------------------------"
  echo "Processando prompt #$((INDEX + 1)):"
  echo "  Prompt: $PROMPT"
  echo ""
  
  # Escapar prompt para JSON
  PROMPT_ESCAPED=$(echo "$PROMPT" | jq -Rs .)
  
  # Gerar seed aleatório para variação
  SEED=$((RANDOM % 1000000000))
  
  # Construir JSON do workflow
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
  
  # Enviar requisição
  echo "  Enviando para ComfyUI..."
  RESPONSE=$(curl -s -X POST "$COMFYUI_URL/prompt" \
    -H "Content-Type: application/json" \
    -d "{
      \"prompt\": $JSON_PAYLOAD,
      \"client_id\": \"$CLIENT_ID\"
    }")
  
  # Extrair prompt_id
  PROMPT_ID=$(echo "$RESPONSE" | jq -r '.prompt_id')
  
  if [ "$PROMPT_ID" != "null" ] && [ -n "$PROMPT_ID" ]; then
    echo "  ✓ Enfileirado (Prompt ID: $PROMPT_ID)"
    
    # Aguardar processamento (geração de imagem demora)
    echo "  ⏳ Aguardando processamento..."
    
    MAX_WAIT=60
    WAIT_TIME=0
    IMAGE_FILENAME=""
    
    while [ $WAIT_TIME -lt $MAX_WAIT ]; do
      sleep 5
      WAIT_TIME=$((WAIT_TIME + 5))
      echo "    Aguardando... (${WAIT_TIME}s)"
      
      # Obter histórico
      HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
      
      # Tentar extrair filename
      IMAGE_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r ".[\"$PROMPT_ID\"].outputs // {} | to_entries[] | select(.value.images != null) | .value.images[0].filename" 2>/dev/null)
      
      if [ "$IMAGE_FILENAME" != "null" ] && [ -n "$IMAGE_FILENAME" ]; then
        break
      fi
    done
    
    if [ "$IMAGE_FILENAME" != "null" ] && [ -n "$IMAGE_FILENAME" ]; then
      # Nome do arquivo de output
      # Extrair extensão
      EXT="${IMAGE_FILENAME##*.}"
      OUTPUT_FILENAME="imagem_${INDEX}_$(echo "$PROMPT" | cut -c1-15 | tr ' ' '_').${EXT}"
      
      # Download da imagem
      echo "  Baixando imagem..."
      curl -s "$COMFYUI_URL/view?filename=$IMAGE_FILENAME&subfolder=&type=output" \
        -o "$OUTPUT_BASE_DIR/$OUTPUT_FILENAME"
      
      if [ -f "$OUTPUT_BASE_DIR/$OUTPUT_FILENAME" ]; then
        FILE_SIZE=$(wc -c < "$OUTPUT_BASE_DIR/$OUTPUT_FILENAME" 2>/dev/null || echo "0")
        FILE_SIZE_KB=$((FILE_SIZE / 1024))
        echo "  ✓ Sucesso! Arquivo: $OUTPUT_FILENAME (${FILE_SIZE_KB} KB)"
      else
        echo "  ⚠ Erro no download do arquivo"
      fi
    else
      echo "  ⚠ Timeout: não foi possível obter a imagem"
    fi
    
  else
    echo "  ✗ Erro ao enfileirar"
    echo "  Resposta: $RESPONSE"
  fi
  
  echo ""
}

# Loop principal - processar cada prompt
TOTAL=${#PROMPTS[@]}

echo "Iniciando processamento batch..."
echo "Total de imagens a gerar: $TOTAL"
echo "Tempo estimado: $((TOTAL * 20)) segundos"
echo ""

for i in $(seq 0 $((TOTAL - 1))); do
  echo "=== Imagem $((i + 1)) de $TOTAL ==="
  gerar_imagem "$i" "${PROMPTS[$i]}"
  
  # Pequena pausa entre requisições para não sobrecarregar
  if [ $i -lt $((TOTAL - 1)) ]; then
    echo "Aguardando 3 segundos antes da próxima requisição..."
    sleep 3
  fi
done

echo "========================================"
echo "Resumo do Processamento Batch:"
echo "  Total de prompts: $TOTAL"
echo "  Diretório de output: $OUTPUT_BASE_DIR"
echo ""

# Listar arquivos gerados
echo "Arquivos gerados:"
ls -lh "$OUTPUT_BASE_DIR" 2>/dev/null | grep -v "^total" | awk '{print "  🖼️  " $9 " (" $5 ")"}'

echo ""
echo "=== Fim do Exemplo 2 ==="
echo ""
echo "DICA: Você pode variar os prompts para explorar diferentes estilos"
echo "      e temas do Z-Image-TurBO!"
