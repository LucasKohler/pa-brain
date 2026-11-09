# Migração para o cérebro

Como aplicar este pacote ao repositório atual (`BR_IT_ONBOARDING_PORTAL_ABONO_DOCS`), que já tem a pasta `docs/`.

## 1. Aplicar a estrutura

1. Crie uma branch no repositório atual.
2. Copie o conteúdo deste pacote para a raiz do repositório. O pacote **não** traz `docs/`: a sua pasta atual fica intacta.
3. `AGENTS.md`: o pacote traz um novo `AGENTS.md` de raiz (mapa do cérebro + regras de edição). Antes de substituir o atual:
   - compare com o `AGENTS.md` existente;
   - o que for regra de **consumo da base** (ordem de leitura, canais, um salto em `related_docs`) deve estar em `docs/.index/README.md`. Se esse arquivo é gerado pelo `build-index`, ajuste o gerador; se é manual, edite-o;
   - mantenha no novo `AGENTS.md` qualquer regra de edição que já valia.

## 2. Remover o pipeline

```powershell
git rm azure-pipelines-docs.yml          # e qualquer outro azure-pipelines*.yml do cérebro
```

Depois:
- remova menções ao pipeline em `docs/_meta/scripts.md`, `docs/_meta/owners.md` e no README;
- se a política de branch tinha **Build Validation** apontando para esse pipeline, remova-a no Azure DevOps, senão os PRs ficam bloqueados;
- a validação passa a ser local, antes de cada PR (comandos no `AGENTS.md`). Revisores obrigatórios por caminho continuam valendo.

## 3. Validar

```powershell
python scripts/skills/validate_skills.py
python scripts/skills/build_catalog.py --check
# + os validadores de docs em scripts/docs/
```

## 4. Instalar e testar numa máquina

```powershell
git clone <URL> "$HOME\.pa-brain"
& "$HOME\.pa-brain\scripts\install\install.ps1"
copilot plugin list                      # deve listar portal-abono
labaidessa-abono                         # deve abrir com o agente labAIdessa-abono
```

Dentro da sessão, confira:
- `/agent` mostra `labAIdessa-abono`;
- `/list-dirs` mostra a pasta `docs` do cérebro;
- pedir uma revisão de C# carrega a skill `review-dotnet-lowlevel`;
- `git push` é negado.

## 5. Convivência com o labAIdessa atual

- O `labAIdessa` instalado hoje em `~/.copilot/agents` (vindo do AI_HARNESS) continua funcionando: o novo se chama `labAIdessa-abono`, então não há conflito de nome.
- Atenção: agentes e skills em `~/.copilot/` têm prioridade sobre os do plugin quando o **nome é igual**. Não crie cópias pessoais com os mesmos nomes do plugin.
- O `labAIdessa-abono` usa o MCP `labAIdessa-git`, que continua configurado pelo AI_HARNESS em `~/.copilot/mcp-config.json`.
- Quando o novo agente estiver validado, decida com o time se o `labAIdessa` genérico continua no repositório de arquitetura.

## 6. Pendências

- `carmouQA-abono`: trazer a definição atual do repositório de arquitetura e completar a camada do Portal Abono.
- Skills de `implement/` e `domain/`: escrever a partir dos padrões reais do código e das regras da base.
- Casos de avaliação em `evals/`: substituir os modelos por perguntas e PRs reais.
- O prompt de evolução anterior (com o MCP `labAIdessa-docs`) fica superado: a base agora é lida diretamente.
