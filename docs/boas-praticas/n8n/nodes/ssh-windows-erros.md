# SSH Node n8n no Windows - Guia de Erros e Troubleshooting

> **Solução de Problemas** - Diagnóstico e correção de erros comuns
> 
> **Última atualização**: Abril 2026

---

## 📋 ÍNDICE DE ERROS

1. [Erros de Working Directory](#1-erros-de-working-directory)
2. [Erros de Conexão](#2-erros-de-conexão)
3. [Erros de Comando](#3-erros-de-comando)
4. [Erros de Permissão](#4-erros-de-permissão)
5. [Erros de Caminho](#5-erros-de-caminho)
6. [Erros de Codificação](#6-erros-de-codificação)
7. [Troubleshooting Avançado](#7-troubleshooting-avançado)

---

## 1. ERROS DE WORKING DIRECTORY

### Erro 1.1: "Working Directory is required"

**Sintoma:**
```
Working Directory is required
```

**Causa:** Campo deixado vazio sem ser expressão

**Solução:**
1. Clique no ícone `fx` ao lado do campo
2. Deixe o campo VAZIO
3. Ou use `.` como valor

**Exemplo correto:**
```json
{
  "workingDirectory": ".",
  "command": "hostname"
}
```

---

### Erro 1.2: "cannot read properties of null (reading 'startsWith')"

**Sintoma:**
```
Error: cannot read properties of null (reading 'startsWith')
```

**Causa:** Valor `null` (texto) digitado no campo

**Solução:**
- **NÃO** digite `null` como texto
- Use `.` ou `%USERPROFILE%`
- Ou use expressão vazia

**ERRADO:**
```json
{
  "workingDirectory": "null",
  "command": "hostname"
}
```

**CORRETO:**
```json
{
  "workingDirectory": ".",
  "command": "hostname"
}
```

---

### Erro 1.3: "The system cannot find the path specified"

**Sintoma:**
```
The system cannot find the path specified
```

**Causas possíveis:**
1. Caminho Linux (`/`) em servidor Windows
2. Diretório não existe
3. Working Directory vazio ou inválido

**Soluções:**

**Caso 1: Caminho Linux**
```json
{
  "workingDirectory": "/",  // ERRADO
  "command": "hostname"
}
```

**Correção:**
```json
{
  "workingDirectory": ".",  // CORRETO
  "command": "hostname"
}
```

**Caso 2: Diretório não existe**
```json
{
  "workingDirectory": "C:\NaoExiste",
  "command": "hostname"
}
```

**Correção:**
```json
{
  "workingDirectory": "C:\Users\Public",
  "command": "hostname"
}
```

---

### Erro 1.4: "The filename, directory name, or volume label syntax is incorrect"

**Sintoma:**
```
The filename, directory name, or volume label syntax is incorrect
```

**Causa:** Caminho com espaços sem aspas ou caracteres inválidos

**Solução:**
```json
{
  "workingDirectory": "C:\Program Files",  // ERRADO
  "command": "hostname"
}
```

**Correção:**
```json
{
  "workingDirectory": "C:\Program Files",  // CORRETO ( Working Directory aceita espaço)
  "command": "hostname"
}
```

**No comando:**
```json
{
  "workingDirectory": ".",
  "command": "dir C:\Program Files"  // ERRADO
}
```

**Correção:**
```json
{
  "workingDirectory": ".",
  "command": "dir \"C:\Program Files\""  // CORRETO
}
```

---

## 2. ERROS DE CONEXÃO

### Erro 2.1: "Connection refused"

**Sintoma:**
```
Error: Connection refused
```

**Causas possíveis:**
1. Serviço SSH não está rodando
2. Firewall bloqueando porta 22
3. IP ou porta incorretos

**Soluções:**

**Verificar serviço SSH:**
```powershell
# No servidor Windows
Get-Service sshd

# Se não estiver rodando:
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

**Verificar firewall:**
```powershell
# No servidor Windows
Get-NetFirewallRule -Name *ssh*

# Adicionar regra se necessário:
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

**Verificar conectividade:**
```powershell
# Do cliente n8n
ping 192.168.1.100
telnet 192.168.1.100 22
```

---

### Erro 2.2: "Authentication failed"

**Sintoma:**
```
Error: Authentication failed
```

**Causas possíveis:**
1. Usuário ou senha incorretos
2. Chave SSH incorreta
3. Autenticação por chave não configurada

**Soluções:**

**Verificar credenciais:**
```json
{
  "host": "192.168.1.100",
  "port": 22,
  "username": "administrator",
  "password": "senha_correta"  // Verifique!
}
```

**Testar manualmente:**
```powershell
ssh administrator@192.168.1.100
```

**Se usar chave privada:**
```powershell
# Verificar permissões da chave
# No servidor Windows, a chave pública deve estar em:
C:\ProgramData\ssh\administrators_authorized_keys  # Para admin
C:\Users\usuario\.ssh\authorized_keys              # Para usuário normal
```

---

### Erro 2.3: "Connection timeout"

**Sintoma:**
```
Error: Connection timeout
```

**Causas possíveis:**
1. Rede não alcança o servidor
2. Firewall bloqueando
3. Servidor desligado

**Soluções:**

**Testar conectividade:**
```powershell
ping 192.168.1.100
telnet 192.168.1.100 22
```

**Verificar rota:**
```powershell
tracert 192.168.1.100
```

**Verificar se servidor está online:**
```powershell
# No servidor Windows
ping -t 127.0.0.1
```

---

## 3. ERROS DE COMANDO

### Erro 3.1: "Command not found"

**Sintoma:**
```
'ls' is not recognized as an internal or external command
```

**Causa:** Comando Linux em servidor Windows

**Solução:**
```json
{
  "command": "ls -la"  // ERRADO
}
```

**Correção:**
```json
{
  "command": "dir"  // CORRETO
}
```

**Tabela de comandos Linux → Windows:**

| Linux | Windows | Funciona? |
|-------|---------|-----------|
| `ls` | `dir` | ✅ |
| `cat` | `type` | ✅ |
| `rm` | `del` | ✅ |
| `cp` | `copy` | ✅ |
| `mv` | `move` | ✅ |
| `pwd` | `cd` | ✅ |
| `mkdir` | `mkdir` | ✅ |
| `grep` | `findstr` | ⚠️ |

---

### Erro 3.2: "The term is not recognized as the name of a cmdlet"

**Sintoma:**
```
The term 'Get-Process' is not recognized as the name of a cmdlet
```

**Causa:** Comando PowerShell em shell CMD

**Solução:**
```json
{
  "command": "Get-Process"  // ERRADO no CMD
}
```

**Correção:**
```json
{
  "command": "powershell.exe -Command \"Get-Process\""  // CORRETO
}
```

---

### Erro 3.3: Comando executa mas não retorna saída

**Sintoma:** Execução bem-sucedida mas stdout vazio

**Causas possíveis:**
1. Comando não produz saída
2. Saída vai para stderr
3. Comando interativo

**Soluções:**

**Caso 1: Comando sem saída**
```json
{
  "command": "cd C:\Windows"  // Não produz saída
}
```

**Correção:**
```json
{
  "command": "cd C:\Windows && dir"  // Produz saída
}
```

**Caso 2: Saída em stderr**
```json
{
  "command": "comando_que_falha"
}
```

**Verifique stderr:**
```json
{
  "command": "comando_que_falha 2>&1"
}
```

---

## 4. ERROS DE PERMISSÃO

### Erro 4.1: "Access is denied"

**Sintoma:**
```
Access is denied
```

**Causa:** Usuário sem permissão suficiente

**Soluções:**

**Verificar permissões:**
```powershell
# No servidor Windows
whoami /priv
```

**Adicionar usuário ao grupo Administrators:**
```powershell
net localgroup Administrators sshuser /add
```

**Executar com privilégios elevados:**
```powershell
# Use runas (não recomendado para automação)
runas /user:Administrator "comando"
```

---

### Erro 4.2: "Permission denied" (chave SSH)

**Sintoma:**
```
Permission denied (publickey)
```

**Causa:** Chave SSH não configurada corretamente

**Soluções:**

**Verificar arquivo authorized_keys:**
```powershell
# Para admin:
type C:\ProgramData\ssh\administrators_authorized_keys

# Para usuário normal:
type C:\Users\usuario\.ssh\authorized_keys
```

**Corrigir permissões:**
```powershell
# Para admin:
icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F"

# Para usuário normal:
icacls "C:\Users\usuario\.ssh\authorized_keys" /inheritance:r /grant "usuario:F"
```

**Reiniciar serviço SSH:**
```powershell
Restart-Service sshd
```

---

## 5. ERROS DE CAMINHO

### Erro 5.1: Caminho com espaços

**Sintoma:** Comando falha silenciosamente ou retorna erro de sintaxe

**Causa:** Espaços sem aspas

**Solução:**
```json
{
  "command": "dir C:\Program Files"  // ERRADO
}
```

**Correção:**
```json
{
  "command": "dir \"C:\Program Files\""  // CORRETO
}
```

---

### Erro 5.2: Barras incorretas

**Sintoma:** Caminho não encontrado

**Causa:** Uso de `/` em vez de `\`

**Solução:**
```json
{
  "command": "dir C:/Windows/System32"  // Pode falhar
}
```

**Correção:**
```json
{
  "command": "dir C:\Windows\System32"  // CORRETO
}
