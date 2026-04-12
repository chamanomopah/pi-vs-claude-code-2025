#!/bin/bash
# Script para validar um documento de arquitetura

ARCH_FILE=$1

if [ -z "$ARCH_FILE" ]; then
  echo "Usage: $0 <arquivo-arquitetura.md>"
  exit 1
fi

if [ ! -f "$ARCH_FILE" ]; then
  echo "Erro: Arquivo não encontrado: $ARCH_FILE"
  exit 1
fi

echo "=== Validando documento de arquitetura: $ARCH_FILE ==="
echo ""

# Seções obrigatórias
sections=(
  "Visão Geral"
  "Requisitos Funcionais"
  "Requisitos Não-Funcionais"
  "Stack Tecnológico"
  "Arquitetura de Componentes"
  "Arquitetura de Dados"
  "Segurança"
  "Deploy e Infraestrutura"
)

missing=0
found=0

for section in "${sections[@]}"; do
  if grep -q "^##[[:space:]]*$section" "$ARCH_FILE"; then
    echo "✓ Seção encontrada: $section"
    ((found++))
  else
    echo "✗ Seção faltando: $section"
    ((missing++))
  fi
done

echo ""
echo "=== Resumo ==="
echo "Seções encontradas: $found/${#sections[@]}"
echo "Seções faltando: $missing"

if [ $missing -eq 0 ]; then
  echo ""
  echo "✓ Documento válido! Agora execute:"
  echo "  /skill:arquiteto-anti-halucinacao validate $ARCH_FILE"
  exit 0
else
  echo ""
  echo "✗ Documento incompleto. Adicione as seções faltando."
  exit 1
fi
