# SSH Node n8n no Windows - Lista de Comandos

> **Referência Completa de Comandos** - Comandos testados e funcionais
> 
> **Última atualização**: Abril 2026

---

## 📋 ÍNDICE

1. [Comandos de Teste](#1-comandos-de-teste)
2. [Comandos de Arquivos](#2-comandos-de-arquivos)
3. [Comandos de Sistema](#3-comandos-de-sistema)
4. [Comandos de Processo](#4-comandos-de-processo)
5. [Comandos de Serviço](#5-comandos-de-serviço)
6. [Comandos de Rede](#6-comandos-de-rede)
7. [Comandos PowerShell](#7-comandos-powershell)

---

## 1. COMANDOS DE TESTE

### Comandos para Testar Conexão

| Comando | Descrição | Saída Exemplo |
|---------|-----------|---------------|
| `hostname` | Nome do computador | `WINSRV01` |
| `whoami` | Usuário atual | `server\administrator` |
| `ver` | Versão do Windows | `Microsoft Windows [Version 10.0.20348.x]` |
| `echo test` | Eco de texto | `test` |
| `date` | Data atual | `The current date is: Sat 04/25/2026` |
| `time` | Hora atual | `The current time is: 11:30:07.00` |

### Sequência de Testes Recomendada

```powershell
# Teste 1: Mais simples
hostname

# Teste 2: Informação de usuário
whoami

# Teste 3: Lista de diretório
dir

# Teste 4: Versão
ver

# Teste 5: Info completa
systeminfo
```

---

## 2. COMANDOS DE ARQUIVOS

### Navegação

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `cd` | Diretório atual | `cd` |
| `cd C:\Windows` | Mudar diretório | `cd C:\Windows` |
| `cd ..` | Voltar um nível | `cd ..` |
| `dir` | Listar arquivos | `dir` |
| `dir /s` | Listar recursivo | `dir /s` |
| `tree` | Ver estrutura | `tree C:\Data` |

### Criação e Remoção

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `mkdir nome` | Criar diretório | `mkdir TestFolder` |
| `rmdir nome` | Remover diretório vazio | `rmdir TestFolder` |
| `del arquivo.txt` | Deletar arquivo | `del test.txt` |
| `del /Q *.*` | Deletar todos (silencioso) | `del /Q *.*` |
| `rmdir /S nome` | Remover diretório com conteúdo | `rmdir /S TestFolder` |

### Cópia e Movimentação

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `copy orig dest` | Copiar arquivo | `copy file.txt file_backup.txt` |
| `move orig dest` | Mover/renomear | `move file.txt file_new.txt` |
| `xcopy orig dest` | Copiar diretório | `xcopy C:\Data D:\Backup /E /I` |
| `robocopy orig dest` | Copiar avançado | `robocopy C:\Data D:\Backup /E` |

### Leitura

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `type arquivo.txt` | Mostrar conteúdo | `type config.txt` |
| `more arquivo.txt` | Mostrar com paginação | `more log.txt` |
| `find "texto" arquivo.txt` | Buscar texto | `find "error" log.txt` |
| `findstr "texto" arquivo.txt` | Buscar avançada | `findstr /C:"error" log.txt` |

---

## 3. COMANDOS DE SISTEMA

### Informações do Sistema

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `systeminfo` | Informações completas | `systeminfo` |
| `ver` | Versão do Windows | `ver` |
| `wmic os get` | Info do SO | `wmic os get Caption,Version` |
| `wmic computersystem get` | Info do computador | `wmic computersystem get Name,Model` |
| `wmic cpu get` | Info do CPU | `wmic cpu get Name,MaxClockSpeed` |

### Variáveis de Ambiente

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `echo %USERPROFILE%` | Home do usuário | `C:\Users\joao` |
| `echo %TEMP%` | Temporários | `C:\Users\joao\AppData\Local\Temp` |
| `echo %APPDATA%` | Dados de app | `C:\Users\joao\AppData\Roaming` |
| `set` | Todas as variáveis | `set` |
| `set PATH` | Variável PATH | `set PATH` |

### Disco

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `vol` | Volume do disco | `vol C:` |
| `fsutil fsinfo drives` | Lista drives | `fsutil fsinfo drives` |
| `wmic logicaldisk get` | Info de discos | `wmic logicaldisk get deviceid,size,freespace` |

---

## 4. COMANDOS DE PROCESSO

### Listagem

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `tasklist` | Lista processos | `tasklist` |
| `tasklist /V` | Lista com detalhes | `tasklist /V` |
| `tasklist /FI "filtro"` | Lista filtrada | `tasklist /FI "IMAGENAME eq notepad.exe"` |
| `wmic process get` | Lista processos (WMI) | `wmic process get Name,ProcessId,PageFileUsage` |

### Controle

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `taskkill /IM nome.exe` | Matar por nome | `taskkill /IM notepad.exe /F` |
| `taskkill /PID 1234` | Matar por PID | `taskkill /PID 1234 /F` |
| `taskkill /F /IM nome.exe` | Forçar kill | `taskkill /F /IM chrome.exe` |
| `start nome.exe` | Iniciar programa | `start notepad.exe` |

### Filtros Úteis

```powershell
# Processos que consomem mais memória
tasklist /FO CSV | findstr /R "^[^,]*,[^,]*,[^,]*,[^,]*,[1-9][0-9][0-9][0-9][0-9]"

# Buscar processo específico
tasklist /FI "IMAGENAME eq notepad.exe"

# Processos de um usuário
tasklist /FI "USERNAME eq joao"

# Processos com PID específico
tasklist /FI "PID eq 1234"
```

---

## 5. COMANDOS DE SERVIÇO

### Listagem e Status

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `sc query` | Listar serviços rodando | `sc query type= service state= all` |
| `sc query nome` | Status de serviço | `sc query wuauserv` |
| `sc qc nome` | Configuração do serviço | `sc qc wuauserv` |
| `net start` | Listar serviços rodando | `net start` |

### Controle

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `sc start nome` | Iniciar serviço | `sc start MySQL80` |
| `sc stop nome` | Parar serviço | `sc stop wuauserv` |
| `sc pause nome` | Pausar serviço | `sc pause spooler` |
| `sc continue nome` | Continuar serviço | `sc continue spooler` |
| `net start nome` | Iniciar serviço (alt) | `net start MySQL80` |
| `net stop nome` | Parar serviço (alt) | `net stop wuauserv` |

### Configuração

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `sc config nome start=auto` | Automático | `sc config wuauserv start=auto` |
| `sc config nome start=demand` | Manual | `sc config wuauserv start=demand` |
| `sc config nome start=disabled` | Desabilitado | `sc config wuauserv start=disabled` |

---

## 6. COMANDOS DE REDE

### Configuração

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `ipconfig` | Configuração IP | `ipconfig` |
| `ipconfig /all` | Configuração completa | `ipconfig /all` |
| `ipconfig /release` | Liberar IP | `ipconfig /release` |
| `ipconfig /renew` | Renovar IP | `ipconfig /renew` |
| `ipconfig /flushdns` | Limpar cache DNS | `ipconfig /flushdns` |
| `ipconfig /displaydns` | Mostrar cache DNS | `ipconfig /displaydns` |

### Conectividade

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `ping host` | Testar conectividade | `ping 8.8.8.8` |
| `ping -n 4 host` | 4 pings | `ping -n 4 google.com` |
| `tracert host` | Rota até host | `tracert google.com` |
| `pathping host` | Rota com latência | `pathping google.com` |

### Portas e Conexões

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `netstat -an` | Todas conexões/portas | `netstat -an` |
| `netstat -an | find LISTENING` | Portas ouvindo | `netstat -an | find LISTENING` |
| `netstat -an | find ESTABLISHED` | Conexões estabelecidas | `netstat -an | find ESTABLISHED` |
| `netstat -r` | Tabela de rota | `netstat -r` |

### DNS

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `nslookup host` | Consultar DNS | `nslookup google.com` |
| `nslookup -type=MX dominio.com` | Registro MX | `nslookup -type=MX gmail.com` |

---

## 7. COMANDOS POWERSHELL

### Cmdlets Básicos

| Cmdlet | Alias CMD | Descrição |
|--------|-----------|-----------|
| `Get-ChildItem` | `dir` | Listar arquivos |
| `Set-Location` | `cd` | Mudar diretório |
| `Get-Process` | `tasklist` | Listar processos |
| `Stop-Process` | `taskkill` | Matar processo |
| `Get-Service` | `sc query` | Listar serviços |
| `Start-Service` | `sc start` | Iniciar serviço |
| `Stop-Service` | `sc stop` | Parar serviço |

### Executando PowerShell via SSH

```json
{
  "workingDirectory": ".",
  "command": "powershell.exe -Command \
