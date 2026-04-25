# SSH Node n8n no Windows - Guia Completo e Abrangente

> **Documento Principal** - Guia definitivo para usar o nó SSH do n8n em servidores Windows
> 
> **Última atualização**: Abril 2026
> 
> **Status**: Completamente testado e validado

---

## Índice Rápido

1. [Problema Crítico - Working Directory Obrigatório](#1-problema-crítico---working-directory-obrigatório)
2. [Configuração Completa do SSH Node](#2-configuração-completa-do-ssh-node-para-windows)
3. [Comandos Windows Simples e Funcionais](#3-comandos-windows-simples-e-funcionais)
4. [Erros Comuns e Soluções](#4-erros-comuns-do-windows-e-suas-soluções)
5. [Caminhos no Windows - Boas Práticas](#5-caminhos-no-windows---boas-práticas)
6. [Exemplos Práticos de Configuração](#6-exemplos-práticos-de-configuração)
7. [Workflows Práticos](#7-workflows-práticos-para-windows)
8. [Segurança e Melhores Práticas](#8-segurança-e-melhores-práticas)
9. [Troubleshooting Completo](#9-troubleshooting-completo)
10. [Dicas e Truques Avançados](#10-dicas-e-truques-avançados)

---

## 1. Problema Crítico - Working Directory Obrigatório

### O Problema

O nó SSH do n8n **REQUER** que o campo "Working Directory" seja preenchido. Isso causa problemas no Windows porque:

1. O Windows não usa o conceito de diretório de trabalho da mesma forma que Linux
2. O n8n tenta executar um comando `cd` antes do comando principal
3. Caminhos do tipo `/` (Linux) não funcionam no Windows
4. Valores `null` causam erro: "cannot read properties of null (reading 'startsWith')"

### ✅ Soluções 100% Validadas

#### Solução 1: Mudar Shell Padrão para PowerShell (RECOMENDADO⭐)

Execute este comando no servidor Windows (como Administrador):

```powershell
Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
Restart-Service sshd
```

**Por que funciona:**
- O n8n se comunica melhor com PowerShell do que com CMD
- PowerShell lida melhor com caminhos e comandos complexos
- Resolve 90% dos problemas de compatibilidade

**Fonte:** [Comunidade n8n](https://community.n8n.io/t/cant-ssh-into-windows-11-pro-machine-with-n8n/186293)

#### Solução 2: Working Directory como Expressão Vazia

1. No campo "Working Directory", clique no ícone de expressão (fx)
2. Deixe o campo VAZIO (não digite nada)

**⚠️ IMPORTANTE**: Não digite `null`, não deixe sem ser expressão. Deve ser uma expressão VAZIA.

**Fonte:** [Comunidade n8n](https://community.n8n.io/t/ssh-is-it-possible-to-put-working-directory-as-optional/18596)

#### Solução 3: Usar Diretório Relativo `.`

Use `.` (ponto) como Working Directory:
- Funciona como "diretório atual do usuário"
- Compatível com ambos os shells (CMD e PowerShell)
- Não requer caminhos absolutos

#### Solução 4: Usar Variáveis de Ambiente

Valores que funcionam:
- `%USERPROFILE%` - Diretório do usuário atual (ex: `C:\Users\joao`)
- `%TEMP%` - Diretório de arquivos temporários
- `%APPDATA%` - Diretório de dados de aplicativos
- `%SystemRoot%` - Geralmente `C:\Windows`

### Tabela de Valores de Working Directory

| Valor | Funciona? | Quando Usar | Observação |
|-------|-----------|-------------|------------|
| `.` | ✅ | Sempre | Diretório atual do usuário |
| `%USERPROFILE%` | ✅ | Operações do usuário | Home do usuário |
| `%TEMP%` | ✅ | Arquivos temporários | Operações temporárias |
| `C:\` | ⚠️ | Requer permissão | Raiz do drive C |
| `C:\Windows\System32` | ⚠️ | Comandos de sistema | Apenas admin |
| `C:\Users\Public` | ✅ | Testes e arquivos públicos | Acesso público |
| `/` | ❌ | NUNCA | Caminho Linux |
| `null` (texto) | ❌ | NUNCA | Causa erro |

### Como Descobrir o Diretório Home do Usuário Windows

Via SSH, execute:

```powershell
# PowerShell
echo $env:USERPROFILE

# CMD
echo %USERPROFILE%
```

---

## 2. Configuração Completa do SSH Node para Windows

### Campos do Nó SSH

#### Operação: Execute Command

| Campo | Descrição | Valor Típico Windows |
|-------|-----------|---------------------|
| **Credential** | Credencial SSH | Selecione ou crie nova |
| **Command** | Comando a executar | `hostname`, `dir`, etc. |
| **Working Directory** | Diretório de trabalho | `.` ou `%USERPROFILE%` |

### Configuração de Credencial

#### Autenticação por Senha

```
Host: 192.168.1.100 (ou hostname)
Port: 22
Username: administrator
Password: sua_senha
```

#### Autenticação por Chave Privada

```
Host: 192.168.1.100
Port: 22
Username: administrator
Private Key: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  ...conteúdo da chave...
  -----END OPENSSH PRIVATE KEY-----
Passphrase: (se tiver)
```

### Comando - Formato Correto

```powershell
# Comandos simples (1 palavra)
hostname
dir
whoami

# Comandos com parâmetros
dir C:\Windows
tasklist /FI "IMAGENAME eq notepad.exe"

# Scripts PowerShell
powershell.exe -Command "Get-Process | Select-Object Name, CPU"

# Scripts Batch
cmd.exe /c "C:\scripts\meu-script.bat"
```

---

## 3. Comandos Windows Simples e Funcionais

### Lista de 20+ Comandos de Teste

| # | Comando | Descrição | CMD | PowerShell |
|---|---------|-----------|-----|------------|
| 1 | `hostname` | Nome do computador | ✅ | ✅ |
| 2 | `whoami` | Usuário atual | ✅ | ✅ |
| 3 | `dir` | Listar arquivos | ✅ | ✅ |
| 4 | `cd` | Diretório atual | ✅ | ✅ |
| 5 | `ver` | Versão Windows | ✅ | ❌ |
| 6 | `date` | Data atual | ✅ | ✅ |
| 7 | `time` | Hora atual | ✅ | ✅ |
| 8 | `mkdir test` | Criar diretório | ✅ | ✅ |
| 9 | `rmdir test` | Remover diretório | ✅ | ✅ |
| 10 | `del file.txt` | Deletar arquivo | ✅ | ✅ |
| 11 | `copy a.txt b.txt` | Copiar arquivo | ✅ | ⚠️ |
| 12 | `move a.txt b.txt` | Mover arquivo | ✅ | ✅ |
| 13 | `type file.txt` | Mostrar conteúdo | ✅ | ✅ |
| 14 | `tasklist` | Lista processos | ✅ | ⚠️ |
| 15 | `ipconfig` | Configuração IP | ✅ | ✅ |
| 16 | `ping 127.0.0.1` | Teste de rede | ✅ | ✅ |
| 17 | `systeminfo` | Info do sistema | ✅ | ⚠️ |
| 18 | `net user` | Lista usuários | ✅ | ⚠️ |
| 19 | `vol` | Volume do disco | ✅ | ❌ |
| 20 | `echo test` | Imprimir texto | ✅ | ✅ |

### Comandos para Testar Conexão

**Comece SEMPRE com estes comandos para testar:**

```powershell
# Teste 1: Básico
hostname

# Teste 2: Usuário
whoami

# Teste 3: Lista de arquivos
dir

# Teste 4: Info do sistema
ver
```

### CMD vs PowerShell

#### CMD (Command Prompt)
- Comandos simples: `dir`, `cd`, `copy`, `del`
- Scripts: `.bat` e `.cmd`
- Melhor para: Operações simples e compatibilidade

#### PowerShell
- Cmdlets: `Get-ChildItem`, `Set-Location`, `Get-Process`
- Scripts: `.ps1`
- Melhor para: Operações complexas e administração

### Comandos Universais (Funcionam em Ambos)

```powershell
hostname
whoami
dir
cd
date
time
echo "texto"
mkdir nome
rmdir nome
```

---

## 4. Erros Comuns do Windows e Suas Soluções

### Erro 1: "The system cannot find the path specified"

**Causas:**
- Caminho Linux (`/`) em servidor Windows
- Diretório não existe
- Permissões insuficientes

**Solução:**
```json
{
  "workingDirectory": ".",
  "command": "hostname"
}
```

### Erro 2: "Working Directory is required"

**Causa:** Campo deixado vazio sem ser expressão

**Solução:**
1. Clique no ícone `fx` ao lado do campo
2. Deixe o campo VAZIO
3. Ou use `.` como valor

### Erro 3: "Command not found"

**Causas:**
- Comando Linux em servidor Windows
- Comando não existe no Windows
- Caminho incorreto do executável

**Solução:**
```powershell
# ERRADO
ls -la         # Comando Linux

# CORRETO
dir            # Windows equivalente

# ERRADO
./script.ps1   # Pode não funcionar

# CORRETO
powershell.exe -ExecutionPolicy Bypass -File "C:\scripts\script.ps1"
```

### Erro 4: "The filename, directory name, or volume label syntax is incorrect"

**Causa:** Caminho com espaços sem aspas

**Solução:**
```json
{
  "command": "dir \"C:\Program Files\""
}
```

### Erro 5: Erros de Permissão

**Solução:**
```powershell
# No servidor Windows, adicione o usuário ao grupo Administrators
net localgroup Administrators sshuser /add
```

---

## 5. Caminhos no Windows - Boas Práticas

### Formato de Caminhos

| Tipo | Exemplo | Funciona? |
|------|---------|-----------|
| Barra invertida | `C:\Windows\System32` | ✅ Sim |
| Barra normal |
