---
name: explain-for-audience
description: Adapta uma explicação do sistema ou de uma mudança ao público - pessoa de produto ou negócio, dev iniciante no projeto ou dev sênior. Use quando pedirem para explicar, ensinar, fazer onboarding ou resumir algo para alguém específico.
metadata:
  category: explain
  roles: "teacher,reviewer"
  owner: "time técnico"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Explicação por público

Pergunte o público só se não estiver claro e ele mudar a resposta. A evidência e a classificação (Confirmado, Inferido, Não determinado) valem para todos os públicos.

## Produto e negócio
- Comece pelo problema do usuário e pela regra de negócio, com ID do documento.
- Descreva comportamento observável (o que a tela ou o processo faz), não classes.
- Use o vocabulário do glossário da base.
- Termine com: o que muda para o usuário, riscos e perguntas em aberto.

## Dev novo no projeto
- Ordem: o que é (1 frase) → fluxo ponta a ponta → onde está no código → armadilhas.
- Explique termos de domínio na primeira ocorrência.
- Aponte 2 ou 3 arquivos para começar a ler e o teste que melhor mostra o comportamento.
- Indique os documentos para aprofundar.

## Dev sênior
- Direto ao mecanismo: decisões, trade-offs, invariantes, concorrência, falhas.
- Destaque o que é não óbvio ou herdado (com o motivo, se documentado).
- Omita o básico.

## Regras gerais
- Exemplos numéricos sempre a partir de uma entrada concreta, com cálculo por etapas.
- Diagrama em Mermaid só se ajudar, sempre com resumo em texto.
- Não apresente intenção de negócio sem fonte; diga "não documentado" quando for o caso.
