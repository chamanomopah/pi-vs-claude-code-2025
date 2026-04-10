#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Extensivos do Kokoro TTS
Validação de qualidade, múltiplas vozes e diferentes textos
"""

import sys
import os
import io
import time
import json
from pathlib import Path
from datetime import datetime

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Importar bibliotecas
try:
    from kokoro import KPipeline
    import soundfile as sf
    import torch
    import gc
except ImportError as e:
    print(f"ERRO: {e}")
    print("Instale as dependências: pip install kokoro soundfile torch")
    sys.exit(1)


# =============================================================================
# TEXTOS DE TESTE
# =============================================================================

TEXTOS = {
    "curto": {
        "nome": "Texto Curto (20-30 segundos)",
        "texto": """Hello and welcome to this journey of self-discovery. Today we explore how small habits can create extraordinary changes in our lives. The science behind habit formation reveals fascinating patterns about human behavior and potential."""
    },
    "longo": {
        "nome": "Texto Longo (1 minuto)",
        "texto": """The psychology of habits is a fascinating field that reveals how our daily actions shape who we are. Habits are not just simple routines; they are powerful neurological patterns that our brains develop to save energy and automate decision-making. Understanding how habits work can be transformative. The habit loop consists of three key components: the cue, the routine, and the reward. The cue triggers your brain to initiate a behavior, the routine is the behavior itself, and the reward is what your brain gets from it. This loop is so strong that it can override conscious decision-making. Research shows that habits never truly disappear; they are encoded in our neural pathways, waiting for the right cue to reactivate. This is why breaking bad habits is so challenging and why building good ones requires deliberate effort and consistency. The good news is that we can harness this power to create positive change in our lives."""
    }
}

# =============================================================================
# VOZES PARA TESTAR
# =============================================================================

VOZES_TESTE = [
    "af_heart",   # Feminina, natural - RECOMENDADA
    "af_bella",   # Feminina, profissional
    "af_sarah",   # Feminina, madura
    "am_adam",    # Masculino
    "am_michael", # Masculino, profissional
    "bf_emma",    # Britânica
]

DESCRICOES_VOZES = {
    "af_heart": "Feminina, americana, natural e calorosa (RECOMENDADA)",
    "af_bella": "Feminina, americana, profissional",
    "af_sarah": "Feminina, americana, madura",
    "am_adam": "Masculino, americano",
    "am_michael": "Masculino, americano, profissional",
    "bf_emma": "Feminina, britânica",
}


# =============================================================================
# FUNÇÕES DE TESTE
# =============================================================================

def obter_info_modelo(pipeline):
    """Obtém informações sobre o modelo usado"""
    info = {
        "modelo": "Kokoro-82M",
        "lang_code": pipeline.lang_code if hasattr(pipeline, 'lang_code') else 'a',
    }
    
    # Tentar obter informações do modelo
    if hasattr(pipeline, 'model'):
        if hasattr(pipeline.model, 'config'):
            config = pipeline.model.config
            if hasattr(config, 'vocab_size'):
                info["vocab_size"] = config.vocab_size
    
    return info


def verificar_cache_modelo():
    """Verifica onde o modelo está cacheado"""
    cache_paths = [
        Path.home() / ".cache" / "huggingface" / "hub",
        Path.home() / ".cache" / "huggingface",
    ]
    
    info_cache = {
        "cache_dir": None,
        "modelo_encontrado": False,
        "tamanho_cache": 0,
    }
    
    for cache_path in cache_paths:
        if cache_path.exists():
            info_cache["cache_dir"] = str(cache_path)
            # Tentar encontrar o modelo Kokoro
            for item in cache_path.rglob("*Kokoro*"):
                if item.is_dir():
                    info_cache["modelo_encontrado"] = True
                    # Calcular tamanho
                    try:
                        info_cache["tamanho_cache"] = sum(
                            f.stat().st_size for f in item.rglob('*') if f.is_file()
                        ) / (1024 * 1024)  # MB
                        break
                    except:
                        pass
    
    return info_cache


def gerar_audio(pipeline, texto, voz, velocidade=1.0, arquivo_saida="teste.wav"):
    """Gera áudio usando o Kokoro"""
    try:
        generator = pipeline(texto, voice=voz, speed=velocidade)
        
        segmentos = []
        for i, (gs, ps, audio) in enumerate(generator):
            segmentos.append({
                "indice": i,
                "audio": audio,
                "grafo": gs,
                "fonemas": ps,
            })
        
        # Combinar todos os segmentos
        if segmentos:
            audio_completo = []
            for seg in segmentos:
                audio_completo.extend(seg["audio"])
            
            # Salvar áudio
            import numpy as np
            audio_array = np.array(audio_completo)
            sf.write(arquivo_saida, audio_array, 24000)
            
            return {
                "sucesso": True,
                "arquivo": arquivo_saida,
                "segmentos": len(segmentos),
                "duracao_segundos": len(audio_array) / 24000,
                "amostras": len(audio_array),
            }
        
        return {"sucesso": False, "erro": "Nenhum áudio gerado"}
        
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}


def teste_vozes_texto_curto(pipeline, diretorio_saida):
    """TESTE 1: Múltiplas Vozes com Texto Curto"""
    print("\n" + "="*80)
    print("TESTE 1: Múltiplas Vozes (Texto Curto)")
    print("="*80)
    
    resultados = []
    texto = TEXTOS["curto"]["texto"]
    
    for voz in VOZES_TESTE:
        print(f"\n🎙️  Testando voz: {voz}")
        print(f"   Descrição: {DESCRICOES_VOZES[voz]}")
        
        arquivo_saida = diretorio_saida / f"teste1_curto_{voz}.wav"
        
        inicio = time.time()
        resultado = gerar_audio(pipeline, texto, voz, 1.0, str(arquivo_saida))
        tempo_processamento = time.time() - inicio
        
        if resultado["sucesso"]:
            tamanho_arquivo = arquivo_saida.stat().st_size / 1024  # KB
            
            info = {
                "voz": voz,
                "descricao": DESCRICOES_VOZES[voz],
                "arquivo": arquivo_saida.name,
                "duracao_segundos": round(resultado["duracao_segundos"], 2),
                "tamanho_kb": round(tamanho_arquivo, 2),
                "segmentos": resultado["segmentos"],
                "tempo_processamento": round(tempo_processamento, 2),
                "taxa_amostragem": 24000,
                "status": "SUCESSO",
            }
            
            print(f"   ✅ SUCESSO!")
            print(f"   📄 Arquivo: {info['arquivo']}")
            print(f"   ⏱️  Duração: {info['duracao_segundos']}s")
            print(f"   📦 Tamanho: {info['tamanho_kb']} KB")
            print(f"   🔄 Tempo de processamento: {info['tempo_processamento']}s")
            print(f"   🎚️  Segmentos: {info['segmentos']}")
            
        else:
            info = {
                "voz": voz,
                "descricao": DESCRICOES_VOZES[voz],
                "status": "FALHOU",
                "erro": resultado["erro"],
            }
            print(f"   ❌ FALHOU: {resultado['erro']}")
        
        resultados.append(info)
        
        # Limpar memória
        gc.collect()
    
    return resultados


def teste_texto_longo(pipeline, diretorio_saida):
    """TESTE 2: Texto Longo (1 minuto) com vozes selecionadas"""
    print("\n" + "="*80)
    print("TESTE 2: Texto Longo (1 minuto)")
    print("="*80)
    
    vozes_texto_longo = ["af_heart", "am_michael", "bf_emma"]
    resultados = []
    texto = TEXTOS["longo"]["texto"]
    
    print(f"\n📝 Texto: {TEXTOS['longo']['nome']}")
    print(f"📊 Palavras: {len(texto.split())}")
    
    for voz in vozes_texto_longo:
        print(f"\n🎙️  Testando voz: {voz}")
        print(f"   Descrição: {DESCRICOES_VOZES[voz]}")
        
        arquivo_saida = diretorio_saida / f"teste2_longo_{voz}.wav"
        
        inicio = time.time()
        resultado = gerar_audio(pipeline, texto, voz, 1.0, str(arquivo_saida))
        tempo_processamento = time.time() - inicio
        
        if resultado["sucesso"]:
            tamanho_arquivo = arquivo_saida.stat().st_size / 1024  # KB
            
            info = {
                "voz": voz,
                "descricao": DESCRICOES_VOZES[voz],
                "arquivo": arquivo_saida.name,
                "duracao_segundos": round(resultado["duracao_segundos"], 2),
                "tamanho_kb": round(tamanho_arquivo, 2),
                "segmentos": resultado["segmentos"],
                "tempo_processamento": round(tempo_processamento, 2),
                "palavras_por_minuto": round(len(texto.split()) / (resultado["duracao_segundos"] / 60), 1),
                "taxa_amostragem": 24000,
                "status": "SUCESSO",
            }
            
            print(f"   ✅ SUCESSO!")
            print(f"   📄 Arquivo: {info['arquivo']}")
            print(f"   ⏱️  Duração: {info['duracao_segundos']}s")
            print(f"   📦 Tamanho: {info['tamanho_kb']} KB")
            print(f"   📈 Palavras/minuto: {info['palavras_por_minuto']}")
            print(f"   🔄 Tempo de processamento: {info['tempo_processamento']}s")
            print(f"   🎚️  Segmentos: {info['segmentos']}")
            
        else:
            info = {
                "voz": voz,
                "descricao": DESCRICOES_VOZES[voz],
                "status": "FALHOU",
                "erro": resultado["erro"],
            }
            print(f"   ❌ FALHOU: {resultado['erro']}")
        
        resultados.append(info)
        
        # Limpar memória
        gc.collect()
    
    return resultados


def teste_velocidades(pipeline, diretorio_saida):
    """TESTE 3: Diferentes velocidades"""
    print("\n" + "="*80)
    print("TESTE 3: Diferentes Velocidades")
    print("="*80)
    
    velocidades = [0.75, 1.0, 1.25, 1.5]
    voz_teste = "af_heart"
    texto = TEXTOS["curto"]["texto"]
    
    resultados = []
    
    print(f"\n🎙️  Voz base: {voz_teste}")
    print(f"📝 Texto: {TEXTOS['curto']['nome']}")
    
    for velocidade in velocidades:
        print(f"\n🎚️  Testando velocidade: {velocidade}x")
        
        arquivo_saida = diretorio_saida / f"teste3_velocidade_{velocidade}.wav"
        
        inicio = time.time()
        resultado = gerar_audio(pipeline, texto, voz_teste, velocidade, str(arquivo_saida))
        tempo_processamento = time.time() - inicio
        
        if resultado["sucesso"]:
            tamanho_arquivo = arquivo_saida.stat().st_size / 1024  # KB
            
            info = {
                "velocidade": velocidade,
                "arquivo": arquivo_saida.name,
                "duracao_segundos": round(resultado["duracao_segundos"], 2),
                "tamanho_kb": round(tamanho_arquivo, 2),
                "tempo_processamento": round(tempo_processamento, 2),
                "status": "SUCESSO",
            }
            
            print(f"   ✅ SUCESSO!")
            print(f"   📄 Arquivo: {info['arquivo']}")
            print(f"   ⏱️  Duração: {info['duracao_segundos']}s")
            print(f"   📦 Tamanho: {info['tamanho_kb']} KB")
            
        else:
            info = {
                "velocidade": velocidade,
                "status": "FALHOU",
                "erro": resultado["erro"],
            }
            print(f"   ❌ FALHOU: {resultado['erro']}")
        
        resultados.append(info)
        
        # Limpar memória
        gc.collect()
    
    return resultados


def obter_info_sistema():
    """Obtém informações do sistema"""
    info = {
        "plataforma": sys.platform,
        "python_version": sys.version,
        "torch_version": torch.__version__,
        "cuda_disponivel": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }
    
    # Tentar obter info do Kokoro
    try:
        import kokoro
        info["kokoro_version"] = getattr(kokoro, '__version__', 'desconhecido')
    except:
        info["kokoro_version"] = "não disponível"
    
    return info


def gerar_relatorio_markdown(resultados, info_sistema, info_modelo, info_cache, diretorio_saida):
    """Gera relatório em formato Markdown"""
    
    arquivo_relatorio = diretorio_saida / "RELATORIO_TESTES_KOKORO.md"
    
    with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE TESTES - KOKORO TTS\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # 1. Informações do Sistema
        f.write("## 1. INFORMAÇÕES DO SISTEMA\n\n")
        f.write("| Propriedade | Valor |\n")
        f.write("|-------------|-------|\n")
        f.write(f"| Plataforma | {info_sistema['plataforma']} |\n")
        f.write(f"| Python | {info_sistema['python_version'].split()[0]} |\n")
        f.write(f"| PyTorch | {info_sistema['torch_version']} |\n")
        f.write(f"| CUDA Disponível | {'Sim' + ' (' + info_sistema['cuda_device'] + ')' if info_sistema['cuda_disponivel'] else 'Não'} |\n")
        f.write(f"| Kokoro | {info_sistema['kokoro_version']} |\n")
        f.write("\n")
        
        # 2. Informações do Modelo
        f.write("## 2. INFORMAÇÕES DO MODELO\n\n")
        f.write("| Propriedade | Valor |\n")
        f.write("|-------------|-------|\n")
        f.write(f"| Modelo | {info_modelo['modelo']} |\n")
        f.write(f"| Código de Idioma | {info_modelo['lang_code']} (americano) |\n")
        f.write(f"| Cache Directory | {info_cache['cache_dir']} |\n")
        f.write(f"| Modelo Encontrado | {'Sim' if info_cache['modelo_encontrado'] else 'Não'} |\n")
        if info_cache['tamanho_cache'] > 0:
            f.write(f"| Tamanho do Cache | {info_cache['tamanho_cache']:.1f} MB |\n")
        f.write("\n")
        
        # 3. TESTE 1: Múltiplas Vozes
        f.write("## 3. TESTE 1: MÚLTIPLAS VOZES (TEXTO CURTO)\n\n")
        f.write(f"**Texto:** {TEXTOS['curto']['nome']}\n")
        f.write(f"**Palavras:** {len(TEXTOS['curto']['texto'].split())}\n\n")
        
        f.write("| Voz | Descrição | Duração (s) | Tamanho (KB) | Segmentos | Processamento (s) | Status |\n")
        f.write("|-----|-----------|-------------|---------------|-----------|-------------------|--------|\n")
        
        for r in resultados["teste1"]:
            if r["status"] == "SUCESSO":
                f.write(f"| {r['voz']} | {r['descricao']} | {r['duracao_segundos']} | {r['tamanho_kb']} | {r['segmentos']} | {r['tempo_processamento']} | ✅ |\n")
            else:
                f.write(f"| {r['voz']} | {r['descricao']} | - | - | - | - | ❌ {r['erro']} |\n")
        
        f.write("\n")
        
        # 4. TESTE 2: Texto Longo
        f.write("## 4. TESTE 2: TEXTO LONGO (1 MINUTO)\n\n")
        f.write(f"**Texto:** {TEXTOS['longo']['nome']}\n")
        f.write(f"**Palavras:** {len(TEXTOS['longo']['texto'].split())}\n\n")
        
        f.write("| Voz | Descrição | Duração (s) | Tamanho (KB) | Palavras/min | Segmentos | Processamento (s) | Status |\n")
        f.write("|-----|-----------|-------------|---------------|---------------|-----------|-------------------|--------|\n")
        
        for r in resultados["teste2"]:
            if r["status"] == "SUCESSO":
                f.write(f"| {r['voz']} | {r['descricao']} | {r['duracao_segundos']} | {r['tamanho_kb']} | {r['palavras_por_minuto']} | {r['segmentos']} | {r['tempo_processamento']} | ✅ |\n")
            else:
                f.write(f"| {r['voz']} | {r['descricao']} | - | - | - | - | - | ❌ {r['erro']} |\n")
        
        f.write("\n")
        
        # 5. TESTE 3: Velocidades
        f.write("## 5. TESTE 3: DIFERENTES VELOCIDADES\n\n")
        f.write(f"**Voz:** af_heart\n")
        f.write(f"**Texto:** {TEXTOS['curto']['nome']}\n\n")
        
        f.write("| Velocidade | Duração (s) | Tamanho (KB) | Processamento (s) | Status |\n")
        f.write("|------------|-------------|---------------|-------------------|--------|\n")
        
        for r in resultados["teste3"]:
            if r["status"] == "SUCESSO":
                f.write(f"| {r['velocidade']}x | {r['duracao_segundos']} | {r['tamanho_kb']} | {r['tempo_processamento']} | ✅ |\n")
            else:
                f.write(f"| {r['velocidade']}x | - | - | - | ❌ {r['erro']} |\n")
        
        f.write("\n")
        
        # 6. Análise de Qualidade (placeholder para avaliação manual)
        f.write("## 6. ANÁLISE DE QUALIDADE (AVALIAÇÃO MANUAL NECESSÁRIA)\n\n")
        f.write("### 6.1. Arquivos de Áudio Gerados\n\n")
        
        f.write("**TESTE 1 - Múltiplas Vozes:**\n")
        for r in resultados["teste1"]:
            if r["status"] == "SUCESSO":
                f.write(f"- `teste1_curto_{r['voz']}.wav` - {r['voz']}: {r['descricao']}\n")
        
        f.write("\n**TESTE 2 - Texto Longo:**\n")
        for r in resultados["teste2"]:
            if r["status"] == "SUCESSO":
                f.write(f"- `teste2_longo_{r['voz']}.wav` - {r['voz']}: {r['descricao']}\n")
        
        f.write("\n**TESTE 3 - Velocidades:**\n")
        for r in resultados["teste3"]:
            if r["status"] == "SUCESSO":
                f.write(f"- `teste3_velocidade_{r['velocidade']}.wav` - Velocidade {r['velocidade']}x\n")
        
        f.write("\n")
        f.write("### 6.2. Checklist de Avaliação Manual\n\n")
        f.write("Para cada áudio, avalie:\n\n")
        f.write("- [ ] Naturalidade da voz\n")
        f.write("- [ ] Entonação adequada\n")
        f.write("- [ ] Ausência de artefatos ou distorções\n")
        f.write("- [ ] Fluidez da fala\n")
        f.write("- [ ] Pronúncia correta\n")
        f.write("- [ ] Cortes ou problemas na reprodução\n")
        f.write("- [ ] Adequação para narração de vídeo\n\n")
        
        # 7. Conclusões
        f.write("## 7. CONCLUSÕES\n\n")
        
        # Contar sucessos/falhas
        total_testes = 0
        sucessos = 0
        
        for teste_key in ["teste1", "teste2", "teste3"]:
            for r in resultados[teste_key]:
                total_testes += 1
                if r["status"] == "SUCESSO":
                    sucessos += 1
        
        taxa_sucesso = (sucessos / total_testes * 100) if total_testes > 0 else 0
        
        f.write(f"### 7.1. Taxa de Sucesso\n\n")
        f.write(f"- **Total de Testes:** {total_testes}\n")
        f.write(f"- **Sucessos:** {sucessos}\n")
        f.write(f"- **Falhas:** {total_testes - sucessos}\n")
        f.write(f"- **Taxa de Sucesso:** {taxa_sucesso:.1f}%\n\n")
        
        f.write(f"### 7.2. Status do Kokoro TTS\n\n")
        if taxa_sucesso >= 90:
            f.write("✅ **FUNCIONANDO PERFEITAMENTE** - O Kokoro TTS está estável e pronto para uso em produção.\n\n")
        elif taxa_sucesso >= 70:
            f.write("⚠️ **FUNCIONANDO COM RESALVAS** - O Kokoro TTS funciona, mas há alguns problemas que devem ser investigados.\n\n")
        else:
            f.write("❌ **PROBLEMAS DETECTADOS** - O Kokoro TTS apresenta problemas significativos que precisam ser resolvidos antes do uso em produção.\n\n")
        
        f.write(f"### 7.3. Próximos Passos\n\n")
        f.write("1. Ouvir manualmente os áudios gerados\n")
        f.write("2. Avaliar a qualidade de cada voz\n")
        f.write("3. Identificar a melhor voz para produção de vídeos\n")
        f.write("4. Documentar quaisquer problemas de qualidade\n")
        f.write("5. Comparar com outras soluções TTS (Edge TTS, etc.)\n\n")
        
        f.write("---\n\n")
        f.write(f"**Relatório gerado automaticamente pelo script `testar_kokoro_completo.py`**\n")
    
    return arquivo_relatorio


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Executa todos os testes"""
    
    print("="*80)
    print("KOKORO TTS - TESTES EXTENSIVOS")
    print("="*80)
    print(f"\nData/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Criar diretório de saída
    diretorio_saida = Path("testes_kokoro")
    diretorio_saida.mkdir(exist_ok=True)
    print(f"\n📁 Diretório de saída: {diretorio_saida.absolute()}")
    
    # Inicializar pipeline
    print("\n🔄 Inicializando Kokoro TTS...")
    inicio_carregamento = time.time()
    pipeline = KPipeline(lang_code='a')
    tempo_carregamento = time.time() - inicio_carregamento
    print(f"✅ Modelo carregado em {tempo_carregamento:.2f} segundos")
    
    # Obter informações do sistema e modelo
    print("\n📊 Coletando informações...")
    info_sistema = obter_info_sistema()
    info_modelo = obter_info_modelo(pipeline)
    info_cache = verificar_cache_modelo()
    
    print(f"   Modelo: {info_modelo['modelo']}")
    print(f"   PyTorch: {info_sistema['torch_version']}")
    print(f"   CUDA: {'Disponível' if info_sistema['cuda_disponivel'] else 'Não disponível'}")
    if info_cache['cache_dir']:
        print(f"   Cache: {info_cache['cache_dir']}")
    
    # Executar testes
    resultados = {
        "teste1": [],
        "teste2": [],
        "teste3": [],
    }
    
    try:
        # TESTE 1: Múltiplas Vozes
        resultados["teste1"] = teste_vozes_texto_curto(pipeline, diretorio_saida)
        
        # TESTE 2: Texto Longo
        resultados["teste2"] = teste_texto_longo(pipeline, diretorio_saida)
        
        # TESTE 3: Velocidades
        resultados["teste3"] = teste_velocidades(pipeline, diretorio_saida)
        
        # Gerar relatório
        print("\n" + "="*80)
        print("GERANDO RELATÓRIO...")
        print("="*80)
        
        arquivo_relatorio = gerar_relatorio_markdown(
            resultados, info_sistema, info_modelo, info_cache, diretorio_saida
        )
        
        print(f"\n✅ Relatório gerado: {arquivo_relatorio}")
        print(f"📁 Diretório dos áudios: {diretorio_saida.absolute()}")
        
        # Resumo final
        total_testes = sum(len(r) for r in resultados.values())
        total_sucessos = sum(sum(1 for r in resultados[teste] if r["status"] == "SUCESSO") for teste in resultados)
        
        print("\n" + "="*80)
        print("RESUMO DOS TESTES")
        print("="*80)
        print(f"✅ Testes bem-sucedidos: {total_sucessos}/{total_testes}")
        print(f"📊 Taxa de sucesso: {total_sucessos/total_testes*100:.1f}%")
        print(f"\n📄 Relatório completo: {arquivo_relatorio}")
        print(f"🎧 Áudios salvos em: {diretorio_saida.absolute()}")
        
        print("\n" + "="*80)
        print("✅ TESTES CONCLUÍDOS!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        # Limpar memória
        del pipeline
        gc.collect()


if __name__ == "__main__":
    main()
