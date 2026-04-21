"""
ComfyUI - Teste de Conexão
Script rápido para testar se o ComfyUI está acessível
"""

import sys
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from utils import check_server, get_queue_info, get_object_info
    
    print("=" * 50)
    print("ComfyUI - Teste de Conexão")
    print("=" * 50)
    
    print("\n1. Verificando servidor...")
    if check_server():
        print("   ✓ Servidor ComfyUI está rodando!")
    else:
        print("   ✗ Servidor não está acessível")
        print("\n   Inicie o ComfyUI e tente novamente:")
        print('   C:\\Users\\JOSE\\Downloads\\confyui\\ComfyUI_windows_portable\\ComfyUI\\run_nvidia_gpu.bat')
        sys.exit(1)
    
    print("\n2. Verificando fila...")
    try:
        queue = get_queue_info()
        queue_running = queue.get("queue_running", [])
        queue_pending = queue.get("queue_pending", [])
        print(f"   ✓ Executando: {len(queue_running)} job(s)")
        print(f"   ✓ Na fila: {len(queue_pending)} job(s)")
    except Exception as e:
        print(f"   ! Aviso: Não foi possível obter info da fila: {e}")
    
    print("\n3. Obtendo informações dos nós...")
    try:
        object_info = get_object_info()
        num_nodes = len(object_info)
        print(f"   ✓ {num_nodes} tipos de nós disponíveis")
        
        # Mostrar alguns exemplos
        sample_nodes = list(object_info.keys())[:5]
        print("   Exemplos de nós:")
        for node in sample_nodes:
            print(f"      - {node}")
    except Exception as e:
        print(f"   ! Aviso: Não foi possível obter info dos nós: {e}")
    
    print("\n" + "=" * 50)
    print("✓ Tudo pronto! Você pode usar os scripts de automação.")
    print("=" * 50)
    print("\nExemplos:")
    print("  python comfyui_kokoro_tts.py --text 'Olá, mundo!' --lang Portuguese")
    print("  python comfyui_z_image_turbo.py --prompt 'um gato astronauta'")
    print("  python comfyui_ltx_video.py --prompt 'Câmera se aproxima' --text-to-video")
    
except ImportError as e:
    print(f"ERRO: {e}")
    print("\nInstale as dependências:")
    print('C:\\Users\\JOSE\\Downloads\\confyui\\ComfyUI_windows_portable\\python_embeded\\python.exe -m pip install requests websockets')
    sys.exit(1)
