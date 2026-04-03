# Fluxograma da Extensão LiveKit para Pi

## Descrição

Este fluxograma visualiza o funcionamento completo da extensão LiveKit para o Pi, que permite interação por voz com o agente de codificação. O diagrama mostra o fluxo completo da conversação, desde o início da sessão até o encerramento, incluindo tratamento de erros e estados de recuperação.

**Componentes principais:**
- **Pi (Coding Agent)**: Agente principal que processa comandos e gera respostas
- **LiveKit Server**: Infraestrutura WebRTC para comunicação de áudio em tempo real
- **Deepgram STT**: Speech-to-Text para transcrição do áudio do usuário
- **Cartesia TTS**: Text-to-Speech para síntese de voz do Pi
- **VAD (Voice Activity Detection)**: Detecção de atividade de voz (usando Silero)

---

## Mermaid Code

```mermaid
graph TD
    %% =============================================
    %% ESTILOS
    %% =============================================
    classDef usuario fill:#e1f5ff,stroke:#0277bd,stroke-width:2px
    classDef pi fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef livekit fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef deepgram fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef cartesia fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef vad fill:#fff8e1,stroke:#f9a825,stroke-width:2px
    classDef erro fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef sucesso fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef decisao fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef inicio fill:#e0f2f1,stroke:#00695c,stroke-width:3px

    %% =============================================
    %% INÍCIO
    %% =============================================
    INICIO([🎤 Iniciar Sessão de Voz]):::inicio

    %% =============================================
    %% INICIALIZAÇÃO
    %% =============================================
    INICIO --> SETUP[Configurar AgentSession<br/>STT, LLM, TTS, VAD]:::pi
    SETUP --> PREWARM[Prewarm VAD<br/>Silero model]:::vad

    %% =============================================
    /// CONEXÃO COM LIVEKIT
    %% =============================================
    PREWARM --> TOKEN{Gerar Token<br/>JWT válido?}:::decisao
    TOKEN -->|Sim| CONNECT[Conectar ao<br/>LiveKit Server]:::livekit
    TOKEN -->|Não| ERRO_TOKEN[❌ Erro: Token inválido/expirado]:::erro
    ERRO_TOKEN --> RETRY_TOKEN[Gerar novo token]:::livekit
    RETRY_TOKEN --> CONNECT

    %% =============================================
    /// VERIFICAÇÃO DE CONEXÃO
    %% =============================================
    CONNECT --> CONEXAO_OK{Conexão<br/>estabelecida?}:::decisao
    CONEXAO_OK -->|Sim| SAUDACAO[🔊 Reproduzir saudação<br/>via Cartesia TTS]:::cartesia
    CONEXAO_OK -->|Não| ERRO_CONNECT[❌ Erro: Falha de conexão]:::erro
    ERRO_CONNECT --> TENTAR_CONNECT[Reiniciar conexão<br/>max 3 tentativas]:::livekit
    TENTAR_CONNECT --> CONEXAO_OK
    TENTAR_CONNECT -->|Excedeu| FALHA([❌ Falha crítica:<br/>Não foi possível conectar]):::erro

    %% =============================================
    /// LOOP PRINCIPAL DE CONVERSAÇÃO
    %% =============================================
    SAUDACAO --> AGUARDAR([⏸️ Aguardando input do usuário]):::inicio

    AGUARDAR --> CAPTURA[🎤 Capturar áudio<br/>via WebRTC]:::livekit

    %% =============================================
    /// DETECÇÃO DE VOZ (VAD)
    %% =============================================
    CAPTURA --> VAD_CHECK{VAD detectou<br/>voz?}:::decisao
    VAD_CHECK -->|Sim| STT_DEEPGRAM[📝 Transcrever áudio<br/>via Deepgram STT]:::deepgram
    VAD_CHECK -->|Não| SILENCIO{Silêncio por<br/>>5 segundos?}:::decisao
    SILENCIO -->|Sim| VERIFICAR_USUARIO{Usuário<br/>presente?}:::decisao
    SILENCIO -->|Não| AGUARDAR

    VERIFICAR_USUARIO -->|Não| ENCERRAR([👋 Encerrar sessão por inatividade]):::inicio
    VERIFICAR_USUARIO -->|Sim| AGUARDAR

    %% =============================================
    /// TRANSCRIÇÃO (STT)
    %% =============================================
    STT_DEEPGRAM --> STT_RESULTADO{Transcrição<br/>bem-sucedida?}:::decisao
    STT_RESULTADO -->|Sim| EXIBIR_TXT[Exibir texto<br/>na UI do Pi]:::pi
    STT_RESULTADO -->|Não| ERRO_STT[❌ Erro STT]:::erro
    ERRO_STT --> RECAPTURAR[Pedir para repetir]:::cartesia
    RECAPTURAR --> AGUARDAR

    %% =============================================
    /// PROCESSAMENTO PELO PI
    %% =============================================
    EXIBIR_TXT --> ENVIAR_PI[Enviar texto ao<br/>Pi Coding Agent]:::pi

    ENVIAR_PI --> PI_PROCESSAR[Processar comando<br/>com LLM]:::pi

    PI_PROCESSAR --> PI_RESULTADO{Processamento<br/>bem-sucedido?}:::decisao
    PI_RESULTADO -->|Sim| PI_RESPOSTA[Gerar resposta<br/>do Pi]:::pi
    PI_RESULTADO -->|Não| ERRO_PI[❌ Erro no Pi]:::erro

    %% =============================================
    /// TRATAMENTO DE ERROS DO PI
    %% =============================================
    ERRO_PI --> TIPO_ERRO{Tipo de erro?}:::decisao

    TIPO_ERRO -->|Comando inválido| RESPONDER_ERRO["Resposta: Não entendi.<br/>Pode reformular?"]:::cartesia
    TIPO_ERRO -->|Erro de ferramenta| RESPONDER_TOOL["Resposta: Erro ao executar.<br/>Tentando novamente..."]:::cartesia
    TIPO_ERRO -->|Erro crítico| RESPONDER_CRITICO["Resposta: Erro fatal.<br/>Encerrando sessão."]:::cartesia

    RESPONDER_ERRO --> AGUARDAR
    RESPONDER_TOOL --> TENTAR_NOVAMENTE[Reprocessar comando]:::pi
    TENTAR_NOVAMENTE --> PI_PROCESSAR
    RESPONDER_CRITICO --> ENCERRAR

    %% =============================================
    /// SÍNTESE DE VOZ (TTS)
    %% =============================================
    PI_RESPOSTA --> TTS_CARTEISA[🔊 Sintetizar voz<br/>via Cartesia TTS]:::cartesia

    TTS_CARTEISA --> TTS_RESULTADO{TTS<br/>bem-sucedido?}:::decisao
    TTS_RESULTADO -->|Sim| REPRODUZIR[🔊 Reproduzir áudio<br/>para o usuário]:::livekit
    TTS_RESULTADO -->|Não| ERRO_TTS[❌ Erro TTS]:::erro

    %% =============================================
    /// TRATAMENTO DE ERROS DE TTS
    %% =============================================
    ERRO_TTS --> FALLBACK_TTS[Tentar TTS fallback<br/>ou mostrar texto]:::pi
    FALLBACK_TTS --> EXIBIR_TEXTO_ERRO[Exibir resposta<br/>como texto]:::pi
    EXIBIR_TEXTO_ERRO --> AGUARDAR

    %% =============================================
    /// VERIFICAÇÃO DE CONTINUIDADE
    %% =============================================
    REPRODUZIR --> VERIFICAR_CONTINUAR{Usuário quer<br/>continuar?}:::decisao
    VERIFICAR_CONTINUAR -->|Sim| AGUARDAR
    VERIFICAR_CONTINUAR -->|Não| ENCERRAR

    %% =============================================
    /// ESTADOS DE ERRO ADICIONAIS
    %% =============================================
    %% Falha de rede
    subgraph REDE ["Falhas de Rede"]
        CHECK_REDE{Conexão<br/>estável?}:::decisao
        ERRO_REDE[❌ Erro de rede]:::erro
        RECONEXAO[Reconectar<br/>automaticamente]:::livekit
    end

    %% Falha de API
    subgraph API_ERROS ["Falhas de API"]
        CHECK_DEEPGRAM{Deepgram<br/>disponível?}:::decisao
        CHECK_CARTEISA{Cartesia<br/>disponível?}:::decisao
        ERRO_API[❌ API indisponível]:::erro
        MODO_FALLBACK[Modo fallback<br/>somente texto]:::pi
    end

    %% =============================================
    /// ESTADOS DE ENCERRAMENTO
    %% =============================================
    ENCERRAR --> LIMPAR[Limpar recursos<br/>e sessões]:::livekit
    LIMPAR --> DESCONECTAR[Desconectar do<br/>LiveKit Server]:::livekit
    DESCONECTAR --> FIM([✅ Sessão encerrada]):::sucesso

    %% =============================================
    /// LABELS ADICIONAIS
    %% =============================================
    subgraph LEGENDA ["Legenda de Componentes"]
        USU((Usuário)):::usuario
        PI_SYS((Pi System)):::pi
        LK((LiveKit Server)):::livekit
        DG((Deepgram STT)):::deepgram
        CT((Cartesia TTS)):::cartesia
        V((VAD Silero)):::vad
    end

    %% Conexões de estados especiais
    CAPTURA -.-> CHECK_REDE
    CHECK_REDE -->|Não| ERRO_REDE
    ERRO_REDE --> RECONEXAO
    RECONEXAO --> CAPTURA

    STT_DEEPGRAM -.-> CHECK_DEEPGRAM
    CHECK_DEEPGRAM -->|Não| ERRO_API
    ERRO_API --> MODO_FALLBACK
    MODO_FALLBACK --> EXIBIR_TXT

    TTS_CARTEISA -.-> CHECK_CARTEISA
    CHECK_CARTEISA -->|Não| ERRO_API
    ERRO_API --> MODO_FALLBACK
    MODO_FALLBACK --> EXIBIR_TEXTO_ERRO
```

---

## Legenda dos Símbolos

| Símbolo | Significado |
|---------|-------------|
| 🎤 | Entrada de áudio do usuário |
| 🔊 | Saída de áudio para o usuário |
| 📝 | Transcrição de texto |
| ✅ | Estado de sucesso |
| ❌ | Estado de erro |
| ⏸️ | Estado de espera |
| 👋 | Encerramento de sessão |
| `()` | Estado inicial/final |
| `[]` | Processo/ação |
| `{}` | Decisão/condição |
| `--->` | Fluxo principal |
| `-.->` | Fluxo de verificação/monitoramento |

---

## Cores dos Componentes

| Cor | Componente | Descrição |
|-----|------------|-----------|
| 🔵 Azul | Usuário | Interface e interações do usuário |
| 🟣 Roxo | Pi System | Agente de codificação e lógica principal |
| 🟠 Laranja | LiveKit Server | Infraestrutura WebRTC |
| 🟢 Verde | Deepgram STT | Transcrição de fala para texto |
| 🔴 Rosa | Cartesia TTS | Síntese de texto para fala |
| 🟡 Amarelo | VAD | Detecção de atividade de voz |
| 🔴 Vermelho | Erro | Estados de erro e falhas |
| 🟢 Verde claro | Sucesso | Estados de sucesso |
| 🟡 Amarelo claro | Decisão | Pontos de decisão no fluxo |
| 🟢 Teal | Início/Fim | Pontos de entrada e saída |

---

## Explicação dos Principais Fluxos

### 1. Fluxo Principal de Conversação

O fluxo principal representa o caminho ideal de uma interação de voz com o Pi:

1. **Inicialização**: Configuração da sessão, prewarming do VAD, geração de token
2. **Conexão**: Conexão ao LiveKit Server e reprodução de saudação
3. **Captura de Áudio**: O usuário fala, o áudio é capturado via WebRTC
4. **Detecção de Voz**: VAD detecta quando o usuário começa/para de falar
5. **Transcrição**: Deepgram STT transcreve o áudio para texto
6. **Processamento**: Pi processa o comando usando LLM
7. **Síntese**: Cartesia TTS gera áudio da resposta
8. **Reprodução**: Áudio é enviado de volta ao usuário
9. **Loop**: Processo se repete até o usuário encerrar

### 2. Fluxo de Tratamento de Erros

Vários tipos de erros são tratados:

- **Erros de token**: Token inválido ou expirado → gerar novo token
- **Erros de conexão**: Falha ao conectar ao LiveKit → tentar reconexão (max 3x)
- **Erros de STT**: Falha na transcrição → pedir para repetir
- **Erros do Pi**: Comando inválido, erro de ferramenta, erro crítico
- **Erros de TTS**: Falha na síntese → fallback para texto
- **Erros de rede**: Conexão instável → reconexão automática
- **Erros de API**: Deepgram/Cartesia indisponíveis → modo texto

### 3. Estados de Encerramento

A sessão pode ser encerrada de várias formas:

- **Inatividade**: Usuário não interage por mais de 5 segundos
- **Escolha do usuário**: Usuário diz "tchau" ou comando similar
- **Erro crítico**: Erro fatal que impede continuação
- **Encerramento normal**: Usuário decide parar

### 4. Mecanismos de Recuperação

O sistema inclui vários mecanismos de recuperação:

- **Reconexão automática**: Em caso de falha de rede
- **Fallback para texto**: Quando TTS/STT falham
- **Tentativas de reprocessamento**: Para erros transitórios
- **Modo degradado**: Operação limitada quando serviços parciais falham

---

## Como Usar Este Fluxograma

### Durante o Desenvolvimento

1. **Mapeamento de requisitos**: Use o fluxograma para identificar todos os componentes necessários
2. **Implementação**: Siga o fluxo principal primeiro, depois adicione tratamento de erros
3. **Testes**: Use os caminhos de erro para criar casos de teste
4. **Documentação**: O fluxograma serve como documentação visual do sistema

### Para Debugging

1. **Identificar o ponto de falha**: Trace o caminho até encontrar onde o fluxo parou
2. **Verificar estados**: Confirme se cada componente está no estado esperado
3. **Testar caminhos alternativos**: Simule erros para testar recuperação
4. **Verificar logs**: Use os estados para correlacionar com logs

### Para Onboarding

1. **Visão geral**: Mostre o fluxograma para novos desenvolvedores
2. **Explicação de componentes**: Use a legenda para explicar cada parte
3. **Cenários**: Percorra o fluxograma com exemplos de uso reais
4. **Referência**: Mantenha o fluxograma acessível durante o desenvolvimento

---

## Notas Técnicas Importantes

### Configuração da AgentSession

```python
session = AgentSession(
    stt=inference.STT(model="deepgram/nova-3-general", language="multi"),
    llm=inference.LLM(model="openai/gpt-4.1-mini"),
    tts=inference.TTS(
        model="cartesia/sonic-3",
        voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
    ),
    vad=silero.VAD.load(),
    preemptive_generation=True,
)
```

### API Keys Necessárias

```env
DEEPGRAM_API_KEY=5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3
CARTESIA_API_KEY=sk_car_d69NmtdJKVbTj8XrrqM4Nt
LIVEKIT_URL=wss://your-server.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
```

### Portas do LiveKit

- `7880` - WebSocket/HTTP principal
- `7881` - WebRTC sobre TCP
- `50000-60000` - WebRTC sobre UDP

---

## Melhorias Futuras

Possíveis melhorias para o fluxograma e sistema:

1. **Multi-agente**: Suporte a handoff entre diferentes agentes especializados
2. **Interrupção**: Capacidade do usuário interromper o Pi durante resposta
3. **Contexto persistente**: Manter contexto entre múltiplas sessões
4. **Feedback visual**: Indicadores visuais de estado (gravando, processando, etc.)
5. **Detecção de emoção**: Análise de tom de voz para respostas mais naturais
6. **Multilíngue**: Detecção automática de idioma
7. **Preempção inteligente**: Previsão de respostas para reduzir latência

---

## Referências

- **LiveKit Agents**: https://github.com/livekit/agents
- **Deepgram Plugin**: https://docs.livekit.io/agents/integrations/stt/deepgram/
- **Cartesia Plugin**: https://docs.livekit.io/agents/integrations/tts/cartesia/
- **Mermaid Docs**: https://mermaid.js.org/

---

**Data de criação**: 2026-04-03
**Versão**: 1.0
**Autor**: Flowchart Agent - Pi Extension Playground
