---
name: review-angular
description: Checklist de revisão para Angular e TypeScript - RxJS e vazamento de inscrições, detecção de mudanças, formulários e validação, tratamento de erros HTTP, segurança e testes. Use ao revisar ou implementar front-end Angular do Portal Abono, IRIS ou LESS.
metadata:
  category: review
  roles: "reviewer,implementer"
  owner: "time frontend"
  version: "1.0.0"
  origin: "original"
  docs: ""
---

# Revisão Angular

Antes de revisar, confira a versão do Angular em `package.json` (por exemplo, se usa componentes standalone e signals) e siga o padrão já usado no projeto.

## RxJS e inscrições
- [ ] Toda inscrição manual é encerrada (`takeUntilDestroyed`, `async` pipe ou `unsubscribe`).
- [ ] Sem `subscribe` aninhado; usar `switchMap`/`concatMap`/`mergeMap` conforme a semântica desejada.
- [ ] `switchMap` em buscas (cancela a anterior); `concatMap` quando a ordem importa; cuidado com `mergeMap` em escrita.
- [ ] Erros tratados em `catchError` sem matar o fluxo quando ele deve continuar.
- [ ] Sem chamada HTTP disparada várias vezes por múltiplos `async` pipes no mesmo observable (usar `shareReplay` com critério).

## Detecção de mudanças e desempenho
- [ ] `ChangeDetectionStrategy.OnPush` onde o padrão do projeto usa; dados de entrada tratados como imutáveis.
- [ ] Sem chamada de função cara diretamente no template.
- [ ] Listas com `track`/`trackBy`.
- [ ] Signals: `computed` sem efeito colateral; `effect` não usado para derivar estado.

## Formulários e regras
- [ ] Validação do front espelha a regra de negócio, mas **a regra vale no backend**; verificar se o backend também valida.
- [ ] Valores numéricos e monetários não sofrem conversão de ponto flutuante nem de formato de localidade ao enviar (`"1.234,56"` x `1234.56`).
- [ ] Datas enviadas com fuso definido; sem deslocamento de um dia por conversão de fuso.
- [ ] Estados de envio: botão desabilitado durante envio (evita duplo envio).

## HTTP e erros
- [ ] Erros HTTP mostram mensagem útil e não expõem detalhes técnicos.
- [ ] Interceptors não engolem erros nem repetem requisições não idempotentes.
- [ ] Contrato com a API conferido contra o DTO do backend (ver `review-contract-compat`).

## Segurança
- [ ] Sem `bypassSecurityTrust*` sem justificativa.
- [ ] Sem `innerHTML` com conteúdo vindo do usuário ou da API sem sanitização.
- [ ] Sem token, dado pessoal ou dado sensível em `localStorage`, logs ou URL.
- [ ] Guards de rota não são a única proteção: o backend precisa autorizar.

## Testes
- [ ] Componente e serviço novos têm teste do comportamento, não só "should create".
- [ ] Testes com `HttpTestingController` verificam a requisição enviada.
