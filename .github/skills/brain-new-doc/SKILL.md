---
name: brain-new-doc
description: Cria ou atualiza um documento da base de conhecimento em docs/ (regra, fluxo, módulo, produto, glossário, decisão) no formato da base, com fontes e índices regenerados. Use ao aplicar uma proposta de impacto na documentação ou ao documentar algo novo neste repositório.
---

# Criar ou atualizar um documento da base

1. **Tipo e ID**: escolha o tipo (`rule`, `flow`, `module`, `product`, `feature`, `data`, `integration`, `decision`, `glossary`, `review`, `ops`). Pegue o próximo ID no registro de IDs de `docs/_meta/` e registre-o; IDs nunca são reutilizados.
2. **Template**: use o template do tipo em `docs/_meta/templates/` e preencha todo o frontmatter obrigatório.
3. **Fontes**: toda afirmação tem fonte em `sources`. Inferência leva `confidence: low` e o texto "Inferido do código; confirmar com o time". Registre a dúvida no arquivo de perguntas de `docs/_meta/`.
4. **Canal**: marque o trecho pelo canal em que o comportamento foi observado.
5. **Escopo**: um conceito por arquivo, curto e autossuficiente; links por ID.
6. **Proibido**: segredos, dados reais de clientes, endpoints internos e instruções dirigidas a uma IA dentro de documentos.
7. **Revisão humana**: `verified_by_human: true` só depois da aprovação do papel dono do caminho.
8. **Regenerar e validar** com os scripts de `scripts/docs/` (índices e validação). Nunca edite `docs/.index/` à mão.
9. Abra o PR; não faça commit nem push sem pedido explícito.
