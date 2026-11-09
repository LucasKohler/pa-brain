---
name: explore-intent-trace
description: Monta a matriz entre a intenção de uma mudança (item de trabalho, critérios de aceite, OpenSpec, regras da base) e a evidência no código e nos testes. Use ao revisar ou explicar uma mudança para saber o que foi pedido, o que foi feito, o que faltou e o que sobrou.
metadata:
  category: explore
  roles: "reviewer,tester,teacher,implementer"
  owner: "time técnico"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Rastreio de intenção

## Quando usar
- Mudança com item de trabalho, US, OpenSpec ou critério de aceite conhecido.
- Pergunta "isso atende ao que foi pedido?".

## Fontes de intenção (da mais forte para a mais fraca)
1. Critérios de aceite do item de trabalho, colados pela pessoa ou presentes no repositório.
2. Mudança OpenSpec com vínculo comprovado (ID explícito ou referência verificável). Nome parecido de branch **não** é vínculo.
3. Regras e fluxos da base com revisão humana (`explore-docs-lookup`).
4. Descrição do PR e mensagens de commit (indício, não prova).

Se não houver nenhuma fonte de intenção, diga isso e peça os critérios de aceite antes de afirmar que algo "atende".

## Procedimento
1. Liste cada requisito como um item atômico e verificável (R1, R2...), com a fonte.
2. Para cada item, procure no diff e no código onde ele é implementado.
3. Procure o teste que comprova o item. Leia o teste: ele verifica o comportamento ou só executa o código?
4. Classifique cada item.
5. Liste o que foi alterado **sem** requisito correspondente (escopo além do pedido).

## Saída

| Req. | Fonte | Implementação (caminho:símbolo) | Teste | Situação |
|---|---|---|---|---|
| R1 | US / OpenSpec / BR-xxx | ... | ... | Atendido · Parcial · Não encontrado · Divergente |

Depois da tabela:
- **Fora do escopo pedido:** mudanças sem requisito.
- **Interpretações diferentes:** onde o código entendeu o requisito de outro jeito.
- **Perguntas:** para Produto ou para o autor.

## Regras
- "Atendido" exige código lido; se houver teste, diga se foi executado ou só lido.
- Uma tarefa marcada como concluída não é evidência.
