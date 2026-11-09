---
name: brain-add-eval
description: Adiciona casos de avaliação para um agente ou skill em evals/, no formato do cérebro, separando conjunto de desenvolvimento e de avaliação. Use ao registrar uma pergunta real, um PR passado com bug conhecido ou uma falha observada de um agente.
---

# Adicionar caso de avaliação

1. **Arquivo**: `evals/agents/<agente>/cases.yaml` ou `evals/skills/<skill>/cases.yaml`.
2. **Conjunto**: `dev` (pode orientar ajustes) ou `eval` (nunca usado para ajustar prompt, skill ou documento). Na dúvida, `eval`.
3. **Campos**: siga o exemplo em `evals/agents/labAIdessa-abono/cases.yaml`: `id`, `set`, `kind`, `prompt`, `context`, `expected_docs`, `expected_findings`, `must_not`, `verified_by_human`.
4. **Origem real**: prefira perguntas e PRs reais do time. Não inclua código proprietário extenso nem dados de clientes: referencie commit, PR ou caminho.
5. **Resultados** de execução ficam em `evals/**/results/` (fora do git), com host, versão do Copilot CLI, modelo, data, resposta e veredito.
6. `verified_by_human: true` só quando alguém conferiu o resultado esperado.
