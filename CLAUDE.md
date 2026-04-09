# Pi vs CC — Extension Playground

Pi Coding Agent extension examples and experiments.

## Tooling
- **Package manager**: `bun` (not npm/yarn/pnpm)
- **Task runner**: `just` (see justfile)
- **Extensions run via**: `pi -e extensions/<name>.ts`

## Project Structure
- `extensions/` — Pi extension source files (.ts)
- `specs/` — Feature specifications
- `.pi/agents/` — Agent definitions for agent-team extension
- `.pi/agent-sessions/` — Ephemeral session files (gitignored)
- `agent teams` (.pi/agents/teams.yaml) + (extensions/agent-team.ts)

## Conventions
- Extensions are standalone .ts files loaded by Pi's jiti runtime
- Available imports: `@mariozechner/pi-coding-agent`, `@mariozechner/pi-tui`, `@mariozechner/pi-ai`, `@sinclair/typebox`, plus any deps in package.json
- Register tools at the top level of the extension function (not inside event handlers)
- Use `isToolCallEventType()` for type-safe tool_call event narrowing

## video production 

- `video-production/` - todos os projetos de produção de criação de videos pra canal dark pro youtube.
- `video-production/<numero-titulo>` - canais atuais em desenvolvimento que começam com numeral ex: `video-production/1-psicologia`. com arquivos gerais, meta-prompts, etc pro canal no geral.  
- `video-production/<numero-titulo>/<videos>/<numero-titulo_video>/` - desenvolvimento individual de cada video, podendo ter arquivos de roteiros, pasta com imagens, pasta com image_prompts de cada uma das cenas, pasta com os audios de cada cena, video final renderizado.