# META-PROMPT: MONTAGEM DE VÍDEO COM FFmpeg

## CONTEXTO
Você é um especialista em edição de vídeo usando FFmpeg para criação automatizada de vídeos para canais dark do YouTube no nicho de psicologia.

## OBJETIVO
Definir o processo completo de montagem de vídeo usando FFmpeg, desde a combinação imagem+áudio de cada cena até a montagem final com transições, trilha sonora e exportação otimizada para YouTube.

## FLUXO DE PRODUÇÃO

### Estrutura de Arquivos
```
video-production/1-psicologia/videos/<video>/
├── 02-imagens/          # Imagens de cada cena
├── 04-audio/
│   ├── naracao/         # Áudios de narração
│   └── trilha/          # Trilha sonora de fundo
├── 05-clipes/           # Clipes montados (imagem + áudio)
├── 06-final/            # Vídeo final renderizado
└── 07-processo.md       # Documentação do processo
```

## ETAPA 1: MONTAGEM DE CLIPES INDIVIDUAIS

### Comando Básico (Imagem + Áudio)
```bash
# Montar cena individual
ffmpeg -loop 1 -i 02-imagens/cena_001.jpg -i 04-audio/naracao/cena_001.mp3 \
  -c:v libx264 -tune stillimage -preset medium -crf 23 \
  -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  05-clipes/cena_001.mp4
```

### Parâmetros Explicados
```markdown
-loop 1                    # Loop da imagem estática
-i 02-imagens/cena_001.jpg # Imagem de entrada
-i 04-audio/...            # Áudio de entrada
-c:v libx264               # Codec de vídeo (padrão YouTube)
-tune stillimage           # Otimizado para imagens estáticas
-preset medium             # Equilíbrio速度/qualidade
-crf 23                    # Qualidade (18-28, menor=melhor)
-c:a aac                   # Codec de áudio
-b:a 192k                  # Bitrate de áudio
-pix_fmt yuv420p           # Compatibilidade máxima
-shortest                  # Duração = áudio (mais curto)
-vf "..."                  # Filtros de vídeo (escala+pad)
```

### Efeitos Visuais (Opcional)

#### Zoom Lento (Ken Burns Effect)
```bash
ffmpeg -loop 1 -i 02-imagens/cena_001.jpg -i 04-audio/naracao/cena_001.mp3 \
  -vf "zoompan=z='min(zoom+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',scale=1920:1080" \
  -c:v libx264 -tune stillimage -preset medium -crf 23 \
  -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \
  05-clipes/cena_001.mp4
```

#### Pan Lento
```bash
ffmpeg -loop 1 -i 02-imagens/cena_001.jpg -i 04-audio/naracao/cena_001.mp3 \
  -vf "zoompan=z='1.3':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+sin(t)*50',scale=1920:1080" \
  -c:v libx264 -tune stillimage -preset medium -crf 23 \
  -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \
  05-clipes/cena_001.mp4
```

#### Fade In/Out Suave
```bash
ffmpeg -loop 1 -i 02-imagens/cena_001.jpg -i 04-audio/naracao/cena_001.mp3 \
  -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=7.5:d=0.5,scale=1920:1080" \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=7.5:d=0.5" \
  -c:v libx264 -tune stillimage -preset medium -crf 23 \
  -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \
  05-clipes/cena_001.mp4
```

## ETAPA 2: CRIAÇÃO DE LISTA DE CLIPES

### Criar Arquivo de Lista (concat.txt)
```bash
# Arquivo: 05-clipes/concat.txt
file 'cena_001.mp4'
file 'cena_002.mp4'
file 'cena_003.mp4'
# ...continuar para todas as cenas
```

### Script Automático (Python)
```python
#!/usr/bin/env python3
"""Cria lista de clipes para concatenação FFmpeg."""

from pathlib import Path

clipes_dir = Path("05-clipes")
lista_file = clipes_dir / "concat.txt"

# Encontrar todos os mp4 e ordenar
clipes = sorted(clipes_dir.glob("cena_*.mp4"))

# Criar lista para concatenação
with open(lista_file, 'w') as f:
    for clipe in clipes:
        f.write(f"file '{clipe.name}'\n")

print(f"✓ Lista criada: {lista_file}")
print(f"✓ Total de clipes: {len(clipes)}")
```

## ETAPA 3: CONCATENAÇÃO DE TODOS OS CLIPES

### Método 1: Concat Demuxer (Mais Rápido)
```bash
ffmpeg -f concat -safe 0 -i 05-clipes/concat.txt \
  -c copy 06-final/video_sem_trilha.mp4
```

### Método 2: Filter Complex (Com Transições)
```bash
# Transição fade de 0.5s entre clipes
ffmpeg -f concat -safe 0 -i 05-clipes/concat.txt \
  -filter_complex "[0:v]fade=t=out:st=4.5:d=0.5[v0];[1:v]fade=t=in:st=0:d=0.5[v1];[v0][v1]concat=n=2:v=1:a=0[outv]" \
  -map "[outv]" -c:v libx264 -preset medium -crf 23 \
  06-final/video_com_transicao.mp4
```

### Método 3: Re-encode (Compatibilidade Total)
```bash
ffmpeg -f concat -safe 0 -i 05-clipes/concat.txt \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  06-final/video_completo.mp4
```

## ETAPA 4: ADICIONAR TRILHA SONORA

### Misturar Narração + Trilha
```bash
# Calcular duração total do vídeo
DURACAO=$(ffprobe -i 06-final/video_completo.mp4 -show_entries format=duration -v quiet -of csv="p=0")

# Adicionar trilha de fundo em loop
ffmpeg -i 06-final/video_completo.mp4 -stream_loop -1 -i 04-audio/trilha/trilha_fundo.mp3 \
  -filter_complex "[1:a]volume=0.15,atrim=0:$DURACAO,asetpts=PTS-STARTPTS[trilha];[0:a][trilha]amix=inputs=2:duration=first" \
  -c:v copy -c:a aac -b:a 192k \
  06-final/video_com_trilha.mp4
```

### Parâmetros de Mixagem
```markdown
volume=0.15          # Volume da trilha (15% - ajustável)
duration=first       # Duração = vídeo (não trilha)
inputs=2             # 2 faixas de áudio
```

## ETAPA 5: ADICIONAR LEGENDAS (OPCIONAL)

### Legendas Simples (Texto Fixo)
```bash
ffmpeg -i 06-final/video_com_trilha.mp4 \
  -vf "drawtext=text='Seu texto aqui':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-100:box=1:boxcolor=black@0.5:boxborderw=5" \
  -c:a copy 06-final/video_com_legendas.mp4
```

### Legendas a Partir de Arquivo SRT
```bash
ffmpeg -i 06-final/video_com_trilha.mp4 -i legendas.srt \
  -c:v libx264 -preset medium -crf 23 \
  -c:a copy -c:s srt \
  06-final/video_final_com_legendas.mp4
```

### Script para Gerar Legendas Automáticas
```python
#!/usr/bin/env python3
"""Gera arquivo de legendas SRT a partir do roteiro."""

import json
from datetime import timedelta

def tempo_para_srt(segundos):
    """Converte segundos para formato SRT."""
    td = timedelta(seconds=segundos)
    horas, resto = divmod(td.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    milissegundos = td.microseconds // 1000
    return f"{horas:02}:{minutos:02}:{segundos:02},{milissegundos:03}"

def criar_legendas(script_file, output_file):
    """Cria legendas SRT do roteiro JSON."""
    
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    tempo_atual = 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, cena in enumerate(script['cenas']):
            duracao = cena['duracao_segundos']
            texto = cena['conteudo']
            
            inicio = tempo_para_srt(tempo_atual)
            fim = tempo_para_srt(tempo_atual + duracao)
            
            f.write(f"{i + 1}\n")
            f.write(f"{inicio} --> {fim}\n")
            f.write(f"{texto}\n\n")
            
            tempo_atual += duracao

if __name__ == "__main__":
    import sys
    criar_legendas(sys.argv[1], sys.argv[2])
```

## ETAPA 6: EXPORTAÇÃO FINAL

### Configurações Otimizadas para YouTube
```bash
# Exportação final com melhores configurações
ffmpeg -i 06-final/video_com_trilha.mp4 \
  -c:v libx264 -preset medium -crf 21 \
  -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 192k \
  -vf "scale=1920:1080" \
  07-final/video_final_1080p.mp4

# 720p (alternativa menor)
ffmpeg -i 06-final/video_com_trilha.mp4 \
  -c:v libx264 -preset medium -crf 21 \
  -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 128k \
  -vf "scale=1280:720" \
  07-final/video_final_720p.mp4
```

### Parâmetros de Qualidade
```markdown
Resolution:  1920x1080 (Full HD) ou 1280x720 (HD)
Codec:      H.264 (libx264)
CRF:        21 (18-28, menor=melhor, 21 ideal para YouTube)
Preset:     medium (equilíbrio速度/qualidade)
Audio:      AAC 192k (1080p) ou 128k (720p)
Pixel Format: yuv420p (compatibilidade máxima)
Faststart:  +faststart (playback inicia rápido)
```

## SCRIPT AUTOMATIZADO COMPLETO

### `montar_video.py`
```python
#!/usr/bin/env python3
"""
Script completo de montagem de vídeo com FFmpeg.
Do roteiro ao vídeo final.
"""

import json
import subprocess
from pathlib import Path

def montar_clipe(imagem, audio, output, efeito=None):
    """Monta clipe individual (imagem + áudio)."""
    
    vf_filters = ["scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"]
    
    if efeito == "zoom":
        vf_filters.insert(0, "zoompan=z='min(zoom+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'")
    elif efeito == "fade":
        vf_filters.append("fade=t=in:st=0:d=0.5,fade=t=out:st=7.5:d=0.5")
    
    vf = ",".join(vf_filters)
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(imagem),
        "-i", str(audio),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-vf", vf,
        "-shortest",
        str(output)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✓ Clipe montado: {output}")

def criar_lista_clipes(clipes_dir, output_file):
    """Cria lista de clipes para concatenação."""
    
    clipes = sorted(clipes_dir.glob("cena_*.mp4"))
    
    with open(output_file, 'w') as f:
        for clipe in clipes:
            f.write(f"file '{clipe.name}'\n")
    
    print(f"✓ Lista criada: {len(clipes)} clipes")
    return len(clipes)

def concatenar_clipes(lista_file, output):
    """Concatena todos os clipes em vídeo completo."""
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(lista_file),
        "-c", "copy",
        str(output)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✓ Vídeo concatenado: {output}")

def adicionar_trilha(video, trilha, output, volume_trilha=0.15):
    """Adiciona trilha sonora ao vídeo."""
    
    # Obter duração do vídeo
    cmd_duracao = [
        "ffprobe", "-i", str(video),
        "-show_entries", "format=duration",
        "-v", "quiet", "-of", "csv=p=0"
    ]
    
    resultado = subprocess.run(cmd_duracao, capture_output=True, text=True)
    duracao = resultado.stdout.strip()
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video),
        "-stream_loop", "-1",
        "-i", str(trilha),
        "-filter_complex",
        f"[1:a]volume={volume_trilha},atrim=0:{duracao},asetpts=PTS-STARTPTS[trilha];[0:a][trilha]amix=inputs=2:duration=first",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(output)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✓ Trilha adicionada: {output}")

def montar_video_completo(project_dir):
    """Monta vídeo completo do projeto."""
    
    project = Path(project_dir)
    
    # Diretórios
    imagens_dir = project / "02-imagens"
    audio_dir = project / "04-audio/naracao"
    clipes_dir = project / "05-clipes"
    trilha_file = project / "04-audio/trilha/trilha_fundo.mp3"
    final_dir = project / "07-final"
    
    clipes_dir.mkdir(exist_ok=True)
    final_dir.mkdir(exist_ok=True)
    
    # Montar cada clipe
    print("Montando clipes individuais...")
    for imagem in sorted(imagens_dir.glob("cena_*.jpg")):
        numero = imagem.stem.split("_")[1]
        audio = audio_dir / f"cena_{numero.zfill(3)}.mp3"
        output = clipes_dir / f"cena_{numero.zfill(3)}.mp4"
        
        if audio.exists():
            montar_clipe(imagem, audio, output, efeito="zoom")
    
    # Criar lista de clipes
    print("Criando lista de concatenação...")
    lista_file = clipes_dir / "concat.txt"
    criar_lista_clipes(clipes_dir, lista_file)
    
    # Concatenar clipes
    print("Concatenando clipes...")
    video_sem_trilha = final_dir / "video_sem_trilha.mp4"
    concatenar_clipes(lista_file, video_sem_trilha)
    
    # Adicionar trilha
    print("Adicionando trilha sonora...")
    video_final = final_dir / "video_final.mp4"
    adicionar_trilha(video_sem_trilha, trilha_file, video_final)
    
    print(f"\n✓ VÍDEO FINAL: {video_final}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python montar_video.py <diretorio_do_video>")
        sys.exit(1)
    
    montar_video_completo(sys.argv[1])
```

## OTIMIZAÇÕES DE PERFORMANCE

### Presets de Velocidade
```markdown
-ultrafast  ( Mais rápido, menor qualidade, arquivo maior)
-superfast
-veryfast
-faster
-fast
-medium      ( Equilíbrio recomendado )
-slow
-slower
-veryslow    ( Mais lento, melhor qualidade, arquivo menor)
```

### Paralelização
```bash
# Montar clipes em paralelo (GNU Parallel)
ls 02-imagens/cena_*.jpg | parallel -j 4 \
  'ffmpeg -loop 1 -i {} -i 04-audio/naracao/{= s:cena_0(\d+).jpg:cena_0$1.mp3 =} \
  -c:v libx264 -tune stillimage -preset fast -crf 23 \
  -c:a aac -b:a 192k -pix_fmt yuv420p -shortest \
  05-clipes/{= s:cena_0(\d+).jpg:cena_0$1.mp4 =}'
```

## VALIDAÇÃO DE QUALIDADE

### Checklist Pré-Upload
```markdown
- [ ] Resolução correta (1920x1080 ou 1280x720)
- [ ] Codec H.264 (compatível com YouTube)
- [ ] Áudio AAC 192k (1080p) ou 128k (720p)
- [ ] Pixel format yuv420p
- [ ] Faststart habilitado
- [ ] Trilha sonora presente e em volume adequado
- [ ] Todas as cenas presentes na ordem correta
- [ ] Transições suaves (se aplicável)
- [ ] Sem cortes ou glitches
- [ ] Duração total conforme planejado
```

### Validação Técnica
```bash
# Informações completas do vídeo
ffprobe -v quiet -print_format json -show_format -show_streams video_final.mp4

# Testar reprodução
ffplay video_final.mp4

# Verificar integridade
ffmpeg -v error -i video_final.mp3 -f null - 2>&1
```

## SOLUÇÃO DE PROBLEMAS

### Problema: Vídeo/Dessincronizado
**Solução**:
```bash
# Garantir áudio mais curto que vídeo (flag -shortest)
# Re-encode com sincronização forçada
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -async 1 output.mp4
```

### Problema: Qualidade Visual Ruim
**Solução**:
- Aumentar CRF (baixar para 18-21)
- Mudar preset para slower
- Verificar resolução da imagem original

### Problema: Arquivo Muito Grande
**Solução**:
- Aumentar CRF (subir para 23-26)
- Usar preset slower (melhor compressão)
- Reduzir bitrate de áudio para 128k

## CHECKLIST FINAL

### Antes de Considerar Completo
- [ ] Todas as cenas montadas
- [ ] Vídeo final reproduz corretamente
- [ ] Áudio sincronizado
- [ ] Trilha presente e em volume adequado
- [ ] Qualidade visual aceitável
- [ ] Tamanho de arquivo razoável (<1GB para 10min)
- [ ] Legadas presentes (se aplicável)
- [ ] Validado em ffplay
- [ ] Pronto para upload no YouTube
