#!/bin/bash
###############################################################################
# EXEMPLO 3 - KOKORO TTS: Upload de Áudio de Referência
# 
# Descrição: Faz upload de um áudio de referência para clonagem de voz
#           e gera novo áudio com a voz clonada
# 
# Requisitos:
#   - ComfyUI rodando em http://127.0.0.1:8188
#   - ComfyUI-Kokoro instalado
#   - Arquivo de áudio de referência (.wav ou .mp3)
# 
# Uso:
#   bash exemplo3_curl_upload.sh /caminho/do/audio_referencia.wav
# 
#   Se não fornecer caminho, usará áudio de teste
# 
# Saída: Áudio salvo em ComfyUI/user/outputs/YYYY-MM-DD/kokoro_tts/exemplo3_upload/
###############################################################################

# Configurações
COMFYUI_URL="http://127.0.0.1:8188"
CLIENT_ID="curl_kokoro_exemplo3"
OUTPUT_DIR="C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/outputs/$(date +%Y-%m-%d)/kokoro_tts/exemplo3_upload"

# Criar diretório de output
mkdir -p "$OUTPUT_DIR"

# Obter caminho do áudio de referência (argumento ou padrão)
REFERENCE_AUDIO="${1:-}"

echo "=== KOKORO TTS - Exemplo 3: Upload de Áudio de Referência ==="
echo ""

# Se não foi fornecido áudio, criar um de teste
if [ -z "$REFERENCE_AUDIO" ]; then
  echo "⚠ Nenhum áudio de referência fornecido."
  echo ""
  echo "Uso: bash exemplo3_curl_upload.sh /caminho/do/audio.wav"
  echo ""
  echo "Este exemplo requer um áudio de referência para clonagem de voz."
  echo "O workflow KOKORO suporta referência de áudio para voice cloning."
  echo ""
  echo "Para usar este exemplo:"
  echo "  1. Tenha um arquivo de áudio .wav ou .mp3"
  echo "  2. Execute: bash exemplo3_curl_upload.sh seu_audio.wav"
  echo ""
  echo "NOTA: O workflow KOKORO atual usa speakers pré-definidos."
  echo "      Para clonagem real de voz, pode ser necessário modificar o workflow."
  echo ""
  
  # Demonstrar com speaker fixo
  echo "Demonstrando com speaker fixo (sem upload de áudio)..."
  echo ""
  
  # Usar workflow padrão com speaker fixo
  TEXTO="Este é um teste de geração de áudio com Kokoro TTS usando speaker pré-definido."
  SPEAKER="am_onyx"
  SPEED=1.0
  LANG="Portuguese"
  
else
  # Verificar se arquivo existe
  if [ ! -f "$REFERENCE_AUDIO" ]; then
    echo "✗ Erro: Arquivo não encontrado: $REFERENCE_AUDIO"
    exit 1
  fi
  
  # Verificar extensão
  EXT="${REFERENCE_AUDIO##*.}"
  if [[ ! "$EXT" =~ ^(wav|mp3|ogg|flac)$ ]]; then
    echo "⚠ Aviso: Extensão .$EXT pode não ser suportada"
    echo "  Formatos recomendados: .wav, .mp3"
  fi
  
  echo "Arquivo de referência: $REFERENCE_AUDIO"
  FILE_SIZE=$(stat -c%s "$REFERENCE_AUDIO" 2>/dev/null || stat -f%z "$REFERENCE_AUDIO" 2>/dev/null)
  echo "Tamanho: $FILE_SIZE bytes"
  echo ""
  
  # Fazer upload do áudio
  echo "Fazendo upload do áudio..."
  
  # Determinar MIME type
  MIME_TYPE="audio/wav"
  if [ "$EXT" == "mp3" ]; then
    MIME_TYPE="audio/mpeg"
  elif [ "$EXT" == "ogg" ]; then
    MIME_TYPE="audio/ogg"
  elif [ "$EXT" == "flac" ]; then
    MIME_TYPE="audio/flac"
  fi
  
  # Upload via curl
  UPLOAD_RESPONSE=$(curl -s -X POST "$COMFYUI_URL/upload/audio" \
    -F "audio=@$REFERENCE_AUDIO;type=$MIME_TYPE" \
    -F "type=input")
  
  echo "Resposta do upload:"
  echo "$UPLOAD_RESPONSE" | jq '.'
  echo ""
  
  # Extrair nome do arquivo carregado
  UPLOADED_NAME=$(echo "$UPLOAD_RESPONSE" | jq -r '.name')
  
  if [ "$UPLOADED_NAME" == "null" ] || [ -z "$UPLOADED_NAME" ]; then
    echo "✗ Erro no upload do áudio"
    exit 1
  fi
  
  echo "✓ Upload realizado: $UPLOADED_NAME"
  echo ""
  
  # NOTA: O workflow KOKORO atual usa speakers fixos, não referência de áudio
  # Em um workflow real de voice cloning, haveria um nó para carregar o áudio
  # e extrair o embedding da voz
  
  echo "NOTA: O workflow atual do Kokoro usa speakers pré-definidos."
  echo "      Para usar o áudio carregado como referência de voz,"
  echo "      seria necessário modificar o workflow com nós adicionais."
  echo ""
  echo "Gerando áudio com speaker fixo (demonstração)..."
  echo ""
  
  TEXTO="Este é um teste de geração de áudio com Kokoro TTS."
  SPEAKER="am_onyx"
  SPEED=1.0
  LANG="Portuguese"
fi

# Construir JSON do workflow
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

echo "Parâmetros da geração:"
echo "  Texto: $TEXTO"
echo "  Speaker: $SPEAKER"
echo "  Velocidade: $SPEED"
echo "  Idioma: $LANG"
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
  echo "Aguardando processamento..."
  
  # Aguardar processamento
  sleep 8
  
  # Obter histórico
  HISTORY_RESPONSE=$(curl -s "$COMFYUI_URL/history/$PROMPT_ID")
  
  # Extrair filename
  AUDIO_FILENAME=$(echo "$HISTORY_RESPONSE" | jq -r ".[\"$PROMPT_ID\"].outputs // {} | to_entries[] | select(.value.audio != null) | .value.audio[0].filename" 2>/dev/null)
  
  if [ "$AUDIO_FILENAME" != "null" ] && [ -n "$AUDIO_FILENAME" ]; then
    echo "✓ Áudio gerado: $AUDIO_FILENAME"
    
    # Download
    curl -s "$COMFYUI_URL/view?filename=$AUDIO_FILENAME&subfolder=&type=output" \
      -o "$OUTPUT_DIR/$AUDIO_FILENAME"
    
    echo "✓ Arquivo salvo em: $OUTPUT_DIR/$AUDIO_FILENAME"
    
    FILE_SIZE=$(wc -c < "$OUTPUT_DIR/$AUDIO_FILENAME" 2>/dev/null || echo "0")
    echo "  Tamanho: $FILE_SIZE bytes"
  else
    echo "⚠ Não foi possível obter o arquivo. Verifique o ComfyUI."
  fi
else
  echo ""
  echo "✗ Erro ao enfileirar workflow"
fi

echo ""
echo "=== Fim do Exemplo 3 ==="
echo ""
echo "NOTA SOBRE VOICE CLONING:"
echo "Para implementar clonagem real de voz com Kokoro:"
echo "  1. O workflow precisa incluir nós para:"
echo "     - Carregar áudio de referência"
echo "     - Extrair embedding/speaker embedding do áudio"
echo "     - Passar o embedding para o KokoroGenerator"
echo "  2. Ou usar um workflow específico para voice cloning"
echo "  3. Verifique a documentação do ComfyUI-Kokoro para detalhes"
