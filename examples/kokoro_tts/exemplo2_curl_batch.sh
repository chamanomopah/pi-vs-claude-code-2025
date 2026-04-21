#!/bin/bash
###############################################################################
# EXEMPLO 2 - KOKORO TTS: Múltiplos Textos (Batch)
# 
# Descrição: Gera múltiplos áudios a partir de uma lista de textos
#           Processa cada texto sequencialmente
# 
# Requisitos:
#   - ComfyUI rodando em http://127.0.0.1:8188
#   - ComfyUI-Kokoro instalado
#   - Utilitário jq para parsing JSON
# 
# Uso:
#   bash exemplo2_curl_batch.sh
# 
# Saída: Áudios salvos em ComfyUI/user/outputs/YYYY-MM-DD/kokoro_tts/exemplo2_batch/
###############################################################################

# Configurações
COMFYUI_URL="http://127.0.0.1:8188"
OUTPUT_BASE_DIR="C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/outputs/$(date +%Y-%m-%d)/kokoro_tts/exemplo2_batch"

# Criar diretório de output
mkdir -p "$OUTPUT_BASE_DIR"

echo "=== KOKORO TTS - Exemplo 2: Batch de Textos ==="
echo ""

# Array de textos para processar
# Cada texto será convertido em um áudio separado
declare -a TEXTOS=(
  "Bom dia! Esta é a primeira mensagem do teste batch."
  "Esta é a segunda mensagem. Estamos testando processamento em lote."
  "Terceira e última mensagem do teste batch do Kokoro TTS."
)

# Configurações de geração
SPEAKER="am_onyx"
SPEED=1.0
LANG="Portuguese"

echo "Configurações:"
echo "  Speaker: $SPEAKER"
echo "  Velocidade: $SPEED"
echo "  Idioma: $LANG"
echo "  Quantidade de textos: ${#TEXTOS[@]}"
echo ""

# Função para enviar requisição TTS
# Args: $1 = índice do texto, $2 = texto
enviar_tts() {
  local INDEX=$1
  local TEXTO=$2
  local CLIENT_ID="curl_kokoro_batch_$INDEX"
  
  echo "----------------------------------------"
  echo "Processando texto #$((INDEX + 1)):"
  echo "  Texto: $TEXTO"
  echo ""
  
  # Construir JSON do workflow
  # O texto precisa ser escapado corretamente para JSON
  TEXTO_ESCAPED=$(echo "$TEXTO" | jq -Rs .)
  
  JSON_PAYLOAD="{
    \"10\": {
      \"inputs\": {
        \"speaker_name\": \"$SPEAKER\"
      },
      \"class_type\": \"KokoroSpeaker\"
    },
    \"11\": {
      \"inputs\": {
        \"speaker\": [\"10\", 0],
        \"text\": $TEXTO_ESCAPED,
        \"speed\": $SPEED,
        \"lang\": \"$LANG\"
      },
      \"class_type\": \"KokoroGenerator\"
    },
    \"12\": {
      \"inputs\": {
        \"audio\": [\"11\", 0]
      },
      \"class_type\": \"PreviewAudio\"
    }
  }"
  
  # Enviar requisição
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
    
    # Aguardar processamento
    echo "  ⏳ Aguardando processamento..."
    
    # Loop para verificar se terminou
    MAX_WAIT=30
    WAIT_TIME=0
    AUDIO_FILENAME=""
    
    while [ $WAIT_TIME -lt $MAX_WAIT ]; do
      sleep 2
      WAIT_TIME=$((WAIT_TIME + 2))
      
      # Obter histórico
      HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
      
      # Tentar extrair filename
      AUDIO_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r ".[\"$PROMPT_ID\"].outputs // {} | to_entries[] | select(.value.audio != null) | .value.audio[0].filename" 2>/dev/null)
      
      if [ "$AUDIO_FILENAME" != "null" ] && [ -n "$AUDIO_FILENAME" ]; then
        break
      fi
    done
    
    if [ "$AUDIO_FILENAME" != "null" ] && [ -n "$AUDIO_FILENAME" ]; then
      # Nome do arquivo de output
      OUTPUT_FILENAME="audio_${INDEX}_$(echo "$TEXTO" | cut -c1-20 | tr ' ' '_').wav"
      
      # Download do áudio
      curl -s "$COMFYUI_URL/view?filename=$AUDIO_FILENAME&subfolder=&type=output" \
        -o "$OUTPUT_BASE_DIR/$OUTPUT_FILENAME"
      
      if [ -f "$OUTPUT_BASE_DIR/$OUTPUT_FILENAME" ]; then
        FILE_SIZE=$(wc -c < "$OUTPUT_BASE_DIR/$OUTPUT_FILENAME" 2>/dev/null)
        echo "  ✓ Sucesso! Arquivo: $OUTPUT_FILENAME ($FILE_SIZE bytes)"
      else
        echo "  ⚠ Erro no download do arquivo"
      fi
    else
      echo "  ⚠ Timeout: não foi possível obter o áudio"
    fi
    
  else
    echo "  ✗ Erro ao enfileirar"
    echo "  Resposta: $RESPONSE"
  fi
  
  echo ""
}

# Loop principal - processar cada texto
TOTAL=${#TEXTOS[@]}

for i in $(seq 0 $((TOTAL - 1))); do
  echo "=== Texto $((i + 1)) de $TOTAL ==="
  enviar_tts "$i" "${TEXTOS[$i]}"
  
  # Pequena pausa entre requisições
  if [ $i -lt $((TOTAL - 1)) ]; then
    sleep 1
  fi
done

echo "========================================"
echo "Resumo do Processamento Batch:"
echo "  Total de textos: $TOTAL"
echo "  Diretório de output: $OUTPUT_BASE_DIR"
echo ""

# Listar arquivos gerados
echo "Arquivos gerados:"
ls -lh "$OUTPUT_BASE_DIR" 2>/dev/null | grep -v "^total" | awk '{print "  📄 " $9 " (" $5 ")"}'

echo ""
echo "=== Fim do Exemplo 2 ==="
