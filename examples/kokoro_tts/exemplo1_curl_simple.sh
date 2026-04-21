#!/bin/bash
###############################################################################
# EXEMPLO 1 - KOKORO TTS: Texto Simples em Português
# 
# Descrição: Gera um áudio a partir de um texto simples em português
# 
# Requisitos:
#   - ComfyUI rodando em http://127.0.0.1:8188
#   - ComfyUI-Kokoro instalado
# 
# Uso:
#   bash exemplo1_curl_simple.sh
# 
# Saída: Áudio salvo em ComfyUI/user/outputs/YYYY-MM-DD/kokoro_tts/exemplo1_simples/
###############################################################################

# Configurações
COMFYUI_URL="http://127.0.0.1:8188"
CLIENT_ID="curl_kokoro_exemplo1"
OUTPUT_DIR="C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/outputs/$(date +%Y-%m-%d)/kokoro_tts/exemplo1_simples"

# Criar diretório de output
mkdir -p "$OUTPUT_DIR"

echo "=== KOKORO TTS - Exemplo 1: Texto Simples ==="
echo "Enviando requisição para ComfyUI..."

# JSON do workflow para KOKORO TTS
# Estrutura baseada no workflow WORKFLOW - KOKORO.json
# - Node 10: KokoroSpeaker (seleção de voz)
# - Node 11: KokoroGenerator (geração de áudio)
# - Node 12: PreviewAudio (preview/preview do áudio)

# Payload JSON - Workflow com texto em português
JSON_PAYLOAD='{
  "10": {
    "inputs": {
      "speaker_name": "am_onyx"
    },
    "class_type": "KokoroSpeaker"
  },
  "11": {
    "inputs": {
      "speaker": [
        "10",
        0
      ],
      "text": "Olá, mundo! Este é um teste de automação do Kokoro TTS.",
      "speed": 1,
      "lang": "Portuguese"
    },
    "class_type": "KokoroGenerator"
  },
  "12": {
    "inputs": {
      "audio": [
        "11",
        0
      ]
    },
    "class_type": "PreviewAudio"
  }
}'

# Enviar requisição para ComfyUI
# Endpoint: /prompt
# Método: POST
# Headers: Content-Type: application/json

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
  echo "  Client ID: $CLIENT_ID"
  echo ""
  echo "Aguardando processamento..."
  
  # Aguardar alguns segundos para processamento
  sleep 5
  
  # Obter histórico para pegar nome do arquivo gerado
  HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
  
  # Extrair filename do áudio gerado
  AUDIO_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r '.[$PROMPT_ID].outputs | to_entries[] | select(.value.audio != null) | .value.audio[0].filename')
  
  if [ "$AUDIO_FILENAME" != "null" ] && [ -n "$AUDIO_FILENAME" ]; then
    echo "✓ Áudio gerado: $AUDIO_FILENAME"
    
    # Download do áudio
    # Endpoint: /view
    # Parâmetros: filename, subfolder, type
    
    SUBFOLDER=""
    TYPE="output"
    
    echo "Baixando áudio..."
    curl -s "$COMFYUI_URL/view?filename=$AUDIO_FILENAME&subfolder=$SUBFOLDER&type=$TYPE" \
      -o "$OUTPUT_DIR/$AUDIO_FILENAME"
    
    echo "✓ Arquivo salvo em: $OUTPUT_DIR/$AUDIO_FILENAME"
  else
    echo "⚠ Aguardando mais tempo para processamento..."
    sleep 5
    
    # Tentar novamente
    HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
    AUDIO_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r '.[$PROMPT_ID].outputs | to_entries[] | select(.value.audio != null) | .value.audio[0].filename')
    
    if [ "$AUDIO_FILENAME" != "null" ] && [ -n "$AUDIO_FILENAME" ]; then
      echo "✓ Áudio gerado: $AUDIO_FILENAME"
      curl -s "$COMFYUI_URL/view?filename=$AUDIO_FILENAME&subfolder=$SUBFOLDER&type=$TYPE" \
        -o "$OUTPUT_DIR/$AUDIO_FILENAME"
      echo "✓ Arquivo salvo em: $OUTPUT_DIR/$AUDIO_FILENAME"
    else
      echo "⚠ Não foi possível obter o arquivo. Verifique manualmente no ComfyUI."
    fi
  fi
else
  echo ""
  echo "✗ Erro ao enfileirar workflow"
  echo "Verifique se:"
  echo "  1. ComfyUI está rodando em $COMFYUI_URL"
  echo "  2. ComfyUI-Kokoro está instalado"
  echo "  3. Não há erros de dependência"
fi

echo ""
echo "=== Fim do Exemplo 1 ==="
