#!/bin/bash
###############################################################################
# TESTE RÁPIDO - Verificar se os exemplos estão funcionando
#
# Este script executa testes básicos para verificar se tudo está funcionando.
#
# Uso: bash teste_rapido.sh
###############################################################################

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                    TESTE RÁPIDO DOS EXEMPLOS                             ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
SUCESSO=0
FALHA=0
WARNING=0

# Função para teste
testar() {
  local descricao=$1
  local comando=$2
  
  echo "Testing: $descricao"
  echo "Comando: $comando"
  
  if eval "$comando" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ SUCESSO${NC}"
    ((SUCESSO++))
  else
    echo -e "${RED}✗ FALHOU${NC}"
    ((FALHA++))
  fi
  echo ""
}

# Função para warning
warning() {
  local descricao=$1
  echo -e "${YELLOW}⚠ $descricao${NC}"
  ((WARNING++))
}

echo "═══════════════════════════════════════════════════════════════════════════"
echo "1. VERIFICANDO ARQUIVOS"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Verificar se diretórios existem
testar "Diretório examples/kokoro_tts/" "[ -d examples/kokoro_tts ]"
testar "Diretório examples/zimage_turbo/" "[ -d examples/zimage_turbo ]"

# Verificar se arquivos de script existem
testar "exemplo1_python (KOKORO)" "[ -f examples/kokoro_tts/exemplo1_python_simple.py ]"
testar "exemplo1_python (Z-IMAGE)" "[ -f examples/zimage_turbo/exemplo1_python_simple.py ]"

# Verificar documentação
testar "README.md" "[ -f examples/README.md ]"
testar "INICIO_RAPIDO.md" "[ -f examples/INICIO_RAPIDO.md ]"

echo "═══════════════════════════════════════════════════════════════════════════"
echo "2. VERIFICANDO CONEXÃO COMFYUI"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Verificar se ComfyUI está rodando
if command -v curl > /dev/null 2>&1; then
  if curl -s http://127.0.0.1:8188/system_stats > /dev/null 2>&1; then
    echo -e "${GREEN}✓ ComfyUI está rodando em http://127.0.0.1:8188${NC}"
    ((SUCESSO++))
  else
    echo -e "${RED}✗ ComfyUI NÃO está respondendo${NC}"
    echo "  Inicie o ComfyUI antes de executar os exemplos"
    ((FALHA++))
  fi
else
  warning "curl não encontrado - não é possível verificar ComfyUI"
fi

echo ""

# Verificar workflows
if [ -f "C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/default/workflows/WORKFLOW - KOKORO.json" ]; then
  echo -e "${GREEN}✓ Workflow KOKORO encontrado${NC}"
  ((SUCESSO++))
else
  echo -e "${RED}✗ Workflow KOKORO NÃO encontrado${NC}"
  ((FALHA++))
fi

if [ -f "C:/Users/JOSE/Downloads/confyui/ComfyUI_windows_portable/ComfyUI/user/default/workflows/WORKFLOW - Z-IMAGE-TURBO.json" ]; then
  echo -e "${GREEN}✓ Workflow Z-IMAGE-TURBO encontrado${NC}"
  ((SUCESSO++))
else
  echo -e "${RED}✗ Workflow Z-IMAGE-TURBO NÃO encontrado${NC}"
  ((FALHA++))
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "3. VERIFICANDO PYTHON"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Verificar Python
if command -v python > /dev/null 2>&1 || command -v python3 > /dev/null 2>&1; then
  echo -e "${GREEN}✓ Python encontrado${NC}"
  ((SUCESSO++))
  
  # Verificar versão
  if command -v python > /dev/null 2>&1; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo "  Versão: $PYTHON_VERSION"
  fi
else
  echo -e "${RED}✗ Python NÃO encontrado${NC}"
  ((FALHA++))
fi

# Verificar bibliotecas Python
if command -v python > /dev/null 2>&1; then
  echo ""
  echo "Verificando bibliotecas Python:"
  
  if python -c "import requests" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ requests${NC}"
  else
    echo -e "  ${RED}✗ requests (instale: pip install requests)${NC}"
  fi
  
  if python -c "import websockets" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ websockets${NC}"
  else
    echo -e "  ${RED}✗ websockets (instale: pip install websockets)${NC}"
  fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "4. CONTAGEM DE ARQUIVOS"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Contar arquivos
SH_COUNT=$(find examples -name "*.sh" | wc -l)
PY_COUNT=$(find examples -name "*.py" | wc -l)
MD_COUNT=$(find examples -name "*.md" | wc -l)

echo "Scripts cURL/bash (.sh): $SH_COUNT"
echo "Scripts Python (.py): $PY_COUNT"
echo "Documentação (.md): $MD_COUNT"
echo ""

# Verificar quantidades esperadas
if [ "$SH_COUNT" -eq 6 ]; then
  echo -e "${GREEN}✓ Quantidade correta de scripts .sh${NC}"
  ((SUCESSO++))
else
  echo -e "${YELLOW}⚠ Esperado 6 scripts .sh, encontrado $SH_COUNT${NC}"
  ((WARNING++))
fi

if [ "$PY_COUNT" -ge 6 ]; then
  echo -e "${GREEN}✓ Quantidade correta de scripts .py${NC}"
  ((SUCESSO++))
else
  echo -e "${YELLOW}⚠ Esperado pelo menos 6 scripts .py, encontrado $PY_COUNT${NC}"
  ((WARNING++))
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "5. RESUMO DO TESTE"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

echo "✓ Sucessos: $SUCESSO"
echo "✗ Falhas: $FALHA"
echo "⚠ Warnings: $WARNING"
echo ""

if [ $FALHA -eq 0 ]; then
  echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║                         ✓ TODOS OS TESTES PASSARAM                          ║${NC}"
  echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo "Você pode executar os exemplos agora:"
  echo ""
  echo "  # KOKORO TTS"
  echo "  python examples/kokoro_tts/exemplo1_python_simple.py"
  echo ""
  echo "  # Z-IMAGE-TURBO"
  echo "  python examples/zimage_turbo/exemplo1_python_simple.py"
  echo ""
else
  echo -e "${RED}╔══════════════════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${RED}║                      ✗ ALGUNS TESTES FALHARAM                            ║${NC}"
  echo -e "${RED}╚══════════════════════════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo "Resolva os problemas acima antes de executar os exemplos."
  echo ""
fi

if [ $WARNING -gt 0 ]; then
  echo -e "${YELLOW}⚠ Existem $WARNING warnings que podem precisar de atenção.${NC}"
  echo ""
fi

echo "═══════════════════════════════════════════════════════════════════════════"
echo "Fim do teste rápido"
echo "═══════════════════════════════════════════════════════════════════════════"
