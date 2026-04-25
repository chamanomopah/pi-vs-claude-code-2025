# Guia Completo do SSH Node do n8n - Foco Windows

**Data da Pesquisa:** 25 de Abril de 2026  
**Versão n8n:** 1.x+  
**Foco:** Ambiente Windows e Boas Práticas

---

## Índice

1. [O que é o SSH Node do n8n](#1-o-que-é-o-ssh-node-do-n8n)
2. [Configuração no Windows](#2-configuração-no-windows)
3. [Boas Práticas de Segurança](#3-boas-práticas-de-segurança)
4. [Comandos Úteis e Simples](#4-comandos-úteis-e-simples)
5. [Troubleshooting - Erros Comuns](#5-troubleshooting---erros-comuns)
6. [Exemplos de Workflows](#6-exemplos-de-workflows)
7. [Referências e Fontes](#7-referências-e-fontes)

---

## 1. O que é o SSH Node do n8n

### Definição

O **SSH node** do n8n é um nó core que permite executar comandos remotos usando o protocolo Secure Shell (SSH). Ele é útil para automação de servidores, manutenção de sistemas e execução de tarefas remotas.

### Operações Suportadas

O SSH node suporta **três operações principais**:

1. **Execute Command** - Executa comandos em um servidor remoto
2. **Download File** - Baixa arquivos de um servidor remoto
3. **Upload File** - Envia arquivos para um servidor remoto

### Casos de Uso Principais

- ✅ Manutenção e limpeza de servidores
- ✅ Reinício de serviços e verificações de espaço em disco
- ✅ Sistemas de health check que executam comandos diagnósticos
- ✅ Deploy automatizado em servidores
- ✅ Backup de configurações de servidores
- ✅ Monitoramento de recursos de VPS
- ✅ Automação de atualizações de sistema
- ✅ Gerenciamento de containers Docker
- ✅ Execução de scripts PowerShell em Windows

---

## 2. Configuração no Windows

### 2.1 Pré-requisitos

#### Para Servidor Windows (Alvo)

1. **OpenSSH Server instalado**
   ```powershell
   # Verificar se está instalado
   Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
   
   # Instalar se necessário
   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
   ```

2. **Configurar o serviço SSH**
   ```powershell
   # Iniciar o serviço
   Start-Service sshd
   
   # Configurar para início automático
   Set-Service -Name sshd -StartupType 'Automatic'
   
   # Confirmar firewall (porta 22)
   Get-NetFirewallRule -Name *ssh*
   ```

3. **Configurar PowerShell como shell padrão (RECOMENDADO)**
   ```powershell
   Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" `
     -Name DefaultShell `
     -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
   
   Restart-Service sshd
   ```

#### Para n8n (Cliente)

- n8n instalado (local, Docker ou cloud)
- Acesso de rede ao servidor Windows
- Credenciais SSH válidas

### 2.2 Configurar Credenciais SSH

#### Método 1: Autenticação por Senha

1. No n8n, vá em **Credentials** > **New Credential**
2. Selecione **SSH** (Password)
3. Configure:
   - **Host**: Endereço IP ou hostname do servidor Windows
   - **Port**: 22 (padrão)
   - **Username**: Usuário Windows (ex: `administrator`)
   - **Password**: Senha do usuário

#### Método 2: Autenticação por Chave Privata (RECOMENDADO)

1. No n8n, vá em **Credentials** > **New Credential**
2. Selecione **SSH** (Private Key)
3. Configure:
   - **Host**: Endereço IP ou hostname
   - **Port**: 22
   - **Username**: Usuário Windows
   - **Private Key**: Cole a chave privada completa
   - **Passphrase**: (opcional) Se a chave tiver passphrase

**⚠️ IMPORTANTE:** Cole a chave privada completa, incluindo as linhas `-----BEGIN` e `-----END`:

```
-----BEGIN OPENSSH PRIVATE KEY-----
... conteúdo da chave ...
-----END OPENSSH PRIVATE KEY-----
```

### 2.3 Configurar o SSH Node

#### Operação: Execute Command

**Campos:**
- **Credential to connect with**: Selecione a credencial SSH criada
- **Command**: Comando a executar (veja seção 4 para exemplos)
- **Working Directory**: 
  - ⚠️ **Windows**: Use `null` (valor nulo, não string) se der erro
  - ⚠️ **Windows**: Ou deixe em branco usando expressão: `{{null}}`
  - ✅ **Linux**: Caminho normal como `/home/user`

#### Operação: Download File

**Campos:**
- **Credential to connect with**: Credencial SSH
- **Path**: Caminho completo do arquivo no servidor remoto
- **File Property**: Nome da propriedade que receberá os dados binários
- **File Name** (opcional): Nome diferente para o arquivo baixado

#### Operação: Upload File

**Campos:**
- **Credential to connect with**: Credencial SSH
- **Input Binary Field**: Campo binário com o arquivo para upload
- **Target Directory**: Diretório de destino no servidor remoto
- **File Name** (opcional): Nome diferente do arquivo

---

## 3. Boas Práticas de Segurança

### 3.1 Proteção de Credenciais

#### Chave de Criptografia n8n

**CRUCIAL:** Configure uma chave de criptografia persistente:

```bash
# Gerar chave segura
openssl rand -hex 32

# Adicionar ao .env ou docker-compose.yml
N8N_ENCRYPTION_KEY=sua_chave_hex_64_caracteres
```

**⚠️ AVISO:** Se perder esta chave, TODAS as credenciais armazenadas ficarão inacessíveis permanentemente.

#### Autenticação por Chave vs Senha

| Método | Segurança | Conveniência | Recomendação |
|--------|-----------|--------------|---------------|
| Chave Privata + Passphrase | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ **Produção** |
| Chave Privata sem Passphrase | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ **Boa opção** |
| Senha | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ **Apenas testes** |

#### Gestão de Chaves SSH

```powershell
# No servidor Windows - Gerar novo par de chaves
ssh-keygen -t ed25519 -C "n8n-automation"

# Copiar chave pública para authorized_keys
type $env:USERPROFILE\.ssh\id_ed25519.pub >> $env:USERPROFILE\.ssh\authorized_keys

# Definir permissões corretas
icacls $env:USERPROFILE\.ssh\authorized_keys /inheritance:r
icacls $env:USERPROFILE\.ssh\authorized_keys /grant:r "$($env:USERNAME):F"
```

### 3.2 Hardening do n8n

#### Variáveis de Ambiente de Segurança

```bash
# Desabilitar nós perigosos (se não necessário)
N8N_NODES_DENYLIST=executeCommand

# Bloquear acesso a variáveis de ambiente
N8N_BLOCK_ENV_ACCESS_IN_NODE=true

# Bloquear acesso a arquivos do n8n
N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=true
```

#### Isolamento de Workflow

- Use sub-workflows para operações sensíveis
- Implemente error handling local
- Valide dados antes de executar comandos SSH

### 3.3 Princípio do Menor Privilégio

#### Para Credenciais SSH

- ✅ Criar usuário dedicado para automação n8n
- ✅ Atribuir apenas permissões necessárias
- ✅ Usar autenticação por chave em produção
- ✅ Rotacionar chaves periodicamente

```powershell
# Criar usuário para automação
New-LocalUser -Name "n8n-automation" -Password (ConvertTo-SecureString "StrongPassword!" -AsPlainText -Force)

# Adicionar a grupos necessários (evite Administrador se possível)
Add-LocalGroupMember -Group "Remote Management Users" -Member "n8n-automation"
```

### 3.4 Monitoramento e Auditoria

- Ativar logs detalhados do OpenSSH
- Revisar execuções de workflow regularmente
- Alertas para falhas de autenticação
- Backup de credenciais armazenadas em cofre seguro

---

## 4. Comandos Úteis e Simples

### 4.1 Comandos Windows (PowerShell/cmd)

#### Informações do Sistema

```powershell
# Nome do host
hostname

# Informações do sistema
systeminfo | Select-String "OS Name","OS Version"

# Espaço em disco
Get-PSDrive C | Select-Object Used,Free,@{Name="UsedGB";Expression={[math]::Round($_.Used/1GB,2)}}

# Uso de CPU
Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object Average

# Memória disponível
Get-WmiObject Win32_OperatingSystem | Select-Object FreePhysicalMemory
```

#### Gerenciamento de Serviços

```powershell
# Listar serviços rodando
Get-Service | Where-Object {$_.Status -eq 'Running'}

# Verificar serviço específico
Get-Service -Name "wuauserv" | Select-Object Name,Status,StartType

# Reiniciar um serviço
Restart-Service -Name "seu-servico" -Force

# Parar serviço
Stop-Service -Name "seu-servico" -Force
```

#### Gerenciamento de Processos

```powershell
# Listar processos
Get-Process

# Matar processo por nome
Stop-Process -Name "notepad" -Force

# Matar processo por PID
Stop-Process -Id 1234 -Force
```

#### Arquivos e Diretórios

`
