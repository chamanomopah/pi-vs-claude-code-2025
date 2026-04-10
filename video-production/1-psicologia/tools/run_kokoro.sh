#!/bin/bash
# Wrapper para executar Kokoro TTS com Conda
# Uso: ./run_kokoro.sh [opcoes]
#   Exemplo: ./run_kokoro.sh
#   Exemplo: ./run_kokoro.sh --vozes

echo "============================================"
echo "Kokoro TTS - Text-to-Speech com PyTorch"
echo "============================================"
echo ""

# Diretório onde este script está localizado
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Tentar encontrar o Python do ambiente Conda
if [ -n "$CONDA_PREFIX" ]; then
    # Se já estiver em um ambiente Conda, use o Python atual
    PYTHON_EXE="$CONDA_PREFIX/bin/python"
else
    # Caso contrário, tente usar conda activate
    if command -v conda &> /dev/null; then
        # Tentar ativar o ambiente kokoro
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate kokoro 2>/dev/null
        PYTHON_EXE="python"
    else
        echo "ERRO: Conda não encontrado!"
        echo ""
        echo "Por favor, instale o Miniconda primeiro:"
        echo "  https://docs.conda.io/en/latest/miniconda.html"
        echo ""
        exit 1
    fi
fi

# Executar o script Python com os argumentos passados
"$PYTHON_EXE" "$SCRIPT_DIR/kokoro_tts.py" "$@"
