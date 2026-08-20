# Workloop Spec

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22004648.svg)](https://doi.org/10.5281/zenodo.22004648)

**Especificação do Workloop Agêntico** · versão 0.1.0-rc5 (rascunho para revisão) · protocolo AISAC · B2 Tech

> Autonomia probabilística para pensar. Governança determinística para agir.
>
> Invariante: liberdade dentro do loop, gate determinístico em toda interface.

Um **workloop agêntico** é um sistema de dois ou mais loops agênticos que interagem entre si por canais explícitos. Quando todos os participantes estão sob uma mesma autoridade de política (a organização que os criou), o workloop é **governado**: nenhuma interação entre loops e nenhuma ação com efeito externo ocorre sem passar por gate determinístico que impõe as políticas e regras de negócio dessa autoridade. Quando o grafo cruza a fronteira da autoridade, o workloop é **aberto** e valem regras defensivas.

| | |
|---|---|
| Texto normativo | [`SPEC.md`](SPEC.md) |
| Página canônica | https://workloop.b2tech.io |
| Versão em inglês | [`SPEC.en.md`](SPEC.en.md) · [página padrão](https://workloop.b2tech.io) |
| DOI | [10.5281/zenodo.22004648](https://doi.org/10.5281/zenodo.22004648) |
| Licença | [CC BY 4.0](LICENSE) |
| Mudanças | [`CHANGELOG.md`](CHANGELOG.md) |
| Como citar | [`CITATION.cff`](CITATION.cff) |

## Status

Rascunho para comentários (*Request for Comments*). Abra uma issue para propor mudanças em definições, invariante, corolários ou requisitos. Ao chegar a `0.1.0`, o texto congela e passa a seguir SemVer (ver seção 13 do spec).

## Nome

"Workloop" e "workloop agêntico" são termos do protocolo AISAC (Bruno Bracaioli / B2 Tech). Use livremente, com atribuição a esta especificação. Não há marca registrada sobre o termo.

## Como citar

Bracaioli, B. (2026). *Workloop Spec: Especificação do Workloop Agêntico* (versão 0.1.0). B2 Tech / protocolo AISAC. DOI: 10.5281/zenodo.22004648. https://workloop.b2tech.io

## Licenças

Texto da especificação: CC BY 4.0 (arquivo `LICENSE`). Script `build.py`: MIT (cabeçalho SPDX).

## Gerar as páginas

```bash
pip install markdown
python3 build.py   # escreve docs/index.html (EN) e docs/pt-br.html (pt-BR)
```

`SPEC.en.md` é a fonte padrão em inglês. `SPEC.md` permanece como a fonte da versão pt-BR.
