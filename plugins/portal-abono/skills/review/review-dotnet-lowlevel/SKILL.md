---
name: review-dotnet-lowlevel
description: Checklist de revisão baixo nível para C#/.NET - async e cancelamento, injeção de dependência, EF Core, nulos, exceções, recursos e concorrência. Use ao revisar ou implementar código C# do Portal Abono, IRIS ou LESS.
metadata:
  category: review
  roles: "reviewer,implementer"
  owner: "time backend"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Revisão baixo nível em C#/.NET

Para cada achado, informe caminho:símbolo e se foi **lido** ou **inferido**. Riscos de desempenho e concorrência sem medição são **Inferido**.

## Async e cancelamento
- [ ] Sem `.Result`, `.Wait()` ou `GetAwaiter().GetResult()` em código chamado por requisição (risco de bloqueio e esgotamento de threads).
- [ ] Sem `async void` fora de handlers de evento.
- [ ] `CancellationToken` recebido é repassado até I/O (EF, HttpClient, filas).
- [ ] Tarefas disparadas sem `await` (fire-and-forget) têm tratamento de erro e escopo próprio.
- [ ] `Task.WhenAll` com muitas tarefas não satura conexões do banco ou serviços externos.

## Injeção de dependência e ciclo de vida
- [ ] Serviço `Singleton` não depende de `Scoped` (ex.: `DbContext`) diretamente.
- [ ] `DbContext` não é compartilhado entre threads nem guardado em campo estático.
- [ ] `HttpClient` vem de `IHttpClientFactory` ou cliente tipado, não `new HttpClient()` por chamada.
- [ ] Background services criam escopo (`IServiceScopeFactory`) por unidade de trabalho.

## EF Core e acesso a dados
- [ ] Sem N+1: navegações acessadas em loop têm `Include`/projeção.
- [ ] Consultas só de leitura usam `AsNoTracking` ou projeção.
- [ ] Filtros aplicados antes de `ToList()`/`AsEnumerable()` (não filtrar em memória).
- [ ] Paginação com ordenação determinística.
- [ ] SQL bruto parametrizado (`FromSql` com interpolação segura ou parâmetros), nunca concatenação.
- [ ] Transação envolve todas as escritas que precisam ser atômicas; leitura-modifica-escrita concorrente tem controle (token de concorrência, lock ou idempotência).
- [ ] `SaveChanges` não é chamado dentro de loop sem necessidade.

## Nulos, limites e tipos
- [ ] Nullable reference types respeitados; sem `!` para silenciar aviso sem justificativa.
- [ ] Conversões e parse com `TryParse` e cultura explícita (`CultureInfo.InvariantCulture` ou pt-BR quando é exibição).
- [ ] Valores monetários em `decimal` (ver `review-financial-correctness`).
- [ ] Datas: `DateTime.Kind` consistente; preferir `DateTimeOffset` ou UTC na persistência.

## Exceções e erros
- [ ] Sem `catch` vazio ou que só registra e engole erro de negócio.
- [ ] `throw;` para relançar (não `throw ex;`).
- [ ] Erro esperado de negócio vira resposta tratada (código HTTP e mensagem), não 500.
- [ ] Logs de erro têm contexto suficiente, sem dados pessoais nem segredos.

## Recursos e desempenho
- [ ] `IDisposable`/`IAsyncDisposable` com `using`/`await using`.
- [ ] Sem alocação ou consulta dentro de loop quente que poderia sair do loop.
- [ ] Cache tem expiração e chave que inclui todos os parâmetros relevantes.

## Concorrência
- [ ] Estado compartilhado (estático, singleton) é imutável ou protegido.
- [ ] Coleções compartilhadas usam tipos concorrentes ou lock.
- [ ] Consumidores de fila são idempotentes (mensagem repetida não duplica efeito).

## Testes
- [ ] Caso de borda novo tem teste que falharia sem a mudança.
- [ ] Testes não dependem de data/hora real nem de ordem de execução.
