---
name: document-doc-impact
description: Identifica quais documentos da base de conhecimento uma mudança de código afeta e propõe as atualizações, com evidência, sem editar a base. Use depois de analisar uma mudança que toca regras de negócio, fluxos, dados, integrações ou decisões documentadas.
metadata:
  category: document
  roles: "reviewer,implementer,documenter"
  owner: "time técnico"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Impacto na documentação

## Procedimento
1. Liste caminhos e símbolos alterados (do diff ou da revisão examinada).
2. Consulte `docs/.index/code-map.json` em `$PA_BRAIN_HOME` para cada caminho; inclua correspondências por glob.
3. Amplie um salto por `related_docs` para regras, fluxos, dados e integrações.
4. Para cada documento candidato, compare o que ele afirma (no canal certo) com o comportamento novo observado.
5. Mudança relevante sem documento ligado é **lacuna**: proponha documento novo com tipo e título.

O mapa ajuda a descobrir, mas não prova cobertura: mudanças podem afetar documentos sem referência ao arquivo alterado.

## Saída

| Documento (ID ou "novo") | Trecho/canal | Mudança proposta | Evidência (caminho:símbolo, escopo) | Classificação | Pergunta ao revisor |
|---|---|---|---|---|---|

Encerre com: "Proposta para revisão humana; nenhum arquivo foi alterado."

## Regras
- Não reescreva regra de negócio a partir do código: o código mostra o comportamento novo; se ele contradiz a regra, é **divergência** para Produto decidir.
- Diferença de hash ou de caminho, sozinha, não justifica alterar um documento.
- Quem aplica a mudança na base é uma pessoa, via PR, seguindo `brain-new-doc` no repositório do cérebro.
