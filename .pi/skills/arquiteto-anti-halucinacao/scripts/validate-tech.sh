#!/bin/bash
# Script para validar existência de uma tecnologia

TECH_NAME=$1
VERSION=${2:-""}

if [ -z "$TECH_NAME" ]; then
  echo "Usage: $0 <technology-name> [version]"
  exit 1
fi

echo "=== Validando tecnologia: $TECH_NAME ${VERSION:+v$VERSION} ==="
echo ""

# Tentar NPM
echo "1. Checando NPM..."
if npm view "$TECH_NAME" 2>/dev/null | grep -q "name"; then
  echo "   ✓ Encontrado em NPM"
  if [ -n "$VERSION" ]; then
    if npm view "$TECH_NAME" versions --json 2>/dev/null | grep -q "\"$VERSION\""; then
      echo "   ✓ Versão $VERSION existe"
    else
      echo "   ✗ Versão $VERSION NÃO encontrada"
      echo "   Versões disponíveis:"
      npm view "$TECH_NAME" versions --json 2>/dev/null | tail -5
    fi
  fi
else
  echo "   ✗ Não encontrado em NPM"
fi

# Tentar PyPI
echo ""
echo "2. Checando PyPI..."
if curl -s "https://pypi.org/pypi/$TECH_NAME/json" | grep -q "\"name\""; then
  echo "   ✓ Encontrado em PyPI"
  if [ -n "$VERSION" ]; then
    if curl -s "https://pypi.org/pypi/$TECH_NAME/$VERSION/json" | grep -q "\"name\""; then
      echo "   ✓ Versão $VERSION existe"
    else
      echo "   ✗ Versão $VERSION NÃO encontrada"
    fi
  fi
else
  echo "   ✗ Não encontrado em PyPI"
fi

# Tentar GitHub
echo ""
echo "3. Checando GitHub..."
GITHUB_SEARCH=$(curl -s "https://api.github.com/search/repositories?q=$TECH_NAME&per_page=1" | grep -o "\"full_name\":[^,]*" | head -1)
if [ -n "$GITHUB_SEARCH" ]; then
  echo "   ✓ Encontrado no GitHub"
else
  echo "   ✗ Não encontrado no GitHub"
fi

echo ""
echo "=== Validação concluída ==="
