# Cérebro do Portal Abono

Repositório único de conhecimento e capacidades de IA para **Portal Abono, IRIS e LESS**:

- **`docs/`**: base de conhecimento do sistema (produto, negócio, arquitetura, regras, fluxos), escrita para agentes e pessoas.
- **`plugins/portal-abono/`**: plugin do Copilot CLI com os agentes do time (`labAIdessa-abono`, `carmouQA-abono`) e as skills por categoria.
- **`.github/plugin/marketplace.json`**: transforma este repositório em um marketplace de plugins do Copilot CLI.

Tudo aqui funciona com o **GitHub Copilot CLI**.

## Estrutura

```
.
├── AGENTS.md                         # mapa do cérebro + regras para quem edita
├── docs/                             # base de conhecimento (índices em docs/.index/)
├── plugins/portal-abono/
│   ├── plugin.json                   # manifesto do plugin (agentes + pastas de skills)
│   ├── CATALOG.md                    # GERADO: catálogo de skills
│   ├── agents/                       # labAIdessa-abono, carmouQA-abono
│   └── skills/
│       ├── explore/                  # entender código, intenção e impacto
│       ├── review/                   # checklists de revisão
│       ├── implement/                # padrões de implementação do projeto
│       ├── verify/                   # verificação por execução (build, testes)
│       ├── document/                 # manter a base de conhecimento
│       ├── explain/                  # ensino e explicação
│       └── domain/                   # casos específicos do negócio
├── .github/
│   ├── plugin/marketplace.json
│   └── skills/                       # skills para MANTER este repositório
├── evals/                            # casos de avaliação por agente e por skill
├── templates/                        # modelos de skill e de agente
└── scripts/
    ├── docs/                         # build-index, validate-docs (já existentes)
    ├── skills/                       # validação e catálogo das skills
    └── install/                      # instalação e lançadores
```

## Instalação (uma vez por máquina)

Pré-requisitos: Git, Copilot CLI autenticado, Python 3 (para os validadores) e PowerShell.

```powershell
git clone <URL-do-repositório> "$HOME\.pa-brain"
& "$HOME\.pa-brain\scripts\install\install.ps1"
```

O instalador:
1. define a variável de usuário `PA_BRAIN_HOME`;
2. registra **este clone local** como marketplace (`copilot plugin marketplace add`);
3. instala o plugin `portal-abono`;
4. adiciona os lançadores ao seu perfil do PowerShell (com confirmação).

Como o marketplace é um caminho local, o plugin é carregado direto da pasta: depois de um `git pull`, as mudanças valem na próxima sessão (ou com `/restart`), sem `copilot plugin update`.

## Uso

```powershell
labaidessa-abono            # revisão e ensino (atualiza o cérebro antes de abrir)
carmouqa-abono              # agente de QA
Update-PaBrain              # só atualiza o clone
```

Dentro de qualquer sessão do Copilot CLI, as skills do plugin ficam disponíveis para todos os agentes e para o Copilot padrão. Os agentes também podem ser chamados com `/agent` ou `copilot --agent labAIdessa-abono`.

## Contribuir

- Skill nova: copie `templates/SKILL.template.md`, siga `AGENTS.md` e rode `python scripts/skills/validate_skills.py`.
- Documento novo: siga os templates de `docs/_meta/templates/` e rode os validadores de `scripts/docs/`.
- Toda mudança entra por PR. Antes de abrir o PR, rode os validadores localmente (veja `AGENTS.md`).

## Donos

| Caminho | Papel responsável |
|---|---|
| `docs/product/**`, `docs/rules/**` | Produto |
| `docs/architecture/**`, `docs/decisions/**` | Arquitetura |
| `plugins/portal-abono/agents/**` | Dono de cada agente |
| `plugins/portal-abono/skills/**` | Time técnico (dono indicado em cada skill) |
