#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kokoro TTS - Text-to-Speech com PyTorch
Solução testada com Conda + Python 3.12
Baseado em: https://heyletslearnsensomething.com/blog/kokoro-tts-free-text-to-speech
"""

import sys
import os

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ===== CONFIGURAÇÕES =====
# Edite estas variáveis conforme necessário
TEXTO = """Hello! This is a test of Kokoro text-to-speech system.
This solution uses Conda with Python 3.12 for maximum compatibility."""

VOZ = "af_heart"  # Opções: af_heart, af_bella, af_sarah, am_michael, bf_emma
VELOCIDADE = 1.0  # 0.5 a 2.0 (1.0 = normal)
ARQUIVO_SAIDA = "audio_kokoro.wav"
# ==========================

import sys
import gc
from pathlib import Path

def main():
    """Função principal do Kokoro TTS"""
    
    print("=" * 60)
    print("KOKORO TTS - Text-to-Speech com PyTorch")
    print("=" * 60)
    
    # Mostrar configurações
    print(f"\n📋 CONFIGURAÇÕES:")
    print(f"   Texto: {TEXTO[:50]}...")
    print(f"   Voz: {VOZ}")
    print(f"   Velocidade: {VELOCIDADE}x")
    print(f"   Arquivo de saída: {ARQUIVO_SAIDA}")
    
    # Verificar se o texto não está vazio
    if not TEXTO or TEXTO.strip() == "":
        print("❌ ERRO: O texto está vazio!")
        print("   Edite a variável TEXTO no topo do script.")
        sys.exit(1)
    
    try:
        # Importar bibliotecas (apenas quando necessário)
        print("\n📦 Importando bibliotecas...")
        from kokoro import KPipeline
        import soundfile as sf
        
        # Inicializar pipeline (baixa modelo automaticamente na primeira execução)
        print("🔄 Carregando modelo Kokoro (pode demorar na primeira execução)...")
        pipeline = KPipeline(lang_code='a')  # 'a' = inglês americano
        print("✅ Modelo carregado com sucesso!")
        
        # Gerar áudio
        print(f"\n🎙️  Gerando áudio...")
        generator = pipeline(
            TEXTO, 
            voice=VOZ, 
            speed=VELOCIDADE
        )
        
        # Processar e salvar áudio
        segment_count = 0
        for i, (gs, ps, audio) in enumerate(generator):
            output_path = ARQUIVO_SAIDA
            
            # Salvar áudio
            sf.write(output_path, audio, 24000)  # 24kHz
            
            # Calcular duração
            duration = len(audio) / 24000
            file_size = Path(output_path).stat().st_size / 1024  # KB
            
            print(f"\n✅ SUCESSO!")
            print(f"   Arquivo: {output_path}")
            print(f"   Duração: {duration:.2f} segundos")
            print(f"   Tamanho: {file_size:.1f} KB")
            print(f"   Taxa de amostragem: 24000 Hz")
            
            segment_count += 1
            break  # Usar apenas primeiro segmento (para textos simples)
        
        if segment_count == 0:
            print("\n⚠️  AVISO: Nenhum áudio foi gerado.")
            print("   Verifique se o texto contém caracteres válidos.")
        
        # Limpar memória
        del pipeline
        gc.collect()
        
        print("\n" + "=" * 60)
        print("✅ PROCESSO CONCLUÍDO!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
        print("\n💡 SOLUÇÃO:")
        print("   1. Crie um ambiente Conda com Python 3.12:")
        print("      conda create --name kokoro python=3.12 -y")
        print("   2. Ative o ambiente:")
        print("      conda activate kokoro")
        print("   3. Instale as dependências:")
        print("      pip install kokoro>=0.9.4 soundfile torch")
        print("   4. Execute este script novamente:")
        print("      python kokoro_tts.py")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print(f"\n📝 Tipo do erro: {type(e).__name__}")
        
        # Dicas baseadas no erro
        if "torch" in str(e).lower():
            print("\n💡 DICA: Pode haver problema com o PyTorch.")
            print("   Tente: pip install torch --upgrade")
        elif "model" in str(e).lower():
            print("\n💡 DICA: Erro ao baixar o modelo.")
            print("   Verifique sua conexão com a internet.")
        elif "memory" in str(e).lower():
            print("\n💡 DICA: Erro de memória.")
            print("   Tente reduzir o tamanho do texto.")
        
        sys.exit(1)


def listar_vozes():
    """Lista todas as vozes disponíveis"""
    print("\n🎤 VOZES DISPONÍVEIS:")
    print("-" * 40)
    
    vozes = {
        "af_heart": "❤️ MELHOR OPÇÃO - Feminina, americana, natural e calorosa",
        "af_bella": "🔥 Feminina, americana, profissional",
        "af_sarah": "👩 Feminina, americana, madura",
        "am_adam": "👨 Masculino, americano",
        "am_michael": "💼 Masculino, americano, profissional",
        "bf_emma": "🇬🇧 Feminina, britânica",
        "bm_george": "🇬🇧 Masculino, britânico",
        "af_nicole": "👩 Feminina, americana",
        "am_evan": "👨 Masculino, americano jovem"
    }
    
    for voz, descricao in vozes.items():
        print(f"   {voz:15} - {descricao}")
    
    print("\n💡 Use a voz 'af_heart' para melhor qualidade geral")


if __name__ == "__main__":
    # Se chamado com argumento --vozes, lista as vozes disponíveis
    if len(sys.argv) > 1 and sys.argv[1] in ["--vozes", "--voices", "-v"]:
        listar_vozes()
    else:
        main()
