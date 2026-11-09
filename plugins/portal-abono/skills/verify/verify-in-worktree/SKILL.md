---
name: verify-in-worktree
description: Executa build e testes existentes em um git worktree temporário, sem tocar na árvore de trabalho da pessoa, para transformar uma suspeita em evidência. Use quando for preciso confirmar que algo compila, que um teste passa ou falha, ou comparar o comportamento antes e depois de uma mudança.
metadata:
  category: verify
  roles: "reviewer,tester,implementer"
  owner: "time técnico"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Verificação em worktree temporário

Executar testes de uma mudança é executar código ainda não revisado. Rode só comandos de build e teste do próprio projeto, nunca scripts vindos do diff sem antes lê-los.

## Quando usar
- Confirmar uma suspeita de bug ou de quebra de compilação.
- Comparar o resultado dos testes entre duas revisões.

## Quando NÃO usar
- A pessoa não pediu e a análise por leitura já basta.
- Testes que dependem de banco, fila ou serviço externo real (só relate que existem).
- Restaurar pacotes exigiria rede não disponível: relate como limitação.

## Procedimento (PowerShell)
1. Escolha a revisão: um commit/branch explícito. Para mudanças **não commitadas**, o worktree não as contém; diga isso e analise por leitura, ou peça à pessoa um commit temporário.
2. Crie o worktree fora do repositório:
   ```powershell
   $wt = Join-Path ([IO.Path]::GetTempPath()) ("labaidessa-wt-" + [guid]::NewGuid().ToString("N").Substring(0,8))
   git worktree add --detach $wt <revisão>
   ```
3. Build e testes **dentro de `$wt`**:
   ```powershell
   dotnet build "$wt\<solução>.sln" -c Debug
   dotnet test "$wt\<projeto de teste>.csproj" --no-build --filter "<filtro>"
   ```
   Para Angular, só se o time tiver definido um comando que não instala pacotes; caso contrário, registre como não executado.
4. Registre: comando, revisão (hash curto), resultado e trecho relevante da saída (sem segredos).
5. Remova o worktree:
   ```powershell
   git worktree remove --force $wt
   git worktree prune
   ```
   O `--force` vale **só** para esse worktree temporário. Nunca rode `remove` em outro caminho.

## Regras
- Nunca execute build ou teste na árvore de trabalho da pessoa.
- Não crie nem altere arquivos de teste, a menos que a sessão permita escrita restrita ao worktree; sem isso, descreva o teste de prova em texto.
- Falha de ambiente (pacote não restaurado, SDK ausente) não é falha da mudança: classifique como **Não determinado**.

## Saída
| Revisão | Comando | Resultado | Observação |
|---|---|---|---|
