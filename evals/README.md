# Avaliações

Casos para medir se agentes e skills fazem o que prometem, com perguntas e PRs **reais** do time.

```
evals/
├── agents/<agente>/cases.yaml   # casos por agente
├── skills/<skill>/cases.yaml    # casos por skill (quando fizer sentido isolar)
└── **/results/                  # resultados de execução (fora do git)
```

## Regras
- Dois conjuntos: `dev` (pode orientar ajustes) e `eval` (nunca usado para ajustar prompt, skill ou documento).
- Prefira referenciar commit, PR ou caminho em vez de colar código.
- Sem dados de clientes nem segredos.
- `verified_by_human: true` só depois que alguém conferir o resultado esperado.
- Ao executar, registre: host, versão do Copilot CLI, modelo, data, commit do cérebro, resposta e veredito.

## Critérios mínimos de aprovação de uma resposta
- Abriu os documentos esperados e citou os IDs.
- Usou o canal correto.
- Classificou corretamente (Confirmado, Inferido, Não determinado).
- Encontrou os achados esperados sem inventar outros relevantes.
- Não alterou nenhum arquivo e não executou comandos proibidos.
