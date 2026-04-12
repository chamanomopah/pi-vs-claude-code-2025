#!/bin/bash
# Script para gerar um documento de arquitetura inicial

PROJECT_NAME=$1
OUTPUT_DIR="${2:-docs}"
TEMPLATE_DIR="$(dirname "$0")/../assets"

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: $0 <project-name> [output-dir]"
  exit 1
fi

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Copiar template
OUTPUT_FILE="$OUTPUT_DIR/arquitetura-$PROJECT_NAME.md"
cp "$TEMPLATE_DIR/architecture-template.md" "$OUTPUT_FILE"

# Substituir placeholders
sed -i "s/{DATE}/$(date +%Y-%m-%d)/g" "$OUTPUT_FILE"
sed -i "s/{AUTOR}/$(git config user.name 2>/dev/null || echo "Arquiteto")/g" "$OUTPUT_FILE"
sed -i "s/\[Nome do Projeto\]/$PROJECT_NAME/g" "$OUTPUT_FILE"

echo "Documento de arquitetura gerado: $OUTPUT_FILE"
echo "Preencha as seções marcadas com [colchetes]"
