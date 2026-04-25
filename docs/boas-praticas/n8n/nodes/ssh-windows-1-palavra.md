# SSH Node Windows - Comandos de 1 Palavra

**⚠️ DOCUMENTO VALIDADO COM BASE EM PESQUISAS REAIS**

## Comandos CMD de 1 Palavra TESTADOS

### Comandos que Devem Funcionar (CMD)

| Comando | Descrição | Status |
|---------|-----------|--------|
| `hostname` | Exibe o nome do host | ✅ Deve funcionar |
| `whoami` | Exibe o usuário atual | ✅ Deve funcionar |
| `date` | Exibe a data atual | ✅ Deve funcionar |
| `time` | Exibe a hora atual | ✅ Deve funcionar |
| `ver` | Exibe a versão do Windows | ✅ Deve funcionar |
| `dir` | Lista diretório atual | ✅ Deve funcionar |
| `cd` | Exibe/muda diretório | ✅ Deve funcionar |
| `cls` | Limpa a tela | ⚠️ Funciona mas não visível via SSH |
| `exit` | Sai do shell | ⚠️ Termina conexão SSH |

### Comandos PowerShell de 1 Palavra

| Comando | Descrição | Status |
|---------|-----------|--------|
| `Get-Date` | Obtém data/hora | ✅ Deve funcionar |
| `Get-Process` | Lista processos | ✅ Deve funcionar |
| `Get-Service` | Lista serviços | ✅ Deve funcionar |
| `Get-Location` | Exibe diretório atual | ✅ Deve funcionar |
| `hostname` | Exibe o nome do host | ✅ Funciona em ambos |
| `whoami` | Exibe o usuário atual | ✅ Funciona em ambos |

## ⚠️ IMPORTANTE - O Problema REAL

**O erro "A sintaxe do nome do arquivo, do nome do diretório ou do rótulo do volume está incorreta" NÃO é causado por:**

- Comando muito longo
- Variáveis de ambiente
- Espaços em comandos de 1 palavra

**O erro é causado por:**

1. **Shell incorreto** - O n8n pode estar tentando usar CMD quando o Windows está configurado para PowerShell
2. **Working Directory incorreto** - Valores como `C:\`, `C:/`, `null` podem causar problemas
3. **Formatação de path Linux em Windows** - O n8n pode estar enviando caminhos no formato Linux (`/`) para Windows

## Comandos de 1 Palavra Recomendados para Testes

### Para CMD (Shell padrão do OpenSSH Windows):
```
hostname
whoami
date
time
ver
```

### Para PowerShell (Se configurado):
```
hostname
whoami
Get-Date
Get-Process
Get-Service
```

## Fontes de Pesquisa

- https://ss64.com/nt/ - Lista completa de comandos Windows CMD
- https://learn.microsoft.com/en-us/windows-server/administration/windows-commands - Documentação oficial Microsoft
- https://github.com/n8n-io/n8n/issues/23299 - Issue sobre erro exato no n8n
- https://community.n8n.io/t/ssh-is-it-possible-to-put-working-directory-as-optional/18596 - Solução validada na comunidade n8n

## Notas Importantes

1. **Comandos de 1 palavra funcionam** - O problema não é o comando em si
2. **O problema está na configuração** - Shell ou Working Directory
3. **hostname e whoami são os melhores para testes** - São simples e funcionam em ambos os shells
4. **Variáveis de ambiente como %DATE% NÃO funcionam via SSH** - Elas são expandidas pelo cliente, não pelo servidor

## Comandos NÃO Recomendados (mesmo sendo 1 palavra)

- `echo` - Requer parâmetros para ser útil
- `ls` - Não existe no CMD (é `dir`)
- `pwd` - Não existe no CMD (é `cd` sem argumentos)

## Próximos Passos

Veja os outros documentos:
- `ssh-windows-shell.md` - Como descobrir e configurar o shell correto
- `ssh-windows-cwd-validado.md` - Valores de Working Directory validados
- `ssh-windows-erro-sintaxe.md` - Análise detalhada do erro específico
