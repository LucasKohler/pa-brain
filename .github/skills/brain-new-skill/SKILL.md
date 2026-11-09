---
name: brain-new-skill
description: Cria ou altera uma skill do plugin portal-abono no padrão do cérebro (categoria, nome com prefixo, frontmatter, metadata, catálogo e validação). Use ao pedir para criar, mover, renomear ou revisar uma skill neste repositório.
---

# Criar ou alterar uma skill do plugin

1. **Categoria**: escolha uma de `explore`, `review`, `implement`, `verify`, `document`, `explain`, `domain`. Regra ou fluxo específico do negócio vai em `domain`.
2. **Nome**: `<categoria>-<tema>` em minúsculas com hífens (`domain-<tema>` para domínio). Confira no `plugins/portal-abono/CATALOG.md` que não existe outro igual.
3. **Pasta**: `plugins/portal-abono/skills/<categoria>/<nome>/SKILL.md`, a partir de `templates/SKILL.template.md`.
4. **Descrição**: o que faz e quando usar, com termos que a pessoa usaria. É ela que faz o Copilot carregar a skill.
5. **Conteúdo**:
   - Procedimento e checklist verificáveis; permissões e formato de resposta ficam no agente, não na skill.
   - Referencie regras da base por ID; não copie o texto das regras.
   - Detalhe longo vai em `references/` dentro da pasta da skill.
   - Scripts em `scripts/` só com revisão do time técnico.
6. **Metadata**: `category`, `roles`, `owner`, `version`, `origin` (e `docs` com IDs, se houver), todos como strings.
7. **Validar e catalogar**:
   ```
   python scripts/skills/validate_skills.py
   python scripts/skills/build_catalog.py
   ```
8. Se algum agente deve usar a skill, atualize a tabela de roteamento no `.agent.md` dele.
9. Abra o PR; não faça commit nem push sem pedido explícito.
