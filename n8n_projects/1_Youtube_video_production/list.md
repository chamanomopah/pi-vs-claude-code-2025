
workflow gerador de videos pra canal dark no youtube

workflow de modelagem 00 (ATUALIZADO - Modelagem de Canal Top Videos) : 2SQKMc2vBxc7nlUK
  - Script Python: youtube_channel_scraper.py (NOVO)
  - Script Python: youtube_transcript_downloader.py (existente)
  - Script Python: video_frame_extractor.py (existente)
  - Gera 4 metaprompts: script, image, thumbnail, title

workflow principal (que executa os subworkflows abaixo):  0_video_production_workflow : 6M2JKleKJhQPIQma (id_workflow)
subworkflow 1 pra gerar gerar o script: 1_script_gen : LPU4FBXyKFIj4sUH
subworkflow 2 pra gerar imagem: 2_image_gen : wPdzosVxWBdPI2FS
subworkflow 3 pra adicionar audio: 3_add_audio : soN9Bjns6tuuKMVH
subworkflow 4 pra gerar video final: 4_Merge_all : Zyi3ZMQxMThwrQIB