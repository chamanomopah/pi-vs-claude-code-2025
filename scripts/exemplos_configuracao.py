#!/usr/bin/env python3
"""
Exemplos de Configuração do Extrator de Frames
===============================================

Este arquivo demonstra como configurar a variável VIDEO_URL
em diferentes situações.
"""

# =============================================================================
# EXEMPLO 1: URL Remota (YouTube, Vimeo, etc)
# =============================================================================
# O vídeo será baixado automaticamente usando yt-dlp
VIDEO_URL_EXEMPLO_1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# =============================================================================
# EXEMPLO 2: Arquivo Local no Windows (formato file:///)
# =============================================================================
# Use este formato quando receber URIs de outras aplicações
# Funciona em qualquer sistema operacional
VIDEO_URL_EXEMPLO_2 = "file:///C:/Users/JOSE/Videos/meu_video.mp4"

# =============================================================================
# EXEMPLO 3: Arquivo Local no Linux/Mac (formato file:///)
# =============================================================================
VIDEO_URL_EXEMPLO_3 = "file:///home/user/videos/meu_video.mp4"

# =============================================================================
# EXEMPLO 4: Arquivo Local no Windows (caminho direto)
# =============================================================================
# Use este formato para simplicidade
VIDEO_URL_EXEMPLO_4 = "C:/Videos/meu_video.mp4"

# =============================================================================
# EXEMPLO 5: Arquivo Local no Linux/Mac (caminho direto)
# =============================================================================
VIDEO_URL_EXEMPLO_5 = "/home/user/videos/meu_video.mp4"

# =============================================================================
# EXEMPLO 6: Caminho relativo ao script
# =============================================================================
# O vídeo está na mesma pasta do script
VIDEO_URL_EXEMPLO_6 = "meu_video.mp4"

# =============================================================================
# EXEMPLO 7: Caminho relativo com subpastas
# =============================================================================
VIDEO_URL_EXEMPLO_7 = "../videos/meu_video.mp4"

# =============================================================================
# DICAS DE USO
# =============================================================================

DICA_1 = """
Use o formato file:/// quando:
- Receber URIs de outras aplicações
- Quiser manter consistência com URLs remotas
- Estiver trabalhando com código cross-platform
"""

DICA_2 = """
Use caminho direto quando:
- Quiser simplicidade
- Souber o caminho exato do arquivo
- Estiver trabalhando apenas com arquivos locais
"""

DICA_3 = """
O script detecta automaticamente o tipo de entrada:
- URL remota (http/https) -> baixa o vídeo
- file:/// -> converte para caminho local
- Caminho direto -> usa como está
"""

if __name__ == "__main__":
    print("=" * 60)
    print("  EXEMPLOS DE CONFIGURACAO - EXTRATOR DE FRAMES")
    print("=" * 60)
    print()
    print("Estes sao os formatos suportados para a variavel VIDEO_URL:")
    print()
    print("1. URL Remota:")
    print(f"   {VIDEO_URL_EXEMPLO_1}")
    print()
    print("2. Arquivo Local - file:/// (Windows):")
    print(f"   {VIDEO_URL_EXEMPLO_2}")
    print()
    print("3. Arquivo Local - file:/// (Linux/Mac):")
    print(f"   {VIDEO_URL_EXEMPLO_3}")
    print()
    print("4. Arquivo Local - Caminho Direto (Windows):")
    print(f"   {VIDEO_URL_EXEMPLO_4}")
    print()
    print("5. Arquivo Local - Caminho Direto (Linux/Mac):")
    print(f"   {VIDEO_URL_EXEMPLO_5}")
    print()
    print("6. Caminho Relativo:")
    print(f"   {VIDEO_URL_EXEMPLO_6}")
    print()
    print("=" * 60)
    print(DICA_1)
    print(DICA_2)
    print(DICA_3)
