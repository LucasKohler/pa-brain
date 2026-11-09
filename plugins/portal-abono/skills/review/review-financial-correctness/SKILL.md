---
name: review-financial-correctness
description: Revisa correção financeira - valores monetários, arredondamento, percentuais e tetos, datas de corte e fuso, idempotência, lançamentos duplicados, trilha de auditoria e dados pessoais (LGPD). Use em qualquer mudança que calcule, grave ou exiba valores, prazos ou benefícios no Portal Abono, IRIS ou LESS.
metadata:
  category: review
  roles: "reviewer,implementer,tester"
  owner: "time técnico"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Correção financeira

As regras do negócio (tetos, percentuais, prazos, elegibilidade) vêm da base de conhecimento (`explore-docs-lookup`), nunca da memória. Se a regra não estiver documentada, registre a dúvida para Produto.

## Valores e cálculo
- [ ] Valores monetários em `decimal` (C#) e tipo exato no banco (`decimal(p,s)`/`numeric`); nunca `double`/`float`.
- [ ] Regra de arredondamento explícita (`MidpointRounding`) e aplicada no ponto certo (por item ou no total) conforme a regra documentada.
- [ ] Percentuais e tetos: ordem das operações confere com a regra; teste com valores no limite exato, logo abaixo e logo acima.
- [ ] Divisões tratam divisor zero e resíduos de rateio (a soma das partes fecha com o total).
- [ ] Front-end não refaz cálculo de forma diferente do backend.

Ao explicar um cálculo, mostre-o por etapas a partir da entrada fornecida.

## Datas e prazos
- [ ] Data de corte, competência e prazos com regra de inclusão/exclusão clara (dia inclusive ou exclusive).
- [ ] Fuso horário consistente entre gravação, cálculo e exibição; datas sem hora não sofrem deslocamento.
- [ ] Dias úteis/feriados vêm da fonte oficial do sistema, não de lista fixa no código.
- [ ] Testes não usam `DateTime.Now`; o relógio é injetável.

## Idempotência e duplicidade
- [ ] Operação que gera efeito financeiro pode ser repetida sem duplicar (chave de idempotência, restrição única ou verificação prévia transacional).
- [ ] Reprocessamento de fila/lote não gera lançamento em dobro.
- [ ] Concorrência entre duas requisições iguais tratada.

## Auditoria e rastreabilidade
- [ ] Alterações de valor, status ou elegibilidade registram quem, quando, o quê e o valor anterior, conforme o padrão do sistema.
- [ ] Registros financeiros não são apagados fisicamente quando o padrão é estorno/inativação.

## Dados pessoais (LGPD)
- [ ] CPF, dados bancários e salário não aparecem em logs, mensagens de erro ou telemetria.
- [ ] Respostas de API não expõem mais dados pessoais do que a tela precisa.

## Saída
Para cada achado: regra (ID do documento), cálculo esperado x obtido com exemplo numérico, e severidade. Violação de regra financeira documentada é **Crítico**.
