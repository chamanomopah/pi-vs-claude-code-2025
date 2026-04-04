# Atualização v1.1 - Suporte a file:/// e Refatoração

## Data
2026-04-04

## Mudanças Implementadas

### 1. Nova Função: `converter_file_url_to_path()`
- Converte URLs no formato `file:///` para caminhos do sistema de arquivos
- Suporta Windows (`file:///C:/path` → `C:\path`)
- Suporta Linux/Mac (`file:///home/user/path` → `/home/user/path`)
- Mantém compatibilidade com outros formatos

### 2. Refatoração Principal: Interface de Linha de Comando
- **REMOVIDA**: Variável `VIDEO_URL` no início do script
- **ADICIONADO**: Argumento posicional `url` via `argparse`
- **PADRÃO**: Agora segue o MESMO padrão do `youtube_transcript_downloader.py`
- **COMPATIBILIDADE**: Interface consistente entre os scripts

### 3. Atualização da Função: `extrair_id_video()`
- Agora processa URLs `file:///` corretamente
- Extrai o nome do arquivo do caminho convertido

### 4. Atualização da Função: `main()`
- Usa `argparse` para processar argumentos da linha de comando
- Detecção automática de três tipos de entrada:
  - URL remota (`http://`, `https://`)
  - Arquivo local (`file:///`)
  - Caminho direto (caminho local normal)
- Mensagens informativas sobre o tipo detectado
- Opções adicionais: `-o/--output`, `-f/--fps`

## Comparação Antes vs Depois

### Antes (v1.0)
```python
# Era necessário editar o script
VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# Depois executar
python video_frame_extractor.py
```

### Depois (v1.1)
```python
# Passa a URL como argumento (como o youtube_transcript_downloader.py)
python video_frame_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Formatos Suportados

| Formato | Exemplo | Ação |
|---------|---------|------|
| URL Remota | `https://youtube.com/watch?v=xxx` | Baixa o vídeo |
| file:/// Windows | `file:///C:/Videos/video.mp4` | Converte e usa |
| file:/// Linux | `file:///home/user/video.mp4` | Converte e usa |
| Caminho Direto | `C:/Videos/video.mp4` | Usa diretamente |
| Caminho Relativo | `video.mp4` | Usa diretamente |

## Testes Realizados

✅ Formato `file:///` no Windows
✅ Caminho direto local
✅ Argumento de linha de comando `url`
✅ Opções `-o` e `-f`
✅ Detecção automática do tipo de entrada
✅ Extração de frames com todos os formatos
✅ Compatibilidade com o padrão do `youtube_transcript_downloader.py`

## Arquivos Modificados

1. `video_frame_extractor.py` - **REFATORADO** - Interface com argparse
2. `README_FRAME_EXTRACTOR.md` - **ATUALIZADO** - Novos exemplos de uso
3. `TEST_FILE_URL_FORMAT.md` - **NOVO** - Testes do formato file:///
4. `exemplos_configuracao.py` - **OBSOLETO** (ainda existe mas não é mais necessário)
5. `COMPARACAO_SCRIPTS.md` - **NOVO** - Comparação entre os scripts
6. `run_frame_extractor.bat` - **ATUALIZADO** - Novas instruções
7. `run_frame_extractor.sh` - **ATUALIZADO** - Novas instruções

## Padrão de Projeto Agora Consistente

Ambos os scripts seguem o **MESMO padrão**:

| Aspecto | youtube_transcript_downloader.py | video_frame_extractor.py |
|---------|----------------------------------|--------------------------|
| Argumento `url` | ✅ Posicional | ✅ Posicional |
| Opção `-o` | ✅ Arquivo de saída | ✅ Pasta de saída |
| argparse | ✅ Sim | ✅ Sim |
| Encoding Windows | ✅ Corrigido | ✅ Corrigido |
| Docstring | ✅ Padrão | ✅ Padrão |
| Tratamento de erros | ✅ sys.exit(1) | ✅ sys.exit(1) |

## Compatibilidade

- ✅ Windows 10/11
- ✅ Linux
- ✅ macOS
- ✅ Python 3.7+
- ✅ OpenCV 4.8+
