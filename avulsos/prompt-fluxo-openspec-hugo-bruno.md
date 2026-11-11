# Prompt: fluxo OpenSpec com os agentes hugoSpec-abono e brunoCode-abono

> Cole tudo abaixo no GitHub Copilot CLI, aberto na raiz do repositório do cérebro. Use **Copilot Fusion High** para gerar o plano e **Standard** para a implementação.

---

Você vai formalizar, no repositório "cérebro" do Portal Abono, o fluxo de desenvolvimento com OpenSpec e dois agentes novos. A base de docs, as skills (incluindo as de implementação baseadas no ub-mode) e os agentes `labAIdessa-abono` e `carmouQA-abono` **já existem** no repositório. Reaproveite tudo isso; não recrie nem duplique.

## Contexto

- Stack: .NET (C#) e Angular. Sistemas: Portal Abono, IRIS e LESS. Setor financeiro.
- Ferramentas: só GitHub Copilot (CLI e Agents window do VS Code). O trabalho é feito em worktrees.
- Ambiente: VDI lenta. Cada agente, sessão ou passo extra tem custo.
- Modelos disponíveis: Copilot Fusion **Standard** e **High**.

Antes de começar, localize no repositório e me diga onde estão:
- os agentes existentes e o padrão de frontmatter que eles usam;
- as skills de implementação do ub-mode (nomes e caminhos);
- os lançadores (`scripts/install/launchers.ps1` ou equivalente);
- o validador e o gerador de catálogo das skills, se existirem;
- a configuração do OpenSpec no repositório e a versão instalada (`openspec --version`);
- como o `carmouQA-abono` funciona hoje. Ele executa de forma automatizada os casos de teste que o QA monta (o que o QA faria manualmente). Descubra:
  - de onde ele lê os casos do QA e em que formato;
  - contra o que ele roda: a aplicação local na worktree ou um ambiente (dev ou homologação) depois do deploy;
  - o que ele precisa receber para rodar uma mudança específica.
  Use isso para posicionar a etapa de QA no fluxo (passo 5 ou depois do deploy, ver a tabela). Não altere o comportamento do `carmouQA-abono`.

Se algo não existir, me diga em vez de criar por conta própria.

## O fluxo (decidido; não reabra sem motivo forte)

| Etapa | Sessão | Agente | Fusion |
|---|---|---|---|
| 1. Explorar (opcional) | nova | `labAIdessa-abono` | Standard |
| 2. Propor: `/opsx-propose <nome>` | nova | `hugoSpec-abono` | Standard (High em mudança grande, ambígua ou com regra financeira) |
| **Gate humano:** eu reviso e aprovo a spec e o `tasks.md` | | | |
| 3. Aplicar: `/opsx-apply`, numa worktree | nova | `brunoCode-abono` | Standard |
| 4. Revisar: diff contra a spec | nova | `labAIdessa-abono` | Standard (High em revisão DEEP, risco financeiro ou segurança) |
| 5. QA: executar de forma automatizada os casos de teste do QA para esta mudança | nova | `carmouQA-abono` | Standard |
| 6. PR no Azure DevOps: **gate humano** e merge | | | |

> Se o `carmouQA-abono` roda contra um ambiente de dev ou homologação, e não contra a aplicação local, a etapa 5 vai para **depois do deploy nesse ambiente**, e não antes do PR. Ajuste a ordem conforme o que encontrar e me diga qual foi a escolha.
| 7. Arquivar: `/opsx-archive` | | | |

Princípios:

1. **Uma sessão nova por etapa.** Cada sessão recebe só os artefatos (spec, `tasks.md`, diff), nunca o histórico da anterior.
2. **Sem orquestrador automático e sem agente explorer separado.** A exploração usa o `labAIdessa-abono`.
3. **Uma única linha de escrita.** Só o `brunoCode-abono` escreve código de produção, e nunca há dois agentes escrevendo em paralelo.
4. **O `tasks.md` é o plano.** O `brunoCode-abono` não roda `/plan` por cima. Plano interno só para uma tarefa grande ou vaga, sem substituir o `tasks.md`.
5. **Não copie as instruções do OpenSpec para dentro dos agentes.** O `openspec update` as regenera. Os agentes chamam os comandos `/opsx-*` e acrescentam só as regras do time e as permissões.
6. **Nem toda mudança passa pelo fluxo completo.** Use OpenSpec quando houver pelo menos 3 destes sinais: requisito ambíguo, mais de um arquivo ou serviço, mais de uma sessão, mais de um revisor, código legado, custo alto de erro. Bug pequeno e óbvio vai direto, sem spec.
7. **Laço de correção com limite.** Revisão ou QA reprovados voltam ao `brunoCode-abono`. Depois de **duas** reprovações na mesma tarefa, volta para o `hugoSpec-abono` revisar a spec.
8. **Os casos do QA são a referência da etapa de QA.** Os cenários `WHEN/THEN` da spec podem servir de insumo para o QA montar ou revisar os casos, mas não os substituem. O `hugoSpec-abono` pode listar no fim da proposta os cenários que o QA deveria cobrir.

## O que implementar

### 1. Agente `hugoSpec-abono`

Crie `hugoSpec-abono.agent.md` na pasta de agentes, no mesmo padrão de frontmatter dos agentes existentes.

- **Papel:** escreve a proposta OpenSpec completa (`proposal.md`, `design.md`, `tasks.md` e specs) a partir do pedido, do código e da base de docs.
- **Ferramentas:** leitura, busca, shell de leitura (`git log`, `git show`, `rg`) e escrita **restrita a `openspec/changes/`**. Não edita código de produção. Se o frontmatter não permitir restringir a escrita por caminho, deixe a regra explícita no texto do agente e me avise da limitação.
- **Regras:**
  - cada requisito tem cenários `WHEN/THEN`;
  - cite o documento de origem da base de docs quando houver;
  - classifique a intenção de negócio como Confirmado, Inferido ou Não determinado;
  - liste perguntas em aberto no fim da proposta, em vez de inventar regra.
- **Formato do `tasks.md`:** cada tarefa traz arquivos prováveis, critério de pronto verificável (qual teste passa) e dependências. Fatias pequenas.
- **Fim:** pede aprovação humana. Nunca chama `/opsx-apply`.

### 2. Agente `brunoCode-abono`

Crie `brunoCode-abono.agent.md`.

- **Papel:** implementa uma mudança OpenSpec aprovada via `/opsx-apply`, seguindo o `tasks.md`.
- **Ferramentas:** leitura e escrita; shell para `dotnet build`, `dotnet test`, testes e lint do Angular, e git de leitura. Sem `git push`, sem rede e sem apagar nada fora da worktree.
- **Regras:**
  - só implementa o que está em `tasks.md` e marca cada tarefa concluída;
  - segue as skills de implementação do ub-mode **que já existem** no repositório (referencie pelos nomes reais);
  - registra pendências em vez de refatorar fora do escopo;
  - commits pequenos, um por fatia, com o porquê, o quê e a prova; nunca commit nem push na main;
  - antes de dizer "pronto", mostra a saída resumida de build e testes (só falhas e totais);
  - aplica o limite do laço de correção (princípio 7).

### 3. Skill do fluxo (orquestrador "de papel")

Crie uma skill de fluxo na categoria de implementação (por exemplo, `implement-change-flow`), seguindo a convenção de nomes do repositório.

- Diz, a partir do estado atual, em que etapa a mudança está e qual o próximo passo. Para isso, olha:
  - se existe `openspec/changes/<nome>/`;
  - se o `tasks.md` está completo;
  - se há commits na worktree;
  - se a revisão e o QA passaram.
- Para cada etapa, informa o agente, o comando exato (`copilot --agent <nome>` e o `/opsx-*`) e o nível do Fusion, conforme a tabela acima.
- Inclui o filtro "quando usar o fluxo completo" (princípio 6).
- **Não executa** os passos. Só orienta.

### 4. Lançadores

Nos lançadores existentes, adicione as funções `hugospec-abono` e `brunocode-abono` (minúsculas, como as atuais), que abrem os agentes `hugoSpec-abono` e `brunoCode-abono`, no mesmo padrão: atualização do cérebro, `--add-dir` da pasta docs, `--allow-tool` e `--deny-tool`.

- `brunocode-abono` abre na worktree atual e avisa se a pasta atual for a main.
- Confira em `copilot --help` se existe flag para escolher o modelo ou o nível do Fusion. Se existir, use Standard por padrão. Se não existir, não invente flag: registre na skill de fluxo que a escolha é manual no seletor de modelos.

### 5. Regras de economia de tokens

Acrescente uma seção curta no `AGENTS.md` e na skill de fluxo:
- Fusion Standard por padrão; High só nos casos da tabela.
- Não trocar de modelo no meio da sessão, para não perder o cache.
- Passar artefatos entre sessões, não histórico.
- Revisão limitada ao diff e aos vizinhos diretos, com profundidade proporcional.
- Pedir saídas resumidas de build e testes.
- Agentes e `AGENTS.md` enxutos.

### 6. Validação e documentação

- Se houver validador e catálogo, atualize-os para reconhecer os novos agentes e a nova skill, e rode-os até passarem sem erro.
- No README, inclua uma seção curta "Fluxo de mudança" apontando para a skill de fluxo.
- Inclua uma seção "Verificar no ambiente real" com estes testes manuais:
  1. `hugospec-abono` abre o agente, e `/opsx-propose` cria a pasta em `openspec/changes/`.
  2. O `hugoSpec-abono` não edita código de produção (impedido ou, no mínimo, instruído).
  3. `brunocode-abono`, numa worktree, roda `/opsx-apply` e segue o `tasks.md` sem criar outro plano.
  4. O `brunoCode-abono` não consegue fazer `git push`, inclusive `git -C . push`.
  5. Os comandos `/opsx-*` funcionam com esses agentes na versão do Copilot e do OpenSpec instalada.
  6. O `labAIdessa-abono` continua sem conseguir escrever.
  7. O `carmouQA-abono` executa os casos do QA de uma mudança real na posição definida no fluxo (local ou depois do deploy).

## Restrições

- Não altere a base de docs nem as skills existentes, exceto para referenciar os novos agentes.
- Não instale pacotes nem ferramentas.
- Não faça commit, push nem abra PR sem eu pedir.
- Português (Brasil) nos textos; inglês em identificadores e código.
- Escreva pouco: cada agente com no máximo ~150 linhas e a skill de fluxo com no máximo ~120 linhas.
- Quando não conseguir confirmar algo (frontmatter, flags, comportamento dos comandos), diga explicitamente o que não confirmou. Não apresente suposição como fato.

## Como trabalhar

1. **Primeiro, só leia e me devolva um plano curto:**
   - o que encontrou no repositório (itens do "Antes de começar");
   - arquivos que vai criar ou alterar;
   - o que confirmou e o que não conseguiu confirmar;
   - dúvidas.
   **Espere minha aprovação.**
2. Depois de aprovado, implemente nesta ordem: agentes, skill de fluxo, lançadores, regras de tokens, validação e docs.
3. **Entregue no fim:** lista de arquivos criados e alterados, saída resumida da validação, pendências e os testes manuais que eu preciso rodar.
