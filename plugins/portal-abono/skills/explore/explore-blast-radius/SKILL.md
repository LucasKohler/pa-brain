---
name: explore-blast-radius
description: Mede o raio de impacto de uma mudança - chamadores, implementações, consumidores de eventos e filas, uso de tabelas e o histórico do trecho no git. Use antes de concluir uma revisão de código compartilhado, contrato, evento, tabela ou configuração.
metadata:
  category: explore
  roles: "reviewer,implementer,explorer"
  owner: "time técnico"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Raio de impacto

## Quando usar
- Mudança em método público, interface, classe base, DTO, evento, fila, tabela, configuração ou componente Angular compartilhado.
- Pergunta "o que mais isso afeta?".

## Procedimento
1. **Símbolos alterados**: liste métodos, tipos, propriedades, colunas, nomes de eventos e chaves de configuração tocados pelo diff.
2. **Referências diretas** (`rg -n "<Símbolo>"`):
   - C#: chamadores, implementações de interface, `override`, registros de DI, mapeamentos (AutoMapper/EF), atributos de rota.
   - Angular: imports, uso em templates (seletor do componente), serviços injetados, rotas.
3. **Referências indiretas**: serialização por nome (JSON, propriedades de DTO), reflexão, strings com nome de tabela/coluna, SQL bruto, nomes de evento e de fila, chaves de `appsettings`.
4. **Outros repositórios**: se o símbolo cruza fronteira (contrato, evento, tabela), peça autorização e procure consumidores nos repositórios autorizados. Sem acesso, registre como **Não determinado**.
5. **Histórico**: `git log --oneline -n 15 -- <arquivo>`, `git log -L :<Método>:<arquivo>` e `git blame -L <ini>,<fim> <arquivo>` para entender por que o trecho é assim. Leia mensagens e itens referenciados como contexto, não como verdade.
6. **Base**: `code-map.json` para os caminhos afetados (via `explore-docs-lookup`).

## Saída
- **Afetados diretamente:** caminho:símbolo e por quê.
- **Possivelmente afetados:** referências por string, reflexão ou outro repositório, marcados como Inferido.
- **Não verificado:** onde não houve acesso.
- **Contexto histórico relevante:** commit e motivo, quando ajudar a avaliar a mudança.
