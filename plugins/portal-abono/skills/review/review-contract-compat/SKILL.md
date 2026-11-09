---
name: review-contract-compat
description: Verifica compatibilidade de contratos - APIs REST, DTOs, eventos e mensagens de fila, schemas e enums - e se a mudança quebra consumidores existentes. Use quando um endpoint, DTO, evento, fila, enum ou payload for alterado.
metadata:
  category: review
  roles: "reviewer,implementer"
  owner: "time técnico"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Compatibilidade de contratos

## Mudanças que quebram consumidores
- [ ] Campo removido ou renomeado (inclusive por mudança de política de serialização, como camelCase).
- [ ] Tipo de campo alterado (ex.: `int` → `string`, data com formato diferente, decimal com outra precisão).
- [ ] Campo opcional que virou obrigatório na entrada.
- [ ] Valor de enum removido, renomeado ou com número alterado; enum serializado como número x texto.
- [ ] Rota, verbo HTTP ou código de status alterado.
- [ ] Semântica alterada com o mesmo formato (o campo continua igual, mas significa outra coisa).
- [ ] Evento/mensagem com nome, tópico, fila ou chave de roteamento alterados.

## Mudanças geralmente seguras (confirmar)
- Campo novo opcional na saída (consumidores precisam ignorar campos desconhecidos).
- Endpoint novo.
- Valor de enum novo (consumidores precisam tolerar valor desconhecido).

## Procedimento
1. Identifique o contrato alterado e sua versão.
2. Encontre consumidores com `explore-blast-radius` (front Angular, outros serviços, jobs, integrações externas).
3. Para cada consumidor, diga se ele quebra, e com que evidência (lido ou inferido).
4. Verifique estratégia de transição: versionamento, campo novo + antigo durante a migração, ordem de implantação (produtor e consumidor).
5. Mensagens já enfileiradas no formato antigo continuam processáveis?

## Saída
| Contrato | Mudança | Consumidor | Quebra? | Evidência | Mitigação sugerida |
|---|---|---|---|---|---|
