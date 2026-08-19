# Workloop Spec

**Especificação do Workloop Agêntico** · versão 0.1.0-rc3 (rascunho para revisão) · protocolo AISAC · B2 Tech

> Liberdade dentro do loop, determinismo na costura.

Um **workloop agêntico** é um sistema de dois ou mais loops agênticos que interagem entre si por canais explícitos. Quando todos os participantes estão sob uma mesma autoridade de política (a organização que os criou), o workloop é **governado**: nenhuma interação entre loops e nenhuma ação com efeito externo ocorre sem passar por gate determinístico que impõe as políticas e regras de negócio dessa autoridade. Quando o grafo cruza a fronteira da autoridade, o workloop é **aberto** e valem regras defensivas.

*An agentic workloop is a system of two or more agentic loops interacting through explicit channels under one policy authority, where every inter-loop interaction and every externally effecting action passes through a deterministic gate enforcing that authority's business rules. English abstract inside the spec.*

| | |
|---|---|
| Texto normativo | [`SPEC.md`](SPEC.md) |
| Página canônica | https://workloop.b2tech.io  |
| DOI | *pendente (Zenodo)* |
| Licença | [CC BY 4.0](LICENSE) |
| Mudanças | [`CHANGELOG.md`](CHANGELOG.md) |
| Como citar | [`CITATION.cff`](CITATION.cff) |

## Status

Rascunho para comentários (*Request for Comments*). Abra uma issue para propor mudanças em definições, invariante, corolários ou requisitos. Ao chegar a `0.1.0`, o texto congela e passa a seguir SemVer (ver seção 13 do spec).

## Nome

"Workloop" e "workloop agêntico" são termos do protocolo AISAC (Bruno Bracaioli / B2 Tech). Use livremente, com atribuição a esta especificação. Não há marca registrada sobre o termo.

## Como citar

Bracaioli, B. (2026). *Workloop Spec: Especificação do Workloop Agêntico* (versão 0.1.0). B2 Tech / protocolo AISAC. DOI: pendente. https://workloop.b2tech.io

## Licenças

Texto da especificação: CC BY 4.0 (arquivo `LICENSE`). Script `build.py`: MIT (cabeçalho SPDX).

## Gerar a página

```bash
pip install markdown
python3 build.py   # escreve docs/index.html a partir de SPEC.md
```

`SPEC.md` é a fonte de verdade; `docs/index.html` é gerado.
