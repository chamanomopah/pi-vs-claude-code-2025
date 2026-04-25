# SSH Node n8n no Windows - Exemplos Práticos

> **Coleção de Exemplos** - JSONs prontos para copiar e colar
> 
> **Última atualização**: Abril 2026

---

## 📋 ÍNDICE DE EXEMPLOS

1. [Testes Básicos](#1-testes-básicos)
2. [Gerenciamento de Arquivos](#2-gerenciamento-de-arquivos)
3. [Monitoramento de Sistema](#3-monitoramento-de-sistema)
4. [Execução de Scripts](#4-execução-de-scripts)
5. [Backup e Restore](#5-backup-e-restore)
6. [Gerenciamento de Processos](#6-gerenciamento-de-processos)
7. [Gerenciamento de Serviços](#7-gerenciamento-de-serviços)
8. [Rede e Conectividade](#8-rede-e-conectividade)
9. [Logs e Eventos](#9-logs-e-eventos)
10. [Workflows Completos](#10-workflows-completos)

---

## 1. TESTES BÁSICOS

### Exemplo 1.1: Teste de Conexão Simples

```json
{
  "operation": "executeCommand",
  "credential": {
    "host": "192.168.1.100",
    "port": 22,
    "username": "administrator",
    "password": "YourPassword123!"
  },
  "workingDirectory": ".",
  "command": "hostname"
}
```

**Saída esperada:** `WINSRV01`

### Exemplo 1.2: Verificar Usuário

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "whoami"
}
```

**Saída esperada:** `server\administrator`

### Exemplo 1.3: Verificar Versão do Windows

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "ver"
}
```

**Saída esperada:** `Microsoft Windows [Version 10.0.20348.x]`

### Exemplo 1.4: Listar Diretório Atual

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "dir"
}
```

---

## 2. GERENCIAMENTO DE ARQUIVOS

### Exemplo 2.1: Criar Diretório

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\Users\Public",
  "command": "mkdir TestFolder"
}
```

### Exemplo 2.2: Criar Arquivo de Texto

```json
{
  "operation": "executeCommand",
  "workingDirectory": "%TEMP%",
  "command": "echo Teste de conexao > test.txt"
}
```

### Exemplo 2.3: Ler Conteúdo de Arquivo

```json
{
  "operation": "executeCommand",
  "workingDirectory": "%TEMP%",
  "command": "type test.txt"
}
```

### Exemplo 2.4: Copiar Arquivo

```json
{
  "operation": "executeCommand",
  "workingDirectory": "%TEMP%",
  "command": "copy test.txt test_backup.txt"
}
```

### Exemplo 2.5: Mover Arquivo

```json
{
  "operation": "executeCommand",
  "workingDirectory": "%TEMP%",
  "command": "move test.txt C:\Users\Public\test.txt"
}
```

### Exemplo 2.6: Deletar Arquivo

```json
{
  "operation": "executeCommand",
  "workingDirectory": "%TEMP%",
  "command": "del test.txt"
}
```

### Exemplo 2.7: Listar com Filtro

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\Windows",
  "command": "dir *.exe"
}
```

### Exemplo 2.8: Buscar Arquivo por Nome

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\\",
  "command": "dir /s /b notepad.exe"
}
```

---

## 3. MONITORAMENTO DE SISTEMA

### Exemplo 3.1: Informações Completas do Sistema

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "systeminfo"
}
```

### Exemplo 3.2: Uso de CPU

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "wmic cpu get loadpercentage /value"
}
```

### Exemplo 3.3: Memória Disponível

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value"
}
```

### Exemplo 3.4: Espaço em Disco

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "wmic logicaldisk get deviceid,size,freespace"
}
```

### Exemplo 3.5: Eventos de Sistema Recentes

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "wevtutil qe System /c:10 /rd:true /f:text"
}
```

### Exemplo 3.6: Temperatura do Sistema (se disponível)

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "powershell.exe -Command \"Get-WmiObject MSAcpi_ThermalZoneTemperature | Select-Object InstanceName, CriticalTripPoint, CurrentTemperature\""
}
```

---

## 4. EXECUÇÃO DE SCRIPTS

### Exemplo 4.1: Executar Script PowerShell Simples

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\Scripts",
  "command": "powershell.exe -ExecutionPolicy Bypass -File \"script.ps1\""
}
```

### Exemplo 4.2: Executar Script PowerShell com Parâmetros

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\Scripts",
  "command": "powershell.exe -ExecutionPolicy Bypass -File \"script.ps1\" -Parameter1 \"Value1\" -Parameter2 \"Value2\""
}
```

### Exemplo 4.3: Executar Script Batch

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\Scripts",
  "command": "cmd.exe /c \"script.bat\""
}
```

### Exemplo 4.4: Executar Comando PowerShell Direto

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "powershell.exe -Command \"Get-Process | Select-Object Name, CPU -First 10\""
}
```

### Exemplo 4.5: Executar Script em Segundo Plano

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\Scripts",
  "command": "start /b powershell.exe -ExecutionPolicy Bypass -File \"background.ps1\""
}
```

---

## 5. BACKUP E RESTORE

### Exemplo 5.1: Backup de Diretório Completo

```json
{
  "operation": "executeCommand",
  "workingDirectory": "D:\\",
  "command": "xcopy \"C:\Data\" \"D:\Backup\Data\" /E /I /H /Y /Z"
}
```

### Exemplo 5.2: Backup com Data no Nome

```json
{
  "operation": "executeCommand",
  "workingDirectory": "D:\\",
  "command": "xcopy \"C:\Data\" \"D:\Backup\Data_%date:~0,4%-%date:~5,2%-%date:~8,2%\" /E /I /H /Y"
}
```

### Exemplo 5.3: Backup Somente de Arquivos Modificados

```json
{
  "operation": "executeCommand",
  "workingDirectory": "D:\\",
  "command": "xcopy \"C:\Data\" \"D:\Backup\Data\" /E /I /H /Y /D /M"
}
```

### Exemplo 5.4: Compactar Diretório (ZIP)

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\\",
  "command": "powershell.exe -Command \"Compress-Archive -Path 'C:\Data\*' -DestinationPath 'C:\Backup\data.zip' -Force\""
}
```

### Exemplo 5.5: Descompactar Arquivo ZIP

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\\",
  "command": "powershell.exe -Command \"Expand-Archive -Path 'C:\Backup\data.zip' -DestinationPath 'C:\Restore' -Force\""
}
```

### Exemplo 5.6: Backup de Banco de Dados (MySQL)

```json
{
  "operation": "executeCommand",
  "workingDirectory": "C:\Backups",
  "command": "\"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe\" -u root -pPassword mydb > backup_%date:~0,4%-%date:~5,2%-%date:~8,2%.sql"
}
```

---

## 6. GERENCIAMENTO DE PROCESSOS

### Exemplo 6.1: Listar Todos os Processos

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "tasklist"
}
```

### Exemplo 6.2: Listar Processos com Detalhes

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "tasklist /V"
}
```

### Exemplo 6.3: Buscar Processo Específico

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "tasklist /FI \"IMAGENAME eq notepad.exe\""
}
```

### Exemplo 6.4: Matar Processo por Nome

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "taskkill /IM notepad.exe /F"
}
```

### Exemplo 6.5: Matar Processo por PID

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "taskkill /PID 1234 /F"
}
```

### Exemplo 6.6: Verificar se Processo Está Rodando

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "tasklist /FI \"IMAGENAME eq notepad.exe\" | find /C \"notepad.exe\""
}
```

### Exemplo 6.7: Reiniciar Aplicação

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "taskkill /IM MyApp.exe /F && start \"\" \"C:\Program Files\MyApp\MyApp.exe\""
}
```

---

## 7. GERENCIAMENTO DE SERVIÇOS

### Exemplo 7.1: Listar Todos os Serviços

```json
{
  "operation": "executeCommand",
  "workingDirectory": ".",
  "command": "sc query type= service state= all"
}
```

### Exemplo 7.2: Verificar Status de Serviço Específico

```js
