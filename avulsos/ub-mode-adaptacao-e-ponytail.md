# Adaptação do ub-mode (Uncle Bob) e do Ponytail para o contexto do trabalho

Data: 09/11/2026
Contexto: stack **.NET + Angular**, IA liberada = **GitHub Copilot (CLI)**, repositório "cérebro" do **Portal Abono** (docs + skills usadas por labAIdessa-abono e carmouQA-abono).

> O ub-mode é usado como **referência de princípios**, não como cópia 1:1. O objetivo é trazer a ideia para o nosso contexto.

---

## 1. O que é o ub-mode

Skill de ~150 linhas (`SKILL.md`) de Robert C. Martin (unclebob), baseada nas regras do `poteto-mode`. Toda mudança segue três fases:

1. **First Make it Work** — Laziness Protocol, TDD, Redesign From First Principles, Attack the Premise, Subtract Before You Add, Build the Lever, Architecture (domínio, fronteiras, tipos, idempotência, estado compartilhado).
2. **Then Make it Right** — Fix Root Causes, unidades verificáveis, testar comportamento, e os quality gates **Crapper / Dryer / Mutator**, mais Refactoring.
3. **Practice** — Keep a Log, Guard the Context Window, Worktree Cleanup, Commit and Push.

Fontes: [README](https://github.com/unclebob/ub-mode/blob/master/README.md) e [SKILL.md](https://github.com/unclebob/ub-mode/blob/master/SKILL.md). Não vi licença listada no repositório; para uso interno não há impedimento prático, mas confirmar antes de redistribuir.

---

## 2. Adaptação do SKILL.md

### 2.1 Manter (independente de linguagem)

| Princípio | Por quê |
|---|---|
| TDD (teste falhando antes) | Base do fluxo de implementação |
| Testar comportamento, não implementação | Evita testes frágeis |
| Boundary Discipline / Type System Discipline | Encaixa em Clean Architecture e tipagem forte (C# e TypeScript) |
| Fix Root Causes | Vale para qualquer bug |
| Sequence work into verifiable units | Facilita revisão |
| Refactoring (fixar comportamento, mudar estrutura, provar) | Vale como está |
| Commits pequenos, com porquê/o quê/prova | Mantém histórico auditável |

### 2.2 Trocar

| Original | Adaptação |
|---|---|
| Crapper (CRAP < 10) | Coverlet/ReportGenerator no .NET; cobertura LCOV no Angular. Mesma fórmula: `CRAP = CC² × (1 − cobertura)³ + CC` |
| Dryer (duplicação ≥ 0,8) | Ver seção 3 (porte para Roslyn ou análise de duplicação existente) |
| Mutator | Stryker.NET (.NET) e Stryker (Angular/TS) |
| Keep a Log | Resumo curto no fim, não log de cada ação (evita verbosidade) |
| Worktree Cleanup | Só se o time usa worktrees; senão, remover |

### 2.3 Remover ou reescrever

- **"Push to the main line at the end"** — remover. Trocar por: *abrir Pull Request no Azure DevOps; nunca push direto na main*.
- **"Build the Lever"** e **"Redesign From First Principles"** — manter só para mudanças grandes e com aprovação humana; em tarefas pequenas conflitam com a "escada" do Ponytail.
- Referências ao Grok, tmux e Clojure — remover.

### 2.4 Empacotamento para o Copilot

O `SKILL.md` do Uncle Bob é instalado em `~/.claude/skills/`. No Copilot CLI o caminho mais seguro é **instruções do repositório**:

- `.github/copilot-instructions.md` e/ou `AGENTS.md` (o Copilot CLI lê os dois).
- Se a versão do Copilot usada na empresa suportar Agent Skills (`SKILL.md`), confirmar na documentação interna — **não verifiquei isso**.

---

## 3. Ferramentas

### 3.1 Ferramentas do Uncle Bob (verificadas nos READMEs)

| Ferramenta | Linguagens suportadas | .NET | Angular (TS) |
|---|---|---|---|
| [crapper](https://github.com/unclebob/crapper) | Clojure, Java, Go, TypeScript, Rust, Python | ❌ | ✅ |
| [dryer](https://github.com/unclebob/dryer) | idem | ❌ | ✅ |
| [mutator](https://github.com/unclebob/mutator) | idem | ❌ | ✅ |
| [uml-viewer](https://github.com/unclebob/uml-viewer) | scanners para Clojure, TS, Rust, Python | ❌ | ✅ |

Detalhes que importam:

- As três primeiras são **0BSD** (pode forkar e modificar).
- **Crapper/mutator para TS** usam LCOV: `npm run coverage`, Vitest ou `c8` sobre `npm test`. Se os projetos Angular usam **Karma/Jasmine**, é preciso um script `coverage` que gere LCOV (o reporter lcov do Karma serve). **Testar num projeto real primeiro.**
- O **mutator** exige o crapper em `../crapper` e usa `npm test` por padrão.
- O **dryer** usa limiar padrão 0,82 (o SKILL.md cita 0,8).
- O **uml-viewer** exige Clojure CLI + Java 21+ e usa um companion Grok em tmux (mailbox em arquivos). Não serve diretamente para o nosso contexto.

### 3.2 Equivalentes para .NET (do meu conhecimento, **não verificados nesta conversa**)

| Necessidade | Opção |
|---|---|
| Cobertura | Coverlet / `dotnet-coverage` |
| Relatório e complexidade | ReportGenerator |
| CRAP | Script pequeno aplicando a fórmula sobre o relatório do Coverlet |
| Mutação | Stryker.NET |
| Duplicação | SonarQube/SonarCloud, ou **porte do Dryer** para Roslyn (a ideia é simples: fingerprint estrutural por método + similaridade de Jaccard) |

Antes de instalar qualquer ferramenta de terceiros na pipeline, alinhar com o time de segurança (setor financeiro).

### 3.3 Viewer novo (referência, não 1:1)

O uml-viewer tem uma fronteira limpa: só **lê arquivos**. Isso permite um viewer próprio:

- **Contrato único:** `architecture.json` com componentes, classes, dependências, níveis (`levels`), CRAP e mutação.
- **Coletores:** Roslyn (estrutura .NET), análise de imports (Angular), conversores dos relatórios do Coverlet e Stryker para o mesmo JSON.
- **Viewer em Angular (MVP):** drill-down namespace → classe → métricas; cor por CRAP/mutação; setas vermelhas quando uma dependência viola a regra de camadas.
- **Substituto do companion:** botão "copiar prompt para o Copilot" com o contexto do que está na tela.
- **Fica para v2:** propostas "what-if" e layout automático sofisticado.

**Pergunta em aberto:** a regra de camadas hoje é Clean Architecture (Domain, Application, Infrastructure, API) ou outra?

---

## 4. Trazendo o Ponytail para o cérebro do Portal Abono

### 4.1 O que é

[Ponytail](https://github.com/dietrichgebert/ponytail) (MIT, Dietrich Gebert) é uma skill/plugin que faz o agente **não over-engineer**: antes de escrever, sobe uma "escada" (reutilizar código existente → stdlib → recurso nativo → só então código novo), mantendo validação, segurança e acessibilidade. Cada atalho vira um comentário `ponytail:` com o caminho de upgrade. Também há comandos de revisão, auditoria e dívida (`/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`).

### 4.2 Resultados publicados (leitura crítica)

- Em sessões reais de Claude Code num repositório FastAPI + React: ~54% menos código, ~20% mais barato, ~27% mais rápido, guardas de segurança intactas.
- Em tarefas isoladas: 80–94% menos código.
- **Os próprios autores avisam que são números de modelos Claude e variam por modelo.** No Copilot os modelos podem ser outros; tratar os números como hipótese e **medir** num caso real do Portal Abono.

### 4.3 Compatibilidade com o Copilot

- Há instalação para o **GitHub Copilot CLI** (plugin: `copilot plugin marketplace add DietrichGebert/ponytail` e `copilot plugin install ponytail@ponytail`).
- Há também **modo só-instruções**: o Copilot CLI lê `AGENTS.md` e `.github/copilot-instructions.md`.
- O plugin usa hooks em **Node.js**; sem `node` no PATH as skills funcionam, mas a ativação sempre-ligada fica silenciosa.

### 4.4 Recomendação: *vendorizar* no cérebro, não instalar plugin

Em ambiente financeiro, é preferível **copiar o conteúdo relevante para o repositório do cérebro** (versionado, revisado em PR) a depender de plugin de marketplace externo:

```
cerebro-portal-abono/
├── docs/                      # o que o produto é (já existente)
└── skills/
    ├── explorer/              # leitura/explicação (labAIdessa) — sem Ponytail
    ├── reviewer/              # revisão — usa a lógica do ponytail-review + gates
    ├── implementer/           # implementação — Ponytail + ub-mode adaptado
    ├── principios/
    │   ├── ponytail.md        # versão enxuta, adaptada (cópia revisada)
    │   └── ub-mode-adaptado.md
    └── casos-especificos/     # regras do Portal Abono, IRIS, LESS
```

### 4.5 Onde cada coisa se aplica

| Agente / skill | Ponytail | ub-mode adaptado |
|---|---|---|
| **labAIdessa-abono** (somente leitura, explica e ensina) | ❌ Não escreve código; a skill não se aplica | Só como referência de "o que é bom" ao explicar |
| **carmouQA-abono** | Parcial (critérios de revisão: "isso era necessário?") | Gates de qualidade como checklist |
| **implementer** | ✅ Sempre ligado | ✅ TDD + boundary/type + gates |
| **reviewer** | ✅ via lógica de review ("o que dava para não escrever?") | ✅ "Make it Right" como checklist |

### 4.6 Conflitos e ordem de precedência

Quando as regras discordarem, a ordem sugerida é:

1. **Regras do Portal Abono / do time** (casos específicos, padrões já adotados).
2. **Segurança e validação** (nunca cortadas, nem pelo Ponytail).
3. **ub-mode adaptado** (TDD, gates).
4. **Ponytail** (menos código possível dentro do que sobrou).

Pontos de atrito conhecidos:

- **Ponytail vs. TDD/mutação:** testes não entram na "dieta". Deixar explícito: *Ponytail aplica-se ao código de produção, não a testes*.
- **Ponytail vs. "Build the Lever":** vale só com aprovação humana.
- **Ponytail vs. Keep a Log:** resumo curto no fim, sem log por ação.
- **Padrões já existentes do Portal Abono:** "reutilizar código existente" deve significar *usar os padrões já presentes no repositório*, e o cérebro precisa apontar quais são.

---

## 5. Plano sugerido

1. **Escrever `ub-mode-adaptado.md`** (seção 2) e a versão enxuta do `ponytail.md`.
2. **Medir o Ponytail** em 2–3 tarefas reais do Portal Abono (com e sem), comparando volume de código e qualidade na revisão.
3. **Testar as ferramentas no lado Angular** (crapper, dryer, mutator) num projeto real; resolver o LCOV do Karma se necessário.
4. **Definir os gates .NET** (Coverlet + Stryker.NET + script de CRAP) e validar com segurança.
5. **Contrato `architecture.json`** e coletor Roslyn.
6. **Viewer em Angular** (MVP), só depois dos itens anteriores.

---

## 6. Pontos em aberto

- O Copilot do trabalho suporta Agent Skills (`SKILL.md`) ou só instruções de repositório?
- Qual a regra de camadas oficial do Portal Abono?
- Projetos Angular usam Karma/Jasmine ou outro runner?
- Política de segurança para Stryker.NET e ferramentas de terceiros na pipeline.
- Licença do ub-mode (não identificada) se for redistribuído.

## Fontes

- [unclebob/ub-mode](https://github.com/unclebob/ub-mode)
- [unclebob/crapper](https://github.com/unclebob/crapper), [dryer](https://github.com/unclebob/dryer), [mutator](https://github.com/unclebob/mutator), [uml-viewer](https://github.com/unclebob/uml-viewer)
- [DietrichGebert/ponytail](https://github.com/dietrichgebert/ponytail)
