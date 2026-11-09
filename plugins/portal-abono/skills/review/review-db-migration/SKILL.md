---
name: review-db-migration
description: Revisa migrações de banco e mudanças de modelo de dados - locks e tempo de execução, backfill, reversão, compatibilidade com a versão anterior da aplicação, índices e integridade. Use quando houver migration do EF Core, script SQL ou mudança em entidade persistida.
metadata:
  category: review
  roles: "reviewer,implementer"
  owner: "time backend"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Revisão de migração de banco

Confirme o banco envolvido (SQL Server ou PostgreSQL); o comportamento de lock e de DDL difere entre eles.

## Segurança da execução
- [ ] Alteração em tabela grande não trava escrita por tempo longo (adicionar coluna com default, alterar tipo, criar índice sem opção online/concurrent).
- [ ] Backfill de muitos registros em lotes, não em um único `UPDATE`.
- [ ] Migração não depende de dados que podem não existir em todos os ambientes.

## Compatibilidade entre versões
- [ ] A versão anterior da aplicação continua funcionando com o banco já migrado (implantação gradual e rollback da aplicação).
- [ ] Remoção ou renomeação de coluna feita em etapas (adicionar nova → migrar uso → remover antiga em entrega posterior).
- [ ] Coluna nova `NOT NULL` tem default ou backfill antes da restrição.

## Reversão
- [ ] Existe caminho de volta (migration `Down` funcional ou script de rollback) ou a irreversibilidade está explícita e aprovada.
- [ ] Perda de dados no `Down` está sinalizada.

## Integridade e desempenho
- [ ] Chaves estrangeiras, restrições únicas e checks refletem as regras de negócio documentadas.
- [ ] Índice novo atende a consultas reais; índice removido não é usado por consulta existente.
- [ ] Tipos de valores monetários e datas corretos (ver `review-financial-correctness`).

## Consistência com o código
- [ ] Modelo EF (configuração e snapshot) bate com o script gerado.
- [ ] SQL bruto, procedures e views que usam as colunas alteradas foram atualizados (`explore-blast-radius`).

## Saída
Indique o risco operacional (lock, duração, perda de dados) separado do risco funcional, e o que precisa ser validado em ambiente com volume real.
