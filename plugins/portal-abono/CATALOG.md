# Catálogo do plugin portal-abono

> Arquivo GERADO por `scripts/skills/build_catalog.py`. Não edite à mão.

## Agentes

| Agente | Descrição |
|---|---|
| `carmouQA-abono` | Agente de QA dos sistemas Portal Abono, IRIS e LESS. PENDENTE - definição a ser trazida do repositório de arquitetura e contextualizada para o Portal Abono. |
| `labAIdessa-abono` | Revisora e professora dos sistemas Portal Abono, IRIS e LESS. Explica código, mudanças locais e fluxos, conecta a implementação às regras de negócio e ao produto, e revisa mudanças com evidência. Não altera código. |

## Skills

### Explorar: entender código, intenção e impacto

| Skill | Papéis | Dono | Versão | Descrição |
|---|---|---|---|---|
| `explore-blast-radius` | reviewer,implementer,explorer | time técnico | 1.0.0 | Mede o raio de impacto de uma mudança - chamadores, implementações, consumidores de eventos e filas, uso de tabelas e o histórico do trecho no git. Use antes de concluir uma revisão de código compartilhado, contrato, evento, tabela ou configuração. |
| `explore-docs-lookup` | explorer,reviewer,implementer,tester,teacher | time técnico | 1.0.0 | Navega a base de conhecimento do Portal Abono, IRIS e LESS (produto, regras de negócio, fluxos, arquitetura, glossário). Use para responder o que é, para que serve ou por que funciona assim, ou para achar os documentos ligados a um arquivo de código. |
| `explore-intent-trace` | reviewer,tester,teacher,implementer | time técnico | 1.0.0 | Monta a matriz entre a intenção de uma mudança (item de trabalho, critérios de aceite, OpenSpec, regras da base) e a evidência no código e nos testes. Use ao revisar ou explicar uma mudança para saber o que foi pedido, o que foi feito, o que faltou e o que sobrou. |

### Revisar: checklists de revisão

| Skill | Papéis | Dono | Versão | Descrição |
|---|---|---|---|---|
| `review-angular` | reviewer,implementer | time frontend | 1.0.0 | Checklist de revisão para Angular e TypeScript - RxJS e vazamento de inscrições, detecção de mudanças, formulários e validação, tratamento de erros HTTP, segurança e testes. Use ao revisar ou implementar front-end Angular do Portal Abono, IRIS ou LESS. |
| `review-contract-compat` | reviewer,implementer | time técnico | 1.0.0 | Verifica compatibilidade de contratos - APIs REST, DTOs, eventos e mensagens de fila, schemas e enums - e se a mudança quebra consumidores existentes. Use quando um endpoint, DTO, evento, fila, enum ou payload for alterado. |
| `review-db-migration` | reviewer,implementer | time backend | 1.0.0 | Revisa migrações de banco e mudanças de modelo de dados - locks e tempo de execução, backfill, reversão, compatibilidade com a versão anterior da aplicação, índices e integridade. Use quando houver migration do EF Core, script SQL ou mudança em entidade persistida. |
| `review-dotnet-lowlevel` | reviewer,implementer | time backend | 1.0.0 | Checklist de revisão baixo nível para C#/.NET - async e cancelamento, injeção de dependência, EF Core, nulos, exceções, recursos e concorrência. Use ao revisar ou implementar código C# do Portal Abono, IRIS ou LESS. |
| `review-financial-correctness` | reviewer,implementer,tester | time técnico | 1.0.0 | Revisa correção financeira - valores monetários, arredondamento, percentuais e tetos, datas de corte e fuso, idempotência, lançamentos duplicados, trilha de auditoria e dados pessoais (LGPD). Use em qualquer mudança que calcule, grave ou exiba valores, prazos ou benefícios no Portal Abono, IRIS ou LESS. |
| `review-security` | reviewer,implementer | time técnico | 1.0.0 | Revisão de segurança de aplicação - autorização por recurso, autenticação, validação de entrada, injeção, exposição de dados, segredos e logs. Use quando a mudança toca endpoints, permissões, entrada externa, integrações, arquivos, logs ou dados pessoais. |

### Implementar: padrões do projeto

_Nenhuma skill ainda._

### Verificar: execução de build e testes

| Skill | Papéis | Dono | Versão | Descrição |
|---|---|---|---|---|
| `verify-in-worktree` | reviewer,tester,implementer | time técnico | 1.0.0 | Executa build e testes existentes em um git worktree temporário, sem tocar na árvore de trabalho da pessoa, para transformar uma suspeita em evidência. Use quando for preciso confirmar que algo compila, que um teste passa ou falha, ou comparar o comportamento antes e depois de uma mudança. |

### Documentar: manter a base de conhecimento

| Skill | Papéis | Dono | Versão | Descrição |
|---|---|---|---|---|
| `document-doc-impact` | reviewer,implementer,documenter | time técnico | 1.0.0 | Identifica quais documentos da base de conhecimento uma mudança de código afeta e propõe as atualizações, com evidência, sem editar a base. Use depois de analisar uma mudança que toca regras de negócio, fluxos, dados, integrações ou decisões documentadas. |

### Explicar: ensino e onboarding

| Skill | Papéis | Dono | Versão | Descrição |
|---|---|---|---|---|
| `explain-for-audience` | teacher,reviewer | time técnico | 1.0.0 | Adapta uma explicação do sistema ou de uma mudança ao público - pessoa de produto ou negócio, dev iniciante no projeto ou dev sênior. Use quando pedirem para explicar, ensinar, fazer onboarding ou resumir algo para alguém específico. |

### Domínio: casos específicos do negócio

_Nenhuma skill ainda._

Total: 12 skills.
