# Lançadores dos agentes do cérebro do Portal Abono para o Copilot CLI.
# Carregado pelo perfil do PowerShell (o install.ps1 oferece adicionar a linha).
#
# Cada lançador:
#   1. atualiza o clone do cérebro com fast-forward (nunca descarta nada local);
#   2. libera a pasta docs/ do cérebro na sessão (--add-dir);
#   3. aplica as permissões do agente (--allow-tool / --deny-tool).
#
# Limites conhecidos: as regras de negação casam pelo início do comando. Formas como
# `git -C <pasta> push` podem não ser reconhecidas pela regra `shell(git push)`; por isso o
# próprio agente também proíbe essas operações. Restrição de pastas não é barreira de segurança.

function Get-PaBrainHome {
    if ($env:PA_BRAIN_HOME) { return $env:PA_BRAIN_HOME }
    return (Join-Path $HOME ".pa-brain")
}

function Update-PaBrain {
    $brain = Get-PaBrainHome
    if (-not (Test-Path (Join-Path $brain ".git"))) {
        Write-Warning "Cérebro não encontrado em '$brain'. Rode scripts/install/install.ps1."
        return
    }
    $out = git -C $brain pull --ff-only --quiet 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Não foi possível atualizar o cérebro (sem rede, alterações locais ou branch divergente). Seguindo com a cópia local."
        Write-Verbose ($out | Out-String)
    }
    $head = git -C $brain log -1 --format="%h %cs" 2>$null
    if ($head) { Write-Host "Cérebro: $head" -ForegroundColor DarkGray }
}

# Comandos que nenhum agente do cérebro pode executar.
$script:PaBrainDenyCommon = @(
    'shell(git push)', 'shell(git commit)', 'shell(git reset)', 'shell(git checkout)',
    'shell(git switch)', 'shell(git restore)', 'shell(git stash)', 'shell(git clean)',
    'shell(git merge)', 'shell(git rebase)', 'shell(git cherry-pick)', 'shell(git am)',
    'shell(git apply)', 'shell(git rm)', 'shell(git mv)',
    'shell(curl)', 'shell(wget)', 'shell(Invoke-WebRequest)', 'shell(Invoke-RestMethod)',
    'shell(iwr)', 'shell(irm)', 'shell(Remove-Item)', 'shell(rm)', 'shell(del)'
)

function ConvertTo-PaToolArgs([string]$Flag, [string[]]$Rules) {
    $result = @()
    foreach ($r in $Rules) { $result += "--$Flag=$r" }
    return $result
}

function labaidessa-abono {
    Update-PaBrain
    $docs = Join-Path (Get-PaBrainHome) "docs"
    # Leitura e Git de leitura sem confirmação; build e testes pedem aprovação a cada comando.
    $allow = ConvertTo-PaToolArgs "allow-tool" @('read', 'shell(git:*)', 'shell(rg:*)')
    $deny  = ConvertTo-PaToolArgs "deny-tool"  ($script:PaBrainDenyCommon + @('write'))
    copilot --agent labAIdessa-abono --add-dir $docs @allow @deny @args
}

function carmouqa-abono {
    # PENDENTE: ajustar permissões quando a definição do carmouQA-abono estiver pronta.
    Update-PaBrain
    $docs = Join-Path (Get-PaBrainHome) "docs"
    $allow = ConvertTo-PaToolArgs "allow-tool" @('read', 'shell(git:*)')
    $deny  = ConvertTo-PaToolArgs "deny-tool"  ($script:PaBrainDenyCommon + @('write'))
    copilot --agent carmouQA-abono --add-dir $docs @allow @deny @args
}
