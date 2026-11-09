# Instala o cérebro do Portal Abono no Copilot CLI desta máquina.
# Não apaga nada, não altera repositórios e pede confirmação antes de mexer no perfil do PowerShell.
#
# Uso:
#   git clone <URL> "$HOME\.pa-brain"
#   & "$HOME\.pa-brain\scripts\install\install.ps1"

[CmdletBinding()]
param(
    [string]$BrainHome = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [switch]$SkipProfile
)

$ErrorActionPreference = "Stop"

function Assert-Command($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Comando '$name' não encontrado. Instale-o e rode de novo."
    }
}

Assert-Command git
Assert-Command copilot

if (-not (Test-Path (Join-Path $BrainHome ".github\plugin\marketplace.json"))) {
    throw "'$BrainHome' não parece ser o cérebro (falta .github\plugin\marketplace.json)."
}

# 1. Variável de ambiente do usuário
[Environment]::SetEnvironmentVariable("PA_BRAIN_HOME", $BrainHome, "User")
$env:PA_BRAIN_HOME = $BrainHome
Write-Host "PA_BRAIN_HOME = $BrainHome"

# 2. Marketplace local (o plugin passa a ser carregado direto desta pasta)
$marketplaces = copilot plugin marketplace list 2>&1 | Out-String
if ($marketplaces -match "pa-brain") {
    Write-Host "Marketplace 'pa-brain' já registrado."
} else {
    copilot plugin marketplace add $BrainHome
    if ($LASTEXITCODE -ne 0) { throw "Falha ao registrar o marketplace." }
}

# 3. Plugin
$plugins = copilot plugin list 2>&1 | Out-String
if ($plugins -match "portal-abono") {
    Write-Host "Plugin 'portal-abono' já instalado."
} else {
    copilot plugin install "portal-abono@pa-brain"
    if ($LASTEXITCODE -ne 0) { throw "Falha ao instalar o plugin." }
}

# 4. Lançadores no perfil do PowerShell (com confirmação)
$launchers = Join-Path $BrainHome "scripts\install\launchers.ps1"
$line = ". `"$launchers`""
if (-not $SkipProfile) {
    $profileText = if (Test-Path $PROFILE) { Get-Content $PROFILE -Raw } else { "" }
    if ($profileText -and $profileText.Contains($launchers)) {
        Write-Host "Lançadores já estão no perfil."
    } else {
        $answer = Read-Host "Adicionar os lançadores ao perfil '$PROFILE'? (s/N)"
        if ($answer -match '^[sSyY]') {
            New-Item -ItemType File -Force -Path $PROFILE | Out-Null
            Add-Content -Path $PROFILE -Value "`n# Cérebro do Portal Abono`n$line"
            Write-Host "Adicionado. Abra um novo terminal ou rode: $line"
        } else {
            Write-Host "Ignorado. Para usar nesta sessão: $line"
        }
    }
}

Write-Host "`nPronto. Teste com: copilot plugin list  e depois  labaidessa-abono"
