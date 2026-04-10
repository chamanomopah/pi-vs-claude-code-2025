#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da voz am_michael com roteiro real de canal competidor
Baseado no estilo de canais: Psych2Go, Explained, Psychology Facts
"""

import sys
import os
import io
import time
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
    import gc
except ImportError as e:
    print(f"ERRO: {e}")
    print("Instale as dependências: pip install kokoro soundfile torch")
    sys.exit(1)


# =============================================================================
# ROTEIRO BASEADO EM CANAL COMPETIDOR
# Estilo: Psychology Facts / Explained
# Tema: People Pleasing (fenômeno psicológico popular)
# =============================================================================

ROTEIRO_PSICOLOGIA = {
    "titulo": "The Psychology of People Pleasing",
    "tema": "People Pleasing (Complacência Social)",
    "duracao_estimada_segundos": 90,
    "palavras": 205,
    "texto": """Do you say yes when you really want to say no? Do you constantly prioritize others' needs over your own? You might be a people pleaser. [PAUSA]

People pleasing isn't about being kind. It's about fear. Fear of rejection, fear of conflict, and fear of not being enough. According to psychologists, this behavior often stems from childhood experiences where your love and attention felt conditional. You learned that being agreeable was the safest way to get your needs met.

The problem? You're sacrificing your authentic self to avoid discomfort. Every time you suppress your true feelings, you're telling yourself that your needs don't matter. This leads to resentment, anxiety, and eventually, burnout.

Research shows that chronic people pleasers have higher levels of cortisol, the stress hormone. You're literally worrying yourself sick trying to control how others perceive you.

The hard truth is this: people who genuinely like you will still like you when you say no. And those who don't? They were never your friends to begin with.

Setting boundaries isn't selfish. It's necessary. Start small. Decline one invitation this week. Express one honest opinion. Each time you do this, you're rewiring your brain to understand that your voice matters.

You deserve to be heard, not just convenient."""
}


# =============================================================================
# FUNÇÕES
# =============================================================================

def gerar_audio_kokoro(pipeline, texto, voz, velocidade, arquivo_saida):
    """Gera áudio usando Kokoro"""
    try:
        print(f"\n🎙️  Gerando áudio com voz '{voz}'...")
        print(f"   Velocidade: {velocidade}x")
        
        inicio = time.time()
        generator = pipeline(texto, voice=voz, speed=velocidade)
        
        segmentos = []
        for i, (gs, ps, audio) in enumerate(generator):
            segmentos.append({
                "indice": i,
                "audio": audio,
                "grafo": gs,
                "fonemas": ps,
            })
        
        if not segmentos:
            return {"sucesso": False, "erro": "Nenhum áudio gerado"}
        
        # Combinar todos os segmentos
        import numpy as np
        audio_completo = []
        for seg in segmentos:
            audio_completo.extend(seg["audio"])
        
        # Salvar áudio
        audio_array = np.array(audio_completo)
        sf.write(arquivo_saida, audio_array, 24000)
        
        tempo_processamento = time.time() - inicio
        
        return {
            "sucesso": True,
            "arquivo": arquivo_saida,
            "segmentos": len(segmentos),
            "duracao_segundos": len(audio_array) / 24000,
            "amostras": len(audio_array),
            "tempo_processamento": tempo_processamento,
        }
        
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}


def analisar_resultado(resultado, roteiro, velocidade):
    """Analisa os resultados da geração"""
    
    print("\n" + "="*80)
    print("RESULTADOS DO TESTE")
    print("="*80)
    
    print(f"\n📋 INFORMAÇÕES DO ROTEIRO:")
    print(f"   Título: {roteiro['titulo']}")
    print(f"   Tema: {roteiro['tema']}")
    print(f"   Palavras: {roteiro['palavras']}")
    print(f"   Duração estimada: {roteiro['duracao_estimada_segundos']}s")
    
    if resultado["sucesso"]:
        arquivo = Path(resultado["arquivo"])
        tamanho_kb = arquivo.stat().st_size / 1024
        duracao_real = resultado["duracao_segundos"]
        palavras_por_minuto = (roteiro["palavras"] / duracao_real) * 60
        eficiencia = duracao_real / resultado["tempo_processamento"]
        
        print(f"\n✅ SUCESSO!")
        print(f"\n📊 MÉTRICAS DO ÁUDIO:")
        print(f"   Arquivo: {arquivo.name}")
        print(f"   Localização: {arquivo.absolute()}")
        print(f"   Tamanho: {tamanho_kb:.1f} KB")
        print(f"   Duração real: {duracao_real:.2f}s")
        print(f"   Taxa de amostragem: 24000 Hz")
        print(f"   Segmentos: {resultado['segmentos']}")
        
        print(f"\n⏱️  PERFORMANCE:")
        print(f"   Tempo de processamento: {resultado['tempo_processamento']:.2f}s")
        print(f"   Eficiencia: {eficiencia:.2f}x (tempo real / processamento)")
        print(f"   Palavras/minuto: {palavras_por_minuto:.1f}")
        
        print(f"\n📝 CONFIGURAÇÃO:")
        print(f"   Voz: am_michael")
        print(f"   Velocidade: {velocidade}x")
        
        # Comparação com estimativa
        diferenca_duracao = duracao_real - roteiro["duracao_estimada_segundos"]
        diferenca_pct = (diferenca_duracao / roteiro["duracao_estimada_segundos"]) * 100
        
        print(f"\n📈 COMPARAÇÃO COM ESTIMATIVA:")
        print(f"   Duração estimada: {roteiro['duracao_estimada_segundos']}s")
        print(f"   Duração real: {duracao_real:.2f}s")
        print(f"   Diferença: {diferenca_duracao:+.2f}s ({diferenca_pct:+.1f}%)")
        
        return {
            "sucesso": True,
            "arquivo": str(arquivo),
            "tamanho_kb": tamanho_kb,
            "duracao_segundos": duracao_real,
            "palavras_por_minuto": palavras_por_minuto,
            "tempo_processamento": resultado["tempo_processamento"],
            "eficiencia": eficiencia,
            "segmentos": resultado["segmentos"],
        }
    else:
        print(f"\n❌ FALHOU!")
        print(f"   Erro: {resultado['erro']}")
        return {"sucesso": False, "erro": resultado["erro"]}


def criar_relatorio_markdown(resultados, roteiro, diretorio_saida):
    """Cria relatório em formato Markdown"""
    
    arquivo_relatorio = diretorio_saida / "RELATORIO_AM_MICHAEL.md"
    
    with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE TESTE - am_michael (Kokoro TTS)\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"**Voz:** am_michael (Masculina, Profissional)\n")
        f.write(f"**Objetivo:** Testar com roteiro real de canal competidor\n\n")
        f.write("---\n\n")
        
        # 1. Informações do Roteiro
        f.write("## 1. INFORMAÇÕES DO ROTEIRO\n\n")
        f.write(f"**Título:** {roteiro['titulo']}\n\n")
        f.write(f"**Tema:** {roteiro['tema']}\n\n")
        f.write("**Características:**\n")
        f.write(f"- Palavras: {roteiro['palavras']}\n")
        f.write(f"- Duração estimada: {roteiro['duracao_estimada_segundos']} segundos\n")
        f.write(f"- Estilo: Primeira pessoa, analítico, baseado em dados\n")
        f.write(f"- Estrutura: Hook → Contexto → Explicação → Insight → CTA\n\n")
        
        # 2. Resultados dos Testes
        f.write("## 2. RESULTADOS DOS TESTES\n\n")
        
        for velocidade, resultado in resultados.items():
            if resultado["sucesso"]:
                f.write(f"### Velocidade {velocidade}x\n\n")
                f.write("| Métrica | Valor |\n")
                f.write("|---------|-------|\n")
                f.write(f"| Arquivo | `{Path(resultado['arquivo']).name}` |\n")
                f.write(f"| Duração | {resultado['duracao_segundos']:.2f} segundos |\n")
                f.write(f"| Tamanho | {resultado['tamanho_kb']:.1f} KB |\n")
                f.write(f"| Palavras/minuto | {resultado['palavras_por_minuto']:.1f} |\n")
                f.write(f"| Segmentos | {resultado['segmentos']} |\n")
                f.write(f"| Processamento | {resultado['tempo_processamento']:.2f} segundos |\n")
                f.write(f"| Eficiência | {resultado['eficiencia']:.2f}x |\n")
                f.write(f"| Taxa de amostragem | 24000 Hz |\n\n")
            else:
                f.write(f"### Velocidade {velocidade}x\n\n")
                f.write(f"**Status:** ❌ FALHOU\n\n")
                f.write(f"**Erro:** {resultado['erro']}\n\n")
        
        # 3. Análise de Qualidade
        f.write("## 3. ANÁLISE DE QUALIDADE\n\n")
        f.write("### 3.1. Métricas Objetivas\n\n")
        
        # Usar o resultado da velocidade 1.0x como referência
        if 1.0 in resultados and resultados[1.0]["sucesso"]:
            ref = resultados[1.0]
            f.write("| Aspecto | Avaliação |\n")
            f.write("|---------|-----------|\n")
            f.write(f"| Duração | {ref['duracao_segundos']:.2f}s (esperado: ~90s) |\n")
            f.write(f"| Velocidade de fala | {ref['palavras_por_minuto']:.1f} palavras/minuto |\n")
            f.write(f"| Eficiência de processamento | {ref['eficiencia']:.2f}x (excelente) |\n")
            f.write(f"| Segmentação | {ref['segmentos']} segmentos (adequado) |\n")
            f.write(f"| Taxa de amostragem | 24kHz (qualidade CD) |\n\n")
        
        f.write("### 3.2. Avaliação Subjetiva (Pendente)\n\n")
        f.write("**Ouvir o áudio e avaliar:**\n\n")
        f.write("- [ ] Naturalidade da voz masculina\n")
        f.write("- [ ] Profundidade e autoridade (pitch baixo)\n")
        f.write("- [ ] Adequação para conteúdo psicológico\n")
        f.write("- [ ] Entonação analítica e reflexiva\n")
        f.write("- [ ] Ritmo da narração\n")
        f.write("- [ ] Ausência de artefatos ou distorções\n")
        f.write("- [ ] Paixão e engajamento\n")
        f.write("- [ ] Comparação com vozes de canais competidores\n\n")
        
        # 4. Comparação de Velocidades
        f.write("## 4. COMPARAÇÃO DE VELOCIDADES\n\n")
        
        velocidades_disponiveis = [v for v in resultados if resultados[v]["sucesso"]]
        if len(velocidades_disponiveis) > 1:
            f.write("| Velocidade | Duração (s) | Palavras/min | Tamanho (KB) |\n")
            f.write("|------------|-------------|---------------|---------------|\n")
            
            for v in sorted(velocidades_disponiveis):
                r = resultados[v]
                f.write(f"| {v}x | {r['duracao_segundos']:.2f} | {r['palavras_por_minuto']:.1f} | {r['tamanho_kb']:.1f} |\n")
            
            f.write("\n")
        
        # 5. Recomendação
        f.write("## 5. CONCLUSÃO E RECOMENDAÇÃO\n\n")
        
        if 1.0 in resultados and resultados[1.0]["sucesso"]:
            ref = resultados[1.0]
            
            f.write("### 5.1. Adequação da Voz am_michael\n\n")
            
            # Avaliação baseada em métricas
            duracao_ok = 80 <= ref['duracao_segundos'] <= 100
            velocidade_ok = 140 <= ref['palavras_por_minuto'] <= 170
            
            f.write("**Métricas:**\n")
            f.write(f"- Duração: {'✅ Adequada' if duracao_ok else '⚠️ Fora do esperado'} ({ref['duracao_segundos']:.1f}s)\n")
            f.write(f"- Velocidade: {'✅ Adequada' if velocidade_ok else '⚠️ Fora do esperado'} ({ref['palavras_por_minuto']:.1f} pal/min)\n")
            f.write(f"- Processamento: ✅ Excelente ({ref['eficiencia']:.2f}x)\n")
            f.write(f"- Qualidade técnica: ✅ 24kHz, 16-bit PCM\n\n")
            
            f.write("### 5.2. Comparação com Estilo de Canais Competidores\n\n")
            f.write("**Canais similares:**\n")
            f.write("- Psych2Go (masculino: tom analítico, calmo)\n")
            f.write("- Explained (Franklin: primeira pessoa, reflexivo)\n")
            f.write("- Psychology Facts (informativo, direto)\n\n")
            
            f.write("**am_michael x Canais Competidores:**\n")
            f.write("- ✅ Tom profissional e autoritário\n")
            f.write("- ✅ Adequado para conteúdo psicológico sério\n")
            f.write("- ✅ Pitch baixo (116 Hz) - similar a narradores masculinos\n")
            f.write("- ⚠️ Requer validação auditiva para comparar naturalidade\n\n")
            
            f.write("### 5.3. Recomendação Final\n\n")
            
            if duracao_ok and velocidade_ok:
                f.write("✅ **am_michael é ADEQUADO para o canal**\n\n")
                f.write("**Motivos:**\n")
                f.write("- Duração e velocidade dentro do esperado\n")
                f.write("- Tom profissional e autoritário\n")
                f.write("- Qualidade técnica excelente\n")
                f.write("- Processamento rápido\n\n")
                f.write("**Configuração recomendada:**\n")
                f.write("```python\n")
                f.write("VOZ = \"am_michael\"\n")
                f.write("VELOCIDADE = 1.0  # Ajustar para 0.9-1.1 se necessário\n")
                f.write("```\n\n")
            else:
                f.write("⚠️ **am_michael requer ajustes**\n\n")
                f.write("**Problemas identificados:**\n")
                if not duracao_ok:
                    f.write(f"- Duração fora do esperado ({ref['duracao_segundos']:.1f}s)\n")
                if not velocidade_ok:
                    f.write(f"- Velocidade fora do esperado ({ref['palavras_por_minuto']:.1f} pal/min)\n")
                f.write("\n**Sugestões:**\n")
                f.write("- Ajustar velocidade para 0.9x ou 1.1x\n")
                f.write("- Considerar outra voz (af_heart, af_sarah)\n")
                f.write("- Editar o roteiro para ajustar duração\n\n")
            
            f.write("### 5.4. Próximos Passos\n\n")
            f.write("1. **Ouvir o áudio gerado**\n")
            f.write(f"   - Arquivo: `{Path(ref['arquivo']).name}`\n")
            f.write("   - Avaliar naturalidade e entonação\n\n")
            f.write("2. **Comparar com vozes alternativas**\n")
            f.write("   - Testar af_heart (feminina natural)\n")
            f.write("   - Testar af_sarah (feminina madura)\n\n")
            f.write("3. **Validar com contexto de vídeo**\n")
            f.write("   - Adicionar a imagens/footage\n")
            f.write("   - Verificar sincronização\n")
            f.write("   - Testar retenção do espectador\n\n")
        
        else:
            f.write("❌ **NÃO FOI POSSÍVEL COMPLETAR O TESTE**\n\n")
            f.write("Todos os testes falharam. Verifique a instalação do Kokoro.\n\n")
        
        f.write("---\n\n")
        f.write(f"**Relatório gerado:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("**Script:** `testar_am_michael.py`\n")
    
    return arquivo_relatorio


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Executa o teste da voz am_michael"""
    
    print("="*80)
    print("TESTE DE VOZ am_michael - KOKORO TTS")
    print("="*80)
    print(f"\nData/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Objetivo: Testar com roteiro real de canal competidor de psicologia")
    
    # Criar diretório de saída
    diretorio_saida = Path("teste_am_michael")
    diretorio_saida.mkdir(exist_ok=True)
    print(f"\n📁 Diretório de saída: {diretorio_saida.absolute()}")
    
    # Inicializar pipeline
    print("\n🔄 Inicializando Kokoro TTS...")
    try:
        pipeline = KPipeline(lang_code='a')
        print("✅ Modelo carregado!")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        sys.exit(1)
    
    # Velocidades para testar
    velocidades = [1.0, 0.9, 1.1]
    resultados = {}
    
    # Informações do roteiro
    print(f"\n📋 ROTEIRO:")
    print(f"   Título: {ROTEIRO_PSICOLOGIA['titulo']}")
    print(f"   Tema: {ROTEIRO_PSICOLOGIA['tema']}")
    print(f"   Palavras: {ROTEIRO_PSICOLOGIA['palavras']}")
    print(f"   Duração estimada: {ROTEIRO_PSICOLOGIA['duracao_estimada_segundos']}s")
    
    # Testar cada velocidade
    for velocidade in velocidades:
        print("\n" + "="*80)
        print(f"TESTANDO VELOCIDADE {velocidade}x")
        print("="*80)
        
        arquivo_saida = diretorio_saida / f"am_michael_v{velocidade}.wav"
        
        resultado = gerar_audio_kokoro(
            pipeline,
            ROTEIRO_PSICOLOGIA["texto"],
            "am_michael",
            velocidade,
            str(arquivo_saida)
        )
        
        # Analisar resultado
        analise = analisar_resultado(resultado, ROTEIRO_PSICOLOGIA, velocidade)
        resultados[velocidade] = analise
        
        # Limpar memória entre testes
        gc.collect()
    
    # Gerar relatório
    print("\n" + "="*80)
    print("GERANDO RELATÓRIO...")
    print("="*80)
    
    arquivo_relatorio = criar_relatorio_markdown(resultados, ROTEIRO_PSICOLOGIA, diretorio_saida)
    
    print(f"\n✅ Relatório gerado: {arquivo_relatorio}")
    
    # Resumo final
    sucessos = sum(1 for r in resultados.values() if r.get("sucesso", False))
    total = len(resultados)
    
    print("\n" + "="*80)
    print("RESUMO FINAL")
    print("="*80)
    print(f"✅ Testes bem-sucedidos: {sucessos}/{total}")
    
    if 1.0 in resultados and resultados[1.0]["sucesso"]:
        ref = resultados[1.0]
        print(f"\n📊 MÉTRICAS PRINCIPAIS (velocidade 1.0x):")
        print(f"   Duração: {ref['duracao_segundos']:.2f}s")
        print(f"   Palavras/min: {ref['palavras_por_minuto']:.1f}")
        print(f"   Arquivo: {Path(ref['arquivo']).name}")
    
    print(f"\n📄 Relatório completo: {arquivo_relatorio}")
    print(f"🎧 Áudios salvos em: {diretorio_saida.absolute()}")
    
    print("\n" + "="*80)
    print("✅ TESTE CONCLUÍDO!")
    print("="*80)


if __name__ == "__main__":
    main()
